from flask import Flask, render_template, jsonify, request, send_file
from ping_checker import IPPingChecker
from scheduler import AutomatedPingScheduler
import os
import threading
import schedule
import time
from datetime import datetime

app = Flask(__name__)

# Excel dosyası yolu
workdir = os.getenv('WORKDIR', '/app/data')
excel_filename = os.getenv('EXCEL_FILENAME', 'IP_Ping_Sonuclari.xlsx')
excel_file = os.path.join(workdir, excel_filename)

# Scheduler instance
scheduler_instance = None
scheduler_thread = None

def init_scheduler():
    """Scheduler'ı başlat"""
    global scheduler_instance
    scheduler_instance = AutomatedPingScheduler(excel_file)
    scheduler_instance.schedule_weekly(day_of_week="monday", hour=9, minute=0)
    
    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    global scheduler_thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Sistem durumunu döndür"""
    checker = IPPingChecker(excel_file)
    
    # Excel dosyasını yükle
    if not checker.load_workbook():
        return jsonify({
            'error': 'Excel dosyası bulunamadı',
            'file_exists': False
        }), 404
    
    # IP listesini al
    ip_list = []
    row_num = 2
    while row_num <= checker.ws.max_row:
        ip_cell = checker.ws[f'A{row_num}']
        if not ip_cell.value:
            break
        
        ip_address = str(ip_cell.value).strip()
        ping_cell = checker.ws[f'B{row_num}']
        time_cell = checker.ws[f'C{row_num}']
        device_cell = checker.ws[f'D{row_num}']
        
        ip_list.append({
            'ip': ip_address,
            'status': ping_cell.value or 'Bilinmiyor',
            'response_time': time_cell.value or '-',
            'device_name': device_cell.value or '-'
        })
        row_num += 1
    
    # İstatistikler
    stats = {
        'total': len(ip_list),
        'success': sum(1 for ip in ip_list if ip['status'] == 'Yanıt Var'),
        'failed': sum(1 for ip in ip_list if ip['status'] == 'Yanıt Yok')
    }
    
    return jsonify({
        'file_exists': True,
        'ip_list': ip_list,
        'stats': stats,
        'last_update': datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    })

@app.route('/api/add-ips', methods=['POST'])
def add_ips():
    """IP adreslerini Excel dosyasına ekle"""
    try:
        data = request.get_json()
        ip_text = data.get('ips', '').strip()
        
        if not ip_text:
            return jsonify({
                'success': False,
                'message': 'IP adresleri boş olamaz'
            }), 400
        
        # IP'leri parse et (satır satır, virgülle veya boşlukla ayrılmış)
        ip_lines = ip_text.split('\n')
        ip_list = []
        
        # Geçici checker oluştur (sadece IP validasyonu için)
        temp_checker = IPPingChecker(excel_file)
        
        for line in ip_lines:
            line = line.strip()
            if not line:
                continue
            
            # Virgül veya boşlukla ayrılmış IP'leri ayır
            ips_in_line = line.replace(',', ' ').split()
            for ip in ips_in_line:
                ip = ip.strip()
                if ip and temp_checker._is_valid_ip(ip):
                    ip_list.append(ip)
        
        if not ip_list:
            return jsonify({
                'success': False,
                'message': 'Geçerli IP adresi bulunamadı'
            }), 400
        
        # Excel dosyasını yükle veya oluştur
        checker = IPPingChecker(excel_file)
        checker.create_sample_file()
        
        if not checker.load_workbook():
            return jsonify({
                'success': False,
                'message': 'Excel dosyası yüklenemedi'
            }), 500
        
        # Mevcut IP'leri kontrol et (tekrar ekleme)
        existing_ips = set()
        row_num = 2
        while row_num <= checker.ws.max_row:
            ip_cell = checker.ws[f'A{row_num}']
            if ip_cell.value:
                existing_ips.add(str(ip_cell.value).strip())
            row_num += 1
        
        # Yeni IP'leri ekle
        new_ips = []
        for ip in ip_list:
            if ip not in existing_ips:
                new_ips.append(ip)
                row_num = checker.ws.max_row + 1
                checker.ws[f'A{row_num}'] = ip
                existing_ips.add(ip)
        
        # Dosyayı kaydet
        checker.wb.save(excel_file)
        
        return jsonify({
            'success': True,
            'message': f'{len(new_ips)} yeni IP adresi eklendi',
            'added_count': len(new_ips),
            'total_count': len(existing_ips)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Hata: {str(e)}'
        }), 500

@app.route('/api/ping', methods=['POST'])
def run_ping():
    """Manuel ping kontrolü başlat"""
    try:
        checker = IPPingChecker(excel_file)
        
        # Dosya yoksa oluştur
        checker.create_sample_file()
        
        # Ping kontrolü yap
        if checker.run_ping_check():
            checker.create_charts()
            
            return jsonify({
                'success': True,
                'message': 'Ping kontrolü tamamlandı'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Ping kontrolü başarısız oldu'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Hata: {str(e)}'
        }), 500

@app.route('/api/clear-ips', methods=['POST'])
def clear_ips():
    """Tüm IP adreslerini temizle (sadece başlıkları bırak)"""
    try:
        checker = IPPingChecker(excel_file)
        
        # Dosya yoksa oluştur
        checker.create_sample_file()
        
        if not checker.load_workbook():
            return jsonify({
                'success': False,
                'message': 'Excel dosyası yüklenemedi'
            }), 500
        
        # Tüm veri satırlarını sil (satır 2'den itibaren)
        max_row = checker.ws.max_row
        deleted_count = 0
        
        for row_num in range(max_row, 1, -1):  # Geriye doğru sil
            ip_cell = checker.ws[f'A{row_num}']
            if ip_cell.value:  # Eğer IP varsa
                # Tüm satırı temizle
                for col in ['A', 'B', 'C', 'D']:
                    cell = checker.ws[f'{col}{row_num}']
                    cell.value = None
                    cell.fill = None
                    cell.font = None
                    cell.alignment = None
                deleted_count += 1
        
        # Dosyayı kaydet
        checker.wb.save(excel_file)
        
        return jsonify({
            'success': True,
            'message': f'{deleted_count} IP adresi temizlendi',
            'deleted_count': deleted_count
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Hata: {str(e)}'
        }), 500

@app.route('/api/download')
def download_excel():
    """Excel dosyasını indir"""
    try:
        if os.path.exists(excel_file):
            return send_file(excel_file, as_attachment=True, 
                           download_name=excel_filename)
        else:
            return jsonify({'error': 'Dosya bulunamadı'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scheduler/status')
def scheduler_status():
    """Zamanlayıcı durumunu döndür"""
    jobs = []
    for job in schedule.jobs:
        jobs.append({
            'next_run': job.next_run.strftime('%d.%m.%Y %H:%M:%S') if job.next_run else 'Bilinmiyor',
            'interval': str(job.interval) if hasattr(job, 'interval') else 'N/A'
        })
    
    return jsonify({
        'active': len(schedule.jobs) > 0,
        'jobs': jobs,
        'jobs_count': len(schedule.jobs)
    })

if __name__ == '__main__':
    # Scheduler'ı başlat
    init_scheduler()
    
    # Flask uygulamasını başlat
    app.run(host='0.0.0.0', port=5000, debug=False)



import schedule
import time
from datetime import datetime
from ping_checker import IPPingChecker

class AutomatedPingScheduler:
    def __init__(self, excel_file):
        self.excel_file = excel_file
        self.checker = IPPingChecker(excel_file)
    
    def run_ping_job(self):
        """Ping işini çalıştır"""
        print(f"\n{'='*60}")
        print(f"⏰ Otomatik Ping Kontrolü Başladı: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        print(f"{'='*60}")
        
        if self.checker.run_ping_check():
            self.checker.create_charts()
            self.checker.show_summary()
        else:
            print("✗ Ping kontrolü başarısız oldu!")
    
    def schedule_weekly(self, day_of_week="monday", hour=9, minute=0):
        """Haftalık zamanlama
        
        Parametreler:
        - day_of_week: "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"
        - hour: Saat (0-23)
        - minute: Dakika (0-59)
        """
        schedule_str = f"{day_of_week.capitalize()} {hour:02d}:{minute:02d}"
        
        if day_of_week.lower() == "monday":
            schedule.every().monday.at(f"{hour:02d}:{minute:02d}").do(self.run_ping_job)
        elif day_of_week.lower() == "tuesday":
            schedule.every().tuesday.at(f"{hour:02d}:{minute:02d}").do(self.run_ping_job)
        elif day_of_week.lower() == "wednesday":
            schedule.every().wednesday.at(f"{hour:02d}:{minute:02d}").do(self.run_ping_job)
        elif day_of_week.lower() == "thursday":
            schedule.every().thursday.at(f"{hour:02d}:{minute:02d}").do(self.run_ping_job)
        elif day_of_week.lower() == "friday":
            schedule.every().friday.at(f"{hour:02d}:{minute:02d}").do(self.run_ping_job)
        elif day_of_week.lower() == "saturday":
            schedule.every().saturday.at(f"{hour:02d}:{minute:02d}").do(self.run_ping_job)
        elif day_of_week.lower() == "sunday":
            schedule.every().sunday.at(f"{hour:02d}:{minute:02d}").do(self.run_ping_job)
        
        print(f"✓ Haftalık zamanlama ayarlandı: Her {schedule_str}")
    
    def schedule_daily(self, hour=9, minute=0):
        """Günlük zamanlama"""
        schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(self.run_ping_job)
        print(f"✓ Günlük zamanlama ayarlandı: Her gün {hour:02d}:{minute:02d}")
    
    def schedule_interval(self, hours=0, minutes=30):
        """Belirli aralıklarla zamanlama (saat ve dakika)"""
        if hours > 0:
            schedule.every(hours).hours.do(self.run_ping_job)
            print(f"✓ {hours} saatlik aralıkla zamanlama ayarlandı")
        elif minutes > 0:
            schedule.every(minutes).minutes.do(self.run_ping_job)
            print(f"✓ {minutes} dakikalık aralıkla zamanlama ayarlandı")
    
    def start_scheduler(self):
        """Zamanlayıcıyı başlat (arka planda çalışır)"""
        print("\n🚀 Zamanlayıcı başlatıldı. Ctrl+C ile durdurun...\n")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Her 60 saniyede bir kontrol et
        except KeyboardInterrupt:
            print("\n\n⏹ Zamanlayıcı durduruldu.")


def main():
    import os
    # Excel dosyası yolu - environment variable'dan al veya varsayılan kullan
    workdir = os.getenv('WORKDIR', '/app/data')
    excel_filename = os.getenv('EXCEL_FILENAME', 'IP_Ping_Sonuclari.xlsx')
    excel_file = os.path.join(workdir, excel_filename)
    scheduler = AutomatedPingScheduler(excel_file)
    
    # ZAMANLAMA SEÇENEKLERI (Aşağıdakilerden birini kullanabilirsiniz):
    
    # Seçenek 1: Her Pazartesi saat 09:00'da çalışır
    scheduler.schedule_weekly(day_of_week="monday", hour=9, minute=0)
    
    # Seçenek 2: Her gün saat 09:00'da çalışır (Seçenek 1'i devre dışı bıraktıktan sonra kullanın)
    # scheduler.schedule_daily(hour=9, minute=0)
    
    # Seçenek 3: Her 6 saatte bir çalışır (Seçenek 1'i devre dışı bıraktıktan sonra kullanın)
    # scheduler.schedule_interval(hours=6)
    
    # Seçenek 4: Her 30 dakikada bir çalışır (Seçenek 1'i devre dışı bıraktıktan sonra kullanın)
    # scheduler.schedule_interval(minutes=30)
    
    # Zamanlayıcıyı başlat
    scheduler.start_scheduler()


if __name__ == "__main__":
    main()

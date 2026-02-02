import psutil
import csv
import time
import random
from datetime import datetime

def get_metrics():
    partitions = psutil.disk_partitions()
    data = []
    
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            
            # Force 15% outliers
            if random.random() < 0.15:
                status = "Outlier"
                used_gb = random.uniform(381.47, usage.total / (1024**3))  # Values above threshold
                free_gb = (usage.total / (1024**3)) - used_gb
                percent = (used_gb / (usage.total / (1024**3))) * 100
            else:
                used_gb = round(usage.used / (1024**3), 2)
                free_gb = round(usage.free / (1024**3), 2)
                percent = round(usage.percent, 2)
                status = "Outlier" if percent > 80 else "Normal"
            
            data.append([
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                partition.device,
                partition.mountpoint,
                partition.fstype,
                round(usage.total / (1024**3), 2),
                used_gb,
                free_gb,
                percent,
                status
            ])
            
        except Exception as e:
            print(f"Error in {partition.mountpoint}: {str(e)}")
    
    return data

def save_data():
    while True:
        with open('disk_data.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow([
                    'Timestamp', 'Device', 'Mountpoint', 'Filesystem',
                    'Total_GB', 'Used_GB', 'Free_GB', 'Usage_Percent', 'Usage_Status'
                ])
            writer.writerows(get_metrics())
        
        time.sleep(5)  # 5 second interval

if __name__ == "__main__":
    save_data()
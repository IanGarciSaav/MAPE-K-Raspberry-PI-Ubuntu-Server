import psutil
import csv
import time
import random
from datetime import datetime

def get_disk_usage():
    partitions = psutil.disk_partitions()
    data = []
    
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            
            # Simulate base variation
            simulated_variation = random.uniform(-10, 10)
            adjusted_percent = max(0, min(100, usage.percent + simulated_variation))
            
            # Force 15% outliers
            if random.random() < 0.15:  # 15% probability
                usage_status = "Outlier"
                # Ensure coherent values for outliers (80-100%)
                adjusted_percent = random.uniform(80.1, 100.0)
                used_gb = usage.total * (adjusted_percent/100) / (1024**3)
                free_gb = (usage.total - (usage.total * (adjusted_percent/100))) / (1024**3)
            else:
                usage_status = "Outlier" if adjusted_percent > 80 else "Normal"
                used_gb = usage.used / (1024**3)
                free_gb = usage.free / (1024**3)
            
            data.append([
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                partition.device,
                partition.mountpoint,
                partition.fstype,
                round(usage.total / (1024**3), 2),  # Total en GB
                round(used_gb, 2),                   # Used GB ajustado
                round(free_gb, 2),                   # Free GB ajustado
                round(adjusted_percent, 2),
                usage_status
            ])
        except Exception as e:
            print(f"Error en {partition.mountpoint}: {str(e)}")
            continue
    
    return data

def save_to_csv(filename='disk_usage.csv'):
    headers = [
        'Timestamp', 'Device', 'Mountpoint', 'Filesystem',
        'Total_GB', 'Used_GB', 'Free_GB', 'Usage_Percent', 'Usage_Status'
    ]
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        
        for _ in range(100):  # 100 muestras para mejor distribución
            data = get_disk_usage()
            if data:
                writer.writerows(data)
            time.sleep(1)  # Intervalo más corto para variedad
        
    print(f"\n✅ Dataset with 15% outliers generated: {filename}")

if __name__ == "__main__":
    save_to_csv()
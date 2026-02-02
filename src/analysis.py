import csv
import configparser
import time

def load_rules():
    config = configparser.ConfigParser()
    config.read('config_rules.txt')
    return {
        'threshold_gb': float(config['Rules']['outlier_threshold_gb']),
        'threshold_percent': float(config['Rules']['outlier_threshold_percent'])
    }

def analyze_data():
    rules = load_rules()
    
    with open('disk_data.csv', 'r') as input_file, open('analysis.csv', 'w', newline='') as output_file:
        reader = csv.DictReader(input_file)
        writer = csv.writer(output_file)
        writer.writerow(['Timestamp', 'Device', 'Status_GB', 'Status_Percent', 'Action'])
        
        for row in reader:
            status_gb = "Outlier" if float(row['Used_GB']) >= rules['threshold_gb'] else "Normal"
            status_percent = "Outlier" if float(row['Usage_Percent']) >= rules['threshold_percent'] else "Normal"
            action = "ALERT" if "Outlier" in [status_gb, status_percent] else "OK"
            
            writer.writerow([
                row['Timestamp'],
                row['Device'],
                status_gb,
                status_percent,
                action
            ])

if __name__ == "__main__":
    while True:
        analyze_data()
        time.sleep(5)
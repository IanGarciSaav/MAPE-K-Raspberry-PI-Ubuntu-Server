import csv
import time

def schedule():
    actions = []
    
    with open('analysis.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Action'] == "ALERT":
                action = {
                    'timestamp': row['Timestamp'],
                    'device': row['Device'],
                    'action': "CLEAN_DISK" if float(row['Status_Percent']) > 80 else "NOTIFY"
                }
                actions.append(action)
    
    with open('actions.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['timestamp', 'device', 'action'])
        writer.writeheader()
        writer.writerows(actions)

if __name__ == "__main__":
    while True:
        schedule()
        time.sleep(5)
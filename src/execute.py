import csv
import time

def execute_actions():
    while True:
        try:
            with open('actions.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    print(f"[{row['timestamp']}] {row['device']} - {row['action']}")
                    
            time.sleep(5)
        except FileNotFoundError:
            print("Waiting for actions...")
            time.sleep(5)

if __name__ == "__main__":
    execute_actions()
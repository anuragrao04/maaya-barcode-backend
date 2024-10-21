import csv
import requests

# URL for the POST request
url = 'http://localhost:6969/create'

with open('./student-deets.csv', 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        data = {
            'srn': row['SRN'],
            'prn': row['PRN'],
            'name': row['Student Name'],
            'semester': row['Sem'],
            'branch': row['Branch']
        }

        response = requests.post(url, json=data)

        if response.status_code == 200:
            print(f"{data['name']} registered")
        else:
            print(f"fucked up for {data['name']}: {response.message}")

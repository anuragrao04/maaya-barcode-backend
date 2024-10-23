import csv
import requests
from concurrent.futures import ThreadPoolExecutor

# URL for the POST request
url = 'https://barcode.maaya-pes.co/create'


def register_student(data):
    response = requests.post(url, json=data)

    if response.status_code != 200:
        print(f"Registration failed for {data['name']}: {response.text}")


with open('./student-deets.csv', 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)

    student_data = [{
        'srn': row['SRN'],
        'prn': row['PRN'],
        'name': row['Student Name'],
        'semester': row['Sem'],
        'branch': row['Branch']
    } for row in reader]

with ThreadPoolExecutor(max_workers=8) as executor:
    executor.map(register_student, student_data)

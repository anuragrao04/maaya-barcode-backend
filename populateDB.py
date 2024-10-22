import csv
import requests

# URL for the POST request
url = 'https://qr.ad-chaos.live/create'

with open('./student-deets.csv', 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        srn = row['SRN/PRN']
        prn = row['SRN/PRN']

        srn_regex = r"^PES2UG\d{2}[A-Za-z]{2}\d{3}$"
        prn_is_srn = re.match(regex, prn)

        if (prn_is_srn):
            prn = getPrnFromSrn(srn)

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

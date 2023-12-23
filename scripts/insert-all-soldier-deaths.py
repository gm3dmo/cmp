
def run():

    import sys
    import urllib3
    import csv
    from cmp.models import SoldierDeath
    from cmp.models import Company

    print()
    title = sys.argv[2]
    print(f"""\033[4;33m{title}\033[0m""")
    print("-" * len(title))
    
    ref_data_url = "https://raw.githubusercontent.com/gm3dmo/old-cmp/main/data/soldier-death.csv"
    http = urllib3.PoolManager()
    r = http.request('GET', ref_data_url)
    print(f"""Fetch table response code: {r.status}""")
    # load the response into a csv dictionary reader
    reader = csv.DictReader(r.data.decode('utf-8').splitlines())
    
    # add a country model for each row in the csv file
    for row in reader:
        #print(f"""row: ({row['id']}) cwgc:({row['cwgc_id']})""")
        try:
            company = Company.objects.filter(name=row['company_id']) 
            if company:
                company = company.first()
            else:
                #print(f"""row: ({row['id']}) cwgc:({row['cwgc_id']})""")
                company = Company.objects.filter(name="UNKNOWN").first()
            cwgc_id = row.get('cwgc_id', 90909) if row.get('cwgc_id') != '' else 90909
            SoldierDeath.objects.create(
                #id=int(row['id']),
                soldier_id = int(row['soldier_id']),
                date =row['Date'],
                company_id = company.id,
                cemetery_id = row['cemetery_id'],
                cwgc_id = cwgc_id
        )
        except Exception as e:
            print(f"""💥row: ({row['id']}) cwgc:({row['cwgc_id']}) company:({row['company_id']}) cemetery:({row['cemetery_id']})""")
            raise e

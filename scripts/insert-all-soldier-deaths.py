
def run():

    from pathlib import Path
    import environ
    import os
    import sys
    import urllib3
    import csv
    import time
    from cmp.models import SoldierDeath
    from cmp.models import Company

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

    env = environ.Env(
    DEBUG=(bool, False)
    )

    github_token= str(f"{env('READ_PAT')}")

    print()
    title = sys.argv[2]

    headers = {
       'Accept': 'application/vnd.github.v3.raw',
       'Authorization': f'Bearer {github_token}'
    }

    print()
    title = sys.argv[2]
    
    start_fetch_time = time.time()
    ref_data_url = "https://api.github.com/repos/gm3dmo/old-cmp/contents/data/soldier-death.csv"
    http = urllib3.PoolManager()
    r = http.request('GET', ref_data_url, headers=headers)
    end_fetch_time = time.time()

    # load the response into a csv dictionary reader
    reader = csv.DictReader(r.data.decode('utf-8').splitlines())
    
    start_insert_time = time.time()
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

    end_insert_time = time.time()
    time_to_fetch = end_fetch_time - start_fetch_time
    time_to_insert = end_insert_time - start_insert_time
    print(f"""\033[4;33m{title}\033[0m Fetch table response code: {r.status} time (seconds) to fetch: {time_to_fetch:.2f} time to insert {time_to_insert:.2f}""")

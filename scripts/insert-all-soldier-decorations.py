
def run():

    from pathlib import Path
    import environ
    import os
    import sys
    import urllib3
    import csv
    import time

    from cmp.models import SoldierDecoration
    from cmp.models import Company
    from cmp.models import Country
    from cmp.models import Soldier


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

    start_fetch_time = time.time()
    ref_data_url = "https://api.github.com/repos/gm3dmo/old-cmp/contents/data/soldier-decoration-utf-8.csv"

    http = urllib3.PoolManager()
    r = http.request('GET', ref_data_url, headers=headers)
    end_fetch_time = time.time()
    # load the response into a csv dictionary reader
    reader = csv.DictReader(r.data.decode('ISO-8859-1').splitlines())
    
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
            country = Country.objects.filter(name=row['country_id'])
            if country:
                country = country.first()
            else:
                country = Country.objects.filter(name="UNKNOWN").first()
            gazette_date = row.get('gazetteDate', None)
            if gazette_date == "":
                gazette_date = None
                
            if int(row.get("id")) == 384:
                print(f"""row: {row}""")
                breakpoint()

            SoldierDecoration.objects.create(
                #id,soldier_id,company_id,decoration_id,gazetteIssue,gazettePage,gazetteDate,citation,notes,country_id
                # create the model
                id = int(row['id']),
                #soldier = soldier
                soldier_id = int(row['soldier_id']),
                company_id  = company.id,
                decoration_id = int(row['decoration_id']),
                gazette_issue = row['gazetteIssue'],
                gazette_page = row['gazettePage'],
                gazette_date = gazette_date,
                citation = row['citation'],
                notes = row['notes'],
                country_id = country.id
        )
        except Exception as e:
            print(f"""💥row: {row}""")
            raise e

    end_insert_time = time.time()
    time_to_fetch = end_fetch_time - start_fetch_time
    time_to_insert = end_insert_time - start_insert_time
    print(f"""\033[4;33m{title}\033[0m Fetch table response code: {r.status} time (seconds) to fetch: {time_to_fetch:.2f} time to insert {time_to_insert:.2f}""")

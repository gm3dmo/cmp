
def run():


    from pathlib import Path
    import environ
    import os
    import sys
    import urllib3
    import csv
    import time
    from cmp.models import Country

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
    ref_data_url = "https://api.github.com/repos/gm3dmo/old-cmp/contents/data/country.csv"
    http = urllib3.PoolManager()
    r = http.request('GET', ref_data_url, headers=headers)
    end_fetch_time = time.time()
    # load the response into a csv dictionary reader
    reader = csv.DictReader(r.data.decode('utf-8').splitlines())
    
    start_insert_time = time.time()
    for row in reader:
        try:
            Country.objects.create(
                id = row['id'],
                name = row['Name'],
                alpha2 = row['Alpha2'],
                alpha3 = row['Alpha3'],
                country_number = row['CountryNumber'],
                flag = ""
        )
        except Exception as e:
            print("Error with: " + row['Name'])
            raise e

    end_insert_time = time.time()
    time_to_fetch = end_fetch_time - start_fetch_time
    time_to_insert = end_insert_time - start_insert_time
    print(f"""\033[4;33m{title}\033[0m Fetch table response code: {r.status} time (seconds) to fetch: {time_to_fetch:.2f} time to insert {time_to_insert:.2f}""")

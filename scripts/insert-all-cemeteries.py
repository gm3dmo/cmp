
def run():

    import sys
    import urllib3
    import csv
    import time
    from cmp.models import Cemetery

    print()
    title = sys.argv[2]

    start_fetch_time = time.time()
    ref_data_url = "https://raw.githubusercontent.com/gm3dmo/old-cmp/main/data/cemetery.csv"
    http = urllib3.PoolManager()
    r = http.request('GET', ref_data_url)
    end_fetch_time = time.time()
    # load the response into a csv dictionary reader
    reader = csv.DictReader(r.data.decode('utf-8').splitlines())
    reader.fieldnames = [field.replace('.', '_') for field in reader.fieldnames]
    
    # add a country model for each row in the csv file
    start_insert_time = time.time()
    for row in reader:
        if row['latitude'] == '':
            row['latitude'] = 0 
        if row['longitude'] == '':
            row['longitude'] = 0
        try:
            Cemetery.objects.create(
                id=row['id'],
                name=row['name'],
                country_id=row['ccn3'],
                latitude=row['latitude'],
                longitude=row['longitude']
        )
        except Exception as e:
            print(f"""💥row: ({row}) """)
            raise e

    end_insert_time = time.time()
    time_to_fetch = end_fetch_time - start_fetch_time
    time_to_insert = end_insert_time - start_insert_time
    print(f"""\033[4;33m{title}\033[0m Fetch table response code: {r.status} time (seconds) to fetch: {time_to_fetch:.2f} time to insert {time_to_insert:.2f}""")

def run():

    import sys
    import urllib3
    import csv
    from cmp.models import Rank

    print()
    title = sys.argv[2]
    print(f"""\033[4;33m{title}\033[0m""")
    print("-" * len(title))
    
    ref_data_url = "https://raw.githubusercontent.com/gm3dmo/old-cmp/main/data/rank.csv"
    http = urllib3.PoolManager()
    r = http.request('GET', ref_data_url)
    print(f"""Fetch table response code: {r.status}""")
    # load the response into a csv dictionary reader
    reader = csv.DictReader(r.data.decode('utf-8').splitlines())
    
    # add a country model for each row in the csv file
    for row in reader:
        #print(row['name'])
        try:
            Rank.objects.create(
                id=row['id'],
                name=row['name'],
                abbreviation=row['abbr'],
                rank_class=row['class']
        )
        except Exception as e:
            print(f"""💥row: ({row}) """)
            raise e

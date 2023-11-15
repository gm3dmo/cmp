
def run():

    import sys
    import urllib3
    import csv
    from cmp.models import SoldierDecoration

    print()
    title = sys.argv[2]
    print(f"""\033[4;33m{title}\033[0m""")
    print("-" * len(title))
    
    ref_data_url = "https://raw.githubusercontent.com/gm3dmo/old-cmp/main/data/soldier-decoration.csv"
    http = urllib3.PoolManager()
    r = http.request('GET', ref_data_url)
    print(r.status)
    # load the response into a csv dictionary reader
    reader = csv.DictReader(r.data.decode('ISO-8859-1').splitlines())
    # breakpoint()
    print(reader) 
    # id,soldier_id,company_id,decoration_id,gazetteIssue,gazettePage,gazetteDate,citation,notes,country_id
    for row in reader:
        print(f"""SoldierDecoration: {row['id']} {row['soldier_id']} """)
        try:
            SoldierDecoration.objects.create(
                id = row['id'],
                name = row['name'],
                notes = row['notes'],
                country_id = row['country_id'],
                details_link = row['details_link'],
                abbreviation = row['abbreviation']
        )
        except Exception as e:
            print("Error with: " + row['id'])

            raise e

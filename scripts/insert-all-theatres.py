
def run():

    import sys
    import urllib3
    import csv
    from cmp.models import Theatre

    print()
    title = sys.argv[2]
    print(f"""\033[4;33m{title}\033[0m""")
    print("-" * len(title))
    
    ref_data_url = "https://raw.githubusercontent.com/gm3dmo/old-cmp/main/data/theatre.csv"
    http = urllib3.PoolManager()
    r = http.request('GET', ref_data_url)
    print(r.status)
    # load the response into a csv dictionary reader
    reader = csv.DictReader(r.data.decode('utf-8').splitlines())
    
    # add a country model for each row in the csv file
    for row in reader:
        print(row['Name'])
        try:
            Theatre.objects.create(
                id=row['id'],
                name=row['Name']
        )
        except Exception as e:
            print("Error with: " + row['Name'])
            raise e

    for theatre in Theatre.objects.all():
       print(f"""{theatre.id} {theatre.name}""")
    

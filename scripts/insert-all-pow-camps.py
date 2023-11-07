
def run():

    import sys
    import urllib3
    import csv
    from cmp.models import PowCamp
    
    ref_data_url = "https://raw.githubusercontent.com/gm3dmo/old-cmp/main/data/pow-camp.csv"
    http = urllib3.PoolManager()
    r = http.request('GET', ref_data_url)
    print(r.status)
    # load the response into a csv dictionary reader
    reader = csv.DictReader(r.data.decode('utf-8').splitlines())
    
    # add a country model for each row in the csv file
    for row in reader:
        print(f""" {row['id']} {row['Name']} ({row['PresentCountry_id']}) {row['WartimeCountry']} {row['Latitude']} {row['Longitude']}""")
        if int(row["id"]) == 59:
            break
        try:
            PowCamp.objects.create(
                id=row['id'],
                name=row['Name'],
                country_id=row['PresentCountry_id'],
                wartime_country=row['WartimeCountry'],
                latitude=row['Latitude'],
                longitude=row['Longitude']
        )
        except Exception as e:
            print("Error with: " + row['Name'])
            raise e


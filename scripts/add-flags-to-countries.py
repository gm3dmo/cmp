
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
    
    ref_data_url = "https://raw.githubusercontent.com/mledoze/countries/master/dist/countries.csv"
    http = urllib3.PoolManager()
    r = http.request('GET', ref_data_url, headers=headers)
    print(r.status)
    reader = csv.DictReader(r.data.decode('utf-8').splitlines())

    # create a dictionary from the reader with key ccna2 and value flag
    flags = {row['cca2']: row['flag'] for row in reader}

    print(flags['GB'])

    # for every country in the database, add the flag if the country is in the dictionary
    for country in Country.objects.all():
        if country.alpha2 in flags:
            country.flag = flags[country.alpha2]
            country.save()
            print(f"""{country.name} {country.alpha2} {country.flag}""")
        else:
            print(f"""{country.name} {country.alpha2} no flag""")
    


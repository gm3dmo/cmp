# cmp

See current progress:

- [cmp-production.up.railway.app](https://cmp-production.up.railway.app/)
- [Army Number Search Tool](https://cmp-production.up.railway.app/tools/army-number-search)

For configuration [django-environ](https://github.com/joke2k/django-environ) is used.


### Countries
The countries are extracted from this article:

https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes

### Populating the Database
1. It is best to simply delet your db using a command such as `rm db.Squlite2`
2. Run migrations `python manage.py makemigrations`
3. Run the bash script to load and populate the data `bash insertall.sh`

### Test Coverage
[![Coverage Status](https://coveralls.io/repos/github/gm3dmo/cmp/badge.svg?branch=main)](https://coveralls.io/github/gm3dmo/cmp?branch=main)

# Corps of Military Police

## Backups

A script called [db_dump_csv.py](https://github.com/gm3dmo/cmp/blob/main/scripts/db_dump_csv.py) dumps CSV files of the tables for cmp_* and uploads them to [cmp-archive](https://github.com/gm3dmo/cmp-archive) where a release is is created.

The script `db_backup_csv.sh` is called from cron each evening:

```bash
#!/bin/bash

# Path to your project
PROJECT_DIR=/home/azureuser/cmp

# Activate virtual environment
source $PROJECT_DIR/.venv/bin/activate

# Set environment variables if needed
export DJANGO_ENV=production

# Run the script
cd $PROJECT_DIR
python scripts/db_dump_csv.py

# Deactivate virtual environment
deactivate
```

Crontab entry:

```
15 18 * * * /home/azureuser/db_backup_csv.sh > /home/azureuser/logs/db_dump.log 2>&1
```

## Development Notes

For configuration [django-environ](https://github.com/joke2k/django-environ) is used.

### Countries
The countries are extracted from this article:

https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes

### Test Coverage
[![Coverage Status](https://coveralls.io/repos/github/gm3dmo/cmp/badge.svg?branch=main)](https://coveralls.io/github/gm3dmo/cmp?branch=main)


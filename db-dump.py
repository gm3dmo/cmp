import os
import sys
import django
import zipfile
import environ
import logzero
import pathlib
import sqlite3
import io

from datetime import datetime
from pathlib import Path
from logzero import logger

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')  # replace 'myproject.settings' with your settings module
django.setup()


env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)


def main():

    current_date = datetime.now()
    db_filename = 'db.sqlite3'
    db_connfile = f'file:{db_filename}?mode=ro'
    conn = sqlite3.connect(db_connfile, uri=True)


    dump_filename= f"""cmp-{current_date.strftime('%Y-%m-%d-%s')}.dump"""
    db_dump_file = Path(f"""{env('ARCHIVE_DIR')}/db-backups/{dump_filename}""")
    logger.info(f"db_dump_file {db_dump_file}")

    with io.open(db_dump_file, 'w') as p:
        for line in conn.iterdump():
            p.write('%s\n' % line)

    logger.info(f'{db_filename} dumped to {db_dump_file}')

    # Zip the dump file
    zip_filename = db_dump_file.with_suffix('.zip')
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
       zipf.write(db_dump_file, arcname=dump_filename)

    logger.info(f'Dump file: {db_dump_file} zipped to: {zip_filename}')


if __name__ == "__main__":
    main()

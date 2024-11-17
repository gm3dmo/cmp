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

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')  # replace 'myproject.settings' with your settings module
django.setup()


env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)


def main():

    account_url = str(f"{env('ACCOUNT_URL')}")
    container_name = str(f"{env('container_name')}")
    default_credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(account_url, credential=default_credential)

    logger.info(f"storage_account: {account_url}")
    logger.info(f"container_name: {container_name}")
    current_date = datetime.now()
    db_filename = 'db.sqlite3'
    db_connfile = f'file:{db_filename}?mode=ro'
    conn = sqlite3.connect(db_connfile, uri=True)


    dump_filename= f"""cmp-{current_date.strftime('%Y-%m-%d-%s')}.dump"""
    db_dump_file = Path(f"""{env('ARCHIVE_DIR')}/db-backups/{dump_filename}""")
    logger.info(f"db_dump_file: {db_dump_file}")

    with io.open(db_dump_file, 'w') as p:
        for line in conn.iterdump():
            p.write('%s\n' % line)

    logger.info(f'{db_filename} dumped to {db_dump_file}')

    # Zip the dump file
    zip_filename = db_dump_file.with_suffix('.zip')
    blob_filename = Path(zip_filename).name

    zs=str(blob_filename)


    logger.info(f"type of z {type(zip_filename)}")
    logger.info(f"zs: {zs}")
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
       zipf.write(db_dump_file, arcname=dump_filename)

    logger.info(f'Dump file: {db_dump_file} zipped to: {zip_filename}')

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=zs)

    print(f"Uploading to Azure Storage as blob: {blob_filename}")

    with open(file=zip_filename, mode="rb") as data:
        blob_client.upload_blob(data)



if __name__ == "__main__":
    main()


import os
import sys
import django
import zipfile
import environ
import logzero
import pathlib

from pathlib import Path
from logzero import logger

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')  # replace 'myproject.settings' with your settings module
django.setup()


env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

from cmp.models import Soldier
from cmp.models import SoldierDeath

# create a data class for soldiers 

class SoldierData:
    def __init__(self, surname, initials, army_number, rank, notes):
        self.id = id 
        self.army_number = army_number
        self.photo_in_original = photo_in_original


def main():

    origin_archive = Path(sys.argv[1])
    logger.info(f"origin_archive: {origin_archive}")
    
    target_archive = "/var/tmp/memorial-image-by-soldier-id.zip"
    logger.info(f"target_archive: {target_archive}")
    # createa writeable zip archive called target_archive

    with zipfile.ZipFile(origin_archive, 'r') as zip_ref:
        zip_contents = zip_ref.namelist()
        counter = 0
        for item in zip_contents:
            if item.endswith('.jpg'):
                    filename = os.path.basename(item)
                    filename = pathlib.Path(filename).stem
                    filename = filename.replace("_","/")
                    soldiers = Soldier.objects.filter(army_number=filename)
                    for soldier in soldiers:
                        logger.info(f"filename: {filename}")
                        logger.info(f"item: {item}")
                        logger.info(f"{counter} Soldier: {soldier.army_number} == {filename}")
                        soldier.photo_in_original = True
                        counter += 1
                        new_filename = Path(f"media-prep/{soldier.id}/memorial/{soldier.id}.jpg")
                        directory_path = os.path.dirname(new_filename)
                        os.makedirs(directory_path, exist_ok=True)
                        file_bytes = zip_ref.read(item)
                        logger.info(f"len: {len(file_bytes)}")
                        with open(new_filename, 'wb') as f:
                           f.write(file_bytes)



    with zipfile.ZipFile(target_archive, 'w') as zip_ref:
        for foldername, subfolders, filenames in os.walk('media'):
            for filename in filenames:
                zip_ref.write(os.path.join(foldername, filename))


    logger.info(f"Total number of soldiers: {counter}")
    logger.info(f"new zip archive: {target_archive}")

if __name__ == "__main__":
    main()

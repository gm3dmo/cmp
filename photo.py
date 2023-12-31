import os
import django
import zipfile
import logzero
import pathlib

from logzero import logger


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')  # replace 'myproject.settings' with your settings module
django.setup()

from cmp.models import Soldier
from cmp.models import SoldierDeath

# create a data class for soldiers 

class SoldierData:
    def __init__(self, surname, initials, army_number, rank, notes):
        self.id = id 
        self.army_number = army_number
        self.photo_in_original = photo_in_original


def main():

    origin_archive = '/Users/gm3dmo/src/old-cmp/grave-images-2023-12-31.zip'

    with zipfile.ZipFile(origin_archive, 'r') as zip_ref:
        zip_contents = zip_ref.namelist()
        # create a counter to count the contents of the zip file
        counter = 0
        for item in zip_contents:
            # if the item is a file, extract it
            if item.endswith('.jpg'):
                    filename = os.path.basename(item)
                    filename = pathlib.Path(filename).stem
                    filename = filename.replace("_","/")
                    soldiers = Soldier.objects.filter(army_number=filename)
                    for soldier in soldiers:
                        logger.info(f"{counter} Soldier: {soldier.army_number} == {filename}")
                        soldier.photo_in_original = True
                        counter += 1

if __name__ == "__main__":
    main()
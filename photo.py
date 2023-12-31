import os
import django
import zipfile
import logzero

from logzero import logger


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')  # replace 'myproject.settings' with your settings module
django.setup()

from cmp.models import Soldier  # replace 'myapp' with your app name

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
                    # increment the counter
                    counter += 1
                    logger.info(f"item: {item} counter: {counter}" )

                #zip_ref.extract(item, '/home/gm3dmo/src/old-cmp/grave-images-2023-12-31')   



if __name__ == "__main__":
    main()
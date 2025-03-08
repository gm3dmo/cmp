import os
import sys
import django

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

# Now import the model after Django is configured
from cmp.models import Soldier

# Add at the top of the script for Windows systems
os.system('color')

def find_provost_mentions():
    # Search for "provost officer" in notes field, case insensitive
    soldiers = Soldier.objects.all()
    
    print("Scanning soldiers' notes for 'provost officer' mentions...")
    print("-" * 50)
    
    found_count = 0
    updated_count = 0
    
    for soldier in soldiers:
        if soldier.notes and "provost officer" in soldier.notes.lower():
            found_count += 1
            print(f"\nSoldier: {soldier.surname}, {soldier.initials}")
            print(f"Notes: {soldier.notes}")
            
            # Add this block to set and save the flag
            if not soldier.provost_officer:
                soldier.provost_officer = True
                soldier.save()
                updated_count += 1
                print("Updated: Set provost_officer flag to True")
            else:
                print("Already flagged as provost officer")
                
            print("-" * 50)
    
    print(f"\nFound {found_count} soldiers with 'provost officer' mentions in their notes.")
    print(f"Updated {updated_count} soldier records.")

if __name__ == "__main__":
    find_provost_mentions() 
import os
import csv
import sys
import django
import sqlite3
import requests
import base64
from pathlib import Path
from datetime import datetime
import json

# Add the project root directory to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.conf import settings


# Configuration variables
OUTPUT_DIR = 'csv_dumps'
GITHUB_REPO = 'gm3dmo/cmp-archive'
GITHUB_API_BASE = f'https://api.github.com/repos/{GITHUB_REPO}/contents'

def create_github_release(github_token, files_uploaded):
    """Create a new GitHub release with the date as the tag name."""
    # Generate the release tag and name based on the current date
    today = datetime.now()
    tag_name = today.strftime("v%Y.%m.%d")
    release_name = today.strftime("Database Snapshot %Y-%m-%d")
    
    # Prepare the release body text
    release_body = f"Database snapshot created on {today.strftime('%Y-%m-%d at %H:%M:%S')}\n\n"
    release_body += f"Files updated:\n"
    for file in files_uploaded:
        filename = os.path.basename(file)
        release_body += f"- {filename}\n"
    
    # Prepare the API request
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    release_data = {
        'tag_name': tag_name,
        'name': release_name,
        'body': release_body,
        'draft': False,
        'prerelease': False
    }
    
    github_api_url = f"https://api.github.com/repos/{GITHUB_REPO}/releases"
    
    # Create the release
    response = requests.post(github_api_url, headers=headers, json=release_data)
    
    if response.status_code in [200, 201]:
        print(f"Successfully created release: {release_name}")
        return True
    else:
        print(f"Failed to create release: {response.status_code}, {response.text}")
        return False

def upload_to_github(file_path, github_token):
    """Upload a file to GitHub repository."""
    with open(file_path, 'rb') as file:
        content = file.read()
    
    # Get the filename only, without path
    filename = os.path.basename(file_path)
    
    # Use a direct path without timestamp directory
    github_path = filename  # Upload directly to root
    # Or use a fixed directory like:
    # github_path = f"csv_files/{filename}"
    
    encoded_content = base64.b64encode(content).decode('utf-8')
    
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    github_api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{github_path}"
    
    # Check if file exists
    response = requests.get(github_api_url, headers=headers)
    
    if response.status_code == 200:
        # File exists, get its SHA
        sha = response.json()['sha']
        data = {
            'message': f'Update {github_path} - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
            'content': encoded_content,
            'sha': sha
        }
        response = requests.put(github_api_url, headers=headers, json=data)
    else:
        # File doesn't exist, create it
        data = {
            'message': f'Create {github_path} - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
            'content': encoded_content
        }
        response = requests.put(github_api_url, headers=headers, json=data)
    
    if response.status_code in [200, 201]:
        print(f"Successfully uploaded {filename} to GitHub repository.")
        return True
    else:
        print(f"Failed to upload {filename}: {response.status_code}, {response.text}")
        return False

def dump_tables_to_csv():
    """Dump all tables starting with 'cmp_' to CSV files."""
    created_files = []
    
    try:
        # Connect to the SQLite database
        db_path = settings.DATABASES['default']['NAME']
        print(f"Connecting to database at {db_path}")
        
        # Check if the database file exists
        if not os.path.exists(db_path):
            print(f"Database file not found at {db_path}")
            print(f"Current working directory: {os.getcwd()}")
            print(f"Absolute path to database: {os.path.abspath(db_path)}")
            raise FileNotFoundError(f"Database file not found: {db_path}")
        
        # Try to connect without read-only mode first
        try:
            connection = sqlite3.connect(db_path)
            print("Connected to database successfully")
        except sqlite3.Error as e:
            print(f"Error connecting to database directly: {e}")
            print("Trying read-only mode...")
            # Use read-only mode as fallback
            connection = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
            print("Connected in read-only mode")
        
        cursor = connection.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        all_tables = cursor.fetchall()
        
        # Filter tables that start with 'cmp_'
        tables = [table[0] for table in all_tables if table[0].startswith('cmp_')]
        
        print(f"Found {len(tables)} tables starting with 'cmp_'")
        
        # Dump each table to a CSV file
        for table in tables:
            try:
                cursor.execute(f"SELECT * FROM {table};")
                rows = cursor.fetchall()
                
                # Get column names
                column_names = [description[0] for description in cursor.description]
                
                # Write to CSV
                output_file = os.path.join(OUTPUT_DIR, f"{table}.csv")
                with open(output_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(column_names)
                    writer.writerows(rows)
                
                print(f"Table {table} dumped to {output_file}")
                created_files.append(output_file)
                
            except Exception as e:
                print(f"Error dumping table {table}: {e}")
        
        connection.close()
        
    except Exception as e:
        print(f"Error connecting to database: {e}")
    
    return created_files

def main():
    try:
        # Make sure Django is properly set up
        print(f"Django settings module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
        print(f"Django BASE_DIR: {settings.BASE_DIR}")
        
        # Create output directory if it doesn't exist
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
            print(f"Created output directory: {OUTPUT_DIR}")
        
        # Get all created CSV files
        print("Dumping tables to CSV...")
        created_files = dump_tables_to_csv()
        
        if not created_files:
            print("No files were created. Check the database connection issues above.")
            return
        
        # Check if in production environment
        django_env = os.environ.get('DJANGO_ENV', '')
        print(f"Current environment: {django_env}")
        
        if django_env.startswith('prod'):
            # Get GitHub token from environment variable or Django settings
            github_token = getattr(settings, 'ARCHIVE_TOKEN', None) or os.environ.get('archive_token')
            
            if not github_token:
                print("GitHub token not found. Set ARCHIVE_TOKEN in settings or archive_token in environment.")
            else:
                print(f"Uploading {len(created_files)} files to GitHub repository...")
                
                # Keep track of successfully uploaded files
                uploaded_files = []
                
                # Upload each file
                for file_path in created_files:
                    if upload_to_github(file_path, github_token):
                        uploaded_files.append(file_path)
                
                # Create a GitHub release if files were uploaded
                if uploaded_files:
                    print("Creating GitHub release...")
                    create_github_release(github_token, uploaded_files)
                else:
                    print("No files were uploaded successfully. Skipping release creation.")
        else:
            print("Not in production environment. Skipping GitHub upload.")
        
        print("Database tables successfully dumped to CSV files.")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()


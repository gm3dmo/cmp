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

def dump_tables_to_csv(db_path=None, output_dir=OUTPUT_DIR):
    """
    Opens a SQLite database in read-only mode and dumps all tables 
    starting with 'cmp_' to CSV files.
    
    Args:
        db_path: Path to the SQLite database file
        output_dir: Directory to save CSV files (created if it doesn't exist)
        
    Returns:
        List of paths to created CSV files
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    
    # Connect to the database in read-only mode
    try:
        # URI format with ?mode=ro for read-only
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()
        print(f"Connected to database: {db_path} (read-only mode)")
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)
    
    # Track created files for GitHub upload
    created_files = []
    
    try:
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        all_tables = cursor.fetchall()
        
        # Filter tables that start with 'cmp_'
        cmp_tables = [table[0] for table in all_tables if table[0].startswith('cmp_')]
        
        if not cmp_tables:
            print("No tables found with prefix 'cmp_'")
            return created_files
        
        print(f"Found {len(cmp_tables)} tables with prefix 'cmp_'")
        
        # Process each table
        for table_name in cmp_tables:
            output_file = os.path.join(output_dir, f"{table_name}.csv")
            
            # Get column names
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = [column[1] for column in cursor.fetchall()]
            
            # Get all rows
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()
            
            # Write to CSV
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                # Write header
                csv_writer.writerow(columns)
                # Write data
                csv_writer.writerows(rows)
            
            print(f"Exported {len(rows)} rows from {table_name} to {output_file}")
            created_files.append(output_file)
    
    except sqlite3.Error as e:
        print(f"Error processing database: {e}")
    
    finally:
        cursor.close()
        conn.close()
        print("Database connection closed")
        
    return created_files

if __name__ == "__main__":
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        
        # Get all created CSV files
        created_files = dump_tables_to_csv()
        
        # Check if in production environment
        if os.environ.get('DJANGO_ENV', '').startswith('prod'):
            # Get GitHub token from environment variable
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
        
        print("Database tables successfully dumped to CSV files.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


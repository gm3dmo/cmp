import os
import csv
import sys
import django
import sqlite3
import requests
import base64
from pathlib import Path
from datetime import datetime

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

def upload_to_github(file_path, github_path):
    """
    Upload a file to GitHub repository using GitHub API
    
    Args:
        file_path: Local path to the file
        github_path: Path in the GitHub repository
    """
    # Get GitHub token from Django settings
    github_token = getattr(settings, 'ARCHIVE_TOKEN', None)
    
    # If not in settings, try environment variable as fallback
    if not github_token:
        github_token = os.environ.get('archive_token')
    
    if not github_token:
        print("Error: 'ARCHIVE_TOKEN' not found in Django settings or as environment variable")
        return False
    
    # Read file content
    with open(file_path, 'rb') as file:
        content = file.read()
    
    # Encode content to base64
    content_encoded = base64.b64encode(content).decode('utf-8')
    
    # Prepare API request
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Check if file already exists
    check_url = f'{GITHUB_API_BASE}/{github_path}'
    response = requests.get(check_url, headers=headers)
    
    # Prepare the request data
    data = {
        'message': f'Update {github_path} - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        'content': content_encoded,
    }
    
    # If file exists, we need the SHA to update it
    if response.status_code == 200:
        data['sha'] = response.json()['sha']
        print(f"Updating existing file: {github_path}")
    else:
        print(f"Creating new file: {github_path}")
    
    # Make the API request to create/update the file
    response = requests.put(check_url, headers=headers, json=data)
    
    if response.status_code in [200, 201]:
        print(f"Successfully uploaded {file_path} to GitHub as {github_path}")
        return True
    else:
        print(f"Failed to upload {file_path} to GitHub. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def dump_tables_to_csv(db_path, output_dir=OUTPUT_DIR):
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
    # Get database path from command line or use default
    db_path = sys.argv[1] if len(sys.argv) > 1 else "db.sqlite3"
    
    # Get output directory from command line or use default
    output_dir = sys.argv[2] if len(sys.argv) > 2 else OUTPUT_DIR
    
    # Dump tables to CSV
    created_files = dump_tables_to_csv(db_path, output_dir)
    print("CSV dump completed")
    
    # Check if we're in production environment
    env = os.environ.get('DJANGO_ENV', '').lower()
    if env.startswith('prod'):
        print("Production environment detected. Uploading files to GitHub...")
        
        # Create a timestamp-based directory in GitHub
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        github_dir = f"backups/{timestamp}"
        
        # Upload each file to GitHub
        for file_path in created_files:
            file_name = os.path.basename(file_path)
            github_path = f"{github_dir}/{file_name}"
            upload_to_github(file_path, github_path)
        
        print("GitHub upload completed")


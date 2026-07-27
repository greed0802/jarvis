#!/usr/bin/env python3
import os
import csv
from datetime import datetime
import hashlib

def get_file_info(file_path, doc_id):
    """Get file information including size, dates, and extension"""
    try:
        # Get file stats
        stat = os.stat(file_path)

        # Get file size in bytes
        file_size = stat.st_size

        # Get created and modified dates
        created_date = datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
        modified_date = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')

        # Get file extension
        _, ext = os.path.splitext(file_path)
        ext = ext.lower() if ext else ''

        # Get filename
        filename = os.path.basename(file_path)

        # Determine category based on path
        category, confidence, suggested_destination = determine_category(file_path)

        return {
            'Document_ID': doc_id,
            'Original_Path': file_path,
            'Filename': filename,
            'Extension': ext,
            'File_Size': file_size,
            'Created_Date': created_date,
            'Modified_Date': modified_date,
            'Detected_Category': category,
            'Confidence': confidence,
            'Suggested_Destination': suggested_destination
        }
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def determine_category(file_path):
    """Determine the category of a file based on its path"""
    path_lower = file_path.lower()

    # Check for specific categories
    if 'anzsmm' in path_lower:
        return 'ANZSMM', 'High', 'knowledge/sources/anzsmm/'
    elif 'standards' in path_lower:
        return 'Standards', 'High', 'knowledge/sources/standards/'
    elif 'specifications' in path_lower:
        return 'Specifications', 'High', 'knowledge/sources/specifications/'
    elif 'projects' in path_lower:
        return 'Projects', 'High', 'knowledge/sources/projects/'
    elif 'councils' in path_lower:
        return 'Councils', 'High', 'knowledge/sources/councils/'
    elif 'reports' in path_lower:
        return 'Reports', 'High', 'knowledge/sources/reports/'
    else:
        return 'Unknown', 'Low', 'knowledge/sources/unknown/'

def generate_inventory(root_dir, output_file):
    """Generate inventory of all files in the knowledge_inbox"""
    files_data = []

    # Walk through all directories and files
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, start=os.path.dirname(root_dir))

            # Generate document ID
            doc_id = f"DOC-{len(files_data)+1:05d}"

            # Get file info
            file_info = get_file_info(file_path, doc_id)
            if file_info:
                files_data.append(file_info)

    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'Document_ID', 'Original_Path', 'Filename', 'Extension',
            'File_Size', 'Created_Date', 'Modified_Date',
            'Detected_Category', 'Confidence', 'Suggested_Destination'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(files_data)

    return len(files_data)

if __name__ == "__main__":
    # Configuration
    knowledge_inbox = "knowledge_inbox"
    output_csv = "knowledge_inventory.csv"

    print(f"Generating inventory from {knowledge_inbox}...")
    file_count = generate_inventory(knowledge_inbox, output_csv)
    print(f"Inventory complete. Found {file_count} files.")
    print(f"Output saved to {output_csv}")
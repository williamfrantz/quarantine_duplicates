#!/usr/bin/env python3
#
# quarantine_duplicates.py
#
import os
import hashlib
import shutil
from pathlib import Path
from collections import defaultdict

def partial_hash(file_path, num_bytes=1024):
    """Calculate a hash of the first `num_bytes` of a file."""
    hasher = hashlib.md5()  # Faster for preliminary checks
    with open(file_path, 'rb') as f:
        hasher.update(f.read(num_bytes))
    return hasher.hexdigest()

def full_hash(file_path):
    """Calculate the full sha256 hash of a file."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

def find_duplicates(base_directory, quarantine_directory):
    """Find duplicate files in a directory, excluding the quarantine directory."""
    size_map = defaultdict(list)
    partial_hash_map = {}
    full_hash_map = {}
    duplicates = []

    # Count total files for progress tracking
    total_files = sum(len(files) for _, _, files in os.walk(base_directory))
    processed_files = 0

    # First, group files by size
    for root, dirs, files in os.walk(base_directory):
        dirs[:] = [d for d in dirs if not d.startswith('.')]  # Exclude hidden directories
        dirs[:] = [d for d in dirs if d not in {'Media Cache Files', '__pycache__'}]  # Exclude commonly known cache directories
        dirs[:] = [d for d in dirs if not d.endswith('.app')]  # Exclude app directories

        root_path = Path(root)
        if quarantine_directory in root_path.parents or root_path == quarantine_directory:
            continue  # Skip the quarantine directory
        for file in files:
            if file in {'.DS_Store', 'Thumbs.db', 'desktop.ini'}:  # Skip system files
                continue
            if file.startswith('.'):  # Skip hidden files
                continue
            file_path = root_path / file
            try:
                file_size = file_path.stat().st_size
                size_map[file_size].append(file_path)
                processed_files += 1
                if processed_files % 100 == 0:  # Update every 100 files
                    print(f"Scanned {processed_files}/{total_files} files...")
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

    print("File size grouping completed. Checking for duplicates...")

    # Check files with the same size for duplicates by hash
    processed_files = 0
    total_file_groups = len(size_map)
    for idx, file_list in enumerate(size_map.values(), start=1):
        if len(file_list) > 1:  # Only compare files with the same size
            for file_path in file_list:
                try:
                    # Calculate the partial hash
                    file_partial_hash = partial_hash(file_path)
                    if file_partial_hash in partial_hash_map:
                        # If partial hash matches, calculate the full hash
                        file_full_hash = full_hash(file_path)
                        if file_full_hash in full_hash_map:
                            # If full hash matches, it's a duplicate
                            duplicates.append((file_path, full_hash_map[file_full_hash]))
                        else:
                            full_hash_map[file_full_hash] = file_path
                    else:
                        partial_hash_map[file_partial_hash] = file_path
                except Exception as e:
                    print(f"Error hashing file {file_path}: {e}")
        processed_files += 1
        if processed_files % 10 == 0 or processed_files == total_file_groups:
            print(f"Processed {processed_files}/{total_file_groups} size groups...")

    return duplicates

def quarantine_duplicates(duplicates, quarantine_directory):
    """Move duplicate files to a quarantine directory."""
    quarantine_directory = Path(quarantine_directory)
    quarantine_directory.mkdir(parents=True, exist_ok=True)

    total_duplicates = len(duplicates)
    for idx, (duplicate, original) in enumerate(duplicates, start=1):
        try:
            quarantine_path = quarantine_directory / duplicate.name
            quarantine_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(duplicate, quarantine_path)
            print(f"Moved {idx}/{total_duplicates}: {duplicate}")
        except Exception as e:
            print(f"Error quarantining file {duplicate}: {e}")

def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 quarantine_duplicates.py <directory>")
        sys.exit(1)

    base_directory = Path(sys.argv[1]).resolve()
    if not base_directory.is_dir():
        print(f"The directory {base_directory} does not exist.")
        sys.exit(1)

    quarantine_directory = base_directory / "Quarantined"

    print(f"Scanning directory: {base_directory}")
    duplicates = find_duplicates(base_directory, quarantine_directory)
    if duplicates:
        print(f"Found {len(duplicates)} duplicate files.")
        print(f"Quarantining duplicates to: {quarantine_directory}")
        quarantine_duplicates(duplicates, quarantine_directory)
    else:
        print("No duplicate files found.")

if __name__ == "__main__":
    main()

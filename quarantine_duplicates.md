### Documentation and Instructions for `quarantine_duplicates.py`

---

#### **Purpose**
The `quarantine_duplicates.py` program identifies duplicate files in a specified directory based on their content. It excludes files in a quarantine directory, which is automatically created in the root of the scanned directory. Duplicate files are moved to the quarantine directory for review and potential deletion.

---

#### **Features**
- Scans a directory and its subdirectories for duplicate files.
- Uses file size as a quick filter before hashing to optimize performance.
- Excludes the `Quarantined` directory from scanning.
- Automatically creates a `Quarantined` directory in the root of the search directory if it doesn’t exist.
- Moves duplicate files to the `Quarantined` directory for safekeeping.

---

#### **Requirements**
1. Python 3.6 or later (Python 3.13 is supported).
2. A system running macOS, Linux, or Windows.
3. Sufficient disk space in the root directory for the quarantine folder.

---

#### **Installation**
1. Download the script and save it as `quarantine_duplicates.py`.
2. Ensure Python is installed and accessible from the terminal:
   ```bash
   python3 --version
   ```

---

#### **Usage**
1. **Run the Program**:
   Open a terminal and navigate to the directory containing the script. Execute the following command:
   ```bash
   python3 quarantine_duplicates.py /path/to/search/directory
   ```
   Replace `/path/to/search/directory` with the directory you want to scan.

2. **Output**:
   - The program will display progress and any errors encountered during the process.
   - The quarantine directory is named `Quarantined` and is created in the root of the specified directory.

3. **Quarantine Folder**:
   - All identified duplicates will be moved to `/path/to/search/directory/Quarantined`.
   - Review the quarantine folder periodically and delete unwanted duplicates.

---

#### **Example**
Assume the directory structure:
```
/example
    ├── file1.txt
    ├── file2.txt
    ├── subdir/
        └── file3.txt
```
Run:
```bash
python3 quarantine_duplicates.py /example
```

- The program identifies duplicate files, such as `file1.txt` and `file3.txt`.
- It moves duplicates to `/example/Quarantined/` for further review.

---

#### **Error Handling**
- If the program encounters a file it cannot process (e.g., due to permissions), it will log an error message and continue scanning other files.
- If the quarantine directory cannot be created, the program will stop with an error.

---

#### **Optimization Details**
1. **File Size Filter**:
   - Files are first grouped by size.
   - Only files of the same size are hashed to check for duplicates.

2. **Hash Calculation**:
   - Uses SHA-256 to uniquely identify files by content.
   - Ensures files with different names or modification dates are detected as duplicates if their contents are identical.

---

#### **Limitations**
1. **Large Data Sets**:
   - Scanning very large directories (e.g., 8TB of data) can take significant time, depending on the number and size of files.
   - Consider running the script overnight for very large datasets.

2. **Not a Real-Time Monitor**:
   - The script identifies duplicates present at the time of scanning. It does not monitor new files added afterward.

3. **Quarantine Naming Conflicts**:
   - If two files with the same name are quarantined, only the first file is retained. Modify the script if you need unique naming for quarantined duplicates.

---

#### **Future Enhancements**
- Add an option to log the duplicates and their original paths to a file for future reference.
- Provide a mode to only list duplicates without moving them.
- Support for ignoring specific file extensions or directories.


import os
import time
from hashlib import sha1

def simulate_upload(file_path):
    """
    Simulate receiving an uploaded file, storing it,
    and computing its master hash to verify data integrity.
    """
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        master_hash = sha1(data).hexdigest()
        print("CSP2: File stored successfully. Master Hash computed:", master_hash)
        return master_hash
    except Exception as e:
        print("CSP2: Error reading file:", e)
        return None

if __name__ == '__main__':
    # Path to the sample file in the project folder
    file_to_upload = os.path.join(os.getcwd(), "sample_file.txt")
    
    # Check if the file exists; if not, create one.
    if not os.path.exists(file_to_upload):
        print("CSP2: sample_file.txt not found. Creating a sample file...")
        with open(file_to_upload, "w") as f:
            f.write("This is a sample file for testing the cloud security project.")
    
    print("CSP2: Waiting to process file upload...")
    time.sleep(2)
    simulate_upload(file_to_upload)

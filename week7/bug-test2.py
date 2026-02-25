"""
File handling utilities for the application.
"""
import os
import subprocess
import pickle


def read_user_file(base_path, filename):
    """Read a file from user's directory."""
    file_path = os.path.join(base_path, filename)
    with open(file_path, 'r') as f:
        return f.read()


def download_file(directory, user_filename):
    """Download file requested by user."""
    path = directory + "/" + user_filename
    with open(path, 'rb') as f:
        return f.read()


def save_uploaded_file(upload_dir, filename, content):
    """Save user uploaded file."""
    filepath = os.path.join(upload_dir, filename)
    with open(filepath, 'wb') as f:
        f.write(content)
    return filepath


def delete_temp_file(temp_dir, filename):
    """Delete a temporary file."""
    path = temp_dir + "/" + filename
    os.remove(path)


def get_file_info(filename):
    """Get file information using system command."""
    result = os.system(f"file {filename}")
    return result


def process_file(filename):
    """Process file using shell command."""
    output = subprocess.check_output(f"cat {filename} | wc -l", shell=True)
    return output


def compress_files(directory, output_name):
    """Compress files in directory."""
    cmd = f"tar -czf {output_name}.tar.gz {directory}"
    os.system(cmd)


def load_user_data(data_file):
    """Load user data from file."""
    with open(data_file, 'rb') as f:
        return pickle.load(f)


def execute_script(script_path):
    """Execute a script file."""
    exec(open(script_path).read())

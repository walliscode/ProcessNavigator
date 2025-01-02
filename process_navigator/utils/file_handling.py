from pathlib import Path
from uuid import uuid4

from flask import current_app

"""
This function takes in a file, extracts the file extension, gives the file a UUID name, and saves the file to the file storage system whilst returning the file name. This uses the Path library
"""


def save_file(file):
    file_extension = Path(file.filename).suffix
    uuid_file_name = str(uuid4())
    file_name = uuid_file_name + file_extension
    full_file_path = Path(current_app.config["FILE_STORAGE"]) / file_name
    file.save(full_file_path)

    return file_name

import json
import os
from app.config import Settings

class DBManager:
    def __init__(self):
        self.db_path = Settings().db_path

    def save_product(self, product):
        # Ensure the file exists; if not, create it with an empty list
        if not os.path.exists(self.db_path):
            with open(self.db_path, "w") as file:
                json.dump([], file, indent=4)
        
        # Open the file in read and write mode
        with open(self.db_path, "r+") as file:
            try:
                # Load existing data
                data = json.load(file)
            except json.JSONDecodeError:
                # If the file is empty or corrupted, initialize with an empty list
                data = []
            
            # Append the new product
            data.append(product)
            
            # Move to the beginning of the file and write the updated data
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()  # Ensure no old data remains if the new data is shorter

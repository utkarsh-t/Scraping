from pydantic_settings import BaseSettings
from datetime import datetime
import os

class Settings(BaseSettings):
    static_token: str 
    db_path: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_path = self.generate_db_path()

    def generate_db_path(self) -> str:
        # Create the directory if it does not exist
        os.makedirs('scrapped_json_data', exist_ok=True)

        # Get current timestamp in DDMMYYYYHHMMSS format
        timestamp = datetime.now().strftime("%d/%m/%YT%H:%M:%S")
        timestamp = timestamp.replace("/", "_").replace(":", "_")
        # Return the path with timestamp
        return f'scrapped_json_data/{timestamp}.json'

    class Config:
        env_file = ".env"

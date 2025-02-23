from .duckdb_database import DuckDBDatabase

class DatabaseBuilder():

    def __init__(self, db_path : str = None):
        self.db_path = db_path

    def database_type(self, database_type : str):
        if database_type == "duckdb":
            self.database_object = DuckDBDatabase(self.db_path)
        return self
        
    def build(self):
        return self.database_object
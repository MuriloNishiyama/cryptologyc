import os
import duckdb
import pandas as pd
from .base_database import BaseDatabase


class DuckDBDatabase(BaseDatabase):
    def __init__(self, db_path: str = None):
        if db_path is None:
            root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
            self.db_path = os.path.join(root_dir, "data", "cryptologyc.db")
        else:
            self.db_path = db_path

    def append_df(self, table_name : str, df_pd : pd.DataFrame):
        with duckdb.connect(self.db_path) as conn:
            try:
                conn.sql(f"INSERT INTO {table_name} SELECT * FROM df_pd")
            except Exception as e:
                if f"Catalog Error: Table with name {table_name} does not exist!" in str(e):
                    conn.sql(f"CREATE TABLE {table_name} AS SELECT * FROM df_pd")
                else:
                    raise Exception(e)
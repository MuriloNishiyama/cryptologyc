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

    def get_last_block(self, currency):
        with duckdb.connect(self.db_path) as conn:
            try:
                return conn.sql(f"SELECT MAX(blockNumber) FROM transactions WHERE currency = '{currency}'").fetchall()[0][0]
            except IndexError:
                return None
            except Exception as e:
                if f"Table with name transactions does not exist!" in str(e):
                    return None
                else:
                    raise Exception(e)

    def append_df(self, table_name : str, df_pd : pd.DataFrame):
        with duckdb.connect(self.db_path) as conn:
            try:
                schema_df = conn.execute(f"PRAGMA table_info({table_name})").fetchdf()
                if not schema_df.empty:
                    table_columns = schema_df["name"].tolist()
                    for col in table_columns:
                        if col not in df_pd.columns:
                            df_pd[col] = None
                    df_pd = df_pd[table_columns]
                conn.sql(f"INSERT INTO {table_name} SELECT * FROM df_pd")
            except Exception as e:
                if f"Table with name {table_name} does not exist!" in str(e):
                    conn.sql(f"CREATE TABLE {table_name} AS SELECT * FROM df_pd")
                else:
                    raise Exception(e)
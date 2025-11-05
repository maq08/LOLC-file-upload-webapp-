 
from sqlalchemy import create_engine
import sys

def get_engine():
    server = '.\SQLEXPRESS'       # Change if needed
    database = 'LOLCUploadsDB' # The DB you created
    driver = 'ODBC Driver 17 for SQL Server'

    try:
        conn_str = (
            f"mssql+pyodbc://@{server}/{database}"
            f"?driver={driver}"
            f"&trusted_connection=yes"
            f"&encrypt=no"
        )
        engine = create_engine(conn_str)
        with engine.connect():
            print("✅ DB connection established!")
        return engine
    except Exception as e:
        print(f"❌ DB connection failed:\n{e}")
        sys.exit()

if __name__ == "__main__":
    get_engine()

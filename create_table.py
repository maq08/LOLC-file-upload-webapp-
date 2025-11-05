from db_connection import get_engine
from sqlalchemy import text

engine = get_engine()

with engine.begin() as conn:
    conn.execute(text("""
    CREATE TABLE UploadedFiles (
        id INT IDENTITY(1,1) PRIMARY KEY,
        upload_id VARCHAR(100),
        filename NVARCHAR(255),
        stored_name NVARCHAR(255),
        path NVARCHAR(500),
        size_bytes INT,
        status VARCHAR(20),
        created_at DATETIME DEFAULT GETDATE()
    );
    """))
print("✅ Table 'UploadedFiles' created successfully!")

import pandas as pd
from sqlalchemy import create_engine

# Step 1: Load your clean CSV data
df = pd.read_csv('data/final_clean_data.csv')

# Step 2: Define your MySQL connection details
username = 'root'           # MySQL username
password = 'peeuparth'      # MySQL password
host = 'localhost'          # Usually 'localhost' if running locally
database = 'complaint_db'   # The database you created in MySQL Workbench

# Step 3: Create the SQLAlchemy connection string
db_connection_str = f'mysql+mysqlconnector://{username}:{password}@{host}/{database}'
db_engine = create_engine(db_connection_str)

# Step 4: Upload your DataFrame to MySQL
df.to_sql('complaints', con=db_engine, if_exists='replace', index=False)

print("✅ Data successfully uploaded to the 'complaints' table in MySQL.")

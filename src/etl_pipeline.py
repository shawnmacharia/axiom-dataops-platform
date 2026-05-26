import pandas as pd
import urllib
from sqlalchemy import create_engine


SERVER = '.\\SQLEXPRESS'        # Double backslash to escape it in Python
DATABASE = 'AXIOM'  


connection_properties = (
    f"Driver={{ODBC Driver 17 for SQL Server}};" 
    f"Server={SERVER};"
    f"Database={DATABASE};"
    f"Trusted_Connection=yes;"
    f"Encrypt=yes;"
    f"TrustServerCertificate=yes;"
)


params = urllib.parse.quote_plus(connection_properties)
connection_string = f"mssql+pyodbc:///?odbc_connect={params}"


sql_connection = create_engine(connection_string)


# Notice we changed the parameter name here to accept the connection
def etl_pipeline(sql_connection):    
    # Expanded customer data
    customers_df = pd.DataFrame({
        'Name': [
            'John Mwangi', 'Amina Mohamed', 'David Otieno', 'Grace Wanjiku', 
            'Evans Kiprop', 'Mercy Chepngetich', 'Joseph Mutua', 'Faith Kwamboka'
        ],
        'Email': [
            'john.mwangi@example.com', 'amina.mohamed@example.com', 'david.otieno@example.com', 'grace.wanjiku@example.com',
            'evans.kiprop@example.com', 'mercy.chep@example.com', 'joseph.mutua@example.com', 'faith.kwamboka@example.com'
        ]
    })
    
    # Expanded orders data
    orders_df = pd.DataFrame({
        'CustomerID': [1, 2, 3, 4, 1, 5, 6, 2, 7, 8, 4, 3],
        'OrderDate': [
            '2026-01-15', '2026-01-20', '2026-02-02', '2026-02-14', 
            '2026-03-01', '2026-03-15', '2026-04-05', '2026-04-18', 
            '2026-05-01', '2026-05-12', '2026-05-20', '2026-05-25'
        ],
        'Total': [
            2500.00, 12000.50, 450.00, 3100.20, 
            1500.00, 8500.00, 620.00, 5300.00, 
            950.00, 15000.00, 2200.00, 1800.00
        ]
    })
    
    print("Loading data into SQL Server AXIOM database...")
    customers_df.to_sql('Customers', con=sql_connection, if_exists='append', index=False)
    orders_df.to_sql('Orders', con=sql_connection, if_exists='append', index=False)
    print("ETL Pipeline finished successfully!")
    
    return None

if __name__ == "__main__":
    etl_pipeline(sql_connection)
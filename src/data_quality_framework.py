import pandas as pd

def check_null_values(sql_connection):
    """Audits the production Customers table for any missing values."""
    print("\n--- [DQ Audit] Checking for Null Values in Customers... ---")
    
    # Read directly from your live SQL Server instance
    customers_df = pd.read_sql_query("SELECT * FROM Customers", con=sql_connection)
    null_counts = customers_df.isnull().sum()
    
    print(null_counts)
    return null_counts

def check_duplicate_rows(sql_connection):
    """Audits the production Orders table for any accidental duplicate rows."""
    print("\n--- [DQ Audit] Checking for Duplicate Rows in Orders... ---")
    
    # Read directly from your live SQL Server instance
    orders_df = pd.read_sql_query("SELECT * FROM Orders", con=sql_connection)
    duplicate_count = orders_df.duplicated().sum()
    
    print(f"Total duplicate rows found: {duplicate_count}")
    return duplicate_count
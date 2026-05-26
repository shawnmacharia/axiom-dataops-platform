import hashlib
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - SECURITY - %(levelname)s - %(message)s')

def mask_pii_data(dataframe, columns_to_mask):
    """
    Hashes sensitive columns (like Emails or SSNs) in a Pandas DataFrame 
    using SHA-256 so the data team can analyze metrics without seeing private info.
    """
    df_masked = dataframe.copy()
    for col in columns_to_mask:
        if col in df_masked.columns:
            # Apply a one-way hash to the data
            df_masked[col] = df_masked[col].apply(
                lambda x: hashlib.sha256(str(x).encode('utf-8')).hexdigest() if pd.notnull(x) else x
            )
            logging.info(f"Successfully masked PII column: {col}")
        else:
            logging.warning(f"Column {col} not found in dataset. Skipping masking.")
    return df_masked

def get_secure_connection_string():
    """
    Retrieves database credentials securely from environment variables 
    instead of hardcoding them in the script.
    """
    server = os.getenv("DB_SERVER", ".\\SQLEXPRESS")
    database = os.getenv("DB_NAME", "AXIOM")
    # In a real app, you'd pull username/password from Azure KeyVault or AWS Secrets Manager here
    return f"Server={server};Database={database};Trusted_Connection=yes;"

if __name__ == "__main__":
    import pandas as pd
    # Quick test to prove the masking works
    sample_data = pd.DataFrame({'Name': ['Alice', 'Bob'], 'Email': ['alice@test.com', 'bob@test.com']})
    print("Original Data:\n", sample_data)
    secure_data = mask_pii_data(sample_data, ['Email'])
    print("\nSecured Data:\n", secure_data)
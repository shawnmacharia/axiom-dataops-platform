import logging
import requests
import os
import pandas as pd
import urllib
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# Configure professional logging formatting
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - AXIOM ALERTS - %(levelname)s - %(message)s'
)

# Replace this with a real Slack/Teams Webhook URL later
WEBHOOK_URL = os.getenv("ALERT_WEBHOOK_URL", "")

def get_db_engine():
    # Targets the local database (or Docker bridge if running in container)
    SERVER = os.getenv("DATABASE_SERVER", ".\\SQLEXPRESS")
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
    return create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

def send_alert(message, severity="WARNING"):
    """Sends an alert to standard output and optionally to a Webhook."""
    log_msg = f"[{severity}] {message}"
    
    if severity == "CRITICAL":
        logging.error(log_msg)
    else:
        logging.warning(log_msg)
        
    # If a webhook URL is configured, push the alert to Slack/Teams
    if WEBHOOK_URL:
        try:
            payload = {"text": f"🚨 *Axiom DataOps Alert* 🚨\n{log_msg}"}
            requests.post(WEBHOOK_URL, json=payload, timeout=5)
            logging.info("Webhook alert dispatched successfully.")
        except Exception as e:
            logging.error(f"Failed to send webhook alert: {e}")

def run_health_checks():
    logging.info("Initiating Axiom Platform Health Checks...")
    engine = get_db_engine()
    
    # Check 1: Database Connection Health
    try:
        with engine.connect() as conn:
            logging.info("Database connection established successfully.")
    except OperationalError as e:
        send_alert("Database connection failed! The SQL Server is unreachable.", "CRITICAL")
        return # Stop further checks if the DB is completely down

    # Check 2: Data Quality (Duplicate Rows)
    try:
        orders_df = pd.read_sql_query("SELECT * FROM Orders", con=engine)
        duplicate_count = orders_df.duplicated().sum()
        
        if duplicate_count > 0:
            send_alert(f"Data Quality Violation: Found {duplicate_count} duplicate rows in the Orders table.", "WARNING")
        else:
            logging.info("Data Quality Check Passed: No duplicate rows detected in Orders.")
            
    except Exception as e:
        send_alert(f"Failed to execute Data Quality checks: {e}", "CRITICAL")

if __name__ == "__main__":
    run_health_checks()
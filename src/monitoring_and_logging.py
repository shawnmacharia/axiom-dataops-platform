import logging
import time
from functools import wraps

logging.basicConfig(level=logging.INFO, format='%(asctime)s - MONITOR - %(levelname)s - %(message)s')

def track_latency(max_latency_seconds=5.0):
    """
    A decorator that wraps around any ETL function to track how long it takes to run.
    If it exceeds max_latency_seconds, it throws a warning.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            # Run the actual function
            result = func(*args, **kwargs)
            
            # Calculate duration
            end_time = time.time()
            execution_time = end_time - start_time
            
            logging.info(f"Function '{func.__name__}' completed in {execution_time:.4f} seconds.")
            
            if execution_time > max_latency_seconds:
                logging.warning(f"PERFORMANCE DEGRADATION: '{func.__name__}' took longer than {max_latency_seconds}s!")
                # Here you could call your alerting_system.send_alert() function
                
            return result
        return wrapper
    return decorator

# --- Quick Test ---
if __name__ == "__main__":
    @track_latency(max_latency_seconds=1.0)
    def simulate_database_load():
        logging.info("Loading massive dataset...")
        time.sleep(1.5)  # Simulating a slow query
        return "Data Loaded"

    simulate_database_load()
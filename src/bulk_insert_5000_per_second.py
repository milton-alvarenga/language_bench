import os
import time
#pip install psycopg2
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
import socket

logfilepath = "./log/bulk_insert_5000_per_second_py.log"

if not os.path.isfile(logfilepath):
    with open(logfilepath,'w') as f:
        f.write("current_time|agent_id|language|environment_id|total_registers_inserted|time_spent_to_insert\n")

f_log = open(logfilepath,"a")



# Get database credentials from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT", "5432")  # Default port for PostgreSQL

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    dbname=DB_NAME,
    port=DB_PORT
)
# Enable autocommit to prevent manual commit after each insertion
conn.autocommit = True



def write_log(f_log, agent_id, total_registers_inserted, time_spent_to_insert):
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
    environment_id = "amb1"

    data = [
        formatted_time,
        agent_id,
        'py',
        environment_id,
        str(total_registers_inserted),
        str(time_spent_to_insert)
    ]

    f_log.write(f"{'|'.join(data)}\n")
    f_log.flush()

def bulk_insert_stock_prices():
    # Generate 5000 unique stock_price records
    records = [(stock_id, round(100 + stock_id * 0.01, 4)) for stock_id in range(1, 5001)]
    
    # Define the SQL for bulk insertion using execute_values for better performance
    sql = """
    INSERT INTO stock_price (stock_id, price)
    VALUES %s
    """
    
    # Execute the bulk insertion
    with conn.cursor() as cur:
        execute_values(cur, sql, records)

try:
    # Number of records to insert per loop
    batchSize = 5000
    agent_id = socket.gethostname()
    while True:
        start_time = time.time()
        
        # Perform the bulk insert
        bulk_insert_stock_prices()
        
        # Calculate the loop execution time
        elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds

        write_log(f_log, agent_id, batchSize, elapsed_time)

        print(f"Inserted stock prices for {batchSize} stocks", flush=True)
        
        # Check if sleep is needed to maintain 1 second (1000 ms) interval
        if elapsed_time < 1000:
            time.sleep((1000 - elapsed_time) / 1000)  # Convert remaining time to seconds
            
except KeyboardInterrupt:
    print("Process interrupted by user.")
finally:
    # Close the database connection
    conn.close()
    print("Database connection closed.")
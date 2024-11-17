import json
import psycopg2
import os

# Database credentials (replace these with actual values or set them as environment variables)
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT", "5432")


# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    dbname=DB_NAME,
    port=DB_PORT
)
conn.autocommit = True  # Enable autocommit mode

#file_path = 
#stock_market_id = 
files_path = ["nyse_full_tickers.json","nasdaq_full_tickers.json"]
#3 nyse
#2 nasdaq
stocks_market_id = [3, 2]

for index,file_path in enumerate(files_path):
    stock_market_id = stocks_market_id[index]

    # Read the JSON file into a variable named json_data
    with open(file_path, "r") as file:
        json_data = json.load(file)


    # SQL insert query.
    # TODO Could be optimized as prepared statement or bulk insertion
    sql_insert = """
    INSERT INTO stock (symbol, nm, stock_market_id)
    VALUES (%s, %s, %s)
    """

    # Parse the JSON data and insert into the database
    try:
        with conn.cursor() as cursor:
            for item in json_data:
                # Extract required fields
                symbol = item["symbol"]
                name = item["name"]
                
                # Execute the insert query
                cursor.execute(sql_insert, (symbol, name, stock_market_id))
                print(f"Inserted stock with symbol: {symbol} and name: {name}")

    except Exception as e:
        print("An error occurred:", e)
    finally:
        # Close the database connection
        conn.close()
        print("Database connection closed.")
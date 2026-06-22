

import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """
    Opens a new connection to the MySQL database using credentials
    from the .env file.
    """
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "seekin_demo")
    )
    return connection


def run_query(sql_query):
    """
    Runs a SELECT query and returns the results as a list of dictionaries,
    e.g. [{"name": "Raj Kumar", "city": "Lucknow"}, {...}, ...]

    Using dictionaries (not plain tuples) makes it much easier to convert
    results into JSON later for the frontend, and to pass into the
    insight generator.
    """
    connection = get_connection()

    
    cursor = connection.cursor(dictionary=True)

    cursor.execute(sql_query)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results



if __name__ == "__main__":
    test_query = "SELECT name, city FROM customers WHERE city = 'Lucknow'"
    print("Running test query:", test_query)

    rows = run_query(test_query)
    print("\nResults:")
    for row in rows:
        print(row)
import psycopg2
from pokimon import fetch_pokemon_data
from dotenv import load_dotenv
import os
import requests

load_dotenv()


# Replace these with your database connection details
db_params = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
}




# Establish a connection to the PostgreSQL database
connection = psycopg2.connect(**db_params)

# Create a cursor to interact with the database
cursor = connection.cursor()

# Define the SQL query to create the table
create_table_query = '''
        CREATE TABLE IF NOT EXISTS pokemons (
            name TEXT PRIMARY KEY,
            image TEXT,
            types TEXT
        );
    '''





# Execute the SQL query to create the table
cursor.execute(create_table_query)



# Assuming you have the fetch_pokemon_data() function from the previous step
pokemons = fetch_pokemon_data()

# Insert the Pokemon data into the database
for pokemon in pokemons:
    name = pokemon['name']
    image = pokemon['image']
    types = ', '.join(pokemon['types'])
    insert_query = f"INSERT INTO pokemons (name, image, types) VALUES ('{name}', '{image}', '{types}')"
    cursor.execute(insert_query)
    print("Doneeee")

# Commit the changes
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()

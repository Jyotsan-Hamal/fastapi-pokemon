from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
import asyncpg
from dotenv import load_dotenv
import os
import uvicorn

app = FastAPI()

load_dotenv()

class Pokemon(BaseModel):
    name: str
    image: str
    types: List[str]

async def get_db_connection():
    conn = await asyncpg.connect(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('DB_NAME'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    return conn

@app.get("/api/v1/pokemons", response_model=List[Pokemon])
async def get_pokemons(name: str = None, type: str = None):
    try:
        conn = await get_db_connection()
        if name and type:
            records = await conn.fetch("SELECT name, image, types FROM pokemons WHERE name LIKE $1 AND types LIKE $2", '%' + name + '%', '%' + type + '%')
        elif name:
            records = await conn.fetch("SELECT name, image, types FROM pokemons WHERE name LIKE $1", '%' + name + '%')
        elif type:
            records = await conn.fetch("SELECT name, image, types FROM pokemons WHERE types LIKE $1", '%' + type + '%')
        else:
            
            records = await conn.fetch('SELECT name, image, types FROM pokemons limit 10')
        
        pokemons = [Pokemon(**dict(record, types=record['types'].split(', '))) for record in records]
        # pokemons = await conn.fetch('SELECT name, image, types FROM pokemons limit 10')
        await conn.close()
        return pokemons
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error: " + str(e))
    
if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
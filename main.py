from fastapi import FastAPI
from database import obtenerLosPrimerosProductos, obtenerProductosPorCodigo
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

app = FastAPI()

@app.get("/producto/{codigo}")
async def buscar_producto(codigo: str):
    producto = obtenerProductosPorCodigo(codigo)
    if producto:
        return producto
    return {"mensaje": "Producto no encontrado"}

@app.get("/productos/")
async def obtener_productos(limit: int = 10):
    productos = obtenerLosPrimerosProductos(limit)
    if productos:
        return productos
    return {"mensaje": "No se encontraron productos"}

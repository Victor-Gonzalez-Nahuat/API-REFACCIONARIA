from fastapi import FastAPI, HTTPException, HTMLResponse
from database import obtenerLosPrimerosProductos, obtenerProductosPorCodigo, obtenerProductosPorNombre
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta property="og:title" content="Catálogo de Refaccionaria Falla" />
        <meta property="og:description" content="Consulta productos actualizados." />
        <meta property="og:image" content="https://i.ibb.co/8LxBQKh2/images.png" />
        <meta property="og:url" content="https://web-refaccionaria-production.up.railway.app/" />
        <meta name="twitter:card" content="summary_large_image">
        <title>Catálogo Refaccionaria</title>
    </head>
    <body>
        <script>
            window.location.href = "https://web-refaccionaria-production.up.railway.app/";
        </script>
    </body>
    </html>
    """

@app.get("/producto/{codigo}")
async def buscar_producto(codigo: str):
    producto = obtenerProductosPorCodigo(codigo)
    if producto:
        return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")

@app.get("/productos/")
async def obtener_productos(limit: int = 10):
    productos = obtenerLosPrimerosProductos(limit)
    if productos:
        return productos
    raise HTTPException(status_code=404, detail="No se encontraron productos")

@app.get("/producto/nombre/{nombre}")
async def obtener_codigo(nombre: str):
    codigo = obtenerProductosPorNombre(nombre)
    if codigo:
        return codigo
    raise HTTPException(status_code=404, detail="Código no encontrado")

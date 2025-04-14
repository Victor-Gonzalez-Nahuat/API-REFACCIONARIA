import pymysql
import os

# Obtener las credenciales desde las variables de entorno
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT')

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )

def obtenerProductosPorCodigo(codigo):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM INARMA01 WHERE codigo = %s", (codigo,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "codigo": row[0],
            "nombre": row[1],
            "precio": row[2],
            "stock": row[3]
        }
    return None

def obtenerLosPrimerosProductos(limit):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM INARMA01 LIMIT %s", (limit,))
    rows = cursor.fetchall()
    conn.close()
    productos = []
    for row in rows:
        productos.append({
            "codigo": row[0],
            "nombre": row[3]  # Asumimos que el nombre está en la cuarta columna
        })
    return productos

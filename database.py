import pymysql
import os

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = int(os.getenv('DB_PORT'))

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )

def obtenerProductosPorNombre(nombre):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_codigo, id_descripcion FROM INARMA01 WHERE id_descripcion = %s
        """, (nombre,))
    arma = cursor.fetchone()

    if not arma:
        conn.close()
        return None
    
    codigo, nombre = arma
    conn.close()
    
    return {
        "codigo": codigo,
        "nombre": nombre
    }


def obtenerProductosPorCodigo(codigo):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_codigo, id_descripcion, id_grupo, id_maximo, id_minimo, id_lista1, id_provee
        FROM INARMA01
        WHERE id_codigo = %s
    """, (codigo,))
    arma = cursor.fetchone()

    if not arma:
        conn.close()
        return None
    
    codigo, nombre, grupo, maximo, minimo, precio_lista, id_proveedor = arma

    cursor.execute("""
        SELECT dt_sadoinicial, dt_entradas, dt_salidas, dt_ultimo_costo, dt_ultima_venta, dt_ultima_compra
        FROM INARAR01
        WHERE dt_codigo = %s
    """, (codigo,))
    arar = cursor.fetchone()

    if arar:
        saldo_inicial, entradas, salidas, ultimo_costo, ultima_venta, ultima_compra = arar
        existencia = (saldo_inicial or 0) + (entradas or 0) - (salidas or 0)
    else:
        existencia = None
        ultimo_costo = None
        ultima_venta = None

    cursor.execute("""
        SELECT dt_cliente
        FROM PRARMA01
        WHERE dt_codigoc = %s
    """, (id_proveedor,))
    proveedor = cursor.fetchone()
    nombre_proveedor = proveedor[0] if proveedor else "Desconocido"

    conn.close()

    return {
        "codigo": codigo,
        "nombre": nombre,
        "grupo": grupo,
        "maximo": maximo,
        "minimo": minimo,
        "precio": precio_lista,
        "existencia": existencia,
        "ultimo_costo": ultimo_costo,
        "ultima_venta": ultima_venta,
        "ultima_compra": ultima_compra,
        "proveedor": nombre_proveedor
    }


def obtenerLosPrimerosProductos(limit):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM INARMA01 LIMIT %s", (limit,))
    rows = cursor.fetchall()
    conn.close()
    productos = []
    for row in rows:
        productos.append({
            "codigo": row[1],
            "nombre": row[3]  
        })
    return productos

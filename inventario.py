import sqlite3

def conectar():
    con = sqlite3.connect("tienda.db")
    con.execute("PRAGMA foreign_keys = ON;")
    return con

def init_db():
    with conectar() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            precio REAL NOT NULL CHECK(precio > 0),
            stock INTEGER NOT NULL CHECK(stock >= 0)
        );""")
        con.execute("""CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL CHECK(cantidad > 0),
            total REAL NOT NULL,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE RESTRICT
        );""")

def registrar_producto():
    nom = input("Nombre: ").strip()
    try:
        pre, stk = float(input("Precio: ")), int(input("Stock: "))
        with conectar() as con:
            con.execute("INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?);", (nom, pre, stk))
        print("[OK] Producto guardado.")
    except Exception as e:
        print(f"[Error] {e}")

def listar_productos():
    with conectar() as con:
        res = con.execute("SELECT id, nombre, precio, stock FROM productos;").fetchall()
        print("\nID | Nombre | Precio | Stock")
        for f in res:
            print(f"{f[0]} | {f[1]} | ${f[2]} | {f[3]}")

def actualizar_producto():
    listar_productos()
    try:
        pid = int(input("ID a actualizar: "))
        pre, stk = float(input("Nuevo precio: ")), int(input("Nuevo stock: "))
        with conectar() as con:
            con.execute("UPDATE productos SET precio = ?, stock = ? WHERE id = ?;", (pre, stk, pid))
        print("[OK] Producto actualizado.")
    except Exception as e:
        print(f"[Error] {e}")

def eliminar_producto():
    listar_productos()
    try:
        pid = int(input("ID a eliminar: "))
        with conectar() as con:
            con.execute("DELETE FROM productos WHERE id = ?;", (pid,))
        print("[OK] Producto eliminado.")
    except sqlite3.IntegrityError:
        print("[Error] No se puede eliminar: el producto tiene ventas registradas.")

def registrar_venta(fallar=False):
    listar_productos()
    try:
        pid = int(input("ID producto: "))
        cant = int(input("Cantidad: "))
        con = conectar()
        try:
            prod = con.execute("SELECT nombre, precio, stock FROM productos WHERE id = ?;", (pid,)).fetchone()
            if not prod:
                print("[Error] Producto inexistente.")
                return
            if prod[2] < cant:
                print(f"[Error] Stock insuficiente (Disponible: {prod[2]}).")
                return
            
            # INICIO TRANSACCIÓN MANUAL
            con.execute("INSERT INTO ventas (producto_id, cantidad, total) VALUES (?, ?, ?);", (pid, cant, prod[1] * cant))
            
            if fallar:
                raise RuntimeError("Fallo provocado entre inserción y actualización de inventario.")
                
            con.execute("UPDATE productos SET stock = stock - ? WHERE id = ?;", (cant, pid))
            con.commit()
            print("[OK] Venta registrada con éxito.")
        except Exception as e:
            con.rollback()
            print(f"[ROLLBACK] Transacción cancelada: {e}")
        finally:
            con.close()
    except ValueError:
        print("[Error] Datos inválidos.")

def ver_ventas():
    with conectar() as con:
        ventas = con.execute("""
            SELECT v.id, p.nombre, v.cantidad, v.total, v.fecha 
            FROM ventas v JOIN productos p ON v.producto_id = p.id;
        """).fetchall()
        print("\nID | Producto | Cant. | Total | Fecha")
        for v in ventas:
            print(f"{v[0]} | {v[1]} | {v[2]} | ${v[3]} | {v[4]}")

def menu():
    init_db()
    opciones = {
        "1": registrar_producto, "2": listar_productos, "3": actualizar_producto,
        "4": eliminar_producto, "5": lambda: registrar_venta(False),
        "6": ver_ventas, "7": lambda: registrar_venta(True)
    }
    while True:
        print("\n1.Crear prod | 2.Listar | 3.Actualizar | 4.Eliminar | 5.Venta | 6.Historial JOIN | 7.Test ROLLBACK | 8.Salir")
        op = input("Opción: ").strip()
        if op == "8":
            break
        accion = opciones.get(op)
        if accion:
            accion()
        else:
            print("Opción inválida.")

if __name__== "__main__":
    menu()
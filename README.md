# Parcial Practico: Sistema de Inventario y Ventas

*Asignatura:* Desarrollo de Aplicaciones con Acceso a Datos  
*tecnologias:* Python 3, SQLite 3  

---

## 1. Modelo de Datos y Entidades

Se implementaron dos tablas vinculadas con clave foranea e integridad referencial (ON DELETE RESTRICT):

sql
CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    precio REAL NOT NULL CHECK(precio > 0),
    stock INTEGER NOT NULL CHECK(stock >= 0)
);

CREATE TABLE ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL CHECK(cantidad > 0),
    total REAL NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE RESTRICT
);


---

## 2. Diagrama de Arquitectura e Interaccion

text
+-------------------------------------------------+
|               USUARIO (Terminal)                |
+------------------------+------------------------+
                         |
                         v
+-------------------------------------------------+
|         CAPA DE LOGICA (inventario.py)          |
|  - Menu interactivo y captura de datos          |
|  - Validaciones de stock y consultas con (?)    |
|  - Control transaccional (BEGIN, COMMIT, ROLL)  |
+------------------------+------------------------+
                         |
                         v
+-------------------------------------------------+
|          BASE DE DATOS (tienda.db)              |
|  - Motor SQLite3 con foreign_keys activadas     |
|  - Tablas relacionadas: productos y ventas      |
+-------------------------------------------------+


---

## 3. Explicacion de la Transaccion y Rollback

El registro de ventas cumple con la propiedad de *Atomicidad*:
1. *Validacion:* Se comprueba existencia del producto y stock disponible.
2. *Insercionn de venta:* Se agrega el registro a la tabla ventas.
3. *Actualizacion de inventario:* Se descuenta la cantidad vendida en productos.
4. *Commit:* Si ambas operaciones concluyen sin error, se ejecuta conn.commit().
5. *Rollback:* Si surge una falla entre la insercion y la actualizacion (probado en la opcion 7), se ejecuta de inmediato conn.rollback(), asegurando que no se guarden ventas incompletas ni se descuente el inventario.

---

## 4. Instrucciones de Ejecucion

1. Clonar el repositorio:
   bash
   git clone https://github.com/saryd/sistema-inventario-sqlite.git
   
2. Ejecutar la aplicacion en la terminal:
   bash
   python inventario.py
   
   (o py inventario.py en Windows).

---

## 5. Evidencias de Ejecucion


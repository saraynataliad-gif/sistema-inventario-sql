# Parcial PrÃ¡ctico: Sistema de Inventario y Ventas

*Asignatura:* Desarrollo de Aplicaciones con Acceso a Datos  
*TecnologÃ­as:* Python 3, SQLite 3  

---

## 1. Modelo de Datos y Entidades

Se implementaron dos tablas vinculadas con clave forÃ¡nea e integridad referencial (ON DELETE RESTRICT):

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

## 2. Diagrama de Arquitectura e InteracciÃ³n

text
+-------------------------------------------------+
|               USUARIO (Terminal)                |
+------------------------+------------------------+
                         |
                         v
+-------------------------------------------------+
|         CAPA DE LÃ“GICA (inventario.py)          |
|  - MenÃº interactivo y captura de datos          |
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

## 3. ExplicaciÃ³n de la TransacciÃ³n y Rollback

El registro de ventas cumple con la propiedad de *Atomicidad*:
1. *ValidaciÃ³n:* Se comprueba existencia del producto y stock disponible.
2. *InserciÃ³n de venta:* Se agrega el registro a la tabla ventas.
3. *ActualizaciÃ³n de inventario:* Se descuenta la cantidad vendida en productos.
4. *Commit:* Si ambas operaciones concluyen sin error, se ejecuta conn.commit().
5. *Rollback:* Si surge una falla entre la inserciÃ³n y la actualizaciÃ³n (probado en la opciÃ³n 7), se ejecuta de inmediato conn.rollback(), asegurando que no se guarden ventas incompletas ni se descuente el inventario.

---

## 4. Instrucciones de EjecuciÃ³n

1. Clonar el repositorio:
   bash
   git clone https://github.com/saryd/sistema-inventario-sqlite.git
   
2. Ejecutar la aplicaciÃ³n en la terminal:
   bash
   python inventario.py
   
   (o py inventario.py en Windows).

---

## 5. Evidencias de EjecuciÃ³n

### 1. CreaciÃ³n y consulta de productos
![Registro Productos](01_registro_productos.png)

### 2. Venta exitosa e historial con JOIN
![Venta Join](02_venta_exitosa_join.png)

### 3. Prueba de fallo controlado y verificaciÃ³n con ROLLBACK
![Prueba Rollback](03_prueba_rollback.png)

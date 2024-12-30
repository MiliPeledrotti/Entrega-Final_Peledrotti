import sqlite3

# Crear la base de datos y la tabla productos
def inicializar_bd():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT
        )
    ''')
    conexion.commit()
    conexion.close()

# Función para registrar un nuevo producto
def registrar_producto():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    while True:
        nombre = input("Ingrese el nombre del producto: ").strip()
        if not nombre:
            print("[ERROR] El nombre no puede estar vacío.")
            continue

        descripcion = input("Ingrese una descripción del producto: ").strip()

        try:
            cantidad = int(input("Ingrese la cantidad del producto: "))
            if cantidad < 0:
                print("[ERROR] La cantidad debe ser un número positivo.")
                continue
        except ValueError:
            print("[ERROR] Debe ingresar un número válido para la cantidad.")
            continue

        try:
            precio = float(input("Ingrese el precio del producto: "))
            if precio < 0:
                print("[ERROR] El precio debe ser un número positivo.")
                continue
        except ValueError:
            print("[ERROR] Debe ingresar un número válido para el precio.")
            continue

        categoria = input("Ingrese la categoría del producto: ").strip()

        cursor.execute('''
            INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, descripcion, cantidad, precio, categoria))

        conexion.commit()
        print(f"[INFO] Producto '{nombre}' registrado exitosamente.")
        break

    conexion.close()

# Función para visualizar todos los productos
def visualizar_productos():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    if productos:
        print("\n[INFO] Inventario de productos:")
        for producto in productos:
            print(f"ID: {producto[0]} | Nombre: {producto[1]} | Descripción: {producto[2]} | Cantidad: {producto[3]} | Precio: ${producto[4]} | Categoría: {producto[5]}")
    else:
        print("[INFO] El inventario está vacío.")

    conexion.close()

# Función para actualizar un producto
def actualizar_producto():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    try:
        id_producto = int(input("Ingrese el ID del producto a actualizar: "))
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
        producto = cursor.fetchone()

        if producto:
            print(f"[INFO] Producto actual: Nombre: {producto[1]}, Descripción: {producto[2]}, Cantidad: {producto[3]}, Precio: {producto[4]}, Categoría: {producto[5]}")

            nombre = input("Nuevo nombre (presione Enter para mantener el actual): ").strip() or producto[1]
            descripcion = input("Nueva descripción (presione Enter para mantener la actual): ").strip() or producto[2]
            cantidad = input("Nueva cantidad (presione Enter para mantener la actual): ").strip()
            precio = input("Nuevo precio (presione Enter para mantener el actual): ").strip()
            categoria = input("Nueva categoría (presione Enter para mantener la actual): ").strip() or producto[5]

            cantidad = int(cantidad) if cantidad else producto[3]
            precio = float(precio) if precio else producto[4]

            cursor.execute('''
                UPDATE productos
                SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?
                WHERE id = ?
            ''', (nombre, descripcion, cantidad, precio, categoria, id_producto))

            conexion.commit()
            print(f"[INFO] Producto con ID {id_producto} actualizado exitosamente.")
        else:
            print("[ERROR] No se encontró un producto con ese ID.")

    except ValueError:
        print("[ERROR] ID inválido. Debe ser un número entero.")

    conexion.close()

# Función para eliminar un producto
def eliminar_producto():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    try:
        id_producto = int(input("Ingrese el ID del producto a eliminar: "))
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
        producto = cursor.fetchone()

        if producto:
            cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
            conexion.commit()
            print(f"[INFO] Producto con ID {id_producto} eliminado correctamente.")
        else:
            print("[ERROR] No se encontró un producto con ese ID.")

    except ValueError:
        print("[ERROR] ID inválido. Debe ser un número entero.")

    conexion.close()

# Función para generar reporte de bajo stock
def reporte_bajo_stock():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    try:
        limite = int(input("Ingrese el límite de stock para el reporte: "))
        cursor.execute("SELECT * FROM productos WHERE cantidad < ?", (limite,))
        productos = cursor.fetchall()

        if productos:
            print("\n[INFO] Productos con bajo stock:")
            for producto in productos:
                print(f"ID: {producto[0]} | Nombre: {producto[1]} | Stock actual: {producto[3]}")
        else:
            print(f"[INFO] Todos los productos tienen un stock igual o superior a {limite}.")

    except ValueError:
        print("[ERROR] Debe ingresar un número válido.")

    conexion.close()

# Menú principal
def menu():
    while True:
        print("\n--- Menú de Gestión de Inventario ---")
        print("1. Registrar producto")
        print("2. Visualizar productos")
        print("3. Actualizar producto")
        print("4. Eliminar producto")
        print("5. Reporte de bajo stock")
        print("6. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_producto()
        elif opcion == "2":
            visualizar_productos()
        elif opcion == "3":
            actualizar_producto()
        elif opcion == "4":
            eliminar_producto()
        elif opcion == "5":
            reporte_bajo_stock()
        elif opcion == "6":
            print("[INFO] Saliendo del programa.")
            break
        else:
            print("[ERROR] Opción inválida. Por favor, seleccione una opción válida.")

# Inicializar base de datos y ejecutar el menú
inicializar_bd()
menu()

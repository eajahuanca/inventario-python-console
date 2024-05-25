import datetime

inventario = {}
ventas = []


def registrar_nuevo_inventario():
    print("Ingrese los productos para registrar el inventario. (Deje el nombre vacío para terminar.)")
    while True:
        producto = input("Nombre del producto: ").strip()
        if not producto:
            break
        cantidad = int(input("Cantidad: "))
        precio = float(input("Precio: "))
        actualizar_inventario(producto, cantidad, precio)
    print("Inventario registrado exitosamente.")


def actualizar_inventario(producto, cantidad, precio):
    if producto in inventario:
        inventario[producto]['cantidad'] += cantidad
        inventario[producto]['precio'] = precio
        print(f"Producto {producto} actualizado en inventario. Nueva cantidad: {inventario[producto]['cantidad']}.")
    else:
        inventario[producto] = {'cantidad': cantidad, 'precio': precio}
        print(f"Producto {producto} agregado al inventario.")


def nueva_venta():
    cliente = input("Nombre del cliente: ").strip()
    productos_vendidos = []
    total_venta = 0
    print("Ingrese los productos vendidos. Deje el nombre vacío para terminar.")
    while True:
        producto = input("Nombre del producto: ").strip()
        if not producto:
            break
        if producto not in inventario:
            print(f"El producto {producto} no está en el inventario.")
            continue
        cantidad = int(input("Cantidad: "))
        if cantidad > inventario[producto]['cantidad']:
            print(f"No hay suficiente inventario de {producto} para realizar la venta.")
            continue
        inventario[producto]['cantidad'] -= cantidad
        precio = inventario[producto]['precio']
        total_producto = cantidad * precio
        total_venta += total_producto
        productos_vendidos.append({
            'producto': producto,
            'cantidad': cantidad,
            'precio': precio,
            'subtotal': total_producto
        })
        verificar_inventario(producto)
    if productos_vendidos:
        venta = {
            'cliente': cliente,
            'productos': productos_vendidos,
            'fecha': datetime.datetime.now(),
            'total': total_venta
        }
        ventas.append(venta)
        print(f"Venta registrada para el cliente {cliente}. Total de la venta: Bs{total_venta:.2f}")
    else:
        print("No se registraron productos vendidos.")


def generar_reporte(fecha_inicio, fecha_fin):
    reporte = [venta for venta in ventas if fecha_inicio <= venta['fecha'] <= fecha_fin]
    return reporte


def visualizar_reporte(reporte):
    if reporte:
        cabecera = ["CLIENTE", "FECHA", "PRODUCTO", "CANTIDAD", "PRECIO", "SUBTOTAL", "TOTAL"]
        ancho_columna = [max(len(str(item)) for item in [titulo] + [
            venta['cliente'] if titulo == "CLIENTE" else venta['fecha'].strftime(
                "%Y-%m-%d %H:%M:%S") if titulo == "FECHA" else producto[titulo.lower()] if titulo != "TOTAL" else venta['total'] for venta in reporte for
            producto in venta['productos']]) for titulo in cabecera]

        titulo_fila = " | ".join(titulo.ljust(col_width) for titulo, col_width in zip(cabecera, ancho_columna))
        separador = "-+-".join("-" * col_width for col_width in ancho_columna)
        print(titulo_fila)
        print(separador)
        for venta in reporte:
            for producto in venta['productos']:
                fila = " | ".join(str(venta['cliente'] if titulo == "CLIENTE" else venta['fecha'].strftime(
                    "%Y-%m-%d %H:%M:%S") if titulo == "FECHA" else producto[titulo.lower()] if titulo != "TOTAL" else venta['total']).ljust(col_width) for
                                 titulo, col_width in zip(cabecera, ancho_columna))
                print(fila)
            print(separador)
    else:
        print("No hay ventas en el rango de fechas especificado.")


def verificar_inventario(producto):
    if inventario[producto]['cantidad'] <= -1:
        print(f"Orden necesaria para {producto}. Cantidad actual: {inventario[producto]['cantidad']}")


def opciones_menu(opcion):
    if opcion == '1':
        registrar_nuevo_inventario()
    elif opcion == '2':
        producto = input("Nombre del producto: ")
        cantidad = int(input("Cantidad: "))
        precio = float(input("Precio: "))
        actualizar_inventario(producto, cantidad, precio)
    elif opcion == '3':
        nueva_venta()
    elif opcion == '4':
        fecha_inicio_str = input("Fecha de inicio (YYYY-MM-DD): ")
        fecha_fin_str = input("Fecha de fin (YYYY-MM-DD): ")
        fecha_inicio = datetime.datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
        fecha_fin = datetime.datetime.strptime(fecha_fin_str, "%Y-%m-%d")
        reporte = generar_reporte(fecha_inicio, fecha_fin)
        visualizar_reporte(reporte)
    elif opcion == '5':
        if len(inventario) > 0:
            print("***** Inventario actual: ")
            cabecera = ["PRODUCTO", "CANTIDAD", "PRECIO"]
            ancho_columna = [max(len(str(item)) for item in [titulo] + [
                producto if titulo == "PRODUCTO" else inventario[producto]['cantidad']
                if titulo == "CANTIDAD"
                else inventario[producto]['precio'] for producto in inventario]) for titulo in cabecera]

            titulo_fila = " | ".join(titulo.ljust(col_width) for titulo, col_width in zip(cabecera, ancho_columna))
            separador = "-+-".join("-" * col_width for col_width in ancho_columna)
            print(titulo_fila)
            print(separador)
            for producto in inventario:
                fila = " | ".join(str(producto if titulo == "PRODUCTO" else inventario[producto]['cantidad'] if titulo == "CANTIDAD" else inventario[producto]['precio']).ljust(col_width) for titulo, col_width in zip(cabecera, ancho_columna))
                print(fila)
            print(separador)
        else:
            print("******** Inventario vacío, sin productos")
    elif opcion == '6':
        print("Saliendo del sistema...")
        return False
    else:
        print("Opción no válida. Intente nuevamente.")
    return True


def visualizar_menu():
    print("\n______________________________________________")
    print("______ Sistema de Gestión de Inventario ______")
    print("|        1. Registrar inventario             |")
    print("|        2. Actualizar inventario            |")
    print("|        3. Realizar venta                   |")
    print("|        4. Generar reporte de ventas        |")
    print("|        5. Ver inventario                   |")
    print("|        6. Salir                            |")
    print("______________________________________________")


def main():
    continuar = True
    while continuar:
        visualizar_menu()
        opcion = input("Seleccione una opción: ")
        continuar = opciones_menu(opcion)


if __name__ == "__main__":
    main()

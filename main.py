import os
import platform


from Laboratorio_1 import(
    ProductoElectronico,
    ProductoAlimenticio,
    GestionProducto
)

def limpiar_pantalla():   # Para limpiar la pantalla
    '''Limpiar pantalla según el sistema operativo'''
    if platform.system() == 'Windows':
        os.system('cls')    # Si el SO es Windows
    else:
        os.system('clear')  # Si el SO es Linux o Mac OS
    


def mostrar_menu():
    print("==============================================")
    print("************ GESTION DE PRODUCTOS ************")
    print("==============================================")
    print('1. Agregar Producto Electrónico\n')
    print('2. Agregar Producto Alimenticio\n')
    print('3. Buscar Producto por codigo\n')
    print('4. Actualizar Producto\n')
    print('5. Eliminar Producto por codigo\n')
    print('6. Mostrar todos los productos\n')
    print('7. Salir\n')


def agregar_producto(gestion, tipo_producto):
    try:
        codigo = int(input('Ingrese codigo del producto: '))
        print()
        tipo = input('Ingrese tipo de producto: electronico/alimenticio: ')
        print()
        nombre = input('Ingrese nombre del producto: ')
        print()
        precio = float(input('Ingrese precio del producto: '))
        print()
        cantidad = int(input('Ingrese cantidad del producto: '))
        print()

        if tipo_producto == '1':
            añosGarantia = int(input('Ingrese años de garantia: '))
            producto = ProductoElectronico(codigo, tipo, nombre, precio, cantidad, añosGarantia)
        elif tipo_producto == '2':
            fechaVencimiento = int(input('Ingrese Fecha de Vencimiento: '))
            producto = ProductoAlimenticio(codigo, tipo, nombre, precio, cantidad, fechaVencimiento)
        else:
            print('Opcion invalida')
            return
        
        gestion.crear_producto(producto)

        input('Presione enter para continuar')
    
    except ValueError as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f'Error inesperado; {e}')


def buscar_producto_por_codigo(gestion):
    codigo = input('Ingrese el codigo del producto')
    print()
    gestion.buscar_producto(codigo)
    input('Presione enter para continuar')

def actualizar_precio_producto(gestion):
    codigo = input('Ingrese codigo de producto para actualizar precio: ')
    print()
    precio = float(input('Ingrese el precio del producto: '))
    print()
    gestion.actualizar_precio(codigo, precio)
    input('Presione enter para continuar')

def eliminar_producto(gestion):
    codigo = input('Ingrese codigo de producto para eliminar: ')
    print()
    gestion.eliminar_producto(codigo)
    input('Presione enter para continuar')

def mostrar_todos_los_productos(gestion):
    for producto in gestion.leer_datos().values():
        if 'añosGarantia' in producto:
            print(f"{producto['nombre']} añosGarantia {producto['añosGarantia']}")
        else:
            print(f"{producto['nombre']} añosGarantia {producto['fechaVencimiento']}")
    input('Presione enter para continuar')

if __name__ == "__main__":

    archivo_productos = 'productos_store.json'
    gestion_productos = GestionProducto(archivo_productos)

    while True:     # Esta parte del código va a mostrar el menú y va a capturar
                    # la opción que elija el usuario
        limpiar_pantalla()
        mostrar_menu()
        opcion = input('Ingrese una opción: ')
        print()

        if opcion == '1' or opcion == '2':
            agregar_producto(gestion_productos, opcion)
        
        elif opcion == '3':
            buscar_producto_por_codigo(gestion_productos)
        
        elif opcion == '4':
            actualizar_precio_producto(gestion_productos)

        elif opcion == '5':
            eliminar_producto(gestion_productos)
        
        elif opcion == '6':
            mostrar_todos_los_productos(gestion_productos)
        
        elif opcion == '7':
            print('Saliendo del programa...')
            break

        else:
            print('Opción No Válida')
            print()




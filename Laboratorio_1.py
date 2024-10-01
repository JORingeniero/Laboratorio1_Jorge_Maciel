# Sistema de Gestión de Productos
# Objetivo: Desarrollar un sistema para manejar productos en un inventario.
#Requisitos:

# 1.Crear una clase base Producto con atributos como nombre, precio, cantidad en stock, etc.
# 2.Definir al menos 2 clases derivadas para diferentes categorías de productos (por ejemplo, ProductoElectronico, ProductoAlimenticio) con atributos y métodos específicos.
# 3.Implementar operaciones CRUD para gestionar productos del inventario.
# 4.Manejar errores con bloques try-except para validar entradas y gestionar excepciones.
# 5.Persistir los datos en archivo JSON.

# Defino la clase base Producto
# Defino los siguientes atributos:
# a- Código: de ocho dígitos. Cada producto, independientemente de su tipo, tiene un código distinto
# b- tipo: electrónico, alimenticio
# c- nombre: nombre del producto
# d- precio: precio del producto en pesos
# e- cantidad: disponibilidad en stock

import mysql.connector
from mysql.connector import Error
from decouple import config
from datetime import datetime


import json

class Producto:

    def __init__(self, codigo, tipo, nombre, precio, cantidad):
        self.__codigo = self.validar_codigo(codigo)
        self.__tipo = tipo
        self.__nombre = nombre
        self.__precio = self.validar_precio(precio)
        self.__cantidad = self.validar_cantidad(cantidad)
    
        # Al estar nuestros atributos protegidos, debemos crear los métodos para que puedan ser accedidos desde otra clase

    @property #Con property convertimos el atributo en una propiedad
    def codigo(self):
        return self.__codigo 
    
    @property #Con property convertimos el atributo en una propiedad
    def tipo(self):
        return self.__tipo
    
    @property
    def nombre(self):
        return self.__nombre.capitalize()
    
    @property
    def precio(self):
        return self.__precio
    
    @property
    def cantidad(self):
        return self.__cantidad

    # Convertimos en propiedad todos nuestros atributos protejidos
    # El property es solamente para consultas. Es el getter
    # Para modificar los datos utilizamos el setter
    # Con el setter podemos realizar una modificación de los valores recibidos para guardarlo en el Json
    # Vamos a validar primero el precio. El precio del producto no puede ser negativo.

    # Setters (corrección del profe)
    
    @precio.setter #Convierte a la función en un setter propiamente dicho
    def precio (self, nuevo_precio):
        self.__precio = self.validar_precio(nuevo_precio)

    @cantidad.setter
    def cantidad (self, nueva_cantidad):
        self.__cantidad = self.validar_cantidad(nueva_cantidad)
    
    # Métodos de validación

    def validar_precio(self, precio):
        try:
            precio_num = float(precio)
            if precio_num < 0:
                raise ValueError ('El precio debe ser un numero positivo')
            return precio_num
        except ValueError:
            raise ValueError ('El precio debe ser una cifra válida')
        

    def validar_cantidad(self, cantidad):
        try:
            cantidad_num = int(cantidad)
            if cantidad_num < 0:
                raise ValueError ('La cantidad debe ser un número positivo')
            return cantidad_num
        except ValueError:
            raise ValueError ('La cantidad debe ser una cifra válida')
        
    def validar_codigo(self, codigo):
        try:
            codigo_num = int(codigo)
            if len(str(codigo)) != 8:
                raise ValueError("El codigo debe ser de 8 dígitos")
            return codigo_num
            
        except ValueError:
            raise ValueError("El codigo debe ser numérico y estar compuesto por 8 dígitos")

    # Creo un método para guardar estos atributos en un diccionario 
    
    def to_dict(self):
        return {
            "codigo": self.codigo,
            "tipo": self.tipo,
            "nombre": self.nombre,
            "precio": self.precio,
            "cantidad": self.cantidad

        }
    
    def __str__(self):
        return f"{self.tipo} {self.nombre}"
    
class ProductoElectronico(Producto):
    def __init__(self, codigo, tipo, nombre, precio, cantidad, añosGarantia):
        super().__init__(codigo, tipo, nombre, precio, cantidad)
        self.__añosGarantia = self.validar_añosGarantia(añosGarantia)
    
    @property
    def añosGarantia (self):
        return self.__añosGarantia
    
    def validar_añosGarantia(self, añosGarantia):
        try:
            añosGarantia_num = int(añosGarantia)
            if añosGarantia_num < 1:
                raise ValueError ('La garantía mínima es de un año')
            return añosGarantia_num
        except ValueError:
            raise ValueError ('Años de Garantía debe ser una cifra válida')

    def to_dict(self):
        data = super().to_dict()
        data['añosGarantia'] = self.añosGarantia
        return data
    
    def __str__(self):
        return f'{super().__str__()} - añosGarantia: {self.añosGarantia}'

class ProductoAlimenticio(Producto):
    def __init__(self, codigo, tipo, nombre, precio, cantidad, fechaVencimiento):
        super().__init__(codigo, tipo, nombre, precio, cantidad)
        self.__fechaVencimiento = self.validar_fecha_vencimiento(fechaVencimiento)
    
    
    @property
    def fechaVencimiento (self):
        return self.__fechaVencimiento
    
        
    def to_dict(self):
        data = super().to_dict()
        data['fechaVencimiento'] = self.fechaVencimiento
        return data
        
    def __str__(self):
        return f'{super().__str__()} - fechaVencimiento: {self.fechaVencimiento}'

class GestionProducto():
    def __init__(self):
        self.host = config ('Db_Host')
        self.database = config ('Db_Name')
        self.user = config ('Db_User')
        self.password = config ('Db_Password') 
        self.port = config ('Db_port')
    
    def connect(self):
        '''Establecer una conexión con la base de datos'''
        try:
            connection = mysql.connector.connect(
                host= self.host,
                database= self.database,
                user= self.user,
                password= self.password,
                port= self.port
            )

            if connection.is_connected():
                return connection

        except Error as e:
            print(f'Error al conectar a la base de datos: {e}')
            return None
            


    # Este método lo único que hace es leer los datos del archivo
    # Con open(self.archivo) accedemos al archivo en modo lectura ('r')

    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file) #leemos el archivo json y lo disponibilizamos en un 
                                        # objeto (datos) para poder manejarlo desde python
        except FileNotFoundError:
            return {}
        except Exception as error:
            raise Exception(f'Error al leer los datos del archivo: {error}')
        else:
            return datos
        
        # Con este método guardamos los datos

    def guardar_datos(self, datos):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=4) #ident=4 son los espacios que se dejan desde el margen izquierdo
                                                #facilita la lectura. 4 es un valor estandard
        except IOError as error:
            print(f'Error al intentar guardar los datos en {self.archivo}: (error)')
            print()
        except Exception as error:
            print(f'Error inesperado: {error}')
            print()

    def crear_producto(self,producto):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    # Se verifica si el producto ya existe a través de su código
                    cursor. execute('select codigo from producto where codigo = %s', (producto.codigo,))
                    if cursor.fetchone():
                        print(f'Error: ya existe un producto con codigo {producto.codigo}')
                        return
                    # Crear producto según su tipo (Alimenticio/Electrónico)
                    if isinstance(producto, ProductoElectronico):
                        query = '''
                        INSERT INTO producto (codigo, tipo, nombre, precio, cantidad)
                        VALUES (%s, %s, %s, %s, %s)
                        '''
                        cursor.execute(query, (producto.codigo, producto.tipo, producto.nombre, producto.precio, producto.cantidad))
                        
                        query = '''
                        INSERT INTO productoelectronico (codigo, añosGarantia)
                        VALUES (%s, %s)
                        '''
                        cursor.execute(query, (producto.codigo, producto.añosGarantia))
                    
                    elif isinstance(producto, ProductoAlimenticio):

                        query = '''
                        INSERT INTO producto (codigo, tipo, nombre, precio, cantidad)
                        VALUES (%s, %s, %s, %s, %s)
                        '''
                        cursor.execute(query, (producto.codigo, producto.tipo, producto.nombre, producto.precio, producto.cantidad))

                        query = '''
                        INSERT INTO productoalimenticio (codigo, fechaVencimiento)
                        VALUES (%s, %s)
                        '''
                        cursor.execute(query, (producto.codigo, producto.fechaVencimiento))
                    
                    connection.commit()
                    print()
                    print(f'Producto tipo {producto.tipo} : -> {producto.nombre} creado exitosamente')

            
        except Exception as error:
            print (f'Error inesperado al crear producto: {error}')
            print()

    def buscar_producto(self, codigo):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute('SELECT * FROM producto WHERE codigo = %s', (codigo,))
                    producto_data = cursor.fetchone()
                    
                    if producto_data:
                        cursor.execute('SELECT añosGarantia FROM productoelectronico WHERE codigo = %s', (codigo,))
                        añosGarantia = cursor.fetchone()

                        if añosGarantia:
                            producto_data['añosGarantia'] = añosGarantia['añosGarantia']
                            producto = ProductoElectronico(**producto_data)
                        
                        else:
                            cursor.execute('SELECT fechaVencimiento FROM productoalimenticio WHERE codigo = %s', (codigo,))
                            fechaVencimiento = cursor.fetchone()

                            if fechaVencimiento:
                                producto_data['fechaVencimiento'] = fechaVencimiento['fechaVencimiento']
                                producto = ProductoAlimenticio(**producto_data)
                            
                            else:
                                producto = Producto(**producto_data)
                        
                        print()
                        print(f'Producto encontrado: -> {producto} Código: -> {codigo}')
                    
                    else:
                        print()
                        print(f'No se encontró Producto con Código: -> {codigo}')
            
        
        except Error as e:
            print('Error al buscar producto: {e}')
        finally:
            if connection.is_connected():
                connection.close()

    def actualizar_precio(self, codigo, nuevo_precio):
        '''Actualizar el precio de un producto en la base de datos'''
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    # Verificar si el código del producto existe
                    cursor.execute('SELECT * FROM producto WHERE codigo = %s', (codigo,))
                    if not cursor.fetchone():
                        print()
                        print(f'No se encuentra producto con código -> {codigo}')
                        return
                    
                    # Si el código del producto existe en la base de datos, procedemos a actualizar su precio
                    cursor.execute('UPDATE producto SET precio = %s WHERE codigo = %s', (nuevo_precio, codigo))

                    if cursor.rowcount > 0:
                        connection.commit()
                        print()
                        print(f'El precio fue actualizado correctamente al valor -> $ {nuevo_precio}')
                    else:
                        print()
                        print(f'No se encontró producto con código -> {codigo}')
                    
        except Exception as e:
            print(f'Error al actualizar precio: {e}')
        finally:
            if connection.is_connected():
                connection.close()
                
    def eliminar_producto(self, codigo):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    # Verificar si el código del producto existe
                    cursor.execute('SELECT * FROM producto WHERE codigo = %s', (codigo,))
                    if not cursor.fetchone():
                        print()
                        print(f'No se encuentra producto con codigo -> {codigo}')
                        return
                    
                    # Si el producto existe, eliminamos dicho producto
                    cursor.execute('DELETE FROM productoelectronico WHERE codigo = %s', (codigo,))
                    cursor.execute('DELETE FROM productoalimenticio WHERE codigo = %s', (codigo,))
                    cursor.execute('DELETE FROM producto WHERE codigo = %s', (codigo,))
                    if cursor.rowcount > 0:
                        connection.commit()
                        print()
                        print(f'El producto con código -> {codigo} fue eliminado de la base de datos')
                    else:
                        print()
                        print(f'No se encontró producto con código -> {codigo}')
                        
        except Exception as e:
            print(f'Error al eliminar producto: {e}')
        
        finally:
            if connection.is_connected():
                connection.close()

    def leer_todos_los_productos(self):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary = True) as cursor:
                    cursor.execute('SELECT * FROM producto')
                    productos_data = cursor.fetchall()

                    productos = []
                    for producto_data in productos_data:
                        codigo = producto_data['codigo']

                        cursor.execute('SELECT añosGarantia FROM productoelectronico WHERE codigo = %s', (codigo,))
                        añosgarantia = cursor.fetchone()

                        if añosgarantia:
                            producto_data['añosGarantia'] = añosgarantia['añosGarantia']
                            producto = ProductoElectronico(**producto_data)
                        
                        else:
                            cursor.execute('SELECT fechaVencimiento FROM productoalimenticio WHERE codigo = %s', (codigo,))
                            fechavencimiento = cursor.fetchone()
                            producto_data['fechaVencimiento'] = fechavencimiento['fechaVencimiento']
                            producto = ProductoAlimenticio(**producto_data)

                        productos.append(producto)
                        
        except Exception as e:
            print(f'Error al mostrar todos los productos: {e}')
        
        else:
            return productos
        
        finally:
            if connection.is_connected():
                connection.close()
        



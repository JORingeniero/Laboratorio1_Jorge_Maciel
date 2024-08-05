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

    @precio.setter #Convierte a la función en un setter propiamente dicho
    def precio (self, nuevo_precio):
        self.__precio = self.validar_precio(nuevo_precio)

    def validar_precio(self, precio):
        try:
            precio_num = float(precio)
            if precio_num < 0:
                raise ValueError ('El precio debe ser un número positivo')
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
                raise ValueError("El código debe ser de 8 dígitos")
            
        except ValueError:
            raise ValueError("El código debe ser numérico y estar compuesto por 8 dígitos")

# Creo un método para guardar estos atributos en un diccionario (archivo Json)
    
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
        self.__fechaVencimiento = self.validar_fechaVencimiento(fechaVencimiento)
    
    @property
    def fechaVencimiento (self):
        return self.__fechaVencimiento
    
    def validar_fechaVencimiento(self, fechaVencimiento):
        try:
            añosGarantia_num = int(fechaVencimiento)
            if añosGarantia_num < 1:
                raise ValueError ('Ingresar fecha de vencimiento en formato DD/MM/AAAA')
            return añosGarantia_num
        except ValueError:
            raise ValueError ('Años de Garantía debe ser una fecha válida')

    def to_dict(self):
        data = super().to_dict()
        data['fechaVencimiento'] = self.fechaVencimiento
        return data
    
    def __str__(self):
        return f'{super().__str__()} - fechaVencimiento: {self.fechaVencimiento}'

class GestionProducto():
    def __init__(self, archivo):
        self.archivo = archivo

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
                json.dump(datos, file, ident=4) #ident=4 son los espacios que se dejan desde el margen izquierdo
                                                #facilita la lectura. 4 es un valor estandard
        except IOError as error:
            print(f'Error al intentar guardar los datos en {self.archivo}: (error)')
            print()
        except Exception as error:
            print(f'Error inesperado: {error}')
            print()

    def crear_producto(self,producto):
        try:
            datos = self.leer_datos()
            codigo = producto.codigo
            if not (codigo) in datos.keys():
                datos[codigo] = producto.to_dic()
                self.guardar_datos(datos)
                print(f'El producto: {producto} fue guardado exitosamente')
                print()
            else:
                print(f'El producto: {producto} ya existe en archivo')
                print()

        except Exception as error:
            print (f'Error inesperado al crear producto: {error}')
            print()

    def buscar_producto(self, codigo):
        try:
            datos = self.leer_datos()
            if codigo in datos:
                producto_data = datos[codigo]
                if 'añosGarantia' in producto_data:
                    producto = ProductoElectronico(**producto_data)
                else:
                    producto = ProductoAlimenticio(**producto_data)
                print(f'Producto encontrado con codigo: {codigo}')
                print()
            else:
                print(f'Producto no encontrado con codigo: {codigo}')
                print()
        
        except Exception as e:
            print('Error al buscar producto: {e}')

    def actualizar_precio(self, codigo, nuevo_precio):
        try:
            datos = self.leer_datos()
            if int(codigo) in datos.keys():
                datos[codigo]['precio'] = nuevo_precio
                self.guardar_datos(datos)
                print(f'precio del producto: {codigo} actualizado correctamente')
                print()
            else:
                print(f'No se encontro producto con el codigo: {codigo}')
                print()
            
        except Exception as e:
            print(f'Error al actualizar precio: {e}')

    def eliminar_producto(self, codigo):
        try:
            datos = self.leer_datos()
            if int(codigo) in datos.keys():
                del datos[codigo]
                self.guardar_datos(datos)
                print(f'Producto con codigo: {codigo} eliminado correctamente')
                print()
            else:
                print(f'No se encontro producto con el codigo: {codigo}')
                print()
            
        except Exception as e:
            print(f'Error al eliminar producto: {e}')

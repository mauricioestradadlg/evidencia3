from pymongo import MongoClient, errors

def conexionMongo():
    try:
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        client.server_info()  
        database = client['tiendaVideojuegos']  
        print("Te pudiste conectar con MongoDB.")  
        return database  
    except errors.ServerSelectionTimeoutError as error:
        print("No pudiste conectarte a MongoDB:", error)  
        return None 

def crearBaseDeDatos():
    database = conexionMongo()
    if database is None:
        return
    juegos_collection = database['juegos']
    ventas_collection = database['ventas']
    
    # Datos de la tabla de juegos
    juegos_data = [
        {
            "id_juego": 1000,
            "titulo": "The Last of Us Parte II Remastered",
            "desarrollador": "Naughty Dog",
            "fecha_lanzamiento": "19/04/2024",
            "plataformas": ["PS5", "Steam"],
            "clasificacion": "M",
            "precio": 1000.00,
            "stock_disponible": 10
        },
        {
            "id_juego": 1001,
            "titulo": "The Last of Us Parte I Remastered",
            "desarrollador": "Naughty Dog",
            "fecha_lanzamiento": "02/09/2022",
            "plataformas": ["PS5", "Steam"],
            "clasificacion": "M",
            "precio": 700.00,
            "stock_disponible": 8
        },
        {
            "id_juego": 1002,
            "titulo": "Suicide Squad Kill the Justice League",
            "desarrollador": "Rocksteady Studios",
            "fecha_lanzamiento": "30/01/2024",
            "plataformas": ["PS5", "Xbox", "Steam"],
            "clasificacion": "M",
            "precio": 300.00,
            "stock_disponible": 15
        },
        {
            "id_juego": 1003,
            "titulo": "Call of Duty Black Ops 6",
            "desarrollador": "Treyarch",
            "fecha_lanzamiento": "25/10/2024",
            "plataformas": ["PS5", "Xbox", "Steam"],
            "clasificacion": "M",
            "precio": 1200.00,
            "stock_disponible": 15
        },
        {
            "id_juego": 1004,
            "titulo": "Call of Duty Modern Warfare III",
            "desarrollador": "Sledgehammer Games",
            "fecha_lanzamiento": "10/11/2023",
            "plataformas": ["PS5", "Xbox", "Steam"],
            "clasificacion": "M",
            "precio": 900.00,
            "stock_disponible": 5
        },
        {
            "id_juego": 1005,
            "titulo": "Call of Duty Modern Warfare II",
            "desarrollador": "Infinity Ward",
            "fecha_lanzamiento": "28/10/2022",
            "plataformas": ["PS5", "Xbox", "Steam"],
            "clasificacion": "M",
            "precio": 800.00,
            "stock_disponible": 10
        }
    ]

    # Datos de la tabla de ventas
    ventas_data = [
        {
            "id_venta": 2000,
            "id_juego": 1000,
            "fecha_venta": "02/05/2025",
            "total_venta": 1000.00
        },
        {
            "id_venta": 2001,
            "id_juego": 1001,
            "fecha_venta": "02/05/2025",
            "total_venta": 700.00
        },
        {
            "id_venta": 2002,
            "id_juego": 1002,
            "fecha_venta": "02/05/2025",
            "total_venta": 300.00
        },
        {
            "id_venta": 2003,
            "id_juego": 1003,
            "fecha_venta": "02/05/2025",
            "total_venta": 1200.00
        },
        {
            "id_venta": 2004,
            "id_juego": 1004,
            "fecha_venta": "02/05/2025",
            "total_venta": 900.00
        },
        {
            "id_venta": 2005,
            "id_juego": 1005,
            "fecha_venta": "02/05/2025",
            "total_venta": 800.00
        }
    ]

    try:
        # Insertar datos solo si las colecciones están vacías
        if juegos_collection.count_documents({}) == 0:
            juegos_collection.insert_many(juegos_data)
            print("Colección 'juegos' creada y datos insertados.")
        else:
            print("La colección 'juegos' ya tiene datos.")

        if ventas_collection.count_documents({}) == 0:
            ventas_collection.insert_many(ventas_data)
            print("Colección 'ventas' creada y datos insertados.")
        else:
            print("La colección 'ventas' ya tiene datos.")
        
    except Exception as error:
        print("Error al insertar los datos:", error)



def line():
    print("_____________________________")

def space():
    print("\n \n")    


def juegoMasVendido():
    database = conexionMongo()
    if database is None:
        return  # Si no se pudo conectar, salir de la función

    ventas_collection = database['ventas']
    juegos_collection = database['juegos']

    try:
        # Obtener todos los registros de ventas
        ventas = ventas_collection.find()

        # Contar las ventas por id_juego
        contarJuegos = {}

        for venta in ventas:
            id_juego = venta.get("id_juego")
            if id_juego in contarJuegos:
                contarJuegos[id_juego] += 1
            else:
                contarJuegos[id_juego] = 1

        if not contarJuegos:
            print("No hay registros de ventas.")
            return

        # Encontrar el id_juego más vendido
        id_mas_vendido = max(contarJuegos, key=contarJuegos.get)
        total_ventas = contarJuegos[id_mas_vendido]

        # Buscar el título del juego en la colección 'juegos'
        juego = juegos_collection.find_one({"id_juego": id_mas_vendido})

        if juego:
            titulo = juego.get("titulo", "Título no encontrado")
            print(f"Juego más vendido del catálogo: {titulo}")
            print(f"Total de ventas: {total_ventas}")
        else:
            print(f"No se encontró el juego con id_juego {id_mas_vendido} en la colección 'juegos'.")
    except Exception as error:
        print("Ocurrió un error al consultar las ventas o juegos:", error)



def juegoMasBarato():
    database = conexionMongo()
    if database is None:
        return  # Si no se pudo conectar, salir de la función
    juegos_collection = database['juegos']
    try:
        # Encontrar el juego con el precio más bajo
        juego_barato = juegos_collection.find_one(sort=[("precio", 1)])  # ordena por precio ascendente y toma el primero
        if juego_barato:
            titulo = juego_barato.get("titulo", "Título no encontrado")
            precio = juego_barato.get("precio", "Precio no disponible")
            print(f"Juego más barato del catálogo: {titulo}")
            print(f"Precio: ${precio}")
        else:
            print("No se encontraron juegos en la colección.")
    except Exception as error:
        print("Ocurrió un error al consultar la colección de juegos:", error)


def juegoMenosVendidoPS5():
    print('juego menos vendido PS5')

def insertarVenta():
    database = conexionMongo()
    if database is None:
        return  # Si no se pudo conectar, salir de la función

    collection = database['ventas']  # Usar la colección 'ventas'
    try:
        # Capturar los datos de la venta
        id_venta = int(input("ID de la venta: "))
        id_juego = int(input("ID del juego vendido: "))
        fecha_venta = input("Fecha de la venta (dd/mm/yyyy): ")
        total_venta = float(input("Total de la venta: "))

        nueva_venta = {  # Crear el documento con los datos ingresados
            "id_venta": id_venta,
            "id_juego": id_juego,
            "fecha_venta": fecha_venta,
            "total_venta": total_venta
        }

        resultado = collection.insert_one(nueva_venta)  # Insertar en la colección
        print("¡Venta agregada exitosamente!")
        print("ID de la nueva venta:", resultado.inserted_id)
    except Exception as error:
        print("Ocurrió un error al insertar la venta:", error)



def addGame():
    database = conexionMongo()
    if database is None:
        return  # No hace nada si no existe la base de datos

    collection = database['juegos']
    try:
        print("Por favor, ingresa los datos del nuevo juego:")
        
        # Solicitud de datos al usuario
        id_juego = int(input("ID del juego: "))
        titulo = input("Título: ")
        desarrollador = input("Desarrollador: ")
        fecha_lanzamiento = input("Fecha de lanzamiento (dd/mm/aaaa): ")
        
        # Separa cada plataforma en un arreglo despues de identificar la coma
        plataformas_input = input("Plataformas (separadas por coma): ")
        plataformas = [plataforma.strip() for plataforma in plataformas_input.split(",")]
        
        clasificacion = input("Clasificación (E, T, M, etc.): ")
        precio = float(input("Precio: "))
        stock_disponible = int(input("Stock disponible: "))

        # Diccionario del nuevo juego
        new_game = {
            "id_juego": id_juego,
            "titulo": titulo,
            "desarrollador": desarrollador,
            "fecha_lanzamiento": fecha_lanzamiento,
            "plataformas": plataformas,
            "clasificacion": clasificacion,
            "precio": precio,
            "stock_disponible": stock_disponible
        }

        # Insertar el nuevo juego en la colección
        result = collection.insert_one(new_game)
        
        print("Juego agregado exitosamente al catálogo!")
        print("ID del nuevo juego en MongoDB:", result.inserted_id)
    except Exception as error:
        print("Ocurrió un error al intentar agregar el juego:", error)



# Menu Principal del programa

def  mainMenu():
    global ciclo
    line()
    space()
    print("EVIDENCIA 3 - BASES DE DATOS")
    space()
    print("Presiona 1 para buscar el juego con más ventas de la tienda")
    print("Presiona 2 para buscar el juego mas barato del catálogo")
    print("Presiona 3 para buscar el videojuego con menos ventas que sea exclusivo de Playstation")
    print("Presiona 4 para hacer una venta")
    print("Presiona 5 para añadir un juego al catalogo")
    print("Presiona 6 para salir ")
    space()

    start = int(input("Selecciona una opcion: "))
      
    if start == 1:
        space()
        juegoMasVendido()

    elif start == 2:
        space()
        juegoMasBarato()

    elif start == 3:
        space()
        juegoMenosVendidoPS5()

    elif start == 4:
        space()
        insertarVenta()

    elif start == 5:
        space()
        addGame()

    elif start == 6:
        ciclo = False    



#Codigo MAIN

ciclo = True

while(ciclo):
    mainMenu()

# llamada a la funcion
#crearBaseDeDatos()


from pymongo import MongoClient, errors

# funcion para conectarse a la base de datos
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

# funcion para crear la base de datos y las colecciones
def crearBaseDeDatos():
    database = conexionMongo()
    if database is None:
        return
    juegos_collection = database['juegos']
    ventas_collection = database['ventas']
    
    # Diccionario coleccion juegos
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

    # Diccionario coleccion ventas
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
        # Insertar datos solo si la coleccion de juegos es null
        if juegos_collection.count_documents({}) == 0:
            juegos_collection.insert_many(juegos_data)
            print("Colección 'juegos' creada y datos insertados.")
        else:
            print("La colección 'juegos' ya tiene datos.")
        # Insertar datos solo si la coleccion de ventas es null
        if ventas_collection.count_documents({}) == 0: 
            ventas_collection.insert_many(ventas_data)
            print("Colección 'ventas' creada y datos insertados.")
        else:
            print("La colección 'ventas' ya tiene datos.")
        
    except Exception as error:
        print("Error al insertar los datos:", error)


# funcion para imprimir linea
def line():
    print("_____________________________")

# funcion para imprimir espacio
def space():
    print("\n \n")    


def juegoMasVendido():
    database = conexionMongo()
    if database is None:
        return  # Si no se pudo conectar, sale de la función

    ventas_collection = database['ventas']
    juegos_collection = database['juegos']

    try:
        # Obtener todos los registros de ventas
        ventas = ventas_collection.find()

        # Contar las ventas por id_juego
        contarJuegos = {}

        # busca todos los registros de ventas mediante un ciclo For contando el id del juego
        for venta in ventas:
            id_juego = venta.get("id_juego")
            if id_juego in contarJuegos:
                contarJuegos[id_juego] += 1
            else:
                contarJuegos[id_juego] = 1

        if not contarJuegos:
            print("No hay registros de ventas.")
            return

        # Encontrar el id_juego más vendido mediante la función max
        id_mas_vendido = max(contarJuegos, key=contarJuegos.get)
        total_ventas = contarJuegos[id_mas_vendido]

        # Buscar el título del juego en la coleccion de juegos que coincida con el id de la venta
        juego = juegos_collection.find_one({"id_juego": id_mas_vendido})


        if juego:
            # parametros: nombre del atributo, valor por defecto si no se encuentra el atributo
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
        juego_barato = juegos_collection.find_one(sort=[("precio", 1)])  # ordena por precio ascendente y toma el primer valor encontrado
        if juego_barato:
            # parametros: nombres de atributos, valores por defecto si no se encuentran los atributos
            titulo = juego_barato.get("titulo", "Título no encontrado")
            precio = juego_barato.get("precio", "Precio no disponible")
            print(f"Juego más barato del catálogo: {titulo}")
            print(f"Precio: ${precio}")
        else:
            print("No se encontraron juegos en la colección.")
    except Exception as error:
        print("Ocurrió un error al consultar la colección de juegos:", error)


def juegoMenosVendidoPS5():
    database = conexionMongo()
    if database is None:
        return  # Si no se pudo conectar, salir de la función

    ventasCollection = database['ventas']
    juegosCollection = database['juegos']

    try:
        # Obtener todos los registros de ventas
        ventas = ventasCollection.find()

        # Contar las ventas por id_juego
        contarJuegos = {}

        # busca todos los registros de ventas mediante un ciclo For contando el id del juego
        for venta in ventas:
            id_juego = venta.get("id_juego")
            if id_juego in contarJuegos:
                contarJuegos[id_juego] += 1
            else:
                contarJuegos[id_juego] = 1

        if not contarJuegos:
            print("No hay registros de ventas.")
            return

        # Filtrar juegos que están disponibles SOLO en PS5 y Steam
        juegos_validos = juegosCollection.find({
            "plataformas": {"$all": ["PS5", "Steam"]},  # debe contener PS5 y Steam
            "$expr": {"$eq": [{"$size": "$plataformas"}, 2]}  # nada mas busca los 2 elementos del arreglo correspondientes
        })

        # Crear una lista de id's válidos
        ids_juegos_validos = [juego["id_juego"] for juego in juegos_validos]

        # Filtra la variable contarJuegos solo con los juegos válidos
        contarJuegosFiltrados = {id_juego: contarJuegos.get(id_juego, 0) for id_juego in ids_juegos_validos}

        # condicional en caso de que no haya juegos disponibles solo en PS5 y Steam
        if not contarJuegosFiltrados:
            print("No hay ventas registradas de juegos disponibles solo en PS5 y Steam.")
            return

        # Encontrar el id del juego con menos ventas en las plataformas PS5 y Steam
        id_menos_vendido = min(contarJuegosFiltrados, key=contarJuegosFiltrados.get)
        total_ventas = contarJuegosFiltrados[id_menos_vendido]

        # Buscar el título del juego en la colección 'juegos' que coincida con el id de la venta
        juego = juegosCollection.find_one({"id_juego": id_menos_vendido})

        if juego:
            titulo = juego.get("titulo", "Título no encontrado")
            print(f"Juego menos vendido (solo en PS5 y Steam): {titulo}")
            print(f"Total de ventas: {total_ventas}")
        else:
            print(f"No se encontró el juego con id_juego {id_menos_vendido} en la colección 'juegos'.")

    except Exception as error:
        print("Ocurrió un error al consultar las ventas o juegos:", error)


def insertarVenta():
    database = conexionMongo()
    if database is None:
        return  # Si no se pudo conectar, salir de la función

    ventas_collection = database['ventas']  # Colección de ventas
    juegos_collection = database['juegos']  # Colección de juegos

    try:
        # Capturar los datos de la venta
        id_venta = int(input("ID de la venta: "))
        id_juego = int(input("ID del juego vendido: "))
        fecha_venta = input("Fecha de la venta (dd/mm/yyyy): ")
        total_venta = float(input("Total de la venta: "))

        # Verificar si el juego existe en el catálogo
        juego = juegos_collection.find_one({"id_juego": id_juego})
        if juego is None:
            print(f"No se encontró ningún juego con ID {id_juego} en el catálogo.")
            return

        # Verificar si hay stock disponible
        stock_actual = juego.get("stock_disponible", 0)
        if stock_actual <= 0:
            print(f"Ya no queda stock disponible para: {juego.get('titulo', 'Sin título')}.")
            return

        # Insertar la venta en la colección de ventas
        nueva_venta = {
            "id_venta": id_venta,
            "id_juego": id_juego,
            "fecha_venta": fecha_venta,
            "total_venta": total_venta
        }

        resultado = ventas_collection.insert_one(nueva_venta)
        print("¡Venta agregada exitosamente!")
        print("ID de la nueva venta:", resultado.inserted_id)

        # Se actualiza el stock del juego vendido (disminuye en 1)
        nuevo_stock = stock_actual - 1
        if nuevo_stock > 0:
            juegos_collection.update_one(
                {"id_juego": id_juego},
                {"$set": {"stock_disponible": nuevo_stock}}
            )
            print(f"Stock actualizado: '{juego.get('titulo')}': {nuevo_stock} piezas")
        else:
            # Si el stock es 0, eliminar el juego del catálogo
            juegos_collection.delete_one({"id_juego": id_juego})
            print(f"El juego '{juego.get('titulo')}' se agotó y fue eliminado del catálogo.")

    except Exception as error:
        print("Ocurrió un error al insertar la venta o actualizar el catálogo:", error)




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


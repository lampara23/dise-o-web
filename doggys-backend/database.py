import os
from pymongo import MongoClient
from dotenv import load_dotenv

print("🔍 Iniciando database.py...")

# Cargar variables de entorno
load_dotenv()

# Usar la URL directamente
MONGODB_URL = "mongodb+srv://doggysadmin:doggys123@cluster0.blllguo.mongodb.net/doggys"
print(f"🔗 URL de MongoDB: {MONGODB_URL}")

try:
    print("🔄 Intentando conectar a MongoDB Atlas...")
    client = MongoClient(MONGODB_URL)
    # Probar la conexión
    client.admin.command('ping')
    print("✅ Conexión a MongoDB Atlas exitosa")
except Exception as e:
    print(f"❌ Error conectando a MongoDB: {e}")
    raise

database = client["doggys"]

# Colecciones
products_collection = database.products
users_collection = database.users
orders_collection = database.orders

print("✅ Colecciones de MongoDB configuradas")

# Datos iniciales
initial_products = [
    {
        "name": "Completo Italiano",
        "price": 2490,
        "stock": 50,
        "description": "Pan, vienesa, palta, tomate y mayonesa",
        "category": "completos",
        "rarity": "common",
        "image": "🌭"
    },
    {
        "name": "Hot Dog Tradicional", 
        "price": 2190,
        "stock": 60,
        "description": "Pan hot dog, vienesa, mostaza, ketchup, pepinillos",
        "category": "hotdogs",
        "rarity": "common",
        "image": "🌭"
    },
    {
        "name": "Combo Victory Royale 🏆",
        "price": 7990, 
        "stock": 25,
        "description": "2 Hot Dogs premium + papas fritas + bebida 500ml",
        "category": "combos",
        "rarity": "epic",
        "image": "🎮"
    }
]

def initialize_database():
    """Insertar datos iniciales si no existen"""
    try:
        print("📊 Contando documentos...")
        count = products_collection.count_documents({})
        print(f"📊 Productos en la base de datos: {count}")
        
        if count == 0:
            print("📥 Insertando productos iniciales...")
            products_collection.insert_many(initial_products)
            print("✅ Productos iniciales insertados en MongoDB Atlas")
        else:
            print("✅ La base de datos ya tiene productos")
    except Exception as e:
        print(f"❌ Error inicializando base de datos: {e}")
        raise

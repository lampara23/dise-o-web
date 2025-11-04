from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from bson import ObjectId

from database import products_collection, initialize_database

app = FastAPI(title="Doggy's API", version="1.0.0")

# CORS para frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar base de datos al iniciar (síncrono)
@app.on_event("startup")
def startup_event():
    try:
        initialize_database()
        print("🚀 Doggy's API iniciada con MongoDB Atlas")
    except Exception as e:
        print(f"❌ Error al iniciar: {e}")

# 📦 PRODUCTOS (síncrono)
@app.get("/api/products")
def get_products(category: Optional[str] = None, search: Optional[str] = None):
    try:
        query = {}
        
        if category and category != "all":
            query["category"] = category
        
        if search:
            query["$or"] = [
                {"name": {"$regex": search, "$options": "i"}},
                {"description": {"$regex": search, "$options": "i"}}
            ]
        
        products = list(products_collection.find(query))
        
        # Convertir ObjectId a string para JSON
        for product in products:
            product["_id"] = str(product["_id"])
        
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener productos: {str(e)}")

@app.post("/api/products")
def create_product(product: dict):
    try:
        result = products_collection.insert_one(product)
        created_product = products_collection.find_one({"_id": result.inserted_id})
        created_product["_id"] = str(created_product["_id"])
        return {"message": "Producto creado!", "product": created_product}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear producto: {str(e)}")

@app.put("/api/products/{product_id}")
def update_product(product_id: str, product: dict):
    try:
        result = products_collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": product}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        updated_product = products_collection.find_one({"_id": ObjectId(product_id)})
        updated_product["_id"] = str(updated_product["_id"])
        return {"message": "Producto actualizado!", "product": updated_product}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar producto: {str(e)}")

@app.delete("/api/products/{product_id}")
def delete_product(product_id: str):
    try:
        result = products_collection.delete_one({"_id": ObjectId(product_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        return {"message": "Producto eliminado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar producto: {str(e)}")

# 👥 USUARIOS
@app.get("/api/users")
def get_users():
    try:
        users = list(users_collection.find())
        for user in users:
            user["_id"] = str(user["_id"])
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {str(e)}")

# 🩺 HEALTH CHECK
@app.get("/api/health")
def health_check():
    try:
        total_products = products_collection.count_documents({})
        return {
            "status": "healthy", 
            "message": "🚀 Doggy's API con FastAPI + MongoDB funcionando!",
            "total_products": total_products
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error de conexión: {str(e)}"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

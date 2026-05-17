from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# os.environ para despliegue. Descomente cuando ya probó todo local.
client = MongoClient(os.environ["MONGO_URI"])

# Conexión al clúster con tus credenciales reales y base de datos personal
#client = MongoClient("mongodb://ISIS2304I20202610:bhh8sK3O0Gcr@157.253.236.88:8087/ISIS2304I20202610")
db = client["ISIS2304I20202610"]


@app.get("/")
def inicio():
    return {"estado": "API funcionando correctamente"}


# ==========================================
# PARTE 1: COMENTARIOS DE BARES (Puntos 6 y 7)
# ==========================================

@app.get('/bares/{bar_id}/comentarios')
def get_comentarios(bar_id: int):
    # Trae los comentarios del bar especificado ocultando el _id de Mongo para que no rompa FastAPI
    comentarios = list(db["comentarios_bares"].find(
        {"bar_id": bar_id},
        {"_id": 0}
    ))
    return comentarios


@app.post('/bares/{bar_id}/comentarios')
def post_comentario(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha'] = datetime.now().isoformat()
    
    # Inserta el comentario recibido en tu colección comentarios_bares
    db["comentarios_bares"].insert_one(datos)
    return {'mensaje': 'Comentario guardado'}


# ==========================================
# PARTE 3: EVENTOS DE BARES (Puntos 12 y 13)
# ==========================================

@app.get('/bares/{bar_id}/eventos')
def get_eventos(bar_id: int):
    # Trae todos los eventos asociados al bar_id mapeado
    eventos = list(db["eventos"].find(
        {"bar_id": bar_id},
        {"_id": 0}
    ))
    return eventos


@app.post('/bares/{bar_id}/eventos')
def post_evento(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha_creacion'] = datetime.now().isoformat()
    
    # Inserta el evento polimórfico (con cualquier estructura que mande el usuario)
    db["eventos"].insert_one(datos)
    return {'mensaje': 'Evento guardado'}
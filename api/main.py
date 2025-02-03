from fastapi import FastAPI, HTTPException, Query
import requests

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API FastAPI funcionando correctamente en Vercel"}

@app.get("/fetch-data")
def fetch_data(
    power: str = Query(..., description="Poder del usuario"),
    num: str = Query(..., description="Cantidad de elementos"),
    status: str = Query(..., description="Estado"),
    order: str = Query(..., description="Orden de los resultados"),
):
    """
    Endpoint que procesa el campo 'status' y lo reemplaza con texto.
    """
    url = "https://lordsmobile.igg.com/project/game_tool/ajax.php?action=get_migration_scroll&lang=es"

    form_data = {
        "power": power,
        "num": num,
        "status": status,
        "order": order
    }

    status_mapping = {
        1: "abandonado",
        2: "normal",
        3: "lleno",
        4: "popular"
    }

    try:
        response = requests.post(url, data=form_data)
        if response.status_code == 200:
            data = response.json()
            if "data" in data and isinstance(data["data"], list):
                for item in data["data"]:
                    if "status" in item and item["status"] in status_mapping:
                        item["status"] = status_mapping[item["status"]]
            return {"respuesta": data}
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error en la solicitud: {response.text}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ocurrió un error: {str(e)}"
        )

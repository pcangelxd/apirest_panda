from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

@app.get("/")
def root():
    return {"mensaje": "¡La API REST está funcionando!"}

@app.post("/fetch-data")
def fetch_data(power: str, num: str, status: str, order: str):
    url = "https://lordsmobile.igg.com/project/game_tool/ajax.php?action=get_migration_scroll&lang=es"

    form_data = {
        "power": power,
        "num": num,
        "status": status,
        "order": order
    }

    try:
        response = requests.post(url, data=form_data)

        if response.status_code == 200:
            return {"respuesta": response.json()}
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
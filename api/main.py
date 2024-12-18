from fastapi import FastAPI, HTTPException, Query
import requests

app = FastAPI()

@app.get("/")
def root():
    return {"mensaje": "¡La API REST está funcionando!"}

@app.get("/fetch-data")
def fetch_data(
    power: str = Query(..., description="Poder del usuario"),
    num: str = Query(..., description="Cantidad de elementos"),
    status: str = Query(..., description="Estado"),
    order: str = Query(..., description="Orden de los resultados"),
):
    """
    Endpoint que acepta solicitudes GET para mostrar JSON directamente.
    """
    url = "https://lordsmobile.igg.com/project/game_tool/ajax.php?action=get_migration_scroll&lang=es"

    # Datos que se enviarán en la solicitud al servidor externo
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

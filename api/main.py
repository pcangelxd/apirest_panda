from fastapi import FastAPI, Query
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from fastapi.responses import Response
import os

app = FastAPI()

BACKGROUND_IMAGE_PATH = "perfil.png"

@app.get("/")
def home():
    return {"message": "API de Perfiles en FastAPI en Vercel está funcionando."}

@app.get("/generate-profile-image")
def generate_profile_image(
    nickname: str = Query(..., description="Nombre del usuario"),
    diamonds: int = Query(..., description="Cantidad de diamantes"),
):
    try:
        if not os.path.exists(BACKGROUND_IMAGE_PATH):
            return {"error": "La imagen base no está disponible en el servidor."}

        img = Image.open(BACKGROUND_IMAGE_PATH)
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()

        nickname_position = (100, 10)
        diamonds_position = (250, 120)

        draw.text(nickname_position, nickname, fill="black", font=font)
        draw.text(diamonds_position, str(diamonds), fill="black", font=font)

        img_io = BytesIO()
        img.save(img_io, format="PNG")
        img_io.seek(0)

        return Response(content=img_io.getvalue(), media_type="image/png")

    except Exception as e:
        return {"error": str(e)}

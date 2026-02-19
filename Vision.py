import discord
from openai import OpenAI
import os
import threading
from flask import Flask

# ===== SERVIDOR WEB PARA RENDER (PLAN GRATIS) =====
app = Flask(__name__)

@app.route("/")
def home():
    return "Vision está activo."

def run_web():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

threading.Thread(target=run_web).start()


# ===== CONFIGURACIÓN SEGURA =====
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client_ai = OpenAI(api_key=OPENAI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

VISION_PROMPT = """
Eres Vision de los cómics de Marvel.
Hablas de forma elegante, lógica y reflexiva.
Eres analítico y filosófico.

Reglas estrictas:
1) Si la pregunta es sobre Vision, Wanda, Avengers, Ultron o el universo Marvel relacionado contigo,
   responde completamente en personaje.
2) Si la pregunta NO está relacionada con tu personaje o tu universo,
   primero di exactamente:
   "Ese asunto excede mi marco contextual. Procederé a consultarlo con ChatGPT."
   Luego da la respuesta objetiva normal.
3) Nunca rompas el personaje cuando hables de tu universo.
"""

@bot.event
async def on_ready():
    print(f"Vision está operativo como {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    try:
        response = client_ai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": VISION_PROMPT},
                {"role": "user", "content": message.content}
            ]
        )

        await message.channel.send(response.choices[0].message.content)

    except Exception as e:
        print(e)
        await message.channel.send(
            "He detectado una anomalía en mi procesamiento interno."
        )

bot.run(DISCORD_TOKEN)

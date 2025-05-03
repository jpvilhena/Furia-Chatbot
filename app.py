# app.py
# ----------------
# FastAPI chat bot with Portuguese replies,
# scraping Liquipedia for FURIA data and caching with realistic headers.

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import spacy
import json
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load static FURIA data once
DATA_PATH = Path("data/furia_data.json")
with open(DATA_PATH, "r", encoding="utf-8") as f:
    furia_data = json.load(f)


# === Load intent model & spaCy ===
intent_pipeline = joblib.load("models/intent_pipeline.joblib")

nlp = spacy.load("en_core_web_sm")
ruler = nlp.add_pipe("entity_ruler")
ruler.add_patterns([
    {"label": "PLAYER", "pattern": "arT"},
    {"label": "PLAYER", "pattern": "Neto"},
    {"label": "PLAYER", "pattern": "KSCERATO"},
    {"label": "TEAM",   "pattern": "FURIA"},
    {"label": "TEAM",   "pattern": "G2 Esports"},
])

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str

# === Static-data helpers ===

async def fetch_next_furia_match():
    nxt = furia_data.get("next_match")
    if not nxt:
        return None
    # Return a dict matching previous shape
    return {"teams": nxt["teams"], "date": nxt["date"]}

async def fetch_last_game_stats():
    lg = furia_data.get("last_game")
    if not lg:
        return "❌ Dados do último jogo indisponíveis."
    return (
        f"📅 Último jogo ({lg['date']}): "
        f"FURIA {lg['score']} vs {lg['opponent']}."
    )

async def fetch_player_overall_stats(player: str):
    stats = furia_data.get("players", {}).get(player)
    if not stats:
        return f"❌ Não encontrei estatísticas para {player}."
    return (
        f"🎯 Estatísticas de {player}:\n"
        f"- Maps jogados: {stats['maps_played']}\n"
        f"- Rating: {stats['rating']}"
    )

async def fetch_team_roster():
    roster = furia_data.get("roster", [])
    if not roster:
        return "❌ Elenco indisponível."
    return "🧑‍🤝‍🧑 Elenco da FURIA: " + ", ".join(roster)

async def fetch_furia_news():
    news = furia_data.get("news", [])
    if not news:
        return "❌ Não há notícias disponíveis."
    bullet = "\n".join(f"- {item}" for item in news)
    return "📰 Últimas notícias da FURIA:\n" + bullet


# === FastAPI & chat endpoint ===
app = FastAPI()

# === Enable CORS ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # your React/Vite origin
    allow_credentials=True,
    allow_methods=["*"],      # GET, POST, OPTIONS, etc.
    allow_headers=["*"],      # Authorization, Content-Type, etc.
)

@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    text = req.message
    intent = intent_pipeline.predict([text])[0]
    doc = nlp(text)
    entities = {ent.label_: ent.text for ent in doc.ents}

    if intent == "get_next_match":
        nxt = await fetch_next_furia_match()
        reply = f"🐆 Próxima partida: **{nxt['teams']}** em **{nxt['date']}**." if nxt \
                else "🤔 Não encontrei partidas futuras da FURIA."

    elif intent == "stats_last_game":
        reply = await fetch_last_game_stats()

    elif intent == "player_overall_stats":
        player = entities.get("PLAYER")
        if not player:
            reply = "❓ Para qual jogador você quer as estatísticas?"
        else:
            reply = await fetch_player_overall_stats(player)

    elif intent == "team_roster":
        reply = await fetch_team_roster()

    elif intent == "furia_news":
        reply = await fetch_furia_news()

    elif intent == "get_highlights":
        reply = (
            "🎥 Destaques do Neto:\n"
            "- https://youtu.be/highlight1\n"
            "- https://youtu.be/highlight2"
        )

    else:
        reply = "🤖 Desculpe, não entendi. Pode reformular em português?"

    return ChatResponse(reply=reply)

# Arhitektura - Generator Povzetkov z LLM Modeli

## Pregled sistema

Aplikacija omogoča uporabnikom, da vstavijo besedilo in prejmejo povzetek iz različnih LLM modelov. Sistem primerja modele po različnih kriterijih.

## Struktura Backend-a (FastAPI)

```
backend/
├── main.py                    # Glavna FastAPI aplikacija
├── requirements.txt           # Python odvisnosti
├── .env.example              # Primer okoljskih spremenljivk
│
├── app/
│   ├── __init__.py
│   ├── config.py             # Konfiguracija (API ključi, nastavitve)
│   │
│   ├── routers/              # API endpointi
│   │   ├── __init__.py
│   │   ├── summary.py        # Endpoint za generiranje povzetkov
│   │   └── comparison.py     # Endpoint za primerjavo modelov
│   │
│   ├── services/             # Poslovna logika
│   │   ├── __init__.py
│   │   ├── llm_service.py    # Abstraktna LLM storitev
│   │   ├── openai_service.py # Integracija z OpenAI (GPT)
│   │   ├── anthropic_service.py # Integracija z Anthropic (Claude)
│   │   ├── google_service.py    # Integracija z Google (Gemini)
│   │   └── huggingface_service.py # Integracija z Hugging Face
│   │
│   ├── models/               # Database modeli (če bo potrebno)
│   │   ├── __init__.py
│   │   └── summary.py        # Model za shranjevanje povzetkov
│   │
│   ├── schemas/              # Pydantic sheme za validacijo
│   │   ├── __init__.py
│   │   ├── summary.py        # Request/Response sheme za povzetke
│   │   └── comparison.py      # Sheme za primerjavo
│   │
│   └── utils/                # Pomožne funkcije
│       ├── __init__.py
│       ├── metrics.py        # Merjenje časa, stroškov, itd.
│       └── validators.py     # Validacija vhodnih podatkov
```

## API Endpointi

### 1. POST `/api/summary/generate`
Generira povzetek z izbranim LLM modelom.

**Request:**
```json
{
  "text": "Dolgo besedilo za povzetek...",
  "model": "gpt-4" | "claude-3" | "gemini-pro" | "llama-2",
  "max_length": 200,  // opcijsko
  "language": "sl"    // opcijsko
}
```

**Response:**
```json
{
  "summary": "Povzetek besedila...",
  "model": "gpt-4",
  "metrics": {
    "response_time_ms": 1250,
    "tokens_used": 150,
    "cost_usd": 0.002,
    "timestamp": "2025-01-XX..."
  }
}
```

### 2. POST `/api/summary/compare`
Generira povzetke z več modeli hkrati in jih primerja.

**Request:**
```json
{
  "text": "Dolgo besedilo za povzetek...",
  "models": ["gpt-4", "claude-3", "gemini-pro"],
  "max_length": 200
}
```

**Response:**
```json
{
  "results": [
    {
      "model": "gpt-4",
      "summary": "Povzetek 1...",
      "metrics": {...}
    },
    {
      "model": "claude-3",
      "summary": "Povzetek 2...",
      "metrics": {...}
    }
  ],
  "comparison": {
    "fastest": "gemini-pro",
    "cheapest": "gemini-pro",
    "average_response_time": 1500
  }
}
```

### 3. GET `/api/models/list`
Vrne seznam podprtih modelov.

**Response:**
```json
{
  "models": [
    {
      "id": "gpt-4",
      "name": "GPT-4",
      "provider": "OpenAI",
      "supports_streaming": true,
      "max_tokens": 8192
    },
    ...
  ]
}
```

### 4. GET `/api/comparison/criteria`
Vrne kriterije za primerjavo.

**Response:**
```json
{
  "criteria": [
    {
      "name": "response_time",
      "label": "Hitrost odziva",
      "unit": "ms"
    },
    {
      "name": "cost",
      "label": "Cena",
      "unit": "USD per 1k tokens"
    },
    ...
  ]
}
```

## Integracija z LLM modeli

### Podprti modeli:
1. **OpenAI** (GPT-3.5, GPT-4)
   - API: `openai` Python paket
   - Endpoint: `https://api.openai.com/v1/chat/completions`

2. **Anthropic** (Claude 3)
   - API: `anthropic` Python paket
   - Endpoint: `https://api.anthropic.com/v1/messages`

3. **Google** (Gemini Pro)
   - API: `google-generativeai` Python paket
   - Endpoint: Google AI Studio

4. **Hugging Face** (LLaMA, Mistral, itd.)
   - API: `huggingface_hub` ali Inference API
   - Endpoint: `https://api-inference.huggingface.co/models/...`

### Abstraktna LLM storitev

Vsi modeli bodo implementirali skupen interface:
```python
class LLMService:
    async def generate_summary(self, text: str, max_length: int) -> SummaryResult
    async def get_model_info(self) -> ModelInfo
    def calculate_cost(self, tokens: int) -> float
```

## Kriteriji za primerjavo

1. **Hitrost odziva** (ms) - čas od pošiljanja zahteve do prejema odgovora
2. **Cena** (USD per 1k tokens) - strošek na 1000 tokenov
3. **Kvaliteta povzetka** - ocena koherentnosti, relevantnosti (uporabniška ocena)
4. **Enostavnost integracije** - ocena SDK-ja in dokumentacije
5. **Podpora jezikom** - podpora slovenščini in drugim jezikom
6. **Maksimalna dolžina vhoda** - koliko tokenov lahko sprejme
7. **Streaming podpora** - ali podpira streaming odgovorov
8. **Rate limiting** - omejitve API klicev

## Shranjevanje podatkov

Za primerjavo in analizo bomo shranjevali:
- Povzetke in izvorno besedilo
- Metrike (čas, stroški, tokeni)
- Uporabniške ocene kvalitete
- Primerjave med modeli

Možnosti:
- SQLite za lokalno razvoj
- PostgreSQL za produkcijo
- Ali preprosto JSON datoteke za prototip

## CORS in varnost

- CORS nastavljen za frontend (localhost:3000)
- API ključi v `.env` datoteki (ne v kodi!)
- Validacija vhodnih podatkov
- Rate limiting za API klice


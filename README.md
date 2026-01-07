# AI Summary - Generator Povzetkov z LLM Modeli

Seminarska naloga: Razvoj in primerjava aplikacij, ki uporabljajo velike jezikovne modele (LLMs)

## Opis projekta

Aplikacija omogoča uporabnikom, da vstavijo besedilo in prejmejo povzetek iz različnih LLM modelov (GPT-4, Claude 3, Gemini Pro, LLaMA 2, itd.). Sistem primerja modele po različnih kriterijih: hitrost odziva, cena, kvaliteta povzetka, itd.

## Struktura projekta

```
AI_Summary/
├── backend/          # FastAPI backend
│   ├── main.py      # Glavna aplikacija
│   ├── app/         # Aplikacijska logika
│   └── requirements.txt
│
├── frontend/        # Next.js frontend
│   ├── src/         # React komponente
│   └── package.json
│
├── ARCHITECTURE.md  # Arhitektura backend-a
├── PROJECT_PLAN.md  # Načrt projekta
└── README.md        # Ta datoteka
```

## Začetek

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
cp .env.example .env
# Uredite .env in dodajte API ključe

uvicorn main:app --reload
```

Backend bo na: http://localhost:8000
API dokumentacija: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend bo na: http://localhost:3000

## Funkcionalnosti

- ✅ Vnos besedila za povzetek
- ✅ Izbira LLM modelov
- ✅ Generiranje povzetkov
- ✅ Primerjava modelov po kriterijih
- ✅ Vizualizacija rezultatov (tabele, grafi)

## Kriteriji primerjave

1. Hitrost odziva (ms)
2. Cena (USD per 1k tokens)
3. Kvaliteta povzetka (ocena 1-5)
4. Enostavnost integracije
5. Podpora jezikom
6. Maksimalna dolžina vhoda
7. Streaming podpora
8. Rate limiting

## Podprti modeli

- OpenAI: GPT-4, GPT-3.5
- Anthropic: Claude 3
- Google: Gemini Pro
- Hugging Face: LLaMA 2, Mistral

## Dokumentacija

- `backend/ARCHITECTURE.md` - Arhitektura backend-a
- `frontend/ARCHITECTURE.md` - Arhitektura frontend-a
- `PROJECT_PLAN.md` - Načrt projekta in faze razvoja

## Avtor

Seminarska naloga za predmet Računalništvo in spletne tehnologije, 2025-26


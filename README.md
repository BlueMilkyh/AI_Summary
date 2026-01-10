# AI Summary - Generator povzetkov z LLM modeli

Aplikacija za generiranje povzetkov z uporabo različnih LLM (Large Language Model) modelov in primerjavo njihovih rezultatov.

## Pregled

Ta aplikacija omogoča:
- Generiranje povzetkov besedil z različnimi LLM modeli
- Primerjavo več modelov hkrati
- Analizo performans modelov (hitrost, stroški, kakovost)
- Shranjevanje rezultatov v Supabase bazo podatkov

## Prenos projekta

### Metoda 1: Git Clone

Če je projekt na Git repozitoriju, ga lahko prenesete z ukazom:

```bash
git clone <repository-url>
cd AI_Summary
```

### Metoda 2: Prenos ZIP datoteke

1. Prenesite ZIP datoteko projekta
2. Razširite ZIP datoteko na želeno lokacijo
3. Odprite terminal in pojdite v mapo projekta

### Metoda 3: Prenos iz GitHub/GitLab

1. Odprite spletni vmesnik repozitorija (GitHub, GitLab, itd.)
2. Kliknite gumb "Code" ali "Clone"
3. Izberite "Download ZIP"
4. Razširite datoteko in odprite mapo

## Zahteve

Pred namestitvijo zagotovite, da imate nameščeno:

- **Python** 3.10 ali novejši
- **Node.js** 18 ali novejši
- **npm** ali **yarn** (paketni upravljalnik)
- **Git** (za clone metodo, opcijsko)

## Namestitev

### 1. Namestitev Backend-a

1. Odprite terminal in pojdite v mapo `backend`:

```bash
cd backend
```

2. Ustvarite virtualno okolje (priporočeno):

```bash
python -m venv venv
```

3. Aktivirajte virtualno okolje:

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

4. Namestite potrebne pakete:

```bash
pip install -r requirements.txt
```

### 2. Namestitev Frontend-a

1. V novem terminalnem oknu pojdite v mapo `frontend`:

```bash
cd frontend
```

2. Namestite odvisnosti:

```bash
npm install
```

## Konfiguracija

### Backend konfiguracija

1. V mapi `backend` ustvarite datoteko `.env` (če še ne obstaja):

```bash
# .env
OPENROUTER_API_KEY=vaš-openrouter-api-ključ
SUPABASE_URL=vaš-supabase-url
SUPABASE_KEY=vaš-supabase-ključ
```

Ali pa uporabite nastavitve v `backend/app/config.py`, kjer so že nastavljeni privzeti ključi.

### Frontend konfiguracija

1. V mapi `frontend` ustvarite datoteko `.env.local` (če je potrebno):

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Zagon aplikacije

### 1. Zagon Backend serverja


Zaženite FastAPI server:

```bash
fastapi dev main.py
```

Backend API bo dostopen na: `http://localhost:8000`
API dokumentacija: `http://localhost:8000/docs`

### 2. Zagon Frontend aplikacije

1. V novem terminalnem oknu pojdite v mapo `frontend`:

```bash
cd frontend
```

2. Zaženite Next.js razvojni server:

```bash
npm run dev
```

Frontend aplikacija bo dostopna na: `http://localhost:3000`

## Uporaba

1. Odprite spletni brskalnik in pojdite na `http://localhost:3000`
2. Vnesite besedilo, ki ga želite povzeti
3. Izberite model ali modele za generiranje povzetka
4. Kliknite gumb za generiranje
5. Pregledajte rezultate in analize

## Struktura projekta

```
AI_Summary/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── config.py       # Konfiguracija aplikacije
│   │   ├── database.py     # Supabase povezava
│   │   ├── models/         # Database modeli
│   │   ├── routers/        # API route handlers
│   │   ├── schemas/        # Pydantic sheme
│   │   ├── services/       # Poslovna logika
│   │   └── utils/          # Pomožne funkcije
│   ├── main.py             # Glavna aplikacija
│   └── requirements.txt    # Python odvisnosti
│
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/            # Next.js app router strani
│   │   ├── components/     # React komponente
│   │   └── lib/            # Pomožne funkcije in API klice
│   ├── package.json        # Node.js odvisnosti
│   └── next.config.ts      # Next.js konfiguracija
│
└── README.md               # Ta datoteka
```

## API dokumentacija

Ko je backend server zagnan, si lahko ogledate interaktivno API dokumentacijo:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Podprti modeli

Aplikacija podpira različne LLM modele preko OpenRouter API:
- GPT-4 in variante
- Claude (Anthropic) modeli
- In drugi modeli, ki jih podpira OpenRouter

Za celoten seznam si oglejte `/api/summary/models` endpoint.

## Opombe

- Zagotovite, da imate veljaven OpenRouter API ključ
- Supabase je opcijski - aplikacija bo delovala tudi brez baze podatkov
- Za produkcijski zagon uporabite ustrezne varnostne nastavitve


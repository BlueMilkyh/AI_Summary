# Google Gemini API Setup

Google Gemini API je že integriran in pripravljen za uporabo.

## API Ključ

API ključ je že nastavljen v `app/config.py` kot privzeta vrednost. Za produkcijo je priporočljivo, da ga premaknete v `.env` datoteko.

## Uporaba

### 1. Preverite, da so odvisnosti nameščene

```bash
pip install -r requirements.txt
```

### 2. API ključ v .env (priporočeno)

Ustvarite `.env` datoteko v `backend/` mapi:

```env
GOOGLE_API_KEY=AIzaSyAAhFfK3YqLm7F2lQ2HA4RCVfXBIfDAa_s
```

### 3. Podprti modeli

- `gemini-pro` - Standardni Gemini Pro model
- `gemini-1.5-pro` - Najnovejši Gemini 1.5 Pro model

### 4. Testiranje

Zaženite backend:

```bash
uvicorn main:app --reload
```

Odprite http://localhost:8000/docs in testirajte endpoint `/api/summary/generate`:

```json
{
  "text": "To je testno besedilo za povzetek. Vsebuje več stavkov in informacij.",
  "model": "gemini-pro",
  "max_length": 200
}
```

### 5. Primerjava modelov

Uporabite endpoint `/api/summary/compare` za primerjavo več modelov hkrati:

```json
{
  "text": "Dolgo besedilo za primerjavo...",
  "models": ["gemini-pro", "gemini-1.5-pro"]
}
```

## Funkcionalnosti

✅ Generiranje povzetkov
✅ Merjenje časa odziva
✅ Izračun stroškov
✅ Primerjava več modelov
✅ Podpora za slovenščino

## Cene (približno)

- Gemini Pro: $0.0005 per 1k input tokens, $0.0015 per 1k output tokens
- Gemini 1.5 Pro: $0.00125 per 1k input tokens, $0.005 per 1k output tokens

## Naslednji koraki

Ko boste testirali Google Gemini, lahko dodate še druge modele (OpenAI, Anthropic, Hugging Face).


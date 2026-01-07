# Vodilnik za implementacijo

Ta dokument vsebuje korake za implementacijo generatorja povzetkov.

## Faza 1: Backend - Osnovna struktura ✅

Struktura je že pripravljena. Naslednji koraki:

### 1.1 Pridobitev API ključev

1. **OpenAI**: https://platform.openai.com/api-keys
2. **Anthropic**: https://console.anthropic.com/
3. **Google AI**: https://makersuite.google.com/app/apikey
4. **Hugging Face**: https://huggingface.co/settings/tokens

Dodajte ključe v `backend/.env` datoteko.

### 1.2 Implementacija prvega LLM servisa

Začnite z OpenAI (najlažji za začetek):

1. Odprite `backend/app/services/openai_service.py`
2. Implementirajte `generate_summary` metodo
3. Implementirajte `calculate_cost` metodo
4. Testirajte z osnovnim besedilom

**Primer implementacije:**
```python
async def generate_summary(self, text: str, max_length: Optional[int] = None):
    start_time = self._measure_time()
    
    prompt = f"Povzemi naslednje besedilo v slovenščini:\n\n{text}"
    if max_length:
        prompt += f"\n\nPovzetek naj bo največ {max_length} znakov."
    
    response = self.client.chat.completions.create(
        model=self.model_name,
        messages=[
            {"role": "system", "content": "Ti si pomočnik za povzemanje besedil."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_length // 4 if max_length else 200  # Približno 4 znaki na token
    )
    
    end_time = self._measure_time()
    summary = response.choices[0].message.content
    
    # Preštej tokene
    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens
    
    metrics = self._create_metrics(start_time, end_time, input_tokens, output_tokens)
    
    return SummaryResponse(
        summary=summary,
        model=self.model_name,
        metrics=metrics
    )
```

### 1.3 Implementacija routerja

1. Odprite `backend/app/routers/summary.py`
2. Implementirajte `generate_summary` endpoint
3. Implementirajte `compare_models` endpoint (uporabi `asyncio.gather` za paralelno izvajanje)

**Primer:**
```python
@router.post("/generate", response_model=SummaryResponse)
async def generate_summary(request: SummaryRequest):
    # Ustvari ustrezen service glede na model
    if request.model.startswith("gpt"):
        service = OpenAIService(request.model, settings.openai_api_key)
    elif request.model.startswith("claude"):
        service = AnthropicService(request.model, settings.anthropic_api_key)
    # ... itd.
    
    result = await service.generate_summary(request.text, request.max_length)
    return result
```

### 1.4 Testiranje backend-a

```bash
cd backend
uvicorn main:app --reload
```

Odprite http://localhost:8000/docs in testirajte endpoint-e.

## Faza 2: Frontend - Osnovna funkcionalnost

### 2.1 Namestitev odvisnosti

```bash
cd frontend
npm install
```

### 2.2 Implementacija komponent

Komponente so že pripravljene, vendar morate:

1. **TextInput**: Preverite ali deluje pravilno
2. **ModelSelector**: Preverite ali se naložijo modeli iz API-ja
3. **SummaryDisplay**: Preverite ali se prikažejo rezultati

### 2.3 Povezovanje z backend-om

1. Preverite `NEXT_PUBLIC_API_URL` v `.env.local` (če potrebno)
2. Testirajte API klice v `lib/api.ts`
3. Preverite CORS nastavitve v backend-u

### 2.4 Testiranje frontend-a

```bash
npm run dev
```

Odprite http://localhost:3000 in testirajte aplikacijo.

## Faza 3: Dodatni LLM modeli

Ko prvi model deluje, dodajte ostale:

1. **Anthropic (Claude)**: `backend/app/services/anthropic_service.py`
2. **Google (Gemini)**: `backend/app/services/google_service.py`
3. **Hugging Face**: `backend/app/services/huggingface_service.py`

Vsak naj implementira `LLMService` interface.

## Faza 4: Primerjava in vizualizacija

### 4.1 Tabela primerjave

Ustvarite komponento `ComparisonTable` za prikaz metrik v tabeli.

### 4.2 Grafi

Namestite `recharts`:
```bash
npm install recharts
```

Ustvarite komponento `ComparisonChart` za vizualizacijo.

## Faza 5: Testiranje in optimizacija

1. Testirajte z različnimi besedili
2. Zberite podatke o metrikah
3. Optimizirajte hitrost (caching, paralelno izvajanje)
4. Izboljšajte error handling

## Faza 6: Dokumentacija

1. Dokumentirajte kodo
2. Napišite seminarsko nalogo
3. Pripravite predstavitev

## Koristni nasveti

- Začnite z enim modelom (OpenAI je najlažji)
- Testirajte z majhnimi besedili na začetku
- Uporabite `.env` za API ključe (ne commitajte jih!)
- Dokumentirajte postopek implementacije za seminarsko
- Shranjujte rezultate testiranja za primerjavo

## Debugging

- **Backend**: Preverite FastAPI docs na `/docs`
- **Frontend**: Uporabite browser DevTools
- **API ključi**: Preverite ali so pravilno nastavljeni v `.env`
- **CORS**: Preverite nastavitve v `main.py`

## Naslednji koraki

1. ✅ Struktura projekta
2. ⏳ Implementacija prvega LLM servisa
3. ⏳ Implementacija routerjev
4. ⏳ Frontend povezovanje
5. ⏳ Dodatni modeli
6. ⏳ Vizualizacija
7. ⏳ Testiranje
8. ⏳ Dokumentacija


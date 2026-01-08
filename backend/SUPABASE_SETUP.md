# Supabase Setup - Shranjevanje podatkov in odločanje

## Pregled

Supabase je integriran za shranjevanje podatkov o povzetkih, primerjavah modelov in omogoča odločanje na podlagi zgodovinskih podatkov.

## Database Schema

### Tabele

1. **`summaries`** - Shranjuje vse generirane povzetke
   - Originalno besedilo
   - Povzetek
   - Model in provider
   - Metrike (čas, stroški, tokeni)

2. **`model_comparisons`** - Shranjuje primerjave med modeli
   - Originalno besedilo
   - JSON z vsemi rezultati
   - Najhitrejši/najcenejši model

3. **`user_ratings`** - Uporabniške ocene kvalitete
   - Povezava na povzetek
   - Ocena 1-5
   - Opcijski feedback

4. **`model_metrics`** - Agregirane metrike (za prihodnost)

### Views

1. **`model_statistics`** - Agregirane statistike po modelih
2. **`best_models_by_criteria`** - Najboljši modeli po kriterijih

## API Endpoints

### Shranjevanje podatkov

- **`POST /api/summary/generate`** - Avtomatično shrani povzetek
- **`POST /api/summary/compare`** - Avtomatično shrani primerjavo
- **`POST /api/summary/rating`** - Shrani uporabniško oceno

### Pridobivanje podatkov

- **`GET /api/summary/statistics?model_name=...`** - Statistike za modele
- **`GET /api/summary/recent?limit=10`** - Zadnji povzetki
- **`GET /api/summary/best-models`** - Najboljši modeli po kriterijih

### Odločanje (Decision Making)

- **`GET /api/decision/recommend?criteria=balanced`** - Priporoči najboljši model
  - `criteria`: `balanced`, `speed`, `cost`, `quality`
- **`GET /api/decision/compare-all`** - Primerjaj vse modele

## Primeri uporabe

### 1. Priporočilo modela

```bash
GET /api/decision/recommend?criteria=balanced
```

Vrne najboljši model glede na:
- Hitrost (40%)
- Ceno (30%)
- Kvaliteto (30%)

### 2. Statistike za model

```bash
GET /api/summary/statistics?model_name=gpt-4o-mini
```

Vrne:
- Povprečen čas odziva
- Povprečne stroške
- Povprečno število tokenov
- Povprečno oceno

### 3. Shranjevanje ocene

```bash
POST /api/summary/rating
{
  "summary_id": "uuid",
  "model_name": "gpt-4o-mini",
  "rating": 5,
  "feedback": "Odličen povzetek!"
}
```

## Namestitev

1. Namestite Supabase paket:
```bash
pip install supabase
```

2. Supabase ključ je že nastavljen v `config.py`

3. Migracije so že aplicirane v Supabase

## Kako deluje odločanje

1. **Zbiranje podatkov**: Vsak generiran povzetek se shrani v bazo
2. **Agregacija**: Statistike se izračunajo iz zgodovinskih podatkov
3. **Odločanje**: Sistem priporoči model na podlagi:
   - Hitrosti (povprečen čas odziva)
   - Stroškov (povprečni stroški)
   - Kvalitete (povprečne uporabniške ocene)

## Naslednji koraki

1. Generirajte nekaj povzetkov z različnimi modeli
2. Ocenite povzetke (rating endpoint)
3. Uporabite decision endpoint za priporočila

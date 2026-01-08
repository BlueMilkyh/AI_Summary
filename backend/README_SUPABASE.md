# Supabase Integracija - Povzetek

## ✅ Implementirano

### Database Schema
- ✅ `summaries` - Shranjevanje povzetkov
- ✅ `model_comparisons` - Shranjevanje primerjav
- ✅ `user_ratings` - Uporabniške ocene
- ✅ `model_metrics` - Agregirane metrike
- ✅ Views za statistike in najboljše modele

### API Endpoints

#### Shranjevanje (avtomatično)
- `POST /api/summary/generate` - Avtomatično shrani povzetek
- `POST /api/summary/compare` - Avtomatično shrani primerjavo

#### Pridobivanje podatkov
- `GET /api/summary/statistics?model_name=...` - Statistike za modele
- `GET /api/summary/recent?limit=10` - Zadnji povzetki
- `GET /api/summary/best-models` - Najboljši modeli po kriterijih
- `POST /api/summary/rating` - Shrani oceno

#### Odločanje (Decision Making)
- `GET /api/decision/recommend?criteria=balanced` - Priporoči model
  - `criteria`: `balanced`, `speed`, `cost`, `quality`
- `GET /api/decision/compare-all` - Primerjaj vse modele

## Namestitev

1. Namestite paket:
```bash
pip install supabase
```

2. Supabase je že nastavljen v `config.py` z anon key

3. Migracije so že aplicirane

## Kako deluje

1. **Avtomatsko shranjevanje**: Ko generirate povzetek, se avtomatično shrani v bazo
2. **Zbiranje statistik**: Sistem zbira metrike za vsak model
3. **Odločanje**: Na podlagi zgodovinskih podatkov sistem priporoča najboljši model

## Primeri

### Priporočilo modela
```bash
GET /api/decision/recommend?criteria=balanced
```

### Statistike
```bash
GET /api/summary/statistics
```

### Shranjevanje ocene
```bash
POST /api/summary/rating
{
  "summary_id": "uuid",
  "model_name": "gpt-4o-mini",
  "rating": 5
}
```

# Načrt Projekta - Generator Povzetkov z LLM Modeli

## Cilj projekta

Razviti prototip aplikacije, ki omogoča generiranje povzetkov besedil z uporabo različnih LLM modelov in njihovo primerjavo po izbranih kriterijih.

## Tehnološki stack

- **Frontend**: Next.js 16 (React 19, TypeScript)
- **Backend**: FastAPI (Python)
- **LLM Integracije**: OpenAI, Anthropic, Google, Hugging Face
- **Vizualizacija**: Recharts ali Chart.js

## Faze razvoja

### Faza 1: Osnovna struktura ✅
- [x] Nastavitev FastAPI backend-a
- [x] Nastavitev Next.js frontend-a
- [x] Osnovna arhitektura in dokumentacija

### Faza 2: Backend implementacija
- [ ] Integracija z OpenAI API (GPT-4, GPT-3.5)
- [ ] Integracija z Anthropic API (Claude 3)
- [ ] Integracija z Google API (Gemini Pro)
- [ ] Integracija z Hugging Face (LLaMA 2 ali Mistral)
- [ ] Implementacija endpointov za povzetke
- [ ] Implementacija endpointov za primerjavo
- [ ] Merjenje metrik (čas, stroški, tokeni)

### Faza 3: Frontend implementacija
- [ ] UI za vnos besedila
- [ ] Komponenta za izbiro modelov
- [ ] Prikaz povzetkov
- [ ] Tabela primerjave
- [ ] Grafi za vizualizacijo
- [ ] Loading stanja in error handling

### Faza 4: Primerjava in analiza
- [ ] Testiranje z različnimi besedili
- [ ] Zbiranje podatkov o metrikah
- [ ] Uporabniške ocene kvalitete
- [ ] Analiza rezultatov

### Faza 5: Dokumentacija in poročilo
- [ ] Dokumentacija kode
- [ ] Pisanje seminarske naloge (8-12 strani)
- [ ] Priprava predstavitve

## Kriteriji za primerjavo modelov

1. **Hitrost odziva** (ms)
   - Merjeno od pošiljanja zahteve do prejema odgovora
   - Povprečje iz več meritev

2. **Cena** (USD per 1k tokens)
   - Strošek na 1000 tokenov
   - Primerjava cen različnih modelov

3. **Kvaliteta povzetka**
   - Koherentnost
   - Relevantnost (ali zajema glavne točke)
   - Uporabniška ocena (1-5 zvezdic)

4. **Enostavnost integracije**
   - Kakovost SDK-ja
   - Kakovost dokumentacije
   - Število vrst kode za integracijo

5. **Podpora jezikom**
   - Kako dobro deluje s slovenščino
   - Podpora drugim jezikom

6. **Maksimalna dolžina vhoda**
   - Koliko tokenov lahko sprejme model
   - Omejitve za dolga besedila

7. **Streaming podpora**
   - Ali podpira streaming odgovorov
   - Uporabno za dolge povzetke

8. **Rate limiting**
   - Omejitve API klicev
   - Vpliv na uporabniško izkušnjo

## Monetizacija - predlogi

### 1. Freemium model
- **Brezplačno**: 5 povzetkov na dan, osnovni modeli
- **Premium** ($9.99/mesec): Neomejeno povzetkov, vsi modeli, export podatkov
- **Pro** ($29.99/mesec): API dostop, bulk processing, prioritetna podpora

### 2. Pay-per-use
- $0.10 na povzetek (ne glede na model)
- Paketi: 10 povzetkov za $0.90, 100 za $8.00

### 3. Enterprise
- Naročnina za podjetja: $99-499/mesec
- API dostop, custom modeli, prioritetna podpora

### Stroški (ocena)
- OpenAI GPT-4: ~$0.03 per 1k input tokens, $0.06 per 1k output tokens
- Anthropic Claude 3: ~$0.015 per 1k input, $0.075 per 1k output
- Google Gemini: ~$0.0005 per 1k input, $0.0015 per 1k output
- Hugging Face: odvisno od modela (lahko brezplačno za nekaj klicev)

### Prihodki (ocena za 1000 uporabnikov)
- 10% premium uporabnikov: 100 × $9.99 = $999/mesec
- 5% pro uporabnikov: 50 × $29.99 = $1,499.50/mesec
- **Skupaj**: ~$2,500/mesec

### Stroški (ocena za 1000 uporabnikov)
- Povprečno 20 povzetkov na uporabnika/mesec
- Povprečno 500 tokenov vhod, 200 tokenov izhod
- Stroški: ~$500-800/mesec (odvisno od modela)
- **Profit**: ~$1,700-2,000/mesec

## Testni scenariji

### Test 1: Kratek članek (500 besed)
- Primerjava hitrosti in stroškov
- Kvaliteta povzetka

### Test 2: Dolg članek (2000 besed)
- Omejitve modelov
- Kvaliteta z daljšimi besedili

### Test 3: Tehnično besedilo
- Natančnost s specializiranimi izrazi
- Ohranitev pomena

### Test 4: Slovenščina
- Kvaliteta prevoda/povzetka v slovenščini
- Podpora slovenskim znakom

## Omejitve in izzivi

1. **API ključi in stroški**
   - Potrebni API ključi za vse modele
   - Omejitev stroškov med razvojem

2. **Rate limiting**
   - Različni limiti za različne modele
   - Vpliv na testiranje

3. **Čas razvoja**
   - Integracija z več API-ji zahteva čas
   - Testiranje in optimizacija

4. **Kvaliteta ocenjevanja**
   - Subjektivna ocena kvalitete
   - Potrebno več ocenjevalcev za objektivnost

## Možne izboljšave

1. **Caching**
   - Shranjevanje povzetkov za ista besedila
   - Zmanjšanje stroškov

2. **Streaming**
   - Prikaz povzetka med generiranjem
   - Boljša uporabniška izkušnja

3. **Več jezikov**
   - Podpora za več jezikov
   - Avtomatska detekcija jezika

4. **Custom nastavitve**
   - Dolžina povzetka
   - Slog povzetka (kratek, srednji, podroben)

5. **Shranjevanje zgodovine**
   - Zgodovina povzetkov
   - Primerjava skozi čas

## Naslednji koraki

1. Pridobitev API ključev za različne modele
2. Implementacija prvega LLM servisa (npr. OpenAI)
3. Implementacija osnovnega frontend-a
4. Testiranje in iteracija


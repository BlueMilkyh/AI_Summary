# Arhitektura Frontend-a - Generator Povzetkov

## Pregled

Next.js aplikacija z React komponentami za interakcijo z uporabnikom in prikaz rezultatov.

## Struktura Frontend-a

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx           # Glavni layout
│   │   ├── page.tsx              # Glavna stran
│   │   ├── globals.css           # Globalni stil
│   │   │
│   │   └── api/                  # API route handlers (če potrebno)
│   │
│   ├── components/
│   │   ├── TextInput/           # Komponenta za vnos besedila
│   │   │   ├── TextInput.tsx
│   │   │   └── TextInput.module.css
│   │   │
│   │   ├── ModelSelector/       # Izbira LLM modelov
│   │   │   ├── ModelSelector.tsx
│   │   │   └── ModelSelector.module.css
│   │   │
│   │   ├── SummaryDisplay/      # Prikaz povzetkov
│   │   │   ├── SummaryDisplay.tsx
│   │   │   └── SummaryDisplay.module.css
│   │   │
│   │   ├── ComparisonTable/     # Tabela primerjave
│   │   │   ├── ComparisonTable.tsx
│   │   │   └── ComparisonTable.module.css
│   │   │
│   │   ├── ComparisonChart/     # Graf primerjave
│   │   │   ├── ComparisonChart.tsx
│   │   │   └── ComparisonChart.module.css
│   │   │
│   │   └── LoadingSpinner/      # Loading indikator
│   │       ├── LoadingSpinner.tsx
│   │       └── LoadingSpinner.module.css
│   │
│   ├── lib/
│   │   ├── api.ts               # API klice k backend-u
│   │   ├── types.ts              # TypeScript tipi
│   │   └── utils.ts              # Pomožne funkcije
│   │
│   └── hooks/
│       ├── useSummary.ts        # Custom hook za povzetke
│       └── useComparison.ts     # Custom hook za primerjavo
│
├── public/                      # Statične datoteke
└── package.json
```

## Glavne funkcionalnosti

### 1. Vnos besedila
- Veliko textarea polje za vnos besedila
- Števec znakov/tokenov
- Gumb za "Naloži iz datoteke" (opcijsko)
- Validacija (min/max dolžina)

### 2. Izbira modelov
- Checkbox seznam vseh podprtih modelov
- Možnost izbire več modelov hkrati
- Prikaz informacij o modelih (cena, hitrost, itd.)
- Gumb "Primerjaj vse"

### 3. Generiranje povzetkov
- Loading stanje med generiranjem
- Prikaz napredeka (če podpira streaming)
- Prikaz rezultatov po modelih
- Side-by-side primerjava

### 4. Prikaz rezultatov
- **Povzetki**: Prikaz povzetka za vsak model
- **Metrike**: Hitrost, stroški, število tokenov
- **Tabela primerjave**: Vse metrike v tabeli
- **Grafi**: Vizualizacija primerjav (Chart.js ali Recharts)

### 5. Interakcija
- Ocena kvalitete povzetka (1-5 zvezdic)
- Shranjevanje primerjav
- Export rezultatov (JSON, CSV)
- Deljenje primerjav

## API integracija

### API klice (v `lib/api.ts`)

```typescript
// Generira povzetek z enim modelom
async function generateSummary(
  text: string, 
  model: string, 
  options?: SummaryOptions
): Promise<SummaryResponse>

// Generira povzetke z več modeli
async function compareModels(
  text: string, 
  models: string[], 
  options?: SummaryOptions
): Promise<ComparisonResponse>

// Vrne seznam podprtih modelov
async function getAvailableModels(): Promise<Model[]>

// Vrne kriterije za primerjavo
async function getComparisonCriteria(): Promise<Criteria[]>
```

## TypeScript tipi (v `lib/types.ts`)

```typescript
interface SummaryRequest {
  text: string;
  model: string;
  max_length?: number;
  language?: string;
}

interface SummaryResponse {
  summary: string;
  model: string;
  metrics: {
    response_time_ms: number;
    tokens_used: number;
    cost_usd: number;
    timestamp: string;
  };
}

interface ComparisonResponse {
  results: SummaryResponse[];
  comparison: {
    fastest: string;
    cheapest: string;
    average_response_time: number;
  };
}

interface Model {
  id: string;
  name: string;
  provider: string;
  supports_streaming: boolean;
  max_tokens: number;
}
```

## UI/UX načrt

### Glavna stran
```
┌─────────────────────────────────────────┐
│  Generator Povzetkov - Primerjava LLM  │
├─────────────────────────────────────────┤
│                                         │
│  [Text Input Area - veliko polje]      │
│  Znakov: 0 / 10000                     │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ ☑ GPT-4 (OpenAI)                │   │
│  │ ☑ Claude 3 (Anthropic)           │   │
│  │ ☐ Gemini Pro (Google)            │   │
│  │ ☐ LLaMA 2 (Hugging Face)         │   │
│  └─────────────────────────────────┘   │
│                                         │
│  [Generiraj povzetek] [Primerjaj vse]  │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ Rezultati:                      │   │
│  │                                 │   │
│  │ GPT-4: [Povzetek...]            │   │
│  │ ⏱ 1.2s | 💰 $0.002 | ⭐⭐⭐⭐    │   │
│  │                                 │   │
│  │ Claude 3: [Povzetek...]         │   │
│  │ ⏱ 1.5s | 💰 $0.003 | ⭐⭐⭐⭐⭐   │   │
│  └─────────────────────────────────┘   │
│                                         │
│  [Tabela primerjave] [Grafi]           │
└─────────────────────────────────────────┘
```

## Odvisnosti

### Potrebne npm pakete:
- `axios` ali `fetch` - za API klice
- `recharts` ali `chart.js` - za grafe
- `react-icons` - za ikone
- `zustand` ali `react-query` - za state management (opcijsko)

## Responsive design

- Desktop: Side-by-side primerjava
- Tablet: Stacked layout
- Mobile: En model naenkrat, swipe med modeli


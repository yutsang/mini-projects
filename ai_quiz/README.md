# AI-Powered Quiz Application

A Streamlit app that generates quiz questions from Excel data using Azure OpenAI.

## Features

- **Excel data**: Load from upload or optional `AF1_mapping.xlsx` in this folder; falls back to built-in sample data if no file is present.
- **Module selection**: Dropdown of unique `Module` values.
- **AI questions**: Azure OpenAI generates five multiple-choice questions (four options each).
- **Scoring**: Submit answers; pass at ≥80% (4/5 correct), with optional detailed breakdown.
- **Session state**: Supports retake and regeneration.

## Setup

### 1. Install dependencies

```bash
cd ai_quiz
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment variables

Copy the template and edit values:

```bash
cp .env.template .env
```

Required in `.env`:

- `AZURE_GPT4_KEY` — Azure OpenAI API key  
- `TARGET_URL` — Azure OpenAI endpoint (e.g. `https://your-resource.openai.azure.com/`)  
- `MODEL_NAME` — **Deployment name** in Azure (must match the name in Azure OpenAI Studio, not necessarily `gpt-4`)  
- `API_VERSION` — Optional; default `2024-02-15-preview`

The app loads `.env` from the `ai_quiz` directory so it works even if you start the process from another working directory.

### 3. Excel file (optional)

Place `AF1_mapping.xlsx` in the `ai_quiz` folder, or upload via the sidebar. Required **column names** (header row):

| Column name   | Content                          |
|---------------|----------------------------------|
| `Module`      | Module group (dropdown values)   |
| `Module name` | Topic / sub-unit title           |
| `Objectives`  | Learning objective text          |

If the file is missing or invalid, the app uses sample rows so you can still explore the UI (quiz generation still needs valid Azure credentials).

## Run

From the `ai_quiz` directory:

```bash
python main.py
```

This starts Streamlit with `streamlit-quiz-app.py`. Equivalent manual command:

```bash
streamlit run streamlit-quiz-app.py
```

Open the URL shown in the terminal (default `http://localhost:8501`).

## Usage

1. Upload an Excel file in the sidebar (optional if `AF1_mapping.xlsx` is present).
2. Pick a **module**, expand **Content** if you want to review objectives.
3. Click **Generate Quiz Questions** (requires Azure OpenAI configured).
4. Answer all five questions, then **Submit Quiz**.
5. Use **Retake Quiz** to clear and generate again if needed.

## Project layout

```
ai_quiz/
├── main.py                 # Recommended entry: python main.py
├── streamlit-quiz-app.py   # Streamlit UI and logic
├── requirements.txt
├── .env.template
├── .env                    # Create locally (not committed)
├── AF1_mapping.xlsx        # Optional local data
└── README.md
```

## Troubleshooting

- **Azure / API errors**: Confirm `TARGET_URL` has no typo, `AZURE_GPT4_KEY` is valid, and `MODEL_NAME` matches your **deployment** name in Azure.
- **“Excel file must contain columns …”**: First row must be headers exactly `Module`, `Module name`, `Objectives`.
- **“Please set AZURE_GPT4_KEY and TARGET_URL”**: Create `ai_quiz/.env` from `.env.template`.
- **Import errors**: Re-run `pip install -r requirements.txt` inside your activated virtual environment.

## License

See `LICENSE`. Use of Azure OpenAI is subject to Microsoft and your account terms.

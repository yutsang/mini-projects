# AI-Powered Quiz Application

A comprehensive Streamlit application that generates customized quiz questions from Excel data using Azure OpenAI.

## Features

- 📁 **Excel Data Integration**: Load data from AF1_mapping.xlsx with Module, Module name, and Objectives columns
- 🎯 **Dynamic Module Selection**: Choose from unique module values via dropdown
- 🤖 **AI-Powered Question Generation**: Uses Azure OpenAI to create 5 multiple choice questions
- 📝 **Interactive Quiz Interface**: Clean UI with radio buttons for 4 choices per question
- ✅ **Automated Scoring**: Regex-based answer validation with Pass (≥80%) or Fail (<80%) results
- 🔄 **Session State Management**: Maintains quiz progress and allows retakes

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

1. Copy `.env.template` to `.env`:
```bash
cp .env.template .env
```

2. Edit `.env` with your Azure OpenAI credentials:
```
AZURE_GPT4_KEY=your_actual_api_key
TARGET_URL=https://your-resource.openai.azure.com/
MODEL_NAME=gpt-4
API_VERSION=2024-02-15-preview
```

### 3. Prepare Excel File

Create or place `AF1_mapping.xlsx` in the project directory with these columns:
- **Column B**: Module (unique values for dropdown)
- **Column C**: Module name
- **Column E**: Objectives

Sample data structure:
```
Module              | Module name         | Objectives
Key audit concepts  | Purpose of an audit | Recognise the purpose and scope...
Key audit concepts  | Audit framework     | Understand the regulatory framework...
```

### 4. Run the Application

```bash
streamlit run streamlit-quiz-app.py
```

## How to Use

1. **Upload Excel File**: Use the sidebar to upload your AF1_mapping.xlsx file
2. **Select Module**: Choose a module from the dropdown to see its content
3. **Generate Quiz**: Click "Generate Quiz Questions" to create 5 MCQ questions using AI
4. **Take Quiz**: Answer all 5 questions using the radio buttons (A, B, C, D)
5. **Submit & Review**: Get immediate feedback with Pass/Fail results and detailed answers

## Technical Implementation

### Core Components

- **Excel Processing**: Uses pandas to read and filter Excel data
- **Azure OpenAI Integration**: Generates structured JSON responses for quiz questions
- **Answer Validation**: Regex patterns (`[ABCD]`) ensure proper answer format
- **Scoring Logic**: Calculates percentage and applies 80% pass threshold
- **Session Management**: Maintains state across user interactions

### Key Functions

- `load_excel_data()`: Loads and validates Excel file structure
- `get_unique_modules()`: Extracts unique module values for dropdown
- `generate_quiz_questions()`: Calls Azure OpenAI API with structured prompts
- `validate_answers()`: Uses regex to check user answers against correct answers
- `calculate_and_display_score()`: Computes final score and displays results

### Error Handling

- File upload validation
- API connection error handling
- JSON response parsing
- Missing environment variables detection

## Quiz Generation Process

1. **Content Extraction**: Filters Excel data by selected module
2. **Prompt Engineering**: Creates structured system and user prompts
3. **API Call**: Sends request to Azure OpenAI with JSON format specification
4. **Response Processing**: Parses and validates returned quiz questions
5. **UI Rendering**: Displays questions with interactive radio buttons

## Scoring System

- **Pass Threshold**: 80% (4 out of 5 questions correct)
- **Answer Validation**: Regex pattern matching for A, B, C, D options
- **Results Display**: Visual feedback with detailed question-by-question breakdown
- **Retake Option**: Users can retake the quiz with new questions

## File Structure

```
project/
├── streamlit-quiz-app.py    # Main application file
├── requirements.txt         # Python dependencies
├── .env.template           # Environment variables template
├── .env                    # Your actual environment variables (create from template)
├── AF1_mapping.xlsx        # Excel data file (your data)
└── README.md              # This file
```

## Troubleshooting

### Common Issues

1. **"No modules found"**: Check Excel file has data in Column B (Module)
2. **API errors**: Verify Azure OpenAI credentials in .env file
3. **File upload issues**: Ensure Excel file has required columns
4. **Package errors**: Install missing dependencies with pip

### Environment Variables

Make sure all required environment variables are set:
- `AZURE_GPT4_KEY`: Your Azure OpenAI API key
- `TARGET_URL`: Your Azure OpenAI endpoint URL
- `MODEL_NAME`: Your model deployment name (e.g., gpt-4)
- `API_VERSION`: API version (e.g., 2024-02-15-preview)

## License

This project is for educational and internal use. Please ensure compliance with Azure OpenAI usage policies.
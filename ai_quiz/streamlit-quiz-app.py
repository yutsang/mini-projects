# AI-Powered Quiz Application with Azure OpenAI Integration
# Author: Assistant
# Description: Streamlit application for generating quiz questions from Excel data using Azure OpenAI

import streamlit as st
import pandas as pd
import os
import json
import re
from openai import AzureOpenAI
from dotenv import load_dotenv
import io

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI-Powered Quiz System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #21808D 0%, #1D7480 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .quiz-container {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .question-box {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #21808D;
    }
    .score-display {
        text-align: center;
        padding: 2rem;
        border-radius: 10px;
        margin: 2rem 0;
    }
    .pass-score {
        background: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .fail-score {
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    .sidebar-info {
        background: #e9ecef;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
def initialize_session_state():
    if 'quiz_data' not in st.session_state:
        st.session_state.quiz_data = None
    if 'current_questions' not in st.session_state:
        st.session_state.current_questions = None
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False
    if 'score_result' not in st.session_state:
        st.session_state.score_result = None
    if 'selected_module' not in st.session_state:
        st.session_state.selected_module = None

# Load Excel data
@st.cache_data
def load_excel_data(uploaded_file=None):
    """Load Excel data from uploaded file or default file"""
    try:
        if uploaded_file is not None:
            df = pd.read_excel(uploaded_file)
        else:
            # Try to load default file
            if os.path.exists("AF1_mapping.xlsx"):
                df = pd.read_excel("AF1_mapping.xlsx")
            else:
                # Create sample data if file doesn't exist
                sample_data = {
                    'Module': ['Key audit concepts', 'Key audit concepts', 'Key audit concepts', 
                              'Planning and risk assessment', 'Planning and risk assessment',
                              'Evidence and documentation', 'Evidence and documentation'],
                    'Module name': ['Purpose of an audit', 'Audit framework', 'Professional skepticism',
                                   'Audit planning', 'Risk assessment', 'Audit evidence', 'Documentation standards'],
                    'Objectives': ['Recognise the purpose and scope of auditing',
                                  'Understand the regulatory framework for auditing',
                                  'Apply professional skepticism in audit procedures',
                                  'Develop comprehensive audit plans',
                                  'Identify and assess audit risks effectively',
                                  'Gather sufficient and appropriate audit evidence',
                                  'Maintain proper audit documentation standards']
                }
                df = pd.DataFrame(sample_data)
        
        # Ensure correct column names
        if 'Module' in df.columns and 'Module name' in df.columns and 'Objectives' in df.columns:
            return df
        else:
            st.error("Excel file must contain columns: 'Module', 'Module name', and 'Objectives'")
            return None
    except Exception as e:
        st.error(f"Error loading Excel file: {str(e)}")
        return None

# Get unique modules
def get_unique_modules(df):
    """Extract unique module values"""
    if df is not None:
        return sorted(df['Module'].unique().tolist())
    return []

# Filter content by module
def filter_module_content(df, selected_module):
    """Get content for selected module"""
    if df is not None and selected_module:
        filtered_df = df[df['Module'] == selected_module]
        content_dict = {}
        for _, row in filtered_df.iterrows():
            content_dict[row['Module name']] = row['Objectives']
        return content_dict
    return {}

# Initialize Azure OpenAI client
def initialize_azure_client():
    """Initialize Azure OpenAI client with environment variables"""
    try:
        api_key = os.getenv('AZURE_GPT4_KEY')
        endpoint = os.getenv('TARGET_URL')
        api_version = os.getenv('API_VERSION', '2024-02-15-preview')
        
        if not api_key or not endpoint:
            st.error("Please set AZURE_GPT4_KEY and TARGET_URL in your .env file")
            return None
        
        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=endpoint
        )
        return client
    except Exception as e:
        st.error(f"Error initializing Azure OpenAI client: {str(e)}")
        return None

# Generate quiz questions using Azure OpenAI
def generate_quiz_questions(client, module_content, module_name):
    """Generate 5 multiple choice questions using Azure OpenAI"""
    try:
        # Prepare content for prompt
        content_text = ""
        for module_topic, objective in module_content.items():
            content_text += f"Topic: {module_topic}\\nObjective: {objective}\\n\\n"
        
        system_prompt = """You are an expert quiz generator. Create exactly 5 multiple choice questions based on the provided module content. 
        
        REQUIREMENTS:
        - Each question must have exactly 4 options (A, B, C, D)
        - Only one correct answer per question
        - Questions should test understanding of the learning objectives
        - Return response in valid JSON format only
        
        JSON FORMAT:
        {
            "questions": [
                {
                    "question": "Question text here?",
                    "options": {
                        "A": "Option A text",
                        "B": "Option B text", 
                        "C": "Option C text",
                        "D": "Option D text"
                    },
                    "correct_answer": "A"
                }
            ]
        }"""
        
        user_prompt = f"Generate 5 multiple choice questions for the module '{module_name}' based on this content:\\n\\n{content_text}"
        
        model_name = os.getenv('MODEL_NAME', 'gpt-4')
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=2000
        )
        
        # Parse JSON response
        response_content = response.choices[0].message.content
        quiz_data = json.loads(response_content)
        
        # Validate response structure
        if 'questions' in quiz_data and len(quiz_data['questions']) == 5:
            return quiz_data['questions']
        else:
            st.error("Invalid response format from Azure OpenAI")
            return None
            
    except json.JSONDecodeError:
        st.error("Failed to parse JSON response from Azure OpenAI")
        return None
    except Exception as e:
        st.error(f"Error generating quiz questions: {str(e)}")
        return None

# Display quiz questions
def display_quiz(questions):
    """Display quiz questions with radio buttons"""
    st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
    st.subheader("🎯 Quiz Questions")
    st.markdown("*Select the best answer for each question:*")
    
    for i, question_data in enumerate(questions, 1):
        st.markdown(f'<div class="question-box">', unsafe_allow_html=True)
        st.markdown(f"**Question {i}:** {question_data['question']}")
        
        options = question_data['options']
        option_list = [f"{key}. {value}" for key, value in options.items()]
        
        # Create unique key for each question
        answer_key = f"question_{i}"
        selected_answer = st.radio(
            f"Select your answer for Question {i}:",
            options=option_list,
            key=answer_key,
            label_visibility="collapsed"
        )
        
        # Store user answer
        if selected_answer:
            # Extract the letter (A, B, C, D) from the selected option
            answer_letter = selected_answer[0]
            st.session_state.user_answers[answer_key] = answer_letter
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Validate answers using regex
def validate_answers(user_answers, correct_answers):
    """Validate user answers against correct answers using regex"""
    if len(user_answers) != len(correct_answers):
        return 0, []
    
    correct_count = 0
    results = []
    
    for i, (user_answer, correct_answer) in enumerate(zip(user_answers.values(), correct_answers), 1):
        # Use regex to validate answer format
        if re.match(r'^[ABCD]$', user_answer) and re.match(r'^[ABCD]$', correct_answer):
            is_correct = user_answer == correct_answer
            if is_correct:
                correct_count += 1
            results.append({
                'question': i,
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct
            })
        else:
            results.append({
                'question': i,
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': False
            })
    
    return correct_count, results

# Calculate and display score
def calculate_and_display_score(questions):
    """Calculate score and display results"""
    if len(st.session_state.user_answers) != 5:
        st.warning("Please answer all 5 questions before submitting.")
        return
    
    # Extract correct answers
    correct_answers = [q['correct_answer'] for q in questions]
    
    # Validate answers
    correct_count, results = validate_answers(st.session_state.user_answers, correct_answers)
    
    # Calculate percentage
    percentage = (correct_count / 5) * 100
    
    # Determine pass/fail
    is_pass = percentage >= 80
    
    # Display results
    if is_pass:
        st.markdown(f'''
        <div class="score-display pass-score">
            <h2>🎉 PASS</h2>
            <h3>Score: {correct_count}/5 ({percentage:.0f}%)</h3>
            <p>Congratulations! You have successfully passed the quiz.</p>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="score-display fail-score">
            <h2>❌ FAIL</h2>
            <h3>Score: {correct_count}/5 ({percentage:.0f}%)</h3>
            <p>You need at least 80% to pass. Please review the material and try again.</p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Show detailed results
    with st.expander("📊 View Detailed Results"):
        for result in results:
            if result['is_correct']:
                st.success(f"Question {result['question']}: ✅ Correct (Your answer: {result['user_answer']})")
            else:
                st.error(f"Question {result['question']}: ❌ Incorrect (Your answer: {result['user_answer']}, Correct: {result['correct_answer']})")
    
    st.session_state.quiz_submitted = True
    st.session_state.score_result = {
        'correct_count': correct_count,
        'percentage': percentage,
        'is_pass': is_pass,
        'results': results
    }

# Main application
def main():
    """Main application function"""
    initialize_session_state()
    
    # Header
    st.markdown('''
    <div class="main-header">
        <h1>🎯 AI-Powered Quiz System</h1>
        <p>Generate customized quiz questions using Azure OpenAI</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
        st.markdown("### 📁 File Upload")
        st.markdown("Upload your AF1_mapping.xlsx file or use sample data")
        st.markdown('</div>', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose Excel file", 
            type=['xlsx', 'xls'],
            help="Upload AF1_mapping.xlsx with Module, Module name, and Objectives columns"
        )
        
        st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
        st.markdown("### ⚙️ Configuration")
        st.markdown("Make sure your .env file contains:")
        st.code("""
AZURE_GPT4_KEY=your_api_key
TARGET_URL=https://your-resource.openai.azure.com/
MODEL_NAME=gpt-4
API_VERSION=2024-02-15-preview
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Load Excel data
    df = load_excel_data(uploaded_file)
    
    if df is not None:
        # Module selection
        st.subheader("📚 Module Selection")
        unique_modules = get_unique_modules(df)
        
        if unique_modules:
            selected_module = st.selectbox(
                "Select a module to generate quiz questions:",
                [""] + unique_modules,
                key="module_selector"
            )
            
            if selected_module:
                st.session_state.selected_module = selected_module
                
                # Display module content
                module_content = filter_module_content(df, selected_module)
                
                with st.expander(f"📋 Content for '{selected_module}'"):
                    for topic, objective in module_content.items():
                        st.markdown(f"**{topic}:** {objective}")
                
                # Generate quiz button
                if st.button("🚀 Generate Quiz Questions", type="primary"):
                    client = initialize_azure_client()
                    
                    if client:
                        with st.spinner("Generating quiz questions using Azure OpenAI..."):
                            questions = generate_quiz_questions(client, module_content, selected_module)
                            
                            if questions:
                                st.session_state.current_questions = questions
                                st.session_state.user_answers = {}
                                st.session_state.quiz_submitted = False
                                st.success("✅ Quiz questions generated successfully!")
                                st.rerun()
        else:
            st.warning("No modules found in the Excel file.")
    
    # Display quiz if questions are generated
    if st.session_state.current_questions and not st.session_state.quiz_submitted:
        display_quiz(st.session_state.current_questions)
        
        # Submit quiz button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("📝 Submit Quiz", type="primary", use_container_width=True):
                calculate_and_display_score(st.session_state.current_questions)
    
    # Display results if quiz is submitted
    if st.session_state.quiz_submitted and st.session_state.score_result:
        # Option to retake quiz
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔄 Retake Quiz", type="secondary", use_container_width=True):
                st.session_state.current_questions = None
                st.session_state.user_answers = {}
                st.session_state.quiz_submitted = False
                st.session_state.score_result = None
                st.rerun()

if __name__ == "__main__":
    main()
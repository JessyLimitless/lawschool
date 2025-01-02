import os
from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)

# Securely set OpenAI API key
openai.api_key = 'sk-'

def generate_case_question(subject):
    """
    Generate a case question dynamically using OpenAI API.
    """
    try:
        prompt = f"Generate a challenging bar exam-style case question for the subject: {subject}."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in US bar exam preparation."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        raise ValueError("Error generating case question")

def evaluate_answer(user_answer, case_question):
    """
    Evaluate the user's answer and generate a score out of 10, feedback, and a correct answer.
    """
    try:
        prompt = f"""
        Evaluate the following user answer against the case question.
        Case Question: {case_question}
        User Answer: {user_answer}
        Provide:
        - A score from 1 to 10.
        - A detailed explanation for why this score was given.
        - Constructive feedback pointing out shortcomings (if any).
        - Praise for what the user did well.
        - An ideal correct answer for comparison.
        Format your response as:
        Score: [1-10]
        Explanation: [...]
        Shortcomings: [...]
        Praise: [...]
        Correct Answer: [...]
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in evaluating legal case answers."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        raise ValueError("Error evaluating the answer")

@app.route('/generate-case', methods=['POST'])
def generate_case():
    """
    Endpoint to generate a case question based on the selected subject.
    """
    data = request.json
    subject = data.get('subject')
    if not subject:
        return jsonify({'error': 'No subject provided'}), 400

    try:
        case_question = generate_case_question(subject)
        return jsonify({'question': case_question})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/evaluate-answer', methods=['POST'])
def evaluate_answer_endpoint():
    """
    Endpoint to evaluate the user's answer and return a score and feedback.
    """
    data = request.json
    user_answer = data.get('user_answer')
    case_question = data.get('case_question')

    if not user_answer or not case_question:
        return jsonify({'error': 'Missing user answer or case question'}), 400

    try:
        evaluation = evaluate_answer(user_answer, case_question)
        return jsonify({'evaluation': evaluation})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    """
    Serve the combined HTML file.
    """
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

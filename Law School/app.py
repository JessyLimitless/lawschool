from flask import Flask, request, jsonify, render_template
import openai

# Initialize the Flask application
app = Flask(__name__)

# Set OpenAI API key (replace 'your-api-key' with your actual key)
openai.api_key = "sk-"

def generate_case_question(subject):
    """
    Generate a bar exam-style case question for the selected subject.
    """
    try:
        prompt = f"Generate a challenging bar exam-style case question for the subject: {subject}."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in bar exam preparation."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        raise ValueError(f"Error generating case question: {e}")

def evaluate_answer(user_answer, case_question):
    """
    Evaluate the user's answer to the case question and return detailed feedback.
    """
    try:
        prompt = f"""
        Evaluate the following user answer against the case question:
        Case Question: {case_question}
        User Answer: {user_answer}
        Provide:
        - A score out of 10
        - A detailed explanation for the score
        - Constructive feedback on shortcomings
        - Praise for positive aspects of the answer
        - The correct answer for comparison

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
                {"role": "system", "content": "You are an expert in legal exam evaluation."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        raise ValueError(f"Error evaluating answer: {e}")

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
    Endpoint to evaluate the user's answer to the case question.
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
    Render the main page of the application.
    """
    return render_template('index.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

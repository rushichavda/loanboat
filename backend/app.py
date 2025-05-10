from flask import Flask, request, jsonify
from flask_cors import CORS
from logic.engine import ConversationEngine
import json

app = Flask(__name__)
CORS(app)

# Initialize engine
engine = ConversationEngine("questions.csv")
conversation_started = False

@app.route('/start', methods=['GET'])
def start():
    global conversation_started
    if not conversation_started:
        engine.reset()
        conversation_started = True
    first_question = engine.get_next_question()
    first_question = replace_placeholders(first_question, engine.collected_data)
    return jsonify({"message": "Conversation started", "question": first_question})

@app.route("/respond", methods=["POST"])
def respond():
    data = request.json
    response = data.get("response", "")

    # Store the response using the engine logic
    if engine.last_question:
        outputs = [o.strip() for o in engine.last_question['Output'].split(',') if o.strip()]
        engine.store_response(response, outputs)
        write_to_json(engine.get_collected_data())

    # Keep asking until a question with all placeholders filled is found
    while True:
        next_question = engine.ask_next_question()
        if not next_question:
            return jsonify({"message": "Thank you for completing the application!"})
        
        # Replace placeholders
        next_question_with_placeholders = replace_placeholders(next_question, engine.collected_data)
        
        if next_question_with_placeholders is not None:
            return jsonify({"question": next_question_with_placeholders})


def write_to_json(data):
    with open('collected_data.json', 'w') as f:
        json.dump(data, f, indent=4)

def replace_placeholders(question, collected_data):
    print(f"Collected Data: {collected_data}")  # Debugging the collected data

    if question:
        print(f"Original question: {question}")  # Debugging the original question

        # If a placeholder is present but data is missing, return None to skip
        if "{your name}" in question and "applicant_name" not in collected_data:
            return None
        
        if "{your college name}" in question and "college_name" not in collected_data:
            return None

        # Replace placeholders if data is available
        if "{your name}" in question:
            question = question.replace("{your name}", collected_data["applicant_name"])
        
        if "{your college name}" in question:
            question = question.replace("{your college name}", collected_data["college_name"])

        print(f"Modified question: {question}")  # Debugging the modified question

    return question




    return question


if __name__ == '__main__':
    app.run(debug=True, port=5001)

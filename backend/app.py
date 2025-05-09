from flask import Flask, request, jsonify
from flask_cors import CORS
from logic.engine import ConversationEngine
import json
import csv

app = Flask(__name__)
CORS(app)

# Initialize the conversation engine with the CSV of questions
engine = ConversationEngine("questions.csv")

# Track if the conversation has started
conversation_started = False

@app.route('/start', methods=['GET'])
def start():
    """Start the conversation by resetting engine and returning the first question."""
    global conversation_started
    if not conversation_started:
        engine.reset()  # Only reset the conversation once
        conversation_started = True
        print("Conversation started.")
    first_question = engine.get_next_question()
    
    # Replace placeholders with real values if needed
    first_question = replace_placeholders(first_question)

    return jsonify({
        "message": "Conversation started",
        "question": first_question
    })

@app.route("/respond", methods=["POST"])
def respond():
    """Process user's response and return next appropriate question."""
    data = request.json
    response = data.get("response")

    print("Received response:", response)
    print("Current Collected Data:", engine.collected_data)

    # Check for early fields (e.g., name, college)
    if "applicant_name" not in engine.collected_data:
        engine.collected_data["applicant_name"] = response
        write_to_json(engine.collected_data)
        return jsonify({"question": replace_placeholders(engine.get_next_question())})

    if "college_name" not in engine.collected_data:
        engine.collected_data["college_name"] = response
        write_to_json(engine.collected_data)
        return jsonify({"question": replace_placeholders(engine.get_next_question())})

    # Handle other questions
    if engine.last_question:
        outputs = engine.last_question['Output'].split(',')
        engine.store_response(response, outputs)
        write_to_json(engine.collected_data)

    next_question = engine.get_next_question()
    if next_question:
        return jsonify({"question": replace_placeholders(next_question)})

    return jsonify({"message": "Thank you for completing the application!"})

def write_to_json(data):
    """Save collected data to a JSON file."""
    with open('collected_data.json', 'w') as f:
        json.dump(data, f, indent=4)
    print("Data saved to collected_data.json")

def replace_placeholders(question):
    """Replace placeholders like {your name} with actual data."""
    if question:
        if "{your name}" in question and "applicant_name" in engine.collected_data:
            question = question.replace("{your name}", engine.collected_data["applicant_name"])
        if "{your collage name}" in question and "college_name" in engine.collected_data:
            question = question.replace("{your collage name}", engine.collected_data["college_name"])
    return question

if __name__ == '__main__':
    app.run(debug=True, port=5001)

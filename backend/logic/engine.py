import csv
import re

class ConversationEngine:
    def __init__(self, question_file_path: str):
        # Load questions from the CSV file
        self.questions = self.load_questions(question_file_path)
        self.collected_data = {}
        self.asked_questions = set()
        self.pending_followups = []
        self.last_question = None

    def load_questions(self, filepath):
        """Load questions and their related information from a CSV file."""
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return [row for row in reader if row.get('Question')]

    def get_next_question(self):
        """Fetch the next question, handling pending follow-up questions first."""
        # Handle follow-ups first
        while self.pending_followups:
            q = self.pending_followups.pop(0)
            if self._should_ask(q):
                self.last_question = q
                return q['Question']

        # Loop through the regular questions and find the next one to ask
        for question in self.questions:
            outputs = [o.strip() for o in question['Output'].split(',') if o.strip()]
            if any(o not in self.collected_data for o in outputs) and self._should_ask(question):
                self.last_question = question
                self.asked_questions.add(question['Question'])

                # Handle follow-ups conditionally based on the output variables
                if len(outputs) > 1:
                    primary_var = outputs[0]
                    self.store_response('', [primary_var])  # Reserve spot for the primary variable
                    return question['Question']

                return question['Question']

        return None  # Return None if no more questions are left

    def _should_ask(self, question):
        """Determine if a question should be asked, based on conditions and whether it has been asked already."""
        if question['Question'] in self.asked_questions:
            return False  # Skip if the question has already been asked
        condition = question.get('Condition', '').strip()
        if not condition:
            return True  # No condition means we can ask it
        try:
            return eval(condition, {}, self.collected_data)  # Evaluate condition based on collected data
        except:
            return False  # In case of any errors in evaluating condition, don't ask

    def store_response(self, response: str, output_vars=None):
        """Store the response and handle any necessary follow-up logic."""
        if not self.last_question:
            return

        # Determine which variables to store based on the last question's outputs
        outputs = output_vars or [o.strip() for o in self.last_question['Output'].split(',') if o.strip()]
        parsed = self.extract_variables_from_response(response, outputs)

        # Store the parsed responses in collected data
        for var in outputs:
            if var not in self.collected_data and var in parsed:
                self.collected_data[var] = parsed[var]

        # If marital status is collected and it's 'Yes', schedule follow-up questions about children
        if "marital_status" in parsed and parsed["marital_status"] == "Yes" and "number_of_children" not in self.collected_data:
            for question in self.questions:
                if "number_of_children" in question.get("Output", "") and question.get("Condition"):
                    self.pending_followups.append(question)

    def extract_variables_from_response(self, response, expected_outputs):
        """Extract variables from the user's response, based on the expected output variables."""
        response_lower = response.lower()
        parsed = {}
        
        # Process each expected output variable
        for var in expected_outputs:
            if var == "marital_status":
                if "yes" in response_lower:
                    parsed[var] = "Yes"
                elif "no" in response_lower:
                    parsed[var] = "No"
            elif var == "number_of_children":
                match = re.search(r'\d+', response)  # Find number of children
                if match:
                    parsed[var] = int(match.group())
            elif var == "applicant_age":
                match = re.search(r'\b\d{2}\b', response)  # Find age in two-digit format
                if match:
                    parsed[var] = int(match.group())
            else:
                parsed[var] = response.strip()  # For other variables, just store the response as it is
        
        return parsed

    def reset(self):
        """Reset the conversation engine to start a fresh session."""
        self.collected_data = {}
        self.asked_questions = set()
        self.pending_followups = []
        self.last_question = None

    def is_complete(self) -> bool:
        """Check if the conversation is complete (i.e., all questions have been answered)."""
        return len(self.collected_data) == len(self.questions)

    def get_collected_data(self) -> dict:
        """Return the collected data."""
        return self.collected_data

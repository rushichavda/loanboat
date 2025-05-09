import csv

class ConversationEngine:
    def __init__(self, questions_file):
        """
        Initializes the conversation engine with the provided questions CSV file.
        """
        self.questions = self.load_questions(questions_file)
        self.collected_data = {}
        self.current_question_index = 0
        self.last_question = None

    def load_questions(self, file_name):
        """
        Load questions from a CSV file into a list of dictionaries.
        Each dictionary contains 'Category', 'Question', and 'Output' keys.
        """
        questions = []
        with open(file_name, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                questions.append({
                    'Category': row['Category'].strip(),
                    'Question': row['Question'].strip(),
                    'Output': row['Output'].strip()
                })
        return questions

    def get_next_question(self):
        """
        Return the next unanswered question, skipping those whose output data is already collected.
        """
        while self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            outputs = [o.strip() for o in question['Output'].split(',')]

            if any(output not in self.collected_data for output in outputs):
                self.last_question = question
                self.current_question_index += 1
                return question['Question']

            self.current_question_index += 1  # Skip already answered question

        return None  # No more questions

    def reset(self):
        """
        Reset the engine to start a fresh conversation.
        """
        self.collected_data = {}
        self.current_question_index = 0
        self.last_question = None
        print("Conversation reset.")

    def store_response(self, response, outputs):
        """
        Store the user's response for the expected outputs.
        """
        for output in outputs:
            self.collected_data[output.strip()] = response

    def is_complete(self):
        """
        Determine whether all questions have been answered.
        """
        required_outputs = {
            output.strip()
            for question in self.questions
            for output in question['Output'].split(',')
        }
        return all(output in self.collected_data for output in required_outputs)

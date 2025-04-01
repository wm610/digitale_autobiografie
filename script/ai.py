from pathlib import Path


class Ai:
    def __init__(self):
        pass

    def generate_new_question(self, profiles : list[Path], amount_answered_question : int, asked_questions : list[str], answers_for_this_category : list[Path]):
        """
            This function needs to consider all the generated problems as well as the last x questions of this category
            It returns the new question

            profiles: summary of compleate answered profiles
            amount_answered_question: number of questions answered in this category
            asked_questions: questions asked in this category
            answers_for_this_category: answers of the questions of this category
        """
        return "new question str"
    
    def generate_summary(self, questions, answers_txt):
        """
            questions
            answers_txt
        """
        return None
from pathlib import Path
import ollama


class Ai:
    def __init__(self):
        self.client = ollama.Client() #TODO still dont know where its best to call it

    def generate_new_question(self, profiles : list[Path], asked_questions : list[str], answers_for_this_category : list[Path], current_category : str):
        """
            This function needs to consider all the generated problems as well as the last x questions of this category
            It returns the new question

            profiles: summary of compleate answered profiles
            asked_questions: questions asked in this category
            answers_for_this_category: answers of the questions of this category
            current_category: String of current category from current indexed string in category list
        """
        # read content of profiles and combine to one string
        profiles_content = [profile.read_text(encoding="utf-8") for profile in profiles]
        profiles_combined = ",".join(profiles_content)

        # combine all questions
        asked_questions_combined = "###".join(asked_questions) if asked_questions else "No questions asked yet. Use profiles for context to ask question about current category."

        # read content of answers and create string with last three
        answers_content = [answer.read_text(encoding="utf-8") for answer in answers_for_this_category]
        if len(answers_content) >= 3:
            last_three_answers = ",".join(answers_content[-3:])
        elif answers_content:
            last_three_answers = ",".join(answers_content)
        else:
            last_three_answers = "No answers available. Use profiles and current category information to generate questions" ##check if edge cases if less than three available works

        # Create final prompt
        prompt = f"{profiles_combined}###{current_category}###{asked_questions_combined}###{last_three_answers}"

        # Send prompt to model
        model = "generate_question"
        response = self.client.generate(model=model, prompt=prompt)
        return response.response
    
    def generate_summary(self, questions : list[str], answers_txt : list[path]):
        """
            questions: List of questions (strings).
            answers_txt: List of Paths to answer files.
        """
        # Read the content of each answer file
        answers_content = [answer.read_text(encoding="utf-8") for answer in answers_txt]

        # Zip questions and answers together
        combined_q_a = [f"{q},{a}" for q, a in zip(questions, answers_content)]

        # Combine all pairs into a single string separated by "###"
        combined_q_a_string = "###".join(combined_q_a)
        
        # Send prompt to model and generate response
        model = "profile"
        response = self.client.generate(model=model, prompt=combined_q_a_string)
        return response.response
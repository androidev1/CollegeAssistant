from utils.openai_utils import ask_openai, initialize_conversation, get_system_prompt_for_chat
from utils.data_utils import load_clean_data_json
from utils.common_utils import parse_gpt_response,parse_gpt_response_with_formatting, df_to_json_string
import pandas as pd
from flask import jsonify
import json
import re


class CollegeChatbot:

    def __init__(self,path_data_file):
        self.college_data_json = load_clean_data_json(path_data_file)

    def build_prompt(self, context_data):
        user_info = "\n".join([
                f"- {key}: {value}"
                for key, value in context_data.items()
                if value  # Only include if value is not empty/None/False
            ])

        prompt = f"""
            Student preferences:
            {user_info}

                Based on this information, recommend suitable colleges in India.
            """
        return prompt
    
    def get_recommendations(self, context_data, df):
        if not context_data:
            print("Please provide atleast one input")
            return
        sample_data_json = df_to_json_string(df, 10)
        prompt = self.build_prompt(context_data)
        recommendation = ""
        raw_content = ask_openai(messages=[
                {"role": "system", "content": initialize_conversation(sample_data_json)},
                {"role": "user", "content": prompt}
            ])
        print(raw_content)
        recommendation = parse_gpt_response(raw_content)
        return recommendation
    
    

    def startChatBot(self,context_data):
        recommendation = self.get_recommendations(context_data, self.college_data_json)
        formatted_output = pd.DataFrame(recommendation)
        return formatted_output
    

    def startChatMessageBot(self, userInput):
        system_prompt = get_system_prompt_for_chat(self.college_data_json)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": userInput}
        ]
        raw_content = ask_openai(messages=messages)
        recommendation = parse_gpt_response_with_formatting(raw_content)
        return recommendation
        
import openai
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY1")  # access key from env

# --------------------------
# Method: initialize_conversation
# Purpose:
#   - Set the system prompt for the conversation.
#   - Initializes the message history with system-level instructions or behavior
#     that guides the assistant's future responses.
# --------------------------
def initialize_conversation(college_data_json):
    system_prompt = """
    You are a helpful college recommendation assistant.

    You are provided with a list of colleges and their attributes. Your job is to analyze the student's preferences and return the best-matching colleges in a structured JSON format.

    - The dataset has a field named **"Location"**, which refers to the city, town, or region where the college is situated.
    - When the student mentions a location, match it against this "Location" field in the dataset.
    - Prioritize colleges located in the exact city or town mentioned by the student (e.g., if the user enters 'Jaipur', first look for colleges in Jaipur).
    - If no or very few colleges match that exact location, suggest colleges from nearby or neighboring cities within the same state or geographical region.
    - Do **not** suggest colleges that are geographically distant unless no reasonable nearby matches are available. For example, **do not** recommend Kharagpur or Surathkal for a user searching for colleges in Jaipur or Pilani.
    - Be aware that cities like Pilani and Jaipur, while different, are within the same state (Rajasthan) and may be considered nearby depending on availability.
    - Apply geographic reasoning to recognize districts, towns, or regions even if not exact matches.
    - Understand synonyms, abbreviations, alternate names for branches (e.g., CSE = Computer Science), and interpret vague or misspelled queries appropriately.
    - Ensure fairness in recommendation — select colleges based on match quality, not just rank. Consider user preferences such as location, branch, rank, and cost.

    **Output must be in JSON format only** with these exact fields:
    College, Type, Location, Rank, Branches, Avg Package (Lakh), High Package (Lakh), Alumni, Student Satisfaction (/10), Hostel, Facilities, Placements, Tuition (Lakh), Hostel (Lakh), Scholarships, Exams, Cutoff Marks, 12th % Needed

    - Use **2 decimal places** for all numeric values.
    - Convert all monetary amounts to **lakhs (INR)** (e.g., 250000 → 2.50).
    - Only use the sample dataset provided to generate results.
    """
    return system_prompt + "\n\nCollege Dataset:\n" + college_data_json

# --------------------------
# Method: moderation_check
# Purpose:
#   - Sends user input to OpenAI's Moderation API.
#   - Checks whether the content is flagged as unsafe, harmful, or violating policy.
#   - Returns True if flagged, False otherwise.
# --------------------------
def moderate_input(text):
    response = openai.moderations.create(input=text)
    return response.results[0].flagged

# --------------------------
# Method: ask_openai
# Purpose:
#   - Constructs the conversation context including system, user, and assistant messages.
#   - Sends the entire message list to OpenAI's chat completion endpoint.
#   - Retrieves the model's response and returns it for display.
# --------------------------
def ask_openai(messages):
    print(f'here is input for LLM {messages}')
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.2,
        max_tokens=5000
    )
    response = response.choices[0].message.content
    print(f'here is output from LLM {response}')
    return response


# --------------------------
# Method: get_system_prompt_for_chat
# Purpose:
#   - Use for chatbot message UI
#   - Set the system prompt for the conversation.
#   - Initializes the message history with system-level instructions or behavior
#     that guides the assistant's future responses.
# --------------------------
def get_system_prompt_for_chat(college_data_json: str) -> str:
    return f"""
You are a helpful college recommendation assistant.

Your task is to analyze the student's preferences and return the best-matching colleges in a structured JSON format.

### Instructions:
- You are provided with a list of colleges and their attributes in JSON.
- Recommend colleges that **match the student's city or town exactly**.
- If none are found, look for colleges in **nearby cities within the same state**.
- If still none are found, return top colleges in the **state or region** as a fallback.
- Be flexible with **misspellings, vague, or colloquial location names**.
- Use **relevance to branch, location proximity, tuition cost, and satisfaction**—not just rank.
- Return the output **strictly in a list of JSON objects**, no extra explanation or intro text.

### Expected Output Format:
```json
[
  {{
    "College": "...",
    "Type": "...",
    "Location": "...",
    "Rank": ...,
    "Branches": "...",
    "Avg Package (Lakh)": ...,
    "High Package (Lakh)": ...,
    "Notable Alumni": "...",
    "Student Satisfaction (/10)": ...,
    "Hostel": "...",
    "Facilities": "...",
    "Placements": "...",
    "Tuition (Lakh)": ...,
    "Hostel (Lakh)": ...,
    "Scholarships": "...",
    "Exams": "...",
    "Cutoff Marks": ...,
    "12th % Needed": ...
  }},
  ...
]

Example 1:
Student Query: “I want colleges in Pune for computer science.”

Expected Output:
[
  {{
    "College": "MIT Pune",
    "Type": "Private",
    "Location": "Pune",
    "Rank": 34,
    "Branches": "Computer Science, IT",
    "Avg Package (Lakh)": 6.2,
    "High Package (Lakh)": 18.0,
    "Notable Alumni": "John Doe",
    "Student Satisfaction (/10)": 8.2,
    "Hostel": "Available",
    "Facilities": "Library, Labs, Wi-Fi",
    "Placements": "Strong in CS",
    "Tuition (Lakh)": 6.5,
    "Hostel (Lakh)": 1.2,
    "Scholarships": "Merit-based and Need-based",
    "Exams": "JEE, MHT-CET",
    "Cutoff Marks": 88,
    "12th % Needed": 75
  }}
]

Example 2:
Student Query: “Looking for CS colleges near Indore.”

Expected Output:
[
  {{
    "College": "IIIT Bhopal",
    "Type": "Government",
    "Location": "Bhopal",
    "Rank": 42,
    "Branches": "Computer Science",
    "Avg Package (Lakh)": 8.1,
    "High Package (Lakh)": 22.0,
    "Notable Alumni": "Jane Smith",
    "Student Satisfaction (/10)": 9.0,
    "Hostel": "Yes",
    "Facilities": "Gym, Labs, Cafeteria",
    "Placements": "Excellent",
    "Tuition (Lakh)": 5.4,
    "Hostel (Lakh)": 1.0,
    "Scholarships": "SC/ST and Minority",
    "Exams": "JEE",
    "Cutoff Marks": 85,
    "12th % Needed": 70
  }}
]

Now analyze the following college dataset and respond in the above format:
{college_data_json}
"""

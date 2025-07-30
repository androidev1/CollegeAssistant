# College Recommendation Chatbot

A Gen AI-powered College Recommendation System using OpenAI. This app takes user preferences such as location, branch etc. and recommends suitable colleges from a structured dataset.

## Project Structure

```
CollegeAssistant/
├── app/
│   ├── static/
│   │   └── style.css
│   ├── templates/
│   │   └── index.html
│   │   └── chatbot.html
│   ├── __init__.py
│   ├── chatbot.py
│   └── routes.py
├── data/
│   └── college_data.csv
├── utils/
│   ├── common_utils.py
│   ├── data_utils.py
│   └── openai_utils.py
├── venv/
├── .env
├── main.py
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/dev-android1/CollegeAssistant
cd CollegeAssistant
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Add OpenAI API Key

Create a `.env` file in the root directory and add your OpenAI key:

```
OPENAI_API_KEY1=your_openai_api_key
```

### 5. Run the Application

```bash
python main.py
```

We have 2 version of app

1. open[http://localhost:5000/] - This will ask predefined questions. The user can skip any question. Atleast one input is required. Finally, we will show them matched college list

2. open [http://localhost:5000/chatbot] - This will show a chat window where user can enter question in natural language and api will process it and will display data.

---

### Screenshots
#### College App version 1 - Step 1
![Screen 1](<screenshots/Picture 2.png>) 

#### College App version 1 - For flagged messages
![Screen 2](<screenshots/picture 8.png>) 

#### College App version 1 - Step 2
![Screen 3](<screenshots/picture 9.png>) 

#### College App version 1 - Step 3
![Screen 4](<screenshots/picture 10.png>)

#### College App version 1 - Output
![Screen 5](<screenshots/Picture 4.png>)

#### College App version 2 - Input + Output
![Screen 6](<screenshots/Picture 3.png>) 

### Data Sample (with initial columns)
![Data](<screenshots/picture 5.png>) 

### Data Sample (with next columns)
![Data Continue](<screenshots/picture 6.png>) 

### Data Sample (with remianing columns)
![Data Continue](<screenshots/picture 7.png>)

### My System Prompt
```
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
```

### My Learning

- Build web app using Flask
- Use openai APIs
- Prompt Engineering for real world scenario

### Notes

- Uses Flask as the web framework.
- College recommendations are driven by OpenAI with context-aware prompts.
- Data is sourced from `college_data.csv`.


### Flow Chart
![Flow Chart](<screenshots/Picture 1.png>)

### Author
Ashish Kumar Agrawal
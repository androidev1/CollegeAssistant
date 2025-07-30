import pandas as pd

def load_clean_data_json(csv_path):
    """
    - Loads a CSV file containing college data into a pandas DataFrame.
    - Cleans and transforms monetary values from INR to Lakhs for readability.
    - Renames relevant columns for consistency and better understanding.
    - Fills missing or empty values with a space to prevent data processing issues downstream.
    - Returns the cleaned and formatted DataFrame ready for recommendation logic.

    """
    df = pd.read_csv(csv_path)
    # Convert INR values to Lakhs and round to 2 decimals
    df["Highest Package (INR)"] = (df["Highest Package (INR)"] / 100000).round(2)
    df["Annual Tuition Fees (INR)"] = (df["Annual Tuition Fees (INR)"] / 100000).round(2)
    df["Annual Hostel Fees (INR)"] = (df["Annual Hostel Fees (INR)"] / 100000).round(2)

    # Rename columns
    df.rename(columns={
        "Highest Package (INR)": "Highest Package (Lakhs)",
        "Average Package (INR)": "Average Package (Lakhs)",
        "Annual Tuition Fees (INR)": "Annual Tuition Fees (Lakhs)",
        "Annual Hostel Fees (INR)": "Annual Hostel Fees (Lakhs)"
    }, inplace=True)

    # Replace NaN or empty values with a space
    df.fillna(" ", inplace=True)
    df.replace("", " ", inplace=True)
    return df

def get_questions():
    """
    - Returns a dictionary of user-interactive questions used to collect preferences and academic background.
    - These questions are used as input prompts to filter or guide the recommendation engine (e.g., preferred location, branch, 12th grade marks).
    """
    questions = {
        "location": "Preferred Location (e.g., Delhi, Pune, Bangalore): ",
        "branch": "Preferred Branch (e.g., CSE, Mechanical): ",
        "12th Marks Required (%)": "Your 12th board marks (%): ",
    } 
    return questions

import pandas as pd
import json
import re


def df_to_json_string(df: pd.DataFrame, num_rows):
    """
    Convert the first `num_rows` rows of a DataFrame to a JSON string.

    Args:
        df (pd.DataFrame): The input DataFrame.
        num_rows (int): Number of rows to include from the top of the DataFrame.

    Returns:
        str: JSON string representing the top rows of the DataFrame.
    """
    return df.head(num_rows).to_json(orient="records", lines=False)

def parse_gpt_response(raw_content):
    """
    Extract and parse JSON data from a raw GPT response.

    Args:
        raw_content (str): The raw text content returned by the OpenAI model.

    Returns:
        dict or list: Parsed JSON content if available, otherwise an empty string.
    """
    recommendation = ""
    # Clean and extract JSON from response
    try:
        # If response includes triple backticks or explanation, remove it
        if "```json" in raw_content:
            raw_content = raw_content.split("```json")[1].split("```")[0]
        elif "```" in raw_content:
            raw_content = raw_content.split("```")[1]

        recommendation = json.loads(raw_content)
    except json.JSONDecodeError as e:
        print("Failed to parse JSON from OpenAI response:", e)
    return recommendation

def parse_gpt_response_with_formatting(raw_content):
    """
    Parse and format a GPT response into an HTML table.

    Args:
        raw_content (str): The raw text content returned by the OpenAI model.

    Returns:
        str: HTML formatted table of the response or fallback string if parsing fails.
    """
    if raw_content is None or (hasattr(raw_content, 'empty') and raw_content.empty):
        return "No recommendations were found based on your inputs."
    else: 
        recommendation = ""
        # Clean and extract JSON from response
        try:
            # If response includes triple backticks or explanation, remove it
            if "```json" in raw_content:
                raw_content = raw_content.split("```json")[1].split("```")[0]
            elif "```" in raw_content:
                raw_content = raw_content.split("```")[1]

            recommendation = json.loads(raw_content)
            df =  pd.DataFrame(recommendation)
            recommendation = df.to_html(classes='table table-striped table-bordered', index=False, escape=False)
            recommendation = f"""
                <div style="max-height: 300px; overflow-y: auto; overflow-x: auto; width: 100%;">
                    <div style="min-width: 600px; width: 100%; overflow-x: auto;">
                        {recommendation}
                    </div>
                </div>
                """
            return recommendation
        except json.JSONDecodeError as e:
            print("Failed to parse JSON from OpenAI response:", e)
            return raw_content
       
 
from flask import Blueprint, render_template, request, session, redirect, url_for,jsonify

from app.chatbot import CollegeChatbot
from utils.data_utils import get_questions
from utils.openai_utils import moderate_input


main = Blueprint('main', __name__)
chatbot = CollegeChatbot('data/college_data.csv')

@main.route('/', methods=['GET', 'POST'])
def index():
    """
    - Entry point of the application.
    - Initializes session variables and begins the step-by-step questionnaire.
    - Moderates input content before processing.
    - Calls the OpenAI API to generate dynamic responses based on user inputs.
    """
    if 'step' not in session:
        session['step'] = 0
        session['responses'] = {}

    step = session['step']
    keys = list(get_questions().keys())
    message = ""
    if request.method == 'POST':
        answer = request.form.get("answer")
        skip = request.form.get("skip")

        # Only moderate if user didn't skip
        if not skip:
            try:
                if answer:
                    flagged = moderate_input(answer)
                    if flagged:
                        message = "⚠️ Your answer was flagged by content moderation. Please revise it."
                    else:
                        session['responses'][keys[step]] = answer
                        session['step'] += 1
                        step = session['step']
                else:
                    message = "⚠️ Please provide input."

            except Exception as e:
                message = f"Moderation check failed: {e}"

        elif not skip:
            session['responses'][keys[step]] = answer
            session['step'] += 1
            step = session['step']
            message = ""
        else:
            session['responses'][keys[step]] = ""
            session['step'] += 1
            step = session['step']
            message = ""
            
    
    if step < len(keys):
        current_key = keys[step]
        current_question = get_questions()[current_key]
        return render_template("index.html",
                               question=current_question,
                               step=step+1,
                               total=len(keys),
                               has_submitted=False, message = message)
    else:
        responses = session.get('responses')
        if all(not v.strip() for v in responses.values()):
            ai_response = "No input provided"
        else:
            ai_response = chatbot.startChatBot(responses)
            # Check if ai_response is empty, None, or empty DataFrame
            if ai_response is None or (hasattr(ai_response, 'empty') and ai_response.empty):
                ai_response = "No recommendations were found based on your inputs."
            else:
                ai_response = ai_response.to_html(classes='table table-striped table-bordered', index=False, escape=False)
        
        # Clear session to allow fresh start
        session.clear()
        return render_template("index.html",
                               has_submitted=True,
                               ai_response=ai_response,
                               responses=responses,
                               user_inputs = responses)

@main.route('/restart', methods=['GET'])
def restart():
    """
    - Clears the existing session state and resets any stored conversation history.
    - Redirects the user back to the homepage to start a new chatbot session.
    """
    session.clear()
    return redirect(url_for('main.index'))  # Calls the index.html route



@main.route("/chatbot")
def chatbotHome():
    """
    - Renders the `chatbot.html` template.
    - This is the main user interface where the chatbot conversation takes place.
    """
    return render_template("chatbot.html")

@main.route("/chatbot/message", methods=["POST"])
def chatbot_message():
    """
    - Receives the user message from the frontend.
    - Checks for moderation 
    - Sends the input to the OpenAI API and returns the response in JSON format.
    - Acts as the backend message handler for AJAX/JS interactions.
    """
    user_message = request.json.get("message", "")
    flagged = moderate_input(user_message)
    if flagged:
        ai_response = "⚠️ Your answer was flagged by content moderation. Please revise it."
    else:
        ai_response = chatbot.startChatMessageBot(user_message)
    response = jsonify({"response": ai_response})
    print(f'here is response after jsonify {response}')
    return response

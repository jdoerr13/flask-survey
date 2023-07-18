from flask import Flask, request, render_template,  redirect, flash , session
from flask_debugtoolbar import DebugToolbarExtension 
from surveys import satisfaction_survey


app = Flask(__name__)

app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False  
debug = DebugToolbarExtension(app)

RESPONSES_KEY = "respon"

@app.route("/")
def show_survey_start():
    """Select a survey."""
    return render_template("start.html", survey=satisfaction_survey)

@app.route("/begin", methods=["POST"])
def start_survey(): #purpose to 
    """Clear the session of responses."""
    session[RESPONSES_KEY] = []  #make sure to inport session (dict like object) above- it refers to a key in the session dictionary where the responses to the survey questions are stored. By assigning an empty list [] to session[RESPONSES_KEY], the code clears any existing responses for the current session.
    return redirect("/questions/0") #redirect the /begin to /questions/0

#HERE EACH QUESTIONS IS HANDLED INDIVIDUALLY 
@app.route("/questions/<int:question_id>", methods=["GET", "POST"])
def handle_question(question_id):
    """Handle a question in the survey."""

    # Retrieve the survey and responses from the session
    survey = satisfaction_survey
    responses = session.get(RESPONSES_KEY)

    # Check if the question ID is valid
    if question_id < 0 or question_id >= len(survey.questions):
        flash("Invalid question ID", "error")
        return redirect("/")


    if len(responses) != question_id:
        # User is trying to access questions out of order, redirect to the correct question
        flash("You're trying to access an invalid question.", "error")
        return redirect(f"/questions/{len(responses)}")

    # Get the current question
    question = survey.questions[question_id]

    if request.method == "POST":
        # Store the user's response in the responses list
        response = request.form.get("response")
        responses.append(response)
        session[RESPONSES_KEY] = responses

        # Check if there are more questions
        if question_id + 1 < len(survey.questions):  #STEP 5- don't hard code 5 as the end
            return redirect(f"/questions/{question_id + 1}")
        else:
            # Handle the submission logic here
            # You can process the responses, store them in a database, etc.
            # This is where you can perform any necessary actions after the user has answered all the questions.
            return redirect("/complete")
    # Render the question template
    return render_template("question.html", question=question, question_id=question_id)


@app.route("/complete") #ALSO STEP 5 THANKING THE USER
def complete():
    """Survey complete. Show completion page."""
    return render_template("complete.html")







#  clearing the session of responses is to ensure that each new survey session starts with an empty list for storing the user's responses. By redirecting the user to the first question after clearing the session, the user is seamlessly transitioned into the survey flow.
# In summary, this code ensures that when a POST request is made to "/begin", the session is cleared of any existing responses, and the user is redirected to the first question of the survey. This allows for a fresh survey experience for each user session. Without the redirect, the function start_survey would continue executing and eventually return a response to the client. However, the response would not include a redirect instruction to a different URL.
# Without the redirect, the client's browser would still maintain the original URL ("/begin") and display the response received from the server. This could result in a situation where the user sees the same page again or remains on the "/begin" page without any indication of proceeding to the next step of the survey.
# In [7]: questions = [question.question for question in satisfact
#    ...: ion_survey.questions]
# In [8]: questions
# Out[8]: 
# ['Have you shopped here before?',
#  'Did someone else shop with you today?',
#  'On average, how much do you spend a month on frisbees?',
#  'Are you likely to shop here again?']
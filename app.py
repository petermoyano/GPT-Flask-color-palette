import openai
from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from dotenv import dotenv_values
import json

# Look for variables in .env and return them in config object
config = dotenv_values('.env')
openai.api_key = config["OPENAI_API_KEY"]

#initialize flask
app = Flask(__name__, template_folder='templates')

#Flask debug toolbar
app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)

#completion call with query
def get_colors(msg):
    res = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"""You are a bot that generates a palette of colors 
        (return between 3 and 6) in response to a text user input. 
        Respond with an array of strings that hold a hex color related with the input text
        Text: {msg}
        """,
        max_tokens=500
    )
    colors = json.loads(res["choices"][0]["text"])
    print(res["choices"][0]["text"])
    return colors
    

####ROUTES####
@app.route("/")
def index():
    res = openai.Completion.create(
        model="text-davinci-003",
        prompt="Give me a funny word."
    )
    # colors = json.loads(res["choices"][0]["text"])
    return render_template("index.html")
    # return render_template("index.html")


@app.route("/palette", methods=["POST"])
def prompt_to_palette( ):
    #extract query from request
    query = request.form.get("query")
    app.logger.warning("This is query!, ", query)
    app.logger.info(f"query is: {query} ")
    #completion request with query
    colors = get_colors (query)

    return {"colors": colors}

# debug mode config
if __name__ == "__main__":
    app.run(debug=True)
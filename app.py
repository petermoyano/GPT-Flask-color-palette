import openai
from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from dotenv import dotenv_values
import json

# Look for variables in .env and return them in config object
config = dotenv_values('.env')
openai.api_key = config["OPENAI_API_KEY"]

#initialize flask and indicate static folder's name
app = Flask(__name__, template_folder='templates', static_url_path='' ,static_folder='static')

#Flask debug toolbar config
app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)


####ROUTES####
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/palette", methods=["POST"])
def prompt_to_palette( ):
    #extract query from request
    query = request.form.get("query")

    #completion request with query
    colors = get_colors (query) #string
    parsedColors = json.loads(colors) 

    return {"colors": parsedColors}

#completion call with query
def get_colors(msg):
    res = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"""You are a color palette generating assistant that responds to text prompts for color palettes.
        You should generate color palettes that fit the theme, mood, or instruncions in the prompt.
        The palettes should be between 2 and 6 colors.

        Q: Convert the following verbal description of a color palette into a list of colors: The mediterranean sea
        A: ["#006699", "#66CCCC", "#F0E68C"] 
        Q: Convert the following verbal description of a color palette into a list of colors: a forest in autumn
        A: [  "#C46210",  "#F2AF5C",  "#A0522D",  "#8B3E2F",  "#228B22",  "#D2691E"]
        Q: Convert the following verbal description of a color palette into a list of colors: {msg}
        A: 
        """,
        max_tokens=500
    )
    if res == None:
        return 
    # colors is of type <class 'str'>
    colors = res["choices"][0]["text"]
    return colors 

# debug mode config
if __name__ == "__main__":
    app.run(debug=True)

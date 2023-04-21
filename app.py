import openai
from flask import Flask, render_template, request
from dotenv import dotenv_values
import json

# Look for variables in .env and return them in config object
config = dotenv_values('.env')
openai.api_key = config["OPENAI_API_KEY"]

#initialize flask
app = Flask(__name__, template_folder='templates')

#completion call with query
def get_colors(query):
    res = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"You are a bot that generates a palette of colors(return between 3 and 6) in response to a text user input. Tex: {query}Respond with an array of strings that hold a hex color related with the input text",
        max_tokens=500
    )
    return res.choices[0].text

#routes
@app.route("/")
def index():
    res = openai.Completion.create(
        model="text-davinci-003",
        prompt="Give me a funny word."
    )
    colors = json.loads(res["choices"][0]["text"])
    return colors
    # return render_template("index.html")

@app.route("/palette", methods=["POST"])
def prompt_to_palette( ):
    #extract query string 
    app.logger.info(request.form.get("query"))
    query = request.form.get("query")
    #completion request with query
    colors = get_colors (query)

    return {"colors": colors}

# debug mode config
if __name__ == "__main__":
    app.run(debug=True)
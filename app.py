import openai
from flask import Flask, render_template, request
from dotenv import dotenv_values

# Look for variables in .env and return them in config object
config = dotenv_values('.env')
openai.api_key = config["OPENAI_API_KEY"]
#initialize flask
app = Flask(__name__, template_folder='templates')

#routes
@app.route("/")
def index():
    res = openai.Completion.create(
        model="text-davinci-003",
        prompt="Give me a funny word."
    )
    return res["choices"][0]["text"]
    # return render_template("index.html")

# @app.route("/palette", methods=["POST"])
# def prompt_to_palette( ):
    #openai completion call

    return render_template("index.html")

# debug mode config
if __name__ == "__main__":
    app.run(debug=True)
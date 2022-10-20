from flask import Flask, jsonify, render_template, request, flash

app = Flask(__name__)
app.secret_key = "T0to_na_p4s_d0rm1"

@app.route("/", methods = ['GET'])
def home():
	return render_template('home.html')

@app.route("/form/", methods=["POST", "GET"])
def form():
	if request.method == "POST":
		tweet = request.form["tweet_input"]
		flash(tweet, "tweet")
		result = "toto"
		flash(result, "result")
	return render_template("form.html")

"""
@app.route("/documentation/", methods = ['GET'])
def documentation():
	return render_template('documentation.html')
"""


def no_body():
	message = {
		"message" : "Pas de texte fourni",
		"documentation" : "insérer lien"
	}
	return jsonify(message), 400


@app.route("/api/lowering/", methods = ["POST"])
def api_lowering_post():
	if not request.is_json:
		return no_body()

	data = request.json
	if "text" not in data.keys():
		return no_body()
	
	text = data["text"]
	return jsonify(text.lower())

if __name__ == "__main__":
	app.run(debug=True)
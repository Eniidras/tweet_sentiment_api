from flask import Flask, jsonify, render_template, request, flash
import modele

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
		result = modele.sentiment_tweet(tweet)
		flash(result, "result")
	return render_template("form.html")


@app.route("/documentation/", methods = ['GET'])
def documentation():
	return render_template('documentation.html')

@app.route("/blog/", methods = ['GET'])
def blog():
	return render_template('blog.html')


def no_body(message):
	message = {
		"message" : message,
		"documentation" : "https://tweet-sentiment-api-ociap7.herokuapp.com/documentation"
	}
	return jsonify(message), 400

@app.route("/api/sentiment_detection/", methods = ["POST"])
def api_sentiment_tweet():
	if not request.is_json:
		return no_body("Pas de document json dans le corps de la requête.")

	data = request.json
	if "text" not in data.keys():
		return no_body("Le corps de la requête n'a pas de champs 'text'.")
	
	text = data["text"]
	result = modele.sentiment_tweet(text)
	return jsonify({"result": result})

if __name__ == "__main__":
	app.run(debug=False)



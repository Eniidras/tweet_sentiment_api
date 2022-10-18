from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def home():
	return render_template('home.html')

@app.route("/documentation/", methods = ['GET'])
def documentation():
	return render_template('documentation.html')

"""
def erreur():
	message = {"message" : "L'id fournit ne correspond à aucun livre"}
	return jsonify(message)
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
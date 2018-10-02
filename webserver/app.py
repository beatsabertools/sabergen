#!/usr/bin/env python3

import flask
import sabergen

app = flask.Flask(__name__)

@app.route("/")
def homepage():
	return "Welcome to SaberGen"

app.run()

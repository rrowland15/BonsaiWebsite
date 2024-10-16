from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pass
    return render_template("index.html")

if __name__ == '__main__':
    #app.run(port=5656,debug=True)
    app.run()
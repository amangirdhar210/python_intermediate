from flask import Flask, render_template, request

app = Flask(__name__)

users = {
    0: {"name": "Aman", "data": "B.Tech CSE"},
    1: {"name": "Data", "data": "B.Tech CSE"},
    2: {"name": "Hello", "data": "B.Tech CSE"},
    3: {"name": "Demo", "data": "B.Tech CSE"},
}



@app.route("/")
def home():
    return "Hello Children!"


@app.route("/home")
def sample_test():
    return render_template("home.html")


@app.route("/add-data", methods=["POST", "GET"])
def sample_input():
    if request.method == "POST":
        return "POST"
    elif request.method == "GET":
        return render_template("form.html")


@app.route("/users", methods=["GET"])
def load_users():
    return render_template("users.html", users=users)


if __name__ == "__main__":
    app.run(debug=True)


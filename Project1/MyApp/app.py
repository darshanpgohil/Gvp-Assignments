from flask import Flask,render_template

app=Flask(__name__)

@app.route("/")
def root():
    return "<h1>Mahadev Mahadev</h1>"

@app.route("/home")
def home():
    name = "Momai Ma"
    l = [1,2,3,4,5,6,7,8,9,10]
    student = {
        "name": "Darshan",
        "age": 20,
        "course": "Msc(it)"
    }
    
    return render_template("home.html",name=name,lst=l,student=student)

@app.route("/name/<string:user_name>")

def name(user_name):
    return render_template("Dynamic.html",uname=user_name)

if __name__ == "__main__":
    app.run()
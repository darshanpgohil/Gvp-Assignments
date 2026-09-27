from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hostel_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

print("Database Connected Successfully")

class Hostel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    room_no = db.Column(db.String(100),nullable=False)
    place = db.Column(db.String(100),nullable=False)
    time_out = db.Column(db.String(100),nullable=False)
    signature1 = db.Column(db.String(100),nullable=False)
    time_in = db.Column(db.String(100),nullable=False)
    signature2 = db.Column(db.String(100),nullable=False)

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/add",methods=['POST'])
def add_info():
    name = request.form.get("name") 
    room = request.form.get("roomNo")
    where_go = request.form.get("place")
    time_out = request.form.get("time_go")
    signature1 = request.form.get("signature_out")
    time_in = request.form.get("time_in")
    signature2 = request.form.get("signature_in")
    
    l = []
    
    l.append(name)
    l.append(room)
    l.append(where_go)
    l.append(time_out)
    l.append(signature1)
    l.append(time_in)
    l.append(signature2)
    
    print(l)
    
    data = Hostel(name=name,room_no=room,place=where_go,time_out=time_out,signature1=signature1,time_in=time_in,signature2=signature2)
    
    db.session.add(data)
    db.session.commit()
    
    return "Data SuccessFully Added"
    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
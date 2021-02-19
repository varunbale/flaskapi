import os
from flask import Flask, request, make_response, jsonify
from firebase_admin import credentials, firestore, initialize_app
import jwt 
import datetime
from functools import wraps


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretkey'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') 

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated

@app.route('/unprotected')
def unprotected():
    return jsonify({'message' : 'Anyone can view this!'})

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message' : 'This is only available for people with valid tokens.'})

@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'varun':
        token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=2)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})



cred = credentials.Certificate('G:\key.json')
default_app = initialize_app(cred)
db = firestore.client()





@app.route('/post',methods=["POST","GET"])
@token_required
def post():
    data={"name":"varun","rollno":0,"stream":"CSE"}
    db.collection("students").add(data)
    data2={"name":"varun1","rollno":1,"stream":"CSE"}
    db.collection("students").document("p2").set(data2)
    return "data posted"

@app.route('/create/<name>/<int:num>/<stream>',methods=['POST','GET'])
def create(name,num,stream):
    db.collection('students').add({"name":name,"rollno":num,"stream":stream})
    return "inserted record"   

@app.route("/list",methods=["GET"])
@token_required
def list():
    docs = db.collection('students').get()
    result=[]
    for doc in docs:
        result.append(doc.to_dict())

    return jsonify(result)    

@app.route('/read/<no>',methods=['GET'])
def read(no):
      docs = db.collection('students').get() 
      for doc in docs:
        if doc.to_dict()["rollno"]==int(no): 
            key = doc.id
            d=db.collection('students').document(key).get()
            return d.to_dict()

      
# doc_ref = db.collection("students")
# doc = doc_ref.get()
# print(doc)
# return "Got"
    



@app.route("/update",methods=["PUT"])
def update():
    docs = db.collection('students').get() 
    for doc in docs:
        if doc.to_dict()["rollno"]==0: 
            key = doc.id
            db.collection('students').document(key).update({"stream":"cse"})     

    return "record updated"         


@app.route('/filterby/<stream>',methods=['GET','POST'])
def filterby(stream):
    docs = db.collection("students").get()
    for doc in docs:
        if doc.to_dict()['stream']==stream:
            key=doc.id
            d=db.collection('students').document(key).get() 
            return d.to_dict()   


@app.route('/delete/<no>',methods=['GET','POST'])
def delete(no):
    docs=db.collection('students').get()
    for doc in docs:
        if doc.to_dict()['rollno']==int(no):
            doc.reference.delete()
    return "record with roll no"+no+"deleted"        


@app.route('/deleteall',methods=["DELETE"])
def deleteall():
    docs = db.collection('students').get() 
    for doc in docs:
        doc.reference.delete()
    return "deleted all fields"        
        




if __name__=="__main__":
    app.run(debug=True)    




import os
from flask import Flask, request, make_response, jsonify
from firebase_admin import credentials, firestore, initialize_app


app = Flask(__name__)

cred = credentials.Certificate('G:\key.json')
default_app = initialize_app(cred)
db = firestore.client()

@app.route('/')
def index():
    if request.authorization and request.authorization.username == 'varun'and request.authorization.password=='1234':
        return "you are in"
       
    
    return make_response('Couldnt verify you')    

@app.route('/post',methods=["POST","GET"])
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




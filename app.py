from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.pnygpje.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']

    bucket_list = list(db.bucket.find({}, {'_id': False}))
    count = len(bucket_list) + 1

    doc = {
        'num':count,
        'bucket':bucket_receive,
        'done' : 0
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg': '버킷 추가 !'})

@app.route("/bucket/update", methods=["PUT"])
def bucket_update():
    num_receive = request.form['num_give']

    db.bucket.update_one({'num':int(num_receive)},{'$set':{'done':1}})
    
    return jsonify({'msg': '버킷 성공 !'})
    
@app.route("/bucket", methods=["GET"])
def bucket_get():
    all_buckets = list(db.bucket.find({},{'_id':False}))
    return jsonify({'result': all_buckets})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
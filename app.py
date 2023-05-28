from flask import Flask,redirect,url_for,render_template,request, jsonify
from pymongo import MongoClient

MONGODB_CONNECTION_STRING = "mongodb+srv://vivi:diana@cluster0.mrbjtkt.mongodb.net/?retryWrites=true&w=majority"
DB_NAME =  "project3"
client = MongoClient(MONGODB_CONNECTION_STRING)
db = client[DB_NAME]

app=Flask(__name__)
@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        nik = request.form['nik']
        nama = request.form['nama']
        jenis = request.form['jenis']
        alamat = request.form['alamat']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        tanggal_masuk = request.form['tanggal_masuk']
        nama_ayah = request.form['nama_ibu']
        nama_ibu = request.form['nama_ibu']
        doc = {
            'nik': nik,
            'nama': nama,
            'jenis': jenis,
            'alamat': alamat,
            'tempat_lahir': tempat_lahir,
            'tanggal_lahir':tanggal_lahir,
            'tanggal_masuk':tanggal_masuk,
            'nama_ayah':nama_ayah,
            'nama_ibu':nama_ibu,
        }
        db.ppdb.insert_one(doc)
        return redirect(url_for(
            'siswa', 
            nik=nik,
            nama=nama, 
            jenis=jenis, 
            alamat=alamat, 
            tempat_lahir=tempat_lahir,
            tanggal_lahir=tanggal_lahir,
            tanggal_masuk=tanggal_masuk,
            nama_ayah=nama_ayah,
            nama_ibu=nama_ibu,
            ))
    return render_template('index.html')

@app.route('/hasil')
def hasil():
    hasils = list(db.ppdb.find({}, {'_id': False}))
    return render_template('hasil_input.html', hasils=hasils)

@app.route('/siswa')
def siswa():
    nik = request.args.get('nik')
    nama = request.args.get('nama')
    jenis = request.args.get('jenis')
    alamat = request.args.get('alamat')
    tempat_lahir = request.args.get('tempat_lahir')
    tanggal_lahir = request.args.get('tanggal_lahir')
    tanggal_masuk = request.args.get('tanggal_masuk')
    nama_ayah = request.args.get('nama_ayah')
    nama_ibu = request.args.get('nama_ibu')
    return render_template('siswa.html',
                            nik=nik,
                            nama=nama, 
                            jenis=jenis, 
                            alamat=alamat, 
                            tempat_lahir=tempat_lahir,
                            tanggal_lahir=tanggal_lahir,
                            tanggal_masuk=tanggal_masuk,
                            nama_ayah=nama_ayah,
                            nama_ibu=nama_ibu,
                           )

@app.route("/delete/<nik>")
def delete(nik):
    db.ppdb.delete_one(
        {'nik':nik}
    )
    return redirect('/hasil')

@app.route('/admin')
def admin():
    return render_template('login_admin.html')


@app.route('/sign_in', methods=['POST'])
def sign_in():
    username_receive = request.form["username_give"]
    password_receive = request.form["password_give"]
    result = db.users.find_one(
        {
            "username": username_receive,
            "password": password_receive,
        }
    )
    
    if result:
        payload = {
            "id": username_receive,
        }

        return jsonify(
            {
                "result": "success",
            }
        )
        
    else:
        return jsonify(
            {
                "result": "fail",
                "msg": "We could not find a user with that id/password combination",
            }
        )
    

@app.route('/sign_up_admin')
def sign_up_admin():
   return render_template('sign_up_admin.html')


@app.route('/input')
def input():
   return render_template('input.html')

@app.route('/sign_up_siswa', methods=['POST'])
def sign_up_siswa():
   return render_template('sign_up_siswa.html')

@app.route("/sign_up/save", methods=["POST"])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    doc = {
        "username": username_receive,
        "password": password_receive,                                       
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)
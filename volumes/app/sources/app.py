from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from hashids import Hashids
from flask_dropzone import Dropzone
from werkzeug.utils import secure_filename
from time import time
import os, shutil
import random, string
import bcrypt

#------------------------------------------------------------------------

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
from models import *

dropzone = Dropzone(app)

#------------------------------------------------------------------------

hashids = Hashids(min_length=64, salt=app.config['SECRET_KEY'])

#------------------------------------------------------------------------

@app.route('/', methods=['GET', 'POST'])
async def index():
    if request.method == 'POST':
        filename = os.listdir('../files/tmp/')[0]

        ftime = request.form.get('time')
        source = '../files/tmp/'+filename
        destination = '../files/'+ftime+'/'+str(time())+'/'
        os.mkdir(destination)
        shutil.move(source, destination+filename)

        one_dl = request.form.get('one_dl')
        print('one_dl = ',one_dl)
        if not one_dl:
            one_dl = 0
        else:
            one_dl = 1

        fpassword = request.form.get('fpassword')
        if fpassword:
            fpassword = bcrypt.hashpw(fpassword.encode('utf-8'), bcrypt.gensalt())
        else:
            fpassword = None

        finfo = Files(fpath = destination, fname = filename, one_dl = one_dl, fpassword = fpassword)
        db.session.add(finfo)
        db.session.commit()

        hid =  hashids.encode(finfo.id)
        file_url = Files.query.filter_by(id = finfo.id).first()
        file_url.url = os.getenv('URL')+hid
        file_url.download_url = os.getenv('URL')+'download/'+hid+'/'+filename
        db.session.commit()

        return render_template('index.html', download_url = os.getenv('URL')+hid)
    else:
        return render_template('index.html')  

@app.route('/upload', methods=['POST'])
def upload():
    # Store files
    for key, f in request.files.items():
        if key.startswith('file'):
            filename = f.filename
            fpath = os.path.join('../files/tmp', secure_filename(filename))
            f.save(fpath)

    # Compress multiple files
    nb_files = len(list(request.files.items()))
    if nb_files > 1:
        filename = ''.join(random.choice(string.ascii_uppercase) for i in range(10))
        
        os.mkdir('../files/tmp/'+filename)

        allfiles = os.listdir('../files/tmp/')
        for f in allfiles:
            shutil.move('../files/tmp/'+f, '../files/tmp/'+filename)
        
        shutil.make_archive('../files/tmp/'+filename, 'zip', '../files/tmp/'+filename)
        shutil.rmtree('../files/tmp/'+filename)
        filename = filename+'.zip'
    return '', 204

@app.route('/<hid>')
def url_redirect(hid):
    original_id = hashids.decode(hid)
    if original_id:
        original_id = original_id[0]
        finfo = Files.query.filter_by(id = original_id).first()

        finfo.clicks = finfo.clicks+1
        db.session.commit()

        if finfo.one_dl == 1 and finfo.clicks > 1:
            shutil.rmtree(finfo.fpath)

        if finfo.fpassword:
            return redirect(url_for('locked', hid = hid))
            
        else:
            return send_from_directory(finfo.fpath, finfo.fname, as_attachment = True)
    else:
        return 'Not Found'

@app.route('/locked/<hid>', methods=['GET', 'POST'])
def locked(hid):
    if request.method == 'GET':
        return render_template('locked.html', hid = hid)
    else:
        original_id = hashids.decode(hid)
        if original_id:
            original_id = original_id[0]
            finfo = Files.query.filter_by(id = original_id).first()

            password = request.form.get('password')
            if bcrypt.checkpw(password.encode('utf-8'), finfo.fpassword):
                return send_from_directory(finfo.fpath, finfo.fname, as_attachment = True)
            else:
                return 'Bad password'
        else:
            return 'Not Found'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
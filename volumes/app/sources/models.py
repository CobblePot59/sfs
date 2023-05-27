from app import app, db
from datetime import datetime

class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fpath = db.Column(db.String(255), default='', nullable=False)
    fname = db.Column(db.String(255), default='', nullable=False)
    fpassword = db.Column(db.String(255), default='', nullable=False)
    url = db.Column(db.String(255), default='', nullable=False)
    download_url = db.Column(db.String(255), default='', nullable=False)
    one_dl = db.Column(db.Boolean, default=0, nullable=False)
    clicks = db.Column(db.Integer, default=0, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

with app.app_context():
    db.create_all()

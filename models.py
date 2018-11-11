from app import db

class Posts(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title,body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class Users(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    post = db.relationship('Posts', backref='owner')

    def __init__(self, user, password):
        self.user = user
        self.password = password
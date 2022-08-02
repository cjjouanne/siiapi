from src import db, login_manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    sessionType = db.Column(db.String(20), nullable=False)
    apiKey = db.Column(db.String(300), nullable=False)
    companies =  db.relationship('Company', backref='user', lazy=True)

    def get_company_ruts(self):
        return [i.rut for i in self.companies]

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "sessionType": self.sessionType,
        }

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}', {self.sessionType})"
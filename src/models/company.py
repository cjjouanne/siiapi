from src import db


class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40), nullable=False)
    rut = db.Column(db.String(50), nullable=False)
    apiKey = db.Column(db.String(300), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rut": self.rut,
            "userId": self.userId
        }

    @staticmethod
    def load_company(company_id):
        return Company.query.get(str(company_id)).serialize()

    @staticmethod
    def load_company_by_name(name):
        return Company.query.filter_by(name=str(name)).first()

    def __repr__(self):
        return f"Institution('{self.id}', '{self.name}', '{self.rut}')"
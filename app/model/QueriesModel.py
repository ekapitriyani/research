from app import db
from app.model.DetailsModel import Details

class Queries(db.Model):
    __tablename__ = "queries"  # Define nama tabel

    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    query_name = db.Column(db.String, nullable=False)
    details = db.relationship("Details", backref="queries", lazy="dynamic")

    def __init__(self, query):
        self.query_name = query

    def __repr__(self):
        return "<Query: {}>".format(self.query)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def getAll():
        queries = Queries.query.all()
        result = list()
        for data in queries:
            print(data.details)
            obj = {
                "id": data.id,
                "query": data.query_name,
                "details": Details.getAll(data.id)
            }
            result.append(obj)
        return result

    @staticmethod
    def findByQueryName(queryName):
        data = Queries.query.filter_by(query_name=queryName).first()
        if data is None:
            return None
        else:
            obj = {
                "id": data.id,
                "query": data.query_name,
                "details": Details.getAll(data.id)
            }
            return obj

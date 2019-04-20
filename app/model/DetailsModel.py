from app import db


class Details(db.Model):
    __tablename__ = "details"  # Define nama table

    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    document = db.Column(db.String, nullable=False)
    label = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Float, nullable=False)
    pembimbing = db.Column(db.String, nullable=False)
    query_id = db.Column(db.Integer, db.ForeignKey("queries.id"))

    def __init__(self, data):
        document, label, score, pembimbing = data
        self.document = document
        self.label = label
        self.score = score
        self.pembimbing = pembimbing

    def __repr__(self):
        return "<Pembimbing: {}>".format(self.pembimbing)

    @staticmethod
    def getAll(queryId):
        details = Details.query.filter_by(query_id=queryId).order_by(Details.score.desc()).all()
        result = list()
        for data in details:
            obj = {
                "id": data.id,
                "document": data.document,
                "label": data.label,
                "score": data.score,
                "pembimbing": data.pembimbing
            }
            result.append(obj)
        return result

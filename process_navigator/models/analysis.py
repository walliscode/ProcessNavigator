from process_navigator.extensions import db


class AnalysisMethod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    analysis_method_part = db.relationship(
        "AnalysisMethodPart", backref=db.backref("analysis_method", lazy=True)
    )

    def __repr__(self):
        return f"<Analysis Method {self.name}>"


class AnalysisMethodPart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    analysis_method_id = db.Column(
        db.Integer, db.ForeignKey("analysis_method.id"), nullable=False
    )

    analysismethod = db.relationship(
        "AnalysisMethod", backref=db.backref("analysis_method_part", lazy=True)
    )

    def __repr__(self):
        return f"<Analysis Method Part {self.name}>"

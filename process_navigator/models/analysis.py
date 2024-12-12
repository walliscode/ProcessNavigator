from process_navigator.extensions import db


class AnalysisMethod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    analysis_method_part = db.relationship(
        "AnalysisMethodPart", back_populates="analysis_method"
    )

    def __repr__(self):
        return f"<Analysis Method {self.name}>"


class AnalysisMethodPart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    analysis_method_id = db.Column(
        db.Integer, db.ForeignKey("analysis_method.id"), nullable=False
    )

    analysis_method = db.relationship(
        "AnalysisMethod", back_populates="analysis_method_part"
    )

    def __repr__(self):
        return f"<Analysis Method Part {self.name}>"

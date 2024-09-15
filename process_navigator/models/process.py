from process_navigator.extensions import db

class Entity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    

    def __repr__(self):
        return f'<Entity {self.name}>'
    

    

class Method(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    entity_id = db.Column(db.Integer, db.ForeignKey('entity.id'), nullable=False)
    entity = db.relationship('Entity', backref=db.backref('methods', lazy=True))
    

    def __repr__(self):
        return f'<Method {self.name}>'
    
class MethodParts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    method_id = db.Column(db.Integer, db.ForeignKey('method.id'), nullable=False)
    method = db.relationship('Method', backref=db.backref('method_parts', lazy=True))
    

    def __repr__(self):
        return f'<MethodParts {self.name}>'
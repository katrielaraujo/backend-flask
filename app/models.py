from app import db, bcrypt

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(60), nullable=False)
    vendas = db.relationship('Venda', backref='usuario', lazy=True)

    def verificar_senhar(self, senha):
        return bcrypt.check_password_hash(self.senha, senha)

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_cliente = db.Column(db.String(100), nullable=False)
    produto = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data_venda = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

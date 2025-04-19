class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    pizza_name = db.Column(db.String, nullable=False)
    normal_qty = db.Column(db.Integer, nullable=False)
    maxi_qty = db.Column(db.Integer, nullable=False)
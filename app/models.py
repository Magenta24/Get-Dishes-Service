from app import db

#associative tables
DishIngredients = db.Table('Dish_Ingredients', db.Model.metadata,
    db.Column('dish_id', db.Integer, db.ForeignKey('Dish.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('Ingredient.id'), primary_key=True)
)

# concertParticipation = db.Table('concertParticipation', db.Model.metadata,
#     db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
#     db.Column('concert_id', db.Integer, db.ForeignKey('concerts.id'))
# )

class Dish(db.Model):
    __tablename__ = 'Dish'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    #ingredients = db.relationship('Ingredient', secondary=DishIngredients, lazy='subquery', backref=db.backref('dishes', lazy=True))
    ingredients = db.relationship('Ingredient',secondary=DishIngredients, overlaps="Dish")

    def __repr__(self):
            return '{}{}{}'.format(self.id, self.name, self.ingredients)

class Ingredient(db.Model):
    __tablename__ = 'Ingredient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.Integer,  db.ForeignKey('Ingredient_Category.id'))

    def __repr__(self):
            return '{}{}{}'.format(self.id, self.name, self.category)

class IngredientCategory(db.Model):
    __tablename__ = 'Ingredient_Category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
            return '{}{}'.format(self.id, self.name)

#associative tables
UserIngredients = db.Table('User_Ingredients', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('User.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('Ingredient.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.relationship('Ingredient',secondary=UserIngredients, overlaps="User")

    def __repr__(self):
            return '{}{}'.format(self.id, self.name)



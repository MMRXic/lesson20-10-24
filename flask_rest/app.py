from config import Config
from flask import Flask, request
from models import db, Pizza
from flask_restful import Resource, Api


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
api = Api(app)
with app.app_context():
    db.create_all()


class PizzaListResource(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        return [pizza.to_dict() for pizza in pizzas]

    def post(self):
        data = request.get_json()
        new_pizza = Pizza(
            name = data["name"],
            price = data["price"],
            ingredients = data["ingredients"]
        )
        db.session.add(new_pizza)
        db.session.commit()
        return new_pizza.to_dict(), 201

api.add_resource(PizzaListResource, "/pizzas")
if __name__ == '__main__':
    app.run(debug=True)


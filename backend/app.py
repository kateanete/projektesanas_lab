from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Norādiet pareizo ceļu līdz SQLite datu bāzes failam
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food_database_detailed_allergens.db'
db = SQLAlchemy(app)

class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    calories = db.Column(db.Float, nullable=False)
    allergens = db.Column(db.String(80))

@app.route('/get_alternatives', methods=['POST'])
def get_alternatives():
    data = request.json
    izvēlētie_produkti = data['selected_items']
    lietotāja_alerģijas = data['allergies']
    kopējais_kaloriju_daudzums = data['total_calories']

    alternatīvas = []
    for produkts in izvēlētie_produkti:
        pārtikas_produkti = FoodItem.query.filter_by(name=produkts['name']).first()
        if pārtikas_produkti and pārtikas_produkti.allergens in lietotāja_alerģijas:
            # Atrast alternatīvu produktu
            alternatīvie_produkti = FoodItem.query.filter(FoodItem.allergens.notin_(lietotāja_alerģijas)).all()
            # Loģika, lai atrastu labākās alternatīvas
            # ...
            alternatīvas.append({'oriģinālais': pārtikas_produkti.name, 'alternatīvas': [alt.name for alt in alternatīvie_produkti]})
    
    # Aprēķināt kopējo produktu svaru, balstoties uz kopējām kalorijām un lietotāja ēdienreizēm
    # ...

    return jsonify({'alternatīvas': alternatīvas, 'kopējais_svars': 'aprēķinātais_svars'})

if __name__ == '__main__':
    app.run(debug=True)

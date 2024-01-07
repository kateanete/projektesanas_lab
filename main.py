from website import create_app
from website.models import Food, db

app = create_app()

with app.app_context():
    if db.session.query(Food).count() == 0:
        Food.import_food_data("website/Food_Alergy.csv")

if __name__ == "__main__":
    app.run(debug=True)

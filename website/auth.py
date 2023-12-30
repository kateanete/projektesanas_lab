from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template("login.html", boolean=False)

@auth.route('/logout')
def logout():
    return "<p>logout</p>"
@auth.route('/ievade',  methods=['GET', 'POST'])
def ievade():
    if request.method == 'POST':
        garums = request.form.get('garums')
        svars = request.form.get('svars')
        kalorijas = request.form.get('kalorijas')
        
        if garums is '':
            flash('Ievadiet garumu', category='error')
        if svars is '':
            flash('Ievadiet svaru', category='error')
        else:
            flash ('Izmaiņas saglabātas, varat izveidot ēdienkarti.', category='success')
    
    return render_template("ievade.html")


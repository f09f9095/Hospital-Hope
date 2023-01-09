from flask import Flask, render_template, request, session, redirect, url_for
from forms import SearchForm

from src.db_conn import db_connect, sql
from src.dictionary import fouls, allowed_insurances, ROOT


app = Flask(__name__)

# Flask configuration class
class conf:
    app.config['SECRET_KEY'] = 'qwerty'


# Home page
@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    # if form.validate_on_submit():
    if request.method == 'POST':
        session['state'] = form.state.data
        session['city'] = form.city.data
        session['hospital'] = form.hospital.data
        session['insurance'] = form.insurance.data
        session['search_type'] = form.search_type.data
        session['search_text'] = form.search_text.data
        return redirect(url_for('results'))
    return render_template('index.html', form=form)

# Edit city list after state has been selected
@app.route('/cities/<state>', methods=['GET'])
def city_edit(state):
    cursor = db_connect(ROOT / "hospital.db").cursor()
    cities = cursor.execute('''
        SELECT DISTINCT city
        FROM hospitals
        WHERE state="{}"
        ORDER BY city ASC
        '''.format(state))
    city_list = [citi[0].title() for citi in cities.fetchall()]
    return {'cities': city_list}

# Edit hospital list after city and state have been selected
@app.route('/hospitals/<city>/<state>', methods=['GET'])
def hospital_edit(city, state):
    cursor = db_connect(ROOT / "hospital.db").cursor()
    hospitals = cursor.execute('''
        SELECT DISTINCT name
        FROM hospitals
        WHERE city="{}"
        AND state="{}"
        ORDER BY name ASC
        '''.format(city, state))
    hospital_list = [hos[0].title() for hos in hospitals.fetchall()]
    return {'hospitals': hospital_list}

# Edit insurance list after hospital has been selected.
# I need to figure out how to get a list of DISTINCT
# insurances used by each hospital.
# Some hospitals list pricing for each insurer as columns,
# others list them in a single column.
# I'll probably need different funcs for columns and one
# for a single column.
@app.route('/insurances/<hospital>', methods=['GET'])
def insurance_edit(hospital):
    cursor = db_connect(ROOT / "chargemaster.db").cursor()
    insurances = cursor.execute('''
        PRAGMA table_info('{}')
        '''.format(hospital)
        )
    insurance_list = [ins[1] for ins in insurances.fetchall()]
    insurance_list = [ins.title() for ins in insurance_list if ins.lower() in allowed_insurances]
    print(insurance_list)
    return {'insurances': insurance_list}

# Search results page
@app.route('/results', methods=['GET'])
def results():
    cursor = db_connect(ROOT / "chargemaster.db").cursor()
    if request.method == 'GET':
        try:
            result = cursor.execute('''
                SELECT description, "base price", "{}"
                FROM "{}"
                WHERE description LIKE "%{}%"
                ORDER BY description ASC
                '''.format(
                    session['insurance'],
                    session['hospital'],
                    session['search_text'].lower()
                    )
                )
            result_list = [
                (description, base_price, insurance_price)
                for
                (description, base_price, insurance_price)
                in result.fetchall()
                ]
            print(result_list)
        except sql.DatabaseError as e:
            print(e)
    return render_template(
        'results.html',
        result_list=result_list
        )

# 404 error
@app.errorhandler(404)
def four_oh_four(error):
    return render_template('404.html'), 404

# Start app
if __name__ == '__main__':
    app.run(debug=True)

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired

from src.db_conn import db_connect
from src.dictionary import ROOT


class SearchForm(FlaskForm):
    cursor = db_connect(ROOT / "hospital.db").cursor()
    # Get list of states from database
    state_list = cursor.execute('''
        SELECT DISTINCT state
        FROM hospitals
        ORDER BY state ASC''')
    #Populate state SelectField
    state = SelectField(label='State', choices=[state[0].upper() for state in state_list.fetchall()])
    city = SelectField(label='City', choices=[], validators=[DataRequired()])
    hospital = SelectField(label='Hospital', choices=[], validators=[DataRequired()])
    insurance = SelectField(label='Insurance', choices=[
        ('uninsured', 'Uninsured')
        ])
    search_type = SelectField(label='Search type', choices=[
        ('procedure', 'Procedure'), ('code', 'Medical Code')
        ])
    search_text = StringField(label='Search', validators=[DataRequired()])
    search_button = SubmitField('Search')
# import Flask object (named as the folder in which the __init__ is located)
from app import app

from flask import Blueprint, render_template, request, redirect, jsonify, make_response
import pandas as pd
import logging
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, NumberRange

# Flask WTForms allow built-in validation of data entries before page submission
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    DateTimeField,
    TimeField,
    validators
)

logging.basicConfig(
    # Log the time (YYYY-MM-DD HH:MM:SS), module name, line of code from which log was called,
    #   level of logging event (e.g., DEBUG, INFO, CRITICAL), and log message
    format='%(asctime)s %(module)s %(lineno)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

class VizData():
    def __init__(self, oper_name, trans_str, trans_end, missn_str, missn_end, oper_data):
        self.oper_name = oper_name
        self.trans_str = trans_str
        self.trans_end = trans_end
        self.missn_str = missn_str
        self.missn_end = missn_end
        self.oper_data = oper_data


# Generate a Flask Blueprint (not necessary for an app this small, but good modular practice)
view_BP = Blueprint("op_viz", __name__, template_folder='templates')

# Use a Report Form for validation of data entries before page submission
class ReportForm(FlaskForm):
    # CSRF validation is not necessary
    class Meta:
        csrf = False

    oper_name = StringField('Operation Name', validators=[validators.length(max=25), validators.DataRequired('Operation Name is required')])

    trans_str = TimeField('Transit Start', format='%H:%M', validators=[validators.Optional()])
    trans_end = TimeField('Transit End', format='%H:%M', validators=[validators.Optional()])

    missn_str = TimeField('Mission Start', format='%H:%M', validators=[validators.DataRequired(message='Mission Start is required')])
    missn_end = TimeField('Mission End', format='%H:%M', validators=[validators.DataRequired(message='Mission End is required')])

    oper_data = FileField('XXX Excel Upload', validators=[FileRequired('XXX File is required'),
                                                          FileAllowed(['xlsx', 'xlsm', 'xls'], 'Only Excel-formatted files are allowed (.xlsx, .xlsm, .xls)')])
    
    submit = SubmitField('Generate View')


# Create a default load page - will be a user-input page for visualization
@view_BP.route('/', methods=['GET', 'POST'])
def index():
    form = ReportForm()
    logging.info('On Intro Page')

    # Load input.html on initial load
    if request.method == 'GET':
        return render_template('input.html', form=form)

    # Load the vizualization page when form is sent ('POST')
    elif form.validate():
        # If the user doesn't submit an excel-type file, reload with a warning message
        user_data = VizData(form.oper_name.data, form.trans_str.data, form.trans_end.data,
                            form.missn_str.data, form.missn_end.data, form.oper_data.data)
        return render_template('visual.html', user_data=user_data)
    else:

        return render_template('input.html', form=form)
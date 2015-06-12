from flask import render_template
from flask.ext.classy import FlaskView


class StructuresView(FlaskView):
    route_base = '/structures'

    def index(self):
        return render_template('structures/index.html')

    def new_structure(self):
        return render_template('structures/new_structure.html')

    def dscan(self):
        pass

from flask import render_template
from flask.ext.classy import FlaskView


class RadarView(FlaskView):
    route_base = '/radar'

    def index(self):
        return render_template('radar/index.html')

    def new_structure(self):
        return render_template('radar/new_structure.html')

    def dscan(self):
        pass

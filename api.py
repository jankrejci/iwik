from flask import request, jsonify
import core
from flask import Flask, render_template, make_response
import json
from datetime import datetime as dt
from forms import SearchForm
from database import writeJourney

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True


@app.route('/iwik/search', methods=["GET", "POST"])
def search():
    form = SearchForm(csrf_enabled=False)
    if form.validate_on_submit():
        source = request.form.get('source') # get data
        destination = request.form.get('destination')
        departure_date = request.form.get('departure_date')

        app = core.Core()
        trains = app.getTrains(source, destination, departure_date)

        for train in trains:
            writeJourney(train)
        
        template = render_template('train_list.html', trains=trains)
        return make_response(template)
    return render_template('index.html', form=form)


if __name__ == '__main__':
   app.run(debug=True)

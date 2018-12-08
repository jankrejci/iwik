from flask import request, jsonify
import core
from flask import Flask, render_template
import json
from datetime import datetime as dt


app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True


@app.route('/ping')
def ping():
  return 'pong'


@app.route('/search', methods=['GET'])
def search():
  source = request.args.get('source')
  destination = request.args.get('destination')
  date_from = request.args.get('date_from')
  date_from = dt.strptime(date_from, "%Y-%m-%d").strftime("%d.%m.%Y")

  app = core.Core()
  trains = app.getTrains(source, destination, date_from)
  return render_template('train_list.html', trains=trains)


if __name__ == '__main__':
   app.run(debug=True)

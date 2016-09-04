from flask import Flask, render_template, request, redirect
import requests
import numpy as np

from bokeh.layouts import gridplot
from bokeh.plotting import figure
from bokeh.embed import components
import pandas as pd
from pandas import DataFrame

def datetime(x):
    return np.array(x, dtype=np.datetime64)

app = Flask(__name__)

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('userinfo.html')
    else:
        stock = request.form['stockticker']
        api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json' % stock
        session = requests.Session()
        session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
        raw_data = session.get(api_url)
        df = raw_data.json()
        data = DataFrame(data = df['data'], columns = df['column_names'])

        p1 = figure(tools=TOOLS,
                     title='Stock Closing Prices',
                     x_axis_label='date',
                     x_axis_type='datetime')
        p1.grid.grid_line_alpha=0.3
        p1.xaxis.axis_label = 'Date'
        p1.yaxis.axis_label = 'Price'
        p1.line(datetime(data['Date']), data['Adj. Close'], color='#A6CEE3', legend=stock)
        p1.legend.location = "top_left"

        """aapl = np.array(AAPL['adj_close'])
        aapl_dates = np.array(AAPL['date'], dtype=np.datetime64)

        window_size = 30
        window = np.ones(window_size)/float(window_size)
        aapl_avg = np.convolve(aapl, window, 'same')

        p2 = figure(x_axis_type="datetime", title="AAPL One-Month Average")
        p2.grid.grid_line_alpha = 0
        p2.xaxis.axis_label = 'Date'
        p2.yaxis.axis_label = 'Price'
        p2.ygrid.band_fill_color = "olive"
        p2.ygrid.band_fill_alpha = 0.1

        p2.circle(aapl_dates, aapl, size=4, legend='close',
                  color='darkgrey', alpha=0.2)

        p2.line(aapl_dates, aapl_avg, legend='avg', color='navy')
        p2.legend.location = "top_left"

        plot = figure(tools=TOOLS,
                      title='Stock Closing Prices',
                      x_axis_label='date',
                      x_axis_type='datetime')
        """
        script, div = components(p1)
        return render_template('graph.html',stockticker=stock, script=script, div=div)

if __name__ == '__main__':
  app.run(port=33507)

from flask import Flask, render_template, request, redirect, Markup
# import pandas as pd
import requests
import simplejson
import datetime
# from bokeh.plotting import figure, output_file, show
# from bokeh.models import ColumnDataSource, DatetimeTickFormatter, NumeralTickFormatter
# from bokeh.embed import components

app = Flask(__name__)

today=datetime.date.today()
month_ago=today-datetime.timedelta(weeks=4)
app.today=today.strftime("%Y-%m-%d")
app.month_ago=month_ago.strftime("%Y-%m-%d")

def convert_date(some_date):
    year, month, date=some_date.split('-')
    new_date=datetime.date(int(year), int(month), int(date))
    return new_date

@app.route('/', methods=['GET'])
def main():
    return render_template('mainPage.html')

@app.route('/data', methods=['GET'])
def data_sources():
    return render_template('dataPage.html')

@app.route('/boot', methods=['GET'])
def tester():
    return render_template('bootstrap_example.html')

@app.route('/scatter', methods=['GET'])
def scatter_pplot():
    return render_template('test3.html')
    # return render_template('error_page.html', ticker='gooop')

@app.route('/error', methods=['GET'])
def data():
    return render_template('error_page.html')


@app.route('/index', methods=['GET'])
def index_page():
    return render_template('mainPage.html')

@app.route('/test', methods=['GET'])
def test_page():

    return render_template('testTemplate.html')

@app.route('/graph', methods=['POST'])
def graph():
    closing_flag, adjusted_flag, volume_flag= [False, False, False]
    ticker=request.form['ticker'].upper()
    # print request.form.keys()
    if 'ticker' in request.form.keys():
        ticker_flag=True
    url='https://www.quandl.com/api/v3/datasets/WIKI/'+ticker+'.json?order=asc&exclude_headers=true&start_date=' + app.month_ago  + '&end_date='+ app.today + '?api_key=KE-fEmypRC5zT61Bs4QT'
    # print url
    r = requests.get(url)
    if r.status_code==404:
        return render_template('error_page.html', ticker=ticker)
    else:

        foo=r.json()
        values=foo[u'dataset'][u'data']
        column_names=foo[u'dataset'][u'column_names']
        valDF=pd.DataFrame(values, columns=column_names )
        valDF['Date']=valDF['Date'].map(convert_date)

        p1=figure(title= 'Data from Quandle WIKI set', plot_height=600, plot_width=600)
        p1.xaxis.axis_label="Date"


        if 'closing_box' in request.form.keys():
            closing_flag=True
            p1.line(valDF['Date'],valDF['Close'], color= "#2222aa", line_width=3,  name="foo", legend=ticker+": Close")
        if 'adjusted_box' in request.form.keys():
            adjusted_flag=True
            p1.line(valDF['Date'],valDF['Adj. Close'], color= "#DB9911", line_width=3,  name="foo", legend=ticker+": Adj. Close")
        if 'volume_box' in request.form.keys():
            volume_flag=True
            p1.line(valDF['Date'],valDF['Volume'], color= "#009900", line_width=3,  name="foo", legend=ticker+": Volume")

        p1.xaxis[0].formatter = DatetimeTickFormatter(formats=dict(days=['%b %d, %Y'],months=['%b- %Y'],years=['%b- %Y']))
        p1.yaxis[0].formatter = NumeralTickFormatter(format='0,0')

        # print 'closing_box' in request.form.keys(), 'adjusted_box' in request.form.keys(), 'volume_box' in request.form.keys()
        # print closing_flag,adjusted_flag, volume_flag


        # p1.line(valDF['Date'],valDF['Close'], color= "#2222aa", line_width=3,  name="foo", legend=ticker+": Close")
        # plot = figure(title= 'Data from Quandle WIKI set')
        # plot.circle( [1,2], [3,4])
        plot_script, plot_div = components(p1)

        # return render_template('interim.html', ticker=request.form['ticker'], closing_flag= request.form['closing_flag'], adjusted_flag= request.form['adjusted_flag'], volume= request.form['volume_flag'])
        return render_template('interim.html', ticker=ticker, plot_script=Markup(plot_script), plot_div=Markup(plot_div))

if __name__ == '__main__':
  app.run(port=33507)
  # app.run(debug=True)


from flask import Flask, Response
from analysis import loadData, createChart

data = loadData()
app = Flask(__name__, static_url_path='', static_folder='.')
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))

@app.route('/vis/<zip>')
def visualize(zip):
    df = data
    #zip = '10017'
    DFFiltered = df[['cuisine','perZip.' + zip]]
    DFFiltered.rename(columns={'perZip.' + zip: 'total'}, inplace=True)
    DFFiltered = DFFiltered.dropna(axis=0, how='any')
    DFFiltered = DFFiltered.sort_values(by=['total'], ascending=False)[:25][['cuisine', 'total']]
    response = ''
    if DFFiltered is not None:
        response = createChart(DFFiltered, zip).to_json()

    return Response(response,
        mimetype='application/json',
        headers={
            'Cache-Control': 'no-cache',
            'Access-Control-Allow-Origin': '*'
        }
    )

if __name__ == '__main__':
    app.run(port=8002)
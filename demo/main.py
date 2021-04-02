from flask import Flask, send_from_directory, request, escape, render_template, jsonify, make_response

from demo.index import index
from demo.engine import boolean_search

app = Flask(__name__)


@app.route("/")
def root():
    return render_template('index.html')


@app.route("/search", methods=['GET'])
def search():
    query = str(escape(request.args.get("query", "")))
    pages, q, rq = boolean_search(query)
    json = []
    for hash in pages:
        json.append({'link': index.hash_index[hash].url, 'title': index.hash_index[hash].title})
    print(json)
    return jsonify(json)


@app.route("/index", methods=['GET'])
def get_index():
    print(index.reverse_index)
    response = app.response_class(
        response=index.to_json(),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/index", methods=['POST'])
def index_page():
    url = str(escape(request.form['url']))
    index.index(url)
    return ""


# TODO database saveng & new page indexing
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

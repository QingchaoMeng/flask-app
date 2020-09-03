from flask import Flask, render_template, request, jsonify
from urllib.request import urlopen
from urllib import parse
import simplejson

app = Flask(__name__)

SUGGEST_BASE_PATH = 'http://localhost:8983/solr/techproducts/suggest?suggest=true&suggest.build=true&suggest' \
                    '.dictionary=mySuggester&wt=json&suggest.q='
SEARCH_BASE_PATH = 'http://localhost:8983/solr/techproducts/select?q=cat:'


@app.route('/', methods=["GET", "POST"])
def search():
    query = None
    numbers = None
    results = None

    # get the search term
    if request.method == "POST":
        query = request.form["autocomplete"]

        # return all results if no input provided
        if query is None or query == "":
            query = "*:*"

        # query for information and return results
        connection = urlopen("{}{}".format(SEARCH_BASE_PATH, parse.quote(query)))
        response = simplejson.load(connection)

        numbers = response['response']['numFound']
        results = response['response']['docs']

    return render_template('index.html', query=query, numresults=numbers, results=results)


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    results = None
    query = request.args.get('q')
    if query is not None:
        connection = urlopen("{}{}".format(SUGGEST_BASE_PATH, parse.quote(query)))
        response = simplejson.load(connection)
        results = response['suggest']['mySuggester'][query]['suggestions']
    return jsonify(matching_results=results)


if __name__ == '__main__':
    app.run(debug=True)

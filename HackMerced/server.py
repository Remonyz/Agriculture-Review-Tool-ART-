from flask import Flask, render_template, request, jsonify
import database

app = Flask(__name__, static_folder='static')

@app.route("/")
def home():
    return render_template("HMP.html")

@app.route("/HMP.html")
def home1():
    return render_template("HMP.html")

@app.route("/HMP2.html")
def search_by_state():
    return render_template("HMP2.html")

@app.route("/HMP3.html")
def compare():
    return render_template("HMP3.html")


@app.route("/get_crop_info")
def get_crop_info():
    state = request.args['state']
    commodity = request.args['commodity']
    acres = float(request.args['acres'])  # Convert acres to float
    profitableCommodity, highestValue = database.findMostProfitable(state)
    profitPerAcre, ppu = database.findProfitPerAcre(state, commodity)
    marginOfError = database.marginOfError(state, commodity)

    # Calculate the possible valuation
    possible_valuation = profitPerAcre * acres

    return jsonify({
        'Profitable Commodity': profitableCommodity,
        'Highest Value': highestValue,
        'Profit Per Acre': profitPerAcre,
        'Possible Valuation': possible_valuation,
        'PPU': ppu,
        f'Margin Of Error For {commodity}': f'{marginOfError}%' if marginOfError is not None else None
    })

@app.route("/getState")
def getState():
    states = database.getState()
    return states

@app.route("/getCommodities")
def getCommodities():
    state = request.args.get('state')  # Get the selected state from the request
    commodities = database.getCommodities(state)
    return jsonify(commodities)

app.run(port=3000, host="0.0.0.0", debug=True)

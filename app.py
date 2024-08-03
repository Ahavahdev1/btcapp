from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# URL da API do CoinGecko para obter o preço do BTC
COINGECKO_API_URL = 'https://api.coingecko.com/api/v3/simple/price'
COINGECKO_PARAMS = {
    'ids': 'bitcoin',
    'vs_currencies': 'usd'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_btc_price')
def get_btc_price():
    try:
        response = requests.get(COINGECKO_API_URL, params=COINGECKO_PARAMS)
        response.raise_for_status()
        data = response.json()
        btc_price = data['bitcoin']['usd']
        return jsonify(btc_price=btc_price)
    except requests.RequestException as e:
        return jsonify(error=str(e)), 500

@app.route('/get_btc_amount')
def get_btc_amount():
    value = request.args.get('value', type=float)
    if value is None:
        return jsonify(amount_btc=0.00)
    
    try:
        response = requests.get(COINGECKO_API_URL, params=COINGECKO_PARAMS)
        response.raise_for_status()
        data = response.json()
        btc_price = data['bitcoin']['usd']
        amount_btc = value / btc_price
        return jsonify(amount_btc=amount_btc)
    except requests.RequestException as e:
        return jsonify(error=str(e)), 500

@app.route('/add', methods=['POST'])
def add():
    value = request.form.get('value', type=float)
    if value is None:
        return render_template('index.html', error="Valor inválido")

    try:
        response = requests.get(COINGECKO_API_URL, params=COINGECKO_PARAMS)
        response.raise_for_status()
        data = response.json()
        btc_price = data['bitcoin']['usd']
        amount_btc = value / btc_price
        
        # Aqui você deve calcular o lucro/prejuízo e porcentagem
        # Exemplo simplificado:
        profit_loss = 0  # Substitua pelo cálculo real
        profit_loss_percentage = 0  # Substitua pelo cálculo real
        
        return render_template('index.html', value=value, btc_price=btc_price, amount_btc=amount_btc, profit_loss=profit_loss, profit_loss_percentage=profit_loss_percentage)
    except requests.RequestException as e:
        return render_template('index.html', error=f"Erro ao obter preço do BTC: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)

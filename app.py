
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# Updated accounts configuration
BUSINESS_UPI = "Q978110034@ybl"       # For amounts < 2000
PERSONAL_UPI = "8826705336@ptyes"     # For amounts >= 2000

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quick Pay</title>
    <style>
        body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: #f4f7f6; }
        .card { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); width: 100%; max-width: 350px; text-align: center; }
        input { width: 100%; padding: 12px; font-size: 18px; margin: 15px 0; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; text-align: center; }
        button { background: #00baf2; color: white; border: none; padding: 12px; width: 100%; font-size: 18px; border-radius: 6px; cursor: pointer; font-weight: bold; }
        button:hover { background: #0098c7; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Enter Bill Amount</h2>
        <form action="/pay" method="POST">
            <input type="number" step="0.01" name="amount" placeholder="₹ Amount" required autofocus>
            <button type="submit">Proceed to Pay</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/pay', methods=['POST'])
def pay():
    try:
        amount = float(request.form['amount'])
    except ValueError:
        return "Invalid amount", 400

    # Conditional routing logic based on threshold
    if amount < 2000:
        target_vpa = BUSINESS_UPI
        narration = "Business Payment"
    else:
        target_vpa = PERSONAL_UPI
        narration = "Personal Payment"

    # Construct standard UPI intent link
    upi_intent = f"upi://pay?pa={target_vpa}&pn=Merchant&am={amount:.2f}&cu=INR&tn={narration}"
    return redirect(upi_intent)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

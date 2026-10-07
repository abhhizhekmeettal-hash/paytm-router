from flask import Flask, request, render_template_string
import urllib.parse

app = Flask(__name__)

BUSINESS_UPI = "Q978110034@ybl"       # For amounts < 2000
PERSONAL_UPI = "8826705336@ptyes"     # For amounts >= 2000

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dynamic QR Payment</title>
        <style>
            body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: #f4f7f6; }
            .card { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); width: 100%; max-width: 350px; text-align: center; }
            input { width: 100%; padding: 12px; font-size: 18px; margin: 15px 0; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; text-align: center; }
            button { background: #00baf2; color: white; border: none; padding: 12px; width: 100%; font-size: 18px; border-radius: 6px; cursor: pointer; font-weight: bold; }
            button:hover { background: #0098c7; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Enter Bill Amount</h2>
            <form action="/generate" method="POST">
                <input type="number" step="0.01" name="amount" placeholder="₹ Amount" required autofocus>
                <button type="submit">Generate QR & Pay</button>
            </form>
        </div>
    </body>
    </html>
    """)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        amount = float(request.form['amount'])
    except ValueError:
        return "Invalid amount", 400

    # Determine routing based on ₹2,000 threshold
    if amount < 2000:
        target_vpa = BUSINESS_UPI
        account_type = "Paytm Business Account"
    else:
        target_vpa = PERSONAL_UPI
        account_type = "Personal Paytm Account"

    # Create the UPI payment string
    upi_intent = f"upi://pay?pa={target_vpa}&pn=Merchant&am={amount:.2f}&cu=INR&tn=Payment"
    
    # URL encode the intent string to generate a scannable QR code image via free API
    encoded_upi = urllib.parse.quote(upi_intent)
    qr_image_url = f"https://api.qrserver.com/v1/create-qr-code/?size=220x220&data={encoded_upi}"

    return render_template_string(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Scan or Pay</title>
        <style>
            body {{ font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; background: #f4f7f6; }}
            .card {{ background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); width: 100%; max-width: 350px; text-align: center; }}
            img {{ border: 2px solid #00baf2; border-radius: 8px; margin: 15px 0; padding: 5px; background: white; }}
            .btn-pay {{ background: #00baf2; color: white; text-decoration: none; display: block; padding: 12px; font-size: 16px; border-radius: 6px; font-weight: bold; margin-top: 15px; }}
            .btn-pay:hover {{ background: #0098c7; }}
            h3 {{ color: #333; margin: 5px 0; }}
            p {{ color: #666; font-size: 13px; margin: 5px 0; }}
            .upi-box {{ background: #f1f3f5; padding: 8px; border-radius: 4px; font-size: 13px; color: #333; margin-top: 10px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h3>Amount: ₹{amount:.2f}</h3>
            <p style="color: #00796b; font-weight: bold;">{account_type}</p>
            
            <!-- Dynamically Generated QR Code -->
            <img src="{qr_image_url}" alt="Dynamic QR Code">
            
            <p>Scan this QR code using any UPI app</p>
            
            <div class="upi-box">UPI ID: <b>{target_vpa}</b></div>

            <!-- Direct Click Link -->
            <a href="{upi_intent}" class="btn-pay">Or Click Here to Open App</a>
            
            <br>
            <a href="/" style="font-size: 12px; color: #666; text-decoration: underline;">← Enter a different amount</a>
        </div>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

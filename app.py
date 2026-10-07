
from flask import Flask, render_template_string, send_from_directory

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Select QR Code to Pay</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; background: #f4f7f6; padding: 15px; margin: 0; }
            .container { max-width: 400px; margin: auto; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
            .section { margin-bottom: 25px; border-bottom: 1px solid #eee; padding-bottom: 20px; }
            .section:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
            img { width: 200px; height: 200px; border-radius: 8px; border: 2px solid #00baf2; margin-top: 10px; }
            h2 { color: #333; font-size: 18px; margin-bottom: 15px; }
            p { font-size: 13px; color: #666; margin: 5px 0; }
            .tag-biz { background: #e0f7fa; color: #00796b; padding: 5px 10px; border-radius: 4px; font-weight: bold; display: inline-block; font-size: 14px; }
            .tag-per { background: #e8f5e9; color: #2e7d32; padding: 5px 10px; border-radius: 4px; font-weight: bold; display: inline-block; font-size: 14px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Select QR Based on Your Bill Amount</h2>
            
            <div class="section">
                <span class="tag-biz">For Less than ₹2,000</span>
                <p><b>Paytm Business Account</b></p>
                <img src="/qr/business" alt="Business QR Code">
                <p>Screenshot & use <b>Scan from Gallery</b> in your UPI app</p>
            </div>

            <div class="section">
                <span class="tag-per">For ₹2,000 & Above</span>
                <p><b>Personal Paytm Account</b></p>
                <img src="/qr/personal" alt="Personal QR Code">
                <p>Screenshot & use <b>Scan from Gallery</b> in your UPI app</p>
            </div>
        </div>
    </body>
    </html>
    """)

@app.route('/qr/business')
def business_qr():
    return send_from_directory('.', 'business_qr.png')

@app.route('/qr/personal')
def personal_qr():
    return send_from_directory('.', 'personal_qr.png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

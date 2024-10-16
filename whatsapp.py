from flask import Flask, request
import pywhatkit

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    msg_from = request.form.get('From')
    msg_body = request.form.get('Body')

    # Send a WhatsApp message using pywhatkit
    pywhatkit.sendwhatmsg("+919483102675", "Hello", 00, 12)

    return "Message received", 200

if __name__ == '__main__':
    app.run(debug=True)

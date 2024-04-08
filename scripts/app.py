from flask import Flask, request
from flask_cors import CORS
import read_emails as re
from simplegmail import Gmail

app = Flask(__name__)
CORS(app)  # Allow Cross-Origin Resource Sharing (CORS)

gmail = None  # Global variable to store Gmail object once authentication is done

@app.route('/authorize', methods=['POST'])
def authorize():
    global gmail
    if gmail is None:
        gmail = Gmail()
        return 'Authentication initiated'
    else:
        return 'Authentication process already started'

@app.route('/readMail', methods=['POST'])
def readMail():
    global gmail
    if gmail is None:
        return 'Please authenticate first'
    else:
        if request.method == 'POST':
            output = re.read_messages()
            return output            
        else:
            return "Bad Request"

if __name__ == '__main__':
    app.run(debug=True)

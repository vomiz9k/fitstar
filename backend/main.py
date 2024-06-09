from app import app, db

@app.route('/')
def hello_world():
    return '123123123'

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8080)
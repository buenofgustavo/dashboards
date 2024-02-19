from src.main.server.server import app 


if __name__ == '__main__':
    app.run_server(host='0.0.0.0',port=2600, debug=True)
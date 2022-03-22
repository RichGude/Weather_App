# Load libraries
import webbrowser
from threading import Timer

from app import app

# Define function for opening a browser that the preferred Flask host
def open_browser():
    webbrowser.open_new('http://127.0.0.1:2000/')

if __name__ == '__main__':
    # Automatically open a web browser window when the app is run
    # Timer(1, open_browser).start()
    app.run(debug=True, host='127.0.0.1', port=2000)
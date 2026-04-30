# main.py — Entry Point

from auth import AuthManager
from login import LoginPage

if __name__ == "__main__":
    auth = AuthManager()
    app  = LoginPage(auth)
    app.run()

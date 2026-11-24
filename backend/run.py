from dotenv import load_dotenv

from app import create_app

load_dotenv()  # reads .env if it exists; real environment variables win
app = create_app()

if __name__ == "__main__":
    app.run(port=5000, debug=False)

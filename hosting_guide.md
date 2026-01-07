# Hosting Guide - AlgoViz

The application is currently running locally. To make it publicly accessible, you can follow these steps:

## Option 1: Render (Recommended)
1.  **Create a GitHub Repository**: Push your code to a new repo on GitHub.
2.  **Connect to Render**: Sign up at [render.com](https://render.com) and create a new "Web Service".
3.  **Configure**:
    - **Runtime**: Python 3
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `gunicorn app:app` (Note: You may need to add `gunicorn` to your requirements.txt)
    - **Environment Variables**: Set `PORT` to `5002` (or Render's default).

## Option 2: Railway
1.  Connect your GitHub repo to Railway.
2.  It will automatically detect the Python environment.
3.  Set the start command to `python app.py`.

## Option 3: Local Tunnel (Quick Demo)
If you just want to show someone the site temporarily while your computer is on:
1.  Install `localtunnel` via npm: `npm install -g localtunnel`
2.  Run the tunnel: `lt --port 5002`
3.  Share the provided URL.

## Option 4: Firebase (Advanced)
If you want to use Firebase, please refer to `FIREBASE_GUIDE.md` in this directory. Note that this requires the Blaze (paid) plan for Python support.

> [!NOTE]
> For production hosting, it is recommended to replace `app.run(debug=True)` with a production server like `gunicorn`.

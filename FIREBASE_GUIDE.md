# Publishing AlgoViz with Firebase Hosting (Flask)

Since AlgoViz uses a Python (Flask) backend, simple static hosting is not enough. You need to use **Firebase Hosting** combined with **Cloud Functions for Firebase (2nd Gen)** or **Cloud Run** to serve the dynamic backend.

**Prerequisites:**
1.  **Node.js & npm**: You must install Node.js to interact with Firebase. [Download here](https://nodejs.org/).
2.  **Firebase Project**: Create a project at [console.firebase.google.com](https://console.firebase.google.com).
3.  **Billing (Blaze Plan)**: Python Cloud Functions require the "Blaze" (Pay as you go) plan.

## Step 1: Install Firebase CLI
Open your terminal (Command Prompt or PowerShell) and run:
```bash
npm install -g firebase-tools
```

## Step 2: Login
```bash
firebase login
```
Follow the browser prompt to authenticate.

## Step 3: Initialize Project
1.  Run the experimental web frameworks setup (easiest for Flask):
    ```bash
    firebase experiments:enable webframeworks
    firebase init hosting
    ```
2.  Select your Firebase project.
3.  It should detect "Web framework: Flask".
4.  Source directory: `.` (Current directory)
5.  Region: `us-central1` (or your preference).

## Step 4: Deploy
```bash
firebase deploy
```

---
**Alternative Manual Setup (If experimental fails):**
If the above doesn't work, you can structure it manually using Cloud Functions Gen 2.

1.  `firebase init functions` -> Select Python.
2.  Edit `functions/main.py` to wrap your Flask app:
    ```python
    from firebase_functions import https_fn
    from firebase_admin import initialize_app
    from app import app  # Import your Flask app

    initialize_app()
    
    @https_fn.on_request()
    def algoviz(req: https_fn.Request) -> https_fn.Response:
        with app.request_context(req.environ):
            return app.full_dispatch_request()
    ```
3.  `firebase init hosting` -> Configure rewrites to function `algoviz`.

## Easier Alternatives (No Billing Required)
Since you already have `vercel.json` configured, deploying to **Vercel** is free and often supports Flask out of the box.
1.  `npm i -g vercel`
2.  `vercel`

Or use **Render.com** (Connect GitHub repo -> Select Python -> Build: `pip install -r requirements.txt` -> Start: `gunicorn app:app`).

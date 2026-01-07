# Deploying AlgoViz to Render.com

Render is the easiest way to host Python applications for free.

## Step 1: Create a GitHub Repository
1.  Log in to [GitHub](https://github.com).
2.  Click the **+** icon in the top right -> **New repository**.
3.  Name it `algoviz` (or similar).
4.  Make it **Public** (easier) or Private.
5.  **Do not** add a README, gitignore, or license (we have them already).
6.  Click **Create repository**.
7.  Copy the URL (e.g., `https://github.com/YOUR_USERNAME/algoviz.git`).

## Step 2: Push Your Code
Open your terminal in VS Code (Ctrl+`) and run these commands:

```bash
# Initialize Git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial deploy"

# Link to GitHub (Replace URL with yours!)
git remote add origin https://github.com/YOUR_USERNAME/algoviz.git

# Rename branch to main
git branch -M main

# Push code
git push -u origin main
```

## Step 3: Configure Render
1.  Go to [dashboard.render.com](https://dashboard.render.com/).
2.  Click **New +** -> **Web Service**.
3.  Select **Build and deploy from a Git repository**.
4.  Connect your GitHub account and select the `algoviz` repo.
5.  **Settings**:
    *   **Name**: `algoviz-app` (or unique name)
    *   **Region**: Closest to you (e.g., Singapore, Frankfurt, US).
    *   **Branch**: `main`
    *   **Root Directory**: Leave blank (since `app.py` is in the root of the repo).
    *   **Runtime**: `Python 3`
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `gunicorn app:app`
6.  Select **Free** plan.
7.  Click **Create Web Service**.

## Step 4: Done!
Render will build your app. It might take a few minutes.
Once done, you will get a URL like `https://algoviz-app.onrender.com`.

# Deployment Guide - GirlChat to Streamlit Cloud

## Step 1: Create GitHub Repository

### 1.1 Go to GitHub
- Visit [github.com](https://github.com)
- Sign in or create an account

### 1.2 Create New Repository
- Click the **"+"** icon in the top right
- Select **"New repository"**
- Repository name: `girlchat`
- Description: `AI Girlfriend Chatbot with Vesper`
- Make it **Public**
- **Don't** check "Add a README file"
- Click **"Create repository"**

### 1.3 Upload Files
You have two options:

#### Option A: Upload via Web Interface
1. In your new repository, click **"uploading an existing file"**
2. Drag and drop these files:
   - `girlchat_streamlit.py`
   - `requirements.txt`
   - `README.md`
   - `.gitignore`
   - `.streamlit/config.toml`
3. Add commit message: "Initial commit"
4. Click **"Commit changes"**

#### Option B: Use Git Commands (Recommended)
```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit"

# Add remote repository (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/girlchat.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 2: Deploy to Streamlit Cloud

### 2.1 Go to Streamlit Cloud
- Visit [share.streamlit.io](https://share.streamlit.io)
- Sign in with your GitHub account

### 2.2 Deploy Your App
1. Click **"New app"**
2. **Repository**: Select `YOUR_USERNAME/girlchat`
3. **Branch**: `main`
4. **Main file path**: `girlchat_streamlit.py`
5. Click **"Deploy!"**

### 2.3 Wait for Deployment
- Streamlit will build and deploy your app
- This usually takes 2-3 minutes
- You'll see a progress bar

### 2.4 Get Your Public URL
- Once deployed, you'll get a URL like:
  `https://girlchat-YOUR_USERNAME.streamlit.app`
- This URL is public and anyone can access it!

## Step 3: Test Your Deployment

### 3.1 Open Your App
- Click the provided URL
- The app should load with the dark theme

### 3.2 Test the Chat
1. Enter your OpenAI API key in the sidebar
2. Send a test message
3. Verify Vesper responds correctly

## Step 4: Share with Others

### 4.1 Share the URL
- Send the Streamlit URL to friends
- They can access it from any device

### 4.2 Instructions for Users
Tell them to:
1. Open the URL
2. Enter their own OpenAI API key
3. Start chatting with Vesper

## Troubleshooting

### Common Issues:

**App won't deploy:**
- Check that all files are uploaded to GitHub
- Verify `requirements.txt` is correct
- Check the main file path in Streamlit Cloud

**API errors:**
- Users need their own OpenAI API key
- API key should start with `sk-`

**Styling issues:**
- Clear browser cache
- Check that custom CSS is loaded

## Security Notes

- ✅ API keys are stored locally in user sessions
- ✅ No sensitive data is stored permanently
- ✅ Each user provides their own API key
- ✅ App is safe for public deployment

## Support

If you encounter issues:
1. Check the Streamlit Cloud logs
2. Verify all files are in the repository
3. Test locally first with `streamlit run girlchat_streamlit.py`

Your app is now live and ready to share! 🎉 
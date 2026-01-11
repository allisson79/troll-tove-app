# ⚡ Quick Deploy - Render.com

The fastest way to get Troll-Tove online! Takes ~5 minutes.

## Step 1: Create Account
Go to [render.com](https://render.com) and sign up with your GitHub account (it's free!)

## Step 2: Create New Web Service
1. Click the **"New +"** button (top right)
2. Select **"Web Service"**
3. Connect your GitHub account if not already connected
4. Find and select the **troll-tove-app** repository

## Step 3: Configure (Most fields auto-fill from render.yaml!)
- **Name**: `troll-tove-app` (or choose your own)
- **Region**: Select closest to your location
- **Branch**: `main` (or your working branch)
- **Runtime**: Python 3 ✅
- **Build Command**: Already set! ✅
- **Start Command**: Already set! ✅

## Step 4: Environment Variables
In the "Environment" section, add:

**SECRET_KEY**
- Click **"Generate"** button to auto-create a secure key
- OR generate manually: `python -c "import secrets; print(secrets.token_hex(32))"`

**FLASK_DEBUG** (optional, defaults to false)
- Set to: `false`

## Step 5: Deploy! 🚀
1. Click **"Create Web Service"**
2. Watch the build logs (it takes 1-2 minutes)
3. When you see "Your service is live 🎉" - you're done!

## Step 6: Visit Your App
Your app will be at: `https://troll-tove-app-xxxx.onrender.com`
(The URL will be shown in the dashboard)

---

## 🎯 Quick Health Check
Test your deployment:
```bash
curl https://your-app-name.onrender.com/health
```

Should return:
```json
{
  "status": "healthy",
  "fotball_predictions": 40,
  "random_predictions": 45,
  "cache_size": 0
}
```

---

## 💡 Pro Tips

### Custom Domain
1. Go to your service **Settings**
2. Click **"Custom Domain"**
3. Add your domain (e.g., `troll-tove.com`)
4. Follow DNS setup instructions

### Auto-Deploy
By default, Render automatically deploys when you push to your GitHub branch. You can:
- Change this in **Settings** → **Auto-Deploy**
- Manually deploy anytime from the **Manual Deploy** section

### Free Tier Notes
- ✅ 750 hours/month free (enough for one app running 24/7)
- ⚠️ App sleeps after 15 minutes of inactivity
- ⏱️ First request after sleep takes ~30 seconds (cold start)
- 💰 Upgrade to paid plan ($7/month) to prevent sleeping

### Monitoring
- View logs in real-time from the **Logs** tab
- Check `/health` endpoint for status monitoring
- Set up alerts in **Notifications** settings

---

## 🔧 Troubleshooting

**Build fails?**
- Check the build logs
- Verify `requirements.txt` is present
- Ensure Python version is compatible (3.9+)

**App won't start?**
- Verify `SECRET_KEY` environment variable is set
- Check startup logs for errors
- Make sure all prediction files exist in repo

**Blank page?**
- Check browser console for errors
- Verify static files are being served
- Check app logs for 404 errors

**Need help?**
- Check full guide: [DEPLOYMENT.md](DEPLOYMENT.md)
- Visit Render docs: [render.com/docs](https://render.com/docs)
- Check app logs in Render dashboard

---

## 🎉 Success!

Når appen din er live, kan folk besøke den og få spådommer fra Troll-Tove! Share the URL with friends and have fun!

Test alle endpoints:
- `https://your-app.onrender.com/` - Main page
- `https://your-app.onrender.com/glimtmodus` - Glimt predictions
- `https://your-app.onrender.com/darkmodus` - Dark predictions
- `https://your-app.onrender.com/health` - Health check

**Gratulerer! Troll-Tove er nå online! 🔮✨**

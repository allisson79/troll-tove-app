# 🚀 Deployment Guide - Troll-Tove App

This guide provides step-by-step instructions for deploying the Troll-Tove app to various cloud platforms.

## Prerequisites

Before deploying, make sure you have:
- A GitHub account with this repository forked/cloned
- Git installed locally
- All code committed and pushed to your GitHub repository

## Table of Contents

1. [Render.com (Recommended)](#rendercom-recommended)
2. [Heroku](#heroku)
3. [Railway.app](#railwayapp)
4. [Vercel](#vercel)
5. [Docker Deployment](#docker-deployment)
6. [Environment Variables](#environment-variables)

---

## Render.com (Recommended)

**Best for**: Simple deployment with free tier, automatic deployments

### Steps:

1. **Sign up** at [render.com](https://render.com) (use your GitHub account)

2. **Create a New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `troll-tove-app` repository

3. **Configure the service**:
   - **Name**: `troll-tove-app` (or your preferred name)
   - **Region**: Choose closest to your users
   - **Branch**: `main` (or your default branch)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`

4. **Set Environment Variables**:
   - Click "Environment" tab
   - Add the following:
     - `SECRET_KEY`: Click "Generate" or use: `python -c "import secrets; print(secrets.token_hex(32))"`
     - `FLASK_DEBUG`: `false`

5. **Deploy**:
   - Click "Create Web Service"
   - Render will automatically deploy your app
   - Access your app at: `https://troll-tove-app.onrender.com` (or your chosen name)

### Using render.yaml (Alternative):

The repository includes a `render.yaml` file. You can also:
1. Go to [render.com](https://render.com)
2. Click "New +" → "Blueprint"
3. Connect your repository
4. Render will automatically detect and use the `render.yaml` configuration

---

## Heroku

**Best for**: Established platform, lots of addons, easy scaling

### Steps:

1. **Sign up** at [heroku.com](https://heroku.com)

2. **Install Heroku CLI**:
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku

   # Ubuntu/Debian
   curl https://cli-assets.heroku.com/install.sh | sh

   # Windows
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

3. **Login to Heroku**:
   ```bash
   heroku login
   ```

4. **Create a new Heroku app**:
   ```bash
   cd /path/to/troll-tove-app
   heroku create troll-tove-app
   # Or just: heroku create (generates random name)
   ```

5. **Set Environment Variables**:
   ```bash
   # Generate a secret key
   heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
   heroku config:set FLASK_DEBUG=false
   ```

6. **Deploy**:
   ```bash
   git push heroku main
   # If your branch is not 'main':
   # git push heroku your-branch-name:main
   ```

7. **Open your app**:
   ```bash
   heroku open
   ```

### Using Heroku Dashboard (Alternative):

1. Go to [dashboard.heroku.com](https://dashboard.heroku.com)
2. Click "New" → "Create new app"
3. Choose app name and region
4. Go to "Deploy" tab
5. Connect to GitHub and select your repository
6. Enable "Automatic Deploys" if desired
7. Click "Deploy Branch"

---

## Railway.app

**Best for**: Modern platform, great developer experience, generous free tier

### Steps:

1. **Sign up** at [railway.app](https://railway.app) (use GitHub)

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `troll-tove-app` repository

3. **Railway will auto-detect**:
   - Python runtime
   - Will automatically use `railway.json` if present
   - Or configure manually:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`

4. **Set Environment Variables**:
   - Click on your service
   - Go to "Variables" tab
   - Add:
     - `SECRET_KEY`: Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`
     - `FLASK_DEBUG`: `false`
     - `PORT`: Railway will set this automatically

5. **Deploy**:
   - Railway automatically deploys on commit
   - Go to "Settings" tab to get your public URL
   - Click "Generate Domain" to get a public URL

---

## Vercel

**Best for**: Frontend-focused projects, edge deployment, fast CDN

**Note**: Vercel is optimized for serverless functions. For a Flask app with state (like our IP cache), Render or Railway might be better choices.

### Steps:

1. **Sign up** at [vercel.com](https://vercel.com) (use GitHub)

2. **Import Project**:
   - Click "Add New" → "Project"
   - Import your GitHub repository

3. **Configure Project**:
   - **Framework Preset**: Other
   - **Build Command**: Leave empty
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements.txt`

4. **Set Environment Variables**:
   - Add in project settings:
     - `SECRET_KEY`: Generate securely
     - `FLASK_DEBUG`: `false`

5. **Deploy**:
   - Click "Deploy"
   - Vercel will use the `vercel.json` configuration
   - Access your app at the provided URL

**Important Notes for Vercel**:
- The IP-based cache will not persist across serverless invocations
- Consider using a Redis cache or similar for production
- Each request may cold-start

---

## Docker Deployment

**Best for**: Containerized deployments, any cloud provider that supports Docker, self-hosting

### Local Docker Testing:

1. **Build the Docker image**:
   ```bash
   docker build -t troll-tove-app .
   ```

2. **Run the container**:
   ```bash
   docker run -d \
     -p 8000:8000 \
     -e SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))") \
     -e FLASK_DEBUG=false \
     --name troll-tove \
     troll-tove-app
   ```

3. **Test the app**:
   ```bash
   curl http://localhost:8000/health
   ```

4. **View logs**:
   ```bash
   docker logs troll-tove
   ```

5. **Stop the container**:
   ```bash
   docker stop troll-tove
   docker rm troll-tove
   ```

### Deploy to Cloud Providers:

#### Google Cloud Run:

```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/YOUR-PROJECT-ID/troll-tove-app

# Deploy to Cloud Run
gcloud run deploy troll-tove-app \
  --image gcr.io/YOUR-PROJECT-ID/troll-tove-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars SECRET_KEY=your-secret-key,FLASK_DEBUG=false
```

#### AWS (Elastic Container Service):

1. Push image to Amazon ECR
2. Create ECS task definition using the image
3. Create ECS service
4. Configure environment variables in task definition

#### DigitalOcean App Platform:

1. Connect your GitHub repository
2. Select "Dockerfile" as build method
3. Set environment variables in the dashboard
4. Deploy

#### Azure Container Instances:

```bash
az container create \
  --resource-group myResourceGroup \
  --name troll-tove-app \
  --image YOUR-REGISTRY/troll-tove-app \
  --dns-name-label troll-tove \
  --ports 8000 \
  --environment-variables SECRET_KEY=your-secret-key FLASK_DEBUG=false
```

---

## Environment Variables

All platforms require these environment variables:

### Required:

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key for sessions | Generate: `python -c "import secrets; print(secrets.token_hex(32))"` |
| `FLASK_DEBUG` | Debug mode (should be false in production) | `false` |

### Optional:

| Variable | Description | Example |
|----------|-------------|---------|
| `API_FOOTBALL_KEY` | For future football API integration | Your API key |
| `PORT` | Port number (usually set by platform) | `8000` |

---

## Post-Deployment Checklist

After deploying to any platform:

- [ ] Visit your app URL to verify it loads
- [ ] Test the main form submission
- [ ] Test `/glimtmodus` endpoint
- [ ] Test `/darkmodus` endpoint
- [ ] Check `/health` endpoint returns JSON
- [ ] Verify SECRET_KEY is set (check logs for warnings)
- [ ] Monitor logs for any errors
- [ ] Test from different IPs to verify caching works
- [ ] Set up custom domain (optional)
- [ ] Configure monitoring/alerting (optional)

---

## Troubleshooting

### App won't start:
- Check environment variables are set correctly
- Review deployment logs for errors
- Verify `requirements.txt` has all dependencies
- Ensure `SECRET_KEY` is set

### App runs but pages don't load:
- Check that prediction files exist (`spaadommer_fotball.txt`, etc.)
- Review application logs
- Test `/health` endpoint

### "Missing SECRET_KEY" error:
- Generate a secret key: `python -c "import secrets; print(secrets.token_hex(32))"`
- Set it in your platform's environment variables

### Cache not working:
- On serverless platforms (Vercel), in-memory cache doesn't persist
- Consider using Redis or similar external cache service

---

## Updating Your Deployed App

### Automatic Deployments (Recommended):
Most platforms support automatic deployments from GitHub:
1. Push changes to your repository
2. Platform automatically detects and deploys

### Manual Deployments:
- **Render**: Click "Manual Deploy" → "Deploy latest commit"
- **Heroku**: `git push heroku main`
- **Railway**: Push to GitHub or click "Deploy" in dashboard
- **Vercel**: Push to GitHub or use `vercel --prod` CLI

---

## Cost Considerations

| Platform | Free Tier | Notes |
|----------|-----------|-------|
| **Render** | 750 hours/month | App sleeps after 15 min of inactivity |
| **Heroku** | 1000 hours/month | Requires credit card, app sleeps after 30 min |
| **Railway** | $5 credit/month | No sleep, but credit-based |
| **Vercel** | Generous limits | Best for frontend/serverless |

---

## Recommended Platform

For Troll-Tove app, we recommend **Render.com** because:
- ✅ Simple setup with `render.yaml`
- ✅ Free tier suitable for hobby projects
- ✅ Automatic deployments from GitHub
- ✅ Good for stateful Python apps
- ✅ Built-in health checks
- ✅ Easy environment variable management

---

## Need Help?

- Check platform-specific documentation
- Review application logs in your platform dashboard
- Test locally first: `gunicorn app:app`
- Visit platform community forums
- Check GitHub repository issues

---

**Happy Deploying! 🚀**

Troll-Tove ønsker deg lykke til med publiseringen! 🔮

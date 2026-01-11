# 📋 Post-Deployment Checklist

Use this checklist after deploying your Troll-Tove app to ensure everything works correctly.

## Basic Functionality Tests

- [ ] **App loads**: Visit your app URL and verify the homepage displays
- [ ] **Main form works**: 
  - [ ] Enter a name and question
  - [ ] Submit the form
  - [ ] Verify you get a prediction response
  - [ ] Check that the prediction makes sense (not an error message)

## Endpoint Tests

- [ ] **Homepage** (`/`): Loads the form correctly
- [ ] **Glimt mode** (`/glimtmodus`): Returns a football-related prediction
- [ ] **Dark mode** (`/darkmodus`): Returns a darker prediction
- [ ] **Health check** (`/health`): Returns JSON with status "healthy"

### Testing Commands
```bash
# Replace YOUR-APP-URL with your actual URL
APP_URL="https://your-app.onrender.com"

# Test health endpoint
curl $APP_URL/health

# Test Glimt mode
curl $APP_URL/glimtmodus

# Test Dark mode  
curl $APP_URL/darkmodus
```

## Security & Configuration

- [ ] **SECRET_KEY is set**: Check logs for "Using randomly generated SECRET_KEY" warning
  - If you see this warning, you need to set SECRET_KEY in environment variables
- [ ] **FLASK_DEBUG is false**: Verify debug mode is disabled in production
  - Check environment variables in your platform dashboard
- [ ] **No sensitive data in logs**: Review logs to ensure no secrets are being printed
- [ ] **HTTPS enabled**: Verify your app URL uses `https://` (most platforms do this automatically)

## Performance & Reliability

- [ ] **Health check endpoint responds quickly** (< 1 second)
- [ ] **Static files load** (CSS, images, JavaScript)
  - Check that the Troll-Tove image displays
  - Check that styling is applied correctly
- [ ] **App handles errors gracefully**:
  - [ ] Try a 404 page (e.g., `/nonexistent-page`) - should show custom 404 page
  - [ ] Submit form with empty values - should handle gracefully

## Caching Tests

- [ ] **IP-based caching works**:
  - [ ] Submit a question and note the prediction
  - [ ] Submit another question from the same location
  - [ ] Verify you get the same prediction (cache working)
  - [ ] Wait 1 hour OR test from different network/IP
  - [ ] Verify you get a different prediction (cache expired or new IP)

## Different Device Tests

Test on multiple devices/browsers if possible:
- [ ] Desktop browser (Chrome/Firefox/Safari)
- [ ] Mobile browser (responsive design)
- [ ] Different network (to test IP caching)

## Monitoring Setup

- [ ] **Check platform dashboard**: Familiarize yourself with:
  - Logs location
  - Metrics/monitoring
  - Environment variables
  - Deployment history
- [ ] **Set up notifications** (optional):
  - Health check alerts
  - Error notifications
  - Deployment notifications

## Optional Enhancements

- [ ] **Custom domain**: Set up your own domain name
- [ ] **Monitoring service**: Set up external monitoring (e.g., UptimeRobot, Pingdom)
- [ ] **Analytics**: Add analytics if desired (Google Analytics, Plausible, etc.)
- [ ] **CDN**: Consider CDN for static files if you expect high traffic

## Platform-Specific Checks

### Render.com
- [ ] Auto-deploy enabled (if desired)
- [ ] Health check path set to `/health`
- [ ] Logs are accessible and readable

### Heroku
- [ ] Dyno is running (not sleeping)
- [ ] Environment variables set in dashboard
- [ ] Logs accessible via `heroku logs --tail`

### Railway
- [ ] Service is deployed and running
- [ ] Domain generated or custom domain set
- [ ] Environment variables configured

### Vercel
- [ ] Deployment successful
- [ ] Environment variables set for production
- [ ] Note: Serverless limitations may affect caching

## Documentation

- [ ] **Update repo README** with live URL (optional)
- [ ] **Share with users**: Provide them with:
  - Main URL
  - Available endpoints
  - Any special features or Easter eggs

## Troubleshooting Performed

If you encountered any issues during deployment, document them here:

**Issue 1**: 
- Problem: 
- Solution: 

**Issue 2**:
- Problem:
- Solution:

---

## ✅ Deployment Complete!

Once all items are checked:
- 🎉 Your Troll-Tove app is successfully deployed!
- 🔮 Share the URL with friends and family
- 📊 Monitor usage and performance
- 🛠️ Keep dependencies updated

**Live URL**: `_________________________________`

**Deployed on**: `_________________________________`

**Deployment date**: `_________________________________`

---

## Need Help?

- Check [DEPLOYMENT.md](DEPLOYMENT.md) for detailed guides
- Review platform-specific documentation
- Check application logs for errors
- Visit [QUICK_DEPLOY.md](QUICK_DEPLOY.md) for Render.com quick start

**Lykke til! Troll-Tove ønsker deg god tur på internett! 🔮✨**

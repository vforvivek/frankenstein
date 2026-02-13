# 🎮 Frankenstein Game - Web Deployment

Valentine horror game with Mario-style platformer mechanics, deployable to the web!

## 🚀 Deployment Instructions

### 1. Repository Structure

Your repository should look like this:

```
your-repo/
├── .github/
│   └── workflows/
│       └── deploy-game.yml
├── main.py (the modified game file)
├── assets/
│   └── sfx/
│       ├── mario_theme.wav
│       ├── jump.wav
│       ├── coin.wav
│       ├── pipe.wav
│       ├── stage_clear.wav
│       ├── powerup.wav
│       ├── kiss.wav
│       └── lightning.wav
├── README.md
└── requirements.txt
```

### 2. Setup Steps

1. **Create GitHub repository** (public)
2. **Create the workflow directory:**
   ```bash
   mkdir -p .github/workflows
   ```
3. **Move the workflow file:**
   ```bash
   mv deploy-game.yml .github/workflows/
   ```
4. **Add your audio files** to `assets/sfx/` directory
5. **Commit and push:**
   ```bash
   git init
   git add .
   git commit -m "Deploy Frankenstein game to web"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

### 3. Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under "Build and deployment":
   - Source: **Deploy from a branch**
   - Branch: Select **gh-pages** (created automatically by the workflow)
   - Folder: **/ (root)**
4. Click **Save**

### 4. Access Your Game

After deployment (2-5 minutes), your game will be available at:
```
https://YOUR_USERNAME.github.io/YOUR_REPO/
```

## 🔐 GitHub Secrets Required

**NONE!** GitHub automatically provides `GITHUB_TOKEN` for deployment.

## 💰 Cost

**$0/month** - Completely free hosting on GitHub Pages!

## 🎮 Game Controls

- **Arrow Keys** or **WASD**: Move left/right
- **SPACE** or **UP**: Jump
- **Mouse**: Click on doors/buttons/assembly parts

## 📝 What Was Modified

The original `frankenstein_game.py` was converted to `main.py` with these changes:

1. ✅ Added `import asyncio`
2. ✅ Made all scene functions async (`async def`)
3. ✅ Added `await asyncio.sleep(0)` in all game loops
4. ✅ Made `main()` function async with await calls
5. ✅ Changed entry point to `asyncio.run(main())`

## 🔧 Troubleshooting

### Build fails with "main.py not found"
- Ensure `main.py` is at the root of your repository
- Check the filename is exactly `main.py` (case-sensitive)

### Game doesn't load in browser
- Check browser console (F12) for errors
- Ensure all audio files are in `assets/sfx/` directory
- Some browsers may require user interaction before playing audio

### GitHub Actions fails
- Check the Actions tab for detailed error logs
- Ensure your repository is public
- Verify Python 3.11 is being used

## 📦 Files Included

- `main.py` - Web-ready game code with async support
- `deploy-game.yml` - GitHub Actions workflow
- `requirements.txt` - Python dependencies
- `README.md` - This file

## 🎉 Next Steps

1. Download `main.py` and `deploy-game.yml`
2. Create your GitHub repo with the structure above
3. Add your audio files
4. Push and watch it deploy!

Your game will be playable by anyone with a web browser - no installation needed!

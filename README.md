# Dark Video Edit

AI reel studio for gamers: finds every kill in your gameplay, lets you keep or remove shots, adds effects and captions, and exports a 9:16 reel. Can also download **only a chosen part** of a YouTube video (with optional crop) instead of the whole video.

## What works now (Phase 1)
- Auto kill detection (red skull badge, top centre of the screen) across many clips
- Shot list with thumbnails: tap to keep or remove; total kills and length update live
- 9:16 export with blurred background, kill shake + flash + boom sound, KILL counter, funny captions (all switchable)
- YouTube: paste link, watch in app (full screen button or F key), choose Start/End (slider, typed time or Mark In/Out), crop 9:16 / 1:1 / 4:5 / 16:9, download only that part
- Browser-login option (cookies) for age-restricted videos
- Auto title and description (templates)

## Next phases
1. YouTube upload, 2. Instagram upload (needs a Business/Creator account and Meta app), 3. Claude-written captions/titles, 4. Highlight score and "best 60s" button, 5. Phone version.

## Run from source (Windows / Mac / Linux)
```
pip install -r requirements.txt
python app/main.py
```
FFmpeg is used from your PATH, or from the bundled `imageio-ffmpeg` binary.

## Headless test (no window)
```
python cli.py scan clip.mp4
python cli.py reel out.mp4 clip1.mp4 clip2.mp4
python cli.py crop in.mp4 out.mp4 9:16
```

## Build the Windows app (.exe)
Push to GitHub. The workflow in `.github/workflows/build.yml` builds it. Open the **Actions** tab, pick the run, download the **DarkVideoEdit-windows** artifact.

## Put it on GitHub
```
git init && git add . && git commit -m "Dark Video Edit"
git branch -M main
git remote add origin https://github.com/YOUR_NAME/dark-video-edit.git
git push -u origin main
```

## Notes
- Kill detection is tuned for the game UI in the sample clips. Other games need their own region/colour (see `detect_kills` in `app/engine.py`).
- Download only your own videos/streams, or ones you have permission to use. Use a secondary Google account for cookie login.
- Output goes to `~/Videos/DarkVideoEdit`.

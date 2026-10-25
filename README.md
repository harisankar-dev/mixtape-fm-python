# mixtape.fm — Python / Streamlit edition

A Python/Streamlit remake of the mixtape.fm digital mixtape concept. This repo is separate from the original Next.js application.

## Features
- Create a mixtape with a title, sender, recipient, note and optional cover image URL
- Add up to 20 YouTube tracks
- Choose among CD player, iPod classic, scrapbook and webcore looks
- Preview the player and play a selected track through YouTube
- Generate shareable URLs by compressing the mixtape data into the URL itself
- No Supabase or database required

## Run locally

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Open https://share.streamlit.io/ and sign in with GitHub.
2. Choose **Create app**.
3. Select repository `harisankar-dev/mixtape-fm-python`, branch `main`, and main file `app.py`.
4. Click **Deploy**.

Official guide: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

## Notes
- No database is used; the mixtape is embedded in the share URL. Very large mixtapes can produce very long URLs.
- Anyone with the complete URL can view the mixtape. Avoid putting private information in the dedication.
- Playback uses YouTube's embedded player and is subject to YouTube restrictions and availability.
- This is a Streamlit remake of the core features, not an exact recreation of every original Next.js animation.

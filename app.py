import base64
import html
import json
import zlib
from urllib.parse import quote

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="mixtape.fm", page_icon="♫", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;700&family=Playfair+Display:ital,wght@0,500;1,500&display=swap');
:root { --paper:#f3eee4; --ink:#201e1a; --muted:#625d54; --line:#d7cfc1; --accent:#c6533b; --panel:#faf7f0; }
.stApp { background:var(--paper); color:var(--ink); }
.block-container { max-width:1180px; padding-top:1.7rem; padding-bottom:3.5rem; }
[data-testid="stHeader"] { background:transparent; }
.brand { display:flex; align-items:center; justify-content:space-between; gap:1rem; border-bottom:1px solid var(--ink); padding:0 0 15px; }
.brand b { font:700 24px 'DM Sans',sans-serif; letter-spacing:-1.2px; color:var(--ink); }
.brand .dot { color:var(--accent); }
.brand .tag { font:10px 'DM Mono',monospace; text-transform:uppercase; letter-spacing:1.5px; color:var(--muted); text-align:right; }
.hero { padding:26px 0 28px; }
.eyebrow { font:11px 'DM Mono',monospace; letter-spacing:2px; color:var(--accent); text-transform:uppercase; }
.hero h1 { margin:10px 0 14px; font:500 clamp(42px,6.5vw,76px)/1.02 'Playfair Display',serif; letter-spacing:-1.8px; color:var(--ink); overflow-wrap:anywhere; }
.hero h1 em { color:var(--accent); font-weight:500; }
.hero p { max-width:680px; color:var(--muted); font:16px/1.7 'DM Sans',sans-serif; }
.panel { background:var(--panel); border:1px solid var(--line); border-radius:5px; padding:20px; margin-bottom:18px; }
.section-title { font:11px 'DM Mono',monospace; letter-spacing:1.7px; color:var(--accent); text-transform:uppercase; border-bottom:1px solid var(--line); padding-bottom:12px; margin-bottom:16px; }
.player-card { background:#26231f; color:#f4eddf; border:1px solid #454039; border-radius:8px; text-align:center; padding:27px 20px 25px; margin:8px 0 14px; }
.player-card h2 { font:500 clamp(27px,4vw,43px)/1.12 'Playfair Display',serif; color:#f4eddf !important; margin:14px auto 10px; overflow-wrap:anywhere; }
.player-card .kicker { font:10px 'DM Mono',monospace; letter-spacing:2px; color:#e68a70; text-transform:uppercase; }
.player-card .to-line { font:11px 'DM Mono',monospace; color:#e0d6c7; letter-spacing:1px; text-transform:uppercase; overflow-wrap:anywhere; }
.player-card .cover { width:152px; height:152px; margin:23px auto 20px; object-fit:cover; border-radius:4px; display:block; }
.player-card .disc { width:150px; height:150px; margin:23px auto 20px; border-radius:50%; background:repeating-radial-gradient(circle at center,#46423b 0 5px,#211f1c 6px 10px); border:1px solid #625b50; display:flex; align-items:center; justify-content:center; }
.player-card .disc-label { width:54px; height:54px; border-radius:50%; background:#c6533b; color:#fff5e9; display:flex; align-items:center; justify-content:center; font:9px/1.3 'DM Mono',monospace; padding:4px; overflow-wrap:anywhere; }
.player-card .note { color:#e6ddcf; font:italic 15px/1.6 'Playfair Display',serif; white-space:pre-wrap; overflow-wrap:anywhere; margin:0 auto 3px; max-width:650px; }
.player-card.ipod { background:#d5d8d4; color:#222720; border:7px solid #e8e9e5; box-shadow:inset 0 0 0 1px #89918a; }
.player-card.ipod h2 { color:#222720 !important; font-family:'DM Sans',sans-serif; }
.player-card.ipod .kicker { color:#4a554b; }.player-card.ipod .to-line,.player-card.ipod .note { color:#343b34; }
.player-card.ipod .disc { background:repeating-radial-gradient(circle,#7d827c 0 5px,#454a45 6px 10px); }
.player-card.scrapbook { background:#e8d7b9; color:#34291e; border:2px dashed #9e7f58; transform:rotate(-.15deg); }
.player-card.scrapbook h2 { color:#34291e !important; }.player-card.scrapbook .kicker { color:#a43f2c; }
.player-card.scrapbook .to-line,.player-card.scrapbook .note { color:#5d4831; }
.player-card.webcore { background:#17172c; border:2px solid #ff67c4; box-shadow:5px 5px 0 #77e6d0; }
.player-card.webcore h2 { color:#ff9edc !important; text-shadow:2px 2px #6a55cb; }.player-card.webcore .kicker { color:#77e6d0; }
.player-card.webcore .to-line,.player-card.webcore .note { color:#f6dafa; }
.player-controls { background:#f8f4ec; border:1px solid var(--line); border-radius:5px; padding:13px; margin:12px 0 18px; }
.stMarkdown, .stMarkdown p, .stCaption, [data-testid="stCaptionContainer"] { color:var(--ink); }
label, .stTextInput label, .stTextArea label, .stSelectbox label, .stNumberInput label, .stSlider label, .stRadio label, .stCheckbox label, [data-testid="stWidgetLabel"] p { color:#2b2823 !important; font-family:'DM Mono',monospace !important; font-size:11px !important; letter-spacing:.6px; text-transform:uppercase; }
div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea, div[data-testid="stNumberInput"] input { background:#fffdf8 !important; color:#201e1a !important; -webkit-text-fill-color:#201e1a !important; border:1px solid #c9c0b2 !important; border-radius:4px !important; }
div[data-testid="stTextInput"] input::placeholder, div[data-testid="stTextArea"] textarea::placeholder { color:#81796d !important; -webkit-text-fill-color:#81796d !important; opacity:1 !important; }
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div { background:#fffdf8 !important; color:#201e1a !important; border-color:#c9c0b2 !important; }
div[data-testid="stSelectbox"] div[data-baseweb="select"] span { color:#201e1a !important; }
div[data-testid="stNumberInput"] button { background:#f6f0e6 !important; color:#201e1a !important; border-color:#c9c0b2 !important; }
.stButton > button, .stLinkButton a { border-radius:3px; background:#201e1a; color:#fff8ee; border:1px solid #201e1a; font:12px 'DM Mono',monospace; letter-spacing:.7px; }
.stButton > button:hover, .stLinkButton a:hover { background:var(--accent); color:white; border-color:var(--accent); }
div[data-testid="stAlert"] { border-radius:4px; }
.track-row { display:flex; gap:14px; align-items:baseline; border-bottom:1px solid var(--line); padding:10px 3px; font:13px 'DM Sans',sans-serif; color:#292620; }
.track-num { color:var(--accent); font:11px 'DM Mono',monospace; }
div[data-testid="stExpander"] { background:#faf7f0; border:1px solid #d7cfc1; border-radius:5px; }
.footer { border-top:1px solid var(--ink); margin-top:34px; padding-top:13px; color:#625d54; font:10px 'DM Mono',monospace; letter-spacing:1px; }
@media(max-width:700px) {
  .block-container { padding:1rem 1rem 2rem; }
  .brand .tag { max-width:150px; line-height:1.5; }
  .hero h1 { letter-spacing:-.8px; }
  .panel { padding:14px; }
  .player-card { padding:24px 12px; }
}
</style>
""", unsafe_allow_html=True)


def yt_id(url):
    url = (url or "").strip()
    for marker in ("youtu.be/", "youtube.com/watch?v=", "youtube.com/embed/", "youtube.com/shorts/", "youtube.com/live/"):
        if marker in url:
            return url.split(marker, 1)[1].split("&", 1)[0].split("?", 1)[0].split("/", 1)[0][:11]
    return url[:11] if len(url) == 11 and "/" not in url else ""


def encode_mix(mix):
    raw = json.dumps(mix, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(zlib.compress(raw, 9)).decode("ascii").rstrip("=")


def decode_mix(value):
    try:
        raw = zlib.decompress(base64.urlsafe_b64decode(value + "=" * (-len(value) % 4)))
        data = json.loads(raw.decode("utf-8"))
        if isinstance(data, dict) and isinstance(data.get("tracks"), list):
            data.setdefault("copy", {})
            data.setdefault("skin", "CD player")
            data["tracks"] = [
                {"title": str(t.get("title", "Untitled track"))[:120], "url": str(t.get("url", ""))[:500]}
                for t in data["tracks"][:20] if isinstance(t, dict) and yt_id(str(t.get("url", "")))
            ]
            return data
    except (ValueError, TypeError, zlib.error, UnicodeDecodeError):
        pass
    return None


DEFAULT_COPY = {
    "hero_eyebrow": "Digital mixtapes for the people you love",
    "hero_title": "Some things are better",
    "hero_accent": "said in songs.",
    "hero_description": "Pick the songs, write the note you can’t quite say out loud, and send someone a little piece of your world.",
    "recipient_eyebrow": "A little something for you",
    "recipient_title": "Someone made you",
    "recipient_accent": "a mixtape.",
    "recipient_description": "Put your headphones on. Take your time.",
    "player_kicker": "A mixtape, made just for you",
    "player_hint": "Press play whenever you need it",
    "side_label": "Side A",
    "dedication_heading": "The dedication",
    "tracklist_heading": "The tracklist",
    "preview_heading": "A little preview",
    "footer_text": "Made with feeling · No database required · Music plays through YouTube",
    "brand_tagline": "A little music, sent with feeling",
    "burn_button_label": "Burn this mixtape ↗",
    "share_button_label": "Open / share mixtape",
    "make_own_label": "Make your own mixtape",
    "now_playing_label": "Now playing",
    "previous_button_label": "◀ PREV",
    "play_button_label": "▶ PLAY",
    "pause_button_label": "Ⅱ PAUSE",
    "next_button_label": "NEXT ▶",
    "playback_note": "Playback is provided by YouTube.",
}


def sync_copy_value(key):
    values = dict(st.session_state.get("copy_values", DEFAULT_COPY))
    values[key] = st.session_state.get(f"copy_{key}", values.get(key, ""))
    st.session_state["copy_values"] = values


def render_brand(copy):
    tagline = html.escape(str(copy.get("brand_tagline", DEFAULT_COPY["brand_tagline"])))
    st.markdown(
        f'<div class="brand"><b>mixtape<span class="dot">.</span>fm</b><div class="tag">{tagline}</div></div>',
        unsafe_allow_html=True,
    )


def render_hero(copy, recipient=False):
    eyebrow = html.escape(str(copy.get("recipient_eyebrow" if recipient else "hero_eyebrow", "")))
    title = html.escape(str(copy.get("recipient_title" if recipient else "hero_title", "")))
    accent = html.escape(str(copy.get("recipient_accent" if recipient else "hero_accent", "")))
    desc = html.escape(str(copy.get("recipient_description" if recipient else "hero_description", "")))
    st.markdown(
        f'<div class="hero"><div class="eyebrow">{eyebrow}</div>'
        f'<h1>{title}<br><em>{accent}</em></h1><p>{desc}</p></div>',
        unsafe_allow_html=True,
    )


def render_player_card(mix):
    copy = mix.get("copy", {})
    skin = {"CD player": "", "iPod classic": "ipod", "Scrapbook": "scrapbook", "Webcore": "webcore"}.get(mix.get("skin", "CD player"), "")
    title = html.escape(str(mix.get("title", "a little mixtape for you")))
    sender = html.escape(str(mix.get("sender", "")))
    recipient = html.escape(str(mix.get("recipient", "")))
    note = html.escape(str(mix.get("note", "")))
    kicker = html.escape(str(copy.get("player_kicker", DEFAULT_COPY["player_kicker"])))
    hint = html.escape(str(copy.get("player_hint", DEFAULT_COPY["player_hint"])))
    side = html.escape(str(copy.get("side_label", DEFAULT_COPY["side_label"])))
    cover = str(mix.get("cover", "")).strip()
    if cover.startswith(("https://", "http://")):
        art = f'<img class="cover" src="{html.escape(cover, quote=True)}" alt="Mixtape cover">'
    else:
        art = f'<div class="disc"><div class="disc-label">{side}</div></div>'
    people = " · ".join(v for v in ([f"From {sender}" if sender else "", f"For {recipient}" if recipient else ""]) if v)
    st.markdown(
        f'<div class="player-card {skin}"><div class="kicker">{kicker}</div><h2>{title}</h2>'
        f'<div class="to-line">{people or hint}</div>{art}<p class="note">{note}</p></div>',
        unsafe_allow_html=True,
    )


def render_track_player(tracks, copy, key):
    valid = []
    for track in tracks:
        video = yt_id(str(track.get("url", "")))
        if video:
            valid.append({"id": video, "title": str(track.get("title", "Untitled track"))[:120]})
    if not valid:
        st.info("Add at least one valid YouTube link to enable playback.")
        return
    tracks_json = json.dumps(valid, ensure_ascii=True, separators=(",", ":")).replace("</", "<\\/")
    ui_labels = {
        "now_playing_label": str(copy.get("now_playing_label", DEFAULT_COPY["now_playing_label"]))[:100],
        "previous_button_label": str(copy.get("previous_button_label", DEFAULT_COPY["previous_button_label"]))[:40],
        "play_button_label": str(copy.get("play_button_label", DEFAULT_COPY["play_button_label"]))[:40],
        "pause_button_label": str(copy.get("pause_button_label", DEFAULT_COPY["pause_button_label"]))[:40],
        "next_button_label": str(copy.get("next_button_label", DEFAULT_COPY["next_button_label"]))[:40],
        "playback_note": str(copy.get("playback_note", DEFAULT_COPY["playback_note"]))[:180],
    }
    labels_json = json.dumps(ui_labels, ensure_ascii=True, separators=(",", ":")).replace("</", "<\\/")
    component_html = f"""
    <!doctype html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    *{{box-sizing:border-box}} body{{margin:0;background:transparent;color:#201e1a;font-family:Arial,sans-serif}}
    .wrap{{border:1px solid #d7cfc1;border-radius:6px;background:#faf7f0;padding:12px}}
    .now{{display:flex;align-items:center;justify-content:space-between;gap:10px;margin:0 0 10px}}
    .label{{font:10px monospace;letter-spacing:1.5px;color:#c6533b;text-transform:uppercase}}
    .song{{font:600 13px Arial,sans-serif;color:#292620;overflow-wrap:anywhere;margin-top:4px}}
    .actions{{display:flex;gap:8px;align-items:center;flex-wrap:wrap}}
    button{{border:1px solid #201e1a;background:#201e1a;color:#fff8ee;border-radius:3px;padding:10px 13px;font:11px monospace;letter-spacing:.5px;cursor:pointer}}
    button.primary{{background:#c6533b;border-color:#c6533b}} button:disabled{{opacity:.45;cursor:default}}
    #ytplayer{{width:100%;aspect-ratio:16/9;min-height:220px;border:0;border-radius:4px;background:#211f1c}}
    .foot{{font:10px monospace;color:#746b5f;margin-top:8px;letter-spacing:.5px;overflow-wrap:anywhere}}
    @media(max-width:540px){{#ytplayer{{min-height:190px}}button{{padding:9px 10px}}}}
    </style></head><body><div class="wrap">
      <div class="now"><div><div class="label" id="nowPlayingLabel"></div><div class="song" id="songTitle"></div></div>
      <div class="label" id="trackCount"></div></div>
      <div class="actions">
        <button id="prevBtn" type="button" aria-label="Previous track"></button>
        <button id="playBtn" class="primary" type="button"></button>
        <button id="nextBtn" type="button" aria-label="Next track"></button>
      </div>
      <div style="height:10px"></div><div id="ytplayer"></div>
      <div class="foot" id="playbackNote"></div>
    </div>
    <script>
    const songs = {tracks_json};
    const labels = {labels_json};
    let current = 0, player = null, ready = false, playing = false;
    const songTitle = document.getElementById('songTitle');
    const trackCount = document.getElementById('trackCount');
    const playBtn = document.getElementById('playBtn');
    document.getElementById('nowPlayingLabel').textContent = labels.now_playing_label;
    document.getElementById('prevBtn').textContent = labels.previous_button_label;
    document.getElementById('nextBtn').textContent = labels.next_button_label;
    document.getElementById('playbackNote').textContent = labels.playback_note;
    function refresh() {{
      songTitle.textContent = songs[current].title || 'Untitled track';
      trackCount.textContent = String(current + 1).padStart(2,'0') + ' / ' + String(songs.length).padStart(2,'0');
      playBtn.textContent = playing ? labels.pause_button_label : labels.play_button_label;
      document.getElementById('prevBtn').disabled = songs.length < 2;
      document.getElementById('nextBtn').disabled = songs.length < 2;
    }}
    function createPlayer() {{
      if (!window.YT || !window.YT.Player) return;
      player = new YT.Player('ytplayer', {{
        width:'100%', height:'390', videoId:songs[current].id,
        playerVars:{{playsinline:1, rel:0, modestbranding:1, controls:1}},
        events:{{
          onReady: function() {{ ready = true; refresh(); }},
          onStateChange: function(e) {{
            playing = e.data === YT.PlayerState.PLAYING;
            refresh();
            if (e.data === YT.PlayerState.ENDED && current < songs.length - 1) {{
              current++; player.loadVideoById(songs[current].id); refresh();
            }}
          }}
        }}
      }});
    }}
    window.onYouTubeIframeAPIReady = createPlayer;
    if (!window.YT || !window.YT.Player) {{
      const tag = document.createElement('script'); tag.src = 'https://www.youtube.com/iframe_api';
      document.head.appendChild(tag);
    }} else {{ createPlayer(); }}
    playBtn.addEventListener('click', function() {{
      if (!ready || !player) return;
      if (playing) player.pauseVideo(); else player.playVideo();
    }});
    document.getElementById('prevBtn').addEventListener('click', function() {{
      if (!ready || !player || songs.length < 2) return;
      current = (current - 1 + songs.length) % songs.length; player.loadVideoById(songs[current].id); playing = true; refresh();
    }});
    document.getElementById('nextBtn').addEventListener('click', function() {{
      if (!ready || !player || songs.length < 2) return;
      current = (current + 1) % songs.length; player.loadVideoById(songs[current].id); playing = true; refresh();
    }});
    refresh();
    </script></body></html>
    """
    components.html(component_html, height=545, scrolling=False)

def make_mix(title, sender, recipient, note, cover, skin, tracks, copy):
    return {
        "title": title[:100], "sender": sender[:80], "recipient": recipient[:80],
        "note": note[:700], "cover": cover[:700], "skin": skin,
        "tracks": [
            {"title": str(t.get("title", "Untitled track"))[:120], "url": str(t.get("url", ""))[:500]}
            for t in tracks if yt_id(str(t.get("url", "")))
        ][:20],
        "copy": {k: str(v)[:500] for k, v in copy.items()},
    }


incoming = decode_mix(st.query_params.get("mix", "")) if st.query_params.get("mix") else None

if incoming:
    incoming.setdefault("copy", {})
    copy = {**DEFAULT_COPY, **incoming["copy"]}
    render_brand(copy)
    st.markdown(
        f'<div class="hero"><div class="eyebrow">{html.escape(str(copy["recipient_eyebrow"]))}</div>'
        f'<h1>{html.escape(str(copy["recipient_title"]))}<br><em>{html.escape(str(copy["recipient_accent"]))}</em></h1>'
        f'<p>{html.escape(str(copy["recipient_description"]))}</p></div>',
        unsafe_allow_html=True,
    )
    render_player_card({**incoming, "copy": copy})
    render_track_player(incoming.get("tracks", []), copy, "recipient")
    st.markdown('<div class="footer">' + html.escape(str(copy.get("footer_text", DEFAULT_COPY["footer_text"]))) + '</div>', unsafe_allow_html=True)
    if st.button(str(copy.get("make_own_label", DEFAULT_COPY["make_own_label"]))):
        st.query_params.clear()
        st.rerun()
else:
    # All displayed copy is part of the share payload, so the recipient sees the custom text too.
    if "copy_values" not in st.session_state:
        st.session_state["copy_values"] = dict(DEFAULT_COPY)
    copy_values = {**DEFAULT_COPY, **st.session_state["copy_values"]}
    st.session_state["copy_values"] = copy_values
    for copy_key, copy_default in copy_values.items():
        st.session_state.setdefault(f"copy_{copy_key}", copy_default)

    render_brand(copy_values)
    render_hero(copy_values)
    left, right = st.columns([1.05, 0.95], gap="large")

    with left:
        with st.container(border=True):
            st.markdown(f'<div class="section-title">01 / {html.escape(str(copy_values["dedication_heading"]))}</div>', unsafe_allow_html=True)
            title = st.text_input("Mixtape title", "a little mixtape for you", max_chars=100)
            a, b = st.columns(2)
            sender = a.text_input("From", placeholder="Your name", max_chars=80)
            recipient = b.text_input("For", placeholder="Their name", max_chars=80)
            note = st.text_area("The note", "Some songs that made me think of you.", max_chars=700, height=115)
            cover = st.text_input("Cover image URL (optional)", placeholder="https://...")
            skin = st.selectbox("Player style", ["CD player", "iPod classic", "Scrapbook", "Webcore"])

        with st.expander("Customise all display text", expanded=False):
            st.caption("Edit the home page, player, recipient page, section headings, and playback controls.")
            st.markdown("**Branding**")
            copy_values["brand_tagline"] = st.text_input("Top-bar tagline", max_chars=100, key="copy_brand_tagline", on_change=sync_copy_value, args=("brand_tagline",))
            st.markdown("**Home page**")
            copy_values["hero_eyebrow"] = st.text_input("Home eyebrow", max_chars=100, key="copy_hero_eyebrow", on_change=sync_copy_value, args=("hero_eyebrow",))
            copy_values["hero_title"] = st.text_input("Home headline", max_chars=100, key="copy_hero_title", on_change=sync_copy_value, args=("hero_title",))
            copy_values["hero_accent"] = st.text_input("Home highlighted line", max_chars=100, key="copy_hero_accent", on_change=sync_copy_value, args=("hero_accent",))
            copy_values["hero_description"] = st.text_area("Home introduction", max_chars=400, key="copy_hero_description", on_change=sync_copy_value, args=("hero_description",))
            st.markdown("**Recipient page**")
            copy_values["recipient_eyebrow"] = st.text_input("Recipient eyebrow", max_chars=100, key="copy_recipient_eyebrow", on_change=sync_copy_value, args=("recipient_eyebrow",))
            copy_values["recipient_title"] = st.text_input("Recipient headline", max_chars=100, key="copy_recipient_title", on_change=sync_copy_value, args=("recipient_title",))
            copy_values["recipient_accent"] = st.text_input("Recipient highlighted line", max_chars=100, key="copy_recipient_accent", on_change=sync_copy_value, args=("recipient_accent",))
            copy_values["recipient_description"] = st.text_area("Recipient introduction", max_chars=400, key="copy_recipient_description", on_change=sync_copy_value, args=("recipient_description",))
            st.markdown("**Player and section labels**")
            copy_values["player_kicker"] = st.text_input("Player kicker", max_chars=100, key="copy_player_kicker", on_change=sync_copy_value, args=("player_kicker",))
            copy_values["player_hint"] = st.text_input("Player hint", max_chars=100, key="copy_player_hint", on_change=sync_copy_value, args=("player_hint",))
            copy_values["side_label"] = st.text_input("Disc label", max_chars=30, key="copy_side_label", on_change=sync_copy_value, args=("side_label",))
            copy_values["dedication_heading"] = st.text_input("Dedication section heading", max_chars=80, key="copy_dedication_heading", on_change=sync_copy_value, args=("dedication_heading",))
            copy_values["tracklist_heading"] = st.text_input("Tracklist heading", max_chars=80, key="copy_tracklist_heading", on_change=sync_copy_value, args=("tracklist_heading",))
            copy_values["preview_heading"] = st.text_input("Preview heading", max_chars=80, key="copy_preview_heading", on_change=sync_copy_value, args=("preview_heading",))
            st.markdown("**Actions and playback**")
            copy_values["burn_button_label"] = st.text_input("Burn button", max_chars=60, key="copy_burn_button_label", on_change=sync_copy_value, args=("burn_button_label",))
            copy_values["share_button_label"] = st.text_input("Share button", max_chars=60, key="copy_share_button_label", on_change=sync_copy_value, args=("share_button_label",))
            copy_values["make_own_label"] = st.text_input("Make-your-own button", max_chars=60, key="copy_make_own_label", on_change=sync_copy_value, args=("make_own_label",))
            copy_values["now_playing_label"] = st.text_input("Now-playing label", max_chars=60, key="copy_now_playing_label", on_change=sync_copy_value, args=("now_playing_label",))
            copy_values["previous_button_label"] = st.text_input("Previous-track button", max_chars=30, key="copy_previous_button_label", on_change=sync_copy_value, args=("previous_button_label",))
            copy_values["play_button_label"] = st.text_input("Play button", max_chars=30, key="copy_play_button_label", on_change=sync_copy_value, args=("play_button_label",))
            copy_values["pause_button_label"] = st.text_input("Pause button", max_chars=30, key="copy_pause_button_label", on_change=sync_copy_value, args=("pause_button_label",))
            copy_values["next_button_label"] = st.text_input("Next-track button", max_chars=30, key="copy_next_button_label", on_change=sync_copy_value, args=("next_button_label",))
            copy_values["playback_note"] = st.text_input("Playback note", max_chars=180, key="copy_playback_note", on_change=sync_copy_value, args=("playback_note",))
            copy_values["footer_text"] = st.text_input("Footer text", max_chars=180, key="copy_footer_text", on_change=sync_copy_value, args=("footer_text",))
            st.session_state["copy_values"] = copy_values

        with st.container(border=True):
            st.markdown(f'<div class="section-title">02 / {html.escape(str(copy_values["tracklist_heading"]))}</div>', unsafe_allow_html=True)
            st.caption("Paste YouTube links or 11-character video IDs. Up to 20 tracks.")
            count = st.number_input("Number of tracks", min_value=1, max_value=20, value=3, step=1)
            tracks = []
            defaults = ["A song for the long way home", "The one that reminds me of you", "Track three"]
            for i in range(int(count)):
                with st.container(border=True):
                    c1, c2 = st.columns([0.9, 1.1])
                    default_title = defaults[i] if i < len(defaults) else f"Track {i+1}"
                    track_title = c1.text_input(f"Track {i+1:02d} title", value=default_title, key=f"track_title_{i}", max_chars=120)
                    track_url = c2.text_input("YouTube URL / ID", key=f"track_url_{i}", placeholder="youtube.com/watch?v=...")
                    tracks.append({"title": track_title, "url": track_url})

    with right:
        with st.container(border=True):
            st.markdown(f'<div class="section-title">03 / {html.escape(str(copy_values["preview_heading"]))}</div>', unsafe_allow_html=True)
            mix = make_mix(title, sender, recipient, note, cover, skin, tracks, copy_values)
            render_player_card(mix)
            valid_tracks = mix["tracks"]
            st.caption(f"{len(valid_tracks)} valid YouTube track(s)")
            if valid_tracks:
                render_track_player(valid_tracks, copy_values, "preview")
            else:
                st.info("Add at least one valid YouTube link to preview playback controls.")

            current_payload = encode_mix(mix) if valid_tracks else ""
            if st.button(str(copy_values.get("burn_button_label", DEFAULT_COPY["burn_button_label"])), use_container_width=True, type="primary"):
                if not valid_tracks:
                    st.warning("Add at least one valid YouTube link before burning your mixtape.")
                else:
                    st.session_state["share_payload"] = current_payload

            if current_payload and st.session_state.get("share_payload") == current_payload:
                try:
                    base_url = st.context.url.split("?", 1)[0]
                except Exception:
                    base_url = ""
                share_url = f"{base_url}?mix={quote(current_payload)}" if base_url else ""
                st.success("Your mixtape is ready to share.")
                if share_url:
                    st.code(share_url, language=None)
                    st.link_button(str(copy_values.get("share_button_label", DEFAULT_COPY["share_button_label"])), share_url, use_container_width=True)
                else:
                    st.info("Deploy the app publicly to generate a shareable link.")
                st.caption("The mixtape details are encoded in the URL, so no database is needed. Very long mixtapes can create long links.")

st.markdown('<div class="footer">' + html.escape(str(copy_values.get("footer_text", DEFAULT_COPY["footer_text"]))) + '</div>' if not incoming else "", unsafe_allow_html=True)

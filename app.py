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

/* Each player skin is a separate design, not a recolour of the same card. */
/* Shared CD hardware design used in editor preview and recipient player card. */
/* CD look: translucent jewel case, iridescent disc, and paper liner notes. */
.player-card.skin-cd { padding:10px; border:1px solid #d9cebd; border-radius:7px; background:#e7ddce; color:#26241f; box-shadow:0 7px 18px rgba(64,47,29,.10); text-align:left; overflow:hidden; }
.cd-jewel { position:relative; overflow:hidden; border-radius:4px; padding:12px; border:1px solid rgba(255,255,255,.92); background:linear-gradient(135deg,#fcf8f0 0%,#e8dece 50%,#f7f1e7 100%); box-shadow:inset 0 0 0 1px #d0c4b2,0 2px 4px rgba(49,39,26,.10); }
.cd-jewel:before { content:""; position:absolute; inset:0; pointer-events:none; background:linear-gradient(118deg,rgba(255,255,255,.62) 0%,rgba(255,255,255,0) 25%,rgba(255,255,255,.12) 50%,rgba(255,255,255,0) 65%,rgba(255,255,255,.25) 100%); }
.cd-topline { position:relative; z-index:1; display:flex; justify-content:space-between; gap:8px; align-items:center; padding-bottom:10px; border-bottom:1px solid #d4c8b7; color:#786c5b; font:9px 'DM Mono',monospace; letter-spacing:1.15px; text-transform:uppercase; }
.cd-topline .serial { color:#c6533b; white-space:nowrap; }
.cd-upper { position:relative; z-index:1; display:grid; grid-template-columns:minmax(112px,.9fr) minmax(0,1.1fr); gap:13px; align-items:center; padding:13px 0; }
.cd-disc-stage { position:relative; display:flex; align-items:center; justify-content:center; min-height:175px; border:1px solid #c9bdab; border-radius:3px; background:linear-gradient(145deg,#eee7dc,#ddd1bd); box-shadow:inset 0 0 0 5px rgba(255,255,255,.22); overflow:hidden; }
.cd-disc-stage:before { content:""; position:absolute; inset:6px; border:1px solid rgba(255,255,255,.55); border-radius:2px; }
.cd-platter { position:relative; isolation:isolate; width:clamp(112px,15vw,166px); max-width:100%; aspect-ratio:1/1; border-radius:50%; flex:0 0 auto; border:1px solid rgba(95,95,91,.62); background:repeating-radial-gradient(circle at center,rgba(255,255,255,.36) 0 1px,transparent 2px 5px),conic-gradient(from 2deg,#a9c4c9,#e7d7c8 10%,#b8b2d7 20%,#ecddc2 30%,#a9d5d0 42%,#e3c3cf 54%,#b4c7d8 67%,#f0e4c9 80%,#a6c7c8 91%,#a9c4c9); box-shadow:0 0 0 4px rgba(255,255,255,.48),0 0 0 5px #b5a996,0 5px 9px rgba(42,34,24,.2); animation:cd-spin 12s linear infinite; }
.cd-platter:before { content:""; position:absolute; inset:0; border-radius:50%; background:conic-gradient(from 35deg,transparent 0deg,rgba(255,255,255,.62) 38deg,transparent 80deg,rgba(255,255,255,.18) 145deg,transparent 190deg,rgba(255,255,255,.52) 260deg,transparent 310deg); mix-blend-mode:screen; pointer-events:none; }
.cd-platter:after { content:""; position:absolute; inset:8px; border:1px solid rgba(255,255,255,.45); border-radius:50%; pointer-events:none; }
.cd-disc-label { position:absolute; width:46%; height:46%; left:50%; top:50%; transform:translate(-50%,-50%); border-radius:50%; background:#c6533b; border:2px solid #f5eadc; color:#fff8ec; display:flex; align-items:center; justify-content:center; overflow:hidden; text-align:center; font:8px/1.25 'DM Mono',monospace; padding:4px; box-shadow:0 0 0 2px rgba(90,78,64,.7),inset 0 0 0 1px rgba(255,255,255,.36); }
.cd-disc-label img { width:100%; height:100%; object-fit:cover; border-radius:50%; }
.cd-center-hole { position:absolute; width:9px; height:9px; left:50%; top:50%; transform:translate(-50%,-50%); border-radius:50%; background:#dcd6ca; border:1px solid #777165; box-shadow:0 0 0 1px rgba(0,0,0,.14); z-index:2; }
.cd-copy { min-width:0; text-align:left; }
.cd-edition { font:9px 'DM Mono',monospace; letter-spacing:1.5px; color:#c6533b; text-transform:uppercase; margin-bottom:9px; }
.cd-copy h2 { font:500 clamp(22px,3.2vw,34px)/1.08 'Playfair Display',serif; color:#28241f !important; margin:0 0 11px; letter-spacing:-.5px; overflow-wrap:anywhere; }
.cd-copy-meta { color:#6e6254; font:9px/1.7 'DM Mono',monospace; letter-spacing:.6px; text-transform:uppercase; overflow-wrap:anywhere; }
.cd-copy-rule { width:38px; height:2px; background:#c6533b; margin:13px 0; }
.cd-copy-hint { color:#7a6b59; font:italic 12px/1.45 'Playfair Display',serif; }
.cd-liner { position:relative; z-index:1; background:linear-gradient(#fbf7ef,#f2eadd); border:1px solid #d4c7b5; border-radius:2px; padding:11px 12px 10px; text-align:left; box-shadow:0 2px 3px rgba(60,47,31,.06); }
.cd-liner-head { display:flex; justify-content:space-between; gap:8px; align-items:center; color:#8a7864; font:8px 'DM Mono',monospace; letter-spacing:1.2px; text-transform:uppercase; border-bottom:1px solid #ddd0be; padding-bottom:7px; margin-bottom:8px; }
.cd-liner-head span:first-child { color:#c6533b; }
.cd-liner .note { color:#494033; font:italic 13px/1.58 'Playfair Display',serif; white-space:pre-wrap; overflow-wrap:anywhere; margin:0; max-width:none; }
.cd-bottom { display:flex; justify-content:space-between; flex-wrap:wrap; gap:6px; position:relative; z-index:1; padding:9px 2px 1px; color:#857765; font:8px 'DM Mono',monospace; letter-spacing:.8px; text-transform:uppercase; }
.cd-case-spine { position:absolute; left:4px; top:48px; bottom:12px; width:3px; border-radius:2px; background:linear-gradient(90deg,#b5a894,#fff9ee,#c5b9a6); box-shadow:1px 0 2px rgba(40,30,20,.12); }
@keyframes cd-spin { to { transform:rotate(360deg); } }
@media(max-width:600px) {
  .player-card.skin-cd { padding:7px; }
  .cd-jewel { padding:9px; }
  .cd-upper { grid-template-columns:minmax(100px,.85fr) minmax(0,1.15fr); gap:9px; }
  .cd-disc-stage { min-height:145px; }
  .cd-copy h2 { font-size:22px; }
  .cd-copy-hint { font-size:11px; }
}

.player-card.skin-cassette { background:#33372e; border:1px solid #686b5d; border-radius:8px; padding:13px; color:#f2ead9; box-shadow:0 7px 15px rgba(42,37,25,.18); text-align:left; }
.cassette-shell { background:linear-gradient(135deg,#d7d2c1,#a7a58f 48%,#d6d0be); border:1px solid #eee7d5; border-radius:5px; padding:10px; box-shadow:inset 0 0 0 1px rgba(255,255,255,.6),inset 0 -3px 6px rgba(36,38,29,.15); }
.cassette-topline { display:flex; justify-content:space-between; gap:8px; color:#414539; font:8px 'DM Mono',monospace; letter-spacing:1.1px; text-transform:uppercase; padding:2px 2px 9px; }
.cassette-label { position:relative; padding:10px 12px 9px; background:linear-gradient(135deg,#f7edda,#e5d5b8); border:1px solid #a89a7e; color:#37372d; min-height:76px; }
.cassette-label:after { content:""; position:absolute; right:10px; top:12px; bottom:12px; width:3px; background:repeating-linear-gradient(to bottom,#c6533b 0 5px,transparent 5px 9px); opacity:.8; }
.cassette-title { font:500 clamp(20px,3vw,30px)/1.12 'Playfair Display',serif; margin:3px 22px 6px 0; color:#282a22; overflow-wrap:anywhere; }
.cassette-meta { font:8px 'DM Mono',monospace; color:#70654f; letter-spacing:.8px; text-transform:uppercase; overflow-wrap:anywhere; }
.cassette-window { position:relative; margin:10px 0 9px; min-height:118px; background:linear-gradient(180deg,#373b31,#20231d); border:1px solid #717363; border-radius:4px; padding:12px 13px; display:flex; align-items:center; justify-content:space-around; gap:9px; overflow:hidden; }
.cassette-window:before { content:""; position:absolute; inset:5px; border:1px solid rgba(237,227,204,.16); border-radius:2px; pointer-events:none; }
.cassette-reel { position:relative; width:72px; height:72px; border:2px solid #bab59f; border-radius:50%; background:repeating-conic-gradient(#d0c7ae 0 12deg,#777b6d 12deg 26deg,#d0c7ae 26deg 36deg); box-shadow:0 0 0 4px #242720,0 0 0 5px #858875,inset 0 0 0 7px #454a3d; flex:0 0 auto; }
.cassette-reel:before { content:""; position:absolute; inset:19px; border-radius:50%; background:#d8cdb2; border:2px solid #777560; box-shadow:inset 0 0 0 4px #aba58d; }
.cassette-reel:after { content:""; position:absolute; width:8px; height:8px; left:50%; top:50%; transform:translate(-50%,-50%); border-radius:50%; background:#393c31; border:1px solid #f3e7cb; }
.cassette-tape { position:absolute; left:29%; right:29%; top:50%; height:17px; transform:translateY(-50%); background:linear-gradient(#b6a889,#e3d6b9 48%,#a5987b); border:1px solid #c9bda1; box-shadow:0 1px 3px #1116; }
.cassette-window-footer { display:flex; justify-content:space-between; gap:8px; color:#dfd6bf; font:8px 'DM Mono',monospace; letter-spacing:1px; margin-top:8px; }
.cassette-screws { display:flex; justify-content:space-between; padding:1px 3px 0; }
.cassette-screws i { width:6px; height:6px; border:1px solid #777766; border-radius:50%; background:#4b4e40; box-shadow:inset 0 0 0 1px #999982; }
.cassette-note { padding:10px 12px; margin-top:10px; background:#e5decc; border:1px solid #b8ad96; color:#454335; font:italic 13px/1.55 'Playfair Display',serif; white-space:pre-wrap; overflow-wrap:anywhere; }
.player-card.skin-ipod { background:linear-gradient(135deg,#e9eae7,#c2c7c2); border:1px solid #a6aba5; border-radius:23px; padding:17px 18px 19px; box-shadow:inset 0 0 0 5px #daddd8, inset 0 0 0 6px #a6aba5, 0 8px 15px #b7aea0; color:#202720; }
.ipod-logo { font:700 11px 'DM Sans',sans-serif; letter-spacing:1.6px; color:#555d56; text-align:center; margin-bottom:12px; }
.ipod-screen { border:3px solid #788178; background:linear-gradient(#e4e9df,#c8d3c5); border-radius:3px; min-height:150px; padding:10px; text-align:left; box-shadow:inset 0 0 10px #a7b19f; }
.ipod-screen-top { display:flex; justify-content:space-between; border-bottom:1px solid #a2ad9c; padding-bottom:6px; color:#4c584b; font:9px 'DM Mono',monospace; }
.ipod-screen-main { display:flex; align-items:center; gap:10px; padding-top:9px; }
.ipod-cover { width:62px; height:62px; flex:0 0 62px; object-fit:cover; border:1px solid #8d9988; }
.ipod-cover.blank { display:grid; place-items:center; background:repeating-linear-gradient(135deg,#aab9a4 0 7px,#d2ddcc 7px 14px); font:10px 'DM Mono',monospace; color:#3d4a3b; }
.ipod-track { min-width:0; font:600 13px/1.25 'DM Sans',sans-serif; color:#263126; overflow-wrap:anywhere; }
.ipod-track small { display:block; font:10px/1.5 'DM Sans',sans-serif; color:#546151; margin-top:4px; }
.ipod-note { font:italic 11px/1.35 'DM Sans',sans-serif; color:#465343; overflow-wrap:anywhere; margin-top:7px; }
.ipod-wheel { width:142px; height:142px; border-radius:50%; margin:18px auto 0; position:relative; background:linear-gradient(145deg,#fbfcfa,#d6d9d5); border:1px solid #9ea39d; box-shadow:inset 0 1px 3px #fff,0 2px 3px #a9aca6; }
.ipod-wheel .wheel-label { position:absolute; color:#727972; font:8px 'DM Sans',sans-serif; letter-spacing:.5px; }
.ipod-wheel .menu { top:16px; left:0; right:0; text-align:center; font-weight:700; }
.ipod-wheel .back { left:17px; top:66px; }.ipod-wheel .next { right:15px; top:66px; }
.ipod-wheel .prev { left:0; right:0; top:40px; text-align:center; transform:rotate(90deg); }
.ipod-wheel .center { position:absolute; width:51px; height:51px; left:50%; top:50%; transform:translate(-50%,-50%); border-radius:50%; background:linear-gradient(#d8dbd7,#b9beb9); border:1px solid #a0a69f; display:grid; place-items:center; color:#555d56; font-size:15px; }

.player-card.skin-scrapbook { background:#e7d5b7; border:1px solid #c3a77d; border-radius:2px; padding:22px 17px 20px; color:#3d2d20; box-shadow:3px 4px 0 #bba17c; transform:rotate(-.4deg); }
.scrap-paper { position:relative; background:#f7ebd6; border:1px solid #d6bd96; padding:24px 15px 20px; color:#3d2d20; box-shadow:0 3px 0 #d0b58a; }
.scrap-tape { position:absolute; top:-10px; left:calc(50% - 38px); width:76px; height:23px; background:#c9b5a0; opacity:.85; transform:rotate(-3deg); border-left:1px dashed #a38d75; border-right:1px dashed #a38d75; }
.scrap-tag { position:absolute; top:8px; right:8px; padding:4px 6px; background:#c6533b; color:#fff5e9; font:8px 'DM Mono',monospace; transform:rotate(5deg); }
.scrap-photo { display:inline-block; background:#fffdf7; padding:7px 7px 20px; transform:rotate(2deg); box-shadow:0 3px 5px #c7b08c; margin:13px auto 17px; }
.scrap-photo img { display:block; width:114px; height:114px; object-fit:cover; }
.scrap-photo .photo-placeholder { width:114px; height:114px; display:grid; place-items:center; background:linear-gradient(135deg,#d9bba0,#ecd5b8 50%,#8a9b8c); color:#fff9eb; font:34px 'Playfair Display',serif; }
.scrap-paper h2 { color:#3d2d20 !important; font:italic 500 clamp(26px,4vw,40px)/1.1 'Playfair Display',serif; }
.scrap-paper .kicker { color:#a43f2c; }
.scrap-paper .to-line { color:#71543b; font-size:10px; }
.scrap-paper .note { color:#684b32; font:italic 15px/1.7 'Playfair Display',serif; border-top:1px dashed #c3a77d; padding-top:12px; margin-top:11px; }
.scrap-hand { font:10px 'DM Mono',monospace; color:#8e7150; letter-spacing:1px; margin-top:12px; }

.player-card.skin-webcore { border:2px solid #ff62c9; border-radius:2px; padding:0; overflow:hidden; background:#14142b; color:#fff; box-shadow:6px 6px 0 #69ead3; text-align:left; }
.web-browser-bar { background:#dbd5ff; color:#24203f; display:flex; gap:5px; align-items:center; padding:8px 9px; font:9px 'DM Mono',monospace; border-bottom:2px solid #ff62c9; }
.web-dot { width:8px; height:8px; border-radius:50%; background:#ff62c9; box-shadow:12px 0 #f4d35e,24px 0 #69ead3; margin-right:20px; flex:0 0 8px; }
.web-window-label { overflow:hidden; white-space:nowrap; text-overflow:ellipsis; }
.web-screen { padding:20px 15px 18px; background:radial-gradient(circle at 50% 10%,#34336d 0,#17172e 55%,#101020 100%); position:relative; }
.web-screen:before { content:""; position:absolute; inset:0; pointer-events:none; background:repeating-linear-gradient(0deg,transparent 0 4px,rgba(255,255,255,.035) 5px 6px); }
.web-badge { display:inline-block; padding:4px 7px; background:#69ead3; color:#18172e; font:900 8px 'DM Mono',monospace; letter-spacing:1px; transform:rotate(-2deg); }
.web-screen h2 { color:#ff8cdb !important; font:700 clamp(24px,3.5vw,38px)/1.1 'DM Sans',sans-serif; text-transform:uppercase; letter-spacing:-1px; text-shadow:3px 3px #5c4bc3; margin:13px 0 8px; }
.web-screen .kicker { color:#69ead3; font-size:9px; }.web-screen .to-line { color:#e4d8ff; font-size:9px; }
.web-art { display:flex; gap:3px; align-items:center; justify-content:center; height:92px; margin:12px 0; border:1px solid #52448d; background:#1c1c3d; overflow:hidden; }
.web-art .bar { width:7px; border-radius:3px 3px 0 0; background:linear-gradient(#ff62c9,#806aff,#69ead3); animation:eq 1s ease-in-out infinite alternate; }
.web-art .bar:nth-child(3n) { animation-delay:-.4s; }.web-art .bar:nth-child(3n + 1) { animation-delay:-.7s; }
@keyframes eq { from { transform:scaleY(.25); opacity:.6; } to { transform:scaleY(1); opacity:1; } }
.web-screen .note { color:#d9d0ff; border-top:1px dashed #6357a3; padding-top:12px; margin-top:10px; font:italic 13px/1.5 'DM Sans',sans-serif; }
.skin-ipod .player-controls, .skin-cd .player-controls, .skin-scrapbook .player-controls, .skin-webcore .player-controls { margin-top:12px; }
.burn-scene { border:1px solid #c8c0b2; border-radius:6px; padding:15px 16px 13px; margin:12px 0 16px; background:#f9f4ea; text-align:center; overflow:hidden; }
.burn-topline { display:flex; justify-content:space-between; gap:10px; font:10px 'DM Mono',monospace; letter-spacing:1px; color:#746b5f; text-transform:uppercase; }
.burn-drive { width:100%; max-width:340px; height:116px; position:relative; margin:13px auto 9px; background:linear-gradient(#4e4941,#292722); border:1px solid #625b50; border-radius:7px; box-shadow:0 5px 0 #d1c7b7; overflow:hidden; }
.burn-slot { position:absolute; left:12%; right:12%; bottom:18px; height:13px; border-radius:2px; background:#111; box-shadow:inset 0 2px 4px #000; }
.burn-led { position:absolute; top:14px; right:16px; width:7px; height:7px; border-radius:50%; background:#d94b36; box-shadow:0 0 8px #f45a40; animation:led-blink .7s infinite alternate; }
.burn-disc { position:absolute; width:82px; height:82px; left:calc(50% - 41px); top:11px; border-radius:50%; border:1px solid #9e968a; background:repeating-radial-gradient(circle,#7b766d 0 2px,#bdb6aa 3px 5px,#5c5851 6px 7px,#c7c0b4 8px 11px); animation:burn-spin 1.8s linear infinite, burn-glow 1.5s ease-in-out infinite alternate; }
.burn-disc:after { content:""; position:absolute; width:25px; height:25px; left:28px; top:28px; border-radius:50%; background:#c6533b; border:2px solid #e0a28e; }
.burn-laser { position:absolute; left:15%; right:15%; top:52px; height:2px; background:#fa5b45; box-shadow:0 0 8px 2px #f6533b; animation:laser-sweep 1.1s ease-in-out infinite alternate; }
.burn-progress { height:5px; background:#ded5c7; margin:11px 0 9px; border-radius:5px; overflow:hidden; }
.burn-progress span { display:block; height:100%; width:100%; background:linear-gradient(90deg,#c6533b,#f1a37c); transform-origin:left; animation:burn-progress 4.2s cubic-bezier(.22,.65,.28,1) both; }
.burn-caption { color:#29251f; font:500 15px 'Playfair Display',serif; }
.burn-sub { color:#746b5f; font:10px 'DM Mono',monospace; margin-top:4px; }
@keyframes burn-spin { to { transform:rotate(360deg); } }
@keyframes burn-glow { from { box-shadow:0 0 3px rgba(246,83,59,.1); } to { box-shadow:0 0 16px rgba(246,83,59,.55); } }
@keyframes laser-sweep { from { transform:translateY(-31px); opacity:.5; } to { transform:translateY(31px); opacity:1; } }
@keyframes burn-progress { from { transform:scaleX(0); } to { transform:scaleX(1); } }
@keyframes led-blink { from { opacity:.3; } to { opacity:1; } }
@media(prefers-reduced-motion:reduce) { .cd-disc,.web-art .bar,.burn-disc,.burn-laser,.burn-led,.burn-progress span { animation:none !important; } }


/* Design-system pass: responsive, readable controls; the physical players carry the personality. */
:root {
  color-scheme: light dark;
  --paper:#EEF1EE; --ink:#18211F; --muted:#52605A; --line:#CDD6D0;
  --accent:#205F55; --panel:#FFFFFF; --surface:#FFFFFF; --surface-soft:#F7FAF8;
  --accent-soft:#E2EEEA; --focus:#174F46;
}
.stApp, [data-testid="stAppViewContainer"] { background:var(--paper) !important; color:var(--ink); }
[data-testid="stMainBlockContainer"], .block-container { max-width:1120px; padding-top:clamp(16px,2.5vw,30px); padding-bottom:clamp(32px,5vw,64px); }
.brand { border-bottom:1px solid var(--line); padding-bottom:14px; }
.brand b { font:700 23px/1.15 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; letter-spacing:-.045em; color:var(--ink); }
.brand .dot { color:var(--accent); }
.brand .tag { font:600 11px/1.4 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; letter-spacing:.09em; color:var(--muted); }
.hero { padding:clamp(24px,4vw,42px) 0 clamp(20px,3vw,32px); }
.hero h1 { max-width:16ch; margin:10px 0 14px; font:650 clamp(2.5rem,6vw,4.4rem)/1.04 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; letter-spacing:-.055em; color:var(--ink); overflow-wrap:anywhere; }
.hero h1 em { color:var(--accent); font-style:normal; font-weight:650; }
.hero p { max-width:650px; color:var(--muted); font:400 16px/1.65 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }
.panel { background:var(--surface); border:1px solid var(--line); border-radius:10px; padding:clamp(14px,2.2vw,22px); margin-bottom:16px; box-shadow:0 1px 2px rgba(24,33,31,.035); }
.section-title { color:var(--muted); border-bottom:1px solid var(--line); padding-bottom:11px; margin-bottom:15px; font:650 12px/1.35 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; letter-spacing:.06em; text-transform:uppercase; }
.stMarkdown, .stMarkdown p, [data-testid="stCaptionContainer"], .stCaption { color:var(--ink); }
.stMarkdown p { line-height:1.55; }
label, .stTextInput label, .stTextArea label, .stSelectbox label, .stNumberInput label, .stSlider label, .stRadio label, .stCheckbox label, [data-testid="stWidgetLabel"] p {
  color:var(--ink) !important; font:600 13px/1.4 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif !important;
  letter-spacing:0 !important; text-transform:none !important;
}
div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea, div[data-testid="stNumberInput"] input {
  background:var(--surface) !important; color:var(--ink) !important; -webkit-text-fill-color:var(--ink) !important;
  border:1px solid var(--line) !important; border-radius:7px !important; font:400 15px/1.45 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif !important;
  min-height:44px; box-shadow:none !important;
}
div[data-testid="stTextArea"] textarea { min-height:104px; }
div[data-testid="stTextInput"] input::placeholder, div[data-testid="stTextArea"] textarea::placeholder { color:var(--muted) !important; -webkit-text-fill-color:var(--muted) !important; opacity:1 !important; }
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div { background:var(--surface) !important; color:var(--ink) !important; border-color:var(--line) !important; border-radius:7px !important; min-height:44px; }
div[data-testid="stSelectbox"] div[data-baseweb="select"] span { color:var(--ink) !important; font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif !important; font-size:14px !important; }
div[data-testid="stNumberInput"] button { background:var(--surface-soft) !important; color:var(--ink) !important; border-color:var(--line) !important; min-width:40px; min-height:44px; }
.stButton > button, .stLinkButton a {
  min-height:44px; padding:10px 15px; border-radius:8px; background:var(--surface); color:var(--ink);
  border:1px solid var(--line); font:600 14px/1.3 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  letter-spacing:0; box-shadow:none; transition:background-color .12s ease,border-color .12s ease,transform .08s ease;
}
.stButton > button:hover, .stLinkButton a:hover { background:var(--accent-soft); color:var(--ink); border-color:var(--accent); }
.stButton > button[kind="primary"], .stButton > button[data-testid="stBaseButton-primary"] { background:var(--accent) !important; color:#FFFFFF !important; border-color:var(--accent) !important; }
.stButton > button:focus-visible, .stLinkButton a:focus-visible, input:focus-visible, textarea:focus-visible, [role="combobox"]:focus-visible { outline:3px solid var(--focus) !important; outline-offset:2px !important; }
.stCaption, [data-testid="stCaptionContainer"] { color:var(--muted) !important; font:400 12px/1.5 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif !important; }
div[data-testid="stAlert"] { border-radius:8px; }
div[data-testid="stExpander"] { background:var(--surface); border:1px solid var(--line); border-radius:9px; }
div[data-testid="stExpander"] summary { min-height:44px; }
.track-row { border-color:var(--line); color:var(--ink); font:400 14px/1.45 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; padding:12px 5px; }
.track-num { color:var(--accent); font:600 12px/1.3 ui-monospace,SFMono-Regular,Menlo,monospace; }
.footer { border-color:var(--line); color:var(--muted); font:400 12px/1.5 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; letter-spacing:0; }
[data-testid="stHorizontalBlock"] { gap:clamp(12px,2vw,22px); }
@media (prefers-color-scheme:dark) {
  :root { --paper:#171C1A; --ink:#F1F4F1; --muted:#B6C0B9; --line:#3B4540; --accent:#87C9B5; --panel:#212825; --surface:#212825; --surface-soft:#272F2B; --accent-soft:#293D36; --focus:#A1D9C8; }
  .stApp, [data-testid="stAppViewContainer"] { background:var(--paper) !important; color:var(--ink); }
  .stMarkdown, .stMarkdown p, [data-testid="stCaptionContainer"], .stCaption, label, [data-testid="stWidgetLabel"] p { color:var(--ink); }
  .brand .tag, .hero p, .stCaption, [data-testid="stCaptionContainer"], .footer { color:var(--muted) !important; }
  div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea, div[data-testid="stNumberInput"] input, div[data-testid="stSelectbox"] div[data-baseweb="select"] > div { background:var(--surface) !important; color:var(--ink) !important; -webkit-text-fill-color:var(--ink) !important; border-color:var(--line) !important; }
  div[data-testid="stTextInput"] input::placeholder, div[data-testid="stTextArea"] textarea::placeholder { color:var(--muted) !important; -webkit-text-fill-color:var(--muted) !important; }
  div[data-testid="stSelectbox"] div[data-baseweb="select"] span { color:var(--ink) !important; }
  .panel, div[data-testid="stExpander"] { background:var(--surface); border-color:var(--line); }
  .stButton > button, .stLinkButton a { background:var(--surface); color:var(--ink); border-color:var(--line); }
  .stButton > button:hover, .stLinkButton a:hover { background:var(--accent-soft); color:var(--ink); }
  .stButton > button[kind="primary"], .stButton > button[data-testid="stBaseButton-primary"] { background:var(--accent) !important; color:#171C1A !important; border-color:var(--accent) !important; }
}
@media (max-width:700px) {
  .block-container, [data-testid="stMainBlockContainer"] { padding:16px 14px 32px; }
  .brand b { font-size:21px; }
  .brand .tag { max-width:155px; font-size:10px; line-height:1.4; }
  .hero h1 { font-size:clamp(2.2rem,10vw,3.4rem); letter-spacing:-.045em; }
  .hero p { font-size:15px; }
  .panel { padding:14px; border-radius:9px; }
  label, .stTextInput label, .stTextArea label, .stSelectbox label, .stNumberInput label, [data-testid="stWidgetLabel"] p { font-size:13px !important; }
  .stButton > button, .stLinkButton a { min-height:44px; width:100%; }
}
@media (prefers-reduced-motion:reduce) {
  *, *::before, *::after { animation-duration:.001ms !important; animation-iteration-count:1 !important; scroll-behavior:auto !important; transition-duration:.001ms !important; }
  .stButton > button:active, .stLinkButton a:active { transform:none !important; }
}
</style>
""", unsafe_allow_html=True)


def install_haptic_bridge():
    """Add page-level tap feedback where the embedded component can access the host page.

    The host-document access is intentionally guarded: some Streamlit/browser versions
    isolate component iframes, in which case player-local feedback still works.
    """
    components.html("""
    <script>
    (function () {
      try {
        const host = window.parent;
        if (!host || !host.document || !host.document.documentElement) return;
        if (host.__mixtapeHapticGlobalSetup) return;
        host.__mixtapeHapticGlobalSetup = true;
        if (typeof host.__mixtapeHapticsEnabled !== "boolean") {
          host.__mixtapeHapticsEnabled = true;
        }
        const style = host.document.createElement("style");
        style.textContent = [
          "button,a,[role=button],input,textarea,select,[data-baseweb=select]{transition:transform .08s ease,filter .08s ease;touch-action:manipulation;-webkit-tap-highlight-color:transparent}",
          "button:active,a:active,[role=button]:active{transform:scale(.985)!important;filter:brightness(.95)}",
          "@media(prefers-reduced-motion:reduce){button,a,[role=button],input,textarea,select{transition:none!important}}"
        ].join("\\n");
        host.document.head.appendChild(style);
        let lastTap = 0;
        const tapTarget = "button,a,input,textarea,select,[role=button],[role=option],[data-baseweb=select]";
        host.document.addEventListener("pointerdown", function (event) {
          if (host.__mixtapeHapticsEnabled === false) return;
          if (!event.target || !event.target.closest || !event.target.closest(tapTarget)) return;
          const now = Date.now();
          if (now - lastTap < 70) return;
          lastTap = now;
          try {
            if (host.navigator && typeof host.navigator.vibrate === "function") {
              host.navigator.vibrate(8);
            }
          } catch (error) {}
        }, true);
      } catch (error) {
        // Cross-origin/sandboxed component: page-wide haptics are unavailable.
      }
    })();
    </script>
    """, height=1, scrolling=False)


install_haptic_bridge()


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
    "footer_text": "",
    "brand_tagline": "PERSONAL MIXTAPE STUDIO",
    "burn_button_label": "Burn this mixtape ↗",
    "share_button_label": "Open / share mixtape",
    "make_own_label": "Make your own mixtape",
    "now_playing_label": "Now playing",
    "previous_button_label": "◀ PREV",
    "play_button_label": "▶ PLAY",
    "pause_button_label": "Ⅱ PAUSE",
    "next_button_label": "NEXT ▶",
    "playback_note": "Playback is provided by YouTube.",
    "burning_text": "Burning your mixtape…",
    "burn_complete_text": "Writing the songs onto a little piece of forever.",
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
    skin = mix.get("skin", "CD player")
    title = html.escape(str(mix.get("title", "a little mixtape for you")))
    sender = html.escape(str(mix.get("sender", "")))
    recipient = html.escape(str(mix.get("recipient", "")))
    note = html.escape(str(mix.get("note", "")))
    kicker = html.escape(str(copy.get("player_kicker", DEFAULT_COPY["player_kicker"])))
    hint = html.escape(str(copy.get("player_hint", DEFAULT_COPY["player_hint"])))
    side = html.escape(str(copy.get("side_label", DEFAULT_COPY["side_label"])))
    cover = str(mix.get("cover", "")).strip()
    people = " · ".join(v for v in ([f"From {sender}" if sender else "", f"For {recipient}" if recipient else ""]) if v)
    people_html = html.escape(people or hint)
    cover_url = html.escape(cover, quote=True) if cover.startswith(("https://", "http://")) else ""
    if skin == "CD player":
        track_count = len(mix.get("tracks", []))
        label_art = f'<img src="{cover_url}" alt="Cover art">' if cover_url else side
        disc = (
            f'<div class="cd-platter"><div class="cd-disc-label">{label_art}</div>'
            f'<div class="cd-center-hole"></div></div>'
        )
        markup = (
            f'<div class="player-card skin-cd"><div class="cd-jewel"><div class="cd-case-spine"></div>'
            f'<div class="cd-topline"><span>mixtape.fm · A personal compilation</span><span class="serial">No. 001</span></div>'
            f'<div class="cd-upper"><div class="cd-disc-stage">{disc}</div>'
            f'<div class="cd-copy"><div class="cd-edition">Made for one person</div><h2>{title}</h2>'
            f'<div class="cd-copy-meta">{people_html}</div><div class="cd-copy-rule"></div>'
            f'<div class="cd-copy-hint">{kicker}</div></div></div>'
            f'<div class="cd-liner"><div class="cd-liner-head"><span>Inside the case</span><span>Side A · {track_count:02d} tracks</span></div>'
            f'<p class="note">{note}</p></div>'
            f'<div class="cd-bottom"><span>CD-R / MIX 01</span><span>Burned with feeling</span><span>44.1 kHz stereo</span></div>'
            f'</div></div>'
        )
    elif skin == "Cassette tape":
        track_count = len(mix.get("tracks", []))
        markup = (
            f'<div class="player-card skin-cassette"><div class="cassette-shell">'
            f'<div class="cassette-topline"><span>mixtape.fm · analogue edition</span><span>TYPE I / NORMAL BIAS</span></div>'
            f'<div class="cassette-label"><div class="cassette-meta">SIDE A · {track_count:02d} TRACK{"S" if track_count != 1 else ""}</div>'
            f'<div class="cassette-title">{title}</div><div class="cassette-meta">{people_html}</div></div>'
            f'<div class="cassette-window"><div class="cassette-reel"></div><div class="cassette-tape"></div>'
            f'<div class="cassette-reel"></div></div>'
            f'<div class="cassette-window-footer"><span>HIGH POSITION</span><span>▰ DOLBY NR</span><span>46 MIN</span></div>'
            f'<div class="cassette-screws"><i></i><i></i><i></i><i></i></div></div>'
            f'<div class="cassette-note">{note}</div></div>'
        )
    elif skin == "iPod classic":
        if cover_url:
            art = f'<img class="ipod-cover" src="{cover_url}" alt="Cover">'
        else:
            art = '<div class="ipod-cover blank">MIX<br>FM</div>'
        markup = (
            f'<div class="player-card skin-ipod"><div class="ipod-logo">iPod</div>'
            f'<div class="ipod-screen"><div class="ipod-screen-top"><span>♫ MUSIC</span><span>100% ▰</span></div>'
            f'<div class="ipod-screen-main">{art}<div class="ipod-track">{title}'
            f'<small>{people_html}</small></div></div><div class="ipod-note">{note}</div></div>'
            f'<div class="ipod-wheel"><span class="wheel-label menu">MENU</span><span class="wheel-label prev">◀</span>'
            f'<span class="wheel-label back">◀◀</span><span class="wheel-label next">▶▶</span>'
            f'<span class="wheel-label" style="right:19px;bottom:14px">▶</span><div class="center">▶</div></div></div>'
        )
    elif skin == "Scrapbook":
        if cover_url:
            photo = f'<img src="{cover_url}" alt="Cover">'
        else:
            photo = '<div class="photo-placeholder">♫</div>'
        markup = (
            f'<div class="player-card skin-scrapbook"><div class="scrap-paper"><div class="scrap-tape"></div>'
            f'<div class="scrap-tag">HANDMADE MIX</div><div class="kicker">{kicker}</div>'
            f'<div class="scrap-photo">{photo}</div><h2>{title}</h2><div class="to-line">{people_html}</div>'
            f'<p class="note">{note}</p><div class="scrap-hand">SIDE A · MADE FOR YOU</div></div></div>'
        )
    else:
        bars = "".join(f'<span class="bar" style="height:{height}px"></span>' for height in [22, 40, 58, 32, 70, 45, 84, 35, 62, 28, 76, 48, 65, 31, 53, 24, 43, 69, 33, 55])
        if cover_url:
            web_art = f'<img src="{cover_url}" alt="Cover" style="width:78px;height:78px;object-fit:cover;border:2px solid #ff62c9">'
        else:
            web_art = bars
        markup = (
            f'<div class="player-card skin-webcore"><div class="web-browser-bar"><span class="web-dot"></span>'
            f'<span class="web-window-label">MIXTAPE.EXE / PLAYER_01</span><span style="margin-left:auto">[_] [X]</span></div>'
            f'<div class="web-screen"><div class="web-badge">NOW LOADING: FEELINGS</div>'
            f'<div class="kicker">{kicker}</div><h2>{title}</h2><div class="to-line">{people_html}</div>'
            f'<div class="web-art">{web_art}</div><p class="note">{note}</p></div></div>'
        )
    st.markdown(markup, unsafe_allow_html=True)


def render_burn_animation(copy):
    headline = html.escape(str(copy.get("burning_text", DEFAULT_COPY.get("burning_text", "Burning your mixtape…"))))
    subline = html.escape(str(copy.get("burn_complete_text", DEFAULT_COPY.get("burn_complete_text", "Writing the songs onto a little piece of forever."))))
    animation = f"""
    <!doctype html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    *{{box-sizing:border-box}} body{{margin:0;background:transparent;font-family:Arial,sans-serif;color:#29251f}}
    .scene{{background:#f2eadd;border:1px solid #d3c4af;border-radius:7px;padding:14px 15px;text-align:center;overflow:hidden}}
    .scene-top{{display:flex;justify-content:space-between;gap:8px;color:#8a7864;font:9px monospace;letter-spacing:1.1px;text-transform:uppercase;border-bottom:1px solid #d8cbb8;padding-bottom:9px}}
    .work-area{{margin:13px auto 12px;position:relative;width:100%;max-width:370px;min-height:148px;display:grid;place-items:center;background:linear-gradient(135deg,#f9f4ea,#e1d5c3);border:1px solid #d0c1ad;border-radius:4px;box-shadow:inset 0 0 0 5px rgba(255,255,255,.24);overflow:hidden}}
    .sleeve{{position:absolute;width:115px;height:137px;left:calc(50% - 95px);top:6px;background:linear-gradient(135deg,#fffaf0,#eee1ce);border:1px solid #d0bda4;box-shadow:2px 3px 0 #c8b49a;transform:rotate(-8deg);animation:sleeve .8s ease-out both}}
    .sleeve:before{{content:"mixtape.fm";position:absolute;top:13px;left:9px;color:#c6533b;font:8px monospace;letter-spacing:.7px}}
    .sleeve:after{{content:"A MIX MADE\\A FOR YOU";white-space:pre;position:absolute;left:9px;bottom:13px;color:#343027;font:500 15px/1.15 Georgia,serif}}
    .disc{{position:relative;width:124px;height:124px;border-radius:50%;border:1px solid #b0a694;background:repeating-radial-gradient(circle at center,rgba(255,255,255,.36) 0 1px,transparent 2px 5px),conic-gradient(from 2deg,#a9c4c9,#e7d7c8 10%,#b8b2d7 20%,#ecddc2 30%,#a9d5d0 42%,#e3c3cf 54%,#b4c7d8 67%,#f0e4c9 80%,#a6c7c8 91%,#a9c4c9);box-shadow:0 0 0 4px rgba(255,255,255,.45),0 0 0 5px #b5a996,0 5px 12px #473a2b33;animation:spin 1.8s linear infinite,arrive .9s ease-out both}}
    .disc:before{{content:"";position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 35deg,transparent,rgba(255,255,255,.6),transparent 80deg,rgba(255,255,255,.2) 145deg,transparent 190deg,rgba(255,255,255,.5) 260deg,transparent 310deg);mix-blend-mode:screen}}
    .disc:after{{content:"";position:absolute;width:39px;height:39px;left:41px;top:41px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#d9755c,#b94a34 75%);border:3px solid #f5eadc;box-shadow:0 0 0 2px #a99b88}}
    .disc-hole{{position:absolute;z-index:2;width:7px;height:7px;left:50%;top:50%;transform:translate(-50%,-50%);border-radius:50%;background:#e6dfd3;border:1px solid #756c5e}}
    .beam{{position:absolute;top:0;bottom:0;width:2px;left:50%;background:#fff;box-shadow:0 0 13px 3px rgba(198,83,59,.34);opacity:.7;animation:beam 1.4s ease-in-out infinite alternate}}
    .progress{{height:5px;background:#ddd0bd;margin:12px 0 9px;border-radius:5px;overflow:hidden}}
    .progress span{{display:block;height:100%;background:linear-gradient(90deg,#c6533b,#dba98c,#a9d5d0);transform-origin:left;animation:progress 4.2s cubic-bezier(.22,.65,.28,1) both}}
    .caption{{font:500 16px Georgia,serif;color:#29251f}}.sub{{color:#786b5a;font:10px monospace;margin-top:5px}}
    .done{{color:#387256;font:10px monospace;letter-spacing:1px;margin-top:5px;opacity:0;animation:done .4s ease-in 3.8s forwards}}
    @keyframes spin{{to{{transform:rotate(360deg)}}}}
    @keyframes arrive{{from{{transform:translateX(20px) rotate(-35deg);opacity:.5}}to{{transform:translateX(0) rotate(0);opacity:1}}}}
    @keyframes sleeve{{from{{transform:translateX(-25px) rotate(-15deg);opacity:0}}to{{transform:translateX(0) rotate(-8deg);opacity:1}}}}
    @keyframes beam{{from{{opacity:.15;transform:translateX(-34px)}}to{{opacity:.65;transform:translateX(34px)}}}}
    @keyframes progress{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
    @keyframes done{{to{{opacity:1}}}}
    @media(prefers-reduced-motion:reduce){{.disc,.beam,.progress span,.sleeve{{animation:none!important}}.done{{opacity:1}}}}
    </style></head><body><div class="scene">
      <div class="scene-top"><span>Preparing your mix</span><span>CD-R · REC ●</span></div>
      <div class="work-area"><div class="sleeve"></div><div class="disc"><div class="disc-hole"></div></div><div class="beam"></div></div>
      <div class="caption">{headline}</div><div class="sub">{subline}</div>
      <div class="progress"><span></span></div><div class="done">✓ MIXTAPE READY TO SHARE</div>
    </div></body></html>
    """
    components.html(animation, height=355, scrolling=False)

def render_track_player(tracks, copy, key, skin="CD player"):
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
    theme_class = {"CD player": "theme-cd", "Cassette tape": "theme-cassette", "iPod classic": "theme-ipod", "Scrapbook": "theme-scrapbook", "Webcore": "theme-webcore"}.get(skin, "theme-cd")
    cassette_markup = ""
    if skin == "Cassette tape":
        cassette_markup = '<div class="cassette-mini-deck" id="cassetteMiniDeck"><div class="cassette-mini-top"><span>CASSETTE · SIDE A</span><span>PLAY / REC</span></div><div class="cassette-mini-window"><div class="cassette-mini-spool"></div><div class="cassette-mini-tape"></div><div class="cassette-mini-spool"></div></div><div class="cassette-mini-status" id="cassetteMiniStatus">STOPPED · PRESS PLAY</div></div>'
    component_html = f"""
    <!doctype html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    *{{box-sizing:border-box}} body{{margin:0;background:transparent;color:#201e1a;font-family:Arial,sans-serif}}
    .wrap{{border:1px solid #d7cfc1;border-radius:6px;background:#faf7f0;padding:12px}}
    .theme-cd{{background:linear-gradient(145deg,#ded9cf,#b9b1a5);border-color:#9c9387;border-radius:4px;padding:10px}}
    .theme-cd .now{{background:#171614;border:1px solid #625b50;border-radius:3px;padding:10px}}
    .theme-cd .label{{color:#e68a70}}.theme-cd .song{{color:#f4eddf}}
    .theme-cd .actions button{{border-radius:2px;background:#292722;border-color:#625b50;color:#f4eddf}}
    .theme-cd .actions button.primary{{background:#c6533b;border-color:#e18c74}}
    .theme-cd #ytplayer{{border:5px solid #292722;border-radius:3px}}
    .theme-cassette{{background:linear-gradient(145deg,#dad5c4,#a9a58e);border:1px solid #f1ead7;border-radius:7px;padding:10px;box-shadow:inset 0 0 0 1px #999783,0 5px 0 #c4bba9}}
    .theme-cassette .now{{background:#e8dfca;border:1px solid #aaa085;border-radius:3px;padding:9px}}
    .theme-cassette .label{{color:#8c4838}}.theme-cassette .song{{color:#292c22}}
    .theme-cassette .actions{{justify-content:center}}
    .theme-cassette .actions button{{background:#33372e;border:1px solid #686b5d;color:#f2ead9;border-radius:3px;box-shadow:inset 0 1px rgba(255,255,255,.12)}}
    .theme-cassette .actions button.primary{{background:#c6533b;border-color:#a73d2a}}
    .theme-cassette #ytplayer{{border:4px solid #34372e;border-radius:4px}}
    .cassette-mini-deck{{background:linear-gradient(145deg,#d7d2c1,#a7a58f 48%,#d6d0be);border:1px solid #eee7d5;border-radius:4px;padding:8px;margin:8px 0 10px;box-shadow:inset 0 0 0 1px rgba(255,255,255,.5)}}
    .cassette-mini-top{{display:flex;justify-content:space-between;gap:8px;color:#414539;font:8px monospace;letter-spacing:1px;padding-bottom:7px}}
    .cassette-mini-window{{position:relative;min-height:75px;display:flex;align-items:center;justify-content:space-around;gap:16px;background:linear-gradient(#373b31,#20231d);border:1px solid #717363;border-radius:3px;padding:8px;overflow:hidden}}
    .cassette-mini-window:before{{content:"";position:absolute;inset:4px;border:1px solid rgba(237,227,204,.16);pointer-events:none}}
    .cassette-mini-spool{{position:relative;width:48px;height:48px;border:2px solid #bab59f;border-radius:50%;background:repeating-conic-gradient(#d0c7ae 0 12deg,#777b6d 12deg 26deg,#d0c7ae 26deg 36deg);box-shadow:0 0 0 3px #242720,0 0 0 4px #858875,inset 0 0 0 5px #454a3d;flex:0 0 auto}}
    .cassette-mini-spool:before{{content:"";position:absolute;inset:12px;border-radius:50%;background:#d8cdb2;border:2px solid #777560;box-shadow:inset 0 0 0 3px #aba58d}}
    .cassette-mini-spool:after{{content:"";position:absolute;width:6px;height:6px;left:50%;top:50%;transform:translate(-50%,-50%);border-radius:50%;background:#393c31;border:1px solid #f3e7cb}}
    .cassette-mini-tape{{position:absolute;left:29%;right:29%;top:50%;height:10px;transform:translateY(-50%);background:linear-gradient(#b6a889,#e3d6b9 48%,#a5987b);border:1px solid #c9bda1}}
    .cassette-mini-deck.is-playing .cassette-mini-spool{{animation:cassette-spin .85s linear infinite}}
    .cassette-mini-status{{font:8px monospace;letter-spacing:1px;color:#4b4d3f;text-align:right;margin-top:6px;text-transform:uppercase}}
    @keyframes cassette-spin{{to{{transform:rotate(360deg)}}}}
    .theme-ipod{{background:linear-gradient(135deg,#e7e9e4,#c5cbc4);border:5px solid #d8dcd6;border-radius:18px;box-shadow:inset 0 0 0 1px #969f96;padding:10px}}
    .theme-ipod .now{{background:#d6e0d0;border:2px solid #7c8979;border-radius:2px;padding:9px;box-shadow:inset 0 0 8px #a4b09e}}
    .theme-ipod .label{{color:#425242}}.theme-ipod .song{{color:#202b20}}
    .theme-ipod .actions{{justify-content:center}}
    .theme-ipod .actions button{{background:linear-gradient(#fdfdfb,#d4d9d3);border:1px solid #9ca49b;color:#3e483e;border-radius:22px;min-width:68px;box-shadow:0 2px 2px #abb1a9}}
    .theme-ipod .actions button.primary{{background:linear-gradient(#d9dfd8,#b7c0b5);color:#243124;border-color:#8c9889}}
    .theme-ipod #ytplayer{{border:3px solid #798779;border-radius:3px}}
    .theme-scrapbook{{background:#f0dfc2;border:2px dashed #b99b70;border-radius:2px;box-shadow:3px 4px 0 #cbb18a;padding:13px}}
    .theme-scrapbook .now{{background:#fff4df;border:1px dashed #cbb18a;padding:10px;transform:rotate(-.2deg)}}
    .theme-scrapbook .label{{color:#9b442f}}.theme-scrapbook .song{{color:#4b3828}}
    .theme-scrapbook .actions button{{background:#7b5b40;border-color:#7b5b40;color:#fff5e6;border-radius:16px}}
    .theme-scrapbook .actions button.primary{{background:#bc4d36;border-color:#bc4d36}}
    .theme-scrapbook #ytplayer{{border:4px solid #fff4df;box-shadow:2px 3px 0 #cbb18a}}
    .theme-webcore{{background:#16162f;border:2px solid #ff62c9;border-radius:2px;box-shadow:5px 5px 0 #69ead3;padding:10px}}
    .theme-webcore .now{{background:#dbd5ff;border:2px solid #ff62c9;padding:9px}}
    .theme-webcore .label{{color:#5c46a8}}.theme-webcore .song{{color:#211e40}}
    .theme-webcore .actions button{{background:#29244f;border:1px solid #ff62c9;border-radius:0;color:#f8e8ff;text-shadow:1px 1px #5c46a8}}
    .theme-webcore .actions button.primary{{background:#ff62c9;border-color:#69ead3;color:#17172c}}
    .theme-webcore #ytplayer{{border:2px solid #69ead3;border-radius:0}}
    .now{{display:flex;align-items:center;justify-content:space-between;gap:10px;margin:0 0 10px}}
    .label{{font:10px monospace;letter-spacing:1.5px;color:#c6533b;text-transform:uppercase}}
    .song{{font:600 13px Arial,sans-serif;color:#292620;overflow-wrap:anywhere;margin-top:4px}}
    .actions{{display:flex;gap:8px;align-items:center;flex-wrap:wrap}}
    button{{border:1px solid #201e1a;background:#201e1a;color:#fff8ee;border-radius:3px;padding:10px 13px;font:11px monospace;letter-spacing:.5px;cursor:pointer}}
    button.primary{{background:#c6533b;border-color:#c6533b}} button:disabled{{opacity:.45;cursor:default}}
    #ytplayer{{width:100%;aspect-ratio:16/9;min-height:220px;border:0;border-radius:4px;background:#211f1c}}
    .foot{{font:10px monospace;color:#746b5f;margin-top:8px;letter-spacing:.5px;overflow-wrap:anywhere}}
    @media(max-width:540px){{#ytplayer{{min-height:190px}}button{{padding:9px 10px}}}}
    </style></head><body><div class="wrap {theme_class}">
      <div class="now"><div><div class="label" id="nowPlayingLabel"></div><div class="song" id="songTitle"></div></div>
      <div class="label" id="trackCount"></div></div>
      {cassette_markup}
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
      const cassetteDeck = document.getElementById('cassetteMiniDeck');
      if (cassetteDeck) {{
        cassetteDeck.classList.toggle('is-playing', playing);
        document.getElementById('cassetteMiniStatus').textContent = playing ? 'PLAYING · REELS IN MOTION' : 'PAUSED · TAPE AT REST';
      }}
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


def render_interactive_player(mix, copy, key):
    """Render the device, its physical controls, and the YouTube player in one iframe.

    Keeping the card and player together means device buttons control the same
    YouTube instance rather than acting as decorative artwork.
    """
    skin = str(mix.get("skin", "CD player"))
    title = html.escape(str(mix.get("title", "Untitled mixtape"))[:100])
    sender = html.escape(str(mix.get("sender", ""))[:80])
    recipient = html.escape(str(mix.get("recipient", ""))[:80])
    note = html.escape(str(mix.get("note", ""))[:700])
    side = html.escape(str(copy.get("side_label", DEFAULT_COPY.get("side_label", "Side A")))[:30])
    kicker = html.escape(str(copy.get("player_kicker", DEFAULT_COPY.get("player_kicker", "A mixtape, made just for you")))[:100])
    hint = html.escape(str(copy.get("player_hint", DEFAULT_COPY.get("player_hint", "Press play whenever you need it")))[:100])
    cover = str(mix.get("cover", "")).strip()
    cover_url = html.escape(cover, quote=True) if cover.startswith(("https://", "http://")) else ""
    people = " · ".join(value for value in ([f"From {sender}" if sender else "", f"For {recipient}" if recipient else ""]) if value)
    people_html = html.escape(people or hint)

    tracks = []
    for track in mix.get("tracks", [])[:20]:
        video_id = yt_id(str(track.get("url", "")))
        if video_id:
            tracks.append({"id": video_id, "title": str(track.get("title", "Untitled track"))[:120]})
    tracks_json = json.dumps(tracks, ensure_ascii=True, separators=(",", ":")).replace("<", "\\u003c")
    labels = {
        "nowPlaying": str(copy.get("now_playing_label", "Now playing"))[:100],
        "play": str(copy.get("play_button_label", "▶ PLAY"))[:40],
        "pause": str(copy.get("pause_button_label", "Ⅱ PAUSE"))[:40],
        "previous": str(copy.get("previous_button_label", "◀ PREV"))[:40],
        "next": str(copy.get("next_button_label", "NEXT ▶"))[:40],
        "playbackNote": str(copy.get("playback_note", "Playback is provided by YouTube."))[:180],
    }
    labels_json = json.dumps(labels, ensure_ascii=True, separators=(",", ":")).replace("<", "\\u003c")

    if skin == "CD player":
        label_art = f'<img src="{cover_url}" alt="Cover art">' if cover_url else side
        device_markup = (
            f'<div class="device cd-device" id="devicePanel">'
            f'<div class="cd-case" id="cdCase"><div class="cd-case-lid"></div><div class="cd-jewel">'
            f'<div class="device-topline"><span>mixtape.fm / compact disc</span><span class="case-serial">CD-R 01</span></div>'
            f'<div class="cd-layout"><button class="cd-disc-touch" data-action="toggle-play" aria-label="Play or pause mixtape">'
            f'<span class="cd-disc"><span class="cd-sheen"></span><span class="cd-disc-label">{label_art}</span><span class="cd-hole"></span></span></button>'
            f'<div class="cd-copy"><div class="eyebrow">PERSONAL COMPILATION</div><h2>{title}</h2>'
            f'<div class="device-meta">{people_html}</div><div class="accent-rule"></div>'
            f'<p class="cd-dedication">{note}</p><div class="cd-kicker">{kicker}</div></div></div>'
            f'<div class="cd-inner-note"><span>INSIDE THE CASE</span><span>{len(tracks):02d} TRACKS · SIDE A</span></div>'
            f'<div class="device-buttons cd-buttons"><button data-action="previous" aria-label="Previous track">◀◀ PREV</button>'
            f'<button data-action="toggle-play" data-play-label>▶ PLAY</button><button data-action="next" aria-label="Next track">NEXT ▶▶</button>'
            f'<button data-action="eject" id="caseButton">OPEN CASE</button></div>'
            f'<div class="cd-case-open-note" id="caseOpenNote" hidden>CASE OPEN · SELECT A TRACK BELOW</div>'
            f'<div class="cd-bottomline"><span>44.1 kHz stereo</span><span>Made for one person</span></div>'
            f'</div></div></div>'
        )
        theme_class = "theme-cd"
    elif skin == "Cassette tape":
        device_markup = (
            f'<div class="device cassette-device" id="devicePanel"><div class="cassette-shell">'
            f'<div class="device-topline"><span>mixtape.fm · analogue edition</span><span>TYPE I / NORMAL BIAS</span></div>'
            f'<div class="cassette-label"><div class="cassette-small">SIDE A · {len(tracks):02d} TRACKS</div>'
            f'<h2>{title}</h2><div class="cassette-small">{people_html}</div></div>'
            f'<div class="cassette-window"><button class="cassette-reel" data-action="toggle-play" aria-label="Play or pause cassette"><span></span></button>'
            f'<div class="cassette-tape-strip"></div><button class="cassette-reel" data-action="toggle-play" aria-label="Play or pause cassette"><span></span></button></div>'
            f'<div class="cassette-status" id="cassetteStatus">STOPPED · PRESS PLAY</div>'
            f'<p class="cassette-note">{note}</p>'
            f'<div class="device-buttons cassette-buttons"><button data-action="previous" aria-label="Rewind to previous track">◀◀ REW</button>'
            f'<button data-action="stop">■ STOP</button><button data-action="toggle-play" data-play-label>▶ PLAY</button>'
            f'<button data-action="next" aria-label="Fast forward to next track">FF ▶▶</button></div>'
            f'</div></div>'
        )
        theme_class = "theme-cassette"
    elif skin == "iPod classic":
        if cover_url:
            art = f'<img class="ipod-cover" src="{cover_url}" alt="Cover art">'
        else:
            art = '<div class="ipod-cover blank">MIX<br>FM</div>'
        device_markup = (
            f'<div class="device ipod-device" id="devicePanel"><div class="ipod-logo">iPod</div>'
            f'<div class="ipod-screen"><div class="ipod-screen-top"><span>♫ MUSIC</span><span id="ipodPlayStatus">READY</span></div>'
            f'<div class="ipod-screen-main">{art}<div class="ipod-track"><strong>{title}</strong>'
            f'<small>{people_html}</small><small id="ipodTrackTitle">Select a track to begin</small></div></div>'
            f'<div class="ipod-note">{note}</div></div>'
            f'<div class="ipod-wheel" aria-label="iPod click wheel">'
            f'<button class="wheel-menu" data-action="toggle-tracklist">MENU</button>'
            f'<button class="wheel-prev" data-action="previous" aria-label="Previous track">◀◀</button>'
            f'<button class="wheel-next" data-action="next" aria-label="Next track">▶▶</button>'
            f'<button class="wheel-stop" data-action="stop" aria-label="Stop playback">■</button>'
            f'<button class="wheel-center" data-action="toggle-play" aria-label="Play or pause"><span data-role="ipod-play-icon">▶</span></button>'
            f'</div><div class="ipod-hint">MENU: TRACKLIST · LEFT / RIGHT: SKIP · CENTER: PLAY</div></div>'
        )
        theme_class = "theme-ipod"
    elif skin == "Scrapbook":
        if cover_url:
            photo = f'<img src="{cover_url}" alt="Cover art">'
        else:
            photo = '<span class="photo-placeholder">♫</span>'
        device_markup = (
            f'<div class="device scrapbook-device" id="devicePanel"><div class="scrap-paper">'
            f'<div class="scrap-tape"></div><div class="scrap-tag">HANDMADE MIX</div>'
            f'<div class="scrap-kicker">{kicker}</div><button class="scrap-photo" data-action="toggle-play" aria-label="Play or pause mixtape">{photo}</button>'
            f'<h2>{title}</h2><div class="device-meta">{people_html}</div><p class="scrap-note">{note}</p>'
            f'<div class="device-buttons"><button data-action="previous">◀ PREV</button><button data-action="toggle-play" data-play-label>▶ PLAY</button>'
            f'<button data-action="next">NEXT ▶</button><button data-action="toggle-tracklist">TRACKLIST</button></div>'
            f'<div class="scrap-bottom">SIDE A · MADE FOR YOU</div></div></div>'
        )
        theme_class = "theme-scrapbook"
    else:
        bars = "".join(f'<span class="equalizer-bar" style="height:{height}px"></span>' for height in [17, 30, 47, 23, 59, 35, 45, 20, 65, 31, 53, 26, 42, 18, 61, 33, 47, 22])
        device_markup = (
            f'<div class="device webcore-device" id="devicePanel"><div class="web-browser-bar">'
            f'<span class="web-dot"></span><span class="web-window-label">MIXTAPE.EXE / PLAYER_01</span>'
            f'<button data-action="toggle-tracklist" aria-label="Toggle tracklist">−</button><button data-action="stop" aria-label="Stop playback">×</button></div>'
            f'<div class="web-screen"><div class="web-badge">NOW LOADING: FEELINGS</div><div class="web-kicker">{kicker}</div>'
            f'<h2>{title}</h2><div class="device-meta">{people_html}</div><div class="web-art">{bars}</div>'
            f'<p class="web-note">{note}</p><div class="device-buttons"><button data-action="previous">◀ PREV</button>'
            f'<button data-action="toggle-play" data-play-label>▶ PLAY</button><button data-action="next">NEXT ▶</button></div></div></div>'
        )
        theme_class = "theme-webcore"

    track_buttons = []
    for index, track in enumerate(tracks):
        track_title = html.escape(str(track.get("title", "Untitled track"))[:120])
        track_buttons.append(
            f'<button class="track-pick" data-action="select-track" data-index="{index}">'
            f'<span class="track-pick-number">{index + 1:02d}</span><span class="track-pick-title">{track_title}</span>'
            f'<span class="track-pick-play">▶</span></button>'
        )
    tracklist_markup = "".join(track_buttons) if track_buttons else '<div class="empty-tracks">Add a valid YouTube URL to enable playback.</div>'

    template = r"""<!doctype html>
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{box-sizing:border-box}
body{margin:0;padding:0;background:transparent;color:#24221d;font-family:Arial,sans-serif;-webkit-tap-highlight-color:transparent}
button{font:inherit;cursor:pointer;touch-action:manipulation;-webkit-tap-highlight-color:transparent}
button:focus-visible{outline:3px solid #c6533b;outline-offset:3px}
button:active{transform:scale(.97)}
.player-shell{width:100%;padding:8px;border:1px solid #d7cfc1;border-radius:7px;background:#f7f2e9;display:grid;gap:11px}
.device{position:relative;width:100%;overflow:hidden}
.device h2{overflow-wrap:anywhere}
.device-topline{display:flex;justify-content:space-between;align-items:center;gap:8px;font:8px monospace;letter-spacing:1px;text-transform:uppercase;color:#70685a}
.device-meta{font:9px/1.55 monospace;letter-spacing:.5px;text-transform:uppercase;overflow-wrap:anywhere;color:#6b6254}
.device-buttons{display:flex;gap:6px;justify-content:center;flex-wrap:wrap;margin-top:11px}
.device-buttons button{border-radius:3px;padding:9px 11px;border:1px solid #6c6254;background:#312f29;color:#f6f0e5;font:9px monospace;letter-spacing:.6px;min-height:34px}
.device-buttons button:disabled{opacity:.35;cursor:default}
.eyebrow{font:9px monospace;letter-spacing:1.5px;color:#c6533b;text-transform:uppercase}
.player-status-line{display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap;background:#201e1a;color:#f3eee4;border-radius:4px;padding:10px 12px;font:10px monospace;letter-spacing:.6px}
.player-status-line #playerStatus{overflow-wrap:anywhere;color:#e6c6ad}
.player-status-line #trackCounter{white-space:nowrap}
.playback-note{font:10px monospace;color:#746b5f;padding:0 2px}
.player-video{width:100%;border-radius:4px;overflow:hidden;background:#171614;border:1px solid #d7cfc1}
#ytplayer{width:100%;min-height:210px;aspect-ratio:16/9;border:0;display:block}
.common-controls{display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap}
.common-controls button,.tracklist-toggle,.haptic-toggle{border:1px solid #c9bfae;border-radius:3px;background:#fcf8ef;color:#24221d;padding:9px 10px;font:9px monospace;letter-spacing:.5px;min-height:34px}
.common-controls button:disabled{opacity:.4;cursor:default}
.tracklist-panel{border:1px solid #d7cfc1;border-radius:4px;padding:8px;background:#fbf7ef}
.tracklist-panel[hidden]{display:none!important}
.track-pick{width:100%;display:flex;align-items:center;gap:10px;border:0;border-bottom:1px solid #e1d8c9;background:transparent;color:#28251f;text-align:left;padding:10px 6px;min-height:40px}
.track-pick:last-child{border-bottom:0}
.track-pick[aria-current="true"]{background:#eee1d0}
.track-pick-number{font:10px monospace;color:#c6533b}
.track-pick-title{flex:1;min-width:0;font:12px Arial,sans-serif;overflow-wrap:anywhere}
.track-pick-play{font-size:11px;color:#c6533b}
.empty-tracks{font:12px Arial,sans-serif;color:#70685a;padding:12px}
.cd-device{padding:10px;border:1px solid #d7cbbb;border-radius:7px;background:#e6ddcf;box-shadow:0 5px 0 #d0c6b7}
.cd-case{position:relative;padding:12px;border:1px solid #fff8eb;border-radius:4px;background:linear-gradient(135deg,#fcf8f0,#e7dece 50%,#f7f1e7);box-shadow:inset 0 0 0 1px #d0c4b2;transition:transform .25s}
.cd-case-lid{height:5px;border-radius:3px;background:linear-gradient(90deg,#c6baa7,#fff9ef,#c6baa7);margin-bottom:10px;transition:height .25s,transform .25s}
.cd-case.is-open .cd-case-lid{height:15px;transform:perspective(500px) rotateX(18deg);background:linear-gradient(#b9ab95,#f5ead7)}
.cd-layout{display:grid;grid-template-columns:minmax(115px,.9fr) minmax(0,1.1fr);gap:12px;align-items:center;padding:15px 0}
.cd-disc-touch{border:0!important;padding:0!important;background:transparent!important;box-shadow:none!important;width:100%;display:flex;align-items:center;justify-content:center;min-width:0}
.cd-disc{display:block;position:relative;isolation:isolate;width:min(100%,165px);aspect-ratio:1;border-radius:50%;border:1px solid #b1a995;background:repeating-radial-gradient(circle,rgba(255,255,255,.42) 0 1px,transparent 2px 5px),conic-gradient(from 5deg,#a9c4c9,#e7d7c8 10%,#b8b2d7 20%,#ecddc2 30%,#a9d5d0 42%,#e3c3cf 54%,#b4c7d8 67%,#f0e4c9 80%,#a6c7c8 91%,#a9c4c9);box-shadow:0 0 0 4px rgba(255,255,255,.45),0 0 0 5px #b5a996,0 5px 12px #473a2b33}
.cd-disc:before{content:"";position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 35deg,transparent,rgba(255,255,255,.6),transparent 80deg,rgba(255,255,255,.2) 145deg,transparent 190deg,rgba(255,255,255,.5) 260deg,transparent 310deg);mix-blend-mode:screen;pointer-events:none}
.cd-sheen{position:absolute;inset:8px;border:1px solid rgba(255,255,255,.45);border-radius:50%}
.cd-disc-label{position:absolute;width:46%;height:46%;left:50%;top:50%;transform:translate(-50%,-50%);border-radius:50%;background:#c6533b;border:2px solid #f5eadc;color:#fff8ec;display:flex;align-items:center;justify-content:center;overflow:hidden;text-align:center;font:8px/1.25 monospace;padding:4px;box-shadow:0 0 0 2px #a99b88}
.cd-disc-label img{width:100%;height:100%;object-fit:cover;border-radius:50%}
.cd-hole{position:absolute;width:8px;height:8px;left:50%;top:50%;transform:translate(-50%,-50%);border-radius:50%;background:#e6dfd3;border:1px solid #756c5e;z-index:2}
.cd-copy{min-width:0;text-align:left}.cd-copy h2{margin:8px 0 10px;font:500 clamp(21px,3vw,31px)/1.1 Georgia,serif;color:#28241f;letter-spacing:-.4px}
.cd-copy .accent-rule{width:32px;height:2px;background:#c6533b;margin:10px 0}
.cd-dedication{font:italic 12px/1.5 Georgia,serif;color:#514737;overflow-wrap:anywhere;margin:0 0 9px}
.cd-kicker{font:8px/1.5 monospace;color:#7a6a57;text-transform:uppercase;letter-spacing:.6px}
.cd-inner-note{display:flex;justify-content:space-between;flex-wrap:wrap;gap:5px;padding:9px 1px;border-top:1px solid #d8cbb9;color:#897a65;font:8px monospace;letter-spacing:1px}
.cd-buttons button{background:#2a2924;border-color:#60594c}.cd-buttons [data-action="eject"]{background:#eee5d7;color:#6d5c49;border-color:#b7a792}
.cd-bottomline{display:flex;justify-content:space-between;gap:8px;color:#857765;font:8px monospace;letter-spacing:.5px;text-transform:uppercase;margin-top:10px}
.cd-case-open-note{font:9px monospace;color:#c6533b;background:#f4e9d9;padding:8px;border-radius:3px;margin-top:6px}
.cd-case-open-note[hidden]{display:none!important}
.cd-device.is-playing .cd-disc{animation:disc-rotate 9s linear infinite}
@keyframes disc-rotate{to{transform:rotate(360deg)}}
.cassette-device{background:#32362e;border:1px solid #666b5a;border-radius:7px;padding:12px;box-shadow:0 5px 0 #c3b9a7}
.cassette-shell{background:linear-gradient(135deg,#d7d2c1,#a7a58f 48%,#d6d0be);border:1px solid #eee7d5;border-radius:4px;padding:10px}
.cassette-label{padding:10px 12px;background:linear-gradient(135deg,#f7edda,#e5d5b8);border:1px solid #a89a7e;color:#37372d}
.cassette-small{font:8px monospace;color:#70654f;letter-spacing:.8px;text-transform:uppercase;overflow-wrap:anywhere}
.cassette-label h2{font:500 clamp(20px,3vw,30px)/1.1 Georgia,serif;color:#282a22;margin:5px 0 7px;overflow-wrap:anywhere}
.cassette-window{position:relative;margin:10px 0 8px;min-height:108px;background:linear-gradient(#373b31,#20231d);border:1px solid #717363;border-radius:4px;padding:12px 13px;display:flex;align-items:center;justify-content:space-around;gap:9px;overflow:hidden}
.cassette-reel{position:relative;padding:0!important;width:68px;height:68px;flex:0 0 auto;border:2px solid #bab59f!important;border-radius:50%!important;background:repeating-conic-gradient(#d0c7ae 0 12deg,#777b6d 12deg 26deg,#d0c7ae 26deg 36deg)!important;box-shadow:0 0 0 4px #242720,0 0 0 5px #858875,inset 0 0 0 7px #454a3d}
.cassette-reel span{position:absolute;inset:18px;border-radius:50%;background:#d8cdb2;border:2px solid #777560;box-shadow:inset 0 0 0 4px #aba58d}
.cassette-reel span:after{content:"";position:absolute;width:7px;height:7px;left:50%;top:50%;transform:translate(-50%,-50%);border-radius:50%;background:#393c31;border:1px solid #f3e7cb}
.cassette-tape-strip{position:absolute;left:29%;right:29%;top:50%;height:15px;transform:translateY(-50%);background:linear-gradient(#b6a889,#e3d6b9 48%,#a5987b);border:1px solid #c9bda1;pointer-events:none}
.cassette-status{text-align:right;color:#dfd6bf;font:8px monospace;letter-spacing:1px}
.cassette-note{padding:9px 10px;margin:9px 0 0;background:#e5decc;border:1px solid #b8ad96;color:#454335;font:italic 12px/1.5 Georgia,serif;white-space:pre-wrap;overflow-wrap:anywhere}
.cassette-device.is-playing .cassette-reel{animation:spool-rotate .85s linear infinite}
@keyframes spool-rotate{to{transform:rotate(360deg)}}
.ipod-device{max-width:430px;margin:0 auto;background:linear-gradient(135deg,#e9eae7,#c2c7c2);border:1px solid #a6aba5;border-radius:24px;padding:16px 18px 18px;box-shadow:inset 0 0 0 5px #daddd8,inset 0 0 0 6px #a6aba5,0 8px 15px #b7aea0}
.ipod-logo{text-align:center;color:#555d56;font:700 12px Arial,sans-serif;letter-spacing:1.5px;margin-bottom:11px}
.ipod-screen{border:3px solid #788178;background:linear-gradient(#e4e9df,#c8d3c5);border-radius:3px;min-height:144px;padding:10px;text-align:left;box-shadow:inset 0 0 10px #a7b19f}
.ipod-screen-top{display:flex;justify-content:space-between;border-bottom:1px solid #a2ad9c;padding-bottom:6px;color:#4c584b;font:8px monospace}
.ipod-screen-main{display:flex;align-items:center;gap:10px;padding-top:9px}
.ipod-cover{width:60px;height:60px;flex:0 0 60px;object-fit:cover;border:1px solid #8d9988}.ipod-cover.blank{display:grid;place-items:center;background:repeating-linear-gradient(135deg,#aab9a4 0 7px,#d2ddcc 7px 14px);font:10px monospace;color:#3d4a3b}
.ipod-track{min-width:0;font:600 12px/1.25 Arial,sans-serif;color:#263126;overflow-wrap:anywhere}.ipod-track small{display:block;font:9px/1.5 Arial,sans-serif;color:#546151;margin-top:4px}
.ipod-note{font:italic 10px/1.35 Arial,sans-serif;color:#465343;overflow-wrap:anywhere;margin-top:7px}
.ipod-wheel{width:160px;height:160px;border-radius:50%;margin:17px auto 0;position:relative;background:linear-gradient(145deg,#fbfcfa,#d6d9d5);border:1px solid #9ea39d;box-shadow:inset 0 1px 3px #fff,0 2px 3px #a9aca6}
.ipod-wheel button{position:absolute;border:0;background:transparent;color:#727972;font:8px Arial,sans-serif;padding:0;min-width:28px;min-height:26px}
.ipod-wheel .wheel-menu{top:11px;left:calc(50% - 25px);width:50px;font-weight:700}
.ipod-wheel .wheel-prev{left:5px;top:calc(50% - 13px);width:42px;height:26px}
.ipod-wheel .wheel-next{right:5px;top:calc(50% - 13px);width:42px;height:26px}
.ipod-wheel .wheel-stop{left:calc(50% - 15px);bottom:8px;width:30px}
.ipod-wheel .wheel-center{left:calc(50% - 27px);top:calc(50% - 27px);width:54px;height:54px;border-radius:50%;background:linear-gradient(#d8dbd7,#b9beb9);border:1px solid #a0a69f;box-shadow:inset 0 1px #fff;font-size:18px;color:#555d56}
.ipod-hint{text-align:center;margin-top:10px;color:#4e584d;font:7px monospace;letter-spacing:.4px}
.scrapbook-device{padding:12px;background:#e7d5b7;border:1px solid #c3a77d;border-radius:2px;box-shadow:3px 4px 0 #bba17c;transform:rotate(-.15deg)}
.scrap-paper{position:relative;background:#f7ebd6;border:1px solid #d6bd96;padding:24px 14px 15px;color:#3d2d20;box-shadow:0 3px 0 #d0b58a;text-align:center}
.scrap-tape{position:absolute;top:-10px;left:calc(50% - 38px);width:76px;height:23px;background:#c9b5a0;opacity:.85;transform:rotate(-3deg);border-left:1px dashed #a38d75;border-right:1px dashed #a38d75}
.scrap-tag{position:absolute;top:8px;right:8px;padding:4px 6px;background:#c6533b;color:#fff5e9;font:8px monospace;transform:rotate(5deg)}
.scrap-kicker{font:8px monospace;letter-spacing:1px;color:#a43f2c;text-transform:uppercase}
.scrap-photo{display:flex;align-items:center;justify-content:center;margin:13px auto 14px;padding:7px 7px 17px;background:#fffdf7;border:0;box-shadow:0 3px 5px #c7b08c;transform:rotate(2deg);min-width:130px;min-height:145px}
.scrap-photo img,.photo-placeholder{width:115px;height:115px;object-fit:cover;display:grid;place-items:center;background:linear-gradient(135deg,#d9bba0,#ecd5b8 50%,#8a9b8c);color:#fff9eb;font:34px Georgia,serif}
.scrap-paper h2{color:#3d2d20;font:italic 500 clamp(24px,4vw,36px)/1.1 Georgia,serif;margin:10px 0}
.scrap-note{color:#684b32;font:italic 13px/1.6 Georgia,serif;border-top:1px dashed #c3a77d;padding-top:10px;margin:9px 0;white-space:pre-wrap;overflow-wrap:anywhere}
.scrap-bottom{font:8px monospace;color:#8e7150;letter-spacing:1px;margin-top:12px}
.webcore-device{border:2px solid #ff62c9;border-radius:2px;background:#14142b;color:#fff;box-shadow:5px 5px #69ead3;overflow:hidden}
.web-browser-bar{background:#dbd5ff;color:#24203f;display:flex;gap:5px;align-items:center;padding:8px 9px;font:9px monospace;border-bottom:2px solid #ff62c9}
.web-dot{width:8px;height:8px;border-radius:50%;background:#ff62c9;box-shadow:12px 0 #f4d35e,24px 0 #69ead3;margin-right:20px;flex:0 0 8px}
.web-window-label{flex:1;overflow:hidden;white-space:nowrap;text-overflow:ellipsis}
.web-browser-bar button{width:25px;height:23px;padding:0;background:#bdb4f5;color:#211e40;border:1px solid #8073cf}
.web-screen{padding:17px 14px 15px;background:radial-gradient(circle at 50% 10%,#34336d 0,#17172e 55%,#101020 100%);position:relative}
.web-badge{display:inline-block;padding:4px 7px;background:#69ead3;color:#18172e;font:900 8px monospace;letter-spacing:1px;transform:rotate(-2deg)}
.web-kicker{color:#69ead3;font:8px monospace;letter-spacing:1.3px;margin-top:12px}
.web-screen h2{color:#ff8cdb;font:700 clamp(24px,3.5vw,36px)/1.1 Arial,sans-serif;text-transform:uppercase;letter-spacing:-1px;text-shadow:3px 3px #5c4bc3;margin:10px 0}
.web-screen .device-meta{color:#e4d8ff}
.web-art{display:flex;gap:4px;align-items:center;justify-content:center;height:65px;margin:12px 0;border:1px solid #52448d;background:#1c1c3d;overflow:hidden}
.equalizer-bar{width:6px;flex:0 0 6px;border-radius:3px 3px 0 0;background:linear-gradient(#ff62c9,#806aff,#69ead3)}
.webcore-device.is-playing .equalizer-bar{animation:eq 1s ease-in-out infinite alternate}
.equalizer-bar:nth-child(3n){animation-delay:-.4s}.equalizer-bar:nth-child(3n + 1){animation-delay:-.7s}
.web-note{color:#d9d0ff;border-top:1px dashed #6357a3;padding-top:10px;margin:9px 0;font:italic 12px/1.5 Arial,sans-serif;white-space:pre-wrap;overflow-wrap:anywhere}
@keyframes eq{from{transform:scaleY(.25);opacity:.6}to{transform:scaleY(1);opacity:1}}
.device-status{margin-top:7px;font:8px monospace;letter-spacing:.8px;color:#867a69;text-transform:uppercase}
.device-status[hidden]{display:none}
@media(max-width:520px){.player-shell{padding:5px;gap:8px}.cd-layout{grid-template-columns:minmax(100px,.9fr) minmax(0,1.1fr);gap:9px}.cd-copy h2{font-size:21px}.cd-dedication{font-size:11px}.cd-disc{width:100%}.cassette-reel{width:55px;height:55px}.cassette-reel span{inset:14px}.ipod-device{padding:14px}.ipod-wheel{width:145px;height:145px}.player-status-line{padding:8px}.common-controls button,.tracklist-toggle,.haptic-toggle{padding:8px}}
@media(prefers-reduced-motion:reduce){.cd-disc,.cassette-device.is-playing .cassette-reel,.webcore-device.is-playing .equalizer-bar{animation:none!important}}
</style>
</head><body>
<div class="player-shell @@PLAYER_THEME@@">
  @@DEVICE_MARKUP@@
  <div class="player-status-line"><span id="nowPlayingLabel"></span><span id="playerStatus">Preparing player…</span><span id="trackCounter"></span></div>
  <div class="common-controls">
    <button data-action="toggle-tracklist" class="tracklist-toggle" id="tracklistToggle">TRACKLIST</button>
    <button data-action="previous" id="prevGlobal">◀ PREV</button>
    <button data-action="toggle-play" data-play-label id="globalPlay">▶ PLAY</button>
    <button data-action="next" id="nextGlobal">NEXT ▶</button>
    <button data-action="toggle-haptics" class="haptic-toggle" id="hapticToggle">HAPTICS ON</button>
  </div>
  <div class="tracklist-panel" id="tracklistPanel" hidden>@@TRACKLIST_MARKUP@@</div>
  <div class="player-video"><div id="ytplayer"></div></div>
  <div class="playback-note" id="playbackNote"></div>
</div>
<script>
const songs = @@TRACKS_JSON@@;
const labels = @@LABELS_JSON@@;
const skin = "@@SKIN@@";
let current = 0;
let player = null;
let ready = false;
let playing = false;
let hapticsEnabled = true;
try {
  if (window.parent && window.parent.__mixtapeHapticsEnabled === false) hapticsEnabled = false;
} catch (error) {}
let apiLoadStarted = false;

function pulseHaptic(duration) {
  try {
    const host = window.parent;
    if (host && host !== window && host.navigator && typeof host.navigator.vibrate === 'function') {
      const result = host.navigator.vibrate(duration);
      if (result !== false) return true;
    }
  } catch (error) {}
  try {
    if (navigator.vibrate) return navigator.vibrate(duration) !== false;
  } catch (error) {}
  return false;
}
function haptic() {
  if (!hapticsEnabled) return;
  pulseHaptic(10);
}
function setStatus(message) {
  const status = document.getElementById('playerStatus');
  if (status) status.textContent = message;
}
function refresh() {
  const track = songs[current];
  const titleText = track ? track.title : 'Add a track to begin';
  const trackTitle = document.getElementById('ipodTrackTitle');
  if (trackTitle) trackTitle.textContent = titleText;
  document.getElementById('nowPlayingLabel').textContent = labels.nowPlaying;
  document.getElementById('trackCounter').textContent = songs.length ? String(current + 1).padStart(2,'0') + ' / ' + String(songs.length).padStart(2,'0') : '00 / 00';
  document.getElementById('playbackNote').textContent = labels.playbackNote;
  document.querySelectorAll('[data-play-label]').forEach(function(button) {
    button.textContent = playing ? labels.pause : labels.play;
  });
  const ipodIcon = document.querySelector('[data-role="ipod-play-icon"]');
  if (ipodIcon) ipodIcon.textContent = playing ? 'Ⅱ' : '▶';
  const device = document.getElementById('devicePanel');
  if (device) {
    device.classList.toggle('is-playing', playing);
  }
  const ipodStatus = document.getElementById('ipodPlayStatus');
  if (ipodStatus) ipodStatus.textContent = playing ? 'PLAYING' : (ready ? 'PAUSED' : 'READY');
  const cassetteStatus = document.getElementById('cassetteStatus');
  if (cassetteStatus) cassetteStatus.textContent = playing ? 'PLAYING · REELS IN MOTION' : 'PAUSED · TAPE AT REST';
  const previousDisabled = !ready || songs.length < 2;
  const nextDisabled = !ready || songs.length < 2;
  document.querySelectorAll('[data-action="previous"]').forEach(function(button) { button.disabled = previousDisabled; });
  document.querySelectorAll('[data-action="next"]').forEach(function(button) { button.disabled = nextDisabled; });
  document.querySelectorAll('[data-action="toggle-play"],[data-action="stop"],[data-action="select-track"]').forEach(function(button) { button.disabled = !ready || !songs.length; });
  const statusText = !songs.length ? 'Add YouTube tracks above' : (!ready ? 'Loading YouTube player…' : (playing ? 'PLAYING' : 'READY'));
  if (!document.getElementById('playerStatus').textContent.startsWith('YouTube error')) setStatus(statusText);
  const trackButtons = document.querySelectorAll('.track-pick');
  trackButtons.forEach(function(button, index) { button.setAttribute('aria-current', index === current ? 'true' : 'false'); });
  const caseButton = document.getElementById('caseButton');
  if (caseButton) caseButton.textContent = document.getElementById('cdCase').classList.contains('is-open') ? 'CLOSE CASE' : 'OPEN CASE';
  const caseNote = document.getElementById('caseOpenNote');
  if (caseNote) caseNote.hidden = !document.getElementById('cdCase').classList.contains('is-open');
  const hapticButton = document.getElementById('hapticToggle');
  if (hapticButton) hapticButton.textContent = hapticsEnabled ? 'HAPTICS ON' : 'HAPTICS OFF';
}
function selectTrack(index, autoPlay) {
  if (!ready || !player || !songs.length) {
    setStatus('YouTube player is still loading');
    return;
  }
  current = (index + songs.length) % songs.length;
  player.loadVideoById(songs[current].id);
  playing = true;
  refresh();
  if (autoPlay !== false) setStatus('Loading ' + songs[current].title);
}
function togglePlay() {
  if (!ready || !player || !songs.length) {
    setStatus(songs.length ? 'YouTube player is still loading' : 'Add at least one track first');
    return;
  }
  if (playing) player.pauseVideo();
  else player.playVideo();
}
function stopPlayback() {
  if (!ready || !player || !songs.length) {
    setStatus('Player is not ready yet');
    return;
  }
  player.pauseVideo();
  player.seekTo(0, true);
  playing = false;
  refresh();
  setStatus('STOPPED · AT THE START OF THE TRACK');
}
function toggleTracklist() {
  const panel = document.getElementById('tracklistPanel');
  const hidden = panel.hasAttribute('hidden');
  if (hidden) panel.removeAttribute('hidden');
  else panel.setAttribute('hidden', '');
  document.getElementById('tracklistToggle').textContent = hidden ? 'HIDE TRACKLIST' : 'TRACKLIST';
  setStatus(hidden ? 'Choose a track from the list' : 'Tracklist closed');
}
function doAction(action, button) {
  if (action !== 'toggle-haptics') haptic();
  if (action === 'toggle-play') togglePlay();
  else if (action === 'previous') selectTrack(current - 1, true);
  else if (action === 'next') selectTrack(current + 1, true);
  else if (action === 'stop') stopPlayback();
  else if (action === 'select-track') selectTrack(Number(button.getAttribute('data-index')) || 0, true);
  else if (action === 'toggle-tracklist') toggleTracklist();
  else if (action === 'toggle-haptics') {
    hapticsEnabled = !hapticsEnabled;
    try { window.parent.__mixtapeHapticsEnabled = hapticsEnabled; } catch (error) {}
    if (hapticsEnabled) pulseHaptic(8);
    refresh();
    setStatus(hapticsEnabled ? 'Haptic feedback enabled where supported' : 'Haptic feedback turned off');
  }
  else if (action === 'eject') {
    const caseElement = document.getElementById('cdCase');
    caseElement.classList.toggle('is-open');
    refresh();
    setStatus(caseElement.classList.contains('is-open') ? 'CASE OPEN' : 'CASE CLOSED');
  }
}
document.addEventListener('click', function(event) {
  const button = event.target.closest('button[data-action]');
  if (!button || button.disabled) return;
  doAction(button.getAttribute('data-action'), button);
});
document.addEventListener('keydown', function(event) {
  if (event.key !== 'Enter' && event.key !== ' ') return;
  const target = event.target;
  if (target && target.matches && target.matches('button[data-action]')) {
    event.preventDefault();
    target.click();
  }
});
function createPlayer() {
  if (!window.YT || !window.YT.Player || player || !songs.length) return;
  apiLoadStarted = true;
  player = new YT.Player('ytplayer', {
    width:'100%', height:'300', videoId:songs[current].id,
    playerVars:{playsinline:1, rel:0, modestbranding:1, controls:1},
    events:{
      onReady:function() {
        ready = true;
        refresh();
        setStatus('READY · ' + songs[current].title);
      },
      onStateChange:function(event) {
        playing = event.data === YT.PlayerState.PLAYING;
        refresh();
        if (event.data === YT.PlayerState.PLAYING) setStatus('PLAYING · ' + songs[current].title);
        else if (event.data === YT.PlayerState.PAUSED) setStatus('PAUSED · ' + songs[current].title);
        else if (event.data === YT.PlayerState.ENDED) {
          if (current < songs.length - 1) selectTrack(current + 1, true);
          else {
            playing = false;
            refresh();
            setStatus('MIXTAPE FINISHED');
          }
        }
      },
      onError:function() {
        ready = false;
        setStatus('YouTube error · try another video');
        refresh();
      }
    }
  });
}
if (songs.length) {
  const script = document.createElement('script');
  script.src = 'https://www.youtube.com/iframe_api';
  script.onload = function() { createPlayer(); };
  document.head.appendChild(script);
  window.onYouTubeIframeAPIReady = createPlayer;
} else {
  document.getElementById('ytplayer').innerHTML = '<div style="padding:24px;color:#746b5f;text-align:center;font:12px Arial">Add a valid YouTube URL to enable playback.</div>';
  setStatus('Add YouTube tracks above');
  refresh();
}
refresh();
</script></body></html>""";

    component_html = (
        template.replace("@@PLAYER_THEME@@", theme_class)
        .replace("@@DEVICE_MARKUP@@", device_markup)
        .replace("@@TRACKS_JSON@@", tracks_json)
        .replace("@@LABELS_JSON@@", labels_json)
        .replace("@@TRACKLIST_MARKUP@@", tracklist_markup)
        .replace("@@SKIN@@", skin.replace('"', ''))
    )
    components.html(component_html, height=970, scrolling=True)

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
    render_interactive_player({**incoming, "copy": copy}, copy, "recipient")
    footer_text = str(copy.get("footer_text", DEFAULT_COPY["footer_text"])).strip()
    if footer_text:
        st.markdown('<div class="footer">' + html.escape(footer_text) + '</div>', unsafe_allow_html=True)
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
            skin = st.selectbox("Player style", ["CD player", "Cassette tape", "iPod classic", "Scrapbook", "Webcore"])

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
            copy_values["burning_text"] = st.text_input("Burn animation headline", max_chars=100, key="copy_burning_text", on_change=sync_copy_value, args=("burning_text",))
            copy_values["burn_complete_text"] = st.text_input("Burn animation subtitle", max_chars=180, key="copy_burn_complete_text", on_change=sync_copy_value, args=("burn_complete_text",))
            copy_values["footer_text"] = st.text_input("Footer text", max_chars=180, key="copy_footer_text", on_change=sync_copy_value, args=("footer_text",))
            st.session_state["copy_values"] = copy_values

        with st.container(border=True):
            st.markdown(f'<div class="section-title">02 / {html.escape(str(copy_values["tracklist_heading"]))}</div>', unsafe_allow_html=True)
            st.caption("Paste YouTube links or 11-character video IDs. Up to 20 tracks.")
            if "track_count" not in st.session_state:
                st.session_state["track_count"] = 0

            count = int(st.session_state["track_count"])
            add_col, remove_col, count_col = st.columns([1, 1, 1.2])
            with add_col:
                if st.button("＋ Add track", use_container_width=True, disabled=count >= 20, key="add_track_button"):
                    st.session_state["track_count"] = min(count + 1, 20)
                    st.rerun()
            with remove_col:
                if st.button("− Remove last", use_container_width=True, disabled=count <= 0, key="remove_track_button"):
                    st.session_state["track_count"] = max(count - 1, 0)
                    st.rerun()
            with count_col:
                st.caption(f"{count} / 20 tracks")

            tracks = []
            defaults = ["A song for the long way home", "The one that reminds me of you", "Track three"]
            if count == 0:
                st.caption("Your tracklist is empty. Press **Add track** to add a song.")
            else:
                for i in range(count):
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
            valid_tracks = mix["tracks"]
            st.caption(f"{len(valid_tracks)} valid YouTube track(s)")
            render_interactive_player(mix, copy_values, "preview")

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
                render_burn_animation(copy_values)
                st.success("Your mixtape is ready to share.")
                if share_url:
                    st.code(share_url, language=None)
                    st.link_button(str(copy_values.get("share_button_label", DEFAULT_COPY["share_button_label"])), share_url, use_container_width=True)
                else:
                    st.info("Deploy the app publicly to generate a shareable link.")
                st.caption("The mixtape details are encoded in the URL, so no database is needed. Very long mixtapes can create long links.")

if not incoming and str(copy_values.get("footer_text", DEFAULT_COPY["footer_text"])).strip():
    st.markdown('<div class="footer">' + html.escape(str(copy_values["footer_text"])) + '</div>', unsafe_allow_html=True)

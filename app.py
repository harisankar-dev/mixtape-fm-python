import base64, json, zlib, html
from urllib.parse import quote
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="mixtape.fm", page_icon="♫", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;700&family=Playfair+Display:ital,wght@0,500;1,500&display=swap');
.stApp{background:#f3eee4;color:#201e1a}.block-container{max-width:1100px;padding-top:2rem}
.brand{display:flex;justify-content:space-between;border-bottom:1px solid #201e1a;padding-bottom:16px}
.brand b{font:700 24px 'DM Sans';letter-spacing:-1px}.brand span{color:#d94b36}
.hero{padding:28px 0}.eyebrow{font:11px 'DM Mono';letter-spacing:2px;color:#d94b36;text-transform:uppercase}
.hero h1{font:500 clamp(42px,7vw,76px)/.98 'Playfair Display';letter-spacing:-2px}.hero em{color:#d94b36}.hero p{max-width:560px;color:#625d54;line-height:1.7}
.panel{background:#faf7f0;border:1px solid #d7cfc1;border-radius:4px;padding:20px;margin-bottom:18px}
.player{background:#26231f;color:#f4eddf;border:1px solid #37332d;border-radius:8px;text-align:center;padding:28px 18px;margin-bottom:18px}
.player h2{font:500 clamp(26px,4vw,42px) 'Playfair Display';color:#f4eddf}.player .kicker{font:10px 'DM Mono';letter-spacing:2px;color:#e68a70}
.ipod{background:#c5c8c5;color:#20231f;border:7px solid #e3e4e0}.scrapbook{background:#e8d7b9;color:#34291e;border:2px dashed #9e7f58}.webcore{background:#17172c;border:2px solid #ff67c4;box-shadow:5px 5px #77e6d0}.webcore h2{color:#ff9edc}
.stButton>button{border-radius:2px;background:#201e1a;color:#fff8ee;border:1px solid #201e1a;font:12px 'DM Mono';letter-spacing:1px}
.stButton>button:hover{background:#d94b36;color:white;border-color:#d94b36}
.track{border-bottom:1px solid #d7cfc1;padding:10px;font:13px 'DM Sans'}
</style>
<div class="brand"><b>mixtape<span>.</span>fm</b><span class="eyebrow">A little music, sent with feeling</span></div>
""", unsafe_allow_html=True)

def yt_id(url):
    url=(url or "").strip()
    for marker in ("youtu.be/","youtube.com/watch?v=","youtube.com/embed/","youtube.com/shorts/"):
        if marker in url:
            return url.split(marker,1)[1].split("&",1)[0].split("?",1)[0].split("/",1)[0]
    return url if len(url)==11 and "/" not in url else ""

def encode_mix(m):
    raw=json.dumps(m,ensure_ascii=False,separators=(",",":")).encode()
    return base64.urlsafe_b64encode(zlib.compress(raw,9)).decode().rstrip("=")

def decode_mix(v):
    try:
        data=json.loads(zlib.decompress(base64.urlsafe_b64decode(v+"="*(-len(v)%4))))
        if isinstance(data,dict) and isinstance(data.get("tracks"),list):
            return data
    except Exception:
        return None
    return None

def player(m):
    css={"CD player":"","iPod classic":"ipod","Scrapbook":"scrapbook","Webcore":"webcore"}.get(m.get("skin","CD player"),"")
    title=html.escape(str(m.get("title","a little mixtape for you")))
    sender=html.escape(str(m.get("sender",""))); recipient=html.escape(str(m.get("recipient","")))
    note=html.escape(str(m.get("note","")))
    cover=str(m.get("cover",""))
    art=f'<img src="{html.escape(cover,quote=True)}" style="width:150px;height:150px;object-fit:cover;border-radius:4px">' if cover.startswith(("https://","http://")) else '<div style="margin:22px auto;width:145px;height:145px;border-radius:50%;background:repeating-radial-gradient(circle,#45413a 0 5px,#201e1a 6px 10px);display:grid;place-items:center"><div style="background:#d94b36;color:white;border-radius:50%;width:55px;height:55px;display:grid;place-items:center;font:10px monospace">SIDE A</div></div>'
    st.markdown(f'<div class="player {css}"><div class="kicker">A MIXTAPE, MADE JUST FOR YOU</div><h2>{title}</h2><div>{("FROM "+sender+" · ") if sender else ""}{("FOR "+recipient) if recipient else "PRESS PLAY WHENEVER YOU NEED IT"}</div>{art}<p style="white-space:pre-wrap;font-style:italic">{note}</p></div>',unsafe_allow_html=True)
    tracks=m.get("tracks",[])
    if not tracks:
        st.info("No valid YouTube tracks in this mixtape.")
        return
    labels=[f"{i+1:02d} · {t.get('title') or 'Untitled track'}" for i,t in enumerate(tracks)]
    choice=st.selectbox("TRACKLIST",labels,key="recipient_track")
    track=tracks[labels.index(choice)]; vid=yt_id(track.get("url",""))
    if vid:
        components.html(f'<iframe width="100%" height="315" src="https://www.youtube-nocookie.com/embed/{vid}?rel=0" title="YouTube player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen style="border-radius:8px"></iframe>',height=330)
    for i,t in enumerate(tracks):
        st.markdown(f'<div class="track"><span style="color:#d94b36">{i+1:02d}</span> &nbsp; {html.escape(str(t.get("title","Untitled track")))}</div>',unsafe_allow_html=True)

incoming=decode_mix(st.query_params.get("mix","")) if st.query_params.get("mix") else None
if incoming:
    st.markdown('<div class="hero"><div class="eyebrow">A little something for you</div><h1>Someone made you<br><em>a mixtape.</em></h1><p>Put your headphones on. Take your time.</p></div>',unsafe_allow_html=True)
    player(incoming)
    if st.button("MAKE YOUR OWN MIXTAPE"):
        st.query_params.clear(); st.rerun()
else:
    st.markdown('<div class="hero"><div class="eyebrow">Digital mixtapes for the people you love</div><h1>Some things are better<br><em>said in songs.</em></h1><p>Pick the songs, write the note you can’t quite say out loud, and send someone a little piece of your world.</p></div>',unsafe_allow_html=True)
    left,right=st.columns([1.05,.95],gap="large")
    with left:
        st.markdown('<div class="panel"><div class="eyebrow">01 / THE DEDICATION</div>',unsafe_allow_html=True)
        title=st.text_input("MIXTAPE TITLE","a little mixtape for you",max_chars=100)
        a,b=st.columns(2)
        sender=a.text_input("FROM",placeholder="your name",max_chars=80)
        recipient=b.text_input("FOR",placeholder="their name",max_chars=80)
        note=st.text_area("THE NOTE","some songs that made me think of you.",max_chars=500)
        cover=st.text_input("COVER IMAGE URL (OPTIONAL)",placeholder="https://...")
        skin=st.selectbox("CHOOSE YOUR PLAYER",["CD player","iPod classic","Scrapbook","Webcore"])
        st.markdown('</div><div class="panel"><div class="eyebrow">02 / THE TRACKLIST</div>',unsafe_allow_html=True)
        count=st.number_input("NUMBER OF TRACKS",min_value=1,max_value=20,value=3,step=1)
        tracks=[]
        for i in range(int(count)):
            with st.container(border=True):
                x,y=st.columns(2)
                defaults=["A song for the long way home","The one that reminds me of you","Track three"]
                t=x.text_input(f"TRACK {i+1:02d} TITLE",value=defaults[i] if i<3 else f"Track {i+1}",key=f"title{i}",max_chars=120)
                u=y.text_input("YOUTUBE URL / ID",key=f"url{i}",placeholder="youtube.com/watch?v=...")
                tracks.append({"title":t,"url":u})
        st.markdown('</div>',unsafe_allow_html=True)
    with right:
        st.markdown('<div class="eyebrow">03 / A LITTLE PREVIEW</div>',unsafe_allow_html=True)
        mix={"title":title,"sender":sender,"recipient":recipient,"note":note,"cover":cover,"skin":skin,"tracks":[t for t in tracks if yt_id(t["url"])]}
        player(mix)
        st.caption(f"{len(mix['tracks'])} valid YouTube track(s)")
        if st.button("BURN THIS MIXTAPE ↗",use_container_width=True):
            if not mix["tracks"]:
                st.warning("Add at least one valid YouTube URL or video ID first.")
            else:
                st.session_state["share_payload"]=encode_mix(mix)
        if st.session_state.get("share_payload"):
            base=st.context.url.split("?",1)[0]
            url=f"{base}?mix={quote(st.session_state['share_payload'])}"
            st.success("Your mixtape is ready to share.")
            st.code(url,language=None)
            st.link_button("OPEN / SHARE MIXTAPE",url,use_container_width=True)
            st.caption("The mixtape is encoded into the URL; no database required. Long mixes can produce long links.")
st.markdown('<div style="border-top:1px solid #201e1a;padding-top:14px;margin-top:35px;font:10px monospace;letter-spacing:1px;color:#777064">MADE WITH FEELING · NO DATABASE REQUIRED · MUSIC PLAYS THROUGH YOUTUBE</div>',unsafe_allow_html=True)

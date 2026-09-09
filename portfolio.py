#!/usr/bin/env python3
"""Editable, deployment-ready portfolio website for Yuvraj Singh."""

import html
import http.server
import json
import mimetypes
import os
import socketserver

PORT = int(os.environ.get("PORT", "8000"))
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "change-me")
DATA_FILE = os.path.join(os.path.dirname(__file__), "portfolio_data.json")

SITE_CONFIG = {
    "config_version": 2,
    "brand": {
        "name": "Yuvraj Singh",
        "monogram": "YS",
        "tag": "DIGITAL DEVELOPER UNIVERSE",
        "cta": "Let's connect",
        "github": "https://github.com/YuvrajSingh-2006/python-coder",
        "linkedin": "https://www.linkedin.com/in/yuvraj-singh-123uv",
        "email": "yuvrajsingh36024@gmail.com",
    },
    "profile": {"image_url": "/pic.jpeg", "alt": "Yuvraj Singh profile photo"},
    "hero": {
        "eyebrow": "Computer Science & Engineering · Jaipur, India",
        "title": "Building ideas into real digital products.",
        "description": (
            "I am a developer and data & cybersecurity enthusiast focused on turning curious questions "
            "into practical software, thoughtful interfaces, and useful experiments."
        ),
        "primary_button": "Explore my work",
        "secondary_button": "Download resume",
        "availability": "Open to opportunities",
    },
    "about": {
        "title": "A builder with a systems mindset.",
        "subtitle": "I enjoy the space where code, data, and human experience meet.",
        "description": (
            "I am a Computer Science & Engineering student who enjoys turning ideas into practical digital "
            "solutions. I work with programming, web development, data analytics, and cybersecurity concepts "
            "while continuously building projects to improve my problem-solving and development skills."
        ),
        "facts": [
            {"label": "Education", "value": "B.Tech · CSE"},
            {"label": "Current stage", "value": "2nd year completed"},
            {"label": "Based in", "value": "Jaipur, India"},
        ],
        "stats": [
            {"value": "02+", "label": "Hackathons"},
            {"value": "∞", "label": "Curiosity"},
            {"value": "01", "label": "Focus: keep building"},
        ],
    },
    "skills": {
        "title": "My toolkit, in orbit.",
        "subtitle": "A growing stack shaped by hands-on projects and deliberate practice.",
        "groups": [
            {"name": "Programming", "items": ["Python", "C", "C++", "Java", "SQL"]},
            {"name": "Web", "items": ["HTML", "CSS", "JavaScript", "React", "Node.js"]},
            {"name": "Data", "items": ["Data analysis", "Excel", "Data visualization", "EDA"]},
            {"name": "Security", "items": ["Cybersecurity fundamentals", "Networking", "Linux"]},
            {"name": "Databases", "items": ["MongoDB", "MySQL"]},
        ],
    },
    "projects": {
        "title": "Selected experiments.",
        "subtitle": "Real projects from my workspace — small, useful, and always teaching me something new.",
        "items": [
            {
                "title": "Portfolio Website",
                "description": "A server-rendered personal portfolio with an editable content API and a premium interactive interface.",
                "category": "Web",
                "year": "2026",
                "image": "/pic3.jpeg",
                "url": "#contact",
            },
            {
                "title": "WhatsApp Automation",
                "description": "A Python automation experiment for scheduling and simplifying repeat communication tasks.",
                "category": "Automation",
                "year": "2025",
                "image": "/pic2.jpeg",
                "url": "#contact",
            },
            {
                "title": "Python ML Demo",
                "description": "A compact machine-learning experiment exploring model-based learning concepts and Python workflows.",
                "category": "Data / ML",
                "year": "2025",
                "image": "/pic.jpeg",
                "url": "#contact",
            },
            {
                "title": "Java Coding Blocks",
                "description": "A Java practice project focused on core programming concepts and beginner-friendly examples.",
                "category": "Java",
                "year": "2024",
                "image": "/pic2.jpeg",
                "url": "#contact",
            },
        ],
    },
    "timeline": [
        {
            "period": "Now",
            "title": "Building in public",
            "description": "Exploring software development, data analytics, and cybersecurity through practical projects.",
        },
        {
            "period": "Education",
            "title": "B.Tech in Computer Science & Engineering",
            "description": "2nd year completed, with a focus on strengthening fundamentals through consistent practice.",
        },
    ],
    "certificates": [],
    "contact": {
        "title": "Let's make the next thing useful.",
        "subtitle": "Have an idea, opportunity, or problem worth exploring? My inbox is open.",
        "message": "I am currently interested in software development, data analytics, cybersecurity, and placement opportunities.",
    },
}


def load_site_config():
    if not os.path.isfile(DATA_FILE):
        return
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as data_file:
            saved_config = json.load(data_file)
        if isinstance(saved_config, dict) and saved_config.get("config_version") == 2:
            def merge_defaults(defaults, saved):
                merged = defaults.copy()
                for key, value in saved.items():
                    if isinstance(value, dict) and isinstance(merged.get(key), dict):
                        merged[key] = merge_defaults(merged[key], value)
                    else:
                        merged[key] = value
                return merged

            defaults = SITE_CONFIG.copy()
            SITE_CONFIG.clear()
            SITE_CONFIG.update(merge_defaults(defaults, saved_config))
    except (OSError, json.JSONDecodeError):
        print("Warning: portfolio_data.json could not be loaded; using defaults.")


def save_site_config(config):
    temporary_file = DATA_FILE + ".tmp"
    with open(temporary_file, "w", encoding="utf-8") as data_file:
        json.dump(config, data_file, indent=2, ensure_ascii=False)
    os.replace(temporary_file, DATA_FILE)


load_site_config()


def esc(value):
    return html.escape(str(value), quote=True)


def render_stats(items):
    return "".join(
        f'<div class="stat"><strong>{esc(item["value"])}</strong><span>{esc(item["label"])}</span></div>'
        for item in items
    )


def render_facts(items):
    return "".join(
        f'<div class="fact"><span>{esc(item["label"])}</span><strong>{esc(item["value"])}</strong></div>'
        for item in items
    )


def render_skill_groups(groups):
    return "".join(
        f'<article class="skill-group reveal"><div class="skill-index">0{index}</div>'
        f'<h3>{esc(group["name"])}</h3><div class="skill-list">'
        + "".join(f'<span>{esc(item)}</span>' for item in group["items"])
        + "</div></article>"
        for index, group in enumerate(groups, 1)
    )


def render_projects(items):
    cards = []
    for item in items:
        image = esc(item.get("image", ""))
        cards.append(
            f'''<article class="project-card reveal" data-category="{esc(item["category"])}">
              <div class="project-image" style="background-image: linear-gradient(135deg, rgba(7,12,26,.12), rgba(7,12,26,.8)), url('{image}')">
                <span class="project-year">{esc(item["year"])}</span>
                <span class="project-arrow">↗</span>
              </div>
              <div class="project-body"><div class="project-category">{esc(item["category"])}</div>
                <h3>{esc(item["title"])}</h3><p>{esc(item["description"])}</p>
                <a href="{esc(item.get("url", "#contact"))}" class="text-link">View case study <span>→</span></a>
              </div>
            </article>'''
        )
    return "".join(cards)


def render_timeline(items):
    if not items:
        return '<p class="empty-state">Timeline details will be added as the journey grows.</p>'
    return "".join(
        f'''<article class="timeline-item reveal"><div class="timeline-marker"></div>
          <div class="timeline-period">{esc(item["period"])}</div><div><h3>{esc(item["title"])}</h3>
          <p>{esc(item["description"])}</p></div></article>'''
        for item in items
    )


def render_certificates(items):
    if not items:
        return '<div class="empty-state"><span class="empty-icon">+</span><strong>Verified credentials coming soon.</strong><p>No certificates are listed yet. This space will only contain confirmed achievements.</p></div>'
    return "".join(
        f'<div class="credential reveal"><span>✦</span><div><strong>{esc(item["title"])}</strong><small>{esc(item.get("issuer", ""))}</small></div></div>'
        for item in items
    )


def admin_page():
    config_json = json.dumps(SITE_CONFIG, ensure_ascii=False).replace("</", "<\\/")
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1"><title>Portfolio Control Panel</title>
    <style>body{{margin:0;padding:40px;background:#080b14;color:#f5f7fb;font:16px/1.5 Segoe UI,sans-serif}}
    main{{width:min(1000px,100%);margin:auto}}textarea,input{{width:100%;box-sizing:border-box;padding:12px;margin:8px 0 20px;background:#111827;color:#fff;border:1px solid #27334e;border-radius:8px}}
    textarea{{min-height:520px;font:13px Consolas,monospace}}button,a{{padding:12px 18px;border:0;border-radius:8px;background:#b8f36b;color:#111;font-weight:700;text-decoration:none;cursor:pointer}}
    #status{{min-height:24px;color:#b8f36b}}</style></head><body><main><h1>Portfolio Control Panel</h1>
    <p>Edit the JSON below, then save it. Changes are stored in <strong>portfolio_data.json</strong>.</p>
    <label>Admin token<input id="token" type="password" placeholder="ADMIN_TOKEN"></label>
    <label>Website content<textarea id="config" spellcheck="false"></textarea></label><p id="status"></p>
    <button id="save">Save changes</button> <a href="/" target="_blank" rel="noopener">Open website</a></main>
    <script>const editor=document.getElementById('config'),token=document.getElementById('token'),status=document.getElementById('status');
    editor.value=JSON.stringify({config_json},null,2); token.value=sessionStorage.getItem('portfolioAdminToken')||'';
    document.getElementById('save').onclick=async()=>{{try{{const response=await fetch('/api/config',{{method:'PUT',headers:{{'Content-Type':'application/json','X-Admin-Token':token.value.trim()}},body:editor.value}});const result=await response.json();if(!response.ok)throw new Error(result.error||'Save failed');sessionStorage.setItem('portfolioAdminToken',token.value.trim());status.textContent='Saved successfully.';}}catch(error){{status.textContent=error.message;status.style.color='#ff9c9c';}}}};</script></body></html>"""


def build_page():
    config = SITE_CONFIG
    brand = config["brand"]
    hero = config["hero"]
    about = config["about"]
    contact = config["contact"]
    template = """<!doctype html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
  <title>__NAME__ — Digital Developer Universe</title>
  <meta name="description" content="__DESCRIPTION__">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
    :root{--bg:#080b14;--surface:#101522;--surface-2:#151c2d;--text:#f5f7fb;--muted:#8994a8;--line:rgba(255,255,255,.1);--lime:#c6f36b;--cyan:#67e8f9;--violet:#a78bfa;--shadow:0 24px 80px rgba(0,0,0,.3)}
    [data-theme="light"]{--bg:#eef2f7;--surface:#fff;--surface-2:#e4eaf2;--text:#101827;--muted:#526078;--line:rgba(16,24,39,.12);--shadow:0 24px 70px rgba(53,69,95,.15)}
    *{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--text);font:15px/1.65 Manrope,Arial,sans-serif;overflow-x:hidden}
    body:before{content:"";position:fixed;inset:0;z-index:-2;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:52px 52px;mask-image:linear-gradient(to bottom,black,transparent 75%)}
    body:after{content:"";position:fixed;inset:-30%;z-index:-3;background:radial-gradient(circle at 14% 10%,rgba(167,139,250,.15),transparent 25%),radial-gradient(circle at 85% 12%,rgba(103,232,249,.1),transparent 20%);pointer-events:none}
    a{color:inherit;text-decoration:none}.container{width:min(1160px,calc(100% - 48px));margin:auto}.mono,.eyebrow,.section-kicker,.project-category,.project-year,.timeline-period,.skill-index{font-family:"DM Mono",monospace}
    .site-header{position:sticky;top:14px;z-index:20}.nav{min-height:68px;border:1px solid var(--line);border-radius:18px;background:color-mix(in srgb,var(--surface) 80%,transparent);backdrop-filter:blur(18px);display:flex;align-items:center;gap:22px;padding:10px 12px 10px 16px;transition:.3s}
    .site-header.scrolled .nav{min-height:56px;border-radius:14px}.brand{display:flex;align-items:center;gap:10px;font-weight:800;letter-spacing:.06em;white-space:nowrap}.brand-mark{display:grid;place-items:center;width:38px;height:38px;border-radius:11px;background:var(--lime);color:#111827;font-size:13px}.brand small{display:block;color:var(--muted);font:10px "DM Mono";letter-spacing:.12em}
    .nav-links{display:flex;gap:19px;margin-left:auto;color:var(--muted);font-size:13px}.nav-links a{transition:.2s}.nav-links a:hover,.nav-links a.active{color:var(--text)}.nav-tools{display:flex;gap:8px;align-items:center}.icon-btn,.menu-btn{width:38px;height:38px;border:1px solid var(--line);border-radius:10px;background:transparent;color:var(--text);cursor:pointer}.nav-cta{padding:10px 15px;border-radius:10px;background:var(--text);color:var(--bg);font-weight:800;font-size:13px}
    .hero{min-height:calc(100vh - 100px);display:grid;grid-template-columns:1fr .86fr;align-items:center;gap:70px;padding:86px 0 70px}.eyebrow,.section-kicker{color:var(--lime);font-size:11px;letter-spacing:.13em;text-transform:uppercase}.eyebrow:before{content:"";display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--lime);margin-right:10px;box-shadow:0 0 14px var(--lime)}h1{font-size:clamp(3.3rem,7vw,6.6rem);line-height:.93;letter-spacing:-.075em;margin:22px 0}.hero h1 em{font-style:normal;color:var(--muted)}.hero-copy{max-width:620px;color:var(--muted);font-size:17px}.actions{display:flex;flex-wrap:wrap;gap:12px;margin:30px 0 25px}.btn{display:inline-flex;align-items:center;gap:10px;padding:14px 19px;border-radius:10px;border:1px solid var(--line);font-weight:800;font-size:13px;transition:.25s}.btn:hover{transform:translateY(-3px);border-color:var(--lime)}.btn-primary{background:var(--lime);color:#111827;border-color:var(--lime)}.social-row{display:flex;gap:16px;color:var(--muted);font:12px "DM Mono"}.social-row a:hover{color:var(--lime)}
    .workspace{position:relative;min-height:500px;display:flex;align-items:center;justify-content:center}.workspace:before{content:"";position:absolute;width:360px;height:360px;border:1px solid rgba(198,243,107,.25);border-radius:50%;box-shadow:0 0 100px rgba(198,243,107,.1),inset 0 0 70px rgba(167,139,250,.08);animation:spin 24s linear infinite}.workspace:after{content:"";position:absolute;width:230px;height:230px;border:1px dashed rgba(103,232,249,.3);border-radius:50%;animation:spin 16s linear infinite reverse}.terminal{position:relative;width:min(100%,450px);z-index:2;border:1px solid var(--line);border-radius:16px;background:rgba(13,18,31,.9);box-shadow:var(--shadow);overflow:hidden;transform:rotate(2deg);transition:.35s}.terminal:hover{transform:rotate(0) translateY(-7px)}.terminal-bar{padding:13px 16px;border-bottom:1px solid var(--line);display:flex;gap:7px;align-items:center;color:var(--muted);font:11px "DM Mono"}.dot{width:8px;height:8px;border-radius:50%;background:#ff6b6b}.dot:nth-child(2){background:#f7c948}.dot:nth-child(3){background:var(--lime)}.terminal-title{margin-left:auto}.terminal-body{padding:22px;font:13px/2 "DM Mono";min-height:260px;color:#b9c4d7}.terminal-body .prompt{color:var(--lime)}.terminal-body .value{color:var(--cyan)}.status-card{position:absolute;z-index:3;right:-13px;bottom:35px;background:var(--surface-2);border:1px solid var(--line);border-radius:12px;padding:13px 15px;box-shadow:var(--shadow);font-size:11px}.status-card b{display:block;color:var(--lime);font:10px "DM Mono";text-transform:uppercase;letter-spacing:.08em}.status-card span{display:block;margin-top:4px}.scanline{height:2px;background:var(--lime);box-shadow:0 0 15px var(--lime);animation:scan 4s ease-in-out infinite}
    section{padding:110px 0;scroll-margin-top:85px}.section-head{display:flex;justify-content:space-between;align-items:end;gap:30px;margin-bottom:38px}.section-head h2{font-size:clamp(2rem,4vw,3.5rem);letter-spacing:-.06em;line-height:1;margin:12px 0 0}.section-head p{max-width:440px;color:var(--muted);margin:0}.about-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:20px}.glass{background:color-mix(in srgb,var(--surface) 88%,transparent);border:1px solid var(--line);border-radius:20px;box-shadow:var(--shadow)}.about-card{padding:34px}.about-card p{color:var(--muted);font-size:16px;max-width:680px}.facts{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:32px}.fact{padding-top:15px;border-top:1px solid var(--line)}.fact span{display:block;color:var(--muted);font:11px "DM Mono";text-transform:uppercase}.fact strong{display:block;margin-top:7px;font-size:13px}.stats-card{padding:20px;display:grid;grid-template-columns:1fr 1fr;gap:12px}.stat{padding:22px;border:1px solid var(--line);border-radius:15px;background:rgba(255,255,255,.025)}.stat strong{display:block;font-size:2rem;letter-spacing:-.06em}.stat span{color:var(--muted);font-size:11px}
    .skills-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:12px}.skill-group{padding:22px 18px;min-height:210px;background:var(--surface);border:1px solid var(--line);border-radius:16px;transition:.25s}.skill-group:hover{transform:translateY(-6px);border-color:var(--lime)}.skill-index{color:var(--lime);font-size:11px}.skill-group h3{font-size:16px;margin:27px 0 20px}.skill-list{display:flex;flex-wrap:wrap;gap:7px}.skill-list span{padding:6px 8px;border:1px solid var(--line);border-radius:7px;color:var(--muted);font-size:11px}
    .project-tools{display:flex;gap:7px;flex-wrap:wrap}.filter{border:1px solid var(--line);background:transparent;color:var(--muted);padding:9px 12px;border-radius:8px;font:11px "DM Mono";cursor:pointer}.filter.active,.filter:hover{background:var(--text);color:var(--bg)}.projects-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}.project-card{background:var(--surface);border:1px solid var(--line);border-radius:18px;overflow:hidden;transition:.3s}.project-card:hover{transform:translateY(-6px);box-shadow:var(--shadow)}.project-card.is-hidden{display:none}.project-image{height:225px;background-size:cover;background-position:center;position:relative}.project-year,.project-arrow{position:absolute;top:14px;padding:7px 9px;border:1px solid rgba(255,255,255,.2);border-radius:7px;background:rgba(7,12,26,.6);color:#fff;font-size:10px}.project-year{left:14px}.project-arrow{right:14px;font:16px Manrope}.project-body{padding:22px}.project-category{color:var(--lime);font-size:10px;text-transform:uppercase;letter-spacing:.1em}.project-body h3{font-size:22px;margin:10px 0 8px;letter-spacing:-.04em}.project-body p{color:var(--muted);font-size:13px;min-height:45px}.text-link{display:inline-flex;gap:10px;color:var(--text);font-size:12px;font-weight:800;margin-top:10px}.text-link span{color:var(--lime);transition:.2s}.text-link:hover span{transform:translateX(4px)}
    .journey-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}.timeline,.credentials{padding:30px}.timeline-item{position:relative;display:grid;grid-template-columns:90px 1fr;gap:22px;padding:0 0 28px 20px;border-left:1px solid var(--line)}.timeline-item:last-child{padding-bottom:0}.timeline-marker{position:absolute;left:-5px;top:2px;width:9px;height:9px;border-radius:50%;background:var(--lime);box-shadow:0 0 0 4px var(--bg),0 0 14px var(--lime)}.timeline-period{color:var(--lime);font-size:11px}.timeline-item h3{font-size:17px;margin:0}.timeline-item p{color:var(--muted);font-size:13px;margin:8px 0 0}.credential{display:flex;gap:15px;align-items:flex-start;padding:15px 0;border-bottom:1px solid var(--line)}.credential>span{color:var(--lime);font-size:20px}.credential small{display:block;color:var(--muted);margin-top:3px}.empty-state{border:1px dashed var(--line);border-radius:12px;padding:28px;color:var(--muted);text-align:center}.empty-state strong{display:block;color:var(--text)}.empty-state p{font-size:12px}.empty-icon{display:grid;place-items:center;margin:0 auto 10px;width:34px;height:34px;border:1px solid var(--lime);border-radius:50%;color:var(--lime);font-size:20px}
    .contact{position:relative;overflow:hidden}.contact-box{padding:55px;display:flex;align-items:end;justify-content:space-between;gap:40px;background:linear-gradient(120deg,rgba(198,243,107,.12),rgba(167,139,250,.1)),var(--surface)}.contact-box h2{max-width:650px;margin:10px 0 14px;font-size:clamp(2.2rem,5vw,4.7rem);line-height:.98;letter-spacing:-.07em}.contact-box p{color:var(--muted);max-width:540px}.contact-form{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:28px;max-width:680px}.contact-form input,.contact-form textarea{width:100%;padding:13px;border:1px solid var(--line);border-radius:9px;background:rgba(0,0,0,.12);color:var(--text);font:13px Manrope}.contact-form textarea{grid-column:1/-1;resize:vertical;min-height:100px}.contact-form button{justify-self:start;cursor:pointer}.contact-note{font:11px "DM Mono";color:var(--muted);margin-top:12px}.contact-orbit{width:150px;height:150px;border:1px solid rgba(198,243,107,.45);border-radius:50%;display:grid;place-items:center;color:var(--lime);font:11px "DM Mono";text-align:center;animation:spin 18s linear infinite}.footer{padding:28px 0 45px;color:var(--muted);font:11px "DM Mono";display:flex;justify-content:space-between;border-top:1px solid var(--line)}.reveal{opacity:0;transform:translateY(18px);transition:.7s ease}.reveal.visible{opacity:1;transform:none}@keyframes spin{to{transform:rotate(360deg)}}@keyframes scan{0%,100%{transform:translateY(0);opacity:.2}50%{transform:translateY(250px);opacity:.8}}@media(max-width:900px){.nav-links{display:none}.menu-btn{display:block}.hero{grid-template-columns:1fr;gap:25px;padding-top:70px}.workspace{min-height:400px}.skills-grid{grid-template-columns:repeat(3,1fr)}.about-grid,.journey-grid{grid-template-columns:1fr}}@media(min-width:901px){.menu-btn{display:none}}@media(max-width:620px){.container{width:min(100% - 28px,1160px)}.brand small,.nav-cta{display:none}.hero{padding:55px 0 25px}h1{font-size:clamp(3rem,16vw,5rem)}section{padding:75px 0}.section-head{display:block}.section-head p{margin-top:16px}.facts,.skills-grid,.projects-grid{grid-template-columns:1fr}.workspace{min-height:350px}.workspace:before{width:280px;height:280px}.terminal{transform:none}.status-card{right:0;bottom:15px}.contact-box{padding:28px;display:block}.contact-orbit{margin:30px auto 0}.contact-form{grid-template-columns:1fr}.contact-form textarea{grid-column:auto}.footer{display:block}.footer span{display:block;margin-top:8px}}
  </style>
</head>
<body>
  <header class="site-header"><div class="container nav">
    <a class="brand" href="#home"><span class="brand-mark">__MONOGRAM__</span><span>__NAME__<small>__TAG__</small></span></a>
    <nav class="nav-links" aria-label="Primary navigation">__NAV__</nav>
    <div class="nav-tools"><button class="icon-btn" id="themeToggle" aria-label="Toggle color theme">◐</button><a class="nav-cta" href="#contact">__CTA__</a><button class="menu-btn" id="menuToggle" aria-label="Open navigation">☰</button></div>
  </div></header>
  <main>
    <section class="hero container" id="home"><div class="hero-copy reveal">
      <div class="eyebrow">__EYEBROW__</div><h1>__TITLE__</h1><p>__HERO_DESCRIPTION__</p>
      <div class="actions"><a class="btn btn-primary" href="#projects">__PRIMARY__ <span>↗</span></a><a class="btn" href="/resume.txt" download>__SECONDARY__ <span>↓</span></a></div>
      <div class="social-row"><a href="__GITHUB__" target="_blank" rel="noopener">GitHub ↗</a><a href="__LINKEDIN__" target="_blank" rel="noopener">LinkedIn ↗</a><a href="mailto:__EMAIL__">Email me ↗</a></div>
    </div><div class="workspace reveal"><div class="terminal"><div class="terminal-bar"><i class="dot"></i><i class="dot"></i><i class="dot"></i><span class="terminal-title">yuvraj.dev / system</span></div><div class="scanline"></div><div class="terminal-body"><div><span class="prompt">›</span> initializing yuvraj.dev...</div><div><span class="prompt">›</span> loading projects... <span class="value">done</span></div><div><span class="prompt">›</span> loading skills... <span class="value">done</span></div><div><span class="prompt">›</span> system.status = <span class="value">"READY"</span></div><div><span class="prompt">›</span> available_for_opportunities = <span class="value">true</span></div><br><div><span class="prompt">_</span> <span class="value">build something meaningful</span></div></div></div><div class="status-card"><b>● system online</b><span>open to opportunities</span></div></div></section>
    <section id="about"><div class="container"><div class="section-head"><div><div class="section-kicker">01 / profile</div><h2>__ABOUT_TITLE__</h2></div><p>__ABOUT_SUBTITLE__</p></div><div class="about-grid"><article class="glass about-card reveal"><p>__ABOUT_DESCRIPTION__</p><div class="facts">__FACTS__</div></article><div class="glass stats-card reveal">__STATS__</div></div></div></section>
    <section id="skills"><div class="container"><div class="section-head"><div><div class="section-kicker">02 / capabilities</div><h2>__SKILLS_TITLE__</h2></div><p>__SKILLS_SUBTITLE__</p></div><div class="skills-grid">__SKILLS__</div></div></section>
    <section id="projects"><div class="container"><div class="section-head"><div><div class="section-kicker">03 / project lab</div><h2>__PROJECTS_TITLE__</h2></div><div><p>__PROJECTS_SUBTITLE__</p><div class="project-tools"><button class="filter active" data-filter="all">All</button><button class="filter" data-filter="Web">Web</button><button class="filter" data-filter="Automation">Automation</button><button class="filter" data-filter="Data / ML">Data / ML</button><button class="filter" data-filter="Java">Java</button></div></div></div><div class="projects-grid">__PROJECTS__</div></div></section>
    <section id="experience"><div class="container"><div class="section-head"><div><div class="section-kicker">04 / trajectory</div><h2>Learning in motion.</h2></div><p>A transparent snapshot of where I am and what I am building toward.</p></div><div class="journey-grid"><div class="glass timeline">__TIMELINE__</div><div class="glass credentials" id="certificates"><div class="section-kicker">05 / verified credentials</div><h3>Certificates & achievements</h3>__CERTIFICATES__</div></div></div></section>
    <section id="github"><div class="container"><div class="glass contact-box reveal"><div><div class="section-kicker">06 / open source window</div><h2>See the code behind the interface.</h2><p>Explore my GitHub repository for programming practice, experiments, and the projects that keep this universe moving.</p><a class="btn btn-primary" href="__GITHUB__" target="_blank" rel="noopener">Open GitHub <span>↗</span></a></div><div class="contact-orbit">CODE<br>IS A<br>CRAFT</div></div></div></section>
    <section class="contact" id="contact"><div class="container"><div class="glass contact-box reveal"><div><div class="section-kicker">07 / contact</div><h2>__CONTACT_TITLE__</h2><p>__CONTACT_SUBTITLE__</p><form class="contact-form" id="contactForm"><input id="contactName" placeholder="Your name" required><input id="contactEmail" type="email" placeholder="Your email" required><textarea id="contactMessage" placeholder="Tell me about the idea..." required></textarea><button class="btn btn-primary" type="submit">Send message ↗</button></form><div class="contact-note" id="formStatus">__CONTACT_MESSAGE__</div></div><div class="contact-orbit">LET'S<br>CONNECT</div></div></div></section>
  </main>
  <footer class="container footer"><span>© 2026 __NAME__</span><span>Designed for a bold new version · Jaipur, India</span></footer>
  <script>
    const root=document.documentElement,header=document.querySelector('.site-header'),toggle=document.getElementById('themeToggle');
    const savedTheme=localStorage.getItem('yuvraj-theme'); if(savedTheme) root.dataset.theme=savedTheme;
    toggle.addEventListener('click',()=>{const next=root.dataset.theme==='light'?'dark':'light';root.dataset.theme=next;localStorage.setItem('yuvraj-theme',next)});
    window.addEventListener('scroll',()=>header.classList.toggle('scrolled',window.scrollY>30),{passive:true});
    const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting)entry.target.classList.add('visible')}),{threshold:.12});
    document.querySelectorAll('.reveal').forEach(item=>observer.observe(item));
    document.querySelectorAll('.filter').forEach(button=>button.addEventListener('click',()=>{document.querySelectorAll('.filter').forEach(item=>item.classList.remove('active'));button.classList.add('active');const filter=button.dataset.filter;document.querySelectorAll('.project-card').forEach(card=>card.classList.toggle('is-hidden',filter!=='all'&&card.dataset.category!==filter))}));
    document.getElementById('menuToggle').addEventListener('click',()=>{const nav=document.querySelector('.nav-links');nav.style.display=nav.style.display==='flex'?'none':'flex';nav.style.position='absolute';nav.style.top='76px';nav.style.left='14px';nav.style.right='14px';nav.style.padding='18px';nav.style.border='1px solid var(--line)';nav.style.borderRadius='14px';nav.style.background='var(--surface)'});
    document.getElementById('contactForm').addEventListener('submit',event=>{event.preventDefault();const name=document.getElementById('contactName').value.trim(),email=document.getElementById('contactEmail').value.trim(),message=document.getElementById('contactMessage').value.trim();const subject=encodeURIComponent('Portfolio inquiry from '+name);const body=encodeURIComponent('Name: '+name+'\\nEmail: '+email+'\\n\\n'+message);window.location.href='mailto:__EMAIL__?subject='+subject+'&body='+body;document.getElementById('formStatus').textContent='Opening your mail client…'});
  </script>
</body></html>"""
    replacements = {
        "__NAME__": esc(brand["name"]), "__MONOGRAM__": esc(brand["monogram"]), "__TAG__": esc(brand["tag"]),
        "__CTA__": esc(brand["cta"]), "__NAV__": "".join(f'<a href="#{href}">{label}</a>' for href, label in [("about", "About"), ("skills", "Skills"), ("projects", "Projects"), ("experience", "Journey"), ("github", "GitHub"), ("contact", "Contact")]),
        "__DESCRIPTION__": esc(hero["description"]), "__EYEBROW__": esc(hero["eyebrow"]), "__TITLE__": esc(hero["title"]),
        "__HERO_DESCRIPTION__": esc(hero["description"]), "__PRIMARY__": esc(hero["primary_button"]), "__SECONDARY__": esc(hero["secondary_button"]),
        "__GITHUB__": esc(brand["github"]), "__LINKEDIN__": esc(brand["linkedin"]), "__EMAIL__": esc(brand["email"]),
        "__ABOUT_TITLE__": esc(about["title"]), "__ABOUT_SUBTITLE__": esc(about["subtitle"]), "__ABOUT_DESCRIPTION__": esc(about["description"]),
        "__FACTS__": render_facts(about["facts"]), "__STATS__": render_stats(about["stats"]), "__SKILLS_TITLE__": esc(config["skills"]["title"]),
        "__SKILLS_SUBTITLE__": esc(config["skills"]["subtitle"]), "__SKILLS__": render_skill_groups(config["skills"]["groups"]),
        "__PROJECTS_TITLE__": esc(config["projects"]["title"]), "__PROJECTS_SUBTITLE__": esc(config["projects"]["subtitle"]),
        "__PROJECTS__": render_projects(config["projects"]["items"]), "__TIMELINE__": render_timeline(config["timeline"]),
        "__CERTIFICATES__": render_certificates(config["certificates"]), "__CONTACT_TITLE__": esc(contact["title"]),
        "__CONTACT_SUBTITLE__": esc(contact["subtitle"]), "__CONTACT_MESSAGE__": esc(contact["message"]),
    }
    for key, value in replacements.items():
        template = template.replace(key, value)
    return template


class PortfolioHandler(http.server.BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def is_admin(self):
        return self.headers.get("X-Admin-Token", "") == ADMIN_TOKEN

    def read_json_body(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, TypeError, UnicodeDecodeError, json.JSONDecodeError):
            return None

    def do_GET(self):
        request_path = self.path.split("?", 1)[0]
        if request_path in ("/", "/index.html"):
            body = build_page().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return
        if request_path == "/admin":
            body = admin_page().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if request_path == "/api/config":
            if not self.is_admin():
                self.send_json(401, {"error": "Admin token required."})
                return
            self.send_json(200, SITE_CONFIG)
            return
        public_path = request_path.lstrip("/")
        base_path = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.abspath(os.path.join(base_path, public_path))
        if public_path and file_path.startswith(base_path) and os.path.isfile(file_path):
            with open(file_path, "rb") as asset:
                data = asset.read()
            self.send_response(200)
            self.send_header("Content-Type", mimetypes.guess_type(file_path)[0] or "application/octet-stream")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        self.send_response(404)
        self.end_headers()

    def do_PUT(self):
        if self.path.split("?", 1)[0] != "/api/config":
            self.send_json(404, {"error": "Endpoint not found."})
            return
        if not self.is_admin():
            self.send_json(401, {"error": "Invalid admin token."})
            return
        updated_config = self.read_json_body()
        if not isinstance(updated_config, dict):
            self.send_json(400, {"error": "Request body must be a JSON object."})
            return
        try:
            save_site_config(updated_config)
            SITE_CONFIG.clear()
            SITE_CONFIG.update(updated_config)
        except OSError as exc:
            self.send_json(500, {"error": f"Could not save configuration: {exc}"})
            return
        self.send_json(200, {"message": "Configuration saved."})

    def log_message(self, format, *args):
        return


class PortfolioServer(socketserver.TCPServer):
    allow_reuse_address = True


def start_server():
    for port in range(PORT, PORT + 10):
        try:
            return PortfolioServer(("127.0.0.1", port), PortfolioHandler), port
        except OSError:
            continue
    raise OSError(f"No free port found starting from {PORT}")


if __name__ == "__main__":
    try:
        httpd, port = start_server()
    except OSError as exc:
        print(f"Unable to start portfolio server: {exc}")
        raise SystemExit(1)
    print(f"Portfolio website running at http://127.0.0.1:{port}")
    print(f"Control panel: http://127.0.0.1:{port}/admin")
    print("Admin token: set ADMIN_TOKEN before starting the server (default: change-me)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        httpd.server_close()

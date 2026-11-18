#!/usr/bin/env python3
"""ArchitectByAI Batch 02 — original animated visual stories.

Episodes 05–07 use continuous Python procedural graphics.
Episode 04 uses an original Blender 3D scene and this script composites
its time-varying text and brand-safe ending.
No external video, photograph, or stock footage is required.
"""
from __future__ import annotations

import argparse
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

ROOT = Path(__file__).resolve().parent
W, H = 540, 960
FPS = 20
DURATION = 16
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REGULAR = ImageFont.truetype(FONT, 22)
SMALL = ImageFont.truetype(FONT, 16)
TINY = ImageFont.truetype(FONT, 11)
HEAD = ImageFont.truetype(BOLD, 27)
END = ImageFont.truetype(BOLD, 24)

EPISODES = {
    "04": {
        "folder": "04_Digital_Product_Studio",
        "slug": "Episode04_Digital_Product_Studio_NEW",
        "color": (248, 188, 102),
        "title": "CREATE & SELL\nDIGITAL PRODUCTS",
        "beats": [
            "What if one idea\ncould become a real product?",
            "Begin on a digital canvas.",
            "Build. Refine. Create.",
            "From creative work\nto ready-to-share.",
        ],
    },
    "05": {
        "folder": "05_Communication_Engine",
        "slug": "Episode05_Communication_Engine_NEW",
        "color": (99, 224, 217),
        "title": "MARKETING & CUSTOMER\nCOMMUNICATION KIT",
        "beats": [
            "What if every message\nknew where to go?",
            "A question becomes\na clear conversation.",
            "Every response\nfollows the right path.",
            "The right message.\nThe right moment.",
        ],
    },
    "06": {
        "folder": "06_Client_Journey",
        "slug": "Episode06_Client_Journey_NEW",
        "color": (255, 178, 116),
        "title": "CLIENT ONBOARDING\n& PROPOSAL TOOLKIT",
        "beats": [
            "A first inquiry.\nA lasting impression.",
            "Listen. Scope. Understand.",
            "Turn the brief\ninto a clear proposal.",
            "Agree. Onboard. Deliver.",
        ],
    },
    "07": {
        "folder": "07_Magical_Coloring",
        "slug": "Episode07_Magical_Coloring_NEW",
        "color": (245, 174, 214),
        "title": "MAGICAL FRIENDS\nCOLORING TOOLKIT",
        "beats": [
            "Can mathematics\ndraw a magical friend?",
            "One fine curve\nfollows another.",
            "Symmetry turns\ninto a little magic.",
            "Now bring the magic\nto life with color.",
        ],
    },
}


def ease(a, b, x):
    z = max(0., min(1., (x-a)/max(.0001, b-a)))
    return z*z*(3-2*z)


def lerp(a, b, k):
    return a + (b-a)*k


def rgba(col, a=255):
    return tuple(col[:3])+(int(a),)


def bezier(a, b, c, d, n=65):
    pts = []
    for u in np.linspace(0, 1, n):
        x=(1-u)**3*a[0]+3*(1-u)**2*u*b[0]+3*(1-u)*u*u*c[0]+u**3*d[0]
        y=(1-u)**3*a[1]+3*(1-u)**2*u*b[1]+3*(1-u)*u*u*c[1]+u**3*d[1]
        pts.append((int(x),int(y)))
    return pts


def partial(draw, pts, progress, fill, width=2):
    n = max(0, min(len(pts),int(len(pts)*progress)))
    if n > 1:
        draw.line(pts[:n],fill=fill,width=width,joint='curve')


def base_gradient(ep):
    # Distinct palette per story. Noise and depth are deliberately subtle.
    palette = {
        "04": ((4,7,22),(25,27,53),(69,40,88)),
        "05": ((3,19,29),(8,49,58),(12,80,75)),
        "06": ((18,9,31),(47,23,55),(100,39,65)),
        "07": ((16,8,35),(40,20,70),(43,67,105)),
    }
    a,b,c = [np.array(q,dtype=float) for q in palette[ep]]
    yy,xx = np.mgrid[:H,:W].astype(float)
    r = np.hypot((xx-W*.51)/(W*.69),(yy-H*.54)/(H*.64))
    gl = np.clip(1-r,0,1)**1.5
    beam = np.exp(-((xx-W*.72)/(W*.52))**2-((yy-H*.65)/(H*.57))**2)
    arr = a[None,None,:]+gl[:,:,None]*(b-a)[None,None,:]+beam[:,:,None]*(c-b)[None,None,:]*.56
    return Image.fromarray(np.uint8(np.clip(arr,0,255)),"RGB").convert("RGBA")


def ambient(im, t, episode):
    layer=Image.new("RGBA",(W,H))
    d=ImageDraw.Draw(layer)
    c=EPISODES[episode]["color"]
    for k in range(46):
        x=int((k*173.7 + 13*math.sin(t*.32+k*1.9))%W)
        y=int(250+(k*59.13 + 17*math.cos(t*.24+k))%490)
        radius=1 if k%5 else 2
        alpha=int(30+25*(1+math.sin(t*1.5+k))*.5)
        d.ellipse((x-radius,y-radius,x+radius,y+radius),fill=rgba(c,alpha))
    im.alpha_composite(layer)
    return im


def glow_paths(im, shapes, blur=10):
    # Each shape is (list of points, rgb, line width, opacity).
    g=Image.new("RGBA",(W,H))
    gd=ImageDraw.Draw(g)
    ink=Image.new("RGBA",(W,H))
    crisp=ImageDraw.Draw(ink)
    for pts, col, width, opacity in shapes:
        if len(pts)>1:
            gd.line(pts, fill=rgba(col,min(opacity,130)),width=width*4,joint="curve")
            crisp.line(pts,fill=rgba(col,opacity),width=width,joint="curve")
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(blur)))
    im.alpha_composite(ink)


def card(im, cx, cy, w, h, line, title=None, fill=(13,24,41,232), height=13):
    layer=Image.new("RGBA",(W,H))
    d=ImageDraw.Draw(layer)
    x0=cx-w//2; y0=cy-h//2
    d.rounded_rectangle((x0+height,y0+height,cx+w//2+height,cy+h//2+height),radius=16,fill=(3,4,15,100))
    d.rounded_rectangle((x0,y0,cx+w//2,cy+h//2),radius=15,fill=fill,outline=rgba(line,220),width=2)
    d.line([(x0+18,y0+18),(x0+w-18,y0+18)], fill=rgba(line,170),width=1)
    if title:
        bbox=d.textbbox((0,0),title,font=SMALL)
        tw=bbox[2]-bbox[0]
        d.text((cx-tw/2,cy+min(13,h*.18)),title,font=SMALL,fill=(234,240,255,240))
    im.alpha_composite(layer)


def text_center(d, s, y, font, color):
    for i,line in enumerate(s.split('\n')):
        box=d.textbbox((0,0),line,font=font)
        tw=box[2]-box[0]
        d.text(((W-tw)/2,y+i*(font.size+8)),line,font=font,fill=color)


def overlay_brand(im,t,ep):
    spec=EPISODES[ep]
    layer=Image.new("RGBA",(W,H))
    d=ImageDraw.Draw(layer)
    accent=spec["color"]
    d.text((W/2,45),"ARCHITECTBYAI   /   USING PYTHON",font=TINY,anchor="mt",fill=rgba(accent,210))
    d.line((W/2-34,75,W/2+34,75),fill=rgba(accent,150),width=2)
    if t<12:
        index=min(3,int(t//3))
        start,end=index*3,(index+1)*3
        fade=min(1,ease(start,start+.5,t),ease(end,end-.42,t) if t>end-.42 else 1)
        white=(244,246,253,int(fade*253))
        text_center(d,spec["beats"][index],108,HEAD,white)
        d.text((W/2,904),"ARCHITECTBYAI   /   ENGINEERED INTELLIGENCE",
               font=TINY,anchor="mt",fill=(225,233,248,125))
    else:
        phase=ease(12,12.8,t)
        d.rounded_rectangle((34,784,506,938),radius=19,fill=(8,9,25,int(222*phase)),
                            outline=rgba(accent,int(200*phase)),width=2)
        text_center(d,spec["title"],805,END,(252,248,247,int(255*phase)))
        d.text((W/2,884),"FOLLOW @architectbyai",font=SMALL,anchor="mt",
               fill=(242,235,247,int(255*phase)))
        d.text((W/2,915),"architectbyai.com",font=TINY,anchor="mt",
               fill=rgba(accent,int(248*phase)))
    im.alpha_composite(layer)
    return im


def render_05(im,t):
    # Incoming customer question becomes a typed reply and a useful follow-up.
    aqua=(93,232,217); blue=(76,166,249); coral=(255,157,113)
    waves=[]
    for k in range(4):
        ph=t*.83+k*.72
        pts=[]
        for x in range(-60,600,6):
            y=510+math.sin(x*.011+ph)*(73+18*math.sin(t*.4+k))
            y+=k*14-21
            pts.append((x,int(y)))
        waves.append((pts,(blue,aqua,coral,blue)[k],2,42))
    glow_paths(im,waves,14)
    enter=ease(.3,3.4,t)
    # Main inbox slab, drawn as depth-shaded floating UI.
    card(im,270,510,270,256,aqua,None,(11,35,52,239),18)
    inky=Image.new("RGBA",(W,H))
    d=ImageDraw.Draw(inky)
    d.text((170,421),"INBOX   /   LIVE",font=SMALL,fill=rgba(aqua,218))
    d.ellipse((394,424,405,435),fill=coral)
    for j in range(4):
        a=ease(1.8+j*.38,2.6+j*.38,t)
        w=int((170-j*16)*a)
        if w:
            d.rounded_rectangle((185,472+j*27,185+w,478+j*27),radius=3,fill=(122,207,232,int(215*a)))
    im.alpha_composite(inky)
    # Envelope follows an actual cubic path, then attaches to the inbox.
    incoming=bezier((-100,675),(58,260),(360,310),(272,500),110)
    travel=ease(0.0,3.3,t)
    idx=min(len(incoming)-1,int(travel*(len(incoming)-1)))
    if idx>2:
        glow_paths(im,[(incoming[:idx],coral,3,230)],12)
    x,y=incoming[idx]
    stamp=Image.new("RGBA",(W,H))
    d=ImageDraw.Draw(stamp)
    wd=88*(1-.49*ease(2.5,3.8,t))
    ht=56*(1-.49*ease(2.5,3.8,t))
    d.rounded_rectangle((x-wd/2,y-ht/2,x+wd/2,y+ht/2),radius=7,fill=(10,43,60,242),outline=coral,width=3)
    d.line([(x-wd/2+4,y-ht/2+4),(x,y+6),(x+wd/2-4,y-ht/2+4)],fill=rgba(coral,200),width=2)
    im.alpha_composite(stamp)
    # A genuine three-way routing transformation: branching pathways
    # grow outward continuously, with distinct delivery cards.
    spread=ease(3.4,7.5,t)
    destinations=[(128,650,"QUESTION",coral),(270,700,"RESPONSE",aqua),(412,650,"FOLLOW-UP",blue)]
    links=[]
    for k,(cx,cy,label,col) in enumerate(destinations):
        path=bezier((270,555),(270+(cx-270)*.36,588),(cx,580),(cx,cy-36),85)
        links.append((path[:max(2,int(len(path)*spread))],col,3,230))
        if spread>.4:
            slide=ease(4.6+k*.2,6.8+k*.18,t)
            yy=int(lerp(565,cy,slide))
            width=110 if k==2 else 118
            card(im,cx,yy,width,72,col,label,(9,30,45,245),9)
    glow_paths(im,links,8)
    # Confirmation ring is a complete visual payoff, not just drifting dots.
    completion=ease(9.2,11.5,t)
    if completion:
        layer=Image.new("RGBA",(W,H));d=ImageDraw.Draw(layer)
        r=20+28*completion
        d.arc((270-r,540-r,270+r,540+r),-90,-90+completion*350,fill=coral,width=3)
        p=[(254,540),(266,551),(290,521)]
        partial(d,p,completion,rgba(aqua,255),4)
        d.text((270,600),"REPLY SENT",font=SMALL,anchor="mt",fill=rgba(aqua,int(255*completion)))
        im.alpha_composite(layer)
    return im


def render_06(im,t):
    # A paperwork story with progressive, legible documents and a signed deal.
    amber=(255,188,107); orchid=(188,133,249); pink=(252,120,153)
    stage=ease(.1,3,t)
    layer=Image.new("RGBA",(W,H))
    d=ImageDraw.Draw(layer)
    # Incoming inquiry flies along a circular intake orbit.
    orbit=[]
    for i in range(85):
        u=i/84
        orbit.append((int(270+180*math.cos(math.pi+.96*math.pi*u)),
                      int(530+146*math.sin(math.pi+.96*math.pi*u))))
    im.alpha_composite(layer)
    glow_paths(im,[(orbit[:max(2,int(len(orbit)*stage))],orchid,3,185)],12)
    # The proposal is a genuinely filled document, not a random empty box.
    reveal=ease(2.4,5.4,t)
    w=int(242*reveal)
    if w>5:
        card(im,270,520,w,310,amber,None,(26,20,43,248),15)
        paper=Image.new("RGBA",(W,H));d=ImageDraw.Draw(paper)
        a=int(248*reveal)
        d.text((166,382),"CLIENT BRIEF",font=REGULAR,fill=rgba(amber,a))
        d.line((166,418,373,418),fill=rgba(amber,a//2),width=2)
        for row,(length,col) in enumerate(((173,orchid),(196,orchid),(154,pink),(203,orchid))):
            p=ease(3.5+row*.53,5.1+row*.62,t)
            d.rounded_rectangle((166,446+row*37,166+int(length*p),452+row*37),radius=3,fill=rgba(col,int(a*p)))
        im.alpha_composite(paper)
    # A route through SCOPE -> PROPOSAL -> DELIVERY is drawn in motion.
    nodes=[(127,730,"SCOPE",orchid),(270,710,"PROPOSAL",amber),(412,730,"DELIVER",pink)]
    link=[]
    for k in range(2):
        p=bezier((nodes[k][0]+28,nodes[k][1]),(217,667),(325,672),(nodes[k+1][0]-26,nodes[k+1][1]),65)
        u=ease(7+k*1.0,9.2+k*1.0,t)
        link.append((p[:max(2,int(u*len(p)))],amber if k else orchid,3,210))
    glow_paths(im,link,10)
    for k,(x,y,label,col) in enumerate(nodes):
        scale=ease(6.0+k*.65,7.7+k*.7,t)
        if scale:
            wd=int(111*scale)
            if wd>10:
                card(im,x,y,wd,67,col,label,(29,20,46,241),8)
    # Handwritten signature animates along a real Bézier curve.
    signature=ease(9,11.8,t)
    sig=[]
    for x in np.linspace(171,369,80):
        u=(x-171)/198
        y=620+18*math.sin(u*4*math.pi)*math.exp(-u*.75)-7*math.sin(u*12*math.pi)
        sig.append((int(x),int(y)))
    glow_paths(im,[(sig[:max(2,int(signature*len(sig)))],amber,3,220)],9)
    if t>10.3:
        stamp=Image.new("RGBA",(W,H));d=ImageDraw.Draw(stamp)
        p=ease(10.4,11.7,t)
        d.ellipse((377,592,413,628),outline=rgba(pink,int(245*p)),width=2)
        d.text((395,602),"✓",font=SMALL,anchor="mt",fill=rgba(amber,int(245*p)))
        im.alpha_composite(stamp)
    return im


def butterfly_paths():
    # Hand-drawn mathematical wing silhouettes; a recognizable, symmetrical
    # magical butterfly character, not a generic radial spirograph.
    right=[]
    segments=[
        ((0,15),(60,-112),(176,-160),(164,-15)),
        ((164,-15),(225,8),(198,70),(147,78)),
        ((147,78),(214,178),(89,213),(36,133)),
        ((36,133),(-15,99),(12,59),(0,15)),
    ]
    for a,b,c,d in segments:
        right.extend(bezier(a,b,c,d,40)[:-1])
    right.append((0,15))
    left=[(-x,y) for x,y in right]
    return right,left


def transform(points,t):
    s=1.08+.032*math.sin(t*.7)
    return [(int(270+x*s),int(517+y*s)) for x,y in points]


def render_07(im,t):
    # Symmetry + parametric tracing -> coloring artwork. Fine, controlled lines.
    pink=(255,179,222); teal=(123,235,234); gold=(255,202,128); vio=(192,155,255)
    R,L=butterfly_paths()
    right,left=transform(R,t),transform(L,t)
    progress=ease(1.0,7.1,t)
    if t>8.7:
        opacity=ease(8.8,11.6,t)
        fill=Image.new("RGBA",(W,H))
        d=ImageDraw.Draw(fill)
        d.polygon(right,fill=rgba(pink,int(65*opacity)))
        d.polygon(left,fill=rgba(teal,int(65*opacity)))
        # transparent gradient gems
        for s in (-1,1):
            cx=270+s*113
            d.ellipse((cx-42,448,cx+42,514),fill=rgba(vio if s==1 else gold,int(128*opacity)))
        im.alpha_composite(fill)
    if progress:
        partial_p_R=right[:max(2,int(len(right)*progress))]
        partial_p_L=left[:max(2,int(len(left)*progress))]
        glow_paths(im,[(partial_p_R,pink,2,245),(partial_p_L,teal,2,245)],8)
        # Tip markers travel continuously as curves are being drawn.
        for pts,col in ((partial_p_R,gold),(partial_p_L,gold)):
            x,y=pts[-1]
            mark=Image.new("RGBA",(W,H));d=ImageDraw.Draw(mark)
            d.ellipse((x-5,y-5,x+5,y+5),fill=rgba(col,245))
            im.alpha_composite(mark)
    # Inner wing veins, with a delayed drawing reveal
    inner=ease(5.2,10.4,t)
    veins=[]
    for side,col in ((1,pink),(-1,teal)):
        for k in range(5):
            ang=k*.45-1
            pts=bezier((side*12,10),
                       (side*(72+17*k),-62+38*k),
                       (side*(120+4*k),-100+70*k),
                       (side*(142-3*k),-75+74*k),60)
            trans=transform(pts,t)
            veins.append((trans[:max(2,int(inner*len(trans)))],col,2,200))
    if inner:glow_paths(im,veins,7)
    # A fine ornamental body and friendly little face.
    body=Image.new("RGBA",(W,H));d=ImageDraw.Draw(body)
    bod=ease(5.5,8.2,t)
    if bod:
        d.ellipse((261,480,279,635),fill=(18,17,47,255),outline=rgba(gold,int(220*bod)),width=2)
        d.ellipse((247,468,293,510),fill=(29,20,55,255),outline=rgba(gold,int(240*bod)),width=2)
        d.ellipse((257,487,262,492),fill=rgba(pink,int(255*bod)))
        d.ellipse((278,487,283,492),fill=rgba(teal,int(255*bod)))
        d.arc((263,489,277,503),0,160,fill=rgba(gold,int(240*bod)),width=1)
        antennas=[
            bezier((262,467),(224,445),(229,410),(216,405),30),
            bezier((278,467),(315,442),(307,412),(327,408),30),
        ]
        for p in antennas:partial(d,p,bod,rgba(gold,240),2)
    im.alpha_composite(body)
    # The epicycle construction appears early as a mechanism/proof, then fades.
    if t<7.5 and t>2.2:
        k=ease(2.2,3.1,t)*(1-ease(6.7,7.6,t))
        ring=Image.new("RGBA",(W,H));d=ImageDraw.Draw(ring)
        px,py=270+118*math.cos(t*.8),430+80*math.sin(t*.8)
        d.ellipse((px-23,py-23,px+23,py+23),outline=rgba(gold,int(130*k)),width=1)
        d.line((px,py,px+14*math.cos(t*3),py+14*math.sin(t*3)),fill=rgba(gold,int(210*k)),width=2)
        d.text((57,733),"x(t) = Σ rₖ cos(kωt)",font=SMALL,fill=rgba(gold,int(198*k)))
        im.alpha_composite(ring)
    return im


def ep04_background(t):
    # Exact frames from our original Blender 3D render. We preserve all camera
    # motion from the 3D scene rather than using still panels or slide swaps.
    # ffmpeg extracts the correctly timed frame for every time t.
    return None


def compose_3d(episode):
    folder=ROOT/EPISODES[episode]["folder"]
    origin=folder/"3d_raw.mp4"
    if not origin.exists():
        raise FileNotFoundError("Episode 04 requires Blender animation frames, not a still or slideshow.")
    return origin


def load_plate(episode):
    source=ROOT/EPISODES[episode]["folder"]/"cinematic_plate.png"
    if not source.exists():
        source=ROOT/EPISODES[episode]["folder"]/"cinematic_plate.jpg"
    if not source.exists():raise FileNotFoundError(source)
    photo=Image.open(source).convert("RGBA")
    ratio=photo.width/photo.height
    if ratio>.64:
        width=W+30
        height=round(width/ratio)
    else:
        height=H+86
        width=round(height*ratio)
    photo=photo.resize((width,height),Image.Resampling.LANCZOS)
    return photo


def photo_progress(episode,t):
    if episode=="04":return ease(5,9.8,t)
    if episode=="05":return ease(2.5,8.2,t)
    if episode=="06":return ease(3,8.7,t)
    return ease(4.0,11.0,t)


def composite_cinematic_photo(im,t,ep,photo):
    progress=photo_progress(ep,t)
    if progress<=0:return im
    # Cinematic stage comes into focus gradually from the geometry it replaced.
    # Spatial wipe is animated continuously, not a crossfade between slides.
    # Keep the gradient above/below wider photographic plates; no black bars.
    plate=im.copy()
    drift_x=int(13*math.sin(t*.37)+15*ease(6,15,t))
    drift_y=int(9*math.sin(t*.21))
    x=(W-photo.width)//2+drift_x
    y=(H-photo.height)//2+drift_y
    if ep=="05":y=150+drift_y
    plate.paste(photo,(x,y))
    xx=np.arange(W,dtype=float)[None,:]
    threshold=-125+progress*(W+250)
    reveal=np.clip((threshold-xx)/130,0,1)
    reveal=np.broadcast_to(reveal,(H,W))
    # An iris glow around the moving reveal edge gives a beautiful
    # beginning-to-end transformation rather than static backgrounds.
    mask=Image.fromarray(np.uint8(reveal*255),"L")
    im.paste(plate,(0,0),mask)
    if progress>.1:
        gold=(255,198,118)
        headx=int(threshold-62)
        if 25<headx<W-25:
            line=Image.new("RGBA",(W,H))
            d=ImageDraw.Draw(line)
            alpha=int(115*math.sin(progress*math.pi))
            d.line((headx,262,headx,770),fill=rgba(gold,alpha),width=2)
            im.alpha_composite(line.filter(ImageFilter.GaussianBlur(18)))
    return im


def animate_photo_detail(im,t,ep):
    # Animated action over the photographic plate that continues after
    # the wipe completes: an action starts, flows and reaches a payoff.
    appear=ease(5,9,t) if ep=="04" else ease(4,9,t)
    if appear<=0:return im
    if ep=="04":
        guide=bezier((185,545),(305,475),(395,405),(425,540),85)
        guide+=bezier((425,540),(469,640),(365,676),(315,690),65)
        amt=ease(6,12,t)
        glow_paths(im,[(guide[:max(2,int(amt*len(guide)))],
                        (250,196,112),2,130)],10)
        # Product milestones are visibly confirmed as they leave the editor.
        if t>9:
            d=ImageDraw.Draw(im)
            pulse=ease(9.2,11.5,t)
            for k,(cx,cy) in enumerate(((400,340),(421,461),(418,564))):
                p=ease(9.2+k*.37,11.4+k*.37,t)
                d.arc((cx-15,cy-15,cx+15,cy+15),-90,-90+360*p,
                      fill=rgba((255,211,145),int(210*p)),width=2)
    elif ep=="05":
        # Gold-to-teal luminous response circulates through the message UI.
        path=bezier((104,480),(145,286),(376,293),(438,481),105)
        partial_p=ease(6.0,11.6,t)
        glow_paths(im,[(path[:max(2,int(len(path)*partial_p))],
                        (247,190,118),2,125)],8)
    elif ep=="06":
        # A genuine signing stroke on the floating proposal.
        path=bezier((189,563),(220,525),(251,623),(292,562),65)
        path+=bezier((292,562),(330,530),(348,595),(373,564),55)
        p=ease(8.3,11.6,t)
        glow_paths(im,[(path[:max(2,int(len(path)*p))],(255,208,132),3,235)],10)
    else:
        # Fine border illumination follows the butterfly silhouette as it
        # changes from coloring-line art into an illuminated fantasy design.
        ring=[]
        for j in range(130):
            a=-.35*math.pi+j/129*1.7*math.pi
            r=190+20*math.sin(4*a+t*.8)
            ring.append((int(W/2+r*math.cos(a)),int(530+r*.83*math.sin(a))))
        p=ease(8,13,t)
        glow_paths(im,[(ring[:max(2,int(p*len(ring)))],
                        (255,204,140),2,95)],15)
    return im


def encode(ep,frames_only=False):
    spec=EPISODES[ep]
    folder=ROOT/spec["folder"]
    folder.mkdir(parents=True,exist_ok=True)
    output=folder/(spec["slug"]+".mp4")
    command=["ffmpeg","-hide_banner","-loglevel","error","-y",
             "-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}",
             "-r",str(FPS),"-i","pipe:0","-an","-c:v","libx264",
             "-preset","veryfast","-crf","19","-pix_fmt","yuv420p",
             "-movflags","+faststart",str(output)]
    process=subprocess.Popen(command,stdin=subprocess.PIPE)
    bg=base_gradient(ep)
    photo=load_plate(ep)
    if ep=="04":
        # Decode actual continuously rendered Blender animation frames and
        # composite one matching time step onto each output frame.
        source=compose_3d(ep)
        reader=subprocess.Popen(["ffmpeg","-hide_banner","-loglevel","error",
             "-i",str(source),"-vf",f"fps={FPS},scale={W}:{H}",
             "-f","rawvideo","-pix_fmt","rgb24","pipe:1"],stdout=subprocess.PIPE)
        last_frame_raw=None
    for n in range(FPS*DURATION):
        t=n/FPS
        if ep=="04":
            raw=reader.stdout.read(W*H*3)
            # Optical interpolation can drop the final 2–3 frames at EOS.
            if len(raw)!=W*H*3:
                if last_frame_raw is None:raise RuntimeError(f"Missing 3D frame at {t}")
                raw=last_frame_raw
            else:
                last_frame_raw=raw
            im=Image.frombytes("RGB",(W,H),raw).convert("RGBA")
            # A few glassy streaks track export progress without obscuring the laptop.
            a=ease(4.3,10.5,t)
            if a:
                wave=[]
                for j in range(65):
                    x=int(65+j*6.2)
                    y=int(725+7*math.sin(j*.18+t*1.9))
                    wave.append((x,y))
                glow_paths(im,[(wave[:max(2,int(a*len(wave)))],spec["color"],2,85)],8)
        else:
            im=ambient(bg.copy(),t,ep)
            if ep=="05":im=render_05(im,t)
            if ep=="06":im=render_06(im,t)
            if ep=="07":im=render_07(im,t)
        im=composite_cinematic_photo(im,t,ep,photo)
        im=animate_photo_detail(im,t,ep)
        im=overlay_brand(im,t,ep)
        if n in (FPS*2,FPS*5,FPS*8,FPS*11,FPS*14):
            im.convert("RGB").save(folder/f"review_{n//FPS:02d}s.jpg",quality=87)
        process.stdin.write(im.convert("RGB").tobytes())
    process.stdin.close()
    code=process.wait()
    if ep=="04":
        reader.stdout.close();reader.wait()
    if code:raise RuntimeError(f"ffmpeg failed {code}")
    print(output)


if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--episode",choices=list(EPISODES)+["all"],default="all")
    args=ap.parse_args()
    for e in (EPISODES if args.episode=="all" else [args.episode]):
        encode(e)

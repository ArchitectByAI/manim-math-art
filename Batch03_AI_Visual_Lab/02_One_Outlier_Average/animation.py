#!/usr/bin/env python3
"""ArchitectByAI B03-V02: One Outlier Hijacks the Average.

Original, deterministic NumPy/Pillow procedural motion design.
The statistical demonstration uses exact population summaries on synthetic values:
[10,11,12,12,13,14,15,16,17] and the same values with 150 appended.
The display scales its vertical axis during the transition (clearly labeled).

Requires numpy, Pillow, ffmpeg on PATH. Render using:
    python animation.py --output out.mp4
"""
from __future__ import annotations
import argparse, math, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE=Path(__file__).resolve().parent
W,H,FPS,DURATION=540,960,18,18
NORMAL=np.array([10,11,12,12,13,14,15,16,17],dtype=float)
WITH=np.append(NORMAL,150.)
assert abs(float(NORMAL.mean())-13.3333333333)<.001
assert float(np.median(NORMAL))==13.
assert float(WITH.mean())==27. and float(np.median(WITH))==13.5
INK=(7,12,27); WHITE=(245,248,255); MUTED=(152,180,202); CYAN=(83,235,223); PINK=(255,118,162); GOLD=(255,204,114)
FP='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT=lambda n,b=False:ImageFont.truetype(FB if b else FP,n)
F11,F13,F15,F17,F21,F26,F29=[FONT(x,x>=21) for x in (11,13,15,17,21,26,29)]

def ease(v):
    v=max(0.,min(1.,v));return v*v*(3-2*v)
def lerp(a,b,f):return a+(b-a)*f

def glow_line(im,points,col,width=3):
    d=ImageDraw.Draw(im,'RGBA')
    for k in (8,5,3):d.line(points,fill=(*col,int(15 if k==8 else 25)),width=width+k,joint='curve')
    d.line(points,fill=(*col,255),width=width,joint='curve')

def txt(d,s,x,y,font=F15,col=WHITE,anchor=None):
    d.text((x,y),s,font=font,fill=col,anchor=anchor,stroke_width=0)
def center(d,s,y,font,col=WHITE):txt(d,s,270,y,font,col,'mt')

def frame(t):
    im=Image.new('RGB',(W,H),INK);d=ImageDraw.Draw(im,'RGBA')
    # subtle technologically inspired luminous rails; original procedural artwork
    for i in range(19):
        x=(i*71+35)%W;y=(i*107+205)%H
        d.ellipse((x-1,y-1,x+1,y+1),fill=(81,121,162,90))
    d.rounded_rectangle((18,17,522,58),radius=14,fill=(14,31,51,255),outline=(48,100,119,255),width=1)
    txt(d,'ARCHITECTBYAI  |  AI VISUAL LAB',29,28,F13,CYAN)
    # hook in first instant, not in a caption
    txt(d,'CAN ONE NUMBER',28,81,F29,WHITE)
    txt(d,'HIJACK THE AVERAGE?',28,117,F26,GOLD)
    txt(d,'Follow for Python • AI • Data Science',30,168,F13,MUTED)
    # one compact animated story panel
    d.rounded_rectangle((19,223,521,727),radius=24,fill=(13,25,45,255),outline=(44,76,101,255),width=2)
    txt(d,'REAL MATH / SYNTHETIC DATA',37,242,F11,(164,197,219))
    if t<3.2: sub='9 ordinary values'
    elif t<7: sub='Now add ONE extreme value'
    elif t<13.5: sub='Compare the two summaries'
    else: sub='One extreme value changes the mean'
    txt(d,sub,37,270,F17,WHITE)
    # axis expansion occurs before the outlier grows to avoid misleading clipping
    zoom=ease((t-3.0)/2.2)
    ymax=lerp(22,160,zoom)
    x0,x1,y0,y1=45,495,322,591
    for i in range(5):
        val=ymax*i/4;yy=y1-(val/ymax)*(y1-y0)
        d.line((x0,yy,x1,yy),fill=(68,96,118,90),width=1)
        txt(d,str(int(round(val))),x0,yy-14,F11,(135,158,179))
    # explicit scale disclosure
    txt(d,f'Y-AXIS 0–{int(ymax)}  |  VALUES',x0,622,F11,(124,170,195))
    data=NORMAL.tolist()+[150]
    plotstart=65;pitch=43.0; bw=24
    appearing=ease((t-.0)/2.5)
    outgrow=ease((t-4.3)/1.1)
    for i,v in enumerate(data):
        if i<9:
            height=min(v/ymax*(y1-y0),y1-y0)*appearing
            col=CYAN
        else:
            height=min(v/ymax*(y1-y0),y1-y0)*outgrow
            col=PINK
        x=plotstart+i*pitch
        top=y1-height
        if height>2:
            d.rounded_rectangle((x,top,x+bw,y1),radius=5,fill=(*col,185),outline=(*col,255),width=1)
            d.line((x+4,top+3,x+bw-4,top+3),fill=(255,255,255,140),width=2)
        if i==9 and outgrow>.4:
            d.ellipse((x-7,top-6,x+bw+7,top+26),outline=(*PINK,int(100+110*math.sin(t*9)**2)),width=2)
        if t>5.1 or i<9:
            txt(d,str(int(v)),x+bw/2,y1+7,F11,col,'mt')
    # marker movement is calculated from the exact arithmetic means/medians
    d.rounded_rectangle((37,647,503,712),radius=17,fill=(19,39,61,255),outline=(48,76,99,255))
    final=t>=5.4
    mean=float(WITH.mean() if final else NORMAL.mean())
    median=float(np.median(WITH) if final else np.median(NORMAL))
    txt(d,'MEAN',53,657,F13,MUTED)
    txt(d,f'{mean:.1f}',53,675,F26,PINK)
    txt(d,'MEDIAN',308,657,F13,MUTED)
    txt(d,f'{median:.1f}',308,675,F26,CYAN)
    if final and 6.0<t<13.7:
        # arrows are qualitative markers; accompanying figures are exact
        d.line((133,684,219,684),fill=(*PINK,200),width=3)
        d.polygon([(220,684),(209,679),(209,689)],fill=(*PINK,200))
        txt(d,'×2.03',228,674,F13,PINK)
    # contrasting phases; meaningful changing story beats
    if t<2.7: phrase='A small, stable dataset.'
    elif t<5.4: phrase='One outlier enters the system.'
    elif t<9.2: phrase='The MEAN more than doubles.'
    elif t<13.9:phrase='The MEDIAN barely moves.'
    else: phrase='SAVE THE DIFFERENCE'
    if t<16:
        center(d,phrase,756,F21,GOLD if t>=13.9 else WHITE)
        if 14<=t<16:
            center(d,'Mean = sum(values) / count',797,F17,WHITE)
            center(d,'Median = middle value(s) when sorted',830,F13,CYAN)
        else:
            center(d,'One outlier: mean 13.3 → 27.0',801,F15,PINK)
            center(d,'Median 13.0 → 13.5',832,F15,CYAN)
        center(d,'@architectbyai  •  Using Python',906,F13,MUTED)
    else:
        d.rounded_rectangle((17,741,523,941),radius=25,fill=(21,41,61,255),outline=(*CYAN,255),width=2)
        center(d,'TURN DATA INTO DECISIONS',764,F21,WHITE)
        center(d,'KPI DASHBOARD TOOLKIT',803,F26,CYAN)
        center(d,'Explore our digital products',852,F15,WHITE)
        center(d,'architectbyai.com',894,F21,WHITE)
    return im

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=BASE/'Batch03_Video02_native.mp4');ap.add_argument('--fps',type=int,default=FPS);a=ap.parse_args()
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(a.fps),'-i','pipe:0','-an','-c:v','libx264','-preset','ultrafast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(a.output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for i in range(DURATION*a.fps):
        try:proc.stdin.write(frame(i/a.fps).tobytes())
        except BrokenPipeError:break
        if i%72==0:print('frame',i,flush=True)
    proc.stdin.close()
    if proc.wait():raise RuntimeError('FFmpeg failed')
    frame(0.05).save(BASE/'thumbnail.png')
    for name,t in [('opening',.05),('outlier',5.5),('insight',10),('save',15),('end',17)]:frame(t).save(BASE/(name+'.png'))
    print('rendered',a.output)
if __name__=='__main__':main()

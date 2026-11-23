#!/usr/bin/env python3
"""ArchitectByAI AI Visual Lab: Why perfect training fit can fail.

Reproducible synthetic illustration of polynomial overfitting.
Train: 11 noisy samples of a smooth function. Chebyshev degree 3 vs 10.
Holdout: 101 independent noiseless evaluation locations for visualization.
Everything is synthetic. The reported errors are root-mean-squared errors.
Usage: python animation.py --output video.mp4
Requires numpy, Pillow and ffmpeg on PATH.
"""
import argparse, subprocess, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W,H=540,960
FPS=20
DURATION=18
NAVY=(8,14,28); PANEL=(15,27,47); MUTED=(142,172,196)
CYAN=(79,231,219); PINK=(255,111,153); GOLD=(255,212,132); WHITE=(242,248,255)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def ft(z,b=False): return ImageFont.truetype(BOLD if b else FONT,z)
F12,F14,F18,F23,F27,F31=ft(12),ft(14),ft(18),ft(23,True),ft(27,True),ft(31,True)

def smooth(v):
    v=max(0,min(1,v));return v*v*(3-2*v)

def data():
    rng=np.random.default_rng(96)
    x=np.linspace(-.93,.93,11)
    f=lambda z:.48*np.sin(2.8*z)+.18*z
    y=f(x)+rng.normal(0,.055,len(x))
    q=np.linspace(-.99,.99,101)
    truth=f(q)
    simple=np.polynomial.chebyshev.chebfit(x,y,3)
    complex_=np.polynomial.chebyshev.chebfit(x,y,10)
    predict=lambda c,z:np.polynomial.chebyshev.chebval(z,c)
    stats={
       'simple_train':float(np.sqrt(np.mean((predict(simple,x)-y)**2))),
       'simple_holdout':float(np.sqrt(np.mean((predict(simple,q)-truth)**2))),
       'complex_train':float(np.sqrt(np.mean((predict(complex_,x)-y)**2))),
       'complex_holdout':float(np.sqrt(np.mean((predict(complex_,q)-truth)**2)))
    }
    assert stats['complex_train']<1e-10 and stats['complex_holdout']>stats['simple_holdout']*10
    return x,y,q,truth,predict(simple,q),predict(complex_,q),stats

X,Y,Q,TRUE,SMALL,BIG,STATS=data()
L,T,R,B=49,279,491,655

def px(x):return L+(x+1)/2*(R-L)
def py(y):return (T+B)/2-y*165

def ctext(d,text,y,font,color):
    bb=d.textbbox((0,0),text,font=font)
    d.text(((W-(bb[2]-bb[0]))/2,y),text,font=font,fill=color)

def line_segments(d,xx,yy,col,width=3,cut=None):
    last=None
    for k,(a,b) in enumerate(zip(xx,yy)):
        if cut is not None and k>cut:break
        p=(px(a),py(b))
        inbounds=L+1<=p[0]<=R-1 and T+1<=p[1]<=B-1
        if last is not None and inbounds and last[1]:
            d.line((*last[0],*p),fill=col,width=width,joint='curve')
        last=(p,inbounds)

def frame(t):
    img=Image.new('RGB',(W,H),NAVY);d=ImageDraw.Draw(img)
    d.text((28,29),'ARCHITECTBYAI  |  AI VISUAL LAB',font=F14,fill=CYAN)
    d.text((28,77),'WHEN PERFECT',font=F31,fill=WHITE)
    d.text((28,117),'FIT GOES WRONG',font=F31,fill=WHITE)
    d.text((28,174),'Follow for real Python + AI experiments',font=F14,fill=MUTED)
    d.rounded_rectangle((23,237,517,712),radius=24,fill=PANEL,outline=(47,73,98),width=2)
    d.text((47,251),'TRAINING DATA  •  SYNTHETIC EXAMPLE',font=F12,fill=(164,194,215))
    d.rectangle((L,T,R,B),fill=(12,23,41))
    for j in range(6):
        xx=L+(R-L)*j/5
        d.line((xx,T,xx,B),fill=(32,52,73),width=1)
    for j in range(6):
        yy=T+(B-T)*j/5
        d.line((L,yy,R,yy),fill=(32,52,73),width=1)
    d.line((L,py(0),R,py(0)),fill=(64,85,102),width=1)
    # truth signal, never disclosed to learner as 'test labels' before reveal
    if t>=9:
        n=int(smooth((t-9)/1.2)*(len(Q)-1))
        line_segments(d,Q,TRUE,(102,120,145),2,cut=n)
    # original train data points enter 0-2 sec
    n=int(smooth((t+.2)/2)*len(X))
    for x,y in zip(X[:n],Y[:n]):
        xx,yy=px(x),py(y)
        d.ellipse((xx-5,yy-5,xx+5,yy+5),fill=GOLD)
    # lower-degree fit enters while high-degree fit eventually overtakes it
    if t>=2:
        count=int(smooth((t-2)/1.3)*(len(Q)-1))
        line_segments(d,Q,SMALL,CYAN,4,cut=count)
    if t>=5:
        count=int(smooth((t-5)/1.5)*(len(Q)-1))
        line_segments(d,Q,BIG,PINK,4,cut=count)
    # out-of-sample measured values are visible on grid later
    if t>=9:
        n=int(smooth((t-9)/1.6)*19)
        for x,y in zip(Q[::5][:n],TRUE[::5][:n]):
            xx,yy=px(x),py(y)
            if T<yy<B:d.ellipse((xx-2.6,yy-2.6,xx+2.6,yy+2.6),fill=(183,198,217))
    d.ellipse((55,672,66,683),fill=GOLD)
    d.text((72,669),'TRAIN DATA',font=F12,fill=WHITE)
    d.line((185,677,207,677),fill=CYAN,width=4)
    d.text((214,669),'SIMPLE',font=F12,fill=WHITE)
    d.line((335,677,357,677),fill=PINK,width=4)
    d.text((364,669),'COMPLEX',font=F12,fill=WHITE)
    # bottom narrative: two model training errors followed by holdout errors
    if t<2.1:
        l1,l2='11 POINTS. ONE PATTERN.','WHAT WOULD YOU LEARN?'
    elif t<5:
        l1,l2='A SIMPLE CURVE','CAPTURES THE TREND.'
    elif t<8.5:
        l1,l2='A COMPLEX CURVE','HITS EVERY TRAINING POINT.'
    elif t<11.8:
        l1,l2='NEW DATA REVEALS','THE HIDDEN PROBLEM.'
    elif t<14:
        l1,l2='PERFECT TRAINING FIT','CAN GENERALIZE WORSE.'
    elif t<16:
        l1,l2='SAVE THIS:','TRAINING FIT ≠ PREDICTIVE POWER'
    else:l1,l2='',''
    if t<16:
        ctext(d,l1,744,F27,WHITE)
        ctext(d,l2,789,F18,CYAN if 14<=t<16 else (177,208,222))
        if 8.5<=t<14:
            ctext(d,'HOLDOUT RMSE: SIMPLE %.2f  |  COMPLEX %.2f'%(STATS['simple_holdout'],STATS['complex_holdout']),854,F12,GOLD)
        elif 5<=t<8.5:
            ctext(d,'TRAIN RMSE: SIMPLE %.2f  |  COMPLEX %.2f'%(STATS['simple_train'],STATS['complex_train']),854,F12,GOLD)
        else:
            ctext(d,'True Python computation  •  synthetic demonstration',857,F12,MUTED)
        ctext(d,'@architectbyai',918,F14,MUTED)
    else:
        d.rounded_rectangle((20,733,520,943),radius=23,fill=(20,38,58),outline=CYAN,width=2)
        ctext(d,'BETTER DECISIONS START',747,F23,WHITE)
        ctext(d,'WITH BETTER DATA',783,F23,WHITE)
        ctext(d,'AI ASSISTANTS & CHATBOTS',829,F18,CYAN)
        ctext(d,'architectbyai.com',871,F23,WHITE)
        ctext(d,'Follow @architectbyai',916,F12,MUTED)
    return img

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output',default=str(Path(__file__).with_name('B03_V03_Overfitting_1080x1920.mp4')))
    a=p.parse_args()
    # native 540x960 rendering, delivery resolution 1080x1920
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',a.output]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for i in range(FPS*DURATION):
            proc.stdin.write(frame(i/FPS).tobytes())
            if i%90==0:print('rendering frame',i,'/',FPS*DURATION,flush=True)
    finally:proc.stdin.close()
    if proc.wait():raise RuntimeError('FFmpeg render failed')
    root=Path(a.output).parent
    for name,t in [('cover',0.7),('middle',7.8),('insight',13.6),('save',15.1),('end',17)]:
        frame(t).resize((1080,1920),Image.Resampling.LANCZOS).save(root/(name+'.png'))
    print('STATS',STATS,flush=True)
    print('complete',a.output,flush=True)
if __name__=='__main__':main()

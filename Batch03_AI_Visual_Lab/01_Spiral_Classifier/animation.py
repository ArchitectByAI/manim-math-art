#!/usr/bin/env python3
"""ArchitectByAI — Batch 03 pilot: a classifier learns two intertwined spirals.
Original NumPy/Pillow/FFmpeg motion graphics; synthetic data and a genuine
regularized gradient-descent classifier on random Fourier features.
Reproduce: python animation.py --out pilot.mp4
Requirements: numpy, pillow, ffmpeg on PATH.
"""
import argparse, math, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H,FPS,DURATION=540,960,20,18
BG=(7,12,28); CYAN=(73,231,224); CORAL=(255,128,160); WHITE=(241,248,255)
BASE=Path(__file__).resolve().parent
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def font(sz,bold=False): return ImageFont.truetype(BOLD if bold else FONT,sz)
F10=font(12); F12=font(14); F16=font(16); F20=font(20,1); F26=font(26,1); F31=font(31,1)

def smooth(x):
    x=np.clip(x,0,1);return x*x*(3-2*x)
def make_data():
    rng=np.random.default_rng(2037)
    u=np.linspace(.1,1,105); theta=4.25*np.pi*u
    r=.09+.80*u
    points=[];labels=[]
    for k in (0,1):
        angle=theta+k*np.pi
        p=np.column_stack([r*np.cos(angle),r*np.sin(angle)])+rng.normal(0,.024,(len(r),2))
        points.append(p);labels.extend([k]*len(r))
    return np.vstack(points),np.asarray(labels)

def learn(P,y,steps=440,nfeatures=280):
    rng=np.random.default_rng(741)
    freqs=rng.normal(size=(2,nfeatures))*7.3
    bias=rng.uniform(0,2*np.pi,nfeatures)
    def feature(X): return np.cos(X@freqs+bias)*np.sqrt(2/nfeatures)
    Z=feature(P); Y=2*y-1
    # Full-batch gradient descent on logistic loss + L2 regularization.
    w=np.zeros(nfeatures); b=0.; history=[]; acc=[]
    for i in range(steps+1):
        if i%8==0:
            history.append((w.copy(),b)); acc.append(float(np.mean(((Z@w+b)>0)==y)))
        scores=np.clip(Z@w+b,-30,30)
        # derivative of logistic loss softplus(-Y*s)
        factor=-Y/(1+np.exp(Y*scores))
        dw=Z.T@factor/len(P)+.0015*w
        db=np.mean(factor)
        w-=3.5*dw;b-=3.5*db
    return feature,history,acc

def centered(draw,txt,y,ft,fill):
    bb=draw.textbbox((0,0),txt,font=ft);draw.text(((W-(bb[2]-bb[0]))/2,y),txt,font=ft,fill=fill)

def rounded(draw,xy,r,fill,outline=None,width=1):draw.rounded_rectangle(xy,r,fill=fill,outline=outline,width=width)

def render_frame(t,P,y,feature,history,acc):
    im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    # atmosphere, small fixed stars
    for x0,y0 in [(40,218),(485,234),(28,835),(498,841),(477,51)]:
        d.ellipse((x0-1,y0-1,x0+1,y0+1),fill=(44,80,108))
    d.text((30,31),'ARCHITECTBYAI  |  AI VISUAL LAB',font=F12,fill=CYAN)
    d.text((30,77),'CAN AI UNTANGLE',font=F31,fill=WHITE)
    d.text((30,117),'TWO SPIRALS?',font=F31,fill=WHITE)
    d.text((30,168),'Follow for Python + AI made visible',font=F12,fill=(175,196,221))
    # graph panel
    left,top,size=24,231,492
    rounded(d,(left,top,left+size,top+size),22,fill=(14,25,45),outline=(49,70,90),width=2)
    # square inner plot
    L,T,S=43,261,454
    # classification model evolves on actual optimisation updates
    plotH=350;plotT=291; plotB=plotT+plotH
    gx=np.linspace(-1.02,1.02,124); gy=np.linspace(-1.02,1.02,96)
    G=np.stack(np.meshgrid(gx,gy),axis=-1).reshape(-1,2)
    idx=int(np.clip((t-2.0)/10.1,0,1)*(len(history)-1))
    w,b=history[idx]
    raw=(feature(G)@w+b).reshape(96,124)
    amp=np.tanh(raw*1.6)
    a=np.maximum(amp,0)[:,:,None];c=np.maximum(-amp,0)[:,:,None]
    # evolving discriminant field blended into panel, never deceptive 'prediction accuracy'
    base=np.zeros((96,124,3),dtype=np.float32);base[:]=[15,28,49]
    base+=a*np.array([44,106,103])+c*np.array([116,40,61])
    field=Image.fromarray(base.clip(0,255).astype('uint8'),'RGB').resize((454,350),Image.Resampling.BILINEAR)
    im.paste(field,(L,plotT));d=ImageDraw.Draw(im)
    # grid drawn on top of inference field
    for v in range(0,455,57):d.line((L+v,plotT,L+v,plotB),fill=(42,62,82),width=1)
    for v in range(0,351,58):d.line((L,plotT+v,L+454,plotT+v),fill=(42,62,82),width=1)
    d.line((L+227,plotT,L+227,plotB),fill=(75,96,112),width=1)
    d.line((L,plotT+175,L+454,plotT+175),fill=(75,96,112),width=1)
    # growing synthetic spiral points, bright and dynamic
    reveal=smooth((t-.15)/2.1); count=int(reveal*105)
    for k in (0,1):
        for p in P[k*105:k*105+count]:
            x=L+227+p[0]*212; yy=plotT+175-p[1]*161
            if L+2<x<L+452 and plotT+2<yy<plotB-2:
                col=CYAN if k==0 else CORAL
                d.ellipse((x-2.4,yy-2.4,x+2.4,yy+2.4),fill=col)
    # training progress info with reproducible, measured training-set accuracy
    d.text((L+12,top+14),'SYNTHETIC DATA  /  TWO CLASSES',font=F10,fill=(158,188,205))
    d.text((L+5,650),'CLASS A',font=F12,fill=CYAN);d.text((L+119,650),'CLASS B',font=F12,fill=CORAL)
    d.text((L+260,650),'TRAINING',font=F12,fill=(155,184,203))
    accuracy=acc[idx]
    d.text((L+348,650),f'{accuracy*100:.0f}%',font=F20,fill=WHITE)
    # moving progress meter
    d.rounded_rectangle((L+6,687,L+448,696),5,fill=(35,54,73))
    if t>2:
        v=int(442*smooth((t-2)/10.1))
        d.rounded_rectangle((L+6,687,L+6+max(4,v),696),5,fill=CYAN)
    # readable stage explanation
    if t<2.5: lines=['TWO PATTERNS.','ONE CHALLENGE.']
    elif t<6: lines=['A STRAIGHT LINE','CANNOT SEPARATE THEM.']
    elif t<12:lines=['THE MODEL LEARNS','A CURVED BOUNDARY.']
    elif t<14:lines=['A NONLINEAR MODEL','CAN RECOGNIZE THE SHAPE.']
    elif t<16:lines=['SAVE THIS INSIGHT:','FEATURES MAKE CURVES POSSIBLE.']
    else: lines=[]
    if t<16:
        centered(d,lines[0],765,F20,WHITE)
        centered(d,lines[1],800,F16,(159,209,220))
        if 14<=t<16:
            centered(d,'RANDOM FOURIER FEATURES + LOGISTIC LOSS',856,F10,CYAN)
        else:
            centered(d,'Original Python experiment  •  synthetic training data',862,F10,(121,153,171))
        centered(d,'@architectbyai',912,F12,(154,180,198))
    else:
        # One featured service; website always present, no price
        d.rounded_rectangle((18,736,522,942),24,fill=(18,38,56),outline=CYAN,width=2)
        centered(d,'FROM DATA TO DECISIONS',756,F20,WHITE)
        centered(d,'DATA INTELLIGENCE',798,F26,CYAN)
        centered(d,'Explore our analytics service',839,F16,WHITE)
        centered(d,'architectbyai.com',881,F20,WHITE)
        centered(d,'Follow @architectbyai',918,F10,(171,192,204))
    return im

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default=str(BASE/'Batch03_01_SpiralAI.mp4'));ap.add_argument('--fps',type=int,default=FPS);ap.add_argument('--duration',type=float,default=DURATION);args=ap.parse_args()
    P,y=make_data();feat,hist,acc=learn(P,y)
    print('training accuracy',acc[0],acc[-1], 'steps',len(hist),flush=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(args.fps),'-i','pipe:0','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',args.out]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for i in range(round(args.duration*args.fps)):
        t=i/args.fps
        im=render_frame(t,P,y,feat,hist,acc)
        proc.stdin.write(im.tobytes())
        if i%60==0:print('frame',i,flush=True)
    proc.stdin.close();ret=proc.wait()
    if ret:raise RuntimeError('ffmpeg failed')
    render_frame(.05,P,y,feat,hist,acc).save(BASE/'thumbnail.png')
    for key,t in [('opening',.05),('progress',7),('reveal',12.5),('save',15),('end',17.1)]:render_frame(t,P,y,feat,hist,acc).save(BASE/f'{key}.png')
    print('rendered',args.out,flush=True)
if __name__=='__main__':main()

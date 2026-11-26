#!/usr/bin/env python3
"""ArchitectByAI AI Visual Lab — Video 06, real K-means grouping on synthetic data.
Run: python animation.py --output file.mp4. Requires numpy, Pillow and FFmpeg.
Rendered at 540x960, delivered at Lanczos-upscaled 1080x1920.
"""
import argparse, math, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W,H,FPS,SECONDS=540,960,20,18
ROOT=Path(__file__).resolve().parent
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
NAVY=(7,13,27); INK=(15,27,49); WHITE=(242,247,255)
CYAN=(81,230,224); PINK=(252,131,163); GOLD=(253,203,113)
COLORS=[CYAN,PINK,GOLD]

def ft(s,bold=False):return ImageFont.truetype(BOLD if bold else FONT,s)
def ease(z):
 z=max(0,min(1,z));return z*z*(3-2*z)
def lerp(a,b,u):return a+(b-a)*u

def dataset():
 r=np.random.default_rng(20261126)
 centers=np.array([[-.63,.40],[.59,.53],[.10,-.61]])
 clouds=[r.normal(loc=c,scale=[.19,.17],size=(34,2)) for c in centers]
 X=np.vstack(clouds)
 # A deliberately poor initial seed demonstrates genuine iterative K-means repositioning.
 seeds=np.array([[-.86,-.70],[.80,-.65],[-.78,.72]],dtype=float)
 hist=[seeds.copy()];labels=[]
 for i in range(12):
  d=((X[:,None,:]-seeds[None,:,:])**2).sum(axis=2)
  lab=np.argmin(d,axis=1); labels.append(lab.copy())
  updated=np.array([X[lab==k].mean(axis=0) if np.any(lab==k) else seeds[k] for k in range(3)])
  hist.append(updated.copy())
  if np.allclose(updated,seeds):break
  seeds=updated
 final=np.argmin(((X[:,None,:]-hist[-1][None,:,:])**2).sum(axis=2),axis=1)
 return X,np.array(hist),final

def center(draw,string,y,size,color=WHITE,bold=False):
 f=ft(size,bold); b=draw.textbbox((0,0),string,font=f)
 draw.text(((W-(b[2]-b[0]))/2,y),string,font=f,fill=color)

def pill(draw,rect,fill,stroke=None,radius=14,w=1):
 draw.rounded_rectangle(rect,radius=radius,fill=fill,outline=stroke,width=w)

def render(t,X,hist,final):
 im=Image.new('RGB',(W,H),NAVY); d=ImageDraw.Draw(im)
 # Decorative curved traces along the background
 for j in range(7):
  y=174+j*106
  d.arc((-230,y-120,790,y+640),195,306,fill=(18,35,58),width=1)
 d.text((28,26),'ARCHITECTBYAI  |  AI VISUAL LAB',font=ft(14,True),fill=CYAN)
 d.text((28,72),'CAN DATA REVEAL',font=ft(31,True),fill=WHITE)
 d.text((28,111),'HIDDEN GROUPS?',font=ft(31,True),fill=WHITE)
 d.text((28,165),'Follow for visual AI + Python experiments',font=ft(13),fill=(166,189,211))
 pill(d,(19,218,521,724),INK,(48,70,95),22,2)
 d.text((39,238),'102 SYNTHETIC DATA POINTS',font=ft(13,True),fill=(178,205,219))
 d.text((405,237),'K = 3',font=ft(17,True),fill=GOLD)
 L,T,S=73,285,394
 for ix in range(9):
  x=L+ix*S/8;d.line((x,T,x,T+S),fill=(29,47,70))
  y=T+ix*S/8;d.line((L,y,L+S,y),fill=(29,47,70))
 def project(p):return L+S*(p[0]+1.25)/2.5,T+S*(1.25-p[1])/2.5
 # Reveal point cloud right away, with a moving wave and subtle bounce.
 reveal=ease((t+.2)/2.3)
 # clustering transitions are exact nearest-centroid labels at interpolated current centers
 phase=ease((t-3.2)/9.7)
 steps=phase*(len(hist)-1)
 idx=min(int(steps),len(hist)-2);alpha=steps-idx
 C=hist[idx]*(1-alpha)+hist[idx+1]*alpha
 assignments=np.argmin(((X[:,None,:]-C[None,:,:])**2).sum(axis=2),axis=1)
 for i,p in enumerate(X):
  if i>=math.floor(reveal*len(X)):continue
  x,y=project(p)
  # Make points animate gently, preserving data classification and coordinate story.
  y+=2.4*math.sin(t*3.5+i*1.8)
  c=(109,139,164) if t<3.2 else COLORS[int(assignments[i])]
  rad=3.8 if t<3.2 else 4.5
  d.ellipse((x-rad,y-rad,x+rad,y+rad),fill=c)
 # K-means centroid animation only after 'algorithm' starts
 if t>=3.2:
  for j,c in enumerate(C):
   x,y=project(c); r=13+1.8*math.sin(t*5+j)
   d.ellipse((x-r-6,y-r-6,x+r+6,y+r+6),outline=COLORS[j],width=2)
   d.ellipse((x-r,y-r,x+r,y+r),fill=COLORS[j],outline=WHITE,width=2)
   d.line((x-7,y,x+7,y),fill=NAVY,width=3);d.line((x,y-7,x,y+7),fill=NAVY,width=3)
 d.text((43,690),'SCATTER',font=ft(12),fill=(135,166,191))
 d.text((172,690),'ASSIGN  →  UPDATE  →  REPEAT',font=ft(12,True),fill=(167,205,221))
 if t<3.2:
  a='A CLOUD OF NUMBERS.';b='DO YOU SEE THREE GROUPS?'
 elif t<7.4:
  a='1. ASSIGN EACH POINT';b='TO ITS NEAREST CENTER.'
 elif t<11.7:
  a='2. MOVE EACH CENTER';b='TO ITS GROUP AVERAGE.'
 elif t<14:
  a='REPEAT UNTIL THE';b='CENTERS STOP MOVING.'
 elif t<16:
  a='SAVE THIS: K-MEANS';b='FINDS SIMILAR DATA GROUPS.'
 else:a='';b=''
 if t<16:
  center(d,a,752,23,WHITE,True);center(d,b,796,18,CYAN if t>=14 else (181,215,233),True)
  if 14<=t<16:
   center(d,'UNSUPERVISED LEARNING  •  K = 3',854,13,GOLD)
  else:
   center(d,'Actual NumPy K-means  |  Illustrative dataset',853,12,(154,177,196))
  center(d,'@architectbyai',915,14,(173,196,214))
 else:
  pill(d,(18,733,522,947),(19,40,61),CYAN,23,2)
  center(d,'TURN INSIGHTS INTO ACTION',750,21,WHITE,True)
  center(d,'MARKETING & CUSTOMER',791,23,CYAN,True)
  center(d,'COMMUNICATION KIT',825,23,CYAN,True)
  center(d,'Explore at architectbyai.com',867,17,WHITE,True)
  center(d,'Follow @architectbyai',914,12,(178,200,218))
 return im

def main():
 pa=argparse.ArgumentParser();pa.add_argument('--output',default=str(ROOT/'B03_V06_Hidden_Groups_1080x1920.mp4'));pa.add_argument('--fps',type=int,default=FPS);args=pa.parse_args()
 X,hist,final=dataset()
 counts=np.bincount(final,minlength=3).tolist()
 print('N',len(X),'steps',len(hist)-1,'cluster sizes',counts,flush=True)
 argsff=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(args.fps),'-i','pipe:0','-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',args.output]
 p=subprocess.Popen(argsff,stdin=subprocess.PIPE)
 try:
  for k in range(args.fps*SECONDS):
   im=render(k/args.fps,X,hist,final);p.stdin.write(im.tobytes())
   if k%90==0:print('frame',k,flush=True)
 finally:p.stdin.close()
 if p.wait()!=0:raise RuntimeError('FFmpeg render failed')
 render(.15,X,hist,final).save(ROOT/'cover.png')
 for n,t in [('opening',.1),('middle',5),('clusters',12),('save',15),('end',17)]:render(t,X,hist,final).save(ROOT/(n+'.png'))
 print('DONE',args.output)
if __name__=='__main__':main()
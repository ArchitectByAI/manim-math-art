#!/usr/bin/env python3
"""ArchitectByAI Creative Growth Studio — Pilot CGS-2026-11-18-001.

A scientifically faithful synthetic demonstration of Simpson's paradox:
within each of two groups the least-squares slope is positive, while
pooled observations have a negative slope. Original procedural animation.

Requires: Python 3.10+, numpy, Pillow, FFmpeg on PATH.
Usage:
  python simpsons_paradox.py --out pilot.mp4             # 1080 x 1920, 24 fps
  python simpsons_paradox.py --out proof.mp4 --width 540 --fps 12
  python simpsons_paradox.py --still 0.0 --out first.png
"""
from __future__ import annotations
import argparse
import os
import math
import subprocess
import wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_W, BASE_H = 1080, 1920
DURATION = 18.0
SEED = 82417
def find_font(linux_name, windows_name):
 # Font files are NOT included; choose locally installed system fonts.
 for path in (os.environ.get('ARCHITECTBYAI_FONT_DIR', '') and str(Path(os.environ['ARCHITECTBYAI_FONT_DIR']) / linux_name),
              f'/usr/share/fonts/opentype/inter/{linux_name}',
              f'C:/Windows/Fonts/{windows_name}',
              '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'):
  if path and Path(path).exists():return path
 raise FileNotFoundError('No suitable font found: set ARCHITECTBYAI_FONT_DIR to a directory of InterDisplay fonts')
FONT_REG=find_font('InterDisplay-Regular.otf','arial.ttf')
FONT_MED=find_font('InterDisplay-Medium.otf','arial.ttf')
FONT_BOLD=find_font('InterDisplay-Bold.otf','arialbd.ttf')
FONT_BLACK=find_font('InterDisplay-ExtraBold.otf','ariblk.ttf')
CYAN=(85,238,235); CORAL=(255,171,138); CREAM=(250,249,239); MUTED=(150,165,190)

rng=np.random.default_rng(SEED)
x_a=np.linspace(1.15,3.86,28)+rng.normal(0,0.09,28)
x_b=np.linspace(6.16,8.87,28)+rng.normal(0,0.09,28)
y_a=6.38+0.65*(x_a-1.15)+rng.normal(0,0.22,28)
y_b=1.52+0.65*(x_b-6.16)+rng.normal(0,0.22,28)
A=np.column_stack([x_a,y_a]); B=np.column_stack([x_b,y_b]); ALL=np.vstack([A,B])
pa=np.polyfit(x_a,y_a,1);pb=np.polyfit(x_b,y_b,1); pall=np.polyfit(ALL[:,0],ALL[:,1],1)
assert pa[0]>0 and pb[0]>0 and pall[0]<0, 'Dataset does not exhibit Simpson reversal'

# Use a single fixed dataset, do not move points after data has settled.
def clamp(x,a=0.0,b=1.0):return max(a,min(b,x))
def smooth(x):
 x=clamp(x);return x*x*(3-2*x)
def interp(a,b,t):return a+(b-a)*t
def rgb_interp(a,b,t):return tuple(int(interp(x,y,t)) for x,y in zip(a,b))
def point_coords(x,y):
 return (round(interp(118,955,x/10)),round(interp(1395,620,y/10)))

class Renderer:
 def __init__(self,width=1080):
  self.W=width;self.H=round(width*16/9)
  self.scale=self.W/BASE_W
  self.fonts={}
  self.background=self.make_background()
  self.dot_a=self.make_dot(CYAN)
  self.dot_b=self.make_dot(CORAL)
  self.start_pos=rng.uniform(-0.65,0.65,(56,2))
  self.phase=rng.uniform(0,6.28,(56,))
 def sc(self,x):return int(round(x*self.scale))
 def box(self,x0,y0,x1,y1):return tuple(self.sc(v) for v in (x0,y0,x1,y1))
 def font(self,size,kind='bold'):
  key=(size,kind)
  if key not in self.fonts:
   fn={'regular':FONT_REG,'medium':FONT_MED,'bold':FONT_BOLD,'black':FONT_BLACK}[kind]
   self.fonts[key]=ImageFont.truetype(fn,max(1,self.sc(size)))
  return self.fonts[key]
 def make_background(self):
  w,h=self.W,self.H
  yy,xx=np.mgrid[0:h,0:w]
  nx=xx/max(w-1,1);ny=yy/max(h-1,1)
  bloom=np.exp(-((nx-.27)**2/.29+(ny-.35)**2/.17))
  lilac=np.exp(-((nx-.84)**2/.13+(ny-.80)**2/.21))
  arr=np.zeros((h,w,3),dtype=np.uint8)
  # Midnight sapphire; large diffuse fields, no stock texture.
  for k,(base,bv,lv) in enumerate(((7,14,12),(12,22,12),(30,30,30))):
   arr[:,:,k]=np.clip(base+bv*bloom+lv*lilac,0,255).astype('uint8')
  img=Image.fromarray(arr,'RGB')
  d=ImageDraw.Draw(img)
  # Fine technical grid with reserved vertical breathing room.
  for x in range(100,985,90):d.line((self.sc(x),self.sc(570),self.sc(x),self.sc(1460)),fill=(20,35,54),width=max(1,self.sc(1)))
  for y in range(595,1440,90):d.line((self.sc(94),self.sc(y),self.sc(984),self.sc(y)),fill=(20,35,54),width=max(1,self.sc(1)))
  d.rounded_rectangle(self.box(74,532,1005,1508),radius=self.sc(42),outline=(55,71,94),width=max(1,self.sc(2)))
  # Background edge/corner ornaments.
  d.line((self.sc(78),self.sc(500),self.sc(140),self.sc(500)),fill=(62,194,216),width=max(1,self.sc(4)))
  d.line((self.sc(920),self.sc(500),self.sc(1000),self.sc(500)),fill=(62,194,216),width=max(1,self.sc(4)))
  return img
 def make_dot(self,color):
  n=self.sc(42);n=max(n,8); rad=n/2
  yy,xx=np.mgrid[0:n,0:n];dd=np.sqrt((xx-rad)**2+(yy-rad)**2)/(rad)
  a=np.clip(65*np.exp(-dd*dd*8)+200*np.exp(-dd*dd*100),0,245).astype(np.uint8)
  out=np.zeros((n,n,4),dtype=np.uint8)
  out[:,:,:3]=color;out[:,:,3]=a
  return Image.fromarray(out,'RGBA')
 def text(self,draw,text,x,y,size,color=CREAM,kind='bold',anchor='la',spacing=8):
  draw.multiline_text((self.sc(x),self.sc(y)),text,font=self.font(size,kind),fill=color,anchor=anchor,spacing=self.sc(spacing))
 def pill(self,draw,xy,word,bg,fg,size=24,pad=20):
  x,y=xy;f=self.font(size,'bold');bbox=draw.textbbox((0,0),word,font=f)
  w=(bbox[2]-bbox[0])/self.scale+2*pad
  draw.rounded_rectangle(self.box(x,y,x+w,y+49),radius=self.sc(23),fill=bg)
  self.text(draw,word,x+pad,y+11,size,fg)
  return w
 def stroke(self,draw,pts,col,width,progress=1.0):
  p=clamp(progress)
  if p<=0:return
  pts=np.array(pts,dtype=float)
  last=(len(pts)-1)*p
  n=int(last)
  points=[tuple(int(v) for v in a) for a in pts[:n+1]]
  if n+1<len(pts):points.append(tuple(int(v) for v in pts[n]+(pts[n+1]-pts[n])*(last-n)))
  if len(points)>1:draw.line(points,fill=col,width=max(1,self.sc(width)),joint='curve')
 def regression_line(self,slope,intercept,xrange=(0.75,9.25),n=75):
  points=[]
  for x in np.linspace(*xrange,n):
   y=slope*x+intercept
   xy=point_coords(x,y)
   points.append((self.sc(xy[0]),self.sc(xy[1])))
  return points
 def draw_axes(self,d,t):
  axis=(100,121,151)
  x0,y0=point_coords(0,0); x1,_=point_coords(10,0); _,y1=point_coords(0,10)
  d.line((self.sc(x0),self.sc(y0),self.sc(x1),self.sc(y0)),fill=axis,width=max(1,self.sc(2)))
  d.line((self.sc(x0),self.sc(y0),self.sc(x0),self.sc(y1)),fill=axis,width=max(1,self.sc(2)))
  self.text(d,'X  /  PREDICTOR',550,1420,19,(130,148,175),'medium',anchor='ma')
  self.text(d,'SYNTHETIC DATA  /  REGRESSION',122,565,18,(122,145,175),'medium')
 def draw_points(self,frame,t):
  progress=smooth(t/2.3)
  particles=np.vstack([A,B]); draw=ImageDraw.Draw(frame)
  for i,(x,y) in enumerate(particles):
   tx,ty=point_coords(x,y)
   ang=self.phase[i]
   # Orbital entry around each true coordinate, then lock in place.
   swirl=(1-progress)*105
   cx=tx+math.cos(ang+6.0*t)*swirl+math.sin(ang*1.3)*(1-progress)*26
   cy=ty+math.sin(ang+6.0*t)*swirl
   col=CYAN if i<28 else CORAL
   sr=self.dot_a if i<28 else self.dot_b
   px=self.sc(cx)-sr.width//2;py=self.sc(cy)-sr.height//2
   frame.paste(sr,(px,py),sr)
   r=self.sc(5)
   draw.ellipse((self.sc(cx)-r,self.sc(cy)-r,self.sc(cx)+r,self.sc(cy)+r),fill=col)
 def draw_top(self,d,t):
  self.text(d,'A  /  A R C H I T E C T B Y A I',86,90,29,(162,188,213),'medium')
  d.rounded_rectangle(self.box(81,150,995,206),radius=self.sc(24),fill=(23,41,63),outline=(39,75,98),width=max(1,self.sc(1)))
  self.text(d,'FOLLOW  ·  VISUAL PYTHON / AI / DATA',108,163,26,(129,236,232),'bold')
  if t<3.0:
   self.text(d,'CAN THE SAME DATA',82,252,75,CREAM,'black')
   self.text(d,'POINT BOTH WAYS?',82,342,73,(125,237,234),'black')
   self.text(d,'WATCH THE TREND CHANGE.',85,452,27,MUTED,'medium')
  elif t<6.15:
   self.text(d,'TWO GROUPS.',82,252,93,CREAM,'black')
   self.text(d,'BOTH RISE.',82,355,93,CYAN,'black')
  elif t<9.55:
   self.text(d,'NOW COMBINE',82,254,86,CREAM,'black')
   self.text(d,'THE DATA.',82,356,90,CORAL,'black')
  else:
   self.text(d,'ONE DATASET.',82,258,82,CREAM,'black')
   self.text(d,'OPPOSITE TREND.',82,352,71,(255,201,171),'black')
 def line_draw(self,d,t):
  aa=self.regression_line(*pa, xrange=(1.0,4.05))
  bb=self.regression_line(*pb, xrange=(6.0,9.1))
  combined=self.regression_line(*pall,xrange=(0.65,9.4))
  if t>=2.25:
   a=smooth((t-2.5)/1.3);b=smooth((t-3.9)/1.3)
   if t>7.2:
    col_a=(53,135,140); col_b=(148,95,80)
   else:
    col_a=CYAN;col_b=CORAL
   self.stroke(d,aa,col_a,8,a);self.stroke(d,bb,col_b,8,b)
   if 3.1<t<7.1:
    self.pill(d,(160,684),'GROUP A  /  UP', (18,63,72),CYAN,23)
    self.pill(d,(634,1177),'GROUP B  /  UP',(75,43,48),CORAL,23)
  if t>=6.5:
   q=smooth((t-6.6)/2.25)
   if q>0:
    self.stroke(d,combined,(80,71,85),22,q)
    self.stroke(d,combined,(247,236,209),8,q)
    # Direction cue: arrow at the descending line endpoint when complete.
    if q>.9:
     xa,ya=combined[-1];sc=self.sc
     d.line((xa-sc(28),ya-sc(24),xa,ya),fill=(255,233,201),width=max(1,sc(8)))
     d.line((xa-sc(26),ya+sc(21),xa,ya),fill=(255,233,201),width=max(1,sc(8)))
   # From the reveal through the insight, a luminous indicator travels the
   # pooled trend. This keeps the mathematical story evolving on screen.
   if t>=9.55:
    phase=(t-9.55)/4.3
    travel=0.5-0.5*math.cos(phase*2*math.pi)
    ix=round(travel*(len(combined)-1))
    cx,cy=combined[ix]
    radius=self.sc(15+4*math.sin(t*5)**2)
    d.ellipse((cx-radius*2,cy-radius*2,cx+radius*2,cy+radius*2),outline=(109,198,199),width=max(2,self.sc(2)))
    d.ellipse((cx-radius,cy-radius,cx+radius,cy+radius),fill=(255,246,218))
 def bottom(self,d,t):
  if t<3:
   self.text(d,'01  /  WATCH THE PATTERN',87,1540,26,(132,148,184),'medium')
   self.text(d,'One dataset. Two hidden groups.',87,1597,39,CREAM,'bold')
   self.text(d,'The answer is not what it seems.',88,1662,30,MUTED,'medium')
  elif t<6.3:
   self.text(d,'02  /  WITHIN EACH GROUP',87,1540,25,(132,148,184),'medium')
   self.text(d,'Both trend lines slope upward.',87,1597,37,CREAM,'bold')
   self.text(d,'Group matters more than you think.',87,1662,29,MUTED,'medium')
  elif t<9.6:
   self.text(d,'03  /  COMBINED',87,1540,25,(132,148,184),'medium')
   self.text(d,'Now the trend points DOWN.',87,1597,42,CREAM,'bold')
   self.text(d,'The groups have different baselines.',87,1662,29,MUTED,'medium')
  else:
   self.text(d,'04  /  THE REVEAL',87,1540,25,(132,148,184),'medium')
   self.text(d,"This is Simpson's paradox.",87,1597,41,CREAM,'bold')
   self.text(d,'Pooling can reverse the relationship.',87,1662,28,MUTED,'medium')
  d.line((self.sc(87),self.sc(1764),self.sc(993),self.sc(1764)),fill=(48,67,87),width=max(1,self.sc(2)))
  self.text(d,'ENGINEERED INTELLIGENCE',87,1795,24,(152,178,204),'medium')
  self.text(d,'@architectbyai',820,1795,23,CYAN,'medium')
 def save_card(self,d):
  d.rounded_rectangle(self.box(66,235,1014,1655),radius=self.sc(56),fill=(11,29,49),outline=(76,134,150),width=max(2,self.sc(4)))
  self.text(d,'SAVE THIS EXPLANATION',540,340,28,CYAN,'bold',anchor='ma')
  self.text(d,"SIMPSON'S",540,520,99,CREAM,'black',anchor='ma')
  self.text(d,'PARADOX',540,635,111,CREAM,'black',anchor='ma')
  d.line((self.sc(135),self.sc(827),self.sc(945),self.sc(827)),fill=(56,94,111),width=max(2,self.sc(3)))
  self.text(d,'WITHIN GROUPS',130,915,33,(167,186,208),'medium')
  self.text(d,'UPWARD TREND',130,965,66,CYAN,'black')
  self.text(d,'WHEN POOLED',130,1130,33,(167,186,208),'medium')
  self.text(d,'DOWNWARD TREND',130,1180,61,CORAL,'black')
  self.text(d,'Grouping changes the answer.',135,1412,36,CREAM,'bold')
  self.text(d,'Synthetic example  ·  least-squares fits',135,1501,24,(147,164,185),'medium')
  self.text(d,'FOLLOW · VISUAL DATA SCIENCE',540,1710,27,CYAN,'bold',anchor='ma')
 def end_card(self,d,t):
  # Sole featured offer: upcoming visual learning series (not open enrollment).
  d.rounded_rectangle(self.box(61,238,1017,1670),radius=self.sc(54),fill=(9,28,49),outline=(56,141,151),width=max(2,self.sc(4)))
  self.text(d,'ARCHITECTBYAI  /  EDUCATION',540,334,30,CYAN,'bold',anchor='ma')
  d.line((self.sc(157),self.sc(428),self.sc(923),self.sc(428)),fill=(60,99,111),width=max(2,self.sc(2)))
  self.text(d,'COMING',540,562,130,CREAM,'black',anchor='ma')
  self.text(d,'SOON',540,700,158,CYAN,'black',anchor='ma')
  self.text(d,'VISUAL',540,985,101,CREAM,'black',anchor='ma')
  self.text(d,'DATA SCIENCE',540,1094,84,CREAM,'black',anchor='ma')
  self.text(d,'LESSONS',540,1193,99,CREAM,'black',anchor='ma')
  self.text(d,'PYTHON  ·  DATA  ·  REAL EXPERIMENTS',540,1383,29,(184,207,223),'medium',anchor='ma')
  self.text(d,'architectbyai.com',540,1531,50,(131,239,228),'bold',anchor='ma')
  self.text(d,'FOLLOW FOR THE NEXT VISUAL PROOF',540,1762,28,CYAN,'bold',anchor='ma')
 def frame(self,t):
  im=self.background.copy();d=ImageDraw.Draw(im)
  if t>=16.0:
   self.end_card(d,t);return im
  if t>=14.0:
   self.save_card(d);return im
  self.draw_axes(d,t)
  self.draw_points(im,t)
  d=ImageDraw.Draw(im)
  self.line_draw(d,t)
  self.draw_top(d,t)
  self.bottom(d,t)
  return im

def make_sound(out_path:Path):
 """Generated original subtle ambient cue, no third-party audio used."""
 sr=24000
 n=int(DURATION*sr)
 t=np.arange(n,dtype=np.float64)/sr
 y=np.zeros(n,dtype=np.float64)
 for j,(start,dur,freq) in enumerate([(0.0,3.0,174.6),(3.0,3.5,220.0),(6.5,3.0,130.8),(9.5,4.3,196.0),(14.0,2.0,261.6),(16.0,2.0,329.6)]):
  mask=(t>=start)&(t<start+dur)
  u=t[mask]-start
  env=(1-np.exp(-u*6.5))*np.minimum(1,(dur-u)/0.9)
  chord=.48*np.sin(2*np.pi*freq*u)+.21*np.sin(2*np.pi*freq*1.501*u)+.10*np.sin(2*np.pi*freq*2.003*u)
  y[mask]+=chord*env*.13
 # light soft transient at reveal, with deterministic noise
 r=np.random.default_rng(4567)
 for start in [0,3.0,6.5,9.5,14.0,16.0]:
  mask=(t>=start)&(t<start+.24); u=t[mask]-start
  y[mask]+=.028*np.sin(2*np.pi*(500-200*u)*u)*np.exp(-u*20)
 y=np.tanh(y*1.4)
 pcm=(y*32767).astype(np.int16)
 with wave.open(str(out_path),'wb') as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(pcm.tobytes())

def render(output,width,fps,with_audio=True):
 r=Renderer(width)
 out=Path(output).resolve();out.parent.mkdir(parents=True,exist_ok=True)
 audio=out.with_suffix('.original_sound.wav')
 if with_audio:make_sound(audio)
 cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{r.W}x{r.H}','-r',str(fps),'-i','-']
 if with_audio:cmd+=['-i',str(audio),'-shortest','-c:a','aac','-b:a','128k']
 else:cmd+=['-an']
 cmd+=['-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(out)]
 p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
 try:
  for i in range(round(DURATION*fps)):
   fr=r.frame(i/fps)
   p.stdin.write(fr.tobytes())
   if i and i%max(1,2*fps)==0:print(f'{i/(fps):.0f}s / {DURATION:.0f}s',flush=True)
  p.stdin.close();err=p.stderr.read();status=p.wait()
 except Exception:
  p.kill();p.wait();raise
 if status:raise RuntimeError(f'ffmpeg failed: {err.decode("utf-8",errors="replace")}')
 if with_audio and audio.exists():audio.unlink()
 print(f'Rendered {out} ({r.W}x{r.H}, {fps}fps, {DURATION}s)')

if __name__=='__main__':
 ap=argparse.ArgumentParser()
 ap.add_argument('--out',default='CGS_Simpsons_Paradox_Pilot.mp4')
 ap.add_argument('--width',type=int,default=1080)
 ap.add_argument('--fps',type=int,default=24)
 ap.add_argument('--still',type=float,default=None)
 ap.add_argument('--silent',action='store_true')
 a=ap.parse_args()
 if a.width%2:ap.error('--width must be even')
 if a.still is not None:
  Renderer(a.width).frame(a.still).save(a.out)
 else:render(a.out,a.width,a.fps,not a.silent)
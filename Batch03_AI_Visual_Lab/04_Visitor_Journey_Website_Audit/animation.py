#!/usr/bin/env python3
"""ArchitectByAI Creative Growth Studio, B03/V04.
Original procedural video illustrating a fictional website visitor journey.
Every statistic is explicitly hypothetical and should not be attributed to a real website.
Requires Pillow and ffmpeg. Run: python animation.py
"""
from PIL import Image, ImageDraw, ImageFont
import math, subprocess, random
from pathlib import Path

OUT=Path(__file__).resolve().parent
W,H=540,960
FPS=20
SECONDS=18
NAVY=(6,13,28); WHITE=(240,248,253); MUTE=(145,172,188)
ICE=(104,229,231); AMBER=(253,187,91); PINK=(244,109,161)
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
REG='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def F(n,bold=False):return ImageFont.truetype(BOLD if bold else REG,n)
def smooth(x):
 x=max(0,min(1,x)); return x*x*(3-2*x)
def mix(a,b,t):return a+(b-a)*t

def alpha(draw,text,x,y,sz,color,bold=False,anchor=None):
 draw.text((x,y),text,fill=color,font=F(sz,bold),anchor=anchor)

def center(draw,text,y,sz,color=WHITE,bold=False):
 alpha(draw,text,W/2,y,sz,color,bold,'mt')

def panel(draw,rect,fill=(14,30,49),stroke=(41,74,91),r=18,width=2):
 draw.rounded_rectangle(rect,radius=r,fill=fill,outline=stroke,width=width)

rng=random.Random(21)
particles=[]
for k in range(112):
 # particles appear, travel vertically, and exit progressively at 'friction' gates
 x=58+(k%14)*30+rng.uniform(-6,6)
 y=323+(k//14)*24
 particles.append((x,y,rng.uniform(-5,5),rng.uniform(0,2*math.pi)))

def frame(t):
 im=Image.new('RGB',(W,H),NAVY)
 d=ImageDraw.Draw(im)
 # fine understated background texture and grids
 for gx in range(26,W,42): d.line((gx,235,gx,747),fill=(14,30,47),width=1)
 for gy in range(247,739,42):d.line((25,gy,W-25,gy),fill=(14,30,47),width=1)
 for px,py in [(34,39),(496,52),(24,209),(492,774),(79,829)]: d.ellipse((px-1,py-1,px+1,py+1),fill=(57,92,113))
 alpha(d,'ARCHITECTBYAI  |  AI VISUAL LAB',29,36,14,ICE,True)
 if t<15.8:
  alpha(d,'WHERE DO YOUR',29,88,34,WHITE,True)
  alpha(d,'VISITORS GO?',29,131,34,WHITE,True)
 else:
  alpha(d,'WHAT IF YOUR WEBSITE',29,88,29,WHITE,True)
  alpha(d,'IS LOSING LEADS?',29,129,29,WHITE,True)
 alpha(d,'Follow @architectbyai for visual tech insights',29,188,13,(173,203,217))
 # graph stage with moving flow: illustrative conversion numbers
 panel(d,(24,248,516,727),fill=(10,25,44),stroke=(46,79,96))
 # main gates with strengths proportional to example
 stages=[('ARRIVE',100,304,ICE),('EXPLORE',42,430,AMBER),('CONTACT',9,555,PINK)]
 for idx,(label,amt,y,col) in enumerate(stages):
  d.rounded_rectangle((40,y-20,500,y+29),12,fill=(17,39,56),outline=(46,77,93),width=1)
  d.rounded_rectangle((42,y-18,42+int(455*amt/100),y+27),11,fill=tuple(int(c*.39) for c in col))
  alpha(d,label,54,y-13,15,WHITE,True)
  alpha(d,f'{amt} / 100',480,y-13,15,WHITE,True,'rt')
  if idx<2:
   # full-width conduits indicate transition; pulsing with animation
   d.line((270,y+33,270,y+86),fill=(39,70,85),width=4)
   v=(t*72)%45
   d.line((270,y+40+v/3,270,y+51+v/3),fill=col,width=4)
 # As time advances, flowing dots visibly fall through successive narrowing gates
 begin=smooth((t+.65)/1.8)
 n=int(begin*100)
 if t<4.8:
  for k in range(n):
   x0,y0,dx,ph=particles[k]
   xx=x0+math.sin(t*2+ph)*2
   yy=375+((k%10)*3)-min(22,smooth((t-2)/2)*28)
   d.ellipse((xx-2.5,yy-2.5,xx+2.5,yy+2.5),fill=ICE)
 elif t<8.1:
  # 42 retained, 58 leave stage 1; count is calculated not imaginary continuous animation
  q=smooth((t-4.7)/1.7)
  for k in range(100):
   x0,y0,dx,ph=particles[k]
   xx=70+(k%14)*28+math.sin(t*2+ph)*2
   if k<42: yy=mix(377,500,q);col=AMBER
   else:
    yy=mix(377,403,q); xx+=q*(95 if k%2 else -95);col=(72,92,105)
   d.ellipse((xx-2.3,yy-2.3,xx+2.3,yy+2.3),fill=col)
 else:
  q=smooth((t-8.1)/2)
  for k in range(42):
   x0,y0,dx,ph=particles[k]
   xx=100+(k%10)*36+math.sin(t*2+ph)*2
   if k<9: yy=mix(500,624,q);col=PINK
   else:yy=mix(500,531,q);xx+=q*(48 if k%2 else -48);col=(68,90,104)
   d.ellipse((xx-2.6,yy-2.6,xx+2.6,yy+2.6),fill=col)
 # timed stage story, progress highlight
 if t<4.0:
  msg1='100 VISITS';msg2='Every visit begins with a chance.'
 elif t<8:
  msg1='58 LEAVE EARLY';msg2='Only 42 explore further.'
 elif t<12:
  msg1='JUST 9 REACH CONTACT';msg2='The journey matters more than traffic.'
 elif t<14:
  msg1='FIND THE FRICTION';msg2='A website audit helps reveal issues.'
 elif t<16:
  msg1='SAVE THIS IDEA';msg2='Visits are not the same as leads.'
 else:
  msg1='';msg2=''
 if t<16:
  center(d,msg1,768,27,ICE,True)
  center(d,msg2,813,16,WHITE)
  center(d,'ILLUSTRATIVE EXAMPLE  |  NOT REAL SITE DATA',861,11,MUTE)
  center(d,'architectbyai.com',913,16,(195,211,224))
 else:
  panel(d,(20,746,520,944),fill=(17,39,58),stroke=ICE,r=20,width=2)
  center(d,'WEBSITE AUDIT',773,30,ICE,True)
  center(d,'Find what your visitors experience.',824,15,WHITE)
  center(d,'Explore our website audit service',853,14,WHITE)
  center(d,'architectbyai.com',897,20,WHITE,True)
 return im

def main():
 target=OUT/'B03_V04_Visitor_Journey_1080x1920.mp4'
 cmd=['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(target)]
 p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 for i in range(FPS*SECONDS):
  p.stdin.write(frame(i/FPS).tobytes())
 p.stdin.close()
 if p.wait()!=0:raise RuntimeError('ffmpeg encoder failed')
 frame(0).resize((1080,1920)).save(OUT/'cover.png')
 for name,t in [('opening',.1),('flow',6),('contact',11),('save',15),('end',17)]:frame(t).save(OUT/(name+'.png'))
 print(target)
if __name__=='__main__':main()
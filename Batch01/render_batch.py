"""ArchitectByAI Batch 01: procedural Python/Pillow animations (not Manim scenes).
Usage: python render_batch.py --episode 2  or  python render_batch.py --all
Requires numpy, Pillow, imageio, imageio-ffmpeg and FFmpeg.
"""
import math, random, argparse, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio.v2 as imageio
ROOT=Path(__file__).resolve().parent
W,H=540,960
FPS,DUR=15,12
N=FPS*DUR
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(s,b=False): return ImageFont.truetype(BOLD if b else FONT,s)
def mix(a,b,t): return a+(b-a)*max(0,min(1,t))
def ease(t): t=max(0,min(1,t));return t*t*(3-2*t)
def line(d,pts,c,w=2):
 if len(pts)>1:d.line(pts,fill=c,width=w,joint='curve')
def txt(d,s,y,size=20,color='#F3F5FF',bold=False):d.text((W//2,y),s,font=font(size,bold),fill=color,anchor='mm')
def node(d,x,y,r=7,col='#65DAF4'):
 d.ellipse((x-r*2,y-r*2,x+r*2,y+r*2),outline='#263B6D',width=2)
 d.ellipse((x-r,y-r,x+r,y+r),fill=col)
def base(k,title,sub,offer):
 im=Image.new('RGB',(W,H),(9,15,35));d=ImageDraw.Draw(im)
 for y in range(0,H,4):
  c=(9+int(y/H*3),15+int(y/H*5),35+int(y/H*12));d.rectangle((0,y,W,y+3),fill=c)
 txt(d,title,75,24,'#FFD563',True);txt(d,sub,110,17)
 d.text((20,H-37),'@architectbyai',font=font(15),fill='#9CAFCB')
 t=k/FPS
 if t>=9.2:
  d.rounded_rectangle((26,730,514,906),radius=22,fill='#182449',outline='#4867A5',width=2)
  txt(d,'FOLLOW @ARCHITECTBYAI',765,21,'#FFD563',True)
  txt(d,offer,810,19,'#FFFFFF',True)
  txt(d,'architectbyai.com' if offer!='MORE MATH + PYTHON ART' else 'New mathematical visuals weekly',856,16,'#A8E6FA')
 return im,d,t
def neural(k):
 im,d,t=base(k,'WHEN A NETWORK LEARNS','USING PYTHON','AI ASSISTANTS & CHATBOTS')
 xs=[90,205,330,448];counts=[3,5,4,2];layers=[]
 for x,n in zip(xs,counts):layers.append([(x,370+(i-(n-1)/2)*83) for i in range(n)])
 for z in range(3):
  for i,(x,y) in enumerate(layers[z]):
   for j,(xx,yy) in enumerate(layers[z+1]):
    val=math.sin(i*2.1+j*1.3+z+min(t,8)*.8)
    c='#54CDEB' if val>0 else '#9B6DE3';d.line((x,y,xx,yy),fill=c,width=1 if abs(val)<.4 else 2)
 for z,L in enumerate(layers):
  for i,(x,y) in enumerate(L):node(d,x,y,7,'#FFD477' if (t*2+z+i)%5<1 else '#7BDEEF')
 for i in range(12):
  phase=(t*.48+i/12)%1
  if phase>.85:continue
  z=min(2,int(phase*3.5));f=(phase*3.5)%1
  a=layers[z][i%len(layers[z])];b=layers[z+1][(i*3)%len(layers[z+1])]
  x=mix(a[0],b[0],f);y=mix(a[1],b[1],f);node(d,x,y,3,'#FFE29B')
 txt(d,'INPUT  →  HIDDEN LAYERS  →  OUTPUT',635,16)
 loss=math.exp(-.47*min(t,9));txt(d,f'LOSS: {loss:.3f}',690,19,'#FF9DAB',True)
 d.line((80,714,460,714),fill='#63729A',width=1)
 pts=[(80+i*3,714-95*(1-math.exp(-.028*i))) for i in range(int(min(120,t*13))+1)]
 line(d,pts,'#62D9CD',3)
 return im
TRAJ=[]
def chaos(k):
 im,d,t=base(k,'CHAOS CREATES BEAUTY','USING PYTHON','MORE MATH + PYTHON ART')
 cx,cy=270,350
 def derivative(s):
  a,b,p,q=s;delta=a-b;den=2-math.cos(2*delta)
  dp=(-9.81*(2*math.sin(a)+math.sin(a-2*b))-2*math.sin(delta)*(q*q+p*p*math.cos(delta)))/den
  dq=(2*math.sin(delta)*(2*p*p+19.62*math.cos(a)+q*q*math.cos(delta)))/den
  return np.array([p,q,dp,dq])
 def traj(delta):
  s=np.array([2.12+delta,1.11,0.,0.]);points=[];dt=.018
  for j in range(1050):
   v1=derivative(s);v2=derivative(s+dt*v1/2);v3=derivative(s+dt*v2/2);v4=derivative(s+dt*v3)
   s=s+dt*(v1+2*v2+2*v3+v4)/6
   x=cx+118*math.sin(s[0])+118*math.sin(s[1]);y=cy+118*math.cos(s[0])+118*math.cos(s[1]);points.append((x,y,s[0],s[1]))
  return points
 global TRAJ
 if not TRAJ:TRAJ=[traj(0),traj(.0005)]
 end=min(1049,int(t/9.1*1049));start=max(0,end-460)
 for i,points in enumerate(TRAJ):
  c='#F083D5' if i else '#65D9F4'
  line(d,[(p[0],p[1]) for p in points[start:end+1:2]],c,2)
  if end>0:
   x,y,a,b=points[end];x1=cx+118*math.sin(a);y1=cy+118*math.cos(a)
   line(d,[(cx,cy),(x1,y1),(x,y)],'#6779AD',2);node(d,x,y,5,c)
 node(d,cx,cy,6,'#FFD66E')
 txt(d,'NEARLY IDENTICAL STARTS',655,19,'#FFFFFF',True)
 txt(d,'TINY DIFFERENCE. WILDLY DIFFERENT PATHS.',688,14,'#F1A6D7')
 return im
def data(k):
 im,d,t=base(k,'FROM DATA TO INSIGHT','USING PYTHON','KPI DASHBOARD TOOLKIT')
 phase=min(1,t/8.6)
 rows=[('01','12,400','12,400'),('02','N/A','11,800'),('03','9,700?','9,700'),('04','14,200','14,200'),('05','-','13,100')]
 d.rounded_rectangle((45,215,495,550),radius=17,fill='#111F3E',outline='#344F78',width=2)
 txt(d,'RAW RECORDS' if phase<.4 else 'CLEANED & VALIDATED',245,19,'#FFD56D',True)
 for i,(idx,raw,clean) in enumerate(rows):
  y=293+i*48
  d.line((65,y+19,475,y+19),fill='#283A5D',width=1)
  d.text((75,y),idx,font=font(16),fill='#8FA5CA')
  d.text((200,y),clean if phase>(i+1)*.11 else raw,font=font(19),fill='#6CE4C8' if phase>(i+1)*.11 else '#F18FAD')
  if phase>(i+1)*.11:d.text((425,y),'✓',font=font(21),fill='#7AE0BD')
 if phase>.42:
  d.rounded_rectangle((55,575,485,714),radius=13,fill='#152548',outline='#385B87')
  vals=[40,65,49,82,71,92];n=int(ease((phase-.42)/.5)*6)
  for i in range(n):
   x=95+i*62;d.rectangle((x,680-vals[i],x+26,680),fill='#58C8E6')
  txt(d,'CLEAN DATA → MEANINGFUL KPIs',748,18,'#F1F5FF',True)
 else:txt(d,'DETECT  →  REPAIR  →  VALIDATE',655,19,'#F2F5FF',True)
 return im
def automation(k):
 im,d,t=base(k,'THE AUTOMATION ENGINE','USING PYTHON','BUSINESS PROCESS AUTOMATION')
 stages=[('NEW INQUIRY',260),('VALIDATE',370),('QUALIFY',480),('ROUTE',590),('NOTIFY',700)]
 for i,(name,y) in enumerate(stages):
  active=t>i*1.45
  d.rounded_rectangle((104,y-35,436,y+35),radius=13,fill='#1B3550' if active else '#17213C',outline='#60DCC6' if active else '#364766',width=2)
  txt(d,name,y,18,'#C9FFF3' if active else '#A2B2D1',True)
  if i<4:
   d.line((270,y+35,270,stages[i+1][1]-35),fill='#6484B5',width=2)
   if active:
    py=y+35+(min(1,(t-i*1.45)/1.2))*(stages[i+1][1]-y-70)
    node(d,270,py,5,'#FFD16D')
 txt(d,'TRIGGER → RULES → ACTION',810,18,'#F5F7FF',True)
 return im
def fourier(k):
 im,d,t=base(k,'DRAWING WITH FOURIER','USING PYTHON','MORE MATH + PYTHON ART')
 coeff=[(95,1,0),(42,-2,.5),(25,3,.2),(17,-4,.8),(11,5,1.2)]
 def p(th):
  x=y=0
  for rad,f,phase in coeff:x+=rad*math.cos(f*th+phase);y+=rad*math.sin(f*th+phase)
  return x,y
 th=t/9.2*2*math.pi;cx,cy=270,470
 points=[];x=y=0
 for rad,f,phase in coeff:
  px,py=x,y;x+=rad*math.cos(f*th+phase);y+=rad*math.sin(f*th+phase)
  d.ellipse((cx+px-rad,cy+py-rad,cx+px+rad,cy+py+rad),outline='#34466F',width=1)
  line(d,[(cx+px,cy+py),(cx+x,cy+y)],'#E3A3EA',2)
  node(d,cx+x,cy+y,3,'#FFD26C')
 n=max(2,int(min(t/9.2,1)*600))
 for i in range(n):
  a=i/600*2*math.pi;xx,yy=p(a);points.append((cx+xx,cy+yy))
 line(d,points,'#65D9EE',3)
 txt(d,'f(t) = Σ cₙeⁱⁿᵗ',737,23,'#FF9AA7',True)
 return im
def website(k):
 im,d,t=base(k,'FROM WIREFRAME TO WEB','USING PYTHON','WEBSITE DEVELOPMENT')
 q=ease(t/7.8)
 d.rounded_rectangle((38,236,502,660),radius=15,fill='#111D36',outline='#7E94C6',width=3)
 d.rectangle((40,237,500,277),fill='#24345B')
 for j,c in enumerate(('#FF8C9D','#F6D179','#7AE1CC')):node(d,66+j*24,257,5,c)
 for i in range(3):
  x=303+i*62
  d.rounded_rectangle((x,249,x+47,266),radius=4,outline='#A9B6D0' if q<.5 else '#7BDBF0',width=1)
 d.rounded_rectangle((65,307,475,500),radius=11,fill='#192949' if q>.45 else '#111D36',outline='#4A6B9C',width=2)
 if q>.15:
  d.ellipse((300,330,445,475),outline='#B78BEA',width=2)
  for i in range(13):
   a=i*2*math.pi/13+q*3
   x=372+57*math.cos(a);y=402+57*math.sin(a)
   node(d,x,y,2,'#7CDAEF')
 d.text((85,340),'BUILD BETTER',font=font(25,True),fill='#FFD46E' if q>.45 else '#A0AEC7')
 d.text((85,378),'DIGITAL EXPERIENCES',font=font(16),fill='#F0F5FF')
 if q>.4:d.rounded_rectangle((85,422,231,457),radius=8,fill='#4D9BB9');d.text((158,440),'EXPLORE',font=font(15,True),fill='white',anchor='mm')
 for i in range(3):
  x=65+i*140
  d.rounded_rectangle((x,526,x+125,626),radius=9,fill='#213B5A' if q>.6 else '#131D32',outline='#4D6A91',width=2)
  if q>.6:
   d.line((x+18,554,x+106,554),fill='#6FD6D9',width=4)
   d.line((x+18,578,x+88,578),fill='#8D9EC2',width=2)
 if t>4:
  d.rounded_rectangle((370,550,485,772),radius=14,fill='#10172C',outline='#E4C2F3',width=3)
  d.rounded_rectangle((379,568,476,745),radius=5,fill='#233653')
  d.rectangle((388,591,467,643),fill='#4866A0')
  for i in range(3):d.line((388,667+i*20,458,667+i*20),fill='#8CCBE4',width=3)
 txt(d,'RESPONSIVE • INTERACTIVE • PURPOSEFUL',810,15,'#DCEAF7',True)
 return im
FUN={2:neural,3:chaos,4:data,5:automation,6:fourier,7:website}
NAMES={2:'Neural_Network_Learns',3:'Chaos_Creates_Beauty',4:'Data_to_Intelligence',5:'Automation_Engine',6:'Drawing_with_Fourier',7:'Digital_Experience'}
def render(ep):
 folder=ROOT/f'Episode_{ep:02d}_{NAMES[ep]}';folder.mkdir(exist_ok=True)
 tmp=folder/'_temp_540.mp4'
 w=imageio.get_writer(str(tmp),fps=FPS,codec='libx264',quality=7,macro_block_size=2)
 for k in range(N):w.append_data(np.asarray(FUN[ep](k)))
 w.close()
 target=folder/'video.mp4'
 subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(tmp),'-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-preset','veryfast','-crf','24','-pix_fmt','yuv420p','-movflags','+faststart',str(target)],check=True)
 tmp.unlink();print('Rendered',target,flush=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--episode',type=int);ap.add_argument('--all',action='store_true');args=ap.parse_args()
 for ep in (range(2,8) if args.all else [args.episode]):render(ep)

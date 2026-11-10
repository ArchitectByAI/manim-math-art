import math, os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import imageio.v2 as imageio
OUT=os.path.dirname(__file__)
W,H=540,960
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def F(n,b=False):
 p='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if b else font
 return ImageFont.truetype(p,n)
def petal(cx,cy,theta,L,width,start=0,steps=90):
 pts=[]
 for i in range(steps+1):
  t=i/steps;r=start+L*t;lateral=width*(math.sin(math.pi*t)**0.86)*(0.82+0.18*t)
  pts.append((cx+r*math.cos(theta)-lateral*math.sin(theta),cy+r*math.sin(theta)+lateral*math.cos(theta)))
 for i in range(steps,-1,-1):
  t=i/steps;r=start+L*t;lateral=width*(math.sin(math.pi*t)**0.86)*(0.82+0.18*t)
  pts.append((cx+r*math.cos(theta)+lateral*math.sin(theta),cy+r*math.sin(theta)-lateral*math.cos(theta)))
 return pts
def frame(k,total=192):
 im=Image.new('RGB',(W,H),(9,14,34));d=ImageDraw.Draw(im)
 for y in range(H):
  a=y/H;d.line((0,y,W,y),fill=(int(8+5*a),int(13+5*a),int(33+13*a)))
 d.text((W/2,65),'THE GEOMETRY OF A FLOWER',font=F(22,True),fill='#FFD35B',anchor='mm')
 d.text((W/2,101),'USING PYTHON',font=F(18),fill='#F0F1FF',anchor='mm')
 cx,cy=W/2,475;progress=min(1,(k+1)/145)
 for rad in (112,164,208):d.ellipse((cx-rad,cy-rad,cx+rad,cy+rad),outline=(31,42,83),width=1)
 layers=[(16,75,14,122,'#376DC6'),(12,67,19,76,'#A377F0'),(8,60,21,32,'#FF79CB'),(8,38,12,8,'#FFD078')]
 for li,(n,L,wi,start,color) in enumerate(layers):
  if progress<li*.15:continue
  vis=max(0,min(1,(progress-li*.15)/.45))
  for j in range(n):
   angle=-math.pi/2+2*math.pi*j/n+(li%2)*math.pi/n
   pts=petal(cx,cy,angle,L,wi,start);cutoff=max(3,int(len(pts)*vis))
   d.line(pts[:cutoff],fill=color,width=2,joint='curve')
   if vis>.98:
    tip=(cx+(start+L)*math.cos(angle),cy+(start+L)*math.sin(angle))
    d.line([(cx+(start+8)*math.cos(angle),cy+(start+8)*math.sin(angle)),tip],fill='#6B689A',width=1)
    for f in (.43,.63):
     px=cx+(start+L*f)*math.cos(angle);py=cy+(start+L*f)*math.sin(angle)
     side=wi*.42*math.sin(math.pi*f)
     for s in (-1,1):
      d.line([(px,py),(px+L*.12*math.cos(angle)+s*side*-math.sin(angle),py+L*.12*math.sin(angle)+s*side*math.cos(angle))],fill='#5D598A',width=1)
 for j in range(24):
  ang=2*math.pi*j/24;x=cx+23*math.cos(ang);y=cy+23*math.sin(ang)
  d.ellipse((x-2,y-2,x+2,y+2),fill='#FFD37B')
 d.ellipse((cx-10,cy-10,cx+10,cy+10),outline='#FFD37B',width=2)
 stage='ONE RULE. ONE SEED.' if k<60 else 'SYMMETRY BUILDS THE PETALS' if k<120 else 'GEOMETRY BECOMES ART'
 d.text((W/2,750),stage,font=F(20,True),fill='#F7F3FF',anchor='mm')
 d.text((W/2,805),'r = a cos(kθ)  •  layered polar symmetry',font=F(15),fill='#F47883',anchor='mm')
 d.text((W-24,H-40),'@architectbyai',font=F(15),fill='#B7C0D9',anchor='ra')
 return im
if __name__=='__main__':
 frame(191).save(os.path.join(OUT,'approved_flower_design.png'))
 writer=imageio.get_writer(os.path.join(OUT,'episode01_v3_flower_test.mp4'),fps=24,codec='libx264',quality=7,macro_block_size=2)
 for k in range(192):writer.append_data(np.asarray(frame(k)))
 writer.close()
 print('created preview')

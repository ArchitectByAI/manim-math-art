#!/usr/bin/env python3
"""ArchitectByAI AI Visual Lab: deterministic Dijkstra shortest-path animation.
Requires Pillow and ffmpeg.  Run: python animation.py
This is a synthetic graph demonstration; weighted edges are not real travel times.
"""
from PIL import Image, ImageDraw, ImageFont
import math, os, subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parent
W,H,FPS,DURATION=540,960,20,18
BG=(7,13,28); WHITE=(241,248,255); MUTED=(151,176,198); CYAN=(74,232,221); PINK=(255,121,170); GOLD=(255,200,114)
REG='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def f(n,b=False):return ImageFont.truetype(BOLD if b else REG,n)
F9=f(11); F12=f(13); F14=f(16); F18=f(19,True); F25=f(25,True); F29=f(29,True)
NODES={'A':(76,128),'B':(208,90),'C':(355,124),'D':(122,260),'E':(272,225),'F':(440,263),'G':(92,393),'H':(232,393),'I':(392,382),'J':(455,468)}
EDGES=[('A','B',4),('A','D',3),('B','C',5),('B','E',2),('D','E',5),('C','E',2),('C','F',4),('D','G',5),('D','H',6),('E','H',3),('E','F',5),('F','I',2),('F','J',9),('G','H',3),('H','I',4),('H','J',8),('I','J',3)]
def dijkstra():
    import heapq
    adj={n:[] for n in NODES}
    for a,b,w in EDGES:adj[a].append((b,w));adj[b].append((a,w))
    dist={n:float('inf') for n in NODES};dist['A']=0;previous={};heap=[(0,'A')];visited=[]
    while heap:
        v,n=heapq.heappop(heap)
        if n in visited:continue
        visited.append(n)
        if n=='J':break
        for dest,w in adj[n]:
            if v+w<dist[dest]:dist[dest]=v+w;previous[dest]=n;heapq.heappush(heap,(v+w,dest))
    path=['J']
    while path[-1]!='A':path.append(previous[path[-1]])
    return visited,path[::-1],int(dist['J']),dist
VISITED,PATH,COST,DIST=dijkstra()
assert COST==sum(next(w for x,y,w in EDGES if set((x,y))==set((a,b))) for a,b in zip(PATH,PATH[1:]))

def center(d,s,y,font,color):
    bb=d.textbbox((0,0),s,font=font);d.text(((W-(bb[2]-bb[0]))/2,y),s,font=font,fill=color)
def ease(x):
    x=max(0,min(1,x));return x*x*(3-2*x)
def shot(t):
    im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    for x,y,r in [(80,92,90),(410,230,145),(240,640,170)]:
        for rr in range(r,10,-14):
            col=(7+int(6*(r-rr)/r),13+int(12*(r-rr)/r),28+int(15*(r-rr)/r))
            d.ellipse((x-rr,y-rr,x+rr,y+rr),outline=col,width=2)
    d.text((28,27),'ARCHITECTBYAI  |  AI VISUAL LAB',font=F12,fill=CYAN)
    d.text((28,77),'CAN CODE FIND',font=F29,fill=WHITE)
    d.text((28,113),'THE BEST ROUTE?',font=F29,fill=WHITE)
    d.text((28,160),'Follow for visual Python + AI experiments',font=F12,fill=MUTED)
    d.rounded_rectangle((18,208,522,758),radius=22,fill=(13,27,46),outline=(48,79,100),width=2)
    d.text((39,224),'DIJKSTRA / SHORTEST PATH',font=F12,fill=(172,200,221))
    d.text((384,224),'SIMULATED',font=F9,fill=(126,163,187))
    ox,oy=34,247
    reveal=ease((t-.1)/2.0)
    # weighted network edges reveal during the opening, alongside moving search halo
    for i,(a,b,w) in enumerate(EDGES):
        x1,y1=NODES[a];x2,y2=NODES[b];x1+=ox;y1+=oy;x2+=ox;y2+=oy
        frac=ease((reveal*len(EDGES)-i))
        if frac<=0:continue
        ex=x1+(x2-x1)*frac;ey=y1+(y2-y1)*frac
        d.line((x1,y1,ex,ey),fill=(57,79,99),width=3)
        if frac>.97:
            mx=(x1+x2)//2;my=(y1+y2)//2
            d.rounded_rectangle((mx-11,my-11,mx+11,my+10),radius=6,fill=(17,34,53))
            centerx=d.textbbox((0,0),str(w),font=F9)[2]
            d.text((mx-centerx/2,my-8),str(w),font=F9,fill=(160,181,202))
    # active algorithm steps; one expansion after another
    step=ease((t-2.9)/9.0)*len(VISITED)
    nvis=min(len(VISITED),int(step))
    done=set(VISITED[:nvis]); active=VISITED[nvis] if nvis<len(VISITED) and t>3 else None
    # final shortest path revealed segment by segment
    route_frac=ease((t-11.7)/2.2)*(len(PATH)-1)
    if t>=11.7:
        for i,(a,b) in enumerate(zip(PATH,PATH[1:])):
            p=ease(route_frac-i)
            if p<=0:continue
            x1,y1=NODES[a];x2,y2=NODES[b]
            for width,color in [(17,(28,90,93)),(8,CYAN)]:
                d.line((x1+ox,y1+oy,x1+ox+(x2-x1)*p,y1+oy+(y2-y1)*p),fill=color,width=width)
    for n,(x,y) in NODES.items():
        x+=ox;y+=oy
        highlight=n in PATH and t>=11.7
        if n==active:
            p=.5+.5*math.sin(t*7)
            rr=20+5*p
            d.ellipse((x-rr,y-rr,x+rr,y+rr),outline=GOLD,width=3)
        color=CYAN if highlight else (PINK if n in done else (100,137,166))
        d.ellipse((x-15,y-15,x+15,y+15),fill=(15,30,51),outline=color,width=3)
        bb=d.textbbox((0,0),n,font=F12)
        d.text((x-(bb[2]-bb[0])/2,y-9),n,font=F12,fill=WHITE)
    # start/target and traversal state
    d.text((41,264),'START  A',font=F12,fill=CYAN)
    d.text((423,264),'GOAL  J',font=F12,fill=PINK)
    if t<3: headline='ONE NETWORK. MANY POSSIBLE PATHS.'; subtitle='Edge numbers = fictional costs'
    elif t<11.7:
        headline='CHECK THE LOWEST COST FIRST';subtitle=f'Nodes examined: {nvis} of {len(VISITED)}'
    elif t<14:
        headline=f'SHORTEST TOTAL COST: {COST}';subtitle='Route: '+'  →  '.join(PATH)
    elif t<16:
        headline='SAVE THIS: DIJKSTRA ALGORITHM';subtitle='Always explore the cheapest known distance'
    else:headline='';subtitle=''
    if t<16:
        center(d,headline,792,F18,WHITE)
        center(d,subtitle,832,F14,(168,211,216))
        center(d,'A real Python graph calculation • illustrative costs',884,F9,MUTED)
        center(d,'@architectbyai',923,F12,(159,191,213))
    else:
        d.rounded_rectangle((15,773,525,948),radius=22,fill=(15,36,54),outline=CYAN,width=2)
        center(d,'TURN ROUTINE WORK INTO FLOW',785,F18,WHITE)
        center(d,'BUSINESS PROCESS',820,F25,CYAN)
        center(d,'AUTOMATION',850,F25,CYAN)
        center(d,'Explore solutions at',888,F12,WHITE)
        center(d,'architectbyai.com',913,F18,WHITE)
    return im

def main():
    out=ROOT/'B03_V07_Dijkstra_Path_1080x1920.mp4'
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',str(out)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for i in range(FPS*DURATION):
        try:proc.stdin.write(shot(i/FPS).tobytes())
        except BrokenPipeError:break
    proc.stdin.close();ret=proc.wait()
    if ret:raise RuntimeError('ffmpeg render error')
    for label,t in [('opening',.3),('search',7.3),('path',13.2),('save',15),('end',17.2)]:shot(t).save(ROOT/(label+'.png'))
    print('VISIT ORDER',VISITED,'PATH',PATH,'COST',COST, 'OUTPUT',out)
if __name__=='__main__':main()
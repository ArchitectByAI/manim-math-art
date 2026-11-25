#!/usr/bin/env python3
"""ArchitectByAI AI Visual Lab, B03-V05: evidence-first knowledge search.

Renders a real TF-IDF/cosine lexical retriever over a fictional business
knowledge base. This is NOT a generative language model, nor a semantic
embedding model. All documents and query are synthetic. The relevant policy
was authored for this animation only. Requires NumPy, Pillow and FFmpeg.
"""
import math, re, subprocess, argparse
from pathlib import Path
from collections import Counter
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
W,H,FPS,SECONDS=540,960,20,18
NAVY=(6,12,28); NAVY2=(14,26,48); WHITE=(240,248,255); DIM=(151,177,204)
CYAN=(92,237,225); BLUE=(81,139,255); GOLD=(255,199,104); PINK=(244,126,162)
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(n,bold=False):return ImageFont.truetype(FB if bold else F,n)
F10=font(12);F11=font(13);F12=font(14);F14=font(17);F16=font(19);F19=font(23,True);F23=font(27,True);F27=font(31,True)

DOCS=[
('RETURNS POLICY','Refunds take 5 business days after approval.'),
('DELIVERY','Shipping orders arrive in 3 to 7 days.'),
('ACCOUNT SECURITY','Password resets require identity verification.'),
('ONBOARDING','New customers get a welcome guide.'),
('CUSTOMER SUPPORT','Support questions are answered within 2 days.')
]
QUERY='How long do refunds take?'
def tok(s):return re.findall(r'[a-z]+',s.lower())
def rank_docs():
    texts=[title+' '+body for title,body in DOCS]+[QUERY]
    terms=sorted(set(w for txt in texts for w in tok(txt)))
    vocab={w:i for i,w in enumerate(terms)}
    tf=np.zeros((len(texts),len(terms)),dtype=float)
    for i,txt in enumerate(texts):
        counts=Counter(tok(txt))
        for w,n in counts.items(): tf[i,vocab[w]]=1+math.log(n)
    # document frequency counts the five documents only; query is excluded
    df=np.sum(tf[:-1]>0,axis=0)
    idf=np.log((len(DOCS)+1)/(df+1))+1
    vectors=tf*idf
    vectors/=np.maximum(1e-12,np.linalg.norm(vectors,axis=1,keepdims=True))
    scores=vectors[:-1]@vectors[-1]
    idx=int(np.argmax(scores))
    return scores,idx
SCORES,WINNER=rank_docs()
assert WINNER==0 and SCORES[0]>max(SCORES[1:])


def smooth(x):
    x=min(1,max(0,x));return x*x*(3-2*x)
def approach(t,a,b):return smooth((t-a)/(b-a))
def mix(a,b,t):return tuple(round(a[i]+(b[i]-a[i])*t) for i in range(3))
def center(d,text,y,ft,fill):
    bbox=d.textbbox((0,0),text,font=ft);d.text(((W-(bbox[2]-bbox[0]))/2,y),text,font=ft,fill=fill)
def rounded(d,xy,r,fill,outline=None,width=1):d.rounded_rectangle(tuple(round(v) for v in xy),radius=r,fill=fill,outline=outline,width=width)
def dashed_line(d,a,b,color,width=2,dash=10):
    x1,y1=a;x2,y2=b;length=math.hypot(x2-x1,y2-y1);n=max(1,math.ceil(length/dash));
    for i in range(0,n,2):
        st=i/n;en=min(1,(i+1)/n)
        d.line((x1+(x2-x1)*st,y1+(y2-y1)*st,x1+(x2-x1)*en,y1+(y2-y1)*en),fill=color,width=width)

def frame(t):
    im=Image.new('RGB',(W,H),NAVY);d=ImageDraw.Draw(im)
    # patterned backdrop; no pre-rendered stock art
    for ix in range(10):
        for iy in range(16):
            x=25+ix*54; y=30+iy*57
            v=.5+.5*math.sin(t*.38+ix*.7+iy*.9)
            c=round(22+12*v)
            d.ellipse((x,y,x+1,y+1),fill=(c,c+12,c+26))
    d.text((24,24),'ARCHITECTBYAI  |  AI VISUAL LAB',font=F11,fill=CYAN)
    d.text((25,81),'HOW DOES AI FIND',font=F27,fill=WHITE)
    d.text((25,120),'THE RIGHT ANSWER?',font=F27,fill=WHITE)
    d.text((25,170),'Follow for real Python + AI experiments',font=F11,fill=DIM)

    # Question enters from left; clearly fictional
    qalpha=approach(t,0,.4)
    qx=26-80*(1-qalpha)
    rounded(d,(qx,214,qx+488,284),19,NAVY2,(56,90,126),2)
    d.ellipse((qx+16,235,qx+42,261),fill=CYAN)
    d.text((qx+24,238),'?',font=F14,fill=NAVY)
    d.text((qx+56,226),'CUSTOMER QUESTION',font=F10,fill=CYAN)
    d.text((qx+56,247),QUERY,font=F14,fill=WHITE)
    # pipeline node and joining lines; moving lines
    ax,ay=270,315
    d.line((270,284,270,314),fill=(43,85,112),width=3)
    d.ellipse((ax-7,ay-7,ax+7,ay+7),fill=CYAN)
    # actual doc ranks: first correct item wins using real retrieval scores
    d.text((29,338),'SEARCHING 5 DOCUMENTS',font=F12,fill=DIM)
    d.text((393,338),'TF-IDF',font=F12,fill=GOLD)
    # cards drop in sequentially
    y0=375; rowh=67
    for i,(title,desc) in enumerate(DOCS):
        y=y0+i*rowh
        appear=approach(t,.5+i*.33,1.25+i*.33)
        if appear<=0:continue
        x=28+round(48*(1-appear));right=512
        selected=i==WINNER
        # switch to green/aqua as retrieval ranking solidifies
        highlight=approach(t,4.5,6.5) if selected else 0
        panel=mix(NAVY2,(14,56,66),highlight)
        outline=mix((42,69,92),CYAN,highlight) if selected else (44,70,98)
        rounded(d,(x,y,right,y+58),13,panel,outline,2 if selected else 1)
        d.text((x+13,y+8),title,font=F12,fill=CYAN if highlight>.4 else WHITE)
        d.text((x+13,y+31),desc,font=F10,fill=DIM)
        # score is a computed cosine, not a guessed decorative percentage
        score=float(SCORES[i]); val=approach(t,3.5+i*.15,6.0+i*.15)
        d.rounded_rectangle((x+354,y+15,x+456,y+22),4,fill=(37,52,70))
        d.rounded_rectangle((x+354,y+15,x+354+max(3,int(102*score*val)),y+22),4,fill=CYAN if selected else BLUE)
        d.text((x+360,y+28),f'{score*val:.2f}',font=F10,fill=CYAN if selected else DIM)
        if highlight>.25:
            d.text((x+456,y+6),'✓',font=F19,fill=CYAN)
    # stage explanation / save card / CTA replaces below-doc footer only
    rounded(d,(25,727,515,932),22,(11,27,50),(48,79,106),2)
    if t<4.2:
        center(d,'FIVE POSSIBLE SOURCES',751,F19,WHITE)
        center(d,'Which one actually answers the question?',795,F12,DIM)
        center(d,'Don\'t guess. Search the knowledge base.',859,F12,CYAN)
    elif t<10.8:
        center(d,'RANK BY RELEVANCE',748,F19,WHITE)
        center(d,'Keyword-weighted vectors + cosine similarity',790,F11,DIM)
        v=approach(t,4.5,6.6)
        center(d,'TOP MATCH: RETURNS POLICY',834,F14,CYAN)
        d.text((104,873),'',font=F10,fill=DIM)
        center(d,'Similarity: '+f'{SCORES[0]*v:.2f}',866,F12,GOLD)
    elif t<14:
        center(d,'RETRIEVE THE EVIDENCE',752,F19,WHITE)
        center(d,'Returns policy says:',798,F12,DIM)
        center(d,'"5 business days after approval."',833,F14,CYAN)
        center(d,'Answer should cite the actual source.',875,F11,DIM)
    elif t<16:
        center(d,'SAVE THIS AI PRINCIPLE',750,F19,WHITE)
        center(d,'RETRIEVE → VERIFY → ANSWER',808,F19,CYAN)
        center(d,'Evidence before confident output.',860,F12,DIM)
    else:
        rounded(d,(25,727,515,932),22,(15,43,56),CYAN,2)
        center(d,'TURN DOCUMENTS INTO ANSWERS',749,F16,WHITE)
        center(d,'KNOWLEDGE SYSTEMS',795,F23,CYAN)
        center(d,'Explore ArchitectByAI services',844,F12,WHITE)
        center(d,'architectbyai.com',882,F19,WHITE)
    # persistent footer, follows from first frame
    d.text((27,939),'@architectbyai',font=F10,fill=(123,148,179))
    d.text((371,939),'SYNTHETIC EXAMPLE',font=F10,fill=(123,148,179))
    return im

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=ROOT/'B03_V05_Knowledge_Search_1080x1920.mp4');args=p.parse_args()
    print('actual cosine scores:',[(DOCS[i][0],round(float(x),4)) for i,x in enumerate(SCORES)],flush=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(args.output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for i in range(FPS*SECONDS):
            proc.stdin.write(frame(i/FPS).tobytes())
            if i%100==0:print('Rendering',i,'/',FPS*SECONDS,flush=True)
    finally:
        proc.stdin.close()
    if proc.wait():raise RuntimeError('FFmpeg render failure')
    for name,t in [('opening',.25),('search',3.3),('ranking',8),('answer',12.3),('save',14.8),('end',17)]:
        frame(t).resize((1080,1920),Image.Resampling.LANCZOS).save(ROOT/(name+'.png'))
    frame(.4).resize((1080,1920),Image.Resampling.LANCZOS).save(ROOT/'cover.png')
    print('DONE',args.output,flush=True)
if __name__=='__main__':main()
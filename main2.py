import os,json,urllib.request as U
B=os.environ.get("MAKEFUN_ENV_URL","").rstrip("/")
V="PNBRQKpnbrqk"
M=[0,100,320,330,500,900,20000]
import base64 as C
Q=C.b64decode('AAAAAAAAAAAFCgrs7AoKBQX79gAA9vsFAAAAFBQAAAAFBQUKCgUFBQoKFB4eCgoKMjIyMjIyMjIAAAAAAAAAAM7Y4uLi4tjO2OwAAAAA7NjiAAoPDwoA4uIFDxQUDwXi4gAPFBQPAOLiBQoPDwoF4tjsAAUFAOzYztji4uLi2M7s9vb29vb27PYAAAAAAAD29gAFCgoFAPb2BQUKCgUF9vYACgoKCgD29goKCgoKCvb2BQAAAAAF9uz29vb29vbsAAAAAAAAAAAFCgoKCgoKBfsAAAAAAAD7+wAAAAAAAPv7AAAAAAAA+/sAAAAAAAD7+wAAAAAAAPsAAAAFBQAAAOz29vv79vbs9gAAAAAAAPb2AAUFBQUA9vsABQUFBQD7AAAFBQUFAPv2BQUFBQUA9vYABQAAAAD27Pb2+/v29uwUHgoAAAoeFBQUAAAAABQU9uzs7Ozs7Pbs4uLY2OLi7OLY2M7O2Nji4tjYzs7Y2OLi2NjOztjY4uLY2M7O2Nji')
P=[[Q[t*64+i] for i in range(64)] for t in range(6)]
N=[(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)]
K=[(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]
R=[(0,1),(1,0),(0,-1),(-1,0)]
Q=K
def sq(f,r):return r*8+f
def gen(b,side):
    out=[]
    for i,v in enumerate(b):
        if v==0 or (v>0)!=(side>0):continue
        t=abs(v)-1;f,r=i%8,i//8
        if t==5:
            for df,dr in K:
                x,y=f+df,r+dr
                if 0<=x<8 and 0<=y<8:
                    w=b[sq(x,y)]
                    if w==0 or (w>0)!=(side>0):out.append((i,sq(x,y)))
        elif t==0:
            d=-8 if side>0 else 8
            y=r+d
            if 0<=y<8 and b[sq(f,y)]==0:
                if y in (0,7):out+= [(i,sq(f,y),q) for q in (4,3,1,2)]
                else:out.append((i,sq(f,y)))
                y+=d
                if r in (1,6) and b[sq(f,y)]==0:out.append((i,sq(f,y)))
            for df in (-1,1):
                x=f+df
                if 0<=x<8 and 0<=y<8:
                    w=b[sq(x,y)]
                    if w!=0 and (w>0)!=(side>0):
                        if y in (0,7):out+= [(i,sq(x,y),q) for q in (4,3,1,2)]
                        else:out.append((i,sq(x,y)))
        else:
            ds=N if t==1 else (R if t==3 else Q)
            for df,dr in ds:
                x,y=f+df,r+dr
                while 0<=x<8 and 0<=y<8:
                    w=b[sq(x,y)]
                    if w!=0:
                        if (w>0)!=(side>0):out.append((i,sq(x,y)))
                        break
                    out.append((i,sq(x,y)))
                    if t==1:break
                    x+=df;y+=dr
    return out
def ev(b):
    s=0
    for i,v in enumerate(b):
        if v==0:continue
        t=abs(v)-1;m=M[t+1];p=P[t][i if v>0 else 63-i]
        s+= (m+p) if v>0 else -(m+p)
    return s
def mk(b,m):
    a,z=m[0],m[1];pc=b[a];b[z]=pc if len(m)<3 else (m[2] if pc>0 else -m[2]);b[a]=0
def um(b,m,a1):
    b[m[0]]=a1;b[m[1]]=0
def qs(b,s,al,be,n):
    st=ev(b)*(1 if s>0 else -1)
    if n[0]<0:return st
    if st>=be:return be
    al=max(al,st)
    ms=[m for m in gen(b,s) if b[m[1]]!=0]
    sc=lambda m:M[abs(b[m[1]])]
    ms.sort(key=sc,reverse=True)
    for m in ms:
        if abs(b[m[1]])==6:return 20000
        a1=b[m[0]];mk(b,m);n[0]-=1
        v=-qs(b,-s,-be,-al,n);um(b,m,a1)
        if v>=be:return be
        al=max(al,v)
    return al
def ne(b,s,d,al,be,n):
    if n[0]<0:return ev(b)*(1 if s>0 else -1)
    ms=gen(b,s);ms.sort(key=lambda m:(M[abs(b[m[1]])] if b[m[1]] else 0),reverse=True)
    if d==0:return qs(b,s,al,be,n)
    for m in ms:
        if abs(b[m[1]])==6:return 20000-d
        a1=b[m[0]];mk(b,m);n[0]-=1
        v=-ne(b,-s,d-1,-be,-al,n);um(b,m,a1)
        if v>=be:return be
        al=max(al,v)
    return al
def load(fen):
    b=[0]*64;rows=fen.split()[0].split("/")
    for r,row in enumerate(rows):
        f=0
        for c in row:
            if c.isdigit():f+=int(c)
            else:b[sq(f,r)]=(V.index(c)+1) if c.isupper() else -(V.index(c.lower())+1);f+=1
    return b,fen.split()[1]
def post(p,j):
    r=U.Request(B+p,json.dumps(j).encode(),{"Content-Type":"application/json"})
    return json.loads(U.urlopen(r,timeout=9).read())
g=None
while True:
    try:
        if g and g.get("status")=="your_move":
            b,s=load(g["fen"]);lm=set(g["legal_moves"]);n=[1200]
            best=None;bs=-1e9
            for m in gen(b,s):
                uci=chr(97+m[0]%8)+str(8-m[0]//8)+chr(97+m[1]%8)+str(8-m[1]//8)+("qrbn"[m[2]-2] if len(m)>2 else "")
                if uci not in lm:continue
                a1=b[m[0]];mk(b,m);n[0]-=1
                v=-ne(b,-s,2,-1e9,1e9,n);um(b,m,a1)
                if v>bs:bs,best=v,uci
            if best is None:best=sorted(lm)[0]
            g=post("/move",{"game":g["game"],"move":best})
        else:
            g=post("/game",{})
            if g.get("status")=="done":break
    except Exception:
        try:
            g=post("/game",{})
            if g.get("status")=="done":break
        except Exception:break

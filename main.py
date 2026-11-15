import os,json,urllib.request as U
B=os.environ.get("MAKEFUN_ENV_URL","").rstrip("/")
V="PNBRQKpnbrqk"
M=[0,100,320,330,500,900,20000]
N=[(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)]
K=[(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]
R=[(0,1),(1,0),(0,-1),(-1,0)]
Q=K
def z(f,r):return r*8+f
def G(b,side):
    o=[]
    for i,v in enumerate(b):
        if v==0 or (v>0)!=(side>0):continue
        t=abs(v)-1;f,r=i%8,i//8
        if t==5:
            for df,dr in K:
                x,y=f+df,r+dr
                if 0<=x<8 and 0<=y<8:
                    w=b[z(x,y)]
                    if w==0 or (w>0)!=(side>0):o.append((i,z(x,y)))
        elif t==0:
            d=-8 if side>0 else 8
            y=r+d
            if 0<=y<8 and b[z(f,y)]==0:
                if y in (0,7):o+= [(i,z(f,y),q) for q in (4,3,1,2)]
                else:o.append((i,z(f,y)))
                y+=d
                if r in (1,6) and b[z(f,y)]==0:o.append((i,z(f,y)))
            for df in (-1,1):
                x=f+df
                if 0<=x<8 and 0<=y<8:
                    w=b[z(x,y)]
                    if w!=0 and (w>0)!=(side>0):
                        if y in (0,7):o+= [(i,z(x,y),q) for q in (4,3,1,2)]
                        else:o.append((i,z(x,y)))
        else:
            ds=N if t==1 else (R if t==3 else Q)
            for df,dr in ds:
                x,y=f+df,r+dr
                while 0<=x<8 and 0<=y<8:
                    w=b[z(x,y)]
                    if w!=0:
                        if (w>0)!=(side>0):o.append((i,z(x,y)))
                        break
                    o.append((i,z(x,y)))
                    if t==1:break
                    x+=df;y+=dr
    return o
def e(b):
 s=0
 for i,v in enumerate(b):
  if v==0:continue
  t=abs(v)-1;x=i%8;y=i//8;d=7-abs(x*2-7)-abs(y*2-7)
  s+=(M[t+1]+(d*2 if t in(1,2)else 0)+(6 if t==0 and(y<2 if v>0 else y>5)else 0))*(1 if v>0 else -1)
 return s
def k(b,m):
    a,z=m[0],m[1];pc=b[a];b[z]=pc if len(m)<3 else (m[2] if pc>0 else -m[2]);b[a]=0
def w(b,m,a1):
    b[m[0]]=a1;b[m[1]]=0
def q(b,s,al,be,n):
    st=e(b)*(1 if s>0 else -1)
    if n[0]<0:return st
    if st>=be:return be
    al=max(al,st)
    ms=[m for m in G(b,s) if b[m[1]]!=0]
    sc=lambda m:M[abs(b[m[1]])]
    ms.sort(key=sc,reverse=True)
    for m in ms:
        if abs(b[m[1]])==6:return 20000
        a1=b[m[0]];k(b,m);n[0]-=1
        v=-q(b,-s,-be,-al,n);w(b,m,a1)
        if v>=be:return be
        al=max(al,v)
    return al
def f(b,s,d,al,be,n):
    if n[0]<0:return e(b)*(1 if s>0 else -1)
    ms=G(b,s);ms.sort(key=lambda m:(M[abs(b[m[1]])] if b[m[1]] else 0),reverse=True)
    if d==0:return q(b,s,al,be,n)
    for m in ms:
        if abs(b[m[1]])==6:return 20000-d
        a1=b[m[0]];k(b,m);n[0]-=1
        v=-f(b,-s,d-1,-be,-al,n);w(b,m,a1)
        if v>=be:return be
        al=max(al,v)
    return al
def h(fen):
    b=[0]*64;rows=fen.split()[0].split("/")
    for r,row in enumerate(rows):
        f=0
        for c in row:
            if c.isdigit():f+=int(c)
            else:b[z(f,r)]=(V.index(c)+1) if c.isupper() else -(V.index(c.upper())+1);f+=1
    return b,1 if fen.split()[1]=="w" else -1
def p(p,j):
    r=U.Request(B+p,json.dumps(j).encode(),{"Content-Type":"application/json"})
    return json.loads(U.urlopen(r,timeout=9).read())
g=None
while True:
    try:
        if g and g.get("status")=="your_move":
            b,s=h(g["fen"]);L2=set(g["legal_moves"]);n=[1200]
            c=None;v0=-1e9
            for m in G(b,s):
                u=chr(97+m[0]%8)+str(8-m[0]//8)+chr(97+m[1]%8)+str(8-m[1]//8)+("qrbn"[m[2]-2] if len(m)>2 else "")
                if u not in L2:continue
                a1=b[m[0]];k(b,m);n[0]-=1
                v=-f(b,-s,2,-1e9,1e9,n);w(b,m,a1)
                if v>v0:v0,c=v,u
            if c is None:c=sorted(L2)[0]
            g=p("/move",{"game":g["game"],"move":c})
        else:
            g=p("/game",{})
            if g.get("status")=="done":break
    except Exception:break

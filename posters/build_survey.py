import re
base=open("poster-volunteers.src.html").read()
qr=re.sub(r'width="(\d+)" height="\d+"',r'viewBox="0 0 \1 \1"',open("qr-survey.svg").read(),count=1)
head=base[:base.index('<main class="poster">')]
brand=re.search(r'<div class="brand">.*?</div>',base,flags=re.S).group(0)
sticker_js=base[base.index('const NS="http://www.w3.org/2000/svg";'):]
URL="greencanteen.plantbasedcampus.org/feedback.html"

def page(name,title,css,main,bg,band,line,origin,rxs,rys,rot,extra_root=""):
    h=head.replace("Volunteers wanted (poster)",title)
    h=h.replace("</style>",css+"\n</style>",1)
    h=h.replace(":root{",":root{"+extra_root,1)
    js=('<script>\n(()=>{const cv=document.getElementById("bg"),c=cv.getContext("2d"),W=cv.width,H=cv.height;\n'
    'function ripples(){const P=document.querySelector(".poster").getBoundingClientRect(),T=document.querySelector("%s").getBoundingClientRect(),k0=W/P.width;\n'
    'const cx=(T.left+T.width/2-P.left)*k0,cy=(T.top+T.height/2-P.top)*k0,rx0=T.width*k0*%s,ry0=T.height*k0*%s,rot=%s*Math.PI/180,step=W/15;\n'
    'c.setTransform(1,0,0,1,0,0);c.fillStyle="%s";c.fillRect(0,0,W,H);\n'
    'for(let k=34;k>=0;k--){c.beginPath();const rx=rx0+k*step,ry=ry0+k*step;\n'
    'for(let a=0;a<=Math.PI*2+.01;a+=.02){const wob=1+.045*Math.sin(a*6+1)+.02*Math.sin(a*11+2)+.03*Math.sin(a*3+k*.35);\n'
    'const ex=Math.cos(a)*rx*wob,ey=Math.sin(a)*ry*wob,x=cx+ex*Math.cos(rot)-ey*Math.sin(rot),y=cy+ex*Math.sin(rot)+ey*Math.cos(rot);a===0?c.moveTo(x,y):c.lineTo(x,y)}\n'
    'c.closePath();c.fillStyle=k%%2?"%s":"%s";c.fill();c.lineWidth=5;c.strokeStyle="%s";c.stroke()}}\n'%(origin,rxs,rys,rot,bg,bg,band,line))
    js+=sticker_js
    html=h+'<main class="poster">\n  <canvas class="bg" id="bg" width="2246" height="3176"></canvas>\n'+main+'\n</main>\n'+js
    html=html.replace("@@QR@@",qr)
    open(name,"w").write(html)

# ---------- A: QR hero, ripples radiate from the QR card (green) ----------
cssA="""
.poster{--bgc:#DFFEAE}
.head{width:196mm}
.qrcard{background:var(--hvid);border:.8mm solid var(--mork);border-radius:14mm;padding:9mm 9mm 10mm;display:flex;flex-direction:column;align-items:center;gap:6mm}
.qrcard .qrbox{width:92mm;height:92mm}
.qrcard .qrbox svg{width:100%;height:100%;display:block}
.qrcard .scan{font-family:var(--display);font-size:13mm;line-height:1}
.url{background:var(--mork);color:var(--lys);border-radius:999px;padding:3mm 9mm;font-size:5.6mm;border:.6mm solid var(--lys)}
"""
mainA=brand+"""
  <div class="head"><span data-sticker="How was|your lunch?" data-size="90"></span></div>
  <div class="qrcard"><div class="qrbox">@@QR@@</div><div class="scan">Scan to tell us</div></div>
  <div class="facts"><div class="pill">Takes about a minute</div></div>
  <div class="lede"><span data-sticker="Our volunteer cooks|read every answer." data-size="40" data-plain="1" data-mm="7.4"></span></div>
  <div class="url">%s</div>"""%URL
page("poster-survey-a.html","Green Canteen – Survey poster A",cssA,mainA,"#DFFEAE","#36471D","#36471D",".qrcard",".62",".62",0)

# ---------- B: rate-your-box row, pink ----------
cssB="""
.poster{--bgc:#FFE1FE}
.head{width:196mm;--s-fill:#fff}
.rate{display:flex;flex-direction:column;align-items:center;gap:4mm}
.rate .row{display:flex;gap:6mm}
.rate .dot{width:32mm;height:32mm;border-radius:50%;background:var(--hvid);border:.8mm solid var(--mork);display:grid;place-items:center;font-family:var(--display);font-size:19mm;line-height:1}
.rate .dot:nth-child(5){background:var(--lys)}
.rate .ends{display:flex;justify-content:space-between;width:100%;font-size:5.6mm;font-weight:500;letter-spacing:.04em;background:var(--hvid);border:.6mm solid var(--mork);border-radius:999px;padding:2.4mm 9mm}
.cta{width:fit-content}
.cta .qr{width:50mm;height:50mm;padding:3.6mm}
"""
mainB=brand+"""
  <div class="head"><span data-sticker="Rate your|lunchbox!" data-size="90"></span></div>
  <div class="rate"><div class="row"><div class="dot">1</div><div class="dot">2</div><div class="dot">3</div><div class="dot">4</div><div class="dot">5</div></div><div class="ends"><span>Not for me</span><span>Delicious</span></div></div>
  <div class="lede"><span data-sticker="Taste, portion and value for money.|One minute, and every answer is read.|Pick your meal, tell us what to change." data-size="40" data-plain="1" data-mm="6.6"></span></div>
  <div class="cta"><div class="qr">@@QR@@</div><div><h3>Scan to give feedback</h3><p>Or visit<br><b>%s</b></p></div></div>"""%URL
mainB=mainB.replace("Taste, portion and value for money.|One minute, and every answer is read.|Pick your meal, tell us what to change.","How did it taste? Was it filling? Good value?|It takes about a minute, and our volunteer|cooks read every answer.")
page("poster-survey-b.html","Green Canteen – Survey poster B",cssB,mainB,"#FFE1FE","#36471D","#36471D",".rate",".52",".95",0)

# ---------- C: dark mode, dishes + QR ----------
cssC="""
.poster{--bgc:#111A03;color:var(--lys)}
.head{width:196mm;--s-fill:var(--pink)}
.sticker .l3{fill:var(--lys);stroke:var(--lys)}
.sticker .l1{fill:var(--mork)}
.eyebrow{font-size:5.6mm;letter-spacing:.14em;text-transform:uppercase;font-weight:500;color:var(--lys)}
.dishes{display:flex;flex-direction:column;align-items:center;gap:4mm}
.dishes .pill{color:var(--mork);border-color:var(--lys);font-size:10.5mm;padding:3.4mm 9mm}
.dishes .pill:nth-child(2){background:var(--lys)}
.dishes .pill:nth-child(3){background:var(--pink)}
.qrcard{background:var(--lys);color:var(--mork);border-radius:14mm;padding:8mm 11mm 8mm 8mm;display:flex;align-items:center;gap:9mm;border:.8mm solid var(--lys);box-shadow:0 0 0 1.6mm var(--mork)}
.qrcard .qrbox{width:70mm;height:70mm;flex:none}
.qrcard .qrbox svg{width:100%;height:100%;display:block}
.qrcard h3{font-family:var(--display);font-weight:400;font-size:13mm;line-height:1.05;margin:0}
.qrcard p{margin:3mm 0 0;font-size:5.8mm;line-height:1.35}
.qrcard b{font-weight:500;background:var(--pink);padding:.6mm 3mm;border-radius:999px;display:inline-block;margin-top:2mm;font-size:4.6mm}
.brand{background:var(--lys)}
"""
mainC=brand+"""
  <div class="head"><span data-sticker="How was|your box?" data-size="90"></span></div>
  <div class="dishes"><div class="eyebrow">Tried one of these?</div><div class="pill">Chilli sin carne</div><div class="pill">Red lentil dal</div><div class="pill">Coconut chickpea curry</div></div>
  <div class="qrcard"><div class="qrbox">@@QR@@</div><div><h3>Tell the cooks</h3><p>Scan, rate it 1 to 5 and say what we should cook next.<br><b>%s</b></p></div></div>"""%URL
page("poster-survey-c.html","Green Canteen – Survey poster C",cssC,mainC,"#111A03","#1F2F08","#DFFEAE",".dishes",".62",".9",0)

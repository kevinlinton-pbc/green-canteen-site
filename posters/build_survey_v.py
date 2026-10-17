import re
base=open("poster-volunteers.src.html").read()
qr=re.sub(r'width="(\d+)" height="\d+"',r'viewBox="0 0 \1 \1"',open("qr-survey.svg").read(),count=1)
head=base[:base.index('<main class="poster">')]
logo=re.search(r'<svg class="logo".*?</svg>',base,flags=re.S).group(0)
brand='<div class="brand">'+logo+'<span>Green Canteen</span></div>'
sticker_js=base[base.index('const NS="http://www.w3.org/2000/svg";'):]
URL="greencanteen.plantbasedcampus.org/feedback.html"
COMMON="""
.poster>*{z-index:2}
.brand{background:none;border:0;padding:0;gap:4mm;font-size:15mm}
.brand .logo{width:16mm}
.head{width:196mm}
.qrcard{background:var(--hvid);border-radius:14mm;padding:10mm 10mm 9mm;display:flex;flex-direction:column;align-items:center;gap:6mm}
.qrbox{width:100mm;height:100mm}
.qrbox svg{width:100%;height:100%;display:block}
.scan{font-family:var(--display);font-size:13mm;line-height:1}
.copy{text-align:center;display:flex;flex-direction:column;gap:3mm}
.copy .c1{font-family:var(--display);font-size:12mm;line-height:1.05}
.copy .c2{font-size:7mm;line-height:1.35}
.foot{font-size:5.8mm;text-align:center;line-height:1.4}
.foot.plain b{background:none;color:var(--mork);padding:0;margin-top:1mm;display:block;font-size:6.2mm}
.foot b{font-weight:500;background:var(--mork);color:var(--lys);border-radius:999px;padding:1mm 4.5mm;display:inline-block;margin-top:2mm}
"""
COPY='<div class="copy"><div class="c1">Takes about a minute.</div><div class="c2">Our volunteer cooks read every answer.</div></div>'
FOOT='<div class="foot">Or visit<br><b>%s</b></div>'%URL
FOOT2='<div class="foot plain">Prefer to type it?<b>%s</b></div>'%URL
FOOT3='<div class="foot plain">Find the survey at<b>%s</b></div>'%URL
HEAD='<div class="head"><span data-sticker="How was|your lunch?" data-size="90"></span></div>'
V={
1:(brand+HEAD+'<div class="qrcard"><div class="qrbox">@@QR@@</div><div class="scan">Scan to tell us</div></div>'+COPY+FOOT,""),
2:(brand+HEAD+'<div class="qrdirect"><div class="qrbox big">@@QR@@</div><div class="scanpill">Scan to tell us</div></div>'+COPY+FOOT2,
   ".qrdirect{display:flex;flex-direction:column;align-items:center;gap:6mm}.qrbox.big{width:116mm;height:116mm}.scanpill{background:var(--hvid);border-radius:999px;padding:3.5mm 11mm;font-family:var(--display);font-size:12.5mm;line-height:1}"),
3:(brand+HEAD+'<div class="qrwrap"><div class="qrcard"><div class="qrbox">@@QR@@</div></div><div class="tag"><span data-sticker="Scan to tell us" data-size="90"></span></div></div>'+COPY+FOOT3,
   ".qrwrap{position:relative;margin-bottom:6mm}.qrwrap .qrcard{padding:10mm 10mm 30mm}.qrwrap .tag{position:absolute;left:50%;bottom:-3mm;width:104mm;transform:translateX(-50%) rotate(-4deg);--s-fill:var(--pink)}"),
}
V[4]=(V[3][0].replace(FOOT3,FOOT),V[3][1])
for bgname,bg,tagfill in [("green","#DFFEAE","#FFE1FE"),("pink","#FFE1FE","#DFFEAE")]:
    for n,(main,css) in V.items():
        h=head.replace("Volunteers wanted (poster)","Survey poster %s %d"%(bgname,n)).replace("</style>",COMMON+".poster{background:%s}\n"%bg+css.replace("var(--pink)",tagfill)+"\n</style>",1)
        html=h+'<main class="poster">\n'+main.replace("@@QR@@",qr)+'\n</main>\n<script>\nfunction ripples(){}\n(()=>{'+sticker_js
        open("poster-survey-%s-%d.html"%(bgname,n),"w").write(html)

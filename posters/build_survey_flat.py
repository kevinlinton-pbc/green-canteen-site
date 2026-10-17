import re
base=open("poster-volunteers.src.html").read()
qr=re.sub(r'width="(\d+)" height="\d+"',r'viewBox="0 0 \1 \1"',open("qr-survey.svg").read(),count=1)
head=base[:base.index('<main class="poster">')]
brand=re.search(r'<div class="brand">.*?</div>',base,flags=re.S).group(0)
sticker_js=base[base.index('const NS="http://www.w3.org/2000/svg";'):]
URL="greencanteen.plantbasedcampus.org/feedback.html"
COMMON="""
.poster>*:not(.qrwrap){z-index:2}
.qrwrap{position:relative;z-index:1;isolation:isolate}
.head{width:196mm}
.qrcard{background:var(--hvid);border:.8mm solid var(--mork);border-radius:14mm;padding:9mm 9mm 10mm;display:flex;flex-direction:column;align-items:center;gap:6mm}
.qrcard .qrbox{width:92mm;height:92mm}
.qrcard .qrbox svg{width:100%;height:100%;display:block}
.qrcard .scan{font-family:var(--display);font-size:13mm;line-height:1}
.url{background:var(--mork);color:var(--lys);border-radius:999px;padding:3mm 9mm;font-size:5.6mm;border:.6mm solid var(--lys)}
"""
MAIN=brand+"""
  <div class="head"><span data-sticker="How was|your lunch?" data-size="90"></span></div>
  <div class="qrwrap"><div class="qrcard"><div class="qrbox">@@QR@@</div><div class="scan">Scan to tell us</div></div></div>
  <div class="facts"><div class="pill">Takes about a minute</div></div>
  <div class="lede"><span data-sticker="Our volunteer cooks|read every answer." data-size="40" data-plain="1" data-mm="7.4"></span></div>
  <div class="url">%s</div>"""%URL
def page(name,title,css):
    h=head.replace("Volunteers wanted (poster)",title).replace("</style>",COMMON+css+"\n</style>",1)
    js="<script>\nfunction ripples(){}\n(()=>{"+sticker_js
    html=h+'<main class="poster">\n'+MAIN.replace("@@QR@@",qr)+'\n</main>\n'+js
    open(name,"w").write(html)
page("poster-survey-1-plate.html","Survey poster 1 plate",
""".poster{background:#DFFEAE}
.qrwrap::before{content:"";position:absolute;left:50%;top:50%;width:262mm;height:150mm;transform:translate(-50%,-50%);border-radius:50%;background:var(--pink);border:.8mm solid var(--mork);z-index:-1}
""")
page("poster-survey-2-pink.html","Survey poster 2 pink",".poster{background:#FFE1FE}\n")
page("poster-survey-3-dark.html","Survey poster 3 dark",
""".poster{background:#111A03;color:var(--lys)}
.head{--s-fill:var(--pink)}
.sticker .l3{fill:var(--lys);stroke:var(--lys)}
.brand{background:var(--lys)}
.qrcard{background:var(--lys);color:var(--mork);border-color:var(--lys);box-shadow:0 0 0 1.6mm #111A03}
.pill{color:var(--mork);border-color:var(--lys);background:var(--pink)}
.url{background:var(--lys);color:var(--mork);border-color:var(--lys)}
""")
page("poster-survey-4-frame.html","Survey poster 4 frame",
""".poster{background:#fff}
.poster::before{content:"";position:absolute;left:10mm;right:10mm;top:10mm;bottom:10mm;background:#DFFEAE;border:.8mm solid var(--mork);border-radius:18mm}
""")
page("poster-survey-5-split.html","Survey poster 5 split",
""".poster{background:linear-gradient(#DFFEAE 0 51%,#1A2805 51% 51.25%,#FFE1FE 51.25%)}
""")

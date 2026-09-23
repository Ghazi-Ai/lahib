#!/usr/bin/env python3
"""يولّد نسخة PDF من بنك أسئلة لاحِب للمراجعة: data/lahib-bank.pdf
   الطريقة: يبني صفحة HTML عربية (اتجاه يمين-يسار) ثم يطبعها بمتصفح Chromium بلا واجهة.
   الاستخدام: python3 tools/build-pdf.py
   يحتاج: chromium أو google-chrome، وخط Cairo (خط الهوية الرسمي؛ نسخته في _work/brand/fonts/) أو بديل عربي."""
import json, os, re, sys, subprocess, tempfile, shutil, datetime, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT  = os.path.join(ROOT, "data", "lahib-bank.pdf")

def AR(n): return str(n).translate(str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩"))
def esc(s): return html.escape(str(s), quote=False)

src = open(os.path.join(ROOT, "data", "bank.js"), encoding="utf-8").read()
bank = json.loads(src[re.search(r"window\.LAHIB_BANK\s*=\s*", src).end():].rstrip().rstrip(";"))
tiers = bank["tiers"]; topics = bank["topics"]
total = sum(len(t["q"][x["id"]]) for t in topics for x in tiers)
today = datetime.date.today()

css = """
@page{ size:A4; margin:18mm 16mm 18mm 16mm }
*{box-sizing:border-box}
html{direction:rtl}
body{font-family:"Cairo","Noto Sans Arabic",sans-serif;font-size:11.5pt;line-height:1.7;color:#1D1F26;margin:0}
h1,h2,h3,.k{font-family:"Cairo",sans-serif}
.cover{height:250mm;display:flex;flex-direction:column;justify-content:center;text-align:center;break-after:page}
.cover .word{font-family:"Cairo",sans-serif;font-size:64pt;font-weight:800;color:#3C7162;line-height:1.1;margin:0}
.cover .sub{font-size:16pt;color:#4a4d57;margin:6mm 0 0}
.cover .meta{margin-top:14mm;font-size:11pt;color:#6B6D76;line-height:2}
.cover .rule{width:60mm;height:3px;margin:10mm auto;background:repeating-linear-gradient(90deg,#B9BBC1 0 6mm,transparent 6mm 10mm)}
.cover .disc{margin-top:16mm;font-size:9.5pt;color:#6B6D76}
.toc{break-after:page}
.toc h2{font-size:18pt;margin:0 0 6mm}
.toc table{width:100%;border-collapse:collapse;font-size:10.5pt}
.toc td{padding:2mm 2mm;border-bottom:1px solid #E4E5E8}
.toc td.n{width:14mm;color:#6B6D76;font-variant-numeric:tabular-nums}
.toc td.v{width:22mm;color:#6B6D76;font-variant-numeric:tabular-nums}
.toc td.s{color:#6B6D76;font-size:9.5pt}
.toc a{color:inherit;text-decoration:none}
.toc tr:hover td{background:#EDF3F1}
.toc td.p{width:14mm;text-align:left;color:#285246;font-weight:700;font-variant-numeric:tabular-nums}
.topic{position:relative}
.pgmark{position:absolute;top:0;inset-inline-end:0;color:#fff;font-size:6pt;line-height:1}
.topic{break-before:page}
.thead{border-inline-start:4px solid #3C7162;padding:2mm 4mm;margin:0 0 5mm;background:#EDF3F1;border-radius:0 3mm 3mm 0}
.thead h2{margin:0;font-size:17pt;font-weight:800}
.thead p{margin:0;color:#4a4d57;font-size:10.5pt}
.tier{margin:5mm 0 2mm;font-size:12.5pt;font-weight:800;padding:1.2mm 3mm;border-radius:2mm;display:inline-block;break-after:avoid}
.tier + .q{break-before:avoid}
.q{break-inside:avoid;margin:0 0 4.5mm;padding:3mm 3.5mm;border:1.2px solid var(--c);border-inline-start-width:4px;border-radius:2.5mm;background:var(--bg)}
.q .qt{margin:0 0 1.5mm;font-weight:700;font-size:11.5pt}
.q .qt b{color:var(--c);font-variant-numeric:tabular-nums;margin-inline-end:2mm}
.ans{background:#fff;border:1px solid var(--c2);border-radius:2mm;padding:2mm 3mm;font-size:10pt;line-height:1.65}
.ans b{color:var(--c)}
.ans .ref{display:block;color:var(--c);font-weight:700;font-size:9.5pt;margin-top:1mm;font-variant-numeric:tabular-nums}
/* لون واحد لكل رتبة: البرونزي بنّي، الفضي رمادي، الذهبي ذهبي */
.q.br,.tier.t-br{--c:#7B502D;--c2:#E3CDBB;--bg:#F8F1EB}
.q.si,.tier.t-si{--c:#4F5260;--c2:#CFD1D8;--bg:#F0F1F4}
.q.go,.tier.t-go{--c:#796B2A;--c2:#E2D9AE;--bg:#F5F1DF}
.tier{color:var(--c);background:var(--bg);border:1.2px solid var(--c2)}
.foot{position:fixed;bottom:-12mm;left:0;right:0;text-align:center;font-size:8.5pt;color:#9a9ca4}
"""

def build(pages=None):
    parts = [f"""<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>لاحِب — بنك الأسئلة</title><style>{css}</style></head><body>
<section class="cover">
  <p class="word">لاحِب</p>
  <p class="sub">بنك أسئلة كود الطرق السعودي — نسخة المراجعة</p>
  <div class="rule"></div>
  <p class="meta">{AR(total)} سؤالًا في {AR(len(topics))} موضوعًا، موضوع لكل مجلد من مجلدات الكود<br>
  ثلاث رتب: برونزي (معلومة تأسيسية) · فضي (اشتراط أو قاعدة) · ذهبي (قيمة دقيقة)<br>
  سؤال وجواب: كل سؤال مرفق بإجابته ومعلومة تُثبّت ومرجعه في الكود (المجلد والبند والصفحة)<br>
  الإصدار {esc(bank.get('version',''))} — {AR(today.strftime('%Y/%m/%d'))}</p>
  <p class="disc">مصدر الأسئلة: كود الطرق السعودي الصادر عن الهيئة العامة للطرق، والمرجع عند أي اختلاف هو نص الكود نفسه.<br>
  «لاحِب» عمل توعوي مستقل، وليس منتجًا رسميًّا صادرًا عن الهيئة.<br>فكرة وإعداد وإشراف: م. غازي السيف — نُفّذ بأدوات برمجية مساعدة تحت إشرافه ومراجعته.</p>
</section>
<section class="toc"><h2>المحتويات</h2><table>"""]
    for i, t in enumerate(topics, 1):
        n = sum(len(t["q"][x["id"]]) for x in tiers)
        pg = AR(pages[t["id"]]) if pages and t["id"] in pages else ""
        parts.append(f'<tr><td class="n">{AR(i)}</td><td><a href="#t-{t["id"]}"><b>{esc(t["name"])}</b></a></td>'
                     f'<td class="s">{esc(t.get("sub",""))}</td><td class="v">مجلد {esc(t["vol"])}</td>'
                     f'<td class="n">{AR(n)}</td><td class="p"><a href="#t-{t["id"]}">{pg}</a></td></tr>')
    parts.append("</table></section>")
    for i, t in enumerate(topics, 1):
        parts.append(f'<section class="topic" id="t-{t["id"]}"><div class="pgmark" dir="ltr">PGMARK{t["id"]}END</div>'
                     f'<div class="thead"><h2>{AR(i)}. {esc(t["name"])}</h2><p>{esc(t.get("sub",""))} — مجلد {esc(t["vol"])}</p></div>')
        num = 0
        for x in tiers:
            qs = t["q"].get(x["id"], [])
            if not qs: continue
            parts.append(f'<div class="tier t-{x["id"]}">{esc(x["name"])} · {AR(x["points"])} نقطة</div>')
            for q in qs:
                num += 1
                parts.append(f'<div class="q {x["id"]}"><p class="qt"><b>{AR(num)}.</b>{esc(q["q"])}</p>'
                             f'<div class="ans"><b>الإجابة:</b> {esc(q["opts"][q["a"]])}<br>{esc(q.get("note",""))}'
                             f'<span class="ref">المرجع: {esc(q["ref"])}</span></div></div>')
        parts.append("</section>")
    parts.append("</body></html>")
    return "".join(parts)

chrome = next((c for c in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable") if shutil.which(c)), None)
if not chrome: sys.exit("✗ لم يُعثر على Chromium لطباعة PDF")
tmp = tempfile.mkdtemp(prefix="lahib-pdf-")
def render(html_text, out):
    page = os.path.join(tmp, "bank.html")
    open(page, "w", encoding="utf-8").write(html_text)
    cmd = [chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
           "--virtual-time-budget=8000", f"--print-to-pdf={out}", "file://" + page]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300)

# الجولة الأولى: بلا أرقام صفحات، ثم نقرأ موضع كل علامة @@id@@ بـ pdftotext
first = os.path.join(tmp, "pass1.pdf")
render(build(), first)
pages = {}
if shutil.which("pdftotext"):
    txt = subprocess.run(["pdftotext", first, "-"], capture_output=True, text=True).stdout
    txt = re.sub("[\u200e\u200f\u202a-\u202e\u2066-\u2069]", "", txt)   # إزالة رموز الاتجاه
    for n, chunk in enumerate(txt.split("\f"), 1):
        for m in re.finditer(r"PGMARK(v\d+)END", chunk):
            pages.setdefault(m.group(1), n)
# الجولة الثانية: بأرقام الصفحات (حجم الفهرس ثابت فلا تتغير الأرقام)
render(build(pages), OUT)
shutil.rmtree(tmp, ignore_errors=True)
print(f"✓ {os.path.relpath(OUT, ROOT)} — {os.path.getsize(OUT)//1024} كيلوبايت، {AR(total)} سؤالًا")

import fs from 'fs';
const GAME = fs.readFileSync('index.html','utf8').match(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/)[1];
const BANKSRC = fs.readFileSync('data/bank.js','utf8').replace('window.LAHIB_BANK','global.window.LAHIB_BANK');

class El {
  constructor(tag='div'){ this.tagName=tag.toUpperCase(); this.children=[]; this._html=''; this._text='';
    this.style={}; this.dataset={}; this.hidden=false; this._cache=null;
    this.classList={ _s:new Set(), add:(...c)=>c.forEach(x=>this.classList._s.add(x)),
      remove:(...c)=>c.forEach(x=>this.classList._s.delete(x)),
      toggle:(c,f)=>{ f?this.classList._s.add(c):this.classList._s.delete(c); },
      contains:c=>this.classList._s.has(c) };
    this.disabled=false; this.onclick=null; this.value='';
  }
  set className(v){ this.classList._s=new Set(String(v).split(/\s+/).filter(Boolean)); }
  get className(){ return [...this.classList._s].join(' '); }
  set innerHTML(v){ this._html=v; this.children=[]; this._cache=null; }
  get innerHTML(){ return this._html; }
  set textContent(v){ this._text=String(v); this._html=String(v).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
  get textContent(){ return this._text; }
  setAttribute(k,v){ this[k]=v; }
  appendChild(c){ this.children.push(c); this._cache=null; return c; }
  querySelector(){ return this._i ||= new El(); }
  querySelectorAll(sel){
    if(!sel || !sel.includes('.cell')) return [];
    const key = sel + '|' + this.children.map(c=>c._html).join('');
    if(this._cache && this._cache.key===key) return this._cache.v;
    const out=[];
    this.children.forEach(col=>{
      const re=/<button class="cell (\w+)"\s*(disabled)?\s*data-ci="(\d+)" data-idx="(\d+)"/g;
      let m; while((m=re.exec(col._html))){
        if(m[2]) continue;
        const b=new El('button'); b.dataset={ci:m[3], idx:m[4]}; b.tier=m[1]; out.push(b);
      }
    });
    this._cache={key, v:out};
    return out;
  }
}

let store={}, clock=0, tickFn=null;
function boot(){
  store={}; clock=0; tickFn=null;
  global.document={ createElement:t=>new El(t), getElementById:id=>(store[id] ||= new El()) };
  global.window={ scrollTo(){} };
  global.setInterval=f=>{ tickFn=f; return 1; };
  global.clearInterval=()=>{ tickFn=null; };
  global.Date = class extends Date { static now(){ return clock; } };
  ['picking','boardview','qview','final','q-opts','q-judge','q-hold','q-reveal','q-tally','q-actions']
    .forEach(id=>{ global.document.getElementById(id).hidden=true; });
  eval(BANKSRC); eval(GAME);
}
const $=id=>global.document.getElementById(id);
const advance=ms=>{ clock+=ms; if(tickFn) tickFn(); };

let pass=0, fail=0;
const ok=(c,m)=>{ c?pass++:(fail++, console.log('  ✗ '+m)); };
const ar=n=>String(n).replace(/\d/g,d=>'٠١٢٣٤٥٦٧٨٩'[d]);
const cells=()=>$('board').querySelectorAll('.cell:not([disabled])');
const scores=()=>[...$('scores').innerHTML.matchAll(/class="pt num">([^<]+)</g)].map(m=>m[1]);
// الخيار الصحيح = الذي نصه يطابق opts[a] للسؤال الحالي
function clickOption(correct, q){
  const box=$('q-opts');
  const target = correct ? q.opts[q.a] : q.opts.find((o,i)=>i!==q.a);
  const esc=t=>t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  const btn = box.children.find(b=>b._html.includes(esc(target)));
  btn.onclick();
}
async function newGame(mode,size){
  boot(); window.setMode(mode);
  window.updateSize(size);
  $('t1').value='ألف'; $('t2').value='باء';
  window.startPicking();
  const n=Math.min(size,4)*2;
  for(let i=0;i<n;i++) $('picks').children.find(c=>!c.disabled).onclick();
  await new Promise(r=>setTimeout(r,600));
}
// يلتقط السؤال المعروض حاليًّا من البنك عبر مطابقة النص
function currentQ(){
  const txt=$('q-text').textContent;
  for(const t of window.LAHIB_BANK.topics) for(const k of ['br','si','go'])
    for(const q of t.q[k]) if(q.q===txt) return q;
  return null;
}

console.log('— تدفّق السؤال واحتساب النقاط —\n');

/* ══ 1) صاحب الدور صح ← يأخذ النقاط ══ */
await newGame('full',2);
cells()[0].onclick();
ok($('q-opts').hidden===false && $('q-hold').hidden===true,'الخيارات تظهر فورًا');
advance(30000);
ok($('q-opts').hidden===false,'الخيارات تبقى ظاهرة');
let q=currentQ(); ok(!!q,'تعذّر إيجاد السؤال في البنك');
clickOption(true,q);                                  // ألف صح
ok($('q-turn').innerHTML.includes('باء'),'انتقل الدور للفريق الثاني');
q=currentQ(); clickOption(true,q);                    // باء صح أيضًا
window.nextTurn();
ok(scores()[0]==='١٠٠' && scores()[1]==='٠', 'صاحب الدور فقط يأخذ النقاط — النتيجة: '+scores());
ok($('q-reveal').hidden===false,'شاشة الكشف ظاهرة');
ok($('r-ref').textContent.startsWith('المرجع:'),'المرجع معروض');
ok($('r-note').textContent.length>10,'المعلومة التثبيتية معروضة');

/* ══ 2) صاحب الدور خطأ والثاني صح ← الثاني يأخذ النقاط ══ */
await newGame('full',2);
cells()[0].onclick(); advance(30000);
q=currentQ(); clickOption(false,q);                   // ألف خطأ
q=currentQ(); clickOption(true,q);                    // باء صح
window.nextTurn();
ok(scores()[0]==='٠' && scores()[1]==='١٠٠','انتقال النقاط للفريق الثاني — النتيجة: '+scores());

/* ══ 3) الاثنان خطأ ← لا نقاط ══ */
await newGame('full',2);
cells()[0].onclick(); advance(30000);
q=currentQ(); clickOption(false,q);
q=currentQ(); clickOption(false,q);
ok($('q-tally').innerHTML.includes('لا نقاط'),'لا نقاط عند خطأ الفريقين');
ok($('q-tally').innerHTML.includes('لا نقاط'),'رسالة «لا نقاط» معروضة');

/* ══ 4) تبديل الدور بعد كل سؤال ══ */
window.nextTurn();
ok($('scores').innerHTML.indexOf('الدور عليه الآن') > $('scores').innerHTML.indexOf('باء') - 200,'تبديل الدور');
const html=$('scores').innerHTML;
ok(html.split('باء')[1] && html.split('باء')[1].includes('الدور عليه الآن'),'الدور صار للفريق الثاني');

/* ══ 5) انتهاء الوقت = إجابة خاطئة ══ */
await newGame('full',2);
cells()[0].onclick();
advance(60000);                                        // انتهى وقت الفريق الأول
ok($('q-turn').innerHTML.includes('باء'),'انتهاء الوقت ينقل الدور للفريق الثاني');
advance(20000);                                        // انتهى وقت الثاني
ok($('q-reveal').hidden===false,'الكشف بعد انتهاء وقت الفريقين');
window.nextTurn();
ok(scores()[0]==='٠' && scores()[1]==='٠','لا نقاط عند انتهاء الوقتين');

/* ══ 6) النمط الثاني: الذهبي بلا خيارات ══ */
await newGame('hard',2);
const gold=cells().filter(c=>c.tier==='go');
ok(gold.length>0,'توجد خانات ذهبية');
gold[0].onclick();
ok($('q-judge').hidden===false,'أزرار تحكيم المقدّم ظاهرة في السؤال الذهبي');
ok($('q-opts').hidden===true,'لا خيارات في السؤال الذهبي');
window.judge(true);                                    // ألف صح
ok($('q-turn').innerHTML.includes('باء'),'انتقل للفريق الثاني بعد التحكيم');
window.judge(false);
window.nextTurn();
ok(scores()[0]==='٥٠٠','الرتبة الذهبية تمنح 500 نقطة — '+scores());

/* ══ 7) البرونزي في النمط الثاني يبقى بخيارات ══ */
await newGame('hard',2);
const bronze=cells().filter(c=>c.tier==='br');
bronze[0].onclick();
ok($('q-judge').hidden===true,'لا تحكيم يدوي في البرونزي بالنمط الثاني');
advance(30000);
ok($('q-opts').hidden===false,'البرونزي يعرض خيارات في النمط الثاني');

/* ══ 8) اكتمال الجولة يعرض النتيجة النهائية ══ */
await newGame('full',2);
let guard=0;
while($('final').hidden && guard++ < 60){
  const c=cells(); if(!c.length) break;
  c[0].onclick(); advance(30000);
  let cq=currentQ(); clickOption(true,cq);
  cq=currentQ(); clickOption(false,cq);
  window.nextTurn();
}
ok($('final').hidden===false,'شاشة النتيجة النهائية ظهرت بعد '+guard+' سؤالًا');
ok(guard===24,'عدد أسئلة الجولة (فردان ← 4 مواضيع) = 24، وجدنا '+guard);
ok($('f-winner').textContent.includes('فاز')||$('f-winner').textContent.includes('تعادل'),'نص النتيجة: '+$('f-winner').textContent);

/* ══ 9) وسائل المساعدة — لصاحب الدور فقط، مرة واحدة لكل فريق ══ */
const alive=()=>$('q-opts').children.filter(b=>!b.classList.contains('gone'));
const esc2=t=>t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
await newGame('full',2);
cells()[0].onclick();
q=currentQ();
ok($('q-aids').hidden===false && $('q-aids').innerHTML.includes('ألف'),'شريط الوسائل باسم صاحب الدور');
window.useAid('half');
ok(alive().length===2,'حذف خيارين أبقى خيارين — وجدنا '+alive().length);
ok(alive().some(b=>b._html.includes(esc2(q.opts[q.a]))),'الخيار الصحيح لم يُحذف');
window.useAid('half');
ok(alive().length===2 && $('q-aids').innerHTML.includes('disabled'),'لا تُستخدم الوسيلة مرتين');
window.useAid('help');
ok($('q-time').textContent==='٩٠','طلب المساعدة أضاف ٣٠ ثانية — '+$('q-time').textContent);
clickOption(true,q);                                   // ألف صح → المرحلة B
ok($('q-turn').innerHTML.includes('باء'),'انتقل الدور للفريق الثاني');
ok(alive().length===2,'الفريق الثاني يرى الخيارين المتبقيين لا الأربعة — وجدنا '+alive().length);
ok($('q-aids').hidden===true,'لا شريط وسائل للفريق الثاني');
window.useAid('half'); window.useAid('swap'); window.useAid('help');
ok(alive().length===2 && $('q-time').textContent==='٢٠','الفريق الثاني لا يستطيع استخدام أي وسيلة');
q=currentQ(); clickOption(false,q); window.nextTurn();
ok($('scores').innerHTML.split('class="used"').length-1===2,'وسيلتا صاحب الدور مشطوبتان والفريق الثاني كامل الوسائل');
cells()[0].onclick();
ok($('q-aids').innerHTML.includes('باء'),'في الدور التالي الوسائل لباء');
window.useAid('half');
ok(alive().length===2,'باء يستخدم حذف خيارين في دوره');

/* ══ 10) تبديل السؤال — يكشف إجابة الحالي أولًا، ثم المقدّم يعرض البديل ══ */
await newGame('full',2);
cells()[0].onclick();
advance(20000);
const before=$('q-text').textContent; const bq=currentQ();
window.useAid('swap');
ok($('q-reveal').hidden===false && $('r-ans').textContent===bq.opts[bq.a],'إجابة السؤال الحالي تُكشف للفائدة');
ok($('q-text').textContent===before,'السؤال لم يتغير قبل ضغط المقدّم');
ok($('q-actions').innerHTML.includes('swapNow'),'زر «اعرض السؤال البديل» ظاهر');
clickOption(true,bq);
ok($('q-turn').innerHTML.includes('تبديل') && scores()[0]==='٠','لا تُحتسب إجابة أثناء التبديل');
window.useAid('help');
ok($('q-time').textContent==='—','لا وسائل أثناء التبديل والمؤقّت متوقف');
window.swapNow();
ok($('q-text').textContent!==before,'نص السؤال تغيّر بعد ضغط المقدّم');
ok($('q-time').textContent==='٦٠','المؤقّت عاد إلى ٦٠ بعد التبديل');
ok($('q-reveal').hidden===true && $('q-opts').hidden===false && alive().length===4,'الكشف اختفى والخيارات الأربعة للسؤال البديل ظاهرة');
q=currentQ(); ok(!!q && q.q===$('q-text').textContent,'السؤال البديل موجود في البنك');
window.useAid('swap');
ok($('q-text').textContent===q.q && $('q-reveal').hidden===true,'لا تبديل ثانٍ للفريق نفسه');
clickOption(true,q); q=currentQ(); clickOption(false,q); window.nextTurn();
ok(scores()[0]==='١٠٠' && $('boardview').hidden===false && cells().length>0,'الجولة تكمل طبيعيًّا بعد التبديل — '+scores());

/* ══ 11) ضبط النقاط للمقدّم ══ */
await newGame('full',2);
window.adjust(0,50); window.adjust(1,-50);
ok(scores()[0]==='٥٠' && scores()[1]==='٠','إضافة ٥٠ وعدم النزول تحت الصفر — '+scores());
window.adjust(0,-100);
ok(scores()[0]==='٠','الخصم يتوقف عند الصفر — '+scores());
ok($('scores').innerHTML.includes('adjust(0,50)'),'أزرار الضبط ظاهرة في بطاقة النتيجة');

console.log(`\nالنتيجة: ${pass} ناجح، ${fail} فاشل`);
process.exit(fail?1:0);

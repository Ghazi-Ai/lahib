# دليل توليد صور لعبة لاحِب

> **تحديث ٢٢ سبتمبر ٢٠٢٦ — الأسلوب المعتمد صار واقعيًّا.**
> بعد تجربة الأسلوب المسطّح على `v308` بدت الصورة فقيرة، فاعتُمد بدله **تصيير ثلاثي الأبعاد واقعي**
> بمواد حقيقية وإضاءة نهار ناعمة وألوان هادئة من لوحة الهيئة نفسها. قيود الهوية لم تتغير:
> لا نص، لا شعار، لا نخلة، لا درع. رمز لاحِب وحده يبقى مسطّحًا لأنه شعار.
> **الشعار المعتمد** هو الأيقونة (طريق أبيض على مربع أخضر)، ويُستخدم في التبويب والترويسة معًا.
>
> **البرومبتات الجاهزة (٣١ ملفًا، صورة واحدة لكل ملف) في `assets/prompts/`**، وكل ملف يذكر مسار الحفظ في آخره.
> تُولَّد كلها بأمر واحد من Codex في الطرفية:
>
> ```bash
> codex "لكل ملف في assets/prompts/ بالترتيب: اقرأه، ولّد الصورة الموصوفة فيه بأداة توليد الصور، واحفظها في المسار المذكور في آخر الملف. تخطَّ أي ملف صورته موجودة مسبقًا."
> ```
>
> ثم `python3 tools/check-images.py`. الصور تُحفظ PNG ثم تُحوَّل WebP وتُنقل أصولها إلى `_work/png-originals/`.
> ما يلي هو الدليل الأصلي (الأسلوب المسطّح) ويبقى مرجعًا للمواضيع والألوان والمقاسات.

ملف جاهز لتسليمه إلى ChatGPT أو Gemini لإنتاج صور اللعبة كاملة — **٣٢ صورة**:
٢٥ لبطاقات المواضيع، ٢ لبطاقتي نمط اللعب، ٣ لميداليات الرتب، ٢ لرمز اللعبة.


---

## الهوية البصرية — مشتقّة من شعار الهيئة العامة للطرق

لوحة ألوان اللعبة كلها مستخرَجة من شعار الهيئة نفسه، لا مختارة اعتباطًا:

| اللون | القيمة | موضعه في الشعار | استعماله في اللعبة |
|---|---|---|---|
| أخضر مزرقّ | `#4D7F71` | النخلة والدرع | اللون الأساسي للواجهة |
| ذهبي خاكي | `#B7A44D` | خطا الطريق داخل الدرع | الرتبة الذهبية والتمييز |
| رمادي دافئ | `#76777A` | اسم الهيئة | المحايدات والنصوص الثانوية |

ومنها اشتُقّت درجات الوضعين الفاتح والليلي بما يحقق تباينًا مقروءًا (٤٫٥:١ فأعلى).


**الطابع العام المستوحى:** هوية الهيئة مسطّحة، هندسية، مكتومة الإشباع، قليلة الزخرفة،
تعتمد أشكالًا صلبة بسيطة بلا تدرّجات لونية ولا ظلال قوية. هذا هو الطابع الذي تحمله الصور الاثنتان والثلاثون.


> **حد فاصل مقصود:** الصور ترث من الهوية **اللون واللغة الهندسية فقط**.
> لا نخلة، ولا درع، ولا ختم رسمي، ولا أي عنصر من عناصر الشعار — فذلك تقليد لعلامة جهة حكومية لا استلهام منها.


---

## كيف تستخدمه

**المقترح:** اضبط **صورة مرجعية واحدة** في ChatGPT (ابدأ بـ `v308` طبقات الرصف، فشكله واضح ومحدّد)،
وكرّر عليها حتى تضبط الزاوية وسماكة الخطوط ودرجة التبسيط.
ثم ارفعها في Gemini كمرجع بصري وولّد الـ٣١ الباقية بصيغة «نفس الأسلوب تمامًا، الموضوع الجديد كذا».

١. الصق **كتلة الأسلوب** أدناه مرة واحدة في بداية المحادثة.
٢. أرسل وصف كل صورة على حدة واطلب توليدها.
٣. احفظ كل صورة **بالاسم المذكور بالضبط** في مجلدها.
٤. افتح `index.html` — الصور تظهر تلقائيًّا، وما لم يُرفع بعدُ يظهر مكانه إطار ملوّن فلا تنكسر الواجهة.


> **لا نص داخل أي صورة إطلاقًا.** النص العربي المولَّد يخرج مشوّهًا وغير قابل للتصحيح،
> وكل الكتابة تأتي من الصفحة نفسها فوق الصورة.


---

## كتلة الأسلوب — الصقها أولًا

```
I need a set of 32 illustrations for an educational quiz game about the Saudi Highway Code,
an official technical code published by the Roads General Authority of Saudi Arabia.
They must look like one coherent set drawn by the same illustrator on the same day.

SHARED STYLE for every image:
Flat vector illustration, institutional-technical style — restrained and precise, not playful.
Three-quarter isometric view, consistent light direction from the upper left.
Solid geometric shapes with flat fills. No gradients, no glow, no drop shadows, no outlines.
Muted, desaturated palette — nothing neon or candy-coloured.
Saudi Arabian desert and road-infrastructure setting.
Centred composition, whole subject inside the frame with generous margin.
Flat single-colour background, no texture, no pattern, no border or frame.

BASE PALETTE (use for everything that is not the accent):
  sand        #EFEDE8
  warm grey   #76777A
  asphalt     #3A3D3C
  off-white   #FFFFFF
I will name ONE accent colour per image. Use it for the main subject only;
keep every supporting element in the base palette.

STRICT RULES: absolutely no text, no letters, no numbers, no captions, no watermarks,
no logos, no brand marks, no government emblems, no palm trees, no shields or crests,
no national symbols. No recognisable human faces.

I will send the images one at a time. Generate a single image each time, at the stated size.
```


---

## المجموعة الأولى — بطاقات المواضيع (٢٥ صورة)

**المجلد:** `assets/topics/` · **المقاس:** ‎760×400‎ بكسل (نسبة 19:10) · **PNG**


الصورة تُقصّ لتملأ الإطار، فاجعل العنصر الرئيس في الوسط.
لون كل صورة مشتقّ من محور مجلدها في الكود، والمحاور كلها تدور حول أخضر الهيئة.


### 1. `v101.png` — قانون الطريق
*نطاق الكود وأحكامه — كود 101*

```
Image 1 of 32. Size 760x400 px (19:10 landscape).
Accent colour: #387161 (authority green). Background: flat #E6F2EF.
Subject: An open technical code manual lying flat, its pages fanning out, with an embossed official-looking seal (abstract, no emblem) and a small ribbon of highway emerging from the pages and curving away.
Same shared style, base palette and strict rules as stated above. No text of any kind.
```

### 2. `v201.png` — قبل أن يُرسم الطريق
*عملية التخطيط — كود 201*

```
Image 2 of 32. Size 760x400 px (19:10 landscape).
Accent colour: #387151 (deep teal). Background: flat #E6F2EB.
Subject: A planning desk seen from above: a regional map, drafting compass and scale ruler, with one future road corridor traced across the map as a bright highlighted band.
Same shared style, base palette and strict rules as stated above. No text of any kind.
```

### 3. `v202.png` — خرائط وإحداثيات
*الأعمال المساحية — كود 202*

```
Image 3 of 32. Size 760x400 px (19:10 landscape).
Accent colour: #387151 (deep teal). Background: flat #E6F2EB.
Subject: A surveyor's total station on a tripod standing on open desert ground, with a faint coordinate grid and elevation contour lines overlaid across the terrain behind it.
Same shared style, base palette and strict rules as stated above. No text of any kind.
```

### 4. `v203.png` — قراءة الأرض
*الدراسات الأولية — كود 203*

```
Image 4 of 32. Size 760x400 px (19:10 landscape).
Accent colour: #387151 (deep teal). Background: flat #E6F2EB.
Subject: A cylindrical soil core sample standing upright showing distinct stratified layers, next to a small geotechnical drilling rig on desert ground.
Same shared style, base palette and strict rules as stated above. No text of any kind.
```

### 5. `v301.png` — رسم المسار
*التصميم الهندسي للطرق — كود 301*

```
Image 5 of 32. Size 760x400 px (19:10 landscape).
Accent colour: #38713B (slate blue). Background: flat #E6F2E6.
Subject: A sweeping dual-carriageway highway curve with lane markings and a central median, shown as a clean design ribbon laid over bare terrain, with faint geometric arcs indicating the curve radius.
Same shared style, base palette and strict rules as stated above. No text of any kind.
```

### 6. `v302.png` — إلى أين تذهب المياه
*الهيدرولوجيا والتصميم الهيدروليكي — كود 302*

```
Image 6 of 32. Size 760x400 px (19:10 landscape).
Accent colour: #38713B (slate blue). Background: flat #E6F2E6.
Subject: A cutaway of a box culvert passing beneath a road embankment, with a lined drainage channel and stylised flowing water entering one side and exiting the other.
Same shared style, base palette and strict rules as stated above. No text of any kind.
```

### 7. `v303.png` — محطات الطريق
*الاستراحات وفحص الشاحنات والمواقف — كود 303*

```
Image 7 of 32. Size 760x400 px (19:10 landscape).
Accent colour: #38713B (slate blue). Background: flat #E6F2E6.
Subject: A desert highway rest area: shaded canopies over parking bays, a small service building, a truck bay to one side, and a slip road connecting to the main highway.
Same shared style, base palette and strict rules as stated above. No text of any kind.
```

### 8. `v304.png` — حين تخرج المركبة
*أنظمة السلامة الخاملة والحواجز — كود 304*

```
Image 8 of 32. Size 760x400 px (19:10 landscape).
Accent colour: #38713B (slate blue). Background: flat #E6F2E6.
Subject: A W-beam steel guardrail running along a road shoulder, with a crash cushion attenuator at its leading end, and a dashed arc showing a vehicle path being safely redirected.
Same shared style, base palette and strict rules as stated above. No text of any kind.
```

### 9. `v305.png` — منطقة أعمال
*تصميم منطقة أعمال الطرق — كود 305*

```
Image 9 of 32. Size 760x400 px (19:10 landscape).
Accent colour: #38713B (slate blue). Background: flat #E6F2E6.
Subject: A road work zone: a tapering line of traffic cones narrowing two lanes into one, temporary barriers, and an arrow board trailer directing traffic.
Same shared style, base palette and strict rules as stated above. No text of any kind.
```

### 10. `v306.png` — أضواء وأسلاك
*المنافع والإنارة وأجهزة التحكم — كود 306*

```
Image 10 of 32. Size 760x400 px (19:10 landscape).
Accent colour: #38713B (slate blue). Background: flat #E6F2E6.
Subject: Tall highway light poles casting cones of light at dusk, with a cutaway strip beneath the road revealing colour-coded utility ducts and cables.
Same shared style, base palette and strict rules as stated above. No text of any kind.
```

### 11. `v307.png` — خضرة ولوحات
*المسطحات الخضراء والإعلانات الخارجية — كود 307*

```
Image 11 of 32. Size 760x400 px (19:10 landscape).
Accent colour: #38713B (slate blue). Background: flat #E6F2E6.
Subject: A landscaped road median planted with low shrubs and desert-tolerant trees, with a blank roadside billboard structure standing beside the carriageway.
Same shared style, base palette and strict rules as stated above. No text of any kind.
```

### 12. `v308.png` — تحت الإسفلت
*تصميم الرصف — كود 308*

```
Image 12 of 32. Size 760x400 px (19:10 landscape).
Accent colour: #38713B (slate blue). Background: flat #E6F2E6.
Subject: A clean cutaway block of road pavement showing four distinct stacked layers from dark asphalt surface down through base, subbase and subgrade, with a tyre resting on the surface.
Same shared style, base palette and strict rules as stated above. No text of any kind.
```

### 13. `v309.png` — مختبر المواد
*مواصفات المواد والاختبارات القياسية — كود 309*

```
Image 13 of 32. Size 760x400 px (19:10 landscape).
Accent colour: #38713B (slate blue). Background: flat #E6F2E6.
Subject: A materials testing bench: a stack of nested test sieves, sample tins of graded aggregate, a conical flask and a compaction mould, arranged neatly.
Same shared style, base palette and strict rules as stated above. No text of any kind.
```

### 14. `v310.png` — جسور وأنفاق
*تصميم الجسور والأنفاق — كود 310*

```
Image 14 of 32. Size 760x400 px (19:10 landscape).
Accent colour: #38713B (slate blue). Background: flat #E6F2E6.
Subject: A concrete girder bridge spanning a dry wadi, its piers rising from the valley floor, with an arched tunnel portal cut into the rock face beyond it.
Same shared style, base palette and strict rules as stated above. No text of any kind.
```

### 15. `v401.png` — من الورق إلى الأرض
*إنشاء الطرق — كود 401*

```
Image 15 of 32. Size 760x400 px (19:10 landscape).
Accent colour: #715138 (desert ochre). Background: flat #F2EBE6.
Subject: A yellow road roller compacting a freshly laid embankment layer, with the compacted smooth surface behind it and loose material ahead.
Same shared style, base palette and strict rules as stated above. No text of any kind.
```

### 16. `v402.png` — بناء العبور
*إنشاء الجسور والأنفاق — كود 402*

```
Image 16 of 32. Size 760x400 px (19:10 landscape).
Accent colour: #715138 (desert ochre). Background: flat #F2EBE6.
Subject: A crawler crane lifting a long precast concrete bridge girder into position between two completed bridge piers.
Same shared style, base palette and strict rules as stated above. No text of any kind.
```

### 17. `v403.png` — تجهيز الطريق
*إنشاء مرافق الطرق — كود 403*

```
Image 17 of 32. Size 760x400 px (19:10 landscape).
Accent colour: #715138 (desert ochre). Background: flat #F2EBE6.
Subject: Large reinforced concrete pipes laid in an open trench beside the road, with a precast manhole chamber being lowered into place.
Same shared style, base palette and strict rules as stated above. No text of any kind.
```

### 18. `v501.png` — عمر الرصف
*نظم إدارة صيانة الرصف — كود 501*

```
Image 18 of 32. Size 760x400 px (19:10 landscape).
Accent colour: #653871 (muted plum). Background: flat #F0E6F2.
Subject: A stretch of asphalt showing progressive surface distress — fine cracking developing into a crack network — with a survey vehicle scanning it from above with a laser fan.
Same shared style, base palette and strict rules as stated above. No text of any kind.
```

### 19. `v502.png` — صحة الجسور
*نظم صيانة الجسور والأنفاق وإدارتها — كود 502*

```
Image 19 of 32. Size 760x400 px (19:10 landscape).
Accent colour: #653871 (muted plum). Background: flat #F0E6F2.
Subject: A bridge inspection unit truck parked on a bridge deck with its articulated arm folded down beneath the deck soffit, an inspector platform at its end.
Same shared style, base palette and strict rules as stated above. No text of any kind.
```

### 20. `v503.png` — صيانة المرافق
*نظم صيانة مرافق الطرق وإدارتها — كود 503*

```
Image 20 of 32. Size 760x400 px (19:10 landscape).
Accent colour: #653871 (muted plum). Background: flat #F0E6F2.
Subject: A roadside maintenance scene: an open equipment control cabinet, a light pole with its access hatch open, and a service van parked on the hard shoulder.
Same shared style, base palette and strict rules as stated above. No text of any kind.
```

### 21. `v601.png` — نبض الحركة
*هندسة المرور — كود 601*

```
Image 21 of 32. Size 760x400 px (19:10 landscape).
Accent colour: #713D38 (clay red). Background: flat #F2E7E6.
Subject: A signalised four-arm intersection viewed from directly above, with traffic signal heads at each approach and smooth flowing streams of vehicles shown as tapered ribbons.
Same shared style, base palette and strict rules as stated above. No text of any kind.
```

### 22. `v602.png` — لغة اللافتات
*الدليل الموحد لأجهزة التحكم المروري — كود 602*

```
Image 22 of 32. Size 760x400 px (19:10 landscape).
Accent colour: #713D38 (clay red). Background: flat #F2E7E6.
Subject: A group of completely blank road sign blanks on posts: a red octagon, a white inverted triangle with red border, a blue circle, and a yellow diamond — all faces entirely empty with no symbols or writing.
Same shared style, base palette and strict rules as stated above. No text of any kind.
```

### 23. `v603.png` — نحو صفر وفيات
*سلامة الطرق — كود 603*

```
Image 23 of 32. Size 760x400 px (19:10 landscape).
Accent colour: #713D38 (clay red). Background: flat #F2E7E6.
Subject: A safe-system street scene: a raised protected pedestrian crossing, roadside safety barriers, a separated cycle path, and a protective shield motif floating subtly above the scene.
Same shared style, base palette and strict rules as stated above. No text of any kind.
```

### 24. `v701.png` — الطريق والبيئة
*الجوانب البيئية للطرق — كود 701*

```
Image 24 of 32. Size 760x400 px (19:10 landscape).
Accent colour: #386771 (olive green). Background: flat #E6F0F2.
Subject: A highway running past protected desert habitat, with a tall noise barrier on one side and a vegetated wildlife crossing bridge arching over the carriageway.
Same shared style, base palette and strict rules as stated above. No text of any kind.
```

### 25. `v801.png` — طريق بلا سائق
*متطلبات المركبات ذاتية القيادة — كود 801*

```
Image 25 of 32. Size 760x400 px (19:10 landscape).
Accent colour: #38715A (sea green). Background: flat #E6F2ED.
Subject: A sleek autonomous vehicle travelling on a smart highway, emitting concentric sensor arcs, with roadside communication units on poles exchanging signal waves with it.
Same shared style, base palette and strict rules as stated above. No text of any kind.
```

---

## المجموعة الثانية — بطاقتا نمط اللعب (صورتان)

**المجلد:** `assets/modes/` · **المقاس:** ‎960×400‎ بكسل (نسبة 12:5) · **PNG**


### 26. `mode-full.png` — المسابقة كاملة بخيارات

```
Image 26 of 32. Size 960x400 px (12:5 landscape).
Accent colour: #387161 (authority green). Background: flat #E6F2EF.
Subject: A row of four identical blank answer tiles floating side by side above a flat game board, all four evenly lit and clearly visible, one of them slightly raised to read as chosen. The tile faces are completely empty.
Same shared style, base palette and strict rules as stated above. No text of any kind.
```

### 27. `mode-gold.png` — الذهبي بدون خيارات

```
Image 27 of 32. Size 960x400 px (12:5 landscape).
Accent colour: #796B2A (authority gold). Background: flat #F0ECDB.
Subject: A single tall card standing alone in a pool of light on a darkened flat stage, with no answer tiles anywhere around it, and a small podium microphone silhouette at the lower edge suggesting a spoken answer. The card face is completely blank.
Same shared style, base palette and strict rules as stated above. No text of any kind.
```

---

## المجموعة الثالثة — ميداليات الرتب (٣ صور)

**المجلد:** `assets/ranks/` · **المقاس:** ‎400×400‎ بكسل (مربّع) · **PNG بخلفية شفافة**


تُعرض داخل قرص دائري، فاجعل التصميم متمركزًا ولا تضع تفاصيل مهمة قرب الحواف.


### 28. `rank-br.png` — برونزي — ١٠٠ نقطة

```
Image 28 of 32. Size 400x400 px (perfect square), transparent background.
Subject: A flat circular medallion in warm bronze #8A5A32, its face showing a straight road running to the horizon with a single dashed centre line.
Flat vector, no metallic gradient or shine — suggest the metal with a single solid tone
and one slightly darker tone for depth. Centred, filling most of the square.
Absolutely no text, no numerals, no laurel wreaths, no national emblems, no palm trees.
```

### 29. `rank-si.png` — فضي — ٢٥٠ نقطة

```
Image 29 of 32. Size 400x400 px (perfect square), transparent background.
Subject: A flat circular medallion in cool silver #8C8D90, its face showing a road forking into two branches, with a simple chevron marking above the split.
Flat vector, no metallic gradient or shine — suggest the metal with a single solid tone
and one slightly darker tone for depth. Centred, filling most of the square.
Absolutely no text, no numerals, no laurel wreaths, no national emblems, no palm trees.
```

### 30. `rank-go.png` — ذهبي — ٥٠٠ نقطة

```
Image 30 of 32. Size 400x400 px (perfect square), transparent background.
Subject: A flat circular medallion in authority gold #B7A44D, its face showing a cloverleaf highway interchange seen from directly above.
Flat vector, no metallic gradient or shine — suggest the metal with a single solid tone
and one slightly darker tone for depth. Centred, filling most of the square.
Absolutely no text, no numerals, no laurel wreaths, no national emblems, no palm trees.
```

---

## المجموعة الرابعة — رمز لاحِب (صورتان)

**المجلد:** `assets/brand/` · **PNG بخلفية شفافة**


الرمز **مجرّد بلا كتابة** — اسم «لاحِب» يُكتب في الصفحة بخط Cairo الحقيقي بجواره.


«اللاحِب» في العربية هو الطريق الواسع الواضح المسلوك — فالرمز طريق مفتوح يمتد إلى أفق.
يرث من هوية الهيئة لونها ولغتها الهندسية المسطّحة، ويفترق عنها في الصورة الظلّية:
لا درع يحيط به، ولا نخلة، وتكوينه مفتوح غير متماثل — فلا يُخلط بالشعار الرسمي.


### 31. `lahib-mark.png` — الرمز (ترويسة الصفحة)

```
Image 31 of 32. Size 512x512 px (perfect square), transparent background.
Colours: main shape #3C7162 (authority green), single accent detail #796B2A (authority gold).
Subject: A minimal abstract logo mark, open and free-standing with no enclosing shape.
A road ribbon seen in one-point perspective, wide at the bottom edge and tapering as it rises,
bending gently to one side so the composition is asymmetric, ending at an open horizon line.
Three evenly spaced dashes run up its centre line; the topmost dash is the gold accent.
Built from straight edges and flat solid fills, in the same geometric language as a
government infrastructure identity: precise, restrained, confident.
No shield, no badge, no circle, no crest, no palm tree, no frame around it.
Must stay legible at 24x24 pixels.
Absolutely no text, no letters, no numerals, no tagline.
```

### 32. `lahib-icon.png` — الأيقونة (تبويب المتصفح)

```
Image 32 of 32. Size 512x512 px (perfect square), no transparency.
Subject: The exact same road mark from image 31, rendered in solid white,
centred on a solid #3C7162 rounded-square background
with a generous margin of about 18% on every side. Nothing else in the frame.
Flat, crisp, high contrast, legible when scaled down to 16x16 pixels.
Absolutely no text, no letters, no numerals.
```

---

## بعد التوليد

| المجلد | العدد | المقاس |
|---|---|---|
| `assets/topics/` | ٢٥ | 760×400 |
| `assets/modes/` | ٢ | 960×400 |
| `assets/ranks/` | ٣ | 400×400 |
| `assets/brand/` | ٢ | 512×512 |

**تحقّق:** `python3 tools/check-images.py` — يخبرك أي صورة ناقصة وأي مقاس غير مطابق والحجم الكلي.


**الحجم:** إن تجاوز المجموع بضعة ميغابايتات، أخبرني أضغطها أو أحوّلها WebP — الفرق ملموس على سرعة الفتح من GitHub Pages.

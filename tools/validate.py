#!/usr/bin/env python3
"""مدقّق بنك أسئلة لعبة لاحِب.
   الاستخدام:  python3 tools/validate.py
   يفحص data/bank.js ويبلّغ عن أي خلل في البنية أو نقص في التغطية."""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "data", "bank.js")
CELLS_PER_TIER = 2          # عدد الخانات لكل رتبة في كل موضوع على اللوحة

def load():
    src = open(PATH, encoding="utf-8").read()
    m = re.search(r"window\.LAHIB_BANK\s*=\s*", src)
    if not m:
        sys.exit("✗ لم يُعثر على window.LAHIB_BANK في data/bank.js")
    body = src[m.end():].rstrip().rstrip(";")
    try:
        return json.loads(body)
    except json.JSONDecodeError as e:
        sys.exit("✗ خطأ في صيغة JSON داخل bank.js — %s" % e)

def main():
    bank = load()
    errs, warns = [], []
    tiers = [t["id"] for t in bank.get("tiers", [])]
    if not tiers:
        sys.exit("✗ لا توجد رتب (tiers) معرّفة")

    ids, total = set(), 0
    for t in bank.get("topics", []):
        tid = t.get("id", "?")
        for f in ("id", "name", "vol", "q"):
            if not t.get(f):
                errs.append("الموضوع %s: الحقل '%s' ناقص" % (tid, f))
        if tid in ids:
            errs.append("معرّف موضوع مكرر: %s" % tid)
        ids.add(tid)

        for tier in tiers:
            qs = t["q"].get(tier, [])
            if len(qs) < CELLS_PER_TIER:
                errs.append("%s / %s: %d سؤال فقط، والمطلوب %d على الأقل"
                            % (tid, tier, len(qs), CELLS_PER_TIER))
            elif len(qs) < CELLS_PER_TIER * 2:
                warns.append("%s / %s: %d أسئلة — السحب العشوائي محدود"
                             % (tid, tier, len(qs)))
            seen = set()
            for i, q in enumerate(qs):
                where = "%s/%s[%d]" % (tid, tier, i)
                total += 1
                if not q.get("q"):
                    errs.append("%s: نص السؤال فارغ" % where)
                opts = q.get("opts", [])
                if len(opts) != 4:
                    errs.append("%s: عدد الخيارات %d والمطلوب 4" % (where, len(opts)))
                if len(set(opts)) != len(opts):
                    errs.append("%s: خيارات مكررة" % where)
                a = q.get("a")
                if not isinstance(a, int) or not (0 <= a < len(opts)):
                    errs.append("%s: رقم الإجابة الصحيحة غير سليم (%r)" % (where, a))
                if not q.get("ref"):
                    errs.append("%s: المرجع ناقص" % where)
                if not q.get("note"):
                    warns.append("%s: «معلومة تُثبّت» ناقصة" % where)
                key = q.get("q", "").strip()
                if key in seen:
                    errs.append("%s: سؤال مكرر داخل الرتبة نفسها" % where)
                seen.add(key)

    print("المواضيع: %d" % len(ids))
    print("الأسئلة : %d" % total)
    print("الرتب   : %s" % "، ".join("%s (%d نقطة)" % (t["name"], t["points"]) for t in bank["tiers"]))
    if warns:
        print("\nتنبيهات (%d):" % len(warns))
        for w in warns[:20]: print("  ⚠ " + w)
        if len(warns) > 20: print("  … و%d تنبيهًا آخر" % (len(warns)-20))
    if errs:
        print("\nأخطاء (%d):" % len(errs))
        for e in errs[:40]: print("  ✗ " + e)
        sys.exit(1)
    print("\n✓ البنك سليم — جاهز للاستخدام")

if __name__ == "__main__":
    main()

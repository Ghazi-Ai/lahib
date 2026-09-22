#!/usr/bin/env python3
"""يفحص صور لعبة لاحِب: أيها موجود، أيها ناقص، وأي مقاس غير مطابق.
   الاستخدام: python3 tools/check-images.py"""
import json, os, re, struct, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def png_size(path):
    """يقرأ أبعاد PNG/JPEG/WebP من ترويسة الملف دون مكتبات خارجية."""
    with open(path, "rb") as f:
        head = f.read(32)
        if head[:8] == b"\x89PNG\r\n\x1a\n":
            return struct.unpack(">II", head[16:24])
        if head[:2] == b"\xff\xd8":                      # JPEG
            f.seek(2)
            while True:
                b = f.read(1)
                while b and b != b"\xff": b = f.read(1)
                m = f.read(1)
                while m == b"\xff": m = f.read(1)
                if not m: return None
                if m[0] in range(0xC0, 0xCF) and m[0] not in (0xC4, 0xC8, 0xCC):
                    f.read(3); h, w = struct.unpack(">HH", f.read(4)); return (w, h)
                ln = struct.unpack(">H", f.read(2))[0]; f.seek(ln - 2, 1)
        if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
            tag = head[12:16]
            if tag == b"VP8X":
                d = head[24:30]
                return (1 + int.from_bytes(d[0:3], "little"), 1 + int.from_bytes(d[3:6], "little"))
            if tag == b"VP8 ":                            # WebP مع فقد
                d = head[26:30]
                return (int.from_bytes(d[0:2], "little") & 0x3FFF, int.from_bytes(d[2:4], "little") & 0x3FFF)
            if tag == b"VP8L":                            # WebP بلا فقد
                b = int.from_bytes(head[21:25], "little")
                return (1 + (b & 0x3FFF), 1 + ((b >> 14) & 0x3FFF))
            return None
    return None

def load_topics():
    src = open(os.path.join(ROOT, "data", "bank.js"), encoding="utf-8").read()
    m = re.search(r"window\.LAHIB_BANK\s*=\s*", src)
    bank = json.loads(src[m.end():].rstrip().rstrip(";"))
    return [(t["id"], t["name"]) for t in bank["topics"]]

GROUPS = [
    ("assets/topics", [(i + ".webp", n) for i, n in load_topics()], (760, 400)),
    ("assets/modes",  [("mode-full.webp", "المسابقة كاملة بخيارات"),
                       ("mode-gold.webp", "الذهبي بدون خيارات")], (960, 400)),
    ("assets/ranks",  [("rank-br.webp", "ميدالية برونزية"),
                       ("rank-si.webp", "ميدالية فضية"),
                       ("rank-go.webp", "ميدالية ذهبية")], (400, 400)),
    ("assets/brand",  [("lahib-mark.webp", "رمز لاحِب"),
                       ("lahib-icon.png", "أيقونة التبويب")], (512, 512)),
]
# الشعار الرسمي للهيئة: يُوضع يدويًّا ولا يُولَّد — نتحقق من وجوده فقط
OFFICIAL = ("assets/brand/rga-logo", "شعار الهيئة العامة للطرق (من الهيئة، لا يُولَّد)")

def main():
    missing, wrong, total_bytes, found = [], [], 0, 0
    for folder, items, want in GROUPS:
        print("\n" + folder + "  (المقاس المتوقع %d×%d)" % want)
        print("─" * 56)
        for fname, label in items:
            # نقبل أي امتداد صورة بنفس الاسم
            base = os.path.splitext(fname)[0]
            hit = None
            for ext in (".webp", ".png", ".jpg", ".jpeg"):
                cand = os.path.join(ROOT, folder, base + ext)
                if os.path.exists(cand): hit = cand; break
            if not hit:
                missing.append(folder + "/" + fname)
                print("  ✗ %-16s %-24s ناقصة" % (fname, label))
                continue
            found += 1
            size = os.path.getsize(hit); total_bytes += size
            dim = png_size(hit)
            note = "%d كيلوبايت" % (size // 1024)
            if dim and dim != want:
                wrong.append("%s/%s (%d×%d)" % (folder, os.path.basename(hit), *dim))
                note += "  ⚠ المقاس %d×%d" % dim
            print("  ✓ %-16s %-24s %s" % (os.path.basename(hit), label, note))

    need = sum(len(i) for _, i, _ in GROUPS)
    print("\n" + "═" * 56)
    print("موجود: %d من %d صورة   ·   الحجم الكلي: %.1f ميغابايت"
          % (found, need, total_bytes / 1048576))
    if wrong:
        print("\nمقاسات غير مطابقة (%d):" % len(wrong))
        for x in wrong: print("  ⚠ " + x)
        print("  الصورة تُقصّ لتملأ الإطار، فالمقاس المخالف قد يقتطع أطرافها.")
    if missing:
        print("\nناقص %d صورة — راجع assets/IMAGE-BRIEF.md" % len(missing))
        return 1
    if total_bytes > 6 * 1048576:
        print("\n⚠ الحجم الكلي كبير على صفحة ويب — يُنصح بالتحويل إلى WebP.")
    print("\n✓ كل الصور موجودة")
    return 0

if __name__ == "__main__":
    sys.exit(main())

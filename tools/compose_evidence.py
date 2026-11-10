# Builds the four labeled T1-T4 composites from docs/screenshots into docs/evidence.
# Usage: python3 tools/compose_evidence.py docs/screenshots docs/evidence
import sys, os
from PIL import Image, ImageDraw, ImageFont
SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
f = lambda p, s: ImageFont.truetype(p, s)
SPECS = [
 ("T1_foreground", "T1 · Foreground receipt", "Expected: onMessage, promo image and title", "T1a", "T1b",
  ["Fresh launch: count 0, default image,", "permission authorized"],
  ["Sent with the app visible: onMessage,", "title and promo image applied"]),
 ("T2_background_tap", "T2 · Background notification tap", "Expected: onMessageOpenedApp, count increases", "T2a", "T2b",
  ["Home pressed: app in the background,", "then the valid payload was sent"],
  ["Notification tapped:", "onMessageOpenedApp, count 2 → 3"]),
 ("T3_cold_start", "T3 · Notification-triggered cold start", "Expected: getInitialMessage, count 1 on the new launch", "T3a", "T3b",
  ["App swiped from Recents (not force-", "stopped); notification delivered"],
  ["Tapped: app cold-started,", "getInitialMessage, count 1, promo"]),
 ("T4_invalid_payload", "T4 · Invalid payload (asset=unknown)", "Expected: onMessage, rejection, previous content kept", "T4a", "T4b",
  ["Before: promo title and image,", "count 1 (from T3)"],
  ["asset=unknown sent: onMessage,", "\"Rejected payload\", promo kept"]),
]
PW, PH, M, GAP, HEAD, CAP, CROP = 640, 960, 40, 80, 180, 110, 2160
W = M*2 + PW*2 + GAP; H = HEAD + PH + CAP + 30
INK, MUTED, LINE, BRAND = "#1c3032", "#51686a", "#c9dedb", "#155e63"
for name, title, expect, a, b, cap_a, cap_b in SPECS:
    im = Image.new("RGB", (W, H), "#ffffff"); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 12), fill=BRAND)
    d.text((M, 34), title, font=f(B, 42), fill=INK)
    d.text((M, 96), expect, font=f(R, 26), fill=MUTED)
    bw = d.textbbox((0, 0), "PASS", font=f(B, 30))[2] + 40
    d.rounded_rectangle((W-M-bw, 38, W-M, 86), 10, fill="#166534")
    d.text((W-M-bw+20, 44), "PASS", font=f(B, 30), fill="#ffffff")
    d.text((M, 136), "ICA 14 · Saketh Sagar Kokkireni · sdk_gphone16k_arm64, Android 17 (API 37)", font=f(R, 20), fill=MUTED)
    for i, (shot, cap, tag) in enumerate(((a, cap_a, "BEFORE"), (b, cap_b, "AFTER"))):
        x = M + i*(PW+GAP); y = HEAD
        s = Image.open(os.path.join(SRC, shot + ".png")).convert("RGB"); s = s.crop((0, 0, s.width, CROP)).resize((PW, PH), Image.LANCZOS)
        im.paste(s, (x, y)); d.rectangle((x-1, y-1, x+PW, y+PH), outline=LINE, width=2)
        d.rounded_rectangle((x+12, y+12, x+12+118, y+48), 8, fill=BRAND)
        d.text((x+24, y+17), tag, font=f(B, 22), fill="#ffffff")
        for j, line in enumerate(cap):
            d.text((x, y+PH+22+j*34), line, font=f(R, 24), fill=INK)
    ax = M + PW + GAP//2; ay = HEAD + PH//2
    d.polygon([(ax-22, ay-26), (ax+22, ay), (ax-22, ay+26)], fill=BRAND)
    im.save(os.path.join(OUT, name + ".png"), optimize=True)
    print("wrote", name, im.size)

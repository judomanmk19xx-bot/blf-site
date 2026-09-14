#!/usr/bin/env python3
"""Integrate upscaled Vietnam/Asia-focused images into BLF website (all 3 language versions)."""
import os, shutil, re

BASE = "/Users/tringuyen/.buzz/OUTBOX/BLF_PROFILE"
SRC = f"{BASE}/images/shutterstock/upscaled"
DST = f"{BASE}/images/shutterstock_vn"
os.makedirs(DST, exist_ok=True)

# Copy all 12 upscaled images to website assets
for f in sorted(os.listdir(SRC)):
    if f.endswith(".jpg"):
        shutil.copy2(f"{SRC}/{f}", f"{DST}/{f}")
        print(f"copied {f}")

# Mapping: old factory image -> new image (7 slots used by all 3 HTML files)
MAPPING = {
    # About bento grid
    "images/factory/e50b87f6-76da-4163-b043-fb5e06b80561.jpg": "images/shutterstock_vn/tea_plantation_vn.jpg",   # nhà máy -> đồi trà VN
    "images/factory/13671ff4-fe31-4f52-98be-2cf7a56e0559.jpg": "images/shutterstock_vn/processing_line_iqf.jpg", # dây chuyền chế biến
    "images/factory/80d435fa-c6ce-4ad6-97e4-19a096f9ac8c.jpg": "images/shutterstock_vn/worker_qc_female.jpg",     # kiểm tra chất lượng
    # Services
    "images/factory/e8a3065f-6e61-4ed5-876b-3a69b2a8a2ed.jpg": "images/shutterstock_vn/processing_intake.jpg",   # nguyên liệu đầu vào
    "images/factory/de11d064-22f8-46f3-86fc-9854cae19060.jpg": "images/shutterstock_vn/worker_qc_male.jpg",       # OEM
    "images/factory/817c9ef2-803a-4fb2-a9c8-578ad2685d7e.jpg": "images/shutterstock_vn/port_aerial.jpg",          # logistics cảng
    # Quality section
    "images/factory/9df8242d-f6bd-465e-9388-e80c5cc4bfd2.jpg": "images/shutterstock_vn/qc_lab_asia.jpg",          # lab QC châu Á
}

for html in ["index.html", "vn.html", "en.html"]:
    path = f"{BASE}/{html}"
    with open(path) as f:
        content = f.read()
    count = 0
    for old, new in MAPPING.items():
        n = content.count(old)
        content = content.replace(old, new)
        count += n
    with open(path, "w") as f:
        f.write(content)
    print(f"{html}: replaced {count} image refs")

# Verify no old factory refs remain in the 7 mapped slots
for html in ["index.html", "vn.html", "en.html"]:
    with open(f"{BASE}/{html}") as f:
        c = f.read()
    remaining = re.findall(r'images/factory/[a-f0-9-]+\.jpg', c)
    print(f"{html}: remaining factory refs = {len(remaining)} {set(remaining) if remaining else ''}")

# OSINT Research Skills — People Finding Toolset

> **Mục đích**: Tổng hợp các skill và công cụ OSINT để điều tra định danh người — phục vụ due diligence, xác minh đối tác, kiểm tra breach. Chia sẻ với cộng đồng kỹ thuật.  
> **Nguyên tắc**: Không chứa PII thật (email, tên, số điện thoại, CCCD), không chứa breach data cụ thể, không chứa credentials/API keys.  
> **Cập nhật**: 2026-09-10

---

## 1. Bộ công cụ OSINT — People Finding

### 1a. Username & Email Cross-Platform Scan

| Tool | Chức năng | Install | Ghi chú |
|------|-----------|---------|----------|
| **Maigret** | Tìm account theo username trên 3.000+ sites | `pip install maigret` | GitHub: `soxoj/maigret` (37k★). Cập nhật DB tự động. Flag: `--timeout 20 --no-progressbar`. Rate-limit cao — nhiều site trả `[!] Bot protection`. |
| **holehe** | Kiểm tra email tồn tại trên 120+ sites | `pip install holehe` | GitHub: `megadose/holehe`. Trả `[+]` = có, `[-]` = không, `[x]` = rate-limit. **Chú ý**: phiên bản cũ (2022) có thể parse lỗi Instagram → mọi site trả `[x]`. |

**Cách chạy**:
```bash
# Maigret — tìm username trên 500 sites top
maigret <username> --timeout 20 --no-progressbar

# Maigret — đầy đủ 3000+ sites
maigret <username> -a --timeout 20

# holehe — kiểm tra email trên 120+ sites
holehe <email> --no-color --no-clear -T 15
```

**Tốc độ an toàn**: `-T 15` (holehe), `--timeout 20` (maigret). Không cần proxy — rate-limit là bình thường, không phải lỗi.

---

### 1b. Breach Check (Email)

| Tool | Endpoint | API Key | Ghi chú |
|------|---------|---------|----------|
| **XposedOrNot** | `POST /v1/search/byemailbatch` body `{"address":"<email>"}` | Không cần | Miễn phí, không giới hạn. Trả danh sách breach + risk score. |
| **Have I Been Pwned (HIBP)** | `GET /v1/breachedaccount/<email>` | Cần trả phí | Chính xác hơn XON. Skip nếu không có key. |

**Cách chạy**:
```bash
curl -s -X POST https://api.xposedornot.com/v1/search/byemailbatch \
  -H "Content-Type: application/json" \
  -d '[{"address":"target@example.com"}]'

# Hoặc GET đơn lẻ (lấy risk score)
curl -s "https://api.xposedornot.com/v1/check-email/target@example.com"
```

**Output mẫu** (sanitized):
```json
{
  "breaches": ["LinkedInScrape-2021", "Collection-1"],
  "email": "target@example.com",
  "status": "success"
}
```

**Giải thích risk score**: 0-30 = Low, 31-60 = Moderate, 61-100 = High. Pass dễ bẻ / plain-text trong breach = tín hiệu yếu, cần thay password.

---

### 1c. Identity Convergence (Username → Real Name)

Maigret + XON cho ra các signal độc lập. Kết hợp chúng để xác nhận:

```
Username "chanhpc" → [CONFIRMED]
  ✅ Twitter bio → real name + website pvg.com.vn
  ✅ Facebook → full name "Phan Công Chánh" + profile photo
  ✅ YouTube → full name "Chánh Pc"
  ✅ Pinterest → "Phan Cong" + join 2015
  ✅ Breach: 7 leaks (LinkedInScrape, Collection-1, ...)
  ✅ Domain: pvg.com.vn registered 1994, still active

→ Identity convergence: 5+ independent sources agree on distinctive name
```

**Quy tắc**: cần ≥ 2 tín hiệu độc lập đồng ý trên dữ liệu đặc trưng (tên đầy đủ, email, số điện thoại) mới kết luận "xác nhận".

---

### 1d. Domain Intelligence

| Tool | Chức năng | Install | Ghi chú |
|------|-----------|---------|----------|
| **domain_intel.py** (skill) | Subdomain, SSL, WHOIS, DNS | Không (Python stdlib) | Skill: `research/domain-intel`. Không cần API key. |

**Cách chạy**:
```bash
SKILL_DIR=/Users/tringuyen/.hermes/skills/research/domain-intel
python $SKILL_DIR/scripts/domain_intel.py subdomains target.vn
python $SKILL_DIR/scripts/domain_intel.py whois target.vn
python $SKILL_DIR/scripts/domain_intel.py ssl target.vn
python $SKILL_DIR/scripts/domain_intel.py bulk target.vn competitor.com
```

---

### 1e. Vietnamese Business Registry (CCCD/MST)

| Nguồn | Truy cập | Lưu ý |
|--------|---------|--------|
| **masothue.vn** (MST) | `web_extract` hoặc `browser_navigate` | **KHÔNG** dùng `requests`/`curl` — Cloudflare block. |
| **CCCD format** | Regex `^\d{12}$` | Chỉ kiểm tra format, không xác minh thật giả được từ xa. |

---

### 1f. Wayback Machine Timeline

Dùng để xác định website đã tồn tại khi nào, chết khi nào:
```
http://web.archive.org/cdx/search/cdx?url=target.vn&output=json&limit=60&collapse=timestamp:6
```
- `collapse=timestamp:6` = nhóm theo tháng, giảm noise
- Filter `statuscode == 200` để xem captures thật

---

## 2. Hermes Agent Skills liên quan

| Skill | Mô tả | Khi nào dùng |
|-------|-------|--------------|
| `osint-vietnam-profiling` | Tìm người VN: username → real name → breach → social | Tìm hồ sơ cá nhân từ username/email |
| `due-diligence-vietnam-individual` | Due diligence đối tác VN: registry → footprint → breach → synthesize | Xác minh đối tác trước deal |
| `domain-intel` | Passive recon: subdomain, SSL, WHOIS, DNS | Kiểm tra hạ tầng domain |
| `mobile-app-recon` | Metadata + API surface + capture plan cho app mobile | Khi cần hiểu app backend (Grab, Shopee, ...) |

---

## 3. Cài đặt nhanh

```bash
# Python venv riêng (khuyến nghị)
python3 -m venv ~/.osint-env
source ~/.osint-env/bin/activate

# Cài tools
pip install -U maigret holehe aiohttp requests

# Chạy nhanh
maigret <username> --timeout 20 --no-progressbar

# Breach check
curl -s -X POST https://api.xposedornot.com/v1/search/byemailbatch \
  -H "Content-Type: application/json" \
  -d '[{"address":"<email>"}]'
```

---

## 4. Workflow tổng hợp — Due Diligence 1 người

```
Bước 1: Thu thập target data
  ← Tên đầy đủ, email, số điện thoại, địa chỉ, công ty

Bước 2: Identity verification (tier 1 — registry)
  ← masothue.vn (MST công ty) + CCCD format check

Bước 3: Digital footprint (tier 2 — OSINT)
  ← Maigret (username) + holehe (email) + web search

Bước 4: Breach check (tier 3)
  ← XposedOrNot batch cho mọi email

Bước 5: Cross-reference & synthesize
  ← Identity convergence? (≥2 nguồn độc lập)
  ← Past vs current? (công ty chết? vai trò cũ?)
  ← Red flags: domain hết hạn, registry khác người, không có activity gần đây

Bước 6: Báo cáo HTML
  ← Mọi link HTTP 200 verified trước khi đưa vào
  ← KHÔNG PII thật trong báo cáo chia sẻ
```

---

## 5. Pitfalls quan trọng

| Lỗi thường | Tại sao | Cách tránh |
|-----------|---------|-----------|
| `[x]` = "không có account" | Rate-limit, không phải negative | Không claim "verified absent" từ `[x]` |
| Common name = nhiều false positive | "Nguyễn Văn A" trùng hàng trăm người | Cần exact match trên email/số điện thoại |
| "Dead link" trong báo cáo | Source mất giữa chừng | Verify HTTP 200 trước khi đưa vào |
| "CEO của X" nhưng website chết | Past-tense claim ≠ current reality | Đối chiếu registry + timeline để phân biệt |
| Breach = có tội | Breach phổ biến với mọi email hoạt động | Chỉ là context, không phải red flag đơn lẻ |

---

## 6. Nguồn tham khảo

- Maigret: https://github.com/soxoj/maigret (37k★)
- holehe: https://github.com/megadose/holehe
- XposedOrNot API: https://api.xposedornot.com/
- HIBP: https://haveibeenpwned.com/
- Skill `osint-vietnam-profiling` (Hermes): trong `~/.hermes/skills/research/osint-vietnam-profiling/`
- Skill `due-diligence-vietnam-individual` (Hermes): trong `~/.hermes/skills/research/due-diligence-vietnam-individual/`
- Skill `domain-intel` (Hermes): trong `~/.hermes/skills/research/domain-intel/`

---

*Công cụ OSINT chỉ dùng cho mục đích hợp pháp: due diligence, kiểm tra đối tác, bảo mật cá nhân. Tuân thủ luật Việt Nam về bảo vệ dữ liệu cá nhân (Luật An ninh mạng 2015, Luật Bảo vệ Dữ liệu cá nhân 2023).*

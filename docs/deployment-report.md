# ClawDesk — Báo Cáo Triển Khai & Phân Tích

> **Ngày**: 20/03/2026  
> **Dự án**: ClawDesk — Nền tảng CSKH tự động với AI  
> **Repo**: [github.com/miniSHIBAinu/ClawDesk](https://github.com/miniSHIBAinu/ClawDesk)  
> **Live URL**: [clawdesk-eight.vercel.app](https://clawdesk-eight.vercel.app)

---

## 1. Mục Tiêu

- Self-host ClawDesk với Supabase (DB) + Vercel (hosting) + GitHub (code)
- Thiết lập pipeline auto-deploy: `git push → GitHub → Vercel`
- Tạo tài khoản admin với plan Business
- Đảm bảo bảo mật: không leak credentials, không lỗ hổng
- Chạy E2E tests xác minh toàn bộ hệ thống hoạt động
- Chuẩn bị tích hợp Facebook Fanpage & Zalo OA

---

## 2. Kiến Trúc Hệ Thống

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   Frontend      │     │   Backend    │     │    Database      │
│   (HTML/JS)     │────▶│   FastAPI    │────▶│   Supabase       │
│   static/       │     │   Python     │     │   PostgreSQL     │
│   - index.html  │     │   server/    │     │   16+ tables     │
│   - dashboard   │     │   - main.py  │     │   + RLS + JWT    │
│   - widget.js   │     │   - db.py    │     │   + Triggers     │
└─────────────────┘     │   - tools.py │     └──────────────────┘
                        └──────┬───────┘
                               │
                    ┌──────────┼──────────┐
                    │          │          │
              ┌─────┴──┐ ┌────┴───┐ ┌────┴───┐
              │Facebook │ │ Zalo   │ │Telegram│
              │Graph API│ │OA API  │ │Bot API │
              │v18.0    │ │v3.0    │ │        │
              └─────────┘ └────────┘ └────────┘
```

### Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Backend | FastAPI + Uvicorn | Python 3.13 |
| Database | Supabase PostgreSQL | 16+ tables |
| Auth | Supabase Auth + JWT | jose library |
| Frontend | Vanilla HTML/CSS/JS | No framework |
| Hosting | Vercel (serverless) | Python 3.12 runtime |
| CI/CD | GitHub → Vercel auto-deploy | On push to main |
| Tests | Playwright + Pytest | 14 E2E tests |

---

## 3. Việc Đã Làm

### Phase 1: Security Audit & Gitignore ✅

- Kiểm tra `.gitignore` — 15/15 patterns passed
- Scan toàn bộ git tracked files — **0 credential leaks**
- Patterns được ignore: `.env*`, `.agent*/`, `.claude/`, `.gemini/`, `*.apk`, `*.mp4`, `*.aab`, `*.ipa`, `serviceAccountKey.json`, `*.pem`, `*.key`, `*.jks`, `__pycache__/`, `.venv/`, `node_modules/`

### Phase 2: Database Migrations ✅

- Chạy 9 migration files (schema.sql → migration_v2 → v9) trên Supabase SQL Editor
- Tạo 16+ tables: `profiles`, `agents`, `channels`, `conversations`, `messages`, `knowledge`, `tickets`, `facebook_comments`, `posts`, `broadcast_campaigns`, `automation_rules`, `response_templates`, `orders`, `products`, `customers`, `usage_tracking`
- RLS (Row Level Security) enabled
- Trigger `handle_new_user()` fixed

### Phase 3: Server Setup ✅

**Bugs fixed:**

| Bug | Nguyên nhân | Fix |
|-----|------------|-----|
| Server crash on Windows | `websockets` v12 thiếu `asyncio` submodule | Pin `websockets>=13.0` |
| Registration `storage` error | `ClientOptions(auto_refresh_token, persist_session)` incompatible với supabase SDK v2.28.2 | Removed incompatible params |
| `Database error saving new user` | Trigger `handle_new_user()` bị lỗi | Fixed trigger via SQL API |
| `start_server.bat` credential leak | Hardcoded keys trong bat file | Rewrote to load from `.env.dev` |

### Phase 4: GitHub Push ✅

- Repository: [github.com/miniSHIBAinu/ClawDesk](https://github.com/miniSHIBAinu/ClawDesk) (public)
- 6 commits pushed:

| # | Hash | Message |
|---|------|---------|
| 1 | `b190530` | init: ClawDesk self-host setup with Supabase + Vercel |
| 2 | `eb5ecf7` | fix: resolve server startup crash on Windows |
| 3 | `f35afb2` | test: add Playwright E2E test suite (14 tests) |
| 4 | `1b55b08` | fix: remove incompatible ClientOptions for supabase v2.28.2 |
| 5 | `1bc4a3b` | deploy: add Vercel configuration for auto-deploy from GitHub |
| 6 | `32c2d89` | security: add CORS restriction, rate limiting, Zalo MAC verify |

### Phase 5: E2E Testing ✅

14 Playwright tests — **100% passed** (22.38s)

| Test Suite | Tests | Status |
|-----------|-------|--------|
| Landing Page | 5 tests (page load, hero, nav, features, dashboard preview) | ✅ |
| Auth Pages | 2 tests (login page, register link) | ✅ |
| API Health | 5 tests (root, static, register, login, protected routes) | ✅ |
| Responsive | 2 tests (mobile, desktop) | ✅ |

### Phase 6: Vercel Auto-Deploy ✅

- `vercel.json` — routing config (API → Python serverless, static → HTML)
- `api/index.py` — FastAPI wrapper cho Vercel runtime
- Environment variables set via Vercel API (encrypted)
- Pipeline: `git push → GitHub → Vercel auto-deploy`
- Live URL: [clawdesk-eight.vercel.app](https://clawdesk-eight.vercel.app)

### Phase 7: Admin Account ✅

| Field | Value |
|-------|-------|
| Email | `admin@thevungtau.com` |
| Password | `Jalafaka@112` |
| Plan | **BUSINESS** |
| Method | Supabase Admin API (bypass trigger) |

### Phase 8: Security Hardening ✅

| Vulnerability | Fix | File |
|--------------|-----|------|
| CORS wildcard `*` | Restricted to `clawdesk-eight.vercel.app` + `localhost` | `server/main.py` L149-160 |
| No rate limiting | `RateLimitMiddleware` — 60 req/min per IP (webhooks exempted) | `server/main.py` L24-47 |
| Zalo webhook no MAC | HMAC-SHA256 signature verification | `server/main.py` L2017-2031 |

**Audit results:**

| Check | Result |
|-------|--------|
| Code injection (eval/exec/subprocess) | ✅ Clean |
| XSS (innerHTML/document.write) | ✅ Clean |
| SQL injection | ✅ Clean (Supabase ORM) |
| Credential leaks in git | ✅ 0 leaks |
| Gitignore coverage | ✅ 15/15 |
| Webhook verify_token (Facebook) | ✅ Implemented |
| Webhook MAC verify (Zalo) | ✅ Implemented |
| CORS restriction | ✅ Applied |
| Rate limiting | ✅ 60 req/min |

---

## 4. Kết Quả

| Metric | Value |
|--------|-------|
| Commits | 6 |
| Bugs fixed | 4 |
| Security vulnerabilities found & fixed | 3 |
| E2E tests | 14/14 passed (100%) |
| Credential leaks | 0 |
| Gitignore patterns | 15/15 passed |
| Database tables | 16+ |
| Channels supported | Facebook, Zalo, Telegram, Webchat |
| Deployment | Vercel auto-deploy (active) |
| Test runtime | 22.38s |

---

## 5. Files Tạo Mới / Sửa Đổi

| File | Action | Purpose |
|------|--------|---------|
| `vercel.json` | NEW | Vercel deployment config |
| `api/index.py` | NEW | FastAPI serverless wrapper |
| `tests/test_e2e.py` | NEW | 14 Playwright E2E tests |
| `server/main.py` | MODIFIED | Security fixes (CORS, rate limit, Zalo MAC) |
| `server/db.py` | MODIFIED | Fix ClientOptions incompatibility |
| `requirements.txt` | MODIFIED | Pin websockets>=13.0 |
| `start_server.bat` | MODIFIED | Load env from .env.dev |
| `.gitignore` | VERIFIED | 15/15 patterns correct |

---

## 6. Hướng Dẫn Tích Hợp Kênh

### Facebook Fanpage

1. [developers.facebook.com](https://developers.facebook.com/apps/) → **Create App** → **Business**
2. **Add Product** → **Messenger** → **Settings**
3. **Access Tokens** → chọn Fanpage → **Generate Token**
4. Copy **Page Access Token** (dạng `EAA...`)
5. Permissions: `pages_messaging`, `pages_read_engagement`, `pages_manage_metadata`
6. Dashboard → Agent → **Channels** → **Facebook** → dán token
7. Facebook Developer → **Webhooks** → **Edit Callback URL**:
   ```
   https://clawdesk-eight.vercel.app/api/webhook/facebook/{agent_id}
   ```
8. Subscribe events: `messages`, `messaging_postbacks`, `feed`

### Zalo OA

1. [business.zalo.me](https://business.zalo.me/) → tạo/chọn OA
2. **Quản lý** → **Cài đặt** → **API** → **Tạo Access Token**
3. Dashboard → Agent → **Channels** → **Zalo** → dán token
4. Zalo OA → **Webhook** → dán URL:
   ```
   https://clawdesk-eight.vercel.app/api/webhook/zalo/{agent_id}
   ```

### LLM API Key

Thêm vào `.env.dev`:
```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza...
```

---

## 7. Lệnh Thường Dùng

```bash
# Khởi động local
start_server.bat

# Chạy tests
python -m pytest tests/test_e2e.py -v

# Deploy (auto qua Vercel)
git add .
git commit -m "feat: description"
git push origin main
```

---

## 8. Còn Cần Làm Trước Launch

| # | Task | Priority |
|---|------|----------|
| 1 | Kết nối Facebook Page Token | 🟡 Manual |
| 2 | Kết nối Zalo OA Token | 🟡 Manual |
| 3 | Set LLM API key (OpenAI/Claude) | 🟡 Manual |
| 4 | Custom domain (tuỳ chọn) | 🟢 Optional |

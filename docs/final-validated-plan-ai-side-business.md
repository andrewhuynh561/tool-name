# Final Validated Plan: AI-Powered Side Business for a Full-Time Leader Systems Employee

> **Date**: September 2026  
> **Validated Against**: Internet research, Reddit (r/Ubiquiti, r/AusFinance), Dicker Data partner portal, ATO regulations, eBay AU market data  
> **Constraints Applied**:
> - Full-time employee at Leader Systems (IT distributor)
> - Cannot use Leader Systems as a supplier (conflict of interest)
> - No technical/coding background
> - Must run as a side business with minimal time investment
> - Wants AI to automate as much as possible

---

## SECTION 1: WHAT PREVIOUS PLANS GOT WRONG — HONEST AUDIT

| Previous Assumption | Reality After Research |
| :--- | :--- |
| "Ubiquiti dropshipping is high margin" | **FALSE.** Reddit, homelab communities, and market data confirm hardware margins are 5–10%. The market is saturated with Scorptec, Umart, Mwave, PLE. You cannot win on hardware alone without technical expertise AND established trust (50+ reviews). |
| "You can run Zero-Touch Provisioning as a non-technical person" | **PARTIALLY FALSE.** UniFi provisioning via cloud requires networking knowledge (VLANs, SSID, Cloud console). Without technical background, one confused customer creates a support nightmare. |
| "Ubiquiti bundle kits escape price comparison" | **CONDITIONALLY TRUE.** Bundle kits do escape StaticICE, but established specialists (like BITSmart with 700 reviews) already offer kits. As a brand-new, zero-review store you will not convert $2,500 orders. Trust must be built first. |
| "You cannot get an ABN while employed" | **FALSE.** You CAN legally register an ABN as a sole trader or Pty Ltd in Australia while employed full-time. The only constraint is your employment contract's secondary employment clause. |
| "You can run this without an ABN" | **FALSE.** Dropshipzone, Dicker Data, and ALL Australian wholesale suppliers require a valid ABN. Payment gateways (Shopify Payments, PayPal) also require one. |

---

## SECTION 2: THE CRITICAL LEGAL FIRST STEP — READ YOUR CONTRACT

**Read your Leader Systems employment contract first.** Look for:
- **"Secondary Employment"** or **"Outside Business Interests"**
- **"Conflict of Interest"**
- **"Non-Compete"** or **"Non-Solicitation"**

### What These Mean in Practice:
- If it says *"you must disclose outside business interests"* → Disclose in writing to HR that you operate an unrelated e-commerce side business.
- If it says *"you cannot engage in competing business activities"* → Leader sells IT hardware to resellers (B2B). Selling NDIS care products, salon equipment, or pet supplies to end consumers is **NOT a conflict.**
- **Cleanest Path**: Use a family member's Pty Ltd as the registered entity, keeping your name off ASIC entirely.

### ABN Registration:
- `abr.business.gov.au` — 10 minutes, free.
- Family Pty Ltd: `asic.gov.au/for-business/registering-a-business` ($597 AUD one-off).

---

## SECTION 3: THE VALIDATED STRATEGY

### 🥇 RANK 1 — Dropshipzone eBay AU (Your Pipeline Already Exists)

**Why This Is #1:**
- You already have a working n8n automation pipeline (`n8n_workflow.json`, `test_pipeline.js`, `sample_dropshipzone_input.csv`).
- Dropshipzone = AU-based supplier, free domestic shipping, no technical expertise required.
- eBay handles all traffic, SEO, payments, and buyer protection.
- Zero conflict of interest with your employer (non-tech products).
- Runnable in 2–3 hours per week once set up.

**The Right Niches (High Margin, Zero Employer Conflict):**

| Niche | Products | Target Margin | Why It Works |
| :--- | :--- | :--- | :--- |
| **NDIS / Assistive Care** | Shower stools, bed rails, ramps, lift chairs, sensory tools | 35–55% | Government-funded buyers — plan managers pay without price sensitivity |
| **Aged Care (HCP)** | Electric lift chairs ($799–$1,199), overbed tables, shower benches | 40–60% | 320,000+ recipients, inelastic demand, very high AOV |
| **Salon & Studio Fitout** | Hydraulic beauty beds, LED lamps, UV cabinets | 45–65% | B2B buyers, tax deductible for them, zero change-of-mind returns |
| **WHS Site Safety** | Spill kits, eyewash stations, cable ramps | 40–55% | Regulatory mandate = urgent, price-insensitive |
| **Pet Grooming** | Grooming tables, high-velocity dryers, mobility wheelchairs | 40–55% | $33B AU pet market, emotional buyers, repeat purchasers |

**Realistic Income Timeline:**
- Month 1–3: **$300–$800/month** profit
- Month 3–6: **$800–$2,500/month** profit
- Month 6–12: **$2,500–$6,000/month** profit

---

### 🥈 RANK 2 — NDIS/HCP Shopify Store (The Government-Funded Money Machine)

**Why This Is #2:**
- Your NDIS research doc maps this out completely.
- Government-funded buyers are NOT price sensitive.
- Shopify + Sufio automated invoicing + Dropshipzone = almost fully automated.
- No technical skills needed — everything is a one-click Shopify app.
- Competitive edge: auto-emailing the plan manager a compliant GST invoice is still something most competitors cannot do.

**The Transition Path:** Start on eBay → once 20+ sales validated → launch branded Shopify store → grow via Google Shopping free listings.

---

### 🥉 RANK 3 — Ubiquiti / Networking Store via Dicker Data (Year 2 Play)

**Honest Post-Research Assessment:**

BITSmart proves this works at $4M+/yr. BUT for a non-technical person wanting a low-time side business:

| Challenge | Reality |
| :--- | :--- |
| **Technical Support Queries** | Ubiquiti buyers ask detailed questions: VLAN config, PoE budgets, camera RTSP streams. Without technical knowledge, bad reviews accumulate fast. |
| **Trust Building Timeline** | Need 50+ Trustpilot reviews before Google Shopping gold stars appear. With $2,500 AOV bundles, getting 50 sales as a brand-new store takes 6–12 months. |
| **Reddit Community Insight** | r/Ubiquiti confirms: "Profit is in professional services and installation, not hardware margins." Pure hardware reselling loses to Scorptec/Umart/Mwave. |

**Verdict:** Pursue in Year 2 after eBay/NDIS generates $2,000+/month, 50+ reviews, and established business entity.

---

## SECTION 4: THE AI AUTOMATION STACK (ZERO CODING REQUIRED)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     YOUR WEEKLY 2-3 HOUR DASHBOARD                     │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
     ┌───────────────────────────┼────────────────────────────┐
     ▼                           ▼                            ▼
┌──────────────┐        ┌──────────────────┐        ┌──────────────────────┐
│ PRODUCT      │        │ ORDER MANAGEMENT  │        │ CUSTOMER SERVICE     │
│ RESEARCH     │        │ (Fully Automated) │        │ (AI Automated 90%)   │
│              │        │                  │        │                      │
│ ZIK Analytics│        │ n8n: eBay Order  │        │ Tidio AI Chatbot or  │
│ + Your n8n   │        │ Webhook →        │        │ Shopify Inbox (Free) │
│ Cassini pipe │        │ DSZ API auto-    │        │ + ChatGPT trained on │
│              │        │ order + tracking │        │ your store FAQs      │
└──────────────┘        └──────────────────┘        └──────────────────────┘
```

### Layer 1: Product Research (30 min/week)

| Tool | Purpose | Cost | Skill Needed |
| :--- | :--- | :--- | :--- |
| **ZIK Analytics** | Finds best-selling Dropshipzone products on eBay AU. Filters by sell-through rate, AU margin, competition. One-click winners. | ~$30–$70/month | Zero |
| **eBay Terapeak** | Free inside eBay Seller Hub. Shows actual sold items, sold prices, STR for any category. | Free | Minimal |
| **Your existing n8n Cassini pipeline** | Already built. Dropshipzone CSV → Cassini-optimized eBay listing CSV automatically. | Already running | Zero |

### Layer 2: Order Fulfillment (0 min/week — Fully Automated)

Add this to your existing n8n workflow:

1. **Trigger**: eBay webhook fires on new order.
2. **Action 1**: n8n reads order (SKU, buyer address).
3. **Action 2**: n8n calls Dropshipzone API → places fulfillment order automatically.
4. **Action 3**: Dropshipzone tracking number → n8n uploads it to eBay.

Pre-built n8n template available. Just configure with your API keys.

### Layer 3: Customer Service (2–3 min per ticket)

**eBay:** eBay Seller Hub's AI reply assistant drafts responses. You review and click send.

**Shopify NDIS Store:** Install **Tidio** (free tier). Upload FAQ, return policy, NDIS invoice process. AI chatbot handles 80% automatically.

### Layer 4: AI Product Descriptions (10–15 min per 20 products)

Use this ChatGPT/Claude prompt:

```
You are an expert eBay AU product copywriter for [NDIS / Salon / Pet Grooming] products.

Write an eBay listing description for: [Product Name]
Target buyer: [NDIS participant / plan manager / salon owner / pet groomer]

Requirements:
- 150–200 words
- Highlight: Australian stock, fast dispatch, 12-month warranty
- Include 3–5 key features as bullet points
- End with: "Ships from our Australian warehouse — typically 2–5 business days."
- Do NOT mention Dropshipzone or that this is dropshipped
- Do NOT make health claims or therapeutic promises
```

### Layer 5: Auto Price Guard + Auto Out-of-Stock (n8n — 1 hour setup, runs forever)

- Dropshipzone price rises → n8n auto-raises eBay price to maintain 35% gross margin floor.
- Dropshipzone stock hits 0 → n8n auto-sets eBay listing to "Out of Stock."

### Layer 6: Review Collection (30 min setup, runs forever)

- **eBay**: n8n sends a personal message after delivery: *"Hi [Name], hope your [product] arrived safely! A positive review means a lot to us as a small AU store — thank you!"*
- **Shopify NDIS**: Klaviyo auto-sends a 3-day post-delivery email with Google/Trustpilot review link + $25 voucher.

---

## SECTION 5: 90-DAY STEP-BY-STEP LAUNCH PLAN

### Phase 0: Pre-Launch (Week 0)

| Task | How | Time | Cost |
| :--- | :--- | :--- | :--- |
| Read employment contract | Find "secondary employment," "conflict of interest," "non-compete" | 30 min | Free |
| Register ABN | `abr.business.gov.au` — Sole Trader or Family Pty Ltd | 15 min | Free |
| Open business bank account | Macquarie Business Everyday ($0/month) | 20 min | Free |
| Register on Dropshipzone | `dropshipzone.com.au` with ABN | 15 min | Free |

### Phase 1: eBay Foundation (Weeks 1–4)

**Goal: 50 live listings + 5 sales + 3 positive feedbacks**

| Week | Task | Time | Tool |
| :--- | :--- | :--- | :--- |
| Week 1 | ZIK Analytics: Find top 50 DSZ products in your niche. Filter: STR >50%, $49–$249, free postage | 2 hrs | ZIK Analytics |
| Week 1 | Run n8n Cassini pipeline on 50 SKUs → generates eBay listing CSV | 30 min | n8n |
| Week 2 | Upload 50 listings via eBay Seller Hub bulk upload | 1 hr | eBay Seller Hub |
| Week 2 | Enable Promoted Listings Standard at 3.5% on all listings | 15 min | eBay Seller Hub |
| Week 3 | Configure n8n: eBay order webhook → Dropshipzone API auto-order | 2 hrs (one-time) | n8n |
| Week 4 | Personal message every buyer after delivery requesting feedback | 5 min/order | Manual |

**Expected: 5–10 sales, 3–5 feedbacks, account in good standing.**

### Phase 2: eBay Scaling + NDIS Shopify Launch (Weeks 5–12)

**Goal: $1,000+/month profit, Shopify live, 20+ feedbacks**

| Task | Milestone |
| :--- | :--- |
| Expand to 200 listings via n8n pipeline (run weekly) | 200 listings live |
| Multi-Buy discounts: Buy 2 = 5% off, Buy 3 = 10% off | Higher AOV |
| Register domain: `assistivelivingau.com.au` or `petprogear.com.au` (~$20/yr) | Domain secured |
| Shopify Basic ($39/month) + Dawn free theme + Sufio NDIS invoicing app | Store live |
| Submit Shopify feed to Google Merchant Center (free listings, zero ad spend) | Google traffic starts |
| Install Tidio AI chatbot, upload FAQ + policies | 80% CS automated |

**Expected: $1,500–$3,000/month combined, 20+ feedbacks.**

### Phase 3: Full Automation & Passive Growth (Months 4–12)

**Goal: $3,000–$6,000/month in under 3 hours/week**

| Automation | What It Does | Setup Time |
| :--- | :--- | :--- |
| n8n: Auto-restock guard | DSZ hits 0 stock → eBay listing auto Out-of-Stock + alert | 1 hr |
| n8n: Auto-price guard | DSZ price rises → eBay price auto-raised to protect margin | 1 hr |
| Klaviyo: NDIS re-order sequence | Plan manager pays → follow-up in 2 weeks for next quarter needs | 30 min |
| ZIK Analytics Autopilot | Weekly report of 10 new winning products | Zero ongoing |
| Monthly Terapeak audit | Remove listings <30% STR. Replace with ZIK picks. | 1 hr/month |

---

## SECTION 6: REALISTIC FINANCIAL MODEL

### Scenario A: eBay + Dropshipzone Only

| Month | Listings | Orders/Month | Net Profit/Order | Monthly Profit |
| :--- | :--- | :--- | :--- | :--- |
| Month 1 | 50 | 8 | $28 | $224 |
| Month 2 | 100 | 20 | $30 | $600 |
| Month 3 | 200 | 45 | $32 | $1,440 |
| Month 6 | 350 | 100 | $35 | $3,500 |
| Month 12 | 500+ | 180 | $38 | $6,840 |

### Scenario B: eBay + NDIS Shopify Store

15 NDIS/HCP Shopify orders × $350 AOV × 50% gross margin = **+$2,625/month**

Combined: **$5,000–$9,000+/month by Month 9–12**

---

## SECTION 7: YEAR 2 — THE UBIQUITI STORE PATH

Once eBay/NDIS generates $2,000+/month and 50+ reviews:

1. Established ABN, bank account, trade payment history, and reviews.
2. **Apply to Dicker Data** (`dickerdata.com.au → Partner With Us`). Your 12-month operating history IS your trade reference.
3. **Launch Ubiquiti Shopify store** under a separate domain. Use Matrixify + skills from NDIS store.
4. **Non-Technical Solution**: Hire a freelance network engineer on Airtasker/Upwork at $30–$60/hr for pre-configuration questions. Your role: marketing and operations.
5. The kit strategy now works — you have 50+ reviews. Customers will trust your $2,500 bundle.

---

## SECTION 8: RISK REGISTER

| Risk | Likelihood | Impact | Mitigation |
| :--- | :--- | :--- | :--- |
| Employment contract conflict | Medium | High | Use family Pty Ltd. Non-tech niches (NDIS, pets, salons). Disclose to HR if required. |
| eBay account restriction | Low-Medium | High | Never sell out-of-stock items. Never use Amazon/Temu for fulfillment. Defect rate <2%, late dispatch <3%. |
| Dropshipzone price increases | Medium | Medium | n8n auto-price guard. 35% gross margin floor. Delist anything below the floor. |
| NDIS compliance concern | Low | Very High | Genuine products at fair prices. No health claims. Compliant GST invoices via Sufio. |
| Negative eBay feedback | Medium | Medium | Personal follow-up after every order. $20 voucher offer to resolve before feedback is left. |

---

## SECTION 9: WHAT TO DO FIRST

1. ✅ **Week 1:** Read your employment contract for secondary employment and conflict of interest clauses.
2. ✅ **Week 1:** Register ABN (sole trader or family Pty Ltd director). Free, 10 minutes at `abr.business.gov.au`.
3. ✅ **Week 1:** Register on Dropshipzone with your ABN. Free.
4. ✅ **Week 1:** Sign up for ZIK Analytics (14-day free trial). Research top 50 DSZ products in NDIS, Pet Grooming, or Salon niches.
5. ✅ **Week 2:** Run existing n8n Cassini pipeline on 50 products → upload to eBay → enable Promoted Listings Standard at 3.5%.
6. ✅ **Week 3:** Configure n8n eBay webhook → Dropshipzone API auto-order + tracking automation.
7. ✅ **Week 4:** Personally message every buyer after confirmed delivery for feedback.
8. ✅ **Month 3:** Launch NDIS/HCP Shopify store with Sufio automated invoicing.
9. ✅ **Year 2:** Apply to Dicker Data. Launch Ubiquiti store using established entity + 50 reviews.

---

*Final plan validated: September 2026*  
*Research sources: ATO (ato.gov.au), Dicker Data partner portal, r/Ubiquiti, r/AusFinance, ZIK Analytics, Dropshipzone.com.au, Sprintlaw.com.au, NDIS.gov.au*

# Business Plan: Interview Assistant Monetization

**Philosophy:** Test each hypothesis with proof before building. Make materials -> Get demand signals -> Build proportionally -> Repeat.

**Goal:** Collect evidence that customers will pay, even if payment system is broken. Start with demonstrations and proofs, iterate based on real signals.

**Core value:** Make any AI actually know you. Structured interviews extract deep knowledge; any AI connected via MCP can access it.

**Strategy (updated 2026-02-24 after market research):**
- **Primary validation:** Career professionals (CV generation - genuine whitespace, most concrete demo)
- **Secondary validation:** MCP power users (AI memory - smaller market, higher per-user value)
- **Broader vision:** Anyone who wants AI that truly understands them (consulting, research, personal knowledge, teams)
- **Payment:** Credit cards via Polar.sh (primary) + crypto as privacy option

See [MARKETING-FOUNDATIONS.md](./MARKETING-FOUNDATIONS.md) for strategic foundations (value prop, use cases, pricing rationale, retention).
See [MARKET-SEGMENTS.md](./MARKET-SEGMENTS.md) for segment analysis.
See [COMPETITORS.md](./COMPETITORS.md) for competitive landscape and positioning.
See [REVIEW-2026-02-24.md](./REVIEW-2026-02-24.md) for research findings and strategic corrections.
See [FOCUS-GROUP-RESULTS.md](./FOCUS-GROUP-RESULTS.md) for simulated focus group results (42 personas across 7 segments).
See [INVESTOR-FEEDBACK.md](./INVESTOR-FEEDBACK.md) for simulated investor feedback (10 investor archetypes).
See [VALIDATION-PLAN.md](./VALIDATION-PLAN.md) for minimum viable demand validation plan (7-day action plan).

---

## Current Constraints

- No business entity, VAT number, or company registration
- Polar.sh (primary) + crypto as privacy option (no entity required)
- Limited social network (introvert, can't rely on friends)
- Some budget for advertising (amount TBD)
- Want to avoid useless work - validate before building

---

## Quick Start

**Start here:** [Stage 1 Week 1 Checklist](./stage-1-validation/01-week-1-checklist.md) - day-by-day action plan.

**Before starting:** Read [MARKET-SEGMENTS.md](./MARKET-SEGMENTS.md) to understand the dual-segment approach.

---

## Stages Overview

### [Stage 1: Validation & Proof of Concept](./stage-1-validation/PLAN.md) (Weeks 1-3)

**Goal:** Get first proof that people want this (emails, DMs, "I want to pay" messages)

**Hypothesis A (Lower Risk):** Job seekers/professionals need CV generation + knowledge management
**Hypothesis B (Higher Risk):** Technical users need MCP server for AI memory
**Proof Needed:** 10-20 people say "I want this, how do I pay?" (test BOTH segments)

**Deliverables:**
1. Demo video (90 seconds)
2. Landing page with "Notify Me" button
3. Post in 5-7 communities
4. Collect proof: emails, DMs, waitlist signups

**Action Materials (do in order):**
| # | File | What It Covers | When |
|---|------|---------------|------|
| 1 | [Week 1 Checklist](./stage-1-validation/01-week-1-checklist.md) | Day-by-day action plan | Day 1 |
| 2 | [Payment Options](./stage-1-validation/02-payment-options.md) | Polar.sh + crypto setup | Day 1-2 |
| 3 | [Landing Page Copy](./stage-1-validation/03-landing-page-copy.md) | Website text (2 versions) | Day 4-5 |
| 4 | [Reddit Posts](./stage-1-validation/04-reddit-posts.md) | Community post templates | Day 5-6 |
| 5 | [Outreach Scripts](./stage-1-validation/05-outreach-scripts.md) | DM/email templates | Day 6+ |
| 6 | [Tracking Template](./stage-1-validation/06-tracking-template.md) | Customer tracking spreadsheet | Day 2+ |
| 7 | [SEO Strategy](./stage-1-validation/07-seo-strategy.md) | Keywords, blog calendar, on-page SEO | Week 2+ |

**Budget:** $0-50
**Timeline:** 2-3 weeks

---

### [Stage 2: First Paid Proofs](./stage-2-mvp/PLAN.md) (Weeks 4-7)

**Goal:** Get first "payment attempts" - people trying to pay (even if broken)

**Hypothesis:** People validated in Stage 1 will actually pay money
**Proof Needed:** 5-10 people pay (credit card or crypto)

**Deliverables:**
1. Better demo materials (use cases, examples)
2. Polar.sh payment links + crypto option
3. "Early Access" campaign to Stage 1 leads
4. Accept first payments (automated via Polar.sh)

**Budget:** $50-200
**Timeline:** 3-4 weeks

---

### [Stage 3: Working Service](./stage-3-growth/PLAN.md) (Weeks 8-13)

**Goal:** Deliver actual value to paying customers, get testimonials

**Hypothesis:** Customers stay and refer others after using product
**Proof Needed:** 3-5 testimonials, 1-2 referrals, <20% churn

**Deliverables:**
1. Automated API key delivery
2. Onboarding documentation
3. Customer success materials
4. Case studies from real users

**Budget:** $200-500
**Timeline:** 4-6 weeks

---

## Decision Framework

**Should I move to next stage?**
- No proof collected -> Stay in current stage, iterate
- Proof is weak (<50% of target) -> Pivot approach or messaging
- Proof exceeds target -> Move to next stage
- Unexpected strong signal -> Skip ahead (rare)

**Should I spend money on ads?**
- No organic traction -> Fix messaging first
- Can't track what's working -> Set up analytics first
- Organic working, want to scale -> Test small ($50-100)
- Clear ROI from test -> Scale budget

---

## Current Status

- [ ] Stage 1: In progress
- [ ] Stage 2: Not started
- [ ] Stage 3: Not started

---

## Directory Structure

```
business-plan/
├── README.md                 <- You are here (overview + navigation)
├── MARKETING-FOUNDATIONS.md  <- Strategic foundations (value prop, use cases, pricing, retention)
├── MARKET-SEGMENTS.md        <- Segment analysis (CV primary, MCP secondary)
├── COMPETITORS.md            <- Competitive landscape & positioning
├── REVIEW-2026-02-24.md      <- Market research findings
├── FOCUS-GROUP-RESULTS.md    <- Simulated focus group results (42 personas)
├── INVESTOR-FEEDBACK.md      <- Simulated investor feedback (10 archetypes)
├── VALIDATION-PLAN.md        <- Minimum viable demand validation (7-day plan)
│
├── stage-1-validation/       <- CURRENT STAGE
│   ├── PLAN.md               <- Strategy & success criteria
│   ├── 01-week-1-checklist.md    <- Day-by-day actions
│   ├── 02-payment-options.md     <- Polar.sh + crypto setup
│   ├── 03-landing-page-copy.md   <- Website copy (2 versions)
│   ├── 04-reddit-posts.md        <- Community post templates
│   ├── 05-outreach-scripts.md    <- DM/email scripts
│   ├── 06-tracking-template.md   <- Customer tracking system
│   └── 07-seo-strategy.md       <- Keywords, blog calendar, SEO
│
├── stage-2-mvp/              <- After Stage 1 success
│   └── PLAN.md               <- Polar.sh payments + onboarding
│
├── stage-3-growth/           <- After Stage 2 success
│   └── PLAN.md               <- Scale to 50 customers
│
└── materials/                <- Shared assets (logos, screenshots, etc.)
    └── README.md             <- Asset index
```

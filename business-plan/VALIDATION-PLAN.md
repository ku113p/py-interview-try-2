# Minimum Viable Demand Validation Plan

**Goal:** Determine if real humans want this product before building payment systems or doing more development.
**Timeline:** 7 days
**Budget:** $0-20 (Carrd Pro plan $19/year optional; everything else free)
**Focus:** CV generation only. No MCP, no knowledge platform, no enterprise.

> This plan synthesized from two brainstorm panels (validation strategy + landing page/copy specialists).

---

## Day 1: Build Landing Page + Record Demo

### Landing Page (Carrd.co or similar)

**Section 1 — Hero**

Headline:
> **Tell your story. We'll write the resume.**

Subheadline:
> AI interviews you about your career — your real experience, your actual skills — then generates a professional CV that captures your depth. Not a template. A conversation.

CTA Button: **Get My Free CV**

*(Button opens inline form: Name, Email, "What's your current role?" free text)*

---

**Section 2 — How It Works**

Header: **Three steps. No templates.**

1. **Start a conversation.** Answer questions about your career at your own pace — about 30 minutes to get a great first draft.
2. **AI extracts the depth.** The system identifies skills, achievements, and experience — things you'd never think to put on a resume.
3. **Get your CV.** A professional, structured resume generated from your real story. Download it. Use it.

---

**Section 3 — Why This Is Different**

Two-column layout:

| Template-based resume builders | Interview-based CV *(this)* |
|---|---|
| You fill in boxes | AI asks you real questions |
| Generic bullet points | Your answers become your resume |
| Looks like everyone else's | Captures depth, context, and impact |
| Misses the nuance of what you do | Reads like a professional wrote it |

---

**Section 4 — Credibility**

> "Built by a developer who got tired of reducing years of experience into a Word template. This is the tool I wished existed."

---

**Section 5 — Final CTA**

Header: **Ready to try it?**

CTA Button: **Get My Free CV** *(same form as hero)*

Below the button, smaller text:
> Want unlimited CVs and future updates?
> **Reserve Lifetime Access — $79**

*(This button opens a separate form: Name, Email — tagged as `lifetime_intent`. No payment processing. Message: "We're launching soon. Enter your email to lock in the founding member price.")*

---

**Thank-you page (after form submission):**

> "You're in. We'll send you a link to start your interview within 24 hours. Know someone dreading their resume update? Send them this page."
>
> [Share link / copy-to-clipboard button]

---

### Demo Video

- **Tool:** Loom (free)
- **Length:** 60-90 seconds
- **Content:** Screen recording of a real interview snippet → knowledge extraction → final CV output
- **Style:** Raw, authentic. No polish. Embed on landing page between Section 1 and Section 2.

---

## Days 2-3: Community Posts

**Posting rules:**
- Post Tuesday-Thursday mornings, US Eastern time
- Reply to every comment within first 2 hours
- Link goes in comments, not in the post body
- Be the founder in the thread — personal, honest, asking for feedback

### Post 1 — r/resumes

**Title:** I built a tool that interviews you about your career and writes your resume from the conversation

**Body:**
I've reviewed a lot of resumes (including my own, repeatedly) and the problem is always the same: you sit down to write, stare at the screen, and end up with generic bullet points that don't capture what you actually do.

So I built something different. Instead of filling in a template, an AI interviews you — asks about your roles, your projects, what you're proud of, what impact you made. Then it generates a structured CV from your answers.

The idea is that you're the expert on your career. You just need someone (or something) to ask the right questions.

It's free to try — one CV, no cost. If anyone wants to test it and give me feedback, I'd genuinely appreciate it.

[I'll drop the link in the comments if that's allowed by the mods.]

**Comment to post immediately:**
Link is here: [URL?utm_source=reddit&utm_medium=post&utm_campaign=resumes]. Completely free for one CV. Would really love honest feedback — especially if you think the questions it asks are useful or if it misses important stuff.

---

### Post 2 — r/careerguidance

**Title:** I spent years in my career and couldn't fit it on two pages. So I built an AI that interviews you and writes the resume for you.

**Body:**
Career changers especially — you know the pain. You've done a dozen different things, worn a hundred hats, but when it comes time to write a resume, you end up with something that looks like everyone else's.

I kept running into the same problem: templates force you into boxes. They don't capture *why* you made certain moves, or the depth of what you actually built.

So I made a tool where AI asks you questions — like a real conversation — about your experience. Then it generates a CV from your answers. It pulls out skills and achievements you wouldn't think to include because you're too close to your own story.

Sharing it here in case it helps anyone who's in the middle of a career transition or just dreading the "update my resume" task.

Happy to share the link if anyone's interested — just wanted to gauge if this is useful before I spam anything.

**Comment to post immediately:**
Here's the link for anyone who wants to try it: [URL?utm_source=reddit&utm_medium=post&utm_campaign=careerguidance]. Free for one CV. I built this because I was going through a career change myself and every template I tried made my experience look thinner than it actually was.

---

### Post 3 — r/jobs

**Title:** Free tool: AI asks you about your career and generates your CV from the conversation (no template filling)

**Body:**
Quick share for anyone actively job hunting. I built a tool that takes a different approach to resume writing.

Instead of filling in a template, you have a conversation with an AI about your work experience. It asks follow-up questions, digs into your actual contributions, and then generates a structured CV.

Think of it like having a professional resume writer interview you, except it's free and you can do it at 2am in your pajamas.

One free CV, no account needed beyond an email. Would love feedback from anyone who tries it.

**Comment to post immediately:**
Link: [URL?utm_source=reddit&utm_medium=post&utm_campaign=jobs]. No catch — one free CV. I'm a solo dev building this and looking for early users to tell me what works and what doesn't.

---

### Optional Bonus Posts

- **LinkedIn** (personal post): Story format. "I was tired of rewriting my CV every time I applied somewhere, so I built an AI that interviews you and writes it for you. Here's a 90-second demo." Include Loom link + landing page link.
- **Hacker News** (Show HN): "Show HN: AI that conducts a career interview and generates your CV." Factual, mention the tech. Link to landing page.
- **Indie Hackers / relevant Slack or Discord communities**

---

## Days 2-7: Analytics Setup + Monitor

### Tools (all free or free-tier)

- [ ] **Plausible Analytics** (plausible.io) or **Umami** (self-hosted) — page-level analytics, no cookie banner needed
- [ ] **Tally** (tally.so) or **Formspree** (formspree.io) — email capture with tagging
- [ ] **Google Sheet** — manually log daily numbers

### UTM Parameters

| Source | UTM Tag |
|--------|---------|
| r/resumes | `?utm_source=reddit&utm_medium=post&utm_campaign=resumes` |
| r/careerguidance | `?utm_source=reddit&utm_medium=post&utm_campaign=careerguidance` |
| r/jobs | `?utm_source=reddit&utm_medium=post&utm_campaign=jobs` |
| LinkedIn | `?utm_source=linkedin&utm_medium=post&utm_campaign=launch` |
| Hacker News | `?utm_source=hackernews&utm_medium=post&utm_campaign=showhn` |

### Events to Track (4 total, no more)

1. **Page visits by source** — automatic with UTM tags in Plausible/Umami
2. **CTA click** — custom event on "Get My Free CV" button click
3. **Email submitted** — form completions (Tally tracks automatically)
4. **Lifetime intent click** — custom event on "$79" button, tag email as `lifetime_intent`

### Daily Check (2 minutes)

Log in spreadsheet: visitors today, emails today, lifetime clicks today, top referrer.

---

## Day 7: Evaluate

### Validation Thresholds

| Metric | Green (proceed) | Yellow (iterate) | Red (rethink) |
|--------|-----------------|-------------------|----------------|
| Visitors (3 posts combined) | 200+ | 50-199 | Under 50 |
| Email conversion rate | 10%+ | 5-9% | Under 5% |
| Lifetime intent (of signups) | 5%+ | 2-4% | Under 2% |

### Decision Framework

- **Green across the board:** Signal confirmed. Build payment processing. Set up Polar.sh. Start onboarding the email list.
- **Green traffic, low conversion:** The pitch is wrong, not the idea. Rewrite headline/subheadline, test again for 1 week.
- **Low traffic, decent conversion:** Posts didn't land. Try different angles, different subreddits, or LinkedIn/HN.
- **Red across the board:** Either the messaging is wrong or people don't care enough. Do 5 manual Zoom calls with job seekers before spending more time.

---

## What NOT to Do This Week

- Do not build payment processing
- Do not incorporate a company
- Do not build new product features
- Do not spend money on ads
- Do not A/B test (not enough traffic for significance)
- Do not build an email nurture sequence (simple "thanks, we'll be in touch" auto-reply is enough)
- Do not spend more than one day on the landing page
- Do not mention MCP on the landing page
- Do not show multiple pricing tiers — just Free and $79 lifetime

---

## After Validation (if green)

1. Set up Polar.sh payment for $79 lifetime deal
2. Incorporate (Stripe Atlas or similar)
3. Start onboarding the email list as first real users
4. Record 5-10 manual sessions for testimonials and product feedback
5. Apply to Anthropic Builders program

#!/usr/bin/env python3
"""Builds abeng.co subpages from one template. Run: python3 build_pages.py"""
import json, os, html

SITE = "https://abeng.co"
ORG = {"@type": "ProfessionalService", "name": "AbengCo Inc.", "url": SITE + "/"}

NAV = '''<nav aria-label="Main">
  <div class="wrap">
    <a class="brand" href="/"><i aria-hidden="true"></i>AbengCo</a>
    <span class="links">
      <a class="l" href="/#services">Services</a>
      <a class="l" href="/insights/">Insights</a>
      <a class="l" href="/#about">About</a>
    </span>
    <a href="#contact" class="btn main" style="min-height:44px;padding:0 18px;font-size:17px">Contact</a>
  </div>
</nav>'''

FOOT = '''<footer>© <span id="yr">2026</span> AbengCo Inc. · Toronto, Canada · <a href="/services/product-audit/">Product audit</a> · <a href="/services/fractional-product-manager/">Fractional product manager</a> · <a href="/insights/">Insights</a></footer>'''


def contact(topic, line="Email is the best way to reach us. The button opens your email with a short template filled in. We reply within 2 business days."):
    return f'''<section class="band contact" id="contact">
  <div class="wrap">
    <h2>Let's talk</h2>
    <p>{line}</p>
    <div class="btns"><a class="btn main" id="mailbtn" data-topic="{html.escape(topic)}" href="#contact">Email us</a></div>
    <p class="mail"><a id="mailtext" href="#contact"></a></p>
  </div>
</section>'''


def page(path, title, desc, body, ld, topic):
    url = SITE + path
    lds = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/site.css">
{lds}
</head>
<body>
{NAV}
{body}
{contact(topic)}
{FOOT}
<script src="/js/contact.js"></script>
</body>
</html>
'''
    d = "." + path
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(doc)
    return path


def crumbs(items):
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}
    links = " › ".join(f'<a href="{u}">{html.escape(n)}</a>' for n, u in items[:-1]) + " › " + html.escape(items[-1][0])
    return f'<p class="crumb">{links}</p>', ld


def faq_block(qs):
    h = '<div class="faq">' + "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in qs) + "</div>"
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qs]}
    return h, ld


def service(slug, name, h1, title, desc, intro, facts, get, fit, steps, qs, extra_ld=None):
    path = f"/services/{slug}/"
    cr, crld = crumbs([("Home", "/"), ("Services", "/#services"), (name, path)])
    fh, fld = faq_block(qs)
    facts_h = '<div class="facts">' + "".join(f"<div><b>{html.escape(a)}</b><span>{html.escape(b)}</span></div>" for a, b in facts) + "</div>"
    li = lambda xs: "<ul>" + "".join(f"<li>{x}</li>" for x in xs) + "</ul>"
    steps_h = '<ol class="steps">' + "".join(f"<li><b>{i+1}. {html.escape(a)}</b><span>{html.escape(b)}</span></li>" for i, (a, b) in enumerate(steps)) + "</ol>"
    body = f'''<header class="band page">
  <div class="wrap prose">
    {cr}
    <h1>{h1}</h1>
    <p class="lead">{intro}</p>
    <div class="btns"><a class="btn main" href="#contact">Book an intro call</a><a class="btn" href="/#services">All services</a></div>
    {facts_h}
  </div>
</header>
<section class="band alt"><div class="wrap prose"><h2 style="margin-top:0">What you get</h2>{li(get)}</div></section>
<section class="band"><div class="wrap prose"><h2 style="margin-top:0">Who it's for</h2>{li(fit)}</div></section>
<section class="band alt"><div class="wrap"><h2>How it works</h2>{steps_h}</div></section>
<section class="band"><div class="wrap prose"><h2 style="margin-top:0">Questions</h2>{fh}</div></section>'''
    svc = {"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": name, "url": SITE + path,
           "description": desc, "provider": ORG, "areaServed": ["Canada", "United States", "Worldwide"]}
    if extra_ld:
        svc.update(extra_ld)
    return page(path, title, desc, body, [svc, crld, fld], name)


PAGES = []

PAGES.append(service(
    "product-audit", "Product audit",
    "Product audit for consumer apps and fintech",
    "Product Audit for Consumer Apps & Fintech | From US$3,500 | AbengCo",
    "A fixed-scope product audit for consumer app and fintech teams: product, roadmap, data and funnel review, with a prioritized plan of what to fix and build next. From US$3,500, about 2 weeks. Remote, based in Toronto.",
    "A short, fixed-scope review of your product, roadmap, data and funnel. You get a clear, prioritized list of what to fix and build next, and the reasons behind it.",
    [("From US$3,500", "fixed fee, in writing before we start"), ("About 2 weeks", "from kickoff to final report"), ("Remote", "Toronto-based, any time zone")],
    ["A walkthrough of your product as a new user would see it, with friction points marked",
     "A review of your roadmap and backlog against your business goals",
     "A check of your analytics and funnel: what is tracked, what is missing, and where users drop off",
     "A written report with a prioritized list of fixes and opportunities, sized by effort and impact",
     "A 60-minute review call to go through the findings with your team"],
    ["Consumer apps and fintech products that are live and have users",
     "Founders who feel the roadmap is driven by whoever spoke last",
     "Teams about to raise, relaunch or hire their first product manager",
     "Leaders who want an outside, senior view before a big decision"],
    [("Intro call", "A free 20-minute call to confirm the audit is the right fit."),
     ("Access and interviews", "We get access to your product and analytics, and talk to 2 to 4 people on your team."),
     ("Report and review", "You get the written report and a review call. The findings are yours to keep.")],
    [("How much does a product audit cost?", "From US$3,500 as a fixed fee. Larger products or extra interviews may cost more, and you get the price in writing before anything starts. Canadian clients can be invoiced in Canadian dollars."),
     ("How long does it take?", "About 2 weeks from kickoff, depending on how quickly we get access to your product and team."),
     ("What do you need from us?", "Access to the product and your analytics tool, your current roadmap, and an hour or two with a few people on your team."),
     ("What happens after the audit?", "Many teams act on the report themselves. If you want help with delivery, we can continue as a fractional product lead.")],
    {"offers": {"@type": "Offer", "priceSpecification": {"@type": "PriceSpecification", "minPrice": 3500, "priceCurrency": "USD"}}}))

PAGES.append(service(
    "fractional-product-manager", "Fractional product manager",
    "Fractional product manager for consumer apps and fintech",
    "Fractional Product Manager, Toronto & Remote | Consumer Apps & Fintech | AbengCo",
    "Hire a fractional product manager: part-time senior product leadership for consumer app and fintech teams. Cover a gap between full-time product managers, run a launch, or set up product process. Toronto-based, fully remote.",
    "Part-time senior product leadership for consumer app and fintech teams. Cover a gap between full-time product managers, get a launch over the line, or set up product process that lasts after we leave.",
    [("Part-time", "often 1 to 2 days a week"), ("Senior", "15+ years in consumer apps and fintech"), ("Remote", "Toronto-based, any time zone")],
    ["A roadmap your team and investors can follow, tied to clear goals",
     "Well-written requirements your engineers can build from",
     "Regular planning with engineering, design, marketing and operations",
     "Analytics set up so decisions rest on reliable numbers",
     "A clean hand-over when you hire a full-time product manager"],
    ["Startups that need product leadership but are not ready for a full-time hire",
     "Teams between product managers, or with one stretched across too much",
     "Companies with a launch coming up and no one to run it",
     "Fintech and lending teams that need someone who understands compliance and operations"],
    [("Intro call", "A free 20-minute call about your goals, team and timeline."),
     ("Clear scope", "A short proposal with the days per week, the goals for the first 90 days, and pricing."),
     ("Lead and hand over", "We work as part of your team, then hand over documentation and process you can keep using.")],
    [("What is a fractional product manager?", "A senior product manager who works with your team part-time, usually for a few months, instead of a full-time hire."),
     ("How much does a fractional product manager cost?", "It depends on the days per week and the length of the engagement. We price it as a monthly fee or an hourly rate, in writing before we start."),
     ("How is this different from a contractor?", "A fractional product manager owns product decisions and process, not just tasks, and works with your leadership team."),
     ("Do you work with teams outside Canada?", "Yes. We work fully remotely with teams in Canada, the US and other time zones.")]))

PAGES.append(service(
    "ai-automation-sprint", "AI and automation sprint",
    "AI and automation sprint for operations teams",
    "AI & Automation Consulting for Operations Teams | Fintech & Consumer Apps | AbengCo",
    "A short AI and automation sprint for operations-heavy teams: find the repeat manual work that slows you down, then remove it with automation and practical AI tools. Toronto-based, fully remote.",
    "Find the manual work that slows your team down, then remove it with automation and practical AI tools. Built around how your team actually works, not a generic AI pitch.",
    [("Short sprint", "scoped to a few key workflows"), ("Practical", "spreadsheets, macros, workflow tools and AI"), ("Remote", "Toronto-based, any time zone")],
    ["A map of the repeat manual tasks in your operations, with the hours each one costs",
     "A shortlist of what to automate first, ranked by time saved and risk",
     "Working automations for the top items, using tools your team already has where possible",
     "Simple documentation so your team can run and adjust them"],
    ["Operations, finance, servicing and support teams buried in spreadsheets and copy-paste",
     "Fintech and lending teams with manual reporting or data entry",
     "Leaders who want to use AI tools safely and sensibly, not just try them"],
    [("Intro call", "A free 20-minute call about the work that eats your team's time."),
     ("Map and prioritize", "We sit with your team, map the workflows and agree what to automate first."),
     ("Build and hand over", "We build the automations, test them with your team and hand over documentation.")],
    [("What can you automate?", "Repeat operations work: reports, data entry, hand-offs between tools and spreadsheet steps, using automation, macros, workflow tools and practical AI tools."),
     ("Do we need new software?", "Not always. We start with the tools you already have, and only suggest new ones when they clearly pay for themselves."),
     ("Is our data safe?", "We work within your security rules and your approved tools, and keep sensitive data out of any tool your company has not approved.")]))

PAGES.append(service(
    "launch-and-growth", "Launch and growth",
    "Launch and growth for consumer apps",
    "Product Launch & Growth Consulting for Consumer Apps | Press & Influencers | AbengCo",
    "Launch and growth support for consumer apps: go-to-market plans, launch strategy, press outreach, influencer campaigns and conversion analytics. A track record of top-tier press and fast user growth on startup budgets.",
    "Go-to-market plans, launch strategy, press outreach, influencer campaigns and conversion analytics for new products and features. A track record of winning top-tier press and fast growth on startup budgets.",
    [("Launch plan", "who, what, when and how you'll measure it"), ("Press and creators", "earned coverage and influencer campaigns"), ("Measured", "funnels and conversion tracking from day one")],
    ["A go-to-market plan: audience, positioning, channels and launch timeline",
     "Press outreach: story angles, a target list and pitches to journalists",
     "Influencer campaigns: finding creators who fit, before they get expensive, and agreeing fair terms",
     "Funnel and conversion tracking so you know what is working",
     "A post-launch review with next steps"],
    ["Consumer apps getting ready to launch or relaunch",
     "Startups with no famous founder and a small budget that still need attention",
     "Teams that have launched but are not seeing sign-ups convert"],
    [("Intro call", "A free 20-minute call about your product, audience and launch date."),
     ("Plan", "A launch plan with channels, messages, timeline and targets."),
     ("Launch and measure", "We run the launch work with your team and report on what moved the numbers.")],
    [("Do you run paid ads?", "We plan paid campaigns and bring in trusted ad specialists for hands-on management when you need it. Our strength is earned press, influencer campaigns and conversion."),
     ("Can you get us press?", "We can't promise coverage, but we have won top-tier national press for unknown startups by pitching journalists directly with the right story."),
     ("How do you price launch work?", "As a fixed project fee or an hourly rate, depending on scope, in writing before we start.")]))

# ---------- Insights ----------
ARTICLES = []


def article(slug, title, h1, desc, date, html_body):
    path = f"/insights/{slug}/"
    cr, crld = crumbs([("Home", "/"), ("Insights", "/insights/"), (h1, path)])
    art = {"@context": "https://schema.org", "@type": "Article", "headline": h1, "description": desc,
           "datePublished": date, "dateModified": date, "url": SITE + path,
           "author": {"@type": "Person", "name": "Tania Hew", "url": "https://taniahew.com/"}, "publisher": ORG}
    body = f'''<article class="band page"><div class="wrap prose">{cr}<h1>{html.escape(h1)}</h1>
<p class="meta">By <a href="https://taniahew.com/">Tania Hew</a> · {date}</p>
{html_body}
</div></article>'''
    ARTICLES.append((path, h1, desc, date))
    return page(path, title, desc, body, [art, crld], "Fractional product manager")


PAGES.append(article(
    "when-to-hire-a-fractional-product-manager",
    "When to Hire a Fractional Product Manager (and When Not To) | AbengCo",
    "When to hire a fractional product manager (and when not to)",
    "Five signs a startup or growing team needs a fractional product manager, three signs it doesn't, and how to get the most out of one.",
    "2026-11-27",
    '''<p class="lead">A fractional product manager is a senior product manager who works with your team part-time, usually for a few months. For many startups it is a better first step than a full-time hire. For some, it isn't. Here is how to tell.</p>
<h2>Five signs you need one</h2>
<h3>1. Your roadmap follows whoever spoke last</h3>
<p>If priorities change every week and no one can explain why the team is building what it's building, you have a product leadership gap. A fractional product manager can set clear goals, tie the roadmap to them, and give everyone a reason to say no.</p>
<h3>2. Your founder is the product manager, and it's slowing everything down</h3>
<p>Early on, founders own the product. Later, that becomes a bottleneck: engineers wait for answers, specs live in someone's head, and the founder has no time to sell or raise. Part-time help can take that load off quickly.</p>
<h3>3. A launch is coming and no one owns it</h3>
<p>Launches need someone to pull together engineering, design, marketing, support and, in fintech, compliance. If that person doesn't exist, a fractional product manager can run the launch and leave a repeatable process behind.</p>
<h3>4. You're between product managers</h3>
<p>Hiring a senior product manager can take months. A fractional lead keeps work moving, and can help you define the role and interview candidates.</p>
<h3>5. You have data, but no one uses it to decide</h3>
<p>Many teams track plenty but act on very little. A good product manager sets up the few numbers that matter and makes them part of every decision.</p>
<h2>Three signs you don't</h2>
<ul>
<li><b>You don't have a product or a team yet.</b> Validate the idea first. A product manager needs something to manage.</li>
<li><b>You need someone full-time, every day, for years.</b> If the product is your whole business and the team is large, hire full-time.</li>
<li><b>You really need engineers.</b> If the plan is clear and the bottleneck is building it, spend the money on engineering.</li>
</ul>
<h2>How to get the most out of a fractional product manager</h2>
<ul>
<li><b>Set goals for the first 90 days.</b> For example, a trusted roadmap, a successful launch, or a hiring plan.</li>
<li><b>Give them real decision rights.</b> Part-time doesn't work if every call needs sign-off.</li>
<li><b>Plan the hand-over from day one.</b> The goal is documentation and process that outlast the engagement.</li>
</ul>
<h2>What it costs</h2>
<p>Fractional product managers usually charge by the hour or a monthly fee, based on days per week. It costs less than a full-time senior hire, with no recruiting fees, benefits or long-term commitment. If you're unsure where to start, a fixed-scope <a href="/services/product-audit/">product audit</a> is a low-risk first step.</p>
<p>Thinking about it for your team? <a href="/services/fractional-product-manager/">See how fractional product management works at AbengCo</a>, or email us for a free 20-minute intro call.</p>'''))

cr, crld = crumbs([("Home", "/"), ("Insights", "/insights/")])
lst = "".join(f'<article class="box"><h3><a href="{p}">{html.escape(h)}</a></h3><p>{html.escape(d)}</p><p class="meta">{dt}</p></article>' for p, h, d, dt in ARTICLES)
PAGES.append(page("/insights/", "Insights on Product Management, Launches & Automation | AbengCo",
                  "Practical articles on product management, fractional product leadership, launches and automation for consumer app and fintech teams, by Tania Hew.",
                  f'<header class="band page"><div class="wrap">{cr}<h1>Insights</h1><p class="lead">Practical notes on product, launches and automation for consumer app and fintech teams.</p></div></header><section class="band alt"><div class="wrap grid3">{lst}</div></section>',
                  [crld], "Intro call"))

# sitemap
urls = ["/"] + PAGES
open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
                               "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
print("\n".join(urls))

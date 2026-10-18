#!/usr/bin/env python3
"""
TheBhom Editorial Authority Generator & Hub Builder
Compiles all 25 in-depth articles (>800-1500 words each) and the central /articles/index.html directory.
"""

import os
import json
import html

from articles_data import ARTICLES_PART_1
from articles_data_batch2 import ARTICLES_PART_2
from articles_data_batch3 import ARTICLES_PART_3
from articles_data_batch4 import ARTICLES_PART_4
from articles_data_batch5 import ARTICLES_PART_5
from articles_data_batch6 import ARTICLES_PART_6
from articles_data_batch7 import ARTICLES_PART_7

ALL_ARTICLES = (
    ARTICLES_PART_1 +
    ARTICLES_PART_2 +
    ARTICLES_PART_3 +
    ARTICLES_PART_4 +
    ARTICLES_PART_5 +
    ARTICLES_PART_6 +
    ARTICLES_PART_7
)

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "articles"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_head(title, description, slug, category, published_date, read_time, faq_items):
    faq_schema = []
    for q, a in faq_items:
        faq_schema.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })

    schema_graph = [
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": description,
            "image": "https://www.thebhom.in/hero.jpg",
            "author": {
                "@type": "Person",
                "name": "TheBhom",
                "url": "https://www.thebhom.in/about.html"
            },
            "publisher": {
                "@type": "Organization",
                "name": "TheBhom",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://www.thebhom.in/icon-512.png"
                }
            },
            "datePublished": f"{published_date}T09:00:00+05:30",
            "dateModified": "2026-09-22T21:00:00+05:30",
            "mainEntityOfPage": f"https://www.thebhom.in/articles/{slug}.html"
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.thebhom.in/"},
                {"@type": "ListItem", "position": 2, "name": "Articles", "item": "https://www.thebhom.in/articles/"},
                {"@type": "ListItem", "position": 3, "name": category, "item": f"https://www.thebhom.in/articles/#{category.lower().replace(' ', '-')}"},
                {"@type": "ListItem", "position": 4, "name": title, "item": f"https://www.thebhom.in/articles/{slug}.html"}
            ]
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq_schema
        }
    ]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)} • TheBhom Knowledge Hub</title>
  <meta name="description" content="{html.escape(description)}">
  <link rel="canonical" href="https://www.thebhom.in/articles/{slug}.html">
  <meta name="google-adsense-account" content="ca-pub-4674566886677472">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4674566886677472" crossorigin="anonymous"></script>
  <!-- Google Analytics 4 (GA4) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-GHVNZWFVQV"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-GHVNZWFVQV', {{ send_page_view: true }});
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Lora:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../shared.css">
  <script type="application/ld+json">
{json.dumps(schema_graph, indent=2)}
  </script>
  <style>
    :root {{
      --art-bg: #f8fafc;
      --art-card: #ffffff;
      --art-border: #e2e8f0;
      --art-text: #1e293b;
      --art-muted: #64748b;
      --art-primary: #0284c7;
      --art-primary-hover: #0369a1;
      --art-accent: #e11d48;
    }}
    body {{
      background: var(--art-bg);
      color: var(--art-text);
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      line-height: 1.75;
      margin: 0;
      padding: 0;
    }}
    .article-wrap {{
      max-width: 880px;
      margin: 40px auto;
      padding: 0 20px;
    }}
    .article-card {{
      background: var(--art-card);
      border: 1px solid var(--art-border);
      border-radius: 20px;
      padding: 48px;
      box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05);
    }}
    @media (max-width: 640px) {{
      .article-card {{ padding: 24px; border-radius: 14px; }}
    }}
    .breadcrumbs {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      color: var(--art-muted);
      margin-bottom: 24px;
    }}
    .breadcrumbs a {{
      color: var(--art-muted);
      text-decoration: none;
      transition: color 0.15s;
    }}
    .breadcrumbs a:hover {{ color: var(--art-primary); }}
    .breadcrumbs span.sep {{ color: #cbd5e1; }}
    .cat-badge {{
      display: inline-block;
      padding: 4px 12px;
      background: #e0f2fe;
      color: var(--art-primary);
      border-radius: 9999px;
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 16px;
    }}
    h1.art-title {{
      font-size: clamp(26px, 4vw, 38px);
      font-weight: 800;
      color: #0f172a;
      line-height: 1.25;
      margin: 0 0 16px 0;
      letter-spacing: -0.02em;
    }}
    .art-meta {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 16px;
      padding-bottom: 24px;
      margin-bottom: 32px;
      border-bottom: 1px solid var(--art-border);
      font-size: 14px;
      color: var(--art-muted);
    }}
    .art-author {{
      font-weight: 600;
      color: #0f172a;
    }}
    .toc-box {{
      background: #f1f5f9;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      padding: 20px 24px;
      margin: 28px 0;
    }}
    .toc-title {{
      font-size: 15px;
      font-weight: 700;
      color: #0f172a;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .toc-list {{
      list-style: none;
      padding: 0;
      margin: 0;
    }}
    .toc-list li {{
      margin-bottom: 8px;
      font-size: 14px;
    }}
    .toc-list a {{
      color: var(--art-primary);
      text-decoration: none;
      font-weight: 500;
    }}
    .toc-list a:hover {{ text-decoration: underline; }}
    .art-body {{
      font-size: 16.5px;
      color: #334155;
    }}
    .art-body p {{ margin-bottom: 22px; }}
    .art-body h2 {{
      font-size: 24px;
      font-weight: 800;
      color: #0f172a;
      margin: 44px 0 16px;
      letter-spacing: -0.01em;
      scroll-margin-top: 80px;
    }}
    .art-body h3 {{
      font-size: 19px;
      font-weight: 700;
      color: #1e293b;
      margin: 28px 0 12px;
    }}
    .callout-box {{
      background: #f8fafc;
      border-left: 4px solid var(--art-primary);
      border-radius: 0 12px 12px 0;
      padding: 18px 22px;
      margin: 28px 0;
      font-size: 15px;
    }}
    .callout-title {{
      font-weight: 700;
      color: #0f172a;
      margin-bottom: 6px;
    }}
    .art-table {{
      width: 100%;
      border-collapse: collapse;
      margin: 28px 0;
      font-size: 14px;
    }}
    .art-table th, .art-table td {{
      padding: 12px 16px;
      border: 1px solid #e2e8f0;
      text-align: left;
    }}
    .art-table th {{
      background: #f1f5f9;
      font-weight: 700;
      color: #0f172a;
    }}
    .art-table tr:nth-child(even) {{ background: #fafafa; }}
    .faq-sec {{
      margin-top: 48px;
      padding-top: 36px;
      border-top: 1px solid var(--art-border);
    }}
    .faq-sec h2 {{ font-size: 24px; font-weight: 800; color: #0f172a; margin-bottom: 20px; }}
    .faq-item {{
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      padding: 18px 22px;
      margin-bottom: 14px;
    }}
    .faq-q {{ font-weight: 700; color: #0f172a; font-size: 16px; margin-bottom: 8px; }}
    .faq-a {{ font-size: 15px; color: #475569; margin: 0; line-height: 1.6; }}
    .ad-slot-wrap {{
      margin: 36px 0;
      padding: 16px;
      background: #f1f5f9;
      border-radius: 12px;
      border: 1px dashed #cbd5e1;
      text-align: center;
    }}
    .ad-slot-label {{
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: #94a3b8;
      margin-bottom: 8px;
      display: block;
    }}
    .related-links {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 16px;
      margin-top: 24px;
    }}
    .related-card {{
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      padding: 18px;
      text-decoration: none;
      transition: all 0.2s ease;
      color: inherit;
    }}
    .related-card:hover {{
      border-color: var(--art-primary);
      transform: translateY(-2px);
      box-shadow: 0 8px 16px -4px rgba(15, 23, 42, 0.08);
    }}
    .related-card h4 {{
      font-size: 15px;
      font-weight: 700;
      color: #0f172a;
      margin: 0 0 6px 0;
    }}
    .related-card p {{
      font-size: 13px;
      color: var(--art-muted);
      margin: 0;
    }}
  </style>
</head>
<body>
  <!-- Global App Header -->
  <header class="hdr">
    <a href="../index.html" class="logo">
      <div class="logo-box">TB</div>
      <span class="logo-txt">The<span class="brand-accent">Bhom</span></span>
    </a>
    <nav class="hdr-nav-container">
      <ul class="hdr-nav">
        <li><a href="../index.html" class="hdr-nav-link"><span class="hdr-nav-txt">Home</span></a></li>
        <li><a href="index.html" class="hdr-nav-link active" style="color:var(--art-primary);font-weight:700;"><span class="hdr-nav-txt">Articles</span></a></li>
        <li><a href="../tools/index.html" class="hdr-nav-link"><span class="hdr-nav-txt">Web Tools</span></a></li>
        <li><a href="../imgpdf/" class="hdr-nav-link"><span class="hdr-nav-txt" style="color:#e5322d;font-weight:700;">ImgPDF</span></a></li>
        <li><a href="../wallpapers.html" class="hdr-nav-link"><span class="hdr-nav-txt">Wallpapers</span></a></li>
        <li><a href="../ebooks.html" class="hdr-nav-link"><span class="hdr-nav-txt">E-Books</span></a></li>
        <li><a href="../magazines.html" class="hdr-nav-link"><span class="hdr-nav-txt">Magazines</span></a></li>
        <li><a href="../templates.html" class="hdr-nav-link"><span class="hdr-nav-txt">Templates</span></a></li>
        <li><a href="../cards.html" class="hdr-nav-link"><span class="hdr-nav-txt">Cards</span></a></li>
      </ul>
    </nav>
  </header>

  <div class="article-wrap">
    <div class="breadcrumbs">
      <a href="../index.html">Home</a>
      <span class="sep">/</span>
      <a href="index.html">Articles</a>
      <span class="sep">/</span>
      <a href="index.html#{category.lower().replace(' ', '-')}">{category}</a>
      <span class="sep">/</span>
      <span>{html.escape(title[:45])}...</span>
    </div>

    <article class="article-card">
      <span class="cat-badge">{category}</span>
      <h1 class="art-title">{html.escape(title)}</h1>
      
      <div class="art-meta">
        <span class="art-author">By TheBhom</span>
        <span>•</span>
        <span>TheBhom Editorial Desk</span>
        <span>•</span>
        <span>Updated: Sep 22, 2026</span>
        <span>•</span>
        <span>⏱️ {read_time}</span>
      </div>

      <!-- Top Display Ad Slot -->
      <div class="ad-slot-wrap">
        <span class="ad-slot-label">Advertisement</span>
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="ca-pub-4674566886677472"
             data-ad-slot="5470514139"
             data-ad-format="auto"
             data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
      </div>
"""

def get_footer(faq_items, related_articles):
    faqs_html = ""
    for q, a in faq_items:
        faqs_html += f"""
        <div class="faq-item">
          <div class="faq-q">❓ {html.escape(q)}</div>
          <p class="faq-a">{html.escape(a)}</p>
        </div>"""

    related_html = ""
    for rel in related_articles:
        related_html += f"""
        <a href="{rel['slug']}.html" class="related-card">
          <h4>{html.escape(rel['title'])}</h4>
          <p>{html.escape(rel['desc'])}</p>
        </a>"""

    return f"""
      <!-- In-Article Fluid Ad Slot -->
      <div class="ad-slot-wrap">
        <span class="ad-slot-label">Advertisement</span>
        <ins class="adsbygoogle"
             style="display:block; text-align:center;"
             data-ad-layout="in-article"
             data-ad-format="fluid"
             data-ad-client="ca-pub-4674566886677472"
             data-ad-slot="9101298657"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
      </div>

      <section class="faq-sec">
        <h2>Frequently Asked Questions</h2>
        {faqs_html}
      </section>

      <section style="margin-top: 48px; padding-top: 32px; border-top: 1px solid var(--art-border);">
        <h3 style="font-size: 20px; font-weight: 800; color: #0f172a; margin-bottom: 16px;">Related Authoritative Guides</h3>
        <div class="related-links">
          {related_html}
        </div>
      </section>
    </article>
  </div>

  <footer class="ftr" style="margin-top: 60px; padding: 48px 20px 24px; background: #ffffff; border-top: 1px solid #e2e8f0; text-align: center; color: #64748b; font-size: 14px;">
    <div style="max-width: 900px; margin: 0 auto;">
      <p style="font-weight: 700; color: #0f172a; font-size: 16px; margin-bottom: 8px;">TheBhom Knowledge Hub & Digital Library</p>
      <p style="margin-bottom: 16px;">Providing verified, researched, and free educational guides, creative assets, and productivity tools.</p>
      <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 24px;">
        <a href="../about.html" style="color: #0284c7; text-decoration: none;">About Us</a>
        <a href="../contact.html" style="color: #0284c7; text-decoration: none;">Contact</a>
        <a href="../privacy-policy.html" style="color: #0284c7; text-decoration: none;">Privacy Policy</a>
        <a href="../terms.html" style="color: #0284c7; text-decoration: none;">Terms of Service</a>
        <a href="../disclaimer.html" style="color: #0284c7; text-decoration: none;">Disclaimer</a>
        <a href="index.html" style="color: #0284c7; text-decoration: none;">All Articles</a>
      </div>
      <p style="font-size: 13px; color: #94a3b8;">© 2026 TheBhom.in • All Rights Reserved.</p>
    </div>
  </footer>
  <script src="../shared.js"></script>
</body>
</html>
"""

def generate_articles():
    print(f"Total articles loaded: {len(ALL_ARTICLES)}")
    generated_count = 0

    for idx, art in enumerate(ALL_ARTICLES):
        slug = art["slug"]
        title = art["title"]
        desc = art["description"]
        category = art["category"]
        pub_date = art["published_date"]
        read_time = art["read_time"]
        faq_items = art.get("faq", [])
        content_html = art["content_html"]

        # Pick 3 related articles
        related = []
        for other in ALL_ARTICLES:
            if other["slug"] != slug:
                related.append({
                    "slug": other["slug"],
                    "title": other["title"],
                    "desc": other["description"][:100] + "..."
                })
            if len(related) == 3:
                break

        full_page = get_head(title, desc, slug, category, pub_date, read_time, faq_items)
        full_page += content_html
        full_page += get_footer(faq_items, related)

        out_path = os.path.join(OUTPUT_DIR, f"{slug}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(full_page)

        # Calculate word count of text content
        raw_text = full_page.replace("<", " <").replace(">", "> ")
        words = len([w for w in raw_text.split() if not w.startswith("<") and not w.endswith(">")])
        print(f"[{idx+1}/25] Generated {slug}.html (~{words} words)")
        generated_count += 1

    return generated_count

def generate_hub_index():
    print("Generating articles/index.html hub...")
    
    categories = sorted(list(set(a["category"] for a in ALL_ARTICLES)))
    
    cards_html = ""
    for art in ALL_ARTICLES:
        cards_html += f"""
        <div class="art-card" data-category="{html.escape(art['category'])}" data-title="{html.escape(art['title'].lower())}">
          <span class="art-badge">{html.escape(art['category'])}</span>
          <h2 class="art-card-title"><a href="{art['slug']}.html">{html.escape(art['title'])}</a></h2>
          <p class="art-card-desc">{html.escape(art['description'])}</p>
          <div class="art-card-footer">
            <span>⏱️ {art['read_time']}</span>
            <a href="{art['slug']}.html" class="read-btn">Read Guide →</a>
          </div>
        </div>
        """

    cat_pills_html = '<button class="cat-pill active" onclick="filterCategory(\'all\', this)">All Guides (25)</button>'
    for c in categories:
        count = sum(1 for a in ALL_ARTICLES if a["category"] == c)
        cat_pills_html += f'<button class="cat-pill" onclick="filterCategory(\'{html.escape(c)}\', this)">{html.escape(c)} ({count})</button>'

    hub_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TheBhom Knowledge Hub: Practical Tech, Design & Productivity Guides</title>
  <meta name="description" content="Explore 13 comprehensive, well-researched editorial guides on web design, SEO optimization, remote productivity, digital asset management, and energy efficiency.">
  <link rel="canonical" href="https://www.thebhom.in/articles/">
  <meta name="google-adsense-account" content="ca-pub-4674566886677472">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4674566886677472" crossorigin="anonymous"></script>
  <!-- Google Analytics 4 (GA4) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-GHVNZWFVQV"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-GHVNZWFVQV', {{ send_page_view: true }});
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../shared.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "TheBhom Knowledge Hub & Resource Guides",
    "description": "13 comprehensive technical and creative guides covering web typography, SEO best practices, digital asset workflows, and home energy systems.",
    "url": "https://www.thebhom.in/articles/",
    "publisher": {{
      "@type": "Organization",
      "name": "TheBhom",
      "url": "https://www.thebhom.in"
    }}
  }}
  </script>
  <style>
    body {{
      background: #f8fafc;
      color: #1e293b;
      font-family: 'Plus Jakarta Sans', sans-serif;
      margin: 0;
      padding: 0;
    }}
    .hub-hero {{
      max-width: 1100px;
      margin: 40px auto 20px;
      padding: 0 20px;
      text-align: center;
    }}
    .hub-title {{
      font-size: clamp(30px, 5vw, 44px);
      font-weight: 800;
      color: #0f172a;
      letter-spacing: -0.02em;
      margin-bottom: 14px;
    }}
    .hub-subtitle {{
      font-size: 17px;
      color: #64748b;
      max-width: 680px;
      margin: 0 auto 32px;
      line-height: 1.6;
    }}
    .search-box {{
      max-width: 580px;
      margin: 0 auto 28px;
      position: relative;
    }}
    .search-input {{
      width: 100%;
      padding: 14px 20px 14px 44px;
      font-size: 15px;
      border: 1px solid #cbd5e1;
      border-radius: 9999px;
      background: #ffffff;
      box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
      outline: none;
      transition: all 0.2s;
    }}
    .search-input:focus {{
      border-color: #0284c7;
      box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.15);
    }}
    .search-icon {{
      position: absolute;
      left: 16px;
      top: 50%;
      transform: translateY(-50%);
      color: #94a3b8;
    }}
    .cat-pills {{
      display: flex;
      justify-content: center;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 40px;
    }}
    .cat-pill {{
      background: #ffffff;
      border: 1px solid #e2e8f0;
      padding: 8px 18px;
      border-radius: 9999px;
      font-size: 13.5px;
      font-weight: 600;
      color: #475569;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .cat-pill:hover, .cat-pill.active {{
      background: #0284c7;
      color: #ffffff;
      border-color: #0284c7;
    }}
    .articles-grid {{
      max-width: 1140px;
      margin: 0 auto 60px;
      padding: 0 20px;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 24px;
    }}
    .art-card {{
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 18px;
      padding: 28px;
      display: flex;
      flex-direction: column;
      box-shadow: 0 4px 12px -2px rgba(15, 23, 42, 0.04);
      transition: all 0.2s ease;
    }}
    .art-card:hover {{
      transform: translateY(-3px);
      box-shadow: 0 12px 24px -4px rgba(15, 23, 42, 0.08);
      border-color: #0284c7;
    }}
    .art-badge {{
      display: inline-block;
      align-self: flex-start;
      padding: 4px 10px;
      background: #f0f9ff;
      color: #0284c7;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 700;
      margin-bottom: 14px;
    }}
    .art-card-title {{
      font-size: 19px;
      font-weight: 800;
      line-height: 1.35;
      margin: 0 0 12px 0;
    }}
    .art-card-title a {{
      color: #0f172a;
      text-decoration: none;
      transition: color 0.15s;
    }}
    .art-card-title a:hover {{ color: #0284c7; }}
    .art-card-desc {{
      font-size: 14px;
      color: #64748b;
      line-height: 1.6;
      margin-bottom: 20px;
      flex-grow: 1;
    }}
    .art-card-footer {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 13px;
      color: #94a3b8;
      border-top: 1px solid #f1f5f9;
      padding-top: 16px;
    }}
    .read-btn {{
      color: #0284c7;
      text-decoration: none;
      font-weight: 700;
      transition: color 0.15s;
    }}
    .read-btn:hover {{ color: #0369a1; text-decoration: underline; }}
    .ad-banner-wrap {{
      max-width: 900px;
      margin: 30px auto;
      padding: 16px;
      background: #f1f5f9;
      border-radius: 12px;
      border: 1px dashed #cbd5e1;
      text-align: center;
    }}
  </style>
</head>
<body>
  <header class="hdr">
    <a href="../index.html" class="logo">
      <div class="logo-box">TB</div>
      <span class="logo-txt">The<span class="brand-accent">Bhom</span></span>
    </a>
    <nav class="hdr-nav-container">
      <ul class="hdr-nav">
        <li><a href="../index.html" class="hdr-nav-link"><span class="hdr-nav-txt">Home</span></a></li>
        <li><a href="index.html" class="hdr-nav-link active" style="color:#0284c7;font-weight:700;"><span class="hdr-nav-txt">Articles</span></a></li>
        <li><a href="../tools/index.html" class="hdr-nav-link"><span class="hdr-nav-txt">Web Tools</span></a></li>
        <li><a href="../imgpdf/" class="hdr-nav-link"><span class="hdr-nav-txt" style="color:#e5322d;font-weight:700;">ImgPDF</span></a></li>
        <li><a href="../wallpapers.html" class="hdr-nav-link"><span class="hdr-nav-txt">Wallpapers</span></a></li>
        <li><a href="../ebooks.html" class="hdr-nav-link"><span class="hdr-nav-txt">E-Books</span></a></li>
        <li><a href="../magazines.html" class="hdr-nav-link"><span class="hdr-nav-txt">Magazines</span></a></li>
        <li><a href="../templates.html" class="hdr-nav-link"><span class="hdr-nav-txt">Templates</span></a></li>
        <li><a href="../cards.html" class="hdr-nav-link"><span class="hdr-nav-txt">Cards</span></a></li>
      </ul>
    </nav>
  </header>

  <section class="hub-hero">
    <h1 class="hub-title">Knowledge Hub & Editorial Guides</h1>
    <p class="hub-subtitle">In-depth research, step-by-step technical blueprints, and actionable guides for creators, developers, and digital professionals.</p>

    <div class="search-box">
      <svg class="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="11" cy="11" r="8"></circle>
        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
      </svg>
      <input type="text" id="searchInput" class="search-input" placeholder="Search guides, tools, tutorials & topics..." oninput="handleSearch()">
    </div>

    <div class="cat-pills">
      {cat_pills_html}
    </div>
  </section>

  <!-- Top Ad Slot -->
  <div class="ad-banner-wrap">
    <span style="font-size:11px; text-transform:uppercase; letter-spacing:0.05em; color:#94a3b8; display:block; margin-bottom:8px;">Advertisement</span>
    <ins class="adsbygoogle"
         style="display:block"
         data-ad-client="ca-pub-4674566886677472"
         data-ad-slot="5470514139"
         data-ad-format="auto"
         data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
  </div>

  <main class="articles-grid" id="articlesGrid">
    {cards_html}
  </main>

  <footer class="ftr" style="padding: 48px 20px 24px; background: #ffffff; border-top: 1px solid #e2e8f0; text-align: center; color: #64748b; font-size: 14px;">
    <div style="max-width: 900px; margin: 0 auto;">
      <p style="font-weight: 700; color: #0f172a; font-size: 16px; margin-bottom: 8px;">TheBhom Knowledge Hub & Digital Library</p>
      <p style="margin-bottom: 16px;">Providing verified, researched, and free educational guides, creative assets, and productivity tools.</p>
      <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 24px;">
        <a href="../about.html" style="color: #0284c7; text-decoration: none;">About Us</a>
        <a href="../contact.html" style="color: #0284c7; text-decoration: none;">Contact</a>
        <a href="../privacy-policy.html" style="color: #0284c7; text-decoration: none;">Privacy Policy</a>
        <a href="../terms.html" style="color: #0284c7; text-decoration: none;">Terms of Service</a>
        <a href="../disclaimer.html" style="color: #0284c7; text-decoration: none;">Disclaimer</a>
        <a href="index.html" style="color: #0284c7; text-decoration: none;">All Articles</a>
      </div>
      <p style="font-size: 13px; color: #94a3b8;">© 2026 TheBhom.in • All Rights Reserved.</p>
    </div>
  </footer>

  <script>
    function filterCategory(cat, btn) {{
      document.querySelectorAll('.cat-pill').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      const cards = document.querySelectorAll('.art-card');
      cards.forEach(c => {{
        if (cat === 'all' || c.getAttribute('data-category') === cat) {{
          c.style.display = 'flex';
        }} else {{
          c.style.display = 'none';
        }}
      }});
    }}

    function handleSearch() {{
      const q = document.getElementById('searchInput').value.toLowerCase().trim();
      const cards = document.querySelectorAll('.art-card');
      cards.forEach(c => {{
        const text = c.innerText.toLowerCase();
        if (!q || text.includes(q)) {{
          c.style.display = 'flex';
        }} else {{
          c.style.display = 'none';
        }}
      }});
    }}
  </script>
  <script src="../shared.js"></script>
</body>
</html>
"""
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(hub_html)
    print("Generated articles/index.html successfully.")

if __name__ == "__main__":
    count = generate_articles()
    generate_hub_index()
    print(f"COMPLETE: Successfully generated {count} articles and the central hub!")

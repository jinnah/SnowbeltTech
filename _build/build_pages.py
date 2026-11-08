"""Assemble SnowBeltTech inner pages from content fragments + the homepage's header/footer."""
import os, re, sys

root, frag_dir = sys.argv[1], sys.argv[2]
home = open(os.path.join(root, 'index.html'), encoding='utf-8').read()
header = re.search(r'<!--HEADER-->.*?<!--/HEADER-->', home, re.S).group(0)
footer = re.search(r'<!--FOOTER-->.*?<!--/FOOTER-->', home, re.S).group(0)
fonts = re.search(r'<link rel="preconnect".*?display=swap" rel="stylesheet">', home, re.S).group(0)
css = re.search(r'<link rel="stylesheet" href="/assets/site\.css[^"]*">', home).group(0)
js = re.search(r'<script src="/assets/site\.js[^"]*" defer></script>', home).group(0)

TPL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="https://snowbelttech.com/{slug}/">
<meta name="robots" content="index, follow">
<meta property="og:type" content="website">
<meta property="og:url" content="https://snowbelttech.com/{slug}/">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="https://snowbelttech.com/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://snowbelttech.com/assets/og-image.png">
<link rel="icon" href="/assets/favicon.ico" sizes="32x32">
<link rel="icon" href="/assets/favicon-32.png" type="image/png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta name="theme-color" content="#0A1730">
{fonts}
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "{service}",
  "url": "https://snowbelttech.com/{slug}/",
  "areaServed": "Western New York",
  "provider": {{ "@type": "ProfessionalService", "name": "SnowBeltTech", "url": "https://snowbelttech.com", "telephone": "+1-646-982-6252",
    "address": {{ "@type": "PostalAddress", "addressLocality": "Buffalo", "addressRegion": "NY", "addressCountry": "US" }} }}
}}
</script>
{css}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

{header}

<main id="main">
{body}
</main>

{footer}

{js}
</body>
</html>
"""

for name in sorted(os.listdir(frag_dir)):
    if not name.endswith('.html'):
        continue
    raw = open(os.path.join(frag_dir, name), encoding='utf-8').read()
    m = re.match(r'<!--META\n(.*?)\n-->\n', raw, re.S)
    meta = dict(line.split(': ', 1) for line in m.group(1).splitlines())
    body = raw[m.end():]
    # page-local <script> blocks go after the shared footer script
    scripts = ''.join(re.findall(r'<script>.*?</script>\n?', body, re.S))
    body = re.sub(r'<script>.*?</script>\n?', '', body, flags=re.S)
    out = TPL.format(header=header, footer=footer, fonts=fonts, css=css,
                     js=js + ('\n' + scripts.strip() if scripts else ''), body=body.strip(), **meta)
    d = os.path.join(root, meta['slug'])
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8', newline='\n').write(out)
    print('wrote', meta['slug'] + '/index.html', len(out))

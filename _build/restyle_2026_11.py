"""One-off restyle (2026-11-08): new fonts (Archivo / Figtree / Instrument Serif) and a brighter palette.
Run from the repo root:  python _build/restyle_2026_11.py
"""
import re

p = 'assets/site.css'
s = open(p, encoding='utf-8').read()

# 1. tokens -------------------------------------------------------------------
root_old = s[s.index(':root{'):s.index('}', s.index(':root{')) + 1]
root_new = """:root{
  --ink:#071A3D; --ink-2:#0E2858; --navy:#153E8F; --teal:#1F6FEB; --ice:#9CCBFF;
  --snow:#F6F8FC; --paper:#FFFFFF; --line:#DDE4F0; --line-dark:#1E3A70;
  --text:#0B1834; --muted:#4F5F7A; --muted-dark:#A3B6D6;
  --ok:#12A66A; --ok-soft:#E2F7EE; --warn:#D98A0B; --warn-soft:#FFF1D6; --alert:#D2483A;
  --signal:#FF7A2F; --signal-hover:#FF8F4F; --signal-ink:#071A3D;
  --sky:#6FB6FF; --go:#3DDC97;
  --r-sm:10px; --r:16px; --r-lg:24px;
  --display:"Archivo", system-ui, sans-serif;
  --body:"Figtree", system-ui, sans-serif;
  --serif:"Instrument Serif", Georgia, serif;
  --mono:"JetBrains Mono", ui-monospace, monospace;
  --wrap:1180px;
  --gutter:max(20px, env(safe-area-inset-left));
}"""
s = s.replace(root_old, root_new)

# 2. type ---------------------------------------------------------------------
s = s.replace('h1,h2,h3{font-family:var(--display);line-height:1.08;letter-spacing:-.02em;margin:0;font-weight:750}',
              'h1,h2,h3{font-family:var(--display);line-height:1.06;letter-spacing:-.022em;margin:0;font-weight:800}\n'
              'h1,h2{font-stretch:106%}')
s = s.replace('h3{font-size:21px;letter-spacing:-.01em;font-weight:650}', 'h3{font-size:21px;letter-spacing:-.012em;font-weight:700}')
s = s.replace('font:400 17px/1.6 var(--body)', 'font:400 17.5px/1.62 var(--body)')
s = s.replace('.hero h1{font-size:clamp(42px,6.6vw,80px);letter-spacing:-.035em;margin:20px 0 22px}',
              '.hero h1{font-size:clamp(44px,6.4vw,82px);line-height:1;letter-spacing:-.03em;margin:22px 0 24px}')
s = s.replace('.hero h1 em{font-style:normal;color:var(--teal);position:relative;white-space:nowrap}',
              '.hero h1 em,.page-hero h1 em,h2 em{font-family:var(--serif);font-style:italic;font-weight:400;font-stretch:100%;letter-spacing:-.01em;color:var(--teal);position:relative;white-space:nowrap;padding-right:.04em}')
s = s.replace('.hero h1 em::after{content:"";position:absolute;left:0;right:0;bottom:.06em;height:.12em;background:var(--signal);opacity:.55;border-radius:4px;z-index:-1}',
              '.hero h1 em::after{content:"";position:absolute;left:-.04em;right:-.02em;bottom:.04em;height:.2em;background:var(--signal);opacity:.35;border-radius:3px;z-index:-1;transform:skewX(-12deg)}\n'
              '.dark h2 em{color:var(--sky)}')
s = s.replace('.page-hero h1{font-size:clamp(36px,5.4vw,64px);letter-spacing:-.03em;',
              '.page-hero h1{font-size:clamp(36px,5.2vw,62px);line-height:1.04;letter-spacing:-.028em;')

# 3. buttons ------------------------------------------------------------------
s = s.replace('.btn-signal{background:var(--signal);color:var(--signal-ink);box-shadow:0 8px 24px -10px rgba(31,211,154,.8)}',
              '.btn-signal{background:var(--signal);color:var(--signal-ink);font-weight:700;box-shadow:0 10px 26px -10px rgba(255,122,47,.75), inset 0 -2px 0 rgba(0,0,0,.12)}')
s = s.replace('.btn-signal:hover{background:#3BE3AD}', '.btn-signal:hover{background:var(--signal-hover)}')
s = s.replace('.btn-ghost:hover{box-shadow:inset 0 0 0 1.5px var(--navy)}', '.btn-ghost:hover{box-shadow:inset 0 0 0 1.5px var(--teal);color:var(--teal)}')

# 4. accents on dark backgrounds: mint -> sky blue / green --------------------
dark_text = ['.dark .eyebrow{color:var(--signal)}', '.svc.feature .svc-tag{color:var(--signal)}',
             '.svc.feature .svc-link{color:var(--signal)}', '.dark-pkg .pkg-kind{color:var(--signal)}']
for rule in dark_text:
    s = s.replace(rule, rule.replace('var(--signal)', 'var(--sky)'))
s = s.replace('.svc.feature .svc-icon{background:rgba(255,255,255,.06);color:var(--signal)}', '.svc.feature .svc-icon{background:rgba(255,255,255,.06);color:var(--sky)}')
s = s.replace('.flow li::before{content:"0" counter(f);font:500 12px var(--mono);color:var(--signal);', '.flow li::before{content:"0" counter(f);font:500 12px var(--mono);color:var(--sky);')
s = s.replace('.human svg{flex:none;color:var(--signal);', '.human svg{flex:none;color:var(--sky);')
s = s.replace('.dark-pkg li::before{border-color:var(--signal)}', '.dark-pkg li::before{border-color:var(--sky)}')
# status dots / logs stay "all clear" green
for a in ['.live{margin-left:auto;display:inline-flex;align-items:center;gap:8px;color:var(--signal)}',
          '.log .ok{color:var(--signal)}']:
    s = s.replace(a, a.replace('var(--signal)', 'var(--go)'))
s = s.replace('.metric b::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--signal);', '.metric b::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--go);')
s = s.replace('.live::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--signal);box-shadow:0 0 0 0 rgba(31,211,154,.6)', '.live::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--go);box-shadow:0 0 0 0 rgba(61,220,151,.6)')
s = s.replace('@keyframes pulse{70%{box-shadow:0 0 0 8px rgba(31,211,154,0)}100%{box-shadow:0 0 0 0 rgba(31,211,154,0)}}', '@keyframes pulse{70%{box-shadow:0 0 0 8px rgba(61,220,151,0)}100%{box-shadow:0 0 0 0 rgba(61,220,151,0)}}')
s = s.replace('.badge-dot{width:10px;height:10px;border-radius:50%;background:var(--signal);box-shadow:0 0 0 4px rgba(31,211,154,.2)', '.badge-dot{width:10px;height:10px;border-radius:50%;background:var(--signal);box-shadow:0 0 0 4px rgba(255,122,47,.25)')
# calculator results: warm orange on navy
s = s.replace('.cm-result b{font:650 28px var(--display);color:var(--signal)}', '.cm-result b{font:800 28px var(--display);color:var(--signal)}')
s = s.replace('.cm-result{background:rgba(31,211,154,.08);border:1px solid rgba(31,211,154,.3);', '.cm-result{background:rgba(255,122,47,.08);border:1px solid rgba(255,122,47,.35);')
s = s.replace('.big-range{font:650 ', '.big-range{font:800 ')
# remaining mint tints (check-mark circles, human note) -> sky
s = s.replace('rgba(31,211,154,', 'rgba(111,182,255,')
s = s.replace('%231FD39A', '%236FB6FF')
# old palette rgba leftovers
s = s.replace('rgba(158,216,240,', 'rgba(111,182,255,')
s = s.replace('rgba(43,139,181,', 'rgba(31,111,235,')
s = s.replace('rgba(23,55,94,', 'rgba(21,62,143,')
s = s.replace('rgba(10,23,48,', 'rgba(7,26,61,')

# 5. backgrounds with more life -----------------------------------------------
s = re.sub(r'\.hero::before\{content:"";position:absolute;inset:0;background:.*?pointer-events:none\}',
           '.hero::before{content:"";position:absolute;inset:0;background:'
           'radial-gradient(42% 55% at 88% 18%, rgba(31,111,235,.20), transparent 70%),'
           'radial-gradient(30% 40% at 70% 85%, rgba(255,122,47,.16), transparent 70%),'
           'radial-gradient(40% 50% at 0% 0%, rgba(111,182,255,.18), transparent 70%);pointer-events:none}', s, flags=re.S)
s = s.replace('.dark::before{content:"";position:absolute;inset:0;background:repeating-linear-gradient(-28deg, transparent 0 46px, rgba(111,182,255,.035) 46px 47px);pointer-events:none}',
              '.dark::before{content:"";position:absolute;inset:0;background:radial-gradient(50% 60% at 100% 0%, rgba(31,111,235,.35), transparent 70%),radial-gradient(40% 50% at 0% 100%, rgba(255,122,47,.12), transparent 70%);pointer-events:none}')
s = s.replace('.tint{background:#E9EEF1}', '.tint{background:#EDF2FC}')
s = s.replace('.strip{background:var(--ink);', '.strip{background:linear-gradient(90deg,var(--ink),#0C2A66);')
s = s.replace('.dh-steps li:first-child::before{background:var(--signal);border-color:var(--signal);color:var(--signal-ink)}',
              '.dh-steps li:first-child::before{background:var(--signal);border-color:var(--signal);color:var(--signal-ink);font-weight:700}')
s = s.replace('.page-hero::before{content:"";position:absolute;inset:0;background:radial-gradient(55% 60% at 90% 10%, rgba(111,182,255,.45), transparent 70%),repeating-linear-gradient(-28deg, transparent 0 46px, rgba(21,62,143,.035) 46px 47px);pointer-events:none}',
              '.page-hero::before{content:"";position:absolute;inset:0;background:radial-gradient(45% 60% at 92% 10%, rgba(31,111,235,.20), transparent 70%),radial-gradient(30% 45% at 75% 95%, rgba(255,122,47,.14), transparent 70%);pointer-events:none}')
# numbers/prices use the display face at heavier weights
s = s.replace('font:650 ', 'font:800 ')
open(p, 'w', encoding='utf-8').write(s)

# 6. fonts link in homepage + inline accents -----------------------------------
ip = 'index.html'
h = open(ip, encoding='utf-8').read()
h = re.sub(r'<link href="https://fonts\.googleapis\.com/css2\?[^"]+" rel="stylesheet">',
           '<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,500..900&family=Figtree:wght@400;500;600;700&family=Instrument+Serif:ital@1&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">', h)
h = h.replace('<span class="svc-tag" style="color:var(--signal)">Our main service</span>', '<span class="svc-tag" style="color:var(--sky)">Our main service</span>')
h = h.replace('assets/site.css?v=20261108"', 'assets/site.css?v=20261108b"')
open(ip, 'w', encoding='utf-8').write(h)
print('restyled')

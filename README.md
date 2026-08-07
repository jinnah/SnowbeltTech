# Snowbelt AI Automation — website

Single-page marketing site. One file: `Snowbelt AI Automation.dc.html`. Open it in a browser, or upload it with `support.js` to any static host.

## Design direction

Deep navy ground (`#0A1B2E`) for trust and structure, ice blue (`#7DD3FC`) and electric cyan (`#22D3EE`) for the automation layer, amber (`#F59E0B`) reserved exclusively for the primary CTA so there is never a question about what to click. White and `#F5F8FB` alternate to separate sections without adding color.

Type: **Manrope** for headings (geometric, confident, not a startup default), **IBM Plex Sans** for body copy — its slight industrial character suits a trades audience.

Buffalo shows up structurally rather than literally: the faint diagonal banding behind the dark sections reads as lake-effect bands moving across the page, and the copy references the region without becoming a tourism site. No snowflakes, no robots, no stock photography.

Diagrams are drawn, not illustrated: the hero flow, the connected-lead system and the phone thread are all real markup, so they stay crisp at any size and can be edited as content.

## Stand-in values to confirm before launch

The bracket placeholders are gone — nothing broken renders to a visitor any more. What
replaced them are **stand-ins that need your real values**. Search and replace:

| Stand-in currently in the file | Where | Notes |
| --- | --- | --- |
| `(716) 555-0100` / `tel:+17165550100` | header call button, mobile nav, final CTA, contact list, footer | 555 numbers are reserved and unreachable by design |
| `hello@snowbelttech.com` | contact list, footer (`mailto:`) | |
| `https://snowbelttech.com` | `og:url`, `og:image`, `twitter:image`, canonical, JSON-LD `url`, `robots.txt`, `sitemap.xml` | guessed from the brand name |
| `https://www.linkedin.com/company/snowbelt-tech` | footer "Follow us" | guessed handle — confirm or remove the link |
| `#contact` | the two former `[BOOKING LINK]` slots | deliberately points at the on-page form so it can never 404; swap for a Calendly/Cal.com URL when you have one |
| `Buffalo, New York · Serving all of Western New York` | footer | no street address invented |

**The pricing band carries real numbers now** — `$2,500 – $6,000`, `$500 – $1,200`,
`$1,500 – $4,500` and `$250 – $900/mo`. These are plausible market rates for a small WNY
agency, not your rates. Confirm them before launch; they are the most consequential
stand-in on the page.

`[N8N WEBHOOK URL]` is **left as-is on purpose** — see "Wiring the form to n8n". While the
value still starts with `[`, the form validates and shows its success state without
sending anything, which is the correct demo behavior. Replacing it with a fake URL would
make the form POST to a dead endpoint.

The phone number shown inside the missed-call demo (`(716) 555-0148`) and the example business name (Northline Heating & Cooling) are illustrative and clearly fictional. Swap or keep as you prefer.

## Wiring the form to n8n

The contact form posts JSON to a webhook. Open the file, find `const WEBHOOK = '[N8N WEBHOOK URL]';` and paste your production webhook URL. While the value still starts with `[`, the form validates and shows the success state without sending anything — useful for demos.

Payload shape:

```json
{
  "name": "Dave Kowalski",
  "businessName": "Northline Heating & Cooling",
  "email": "dave@example.com",
  "phone": "716-555-0148",
  "businessType": "HVAC",
  "goal": "We miss a lot of calls in January.",
  "preferredContact": "Phone",
  "marketingConsent": false,
  "source": "snowbelt-website",
  "submittedAt": "2026-08-05T14:12:03.918Z"
}
```

Suggested n8n workflow: **Webhook (POST)** → **Google Sheets: Append Row** → **Gmail/SMTP: notify yourself** → **Twilio: SMS alert** → optionally an **IF** node on `marketingConsent` before adding to a marketing list.

Two things to set on the n8n side:

1. **CORS.** The browser posts cross-origin. In the Webhook node's options add response headers `Access-Control-Allow-Origin: https://yourdomain.com` and `Access-Control-Allow-Headers: content-type`, and add a second Webhook node on the same path with method `OPTIONS` returning 200. Alternatively proxy `/api/lead` on your host to n8n and keep it same-origin.
2. **Spam.** The form has no captcha. Add a honeypot field or rate-limit the webhook if it starts collecting junk.

The form does not wait for the webhook response — it shows the success state immediately and fires the request in the background, so a slow n8n instance never blocks the visitor. If you want the success state to depend on a 200 response, move `this.setState({ sent: true })` into the fetch's `.then()`.

## SEO

**In the page already:** title, meta description, Open Graph + Twitter card tags, canonical link, `robots` meta, and `ProfessionalService` JSON-LD with a six-service `hasOfferCatalog`. Headings run h1 → h2 → h3 with no skips — the hero headline is the only h1. The footer carries a natural service-area paragraph naming the WNY towns you cover (not a keyword block).

**Before launch — replace `https://snowbelttech.com` everywhere** if that isn't the real
origin. It appears in `og:url`, `og:image`, `twitter:image`, the canonical link, the
JSON-LD `url`, `robots.txt` and `sitemap.xml`. Use the full origin with no trailing slash.

**Then:**

1. ~~Make `assets/og-image.png`~~ — **done.** Built at 1200×630 from the light logo on the
   hero's navy gradient; source is `_build/og.html`, so you can edit that file and
   re-screenshot it at a 1200×630 viewport to regenerate.
2. **Claim and fill the Google Business Profile.** For a local service business this outranks almost everything else on the page. Once it's live, add its URL to the JSON-LD as `sameAs`.
3. **Fill in the real NAP.** The structured data deliberately omits phone, address and geo because inventing them is worse than leaving them out. Add `telephone` and a full `address` once they exist, and keep them character-for-character identical to the Google Business Profile.
4. ~~Add `<html lang="en">`~~ — **done**, it's on the root element.

**Single-page tradeoff worth knowing.** One page can only rank for one primary intent. Someone searching "website design Buffalo" and someone searching "missed call text back" want different pages. When you're ready to compete on more than the brand name, the highest-value additions are separate indexable pages per service (`/web-design-buffalo`, `/local-seo-analysis`) and per service area — each with its own title, description and h1. The current page is the right hub for those to link from.

**Don't** add a keyword-stuffed footer, hidden text, or an FAQ section written for search engines rather than customers. Google's local algorithm weighs proximity, prominence and profile completeness far more than on-page repetition.

## Accessibility & behavior

Skip link, keyboard-reachable nav with a visible 3px cyan focus ring, labeled form controls with inline error messages, `aria-selected` on both the industry tabs and the missed-call trade tabs, and `prefers-reduced-motion` handling that stops the flow animations and renders the missed-call thread instantly. Marketing consent is unchecked by default. All tap targets are at least 44px.

Layout is fluid — `clamp()` and auto-fit grids rather than fixed breakpoints — with JS-driven switches at 768px (hero visual) and 1040px (two-column hero, desktop nav). Header height, hero padding and type scale with `clamp()` between those points, and horizontal padding respects `env(safe-area-inset-*)` for notched iPhones.

**Tap-to-call.** Below 1040px the header carries a navy "Call" pill next to the menu
button, and the mobile menu repeats it with the number spelled out. Both are `tel:` links.
The header row's gap is `clamp(10px,3vw,28px)` and the call pill and menu button are both
`flex:none`, so at 320px the logo, call button and menu button all still fit with the menu
button at its full 44px rather than being squeezed to 36px.

**Mobile hero (below 768px)** is deliberately different from desktop, not a squeezed copy: the long service list collapses to a compact "AI automation for local businesses" pill, a one-line value sentence appears under the headline, the CTA goes full width with a "Free review · No obligation · 15 minutes" reassurance line, and the eight-node flow board is replaced by a four-stage glass card (Website visit → Lead captured → Follow-up → Job booked) that lays out fluidly — 4 across, 2×2 below 400px — with no scaled canvas, so nothing clips at 320px.

## Animated sections

Three things run on their own; all of them stop for `prefers-reduced-motion`.

- **Hero journey** — four stages advance on a loop: missed call → instant text → CRM updated → job booked. Orange lands only on the booking.
- **Connected lead system** — the full multi-channel diagram. The source channel rotates each cycle and the notified role changes with it (a missed call wakes the dispatcher, a form goes to the estimator).
- **Missed-call thread** — three trade conversations (HVAC, Roofing, Concrete) play in sequence. Visitors can jump to a trade with the tabs; edit the `THREADS` array to change the copy, the business names or the logged-lead line.

## Imagery

The original brief called for no stock photography, and the diagrams are still drawn
markup. The one exception is the **industry card**, which now carries a photograph per
trade in `assets/industries/` (`hvac`, `plumbing`, `electrical`, `roofing`, `landscaping`,
`cleaning`, `auto`, `contracting`, `professional`). They are generated images, cool-graded
to the navy palette and sat under a `#0A1B2E` gradient that fades the bottom of the frame
into the card, so they read as part of the surface rather than pasted onto it. Each swaps
with its tab and carries its own `alt` text from the `INDUSTRIES` array.

They are 900px wide JPEGs, ~40–85 KB each, ~490 KB for the whole set, and lazy-loaded — only
the visible one costs anything on first paint. To drop the photography entirely, delete the
image band `<div>` at the top of the industry card; nothing else depends on it.

**Icons and social card** are in `assets/`: `favicon.ico` (32px), `favicon-32.png`,
`apple-touch-icon.png` (180px), `icon-512.png` and `og-image.png` (1200×630). All are
derived from the real logo rather than redrawn — `_build/favicon.html` and `_build/og.html`
are the sources; screenshot them at 512×512 and 1200×630 to regenerate.

## Hosting (Docker)

The site ships as an nginx container. There is no build step — the image is the static
files plus a server config.

```bash
git clone https://github.com/jinnah/SnowbeltTech.git
cd SnowbeltTech
docker compose up -d --build
```

That serves the site on **port 8080**. To use port 80 instead:

```bash
echo "HTTP_PORT=80" > .env
docker compose up -d
```

The default is 8080 rather than 80 so a first run cannot fail by colliding with an
Apache or nginx already listening on 80 on a fresh VPS.

To deploy an update after pushing changes:

```bash
git pull && docker compose up -d --build
```

**Verified working:** image builds at 77 MB, container reports `healthy`, the page renders
with all images, and excluded paths (`/uploads/…`, `/_build/…`, `/README.md`, the `.dc.html`
copy) correctly return 404.

### TLS — read before pointing a domain at this

**This container speaks plain HTTP only.** It has no certificate and no port 443. Putting
it straight on the internet at port 80 means an unencrypted site, a browser "Not secure"
warning, and — because the canonical URL and the OG tags all say `https://` — a mismatch
between what you advertise and what you serve.

Pick one before going live:

- **Caddy or Traefik in front**, in the same compose project. Caddy gets a Let's Encrypt
  certificate automatically from just a domain name and is the shortest path.
- **Cloudflare in front** with proxying enabled. TLS terminates at Cloudflare; the origin
  stays HTTP. Fastest to set up if the DNS is already there.
- **Host nginx or Caddy on the VPS** as a reverse proxy to `127.0.0.1:8080`, with certbot.
  Sensible if you will host more than this one site.

In every case, keep the container bound to a local port and let the proxy hold 80 and 443.

### What is in the image

Only what the site serves: `index.html`, `support.js`, `robots.txt`, `sitemap.xml` and
`assets/`. `.dockerignore` keeps `uploads/`, `_ds/`, `_build/`, `scraps/` and the docs out —
that is roughly 5 MB of design-process baggage.

`Snowbelt AI Automation.dc.html` is deliberately **not** in the image. It is byte-identical
to `index.html`, so serving both would publish the same page at two URLs and split its
search ranking.

Server behaviour, in `docker/nginx.conf`:

- `index.html` and `support.js` are `no-cache`, so a redeploy is visible immediately
- `assets/` is cached 7 days — not `immutable`, because filenames are not content-hashed
  and a long cache would strand visitors on a stale image after an update
- gzip on text; images are already compressed
- `nosniff`, `SAMEORIGIN`, `strict-origin-when-cross-origin`, and `server_tokens off`
- unknown paths 404 rather than falling back to `index.html` — this is one page with
  anchor navigation, not a client-side router, so a fallback would return 200 for URLs
  that do not exist and invite duplicate indexing

There is no Content-Security-Policy. The page is built from inline style attributes and an
inline script, so any CSP would need `'unsafe-inline'` for both and buy very little. See
the note in `docker/security-headers.conf`.

## Deploying to a static host instead

If you would rather skip Docker: upload `index.html`, `support.js`, `robots.txt`,
`sitemap.xml` and `assets/` to Netlify, Vercel, Cloudflare Pages, or any static host.
Fonts load from Google Fonts; nothing else is fetched. No build step.

`index.html` and `Snowbelt AI Automation.dc.html` are kept byte-identical — edit one and
copy it over the other, or the two will drift and the wrong one may ship.

`_build/` is tooling, not site content; it does not need to be uploaded. Neither does
`_ds/` — that folder is an unrelated "Organic" design system (cream, terracotta,
Caprasimo) that came along in the export and has nothing to do with this site.

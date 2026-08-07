# Static marketing site - no build step, so this is a single stage.
FROM nginx:1.27-alpine

# Replace the stock server block with ours.
RUN rm /etc/nginx/conf.d/default.conf \
 && mkdir -p /etc/nginx/snippets
COPY docker/nginx.conf              /etc/nginx/conf.d/site.conf
COPY docker/security-headers.conf   /etc/nginx/snippets/security-headers.conf

WORKDIR /usr/share/nginx/html

# Copy only what the site actually serves. "Snowbelt AI Automation.dc.html" is
# deliberately excluded: it is the Claude Design round-trip file and is kept
# byte-identical to index.html, so shipping it would serve the same page at a
# second URL and split its search ranking.
COPY index.html   ./
COPY support.js   ./
COPY robots.txt   ./
COPY sitemap.xml  ./
COPY assets/      ./assets/

# Legal pages. Directory-style URLs, so nginx's `index index.html` serves each
# one at /privacy-policy/ and /sms-terms/ without a redirect.
COPY privacy-policy/ ./privacy-policy/
COPY sms-terms/      ./sms-terms/

# Fail the container if nginx stops serving. busybox wget ships in the alpine
# image, so this needs no extra packages.
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://127.0.0.1/ || exit 1

EXPOSE 80

# nginx:alpine already sets the correct CMD and runs in the foreground.

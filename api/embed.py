from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)

        title = query.get("title", [""])[0]
        description = query.get("description", [""])[0]
        color = query.get("color", ["5865F2"])[0]
        image = query.get("image", [""])[0]
        thumbnail = query.get("thumbnail", [""])[0]
        url = query.get("url", [""])[0]
        author_name = query.get("author_name", [""])[0]
        author_url = query.get("author_url", [""])[0]
        author_icon = query.get("author_icon", [""])[0]
        footer_text = query.get("footer_text", [""])[0]
        footer_icon = query.get("footer_icon", [""])[0]
        timestamp = query.get("timestamp", [""])[0]
        provider_name = query.get("provider_name", [""])[0]
        provider_url = query.get("provider_url", ["https://google.com"])[0]

        # Discord unfurls this page by reading the og:*/twitter:* tags below -
        # it isn't a real embed object, so there's no native "author" or
        # "footer" slot the way a bot-sent embed has. author_name/footer_text/
        # timestamp are folded into the visible description text instead,
        # stacked the way a real embed visually lays them out (author line on
        # top, footer + timestamp on the bottom). author_icon has no OG/Twitter
        # tag that renders as a small icon distinct from the main image, so it
        # is accepted (for forward compatibility) but intentionally has no
        # visual effect here - that's a hard limitation of link-preview
        # embeds, not an oversight.
        composed_description = description
        if author_name:
            composed_description = f"{author_name}\n{composed_description}"
        footer_line = ""
        if footer_text and timestamp:
            footer_line = f"{footer_text} • {timestamp}"
        elif footer_text:
            footer_line = footer_text
        elif timestamp:
            footer_line = timestamp
        if footer_line:
            composed_description = f"{composed_description}\n\n{footer_line}"

        html = f"""
<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">

<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{composed_description}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image}">
<meta property="theme-color" content="#{color}">
<meta property="og:site_name" content="{provider_name}">

<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{composed_description}">
<meta name="twitter:image" content="{thumbnail or image}">

<title>{title}</title>

</head>
<body>

<script>
window.location.href = "{provider_url}";
</script>

</body>
</html>
"""

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

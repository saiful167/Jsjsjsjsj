import requests
import re
from urllib.parse import quote
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # URL param পড়া
        if "url=" not in self.path:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Missing url parameter')
            return

        tiktok_url = self.path.split("url=")[1]
        tiktok_url = tiktok_url.split("&")[0]

        ssstik_url = "https://ssstik.io/abc?url=dl"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "HX-Request": "true",
            "HX-Trigger": "_gcaptcha_pt",
            "HX-Target": "target",
            "HX-Current-URL": "https://ssstik.io/snaptik-tiktok-downloader-1",
            "User-Agent": "Mozilla/5.0"
        }

        data = f"id={quote(tiktok_url)}&locale=en"

        try:
            r = requests.post(ssstik_url, headers=headers, data=data, timeout=15)
            html = r.text

            # tikcdn.io direct link extract
            match = re.search(r'https://tikcdn\.io/ssstik/[^"]+', html)

            if not match:
                raise Exception("Download link not found")

            video_url = match.group(0)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps({
                "status": "success",
                "video": video_url
            }).encode())

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "error",
                "message": str(e)
            }).encode())

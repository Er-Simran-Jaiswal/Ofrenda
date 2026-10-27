#!/usr/bin/env python3
"""Ofrenda: a private, offline altar builder. Python stdlib + a local Ollama model."""
import json, os, urllib.request, webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

OLLAMA = os.environ.get("OLLAMA_URL", "http://localhost:11434")
MODEL = os.environ.get("OFRENDA_MODEL", "llama3.2")
PORT = int(os.environ.get("PORT", "8484"))
HERE = os.path.dirname(os.path.abspath(__file__))

SYSTEM = ("You help people write remembrances for loved ones who have died, in the spirit of "
          "Día de los Muertos. Be warm, specific and gentle. Use ONLY the details given; never invent "
          "facts, quotes or events. Never speak as the person who died.")

def ask_model(d):
    prompt = (f"Name: {d['name']}\nRelationship to me: {d['relation']}\n"
              f"Favorite foods: {d['foods']}\nFavorite songs: {d['songs']}\nA story I carry: {d['story']}\n\n"
              "Write two things separated by a line containing only ---\n"
              "1) A remembrance of 120-160 words, written by me, addressed to them, using the details.\n"
              "2) A playful four-line calaverita verse (rhyming, affectionate, never mocking).")
    body = json.dumps({"model": MODEL, "stream": False, "messages": [
        {"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(OLLAMA + "/api/chat", body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        text = json.load(r)["message"]["content"].strip()
    a, _, b = text.partition("---")
    return {"remembrance": a.strip(), "verse": b.strip()}

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _send(self, code, ctype, data):
        self.send_response(code); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)
    def do_GET(self):
        with open(os.path.join(HERE, "index.html"), "rb") as f:
            self._send(200, "text/html; charset=utf-8", f.read())
    def do_POST(self):
        try:
            d = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            out = ask_model({k: str(d.get(k, ""))[:1500] for k in ("name", "relation", "foods", "songs", "story")})
            self._send(200, "application/json", json.dumps(out).encode())
        except Exception as e:
            msg = f"Could not reach the local model ({MODEL}). Is Ollama running? Try: ollama pull {MODEL}. Details: {e}"
            self._send(500, "application/json", json.dumps({"error": msg}).encode())

if __name__ == "__main__":
    print(f"Ofrenda running at http://localhost:{PORT} using {MODEL} (nothing leaves this machine)")
    webbrowser.open(f"http://localhost:{PORT}")
    HTTPServer(("127.0.0.1", PORT), H).serve_forever()
from http.server import HTTPServer, BaseHTTPRequestHandler
import json


POSTS = [
    {"id": 1, "title": "Test Post", "body": "Hello World"},
    {"id": 2, "title": "Another Post", "body": "More content"},
]


class MockHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/posts":
            self._respond(200, POSTS)
        else:
            self._respond(404, {"error": "Not found"})

    def do_POST(self):
        if self.path == "/posts":
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length)
            try:
                data = json.loads(raw)
                print("Received data:", data)
            except Exception:
                data = {}
            new_post = {"id": len(POSTS) + 1, "title": data["title"], "body": data["body"]}
            POSTS.append(new_post)
            self._respond(201, new_post)
        else:
            self._respond(404, {"error": "Not found"})

    def _respond(self, status: int, body):
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format, *args):
        print(f"[mock] {self.address_string()} - {format % args}")


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8080), MockHandler)
    print("Mock server running on http://localhost:8080")
    server.serve_forever()

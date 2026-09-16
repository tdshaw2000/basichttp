import argparse
import functools
import http.server
import socketserver

class LegacyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def send_header(self, keyword, value):
        # Strip any "; charset=..." from Content-Type - old browsers like
        # Netscape 1.0 can't parse MIME parameters and treat the whole
        # string (e.g. "text/html; charset=utf-8") as an unknown file type.
        if keyword.lower() == "content-type" and ";" in value:
            value = value.split(";")[0].strip()
        super().send_header(keyword, value)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Minimal HTTP server for old browsers (strips charset from Content-Type)."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Root directory to serve (default: current directory)",
    )
    parser.add_argument(
        "-p", "--port", type=int, default=8080, help="Port to listen on (default: 8080)"
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    # functools.partial binds `directory` the same way http.server's own
    # --directory flag does, so relative file requests resolve against it
    # regardless of where this script was launched from.
    handler = functools.partial(LegacyHTTPRequestHandler, directory=args.directory)

    with socketserver.TCPServer(("", args.port), handler) as httpd:
        print(f"Serving {args.directory!r} on port {args.port} (charset stripped from Content-Type)")
        httpd.serve_forever()

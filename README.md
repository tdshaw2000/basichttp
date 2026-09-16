# basichttp

A minimal Python HTTP server for testing early-90s web browsers (e.g. Netscape 1.0 on Windows 3.1) against a real site.

Old browsers can't parse MIME parameters, so a `Content-Type` header like `text/html; charset=utf-8` gets treated as an unknown file type. This server strips the `; charset=...` suffix before sending headers, so responses come back as plain `text/html`, `image/gif`, etc.

## Usage

```
python3 basic_http_server.py [directory] [-p PORT]
```

- `directory` (optional): root directory to serve. Defaults to the current directory.
- `-p, --port` (optional): port to listen on. Defaults to `8080`.

Example, serving the included `site` directory on the default port:

```
python3 basic_http_server.py site
```

Then point the Win31 browser at `http://<host-ip>:8080/`.

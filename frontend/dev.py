import os
import pathlib
import http.server
import socketserver
import webbrowser
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Get the directory where the script is located
script_dir = pathlib.Path(__file__).parent.absolute()

# Note: PORT must be 8000 if you want to access the api at
# https://donations.effectivealtruism.org.au/partner_charities or
# https://donations.effectivealtruism.org.au/referral_sources
PORT = 8001


class BuildHandler(FileSystemEventHandler):
    """Handler for rebuilding the form when files change"""

    def on_modified(self, event):
        # Skip hidden files, dist directory, and non-relevant files
        if (
            event.is_directory
            or event.src_path.endswith(".py")
            or "/dist/" in event.src_path
            or "/.git/" in event.src_path
        ):
            return

        print(f"File changed: {event.src_path}. Rebuilding...")
        subprocess.run(["python", str(script_dir / "build.py")], check=True)
        print("Rebuild complete!")


def start_server():
    """Start the HTTP server"""
    print(f"Starting HTTP server at http://localhost:{PORT}")
    # Change to the script directory to ensure paths are correct
    os.chdir(script_dir)

    # Build the form first
    print("Building the donation form...")
    subprocess.run(["python", str(script_dir / "build.py")], check=True)

    # Set up file watcher for auto-rebuild
    event_handler = BuildHandler()
    observer = Observer()
    observer.schedule(event_handler, script_dir / "src", recursive=True)
    observer.start()

    # Create the HTTP server
    handler = http.server.SimpleHTTPRequestHandler
    os.chdir(script_dir / "dist")
    httpd = socketserver.TCPServer(("", PORT), handler)

    print(f"Server started at http://localhost:{PORT}/")
    print("Opening browser...")
    webbrowser.open(f"http://localhost:{PORT}/")

    try:
        print("Press Ctrl+C to stop the server")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server and file watcher...")
        observer.stop()

    observer.join()
    httpd.server_close()
    print("Server stopped.")


if __name__ == "__main__":
    start_server()

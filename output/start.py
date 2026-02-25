"""Start both backend and frontend in one command."""

import os
import signal
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT, "backend")
FRONTEND_DIR = os.path.join(ROOT, "frontend")

def main():
    # Validate API key
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(ROOT), ".env"))
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set. Add it to your .env file.")
        sys.exit(1)

    # Auto-install frontend deps if needed
    if not os.path.isdir(os.path.join(FRONTEND_DIR, "node_modules")):
        print("Installing frontend dependencies...")
        subprocess.run(["npm", "install"], cwd=FRONTEND_DIR, shell=True, check=True)

    print("Starting backend (port 7777) and frontend (port 5173)...")
    print("  Backend:  http://localhost:7777")
    print("  Frontend: http://localhost:5173")
    print("  API docs: http://localhost:7777/docs")
    print("  Press Ctrl+C to stop both.\n")

    backend = subprocess.Popen(
        [sys.executable, os.path.join(BACKEND_DIR, "serve.py")],
        cwd=BACKEND_DIR,
    )
    frontend = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=FRONTEND_DIR,
        shell=True,
    )

    try:
        backend.wait()
    except KeyboardInterrupt:
        pass
    finally:
        for proc in [backend, frontend]:
            try:
                proc.terminate()
                proc.wait(timeout=5)
            except Exception:
                proc.kill()


if __name__ == "__main__":
    main()

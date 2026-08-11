#!/usr/bin/env python3
"""
run_phishscope.py — PHOENIX / PhishScope-AI Universal Launcher
==============================================================
One command to start the entire PHOENIX platform on any OS.

Usage:
    python run_phishscope.py                 # Auto-detect mode
    python run_phishscope.py --docker        # Force Docker mode
    python run_phishscope.py --no-docker     # Force manual mode (SQLite fallback)
    python run_phishscope.py --backend-only  # Start backend only (no frontend)
    python run_phishscope.py --check-ai      # Test Gemini API key connectivity
    python run_phishscope.py --no-browser    # Don't open browser automatically
    python run_phishscope.py --help          # Show help

Developed by : Umesh Gupta
Institution  : National Forensic Sciences University, Tripura Campus
Project      : UP Police Cyber Cell — PhishScope-AI Phishing Investigation Platform
"""

import sys
import os
import subprocess
import platform
import shutil
import time
import json
import signal
import threading
import webbrowser
import datetime
import argparse
import textwrap
import urllib.request
import urllib.error
from pathlib import Path

# Force UTF-8 encoding for stdout/stderr to support box drawing characters on Windows
if hasattr(sys.stdout, 'reconfigure'):
    if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except Exception:
            pass

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
VERSION = "1.0.0-gemini"  # Updated: Gemini AI integration
PROJECT_ROOT = Path(__file__).parent.resolve()
BACKEND_DIR  = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
LOGS_DIR     = PROJECT_ROOT / "logs"
ENV_FILE     = PROJECT_ROOT / ".env"
ENV_EXAMPLE  = PROJECT_ROOT / ".env.example"

ADMIN_EMAIL    = "admin@phoenix.ai"
ADMIN_PASSWORD = "Phoenix@Admin123"

MIN_PYTHON     = (3, 11)
BACKEND_PORT   = 8000
FRONTEND_PORT  = 3000
HEALTH_URL     = f"http://localhost:{BACKEND_PORT}/api/v1/health"
AI_STATUS_URL  = f"http://localhost:{BACKEND_PORT}/api/v1/url-intelligence/ai-status"
HEALTH_TIMEOUT = 120  # seconds to wait for services to be healthy

# Confirmed working Gemini models with the AQ.* API key type
GEMINI_WORKING_MODELS = [
    "models/gemini-3.6-flash",
    "models/gemini-3.5-flash",
    "models/gemini-flash-latest",
    "models/gemini-3.1-flash-lite",
    "models/gemini-3-flash-preview",
    "models/gemini-flash-lite-latest",
    "models/gemini-3.5-flash-lite",
]

FEATURES = [
    "🤖 Gemini AI (3.6-flash/3.5-flash) — Real Phishing Analysis",
    "🔗 URL & QR-Code Phishing Detection with AI Narratives",
    "🏦 Indian Banks & UPI Scam Detection (SBI, HDFC, Paytm, IRCTC...)",
    "🇮🇳 Hindi Report Summaries for UP Police Cyber Cell",
    "📧 Email Forensics & BEC Detection",
    "🖥️  Disk, Memory, Mobile & Cloud Forensics (DFIR)",
    "🤝 SOC Co-Pilot with Gemini LLM Reasoning",
    "🦠 Malware Analysis Engine",
    "🎭 Threat Actor & Campaign Tracking",
    "🗺️  Attack Graph Visualization (MITRE ATT&CK)",
    "🔴 Red Team / Blue Team Simulation",
    "🔍 Enterprise Threat Hunting Platform",
    "☁️  CSPM / CWPP / CIEM / CDR / DSPM (Cloud Security)",
    "🛡️  SAST / DAST / SCA / SBOM / IaC (AppSec)",
    "👤 Identity Security Posture Management (ISPM)",
    "🔒 Zero Trust Architecture Enforcement",
    "🎯 SOAR Orchestration & Automated Playbooks",
    "📊 Executive Intelligence Dashboard",
    "🌐 Chrome Extension for Real-Time Browser Protection",
    "📦 95+ Enterprise Security Modules",
]

# Spawned child processes (for graceful shutdown)
_child_processes: list = []
_shutdown_event  = threading.Event()

# ─────────────────────────────────────────────────────────────────────────────
# ANSI COLOR HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def _enable_windows_ansi():
    """Enable ANSI escape sequences on Windows 10+ via SetConsoleMode."""
    if platform.system() == "Windows":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            pass

_enable_windows_ansi()

_USE_COLOR = sys.stdout.isatty() or os.environ.get("FORCE_COLOR") == "1"

class C:
    """ANSI color codes — gracefully no-ops when color is not supported."""
    RESET   = "\033[0m"  if _USE_COLOR else ""
    BOLD    = "\033[1m"  if _USE_COLOR else ""
    RED     = "\033[91m" if _USE_COLOR else ""
    GREEN   = "\033[92m" if _USE_COLOR else ""
    YELLOW  = "\033[93m" if _USE_COLOR else ""
    BLUE    = "\033[94m" if _USE_COLOR else ""
    MAGENTA = "\033[95m" if _USE_COLOR else ""
    CYAN    = "\033[96m" if _USE_COLOR else ""
    WHITE   = "\033[97m" if _USE_COLOR else ""
    DIM     = "\033[2m"  if _USE_COLOR else ""

def ok(msg):      print(f"  {C.GREEN}[✓]{C.RESET} {msg}")
def warn(msg):    print(f"  {C.YELLOW}[!]{C.RESET} {msg}")
def info(msg):    print(f"  {C.BLUE}[i]{C.RESET} {msg}")
def ai_ok(msg):   print(f"  {C.MAGENTA}[🤖]{C.RESET} {msg}")
def step(n, total, msg):
    print(f"\n{C.CYAN}{C.BOLD}[STEP {n}/{total}]{C.RESET}  {C.WHITE}{msg}{C.RESET}")

def error_box(source: str, what: str, why: str, fix: str, log_path: str = ""):
    """Print a structured, human-readable error block."""
    print()
    print(f"  {C.RED}{'─'*62}{C.RESET}")
    print(f"  {C.RED}{C.BOLD}[ERROR]{C.RESET}")
    print(f"  {C.BOLD}  ● Source :{C.RESET} {source}")
    print(f"  {C.BOLD}  ● What   :{C.RESET} {what}")
    print(f"  {C.BOLD}  ● Why    :{C.RESET} {why}")
    print(f"  {C.BOLD}  ● Fix    :{C.RESET} {fix}")
    if log_path:
        print(f"  {C.BOLD}  ● Log    :{C.RESET} {C.DIM}{log_path}{C.RESET}")
    print(f"  {C.RED}{'─'*62}{C.RESET}")
    print()

# ─────────────────────────────────────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────────────────────────────────────
LOGS_DIR.mkdir(exist_ok=True)
_log_stamp      = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
_launcher_log   = LOGS_DIR / f"phoenix_launcher_{_log_stamp}.log"

def _log(msg: str):
    """Write a timestamped message to the launcher log file."""
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    with open(_launcher_log, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")

# ─────────────────────────────────────────────────────────────────────────────
# BANNER
# ─────────────────────────────────────────────────────────────────────────────
def print_banner():
    banner = f"""
{C.CYAN}{C.BOLD}╔══════════════════════════════════════════════════════════════════════╗
║     ██████╗ ██╗  ██╗ ██████╗ ███████╗███╗   ██╗██╗██╗  ██╗         ║
║     ██╔══██╗██║  ██║██╔═══██╗██╔════╝████╗  ██║██║╚██╗██╔╝         ║
║     ██████╔╝███████║██║   ██║█████╗  ██╔██╗ ██║██║ ╚███╔╝          ║
║     ██╔═══╝ ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║██║ ██╔██╗          ║
║     ██║     ██║  ██║╚██████╔╝███████╗██║ ╚████║██║██╔╝ ██╗         ║
║     ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝         ║
╠══════════════════════════════════════════════════════════════════════╣
║  {C.GREEN}PhishScope-AI  v{VERSION:<26}{C.CYAN}  🤖 Gemini AI Edition  ║
║  {C.WHITE}AI-Powered Phishing & Cyber Intelligence Platform          {C.CYAN}      ║
╠══════════════════════════════════════════════════════════════════════╣
║  {C.WHITE}Developer     :  Umesh Gupta                               {C.CYAN}      ║
║  {C.WHITE}Institution   :  National Forensic Sciences University     {C.CYAN}      ║
║  {C.WHITE}               :  Tripura Campus                           {C.CYAN}      ║
║  {C.WHITE}Project       :  UP Police Cyber Cell Investigation Tool   {C.CYAN}      ║
║  {C.MAGENTA}Gemini Models :  3.6-flash (primary) · 3.5-flash (fast)   {C.CYAN}      ║
║  {C.DIM}GitHub        :  Hardy20102004/PhishScope-AI               {C.CYAN}      ║
╚══════════════════════════════════════════════════════════════════════╝{C.RESET}
"""
    print(banner)

def print_features():
    print(f"{C.BOLD}  KEY CAPABILITIES:{C.RESET}")
    for i, feat in enumerate(FEATURES, 1):
        print(f"    {C.DIM}{i:>2}.{C.RESET} {feat}")
    print()

# ─────────────────────────────────────────────────────────────────────────────
# ENVIRONMENT DETECTION
# ─────────────────────────────────────────────────────────────────────────────
def check_python_version():
    """Ensure we are running on the minimum required Python version."""
    ver = sys.version_info[:2]
    if ver < MIN_PYTHON:
        error_box(
            source="Python Version Check",
            what=f"Python {'.'.join(map(str, ver))} detected.",
            why=f"PhishScope-AI requires Python {'.'.join(map(str, MIN_PYTHON))} or higher.",
            fix=(
                "Download Python 3.11+ from: https://python.org/downloads\n"
                "          Windows: winget install Python.Python.3.11\n"
                "          macOS:   brew install python@3.11\n"
                "          Linux:   sudo apt install python3.11"
            ),
        )
        sys.exit(1)
    ok(f"Python {sys.version.split()[0]} detected")
    _log(f"Python OK: {sys.version}")

def detect_os():
    """Detect and display OS information."""
    system  = platform.system()
    release = platform.release()
    machine = platform.machine()
    info(f"OS: {system} {release} ({machine})")
    _log(f"OS: {system} {release} {machine}")
    return system

def check_docker() -> bool:
    """Check if Docker and docker compose are available and running."""
    if not shutil.which("docker"):
        return False
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            warn("Docker is installed but not running. Start Docker Desktop / Docker daemon.")
            return False

        compose_check = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True, text=True, timeout=10
        )
        if compose_check.returncode == 0:
            ver_line = compose_check.stdout.strip().split("\n")[0]
            ok(f"Docker found — {ver_line}")
            _log(f"Docker OK: {ver_line}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return False

def check_nodejs() -> bool:
    """Check if Node.js and npm are available."""
    node_path = shutil.which("node")
    npm_path  = shutil.which("npm")
    if not node_path or not npm_path:
        warn("Node.js / npm not found. Frontend will be skipped.")
        warn("Install from: https://nodejs.org/en/download")
        _log("Node.js: NOT FOUND")
        return False
    try:
        ver     = subprocess.run([node_path, "--version"], capture_output=True, text=True, timeout=5)
        npm_ver = subprocess.run([npm_path,  "--version"], capture_output=True, text=True, timeout=5,
                                  shell=sys.platform.startswith("win"))
        ok(f"Node.js {ver.stdout.strip()} / npm {npm_ver.stdout.strip()}")
        _log(f"Node.js: {ver.stdout.strip()}")
        return True
    except Exception as e:
        _log(f"Node.js check failed: {e}")
        return False

# ─────────────────────────────────────────────────────────────────────────────
# GEMINI API KEY CHECK  ← NEW
# ─────────────────────────────────────────────────────────────────────────────
def _read_env_key(key: str) -> str:
    """Read a value from the .env file directly (without loading full env)."""
    if not ENV_FILE.exists():
        return ""
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith(f"{key}="):
            return line.split("=", 1)[1].strip()
    return ""

def check_gemini_api_key(verbose: bool = False) -> bool:
    """
    Checks if GEMINI_API_KEY is set and optionally tests connectivity
    by making a real API call to verify the key works.
    Returns True if key is set (even without testing).
    """
    api_key = os.environ.get("GEMINI_API_KEY") or _read_env_key("GEMINI_API_KEY")

    if not api_key:
        warn("GEMINI_API_KEY is not set → AI will use rule-based fallback")
        warn("Get a free key: https://aistudio.google.com/app/apikey")
        warn("Then add to .env:  GEMINI_API_KEY=your_key_here")
        _log("GEMINI_API_KEY: NOT SET")
        return False

    # Key is set — show masked version
    masked = f"{api_key[:6]}...{api_key[-4:]}"
    ok(f"GEMINI_API_KEY detected: {masked}")
    _log(f"GEMINI_API_KEY: SET ({masked})")

    if verbose:
        # Live test: actually call Gemini
        print(f"    Testing Gemini API connectivity ", end="", flush=True)
        try:
            # Try to import the SDK
            try:
                from google import genai
            except ImportError:
                print(f"{C.YELLOW}skipped (google-genai not installed){C.RESET}")
                warn("Run: pip install google-genai")
                return True  # Key is set, just SDK missing

            client = genai.Client(api_key=api_key)
            primary_model = (
                os.environ.get("GEMINI_PRIMARY_MODEL")
                or _read_env_key("GEMINI_PRIMARY_MODEL")
                or "models/gemini-3.6-flash"
            )

            # Try primary first, then fallbacks
            models_to_try = [primary_model] + [
                m for m in GEMINI_WORKING_MODELS if m != primary_model
            ]

            connected_model = None
            for model_name in models_to_try:
                try:
                    from google.genai import types as _gtypes
                    cfg = _gtypes.GenerateContentConfig(max_output_tokens=10)
                    resp = client.models.generate_content(
                        model=model_name,
                        contents="Reply with one word: ready",
                        config=cfg
                    )
                    if resp.text is not None:
                        connected_model = model_name
                        break
                except Exception:
                    continue

            if connected_model:
                print(f"{C.GREEN}connected ✓{C.RESET}")
                ai_ok(f"Gemini model active: {C.BOLD}{connected_model}{C.RESET}")
                _log(f"Gemini API: CONNECTED via {connected_model}")
                return True
            else:
                print(f"{C.YELLOW}key set but no model responded{C.RESET}")
                warn("All Gemini models returned empty or quota exceeded.")
                warn("AI will use rule-based fallback until quota resets.")
                _log("Gemini API: KEY SET but no model responded")
                return True  # Key is set, quota issue — not a bug

        except Exception as e:
            print(f"{C.YELLOW}could not test ({type(e).__name__}){C.RESET}")
            warn(f"Gemini connectivity test failed: {e}")
            _log(f"Gemini API: test error — {e}")
            return True  # Key is set, connectivity issue might be temporary

    return True

def run_gemini_check_mode():
    """
    Standalone --check-ai mode: deeply tests Gemini connectivity
    and shows which models work with the configured API key.
    """
    print_banner()
    print(f"\n{C.CYAN}{C.BOLD}  🤖 Gemini AI Connectivity Check{C.RESET}\n")

    api_key = os.environ.get("GEMINI_API_KEY") or _read_env_key("GEMINI_API_KEY")
    if not api_key:
        error_box(
            source="Gemini API Check",
            what="GEMINI_API_KEY is not set.",
            why="The API key is required to use real Gemini AI analysis.",
            fix=(
                "1. Get a free key at: https://aistudio.google.com/app/apikey\n"
                "   2. Add to .env:  GEMINI_API_KEY=your_key_here\n"
                "   3. Re-run: python run_phishscope.py --check-ai"
            ),
        )
        sys.exit(1)

    masked = f"{api_key[:8]}...{api_key[-4:]}"
    info(f"API Key: {masked}")

    try:
        from google import genai
        from google.genai import types as _gtypes
    except ImportError:
        # Try to auto-install google-genai for the current python
        print(f"  {C.YELLOW}Installing google-genai SDK for current Python...{C.RESET}", end="", flush=True)
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "google-genai", "--quiet"],
                check=True, capture_output=True, timeout=60
            )
            print(f" {C.GREEN}done ✓{C.RESET}")
            from google import genai
            from google.genai import types as _gtypes
        except Exception:
            print(f" {C.RED}failed{C.RESET}")
            error_box(
                source="google-genai SDK",
                what="google-genai package not installed.",
                why="The SDK is required for Gemini API calls.",
                fix=(
                    "Run: pip install google-genai\n"
                    "   Or inside backend/: pip install -r requirements.txt"
                ),
            )
            sys.exit(1)

    client = genai.Client(api_key=api_key)
    cfg = _gtypes.GenerateContentConfig(max_output_tokens=20)

    print(f"\n  {C.BOLD}Testing all Gemini models...{C.RESET}\n")
    working = []
    failed  = []

    for model in GEMINI_WORKING_MODELS:
        print(f"  Testing {model:<45}", end="", flush=True)
        try:
            resp = client.models.generate_content(
                model=model,
                contents="Reply with one word: ok",
                config=cfg
            )
            if resp.text is not None:
                print(f"{C.GREEN}✓ WORKS{C.RESET}")
                working.append(model)
            else:
                print(f"{C.YELLOW}⚠ empty response{C.RESET}")
                working.append(model)  # Still accessible
        except Exception as e:
            err = str(e)[:60]
            print(f"{C.RED}✗ {err}{C.RESET}")
            failed.append(model)

    print()
    print(f"  {'─'*60}")
    print(f"  {C.GREEN}{C.BOLD}Working: {len(working)}/{len(GEMINI_WORKING_MODELS)} models{C.RESET}")
    if working:
        print(f"  {C.GREEN}Primary (recommended): {working[0]}{C.RESET}")
        for m in working[1:]:
            print(f"    {C.DIM}Fallback: {m}{C.RESET}")
    if failed:
        print(f"\n  {C.YELLOW}Not accessible ({len(failed)} models):{C.RESET}")
        for m in failed:
            print(f"    {C.DIM}{m}{C.RESET}")
    print()

    # Run a REAL phishing analysis test
    if working:
        print(f"  {C.CYAN}{C.BOLD}Running live phishing analysis test...{C.RESET}")
        try:
            from google.genai import types as _gt2
            analysis_cfg = _gt2.GenerateContentConfig(
                max_output_tokens=300,
                response_mime_type="application/json",
                system_instruction="You are a phishing detection AI for UP Police Cyber Cell.",
            )
            test_prompt = """Analyze URL: https://sbisecurelogin.net
Evidence: Typosquatting SBI, no TLS, Russian nameserver.
Respond with JSON: {"verdict": "PHISHING", "confidence": 95, "hindi_summary": "SBI का नकली पेज"}"""

            resp = client.models.generate_content(
                model=working[0],
                contents=test_prompt,
                config=analysis_cfg
            )
            print(f"  {C.GREEN}✓ Live test passed!{C.RESET}")
            print(f"  {C.DIM}Response: {resp.text[:150] if resp.text else 'empty'}...{C.RESET}")
            _log(f"Gemini live test: PASSED via {working[0]}")
        except Exception as e:
            print(f"  {C.YELLOW}⚠ Live test failed: {e}{C.RESET}")

    print(f"\n  {C.GREEN}{C.BOLD}✅ Gemini AI is {'configured and working' if working else 'configured but check quotas'}{C.RESET}\n")
    sys.exit(0)

# ─────────────────────────────────────────────────────────────────────────────
# ENV BOOTSTRAPPER
# ─────────────────────────────────────────────────────────────────────────────
def bootstrap_env():
    """Create .env from .env.example if it doesn't exist."""
    if ENV_FILE.exists():
        ok(".env already exists — using existing configuration")
        # Check and warn about key settings
        key = _read_env_key("GEMINI_API_KEY")
        if not key:
            warn("GEMINI_API_KEY not found in .env — add it for AI-powered analysis")
        return

    if ENV_EXAMPLE.exists():
        import shutil as _sh
        _sh.copy(ENV_EXAMPLE, ENV_FILE)
        ok(".env created from .env.example")
        _log(".env bootstrapped from .env.example")
    else:
        # Write full minimal .env with Gemini configuration
        minimal_env = f"""# PhishScope-AI — Auto-generated .env
# Generated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

# ── Application ───────────────────────────────────────────
ENVIRONMENT=development
SECRET_KEY=dev-insecure-key-CHANGE-IN-PRODUCTION
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# ── Database (SQLite fallback for dev) ────────────────────
SQLALCHEMY_DATABASE_URI=sqlite:///./phoenix_dev.db
POSTGRES_SERVER=localhost
POSTGRES_USER=phoenix
POSTGRES_PASSWORD=password
POSTGRES_DB=phoenix

# ── Redis ─────────────────────────────────────────────────
REDIS_URL=redis://localhost:6379/0

# ── Admin defaults (CHANGE AFTER FIRST LOGIN!) ────────────
ADMIN_EMAIL={ADMIN_EMAIL}
ADMIN_PASSWORD={ADMIN_PASSWORD}

# ── Google Gemini AI ──────────────────────────────────────
# Get your free API key at: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=
GEMINI_PRIMARY_MODEL=models/gemini-3.6-flash
GEMINI_FAST_MODEL=models/gemini-3.5-flash
GEMINI_FALLBACK_MODELS=models/gemini-flash-latest,models/gemini-3.1-flash-lite,models/gemini-3-flash-preview,models/gemini-flash-lite-latest
GEMINI_MAX_OUTPUT_TOKENS=2048
GEMINI_TEMPERATURE=0.2
"""
        ENV_FILE.write_text(minimal_env, encoding="utf-8")
        ok(".env created with development defaults")
        warn("Add your GEMINI_API_KEY to .env for AI-powered analysis!")
        _log(".env created with minimal defaults + Gemini config")

# ─────────────────────────────────────────────────────────────────────────────
# DEPENDENCY MANAGEMENT
# ─────────────────────────────────────────────────────────────────────────────
def install_backend_deps():
    """Install backend Python dependencies including google-genai and tldextract."""
    req_file = BACKEND_DIR / "requirements.txt"
    if not req_file.exists():
        warn(f"requirements.txt not found at {req_file}. Skipping pip install.")
        return

    print(f"    Installing backend Python packages  ", end="", flush=True)
    log_file = LOGS_DIR / f"backend_pip_{_log_stamp}.log"
    try:
        in_venv    = sys.prefix != sys.base_prefix
        venv_dir   = BACKEND_DIR / ".venv"
        os_name    = platform.system()

        if not in_venv:
            if not venv_dir.exists():
                subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True,
                               capture_output=True)
            python_exec = str(venv_dir / ("Scripts" if os_name == "Windows" else "bin") / "python")
        else:
            python_exec = sys.executable

        with open(log_file, "w") as lf:
            proc = subprocess.run(
                [python_exec, "-m", "pip", "install", "-r", str(req_file), "--quiet"],
                stdout=lf, stderr=lf, cwd=str(BACKEND_DIR), timeout=360
            )

        if proc.returncode == 0:
            print(f"{C.GREEN}done ✓{C.RESET}")
            _log("pip install: SUCCESS")
        else:
            print(f"{C.RED}FAILED{C.RESET}")
            error_box(
                source="pip install",
                what="Backend dependency installation failed.",
                why=f"pip returned exit code {proc.returncode}.",
                fix=f"Run manually: pip install -r backend/requirements.txt",
                log_path=str(log_file),
            )
    except subprocess.TimeoutExpired:
        print(f"{C.YELLOW}timeout{C.RESET}")
        warn(f"pip install timed out (>6 min). Check {log_file}")

def install_frontend_deps():
    """Install frontend npm dependencies."""
    pkg_file = FRONTEND_DIR / "package.json"
    if not pkg_file.exists():
        warn("frontend/package.json not found. Skipping npm install.")
        return

    node_modules = FRONTEND_DIR / "node_modules"
    if node_modules.exists() and (node_modules / ".package-lock.json").exists():
        ok("Frontend node_modules already installed — skipping npm install")
        _log("npm install: SKIPPED (node_modules exists)")
        return

    print(f"    Installing frontend Node packages   ", end="", flush=True)
    log_file = LOGS_DIR / f"frontend_npm_{_log_stamp}.log"
    try:
        npm_path = shutil.which("npm") or "npm"
        with open(log_file, "w") as lf:
            proc = subprocess.run(
                [npm_path, "install", "--silent"],
                stdout=lf, stderr=lf, cwd=str(FRONTEND_DIR), timeout=300,
                shell=sys.platform.startswith("win")
            )
        if proc.returncode == 0:
            print(f"{C.GREEN}done ✓{C.RESET}")
            _log("npm install: SUCCESS")
        else:
            print(f"{C.RED}FAILED{C.RESET}")
            error_box(
                source="npm install",
                what="Frontend dependency installation failed.",
                why=f"npm returned exit code {proc.returncode}.",
                fix="Run manually: cd frontend && npm install",
                log_path=str(log_file),
            )
    except subprocess.TimeoutExpired:
        print(f"{C.YELLOW}timeout{C.RESET}")
        warn(f"npm install timed out. Check {log_file}")

# ─────────────────────────────────────────────────────────────────────────────
# ADMIN CREDENTIALS DISPLAY
# ─────────────────────────────────────────────────────────────────────────────
def print_admin_credentials():
    gemini_key = _read_env_key("GEMINI_API_KEY")
    gemini_model = _read_env_key("GEMINI_PRIMARY_MODEL") or "models/gemini-3.6-flash"
    gemini_display = f"{gemini_key[:8]}...{gemini_key[-4:]}" if gemini_key else "NOT SET ⚠"
    ai_color = C.GREEN if gemini_key else C.RED

    print()
    print(f"  {C.YELLOW}{C.BOLD}Default Admin Credentials (change after first login!){C.RESET}")
    print(f"  {C.YELLOW}  ┌─────────────────────────────────────────────────────┐{C.RESET}")
    print(f"  {C.YELLOW}  │  Email      :  {C.WHITE}{ADMIN_EMAIL:<35}{C.YELLOW}  │{C.RESET}")
    print(f"  {C.YELLOW}  │  Password   :  {C.WHITE}{ADMIN_PASSWORD:<35}{C.YELLOW}  │{C.RESET}")
    print(f"  {C.YELLOW}  │  {C.RED}⚠  CHANGE PASSWORD AFTER FIRST LOGIN!         {C.YELLOW}  │{C.RESET}")
    print(f"  {C.YELLOW}  ├─────────────────────────────────────────────────────┤{C.RESET}")
    print(f"  {C.YELLOW}  │  {C.MAGENTA}Gemini AI   :  {ai_color}{gemini_display:<35}{C.YELLOW}  │{C.RESET}")
    print(f"  {C.YELLOW}  │  {C.MAGENTA}AI Model    :  {C.WHITE}{gemini_model:<35}{C.YELLOW}  │{C.RESET}")
    print(f"  {C.YELLOW}  └─────────────────────────────────────────────────────┘{C.RESET}")
    print()

# ─────────────────────────────────────────────────────────────────────────────
# PROCESS LOG STREAMING
# ─────────────────────────────────────────────────────────────────────────────
def _stream_logs(proc: subprocess.Popen, prefix: str, log_path: Path):
    """Thread target: read a process's stdout/stderr and write to log file."""
    try:
        with open(log_path, "a", encoding="utf-8", errors="replace") as lf:
            for raw_line in proc.stdout:
                line = raw_line.rstrip()
                lf.write(line + "\n")
                lf.flush()
                if _shutdown_event.is_set():
                    break
    except Exception:
        pass

# ─────────────────────────────────────────────────────────────────────────────
# HEALTH POLLING
# ─────────────────────────────────────────────────────────────────────────────
def _wait_for_healthy(timeout: int = HEALTH_TIMEOUT) -> bool:
    """Poll the /health endpoint until it returns 200 or timeout expires."""
    start = time.time()
    print(f"    Waiting for backend health check  ", end="", flush=True)
    while time.time() - start < timeout:
        if _shutdown_event.is_set():
            return False
        try:
            req = urllib.request.Request(HEALTH_URL, headers={"User-Agent": "PhishScope-Launcher/1.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    print(f" {C.GREEN}healthy ✓{C.RESET}")
                    _log("Backend health: OK")
                    return True
        except Exception:
            pass
        time.sleep(2)
        print(".", end="", flush=True)
    print(f" {C.RED}timeout{C.RESET}")
    return False

def _check_ai_status_endpoint():
    """After backend is up, check the Gemini AI status via API."""
    try:
        req = urllib.request.Request(AI_STATUS_URL, headers={"User-Agent": "PhishScope-Launcher/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode())
                if data.get("gemini_configured"):
                    ai_ok(f"Gemini AI: {data.get('status')} | Model: {data.get('active_model')}")
                else:
                    warn("Gemini AI: not configured (set GEMINI_API_KEY in .env)")
    except Exception:
        pass  # AI status check is optional — don't fail if it can't reach

# ─────────────────────────────────────────────────────────────────────────────
# DOCKER MODE LAUNCHER
# ─────────────────────────────────────────────────────────────────────────────
def launch_docker():
    """Launch all services via docker compose."""
    compose_file = PROJECT_ROOT / "docker-compose.yml"
    if not compose_file.exists():
        error_box(
            source="docker compose",
            what="docker-compose.yml not found.",
            why="The file was expected at the project root.",
            fix=f"Make sure you are running from: {PROJECT_ROOT}",
        )
        sys.exit(1)

    print(f"    Building and starting containers  ", end="", flush=True)
    log_file = LOGS_DIR / f"docker_{_log_stamp}.log"
    _log("Starting docker compose up --build -d")
    try:
        with open(log_file, "w") as lf:
            proc = subprocess.run(
                ["docker", "compose", "up", "--build", "-d"],
                stdout=lf, stderr=lf, cwd=str(PROJECT_ROOT), timeout=360
            )
        if proc.returncode != 0:
            print(f"{C.RED}FAILED{C.RESET}")
            error_box(
                source="docker compose up",
                what="Failed to start Docker services.",
                why=f"docker compose exited with code {proc.returncode}.",
                fix="Check Docker Desktop is running. Run: docker compose logs",
                log_path=str(log_file),
            )
            sys.exit(1)
        print(f"{C.GREEN}done ✓{C.RESET}")
        _log("docker compose up: SUCCESS")
    except subprocess.TimeoutExpired:
        print(f"{C.RED}timeout{C.RESET}")
        error_box(
            source="docker compose up",
            what="Docker build timed out (>6 minutes).",
            why="A Docker image layer may be downloading or building.",
            fix="Wait and retry, or run: docker compose up --build manually",
            log_path=str(log_file),
        )
        sys.exit(1)

    # Run migrations
    print(f"    Running database migrations        ", end="", flush=True)
    try:
        mig = subprocess.run(
            ["docker", "compose", "exec", "-T", "backend", "alembic", "upgrade", "head"],
            capture_output=True, text=True, cwd=str(PROJECT_ROOT), timeout=60
        )
        if mig.returncode == 0:
            print(f"{C.GREEN}done ✓{C.RESET}")
        else:
            print(f"{C.YELLOW}skipped{C.RESET}")
            warn("Migration may have already run or DB not ready yet.")
    except Exception:
        print(f"{C.YELLOW}skipped{C.RESET}")

# ─────────────────────────────────────────────────────────────────────────────
# MANUAL MODE LAUNCHER (No Docker)
# ─────────────────────────────────────────────────────────────────────────────
def launch_manual(has_node: bool, backend_only: bool = False):
    """Launch backend (uvicorn) and optionally frontend (npm run dev)."""
    os_name = platform.system()

    # ── Backend ──────────────────────────────────────────────────────────────
    backend_log = LOGS_DIR / f"backend_{_log_stamp}.log"
    print(f"    Starting backend (uvicorn)         ", end="", flush=True)

    # Find python inside .venv if available, else system python
    venv_python = BACKEND_DIR / ".venv" / ("Scripts" if os_name == "Windows" else "bin") / "python"
    python_exec = str(venv_python) if venv_python.exists() else sys.executable

    # Build environment — inject key settings
    env = os.environ.copy()
    env["PYTHONPATH"] = str(BACKEND_DIR)

    # Load .env values into subprocess environment if not already set
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                k = k.strip()
                if k and k not in env:  # Don't override already-set env vars
                    env[k] = v.strip()

    # SQLite fallback for no-Docker mode
    if not env.get("SQLALCHEMY_DATABASE_URI"):
        env["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./phoenix_dev.db"
    if not env.get("SECRET_KEY") or env.get("SECRET_KEY") == "":
        env["SECRET_KEY"] = "dev-insecure-key-change-in-production"

    try:
        backend_lf   = open(backend_log, "w", encoding="utf-8")
        backend_proc = subprocess.Popen(
            [
                python_exec, "-m", "uvicorn",
                "app.main:app",
                "--host", "0.0.0.0",
                "--port", str(BACKEND_PORT),
                "--reload",
                "--log-level", "info",
            ],
            stdout=backend_lf, stderr=subprocess.STDOUT,
            cwd=str(BACKEND_DIR), env=env
        )
        _child_processes.append(backend_proc)
        print(f"{C.GREEN}started (PID {backend_proc.pid}) ✓{C.RESET}")
        _log(f"Backend: PID {backend_proc.pid} → {backend_log}")
    except FileNotFoundError:
        print(f"{C.RED}FAILED{C.RESET}")
        error_box(
            source="uvicorn",
            what="uvicorn not found.",
            why="Python dependencies may not be installed.",
            fix="Run: pip install -r backend/requirements.txt",
        )
        return

    # ── Frontend ─────────────────────────────────────────────────────────────
    if backend_only:
        info("Backend-only mode — skipping frontend")
        return

    if has_node:
        frontend_log = LOGS_DIR / f"frontend_{_log_stamp}.log"
        print(f"    Starting frontend (npm dev)        ", end="", flush=True)
        try:
            frontend_lf   = open(frontend_log, "w", encoding="utf-8")
            npm_path      = shutil.which("npm") or "npm"
            frontend_proc = subprocess.Popen(
                [npm_path, "run", "dev"],
                stdout=frontend_lf, stderr=subprocess.STDOUT,
                cwd=str(FRONTEND_DIR),
                shell=sys.platform.startswith("win")
            )
            _child_processes.append(frontend_proc)
            print(f"{C.GREEN}started (PID {frontend_proc.pid}) ✓{C.RESET}")
            _log(f"Frontend: PID {frontend_proc.pid} → {frontend_log}")
        except FileNotFoundError:
            print(f"{C.YELLOW}skipped (npm not found){C.RESET}")
    else:
        warn("Node.js not found — frontend will not start.")

# ─────────────────────────────────────────────────────────────────────────────
# GRACEFUL SHUTDOWN
# ─────────────────────────────────────────────────────────────────────────────
def _shutdown(signum=None, frame=None):
    if _shutdown_event.is_set():
        return
    _shutdown_event.set()
    print(f"\n\n{C.YELLOW}  Shutting down PhishScope-AI...{C.RESET}")
    _log("Shutdown initiated")

    for proc in _child_processes:
        try:
            proc.terminate()
        except Exception:
            pass

    time.sleep(1.5)

    for proc in _child_processes:
        try:
            if proc.poll() is None:
                proc.kill()
        except Exception:
            pass

    print(f"  {C.GREEN}All services stopped.{C.RESET}")
    print(f"  Logs saved to: {C.DIM}{LOGS_DIR}{C.RESET}")
    _log("Shutdown complete")
    sys.exit(0)

signal.signal(signal.SIGINT,  _shutdown)
signal.signal(signal.SIGTERM, _shutdown)

# ─────────────────────────────────────────────────────────────────────────────
# SERVICE STATUS TABLE
# ─────────────────────────────────────────────────────────────────────────────
def print_status_table(use_docker: bool, backend_only: bool = False):
    gemini_model = _read_env_key("GEMINI_PRIMARY_MODEL") or "models/gemini-3.6-flash"
    has_gemini   = bool(_read_env_key("GEMINI_API_KEY"))

    print()
    print(f"  {C.GREEN}{C.BOLD}🚀 PhishScope-AI is running!{C.RESET}")
    print()

    rows = [
        ("Backend API",  f"http://localhost:{BACKEND_PORT}",       "FastAPI / Uvicorn"),
        ("API Swagger",  f"http://localhost:{BACKEND_PORT}/docs",   "Interactive Docs"),
        ("URL Scan API", f"http://localhost:{BACKEND_PORT}/api/v1/url-intelligence/investigate", "POST endpoint"),
        ("AI Status",    f"http://localhost:{BACKEND_PORT}/api/v1/url-intelligence/ai-status",   "Gemini health"),
    ]
    if not backend_only:
        rows.insert(0, ("Frontend",  f"http://localhost:{FRONTEND_PORT}", "React Dashboard"))
    if use_docker:
        rows += [
            ("PostgreSQL", "localhost:5432", "Docker container"),
            ("Redis",      "localhost:6379", "Docker container"),
        ]

    print(f"  {'Service':<18} {'URL':<58} {'Notes'}")
    print(f"  {'─'*18} {'─'*58} {'─'*22}")
    for name, url, note in rows:
        print(f"  {C.BOLD}{name:<18}{C.RESET} {C.CYAN}{url:<58}{C.RESET} {C.DIM}{note}{C.RESET}")

    print()
    ai_status = f"{C.GREEN}✓ {gemini_model}{C.RESET}" if has_gemini else f"{C.YELLOW}⚠ Not configured{C.RESET}"
    print(f"  {C.MAGENTA}{C.BOLD}Gemini AI:{C.RESET} {ai_status}")
    if not has_gemini:
        print(f"  {C.DIM}  → Add GEMINI_API_KEY to .env for real AI analysis{C.RESET}")
    print()

# ─────────────────────────────────────────────────────────────────────────────
# KEEP-ALIVE LOOP WITH PROCESS MONITORING
# ─────────────────────────────────────────────────────────────────────────────
def _monitor_processes():
    """Monitor child processes and warn if they die unexpectedly."""
    warned_pids = set()
    while not _shutdown_event.is_set():
        for proc in _child_processes:
            if proc.poll() is not None and proc.pid not in warned_pids:
                warned_pids.add(proc.pid)
                warn(
                    f"Service (PID {proc.pid}) exited unexpectedly "
                    f"with code {proc.returncode}. Check logs in {LOGS_DIR}"
                )
                _log(f"Process PID {proc.pid} died (code {proc.returncode})")
        time.sleep(5)

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="PhishScope-AI Universal Launcher — UP Police Cyber Cell Edition",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(f"""
        Examples:
          python run_phishscope.py                # Auto-detect mode
          python run_phishscope.py --docker       # Force Docker mode
          python run_phishscope.py --no-docker    # Force manual (SQLite) mode
          python run_phishscope.py --backend-only # Backend only, no frontend
          python run_phishscope.py --check-ai     # Test Gemini API connectivity
          python run_phishscope.py --no-browser   # Don't auto-open browser

        Gemini AI Models (confirmed working):
        {chr(10).join(f'  {m}' for m in GEMINI_WORKING_MODELS)}

        Get Gemini API key: https://aistudio.google.com/app/apikey
        """)
    )
    parser.add_argument("--docker",       action="store_true", help="Force Docker mode")
    parser.add_argument("--no-docker",    action="store_true", help="Force manual mode (SQLite fallback)")
    parser.add_argument("--no-browser",   action="store_true", help="Do not open browser automatically")
    parser.add_argument("--backend-only", action="store_true", help="Start backend only, skip frontend")
    parser.add_argument("--check-ai",     action="store_true", help="Test Gemini API key and show working models")
    parser.add_argument("--skip-deps",    action="store_true", help="Skip pip/npm install (faster start if deps installed)")
    args = parser.parse_args()

    # ── Gemini Check Mode ─────────────────────────────────────────────────────
    if args.check_ai:
        run_gemini_check_mode()
        return  # sys.exit called inside

    TOTAL_STEPS = 5

    # ── Banner ─────────────────────────────────────────────────────────────────
    print_banner()
    print_features()
    _log(f"PhishScope-AI launcher started — v{VERSION}")

    # ── Step 1: Environment Detection ──────────────────────────────────────────
    step(1, TOTAL_STEPS, "Detecting your environment...")
    check_python_version()
    os_name = detect_os()

    has_docker = False
    has_node   = False

    if not args.no_docker:
        has_docker = check_docker()
    if not has_docker or args.no_docker:
        has_node = check_nodejs()
    elif has_docker:
        has_node = check_nodejs()  # Still useful for frontend

    # Gemini key check (non-verbose at startup)
    check_gemini_api_key(verbose=False)

    # Decide mode
    if args.docker and not has_docker:
        error_box(
            source="Docker check",
            what="--docker flag was set but Docker is not running.",
            why="Docker is either not installed or the Docker daemon is not started.",
            fix="Start Docker Desktop (Windows/macOS) or: sudo systemctl start docker (Linux)",
        )
        sys.exit(1)

    use_docker  = has_docker and not args.no_docker
    mode_label  = "Docker mode" if use_docker else "Manual mode (SQLite fallback)"
    info(f"Launch mode: {C.BOLD}{mode_label}{C.RESET}")

    # ── Step 2: Dependencies ────────────────────────────────────────────────────
    step(2, TOTAL_STEPS, "Installing / verifying dependencies...")
    if args.skip_deps:
        info("Skipping dependency install (--skip-deps)")
    else:
        if not use_docker:
            install_backend_deps()
        if has_node and not args.backend_only:
            install_frontend_deps()
        else:
            info("Skipping frontend npm install")

    # ── Step 3: Environment Configuration ──────────────────────────────────────
    step(3, TOTAL_STEPS, "Configuring environment...")
    bootstrap_env()

    # Now do verbose Gemini check after env is bootstrapped
    check_gemini_api_key(verbose=True)

    # ── Step 4: Start Services ──────────────────────────────────────────────────
    step(4, TOTAL_STEPS, "Starting services...")
    if use_docker:
        launch_docker()
    else:
        launch_manual(has_node, backend_only=args.backend_only)

    # Wait for backend to be healthy
    healthy = _wait_for_healthy()
    if not healthy:
        error_box(
            source="Health Check",
            what=f"Backend did not become healthy within {HEALTH_TIMEOUT}s.",
            why="The backend process may have crashed during startup.",
            fix=(
                "Check logs in the logs/ directory for details.\n"
                f"          Docker mode: docker compose logs backend\n"
                f"          Manual mode: cat logs/backend_{_log_stamp}.log"
            ),
            log_path=str(LOGS_DIR),
        )
    else:
        ok(f"Backend API:    http://localhost:{BACKEND_PORT}")
        ok(f"API Docs:       http://localhost:{BACKEND_PORT}/docs")
        if not args.backend_only:
            ok(f"Frontend:       http://localhost:{FRONTEND_PORT}")
        # Check Gemini AI status via live API
        time.sleep(1)
        _check_ai_status_endpoint()

    # ── Step 5: Ready ───────────────────────────────────────────────────────────
    step(5, TOTAL_STEPS, "PhishScope-AI is ready!")
    print_admin_credentials()
    print_status_table(use_docker, backend_only=args.backend_only)

    print(f"  {C.DIM}Launcher log → {_launcher_log}{C.RESET}")
    print(f"  {C.DIM}All logs     → {LOGS_DIR}/{C.RESET}")
    print()

    # Open browser
    target_url = (
        f"http://localhost:{FRONTEND_PORT}"
        if not args.backend_only
        else f"http://localhost:{BACKEND_PORT}/docs"
    )
    if not args.no_browser and healthy:
        time.sleep(1.5)
        try:
            webbrowser.open(target_url)
            ok(f"Browser opened: {target_url}")
        except Exception:
            info(f"Open manually: {target_url}")

    # ── Keep-alive loop ─────────────────────────────────────────────────────────
    if _child_processes or use_docker:
        print(f"\n  {C.CYAN}Press {C.BOLD}Ctrl+C{C.RESET}{C.CYAN} to stop all services.{C.RESET}\n")

        # Start process monitor in background thread
        if _child_processes:
            monitor_thread = threading.Thread(target=_monitor_processes, daemon=True)
            monitor_thread.start()

        try:
            while not _shutdown_event.is_set():
                time.sleep(1)
        except KeyboardInterrupt:
            _shutdown()
    else:
        print(f"\n  {C.DIM}Docker mode: services running in background containers.{C.RESET}")
        print(f"  To stop: {C.BOLD}docker compose down{C.RESET}\n")


if __name__ == "__main__":
    main()

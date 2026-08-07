#!/usr/bin/env python3
"""
run_phishscope.py — PHOENIX / PhishScope-AI Universal Launcher
==============================================================
One command to start the entire PHOENIX platform on any OS.

Usage:
    python run_phishscope.py              # Auto-detect mode
    python run_phishscope.py --docker     # Force Docker mode
    python run_phishscope.py --no-docker  # Force manual mode (SQLite fallback)
    python run_phishscope.py --help       # Show help

Developed by : Umesh Gupta
Institution  : National Forensic Sciences University, Tripura Campus
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
from pathlib import Path

# Force UTF-8 encoding for stdout/stderr to support box drawing characters on Windows
if hasattr(sys.stdout, 'reconfigure'):
    if sys.stdout.encoding.lower() != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except Exception:
            pass
# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
VERSION = "0.1.0"
PROJECT_ROOT = Path(__file__).parent.resolve()
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
LOGS_DIR = PROJECT_ROOT / "logs"
ENV_FILE = PROJECT_ROOT / ".env"
ENV_EXAMPLE = PROJECT_ROOT / ".env.example"

ADMIN_EMAIL = "admin@phoenix.ai"
ADMIN_PASSWORD = "Phoenix@Admin123"

MIN_PYTHON = (3, 11)
BACKEND_PORT = 8000
FRONTEND_PORT = 3000
HEALTH_URL = f"http://localhost:{BACKEND_PORT}/api/v1/health"
HEALTH_TIMEOUT = 120  # seconds to wait for services to be healthy

FEATURES = [
    "URL & QR-Code Phishing Detection",
    "AI-Powered Threat Intelligence Feed",
    "Email Forensics & BEC Detection",
    "Disk, Memory, Mobile & Cloud Forensics (DFIR)",
    "SOC Co-Pilot with LLM Reasoning",
    "Malware Analysis Engine",
    "Threat Actor & Campaign Tracking",
    "Attack Graph Visualization (MITRE ATT&CK)",
    "Red Team / Blue Team Simulation",
    "Enterprise Threat Hunting Platform",
    "CSPM / CWPP / CIEM / CDR / DSPM (Cloud Security)",
    "SAST / DAST / SCA / SBOM / IaC (AppSec)",
    "Identity Security Posture Management (ISPM)",
    "Zero Trust Architecture Enforcement",
    "SOAR Orchestration & Automated Playbooks",
    "Executive Intelligence Dashboard",
    "Cyber Resilience & BCP Planning",
    "CTEM — Continuous Threat Exposure Management",
    "Chrome Extension for Real-Time Browser Protection",
    "95+ Enterprise Security Modules",
]

# Spawned child processes (for graceful shutdown)
_child_processes: list = []
_shutdown_event = threading.Event()

# ─────────────────────────────────────────────────────────────────────────────
# ANSI COLOR HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def _enable_windows_ansi():
    """Enable ANSI escape sequences on Windows 10+ via SetConsoleMode."""
    if platform.system() == "Windows":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            # Enable ENABLE_VIRTUAL_TERMINAL_PROCESSING (0x0004)
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            pass  # Fall through to no-color mode silently

_enable_windows_ansi()

# Check if terminal supports colors
_USE_COLOR = sys.stdout.isatty() or os.environ.get("FORCE_COLOR") == "1"

class C:
    """ANSI color codes — gracefully no-ops when color is not supported."""
    RESET  = "\033[0m"   if _USE_COLOR else ""
    BOLD   = "\033[1m"   if _USE_COLOR else ""
    RED    = "\033[91m"  if _USE_COLOR else ""
    GREEN  = "\033[92m"  if _USE_COLOR else ""
    YELLOW = "\033[93m"  if _USE_COLOR else ""
    BLUE   = "\033[94m"  if _USE_COLOR else ""
    CYAN   = "\033[96m"  if _USE_COLOR else ""
    WHITE  = "\033[97m"  if _USE_COLOR else ""
    DIM    = "\033[2m"   if _USE_COLOR else ""

def ok(msg):    print(f"  {C.GREEN}[✓]{C.RESET} {msg}")
def warn(msg):  print(f"  {C.YELLOW}[!]{C.RESET} {msg}")
def info(msg):  print(f"  {C.BLUE}[i]{C.RESET} {msg}")
def step(n, total, msg): print(f"\n{C.CYAN}{C.BOLD}[STEP {n}/{total}]{C.RESET}  {C.WHITE}{msg}{C.RESET}")

def error_box(source: str, what: str, why: str, fix: str, log_path: str = ""):
    """Print a structured, human-readable error block."""
    print()
    print(f"  {C.RED}{'─'*60}{C.RESET}")
    print(f"  {C.RED}{C.BOLD}[ERROR]{C.RESET}")
    print(f"  {C.BOLD}  ● Source :{C.RESET} {source}")
    print(f"  {C.BOLD}  ● What   :{C.RESET} {what}")
    print(f"  {C.BOLD}  ● Why    :{C.RESET} {why}")
    print(f"  {C.BOLD}  ● Fix    :{C.RESET} {fix}")
    if log_path:
        print(f"  {C.BOLD}  ● Log    :{C.RESET} {C.DIM}{log_path}{C.RESET}")
    print(f"  {C.RED}{'─'*60}{C.RESET}")
    print()

# ─────────────────────────────────────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────────────────────────────────────
LOGS_DIR.mkdir(exist_ok=True)
_log_stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
_launcher_log = LOGS_DIR / f"phoenix_launcher_{_log_stamp}.log"

def _log(msg: str):
    """Write a message to the launcher log file."""
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    with open(_launcher_log, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")

# ─────────────────────────────────────────────────────────────────────────────
# BANNER
# ─────────────────────────────────────────────────────────────────────────────
def print_banner():
    banner = f"""
{C.CYAN}{C.BOLD}╔══════════════════════════════════════════════════════════════════╗
║         PHOENIX — PhishScope-AI  v{VERSION:<28}     ║
║         AI-Powered Cyber Intelligence Platform                   ║
╠══════════════════════════════════════════════════════════════════╣
║  Developed by  :  Umesh Gupta                                    ║
║  Institution   :  National Forensic Sciences University          ║
║                   Tripura Campus                                 ║
║  GitHub        :  Hardy20102004/PhishScope-AI                    ║
╚══════════════════════════════════════════════════════════════════╝{C.RESET}
"""
    print(banner)

def print_features():
    print(f"{C.BOLD}  KEY FEATURES:{C.RESET}")
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
                "          Linux:   sudo apt install python3.11 (Ubuntu/Debian)"
            ),
        )
        sys.exit(1)
    ok(f"Python {sys.version.split()[0]} detected")
    _log(f"Python OK: {sys.version}")

def detect_os():
    """Detect and display OS information."""
    system = platform.system()
    release = platform.release()
    machine = platform.machine()
    info(f"OS: {system} {release} ({machine})")
    _log(f"OS: {system} {release} {machine}")
    return system

def check_docker() -> bool:
    """Check if Docker and docker compose are available."""
    docker_path = shutil.which("docker")
    if not docker_path:
        return False
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            warn("Docker is installed but not running. Start Docker Desktop / Docker daemon.")
            return False

        # Check docker compose (v2 plugin)
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
    npm_path = shutil.which("npm")
    if not node_path or not npm_path:
        warn("Node.js / npm not found. Frontend will be skipped in no-Docker mode.")
        warn("Install from: https://nodejs.org/en/download")
        _log("Node.js: NOT FOUND")
        return False
    try:
        ver = subprocess.run([node_path, "--version"], capture_output=True, text=True, timeout=5)
        npm_ver = subprocess.run([npm_path, "--version"], capture_output=True, text=True, timeout=5, shell=sys.platform.startswith("win"))
        ok(f"Node.js {ver.stdout.strip()} / npm {npm_ver.stdout.strip()}")
        _log(f"Node.js: {ver.stdout.strip()}")
        return True
    except Exception as e:
        _log(f"Node.js check failed: {e}")
        return False

# ─────────────────────────────────────────────────────────────────────────────
# ENV BOOTSTRAPPER
# ─────────────────────────────────────────────────────────────────────────────
def bootstrap_env():
    """Create .env from .env.example if it doesn't exist."""
    if ENV_FILE.exists():
        ok(".env already exists — using existing configuration")
        return
    if ENV_EXAMPLE.exists():
        import shutil as _sh
        _sh.copy(ENV_EXAMPLE, ENV_FILE)
        ok(f".env created from .env.example")
        _log(".env bootstrapped from .env.example")
    else:
        # Write minimal .env inline
        minimal_env = f"""# PhishScope-AI — Auto-generated .env
ENVIRONMENT=development
SECRET_KEY=dev-insecure-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database (SQLite fallback for dev)
SQLALCHEMY_DATABASE_URI=sqlite:///./phoenix_dev.db
POSTGRES_SERVER=localhost
POSTGRES_USER=phoenix
POSTGRES_PASSWORD=password
POSTGRES_DB=phoenix

# Redis
REDIS_URL=redis://localhost:6379/0

# Admin defaults
ADMIN_EMAIL={ADMIN_EMAIL}
ADMIN_PASSWORD={ADMIN_PASSWORD}
"""
        ENV_FILE.write_text(minimal_env, encoding="utf-8")
        ok(".env created with development defaults")
        _log(".env created with minimal defaults")

# ─────────────────────────────────────────────────────────────────────────────
# DEPENDENCY MANAGEMENT
# ─────────────────────────────────────────────────────────────────────────────
def install_backend_deps():
    """Install backend Python dependencies."""
    req_file = BACKEND_DIR / "requirements.txt"
    if not req_file.exists():
        warn(f"requirements.txt not found at {req_file}. Skipping pip install.")
        return
    print(f"    Installing backend Python packages ", end="", flush=True)
    log_file = LOGS_DIR / f"backend_pip_{_log_stamp}.log"
    try:
        in_venv = sys.prefix != sys.base_prefix
        if not in_venv:
            venv_dir = BACKEND_DIR / ".venv"
            if not venv_dir.exists():
                subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
            os_name = platform.system()
            python_exec = str(venv_dir / ("Scripts" if os_name == "Windows" else "bin") / "python")
        else:
            python_exec = sys.executable

        with open(log_file, "w") as lf:
            proc = subprocess.run(
                [python_exec, "-m", "pip", "install", "-r", str(req_file), "--quiet"],
                stdout=lf, stderr=lf, cwd=str(BACKEND_DIR), timeout=300
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
        warn(f"pip install timed out. Check {log_file}")

def install_frontend_deps():
    """Install frontend npm dependencies."""
    pkg_file = FRONTEND_DIR / "package.json"
    if not pkg_file.exists():
        warn("frontend/package.json not found. Skipping npm install.")
        return
    print(f"    Installing frontend Node packages  ", end="", flush=True)
    log_file = LOGS_DIR / f"frontend_npm_{_log_stamp}.log"
    try:
        with open(log_file, "w") as lf:
            npm_path = shutil.which("npm") or "npm"
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
    print()
    print(f"  {C.YELLOW}{C.BOLD}Default Admin Credentials (change after first login!){C.RESET}")
    print(f"  {C.YELLOW}  ┌─────────────────────────────────────────────┐{C.RESET}")
    print(f"  {C.YELLOW}  │  Email    :  {C.WHITE}{ADMIN_EMAIL:<29}{C.YELLOW}  │{C.RESET}")
    print(f"  {C.YELLOW}  │  Password :  {C.WHITE}{ADMIN_PASSWORD:<29}{C.YELLOW}  │{C.RESET}")
    print(f"  {C.YELLOW}  │  {C.RED}⚠  CHANGE PASSWORD AFTER FIRST LOGIN!   {C.YELLOW}  │{C.RESET}")
    print(f"  {C.YELLOW}  └─────────────────────────────────────────────┘{C.RESET}")
    print()

# ─────────────────────────────────────────────────────────────────────────────
# PROCESS LOG STREAMING
# ─────────────────────────────────────────────────────────────────────────────
def _stream_logs(proc: subprocess.Popen, prefix: str, log_path: Path):
    """Thread target: read a process's stdout/stderr and write to log + console."""
    prefix_colored = f"{C.DIM}[{prefix}]{C.RESET} "
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
    import urllib.request
    import urllib.error
    start = time.time()
    dots = 0
    print(f"    Waiting for backend ", end="", flush=True)
    while time.time() - start < timeout:
        if _shutdown_event.is_set():
            return False
        try:
            with urllib.request.urlopen(HEALTH_URL, timeout=3) as resp:
                if resp.status == 200:
                    print(f" {C.GREEN}healthy ✓{C.RESET}")
                    _log("Backend health: OK")
                    return True
        except Exception:
            pass
        time.sleep(2)
        print(".", end="", flush=True)
        dots += 1
    print(f" {C.RED}timeout{C.RESET}")
    return False

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

    print(f"    Building and starting containers ", end="", flush=True)
    log_file = LOGS_DIR / f"docker_{_log_stamp}.log"
    _log("Starting docker compose up --build -d")
    try:
        with open(log_file, "w") as lf:
            proc = subprocess.run(
                ["docker", "compose", "up", "--build", "-d"],
                stdout=lf, stderr=lf, cwd=str(PROJECT_ROOT), timeout=300
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
            what="Docker build timed out (>5 minutes).",
            why="A Docker image layer may be downloading or building.",
            fix="Wait and retry, or run: docker compose up --build manually",
            log_path=str(log_file),
        )
        sys.exit(1)

    # Run migrations
    print(f"    Running database migrations      ", end="", flush=True)
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
def launch_manual(has_node: bool):
    """Launch backend (uvicorn) and frontend (npm run dev) as subprocesses."""
    os_name = platform.system()

    # ── Backend ──────────────────────────────────────────────────────────────
    backend_log = LOGS_DIR / f"backend_{_log_stamp}.log"
    print(f"    Starting backend (uvicorn)       ", end="", flush=True)

    # Find python/uvicorn inside .venv if available, else system
    venv_python = BACKEND_DIR / ".venv" / ("Scripts" if os_name == "Windows" else "bin") / "python"
    python_exec = str(venv_python) if venv_python.exists() else sys.executable

    env = os.environ.copy()
    env["PYTHONPATH"] = str(BACKEND_DIR)
    # Force SQLite for no-Docker mode
    if "SQLALCHEMY_DATABASE_URI" not in env:
        env["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./phoenix_dev.db"
    if "SECRET_KEY" not in env or env.get("SECRET_KEY") == "":
        env["SECRET_KEY"] = "dev-insecure-key-change-in-production"

    try:
        backend_lf = open(backend_log, "w", encoding="utf-8")
        backend_proc = subprocess.Popen(
            [
                python_exec, "-m", "uvicorn",
                "app.main:app",
                "--host", "0.0.0.0",
                "--port", str(BACKEND_PORT),
                "--reload",
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

    # ── Frontend ─────────────────────────────────────────────────────────────
    if has_node:
        frontend_log = LOGS_DIR / f"frontend_{_log_stamp}.log"
        print(f"    Starting frontend (npm dev)      ", end="", flush=True)
        try:
            frontend_lf = open(frontend_log, "w", encoding="utf-8")
            npm_path = shutil.which("npm") or "npm"
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
    print(f"\n\n{C.YELLOW}  Shutting down PHOENIX...{C.RESET}")
    _log("Shutdown initiated")

    for proc in _child_processes:
        try:
            proc.terminate()
        except Exception:
            pass

    time.sleep(1)
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

signal.signal(signal.SIGINT, _shutdown)
signal.signal(signal.SIGTERM, _shutdown)

# ─────────────────────────────────────────────────────────────────────────────
# SERVICE STATUS TABLE
# ─────────────────────────────────────────────────────────────────────────────
def print_status_table(use_docker: bool):
    print()
    print(f"  {C.GREEN}{C.BOLD}All systems operational!{C.RESET}")
    print()
    rows = [
        ("Backend API",  f"http://localhost:{BACKEND_PORT}",      "FastAPI / Uvicorn"),
        ("API Docs",     f"http://localhost:{BACKEND_PORT}/docs",  "Swagger UI"),
        ("Frontend",     f"http://localhost:{FRONTEND_PORT}",      "React Dashboard"),
    ]
    if use_docker:
        rows += [
            ("PostgreSQL", "localhost:5432", "Docker container"),
            ("Redis",      "localhost:6379", "Docker container"),
        ]
    print(f"  {'Service':<15} {'URL':<40} {'Notes'}")
    print(f"  {'─'*15} {'─'*40} {'─'*20}")
    for name, url, note in rows:
        print(f"  {C.BOLD}{name:<15}{C.RESET} {C.CYAN}{url:<40}{C.RESET} {C.DIM}{note}{C.RESET}")
    print()

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="PhishScope-AI Universal Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Examples:
          python run_phishscope.py              # Auto-detect mode
          python run_phishscope.py --docker     # Force Docker mode
          python run_phishscope.py --no-docker  # Force manual (SQLite) mode
        """)
    )
    parser.add_argument("--docker",    action="store_true", help="Force Docker mode")
    parser.add_argument("--no-docker", action="store_true", help="Force manual mode (SQLite fallback)")
    parser.add_argument("--no-browser", action="store_true", help="Do not open browser automatically")
    args = parser.parse_args()

    TOTAL_STEPS = 5

    # ── Banner ────────────────────────────────────────────────────────────────
    print_banner()
    print_features()
    _log(f"PHOENIX launcher started — v{VERSION}")

    # ── Step 1: Environment Detection ─────────────────────────────────────────
    step(1, TOTAL_STEPS, "Detecting your environment...")
    check_python_version()
    os_name = detect_os()

    has_docker = False
    has_node   = False

    if not args.no_docker:
        has_docker = check_docker()
    if not has_docker and not args.docker:
        has_node = check_nodejs()
    elif has_docker:
        has_node = check_nodejs()  # Still useful for extension build

    # Decide mode
    if args.docker and not has_docker:
        error_box(
            source="Docker check",
            what="--docker flag was set but Docker is not running.",
            why="Docker is either not installed or the Docker daemon is not started.",
            fix="Start Docker Desktop (Windows/macOS) or run: sudo systemctl start docker (Linux)",
        )
        sys.exit(1)

    use_docker = has_docker and not args.no_docker
    mode_label = "Docker mode" if use_docker else "Manual mode (SQLite fallback)"
    info(f"Launch mode: {C.BOLD}{mode_label}{C.RESET}")

    # ── Step 2: Dependencies ──────────────────────────────────────────────────
    step(2, TOTAL_STEPS, "Installing dependencies...")
    if not use_docker:
        install_backend_deps()
    if has_node:
        install_frontend_deps()
    else:
        info("Skipping frontend npm install (Node.js not found)")

    # ── Step 3: Environment Configuration ────────────────────────────────────
    step(3, TOTAL_STEPS, "Configuring environment...")
    bootstrap_env()

    # ── Step 4: Credentials & Launch ─────────────────────────────────────────
    step(4, TOTAL_STEPS, "Starting services...")
    if use_docker:
        launch_docker()
    else:
        launch_manual(has_node)

    # Wait for backend to be healthy
    healthy = _wait_for_healthy()
    if not healthy:
        error_box(
            source="Health Check",
            what=f"Backend did not become healthy within {HEALTH_TIMEOUT}s.",
            why="The backend process may have crashed during startup.",
            fix=(
                "Check logs in the logs/ directory for details.\n"
                f"          Try: docker compose logs backend  (Docker mode)\n"
                f"          Or:  cat logs/backend_{_log_stamp}.log  (manual mode)"
            ),
            log_path=str(LOGS_DIR),
        )
        # Don't exit — allow user to inspect
    else:
        ok(f"Backend API online: http://localhost:{BACKEND_PORT}")
        ok(f"API Documentation:  http://localhost:{BACKEND_PORT}/docs")
        ok(f"Frontend Dashboard: http://localhost:{FRONTEND_PORT}")

    # ── Step 5: Ready ─────────────────────────────────────────────────────────
    step(5, TOTAL_STEPS, "PHOENIX is ready!")
    print_admin_credentials()
    print_status_table(use_docker)

    print(f"  {C.DIM}Launcher log → {_launcher_log}{C.RESET}")
    print(f"  {C.DIM}All logs     → {LOGS_DIR}/{C.RESET}")
    print()

    # Open browser
    if not args.no_browser and healthy:
        time.sleep(1)
        try:
            webbrowser.open(f"http://localhost:{FRONTEND_PORT}")
            ok("Browser opened automatically.")
        except Exception:
            info(f"Open manually: http://localhost:{FRONTEND_PORT}")

    # ── Keep-alive loop ───────────────────────────────────────────────────────
    if _child_processes or use_docker:
        print(f"\n  {C.CYAN}Press {C.BOLD}Ctrl+C{C.RESET}{C.CYAN} to stop all services.{C.RESET}\n")
        try:
            while not _shutdown_event.is_set():
                # Check if any process died unexpectedly
                for proc in _child_processes:
                    if proc.poll() is not None and not _shutdown_event.is_set():
                        warn(f"A service process (PID {proc.pid}) exited unexpectedly. Check logs.")
                        _log(f"Process PID {proc.pid} died unexpectedly (code {proc.returncode})")
                time.sleep(5)
        except KeyboardInterrupt:
            _shutdown()
    else:
        print(f"\n  {C.DIM}Docker mode: services are running in background containers.{C.RESET}")
        print(f"  To stop: {C.BOLD}docker compose down{C.RESET}\n")

if __name__ == "__main__":
    main()

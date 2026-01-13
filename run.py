#!/usr/bin/env python3
"""
Baltimore Intel - Quick Start Script

Starts all services for the intelligence platform.
"""

import subprocess
import sys
import os
import argparse
from pathlib import Path

ROOT_DIR = Path(__file__).parent
BALTIMORE_INTEL_DIR = ROOT_DIR / "baltimore_intel"
WATCHER_DIR = ROOT_DIR / "Watcher"


def run_docker():
    """Start all services via Docker Compose."""
    print("Starting Baltimore Intel via Docker...")
    subprocess.run(
        ["docker-compose", "-f", "docker-compose.full.yml", "up", "-d"],
        cwd=ROOT_DIR,
        check=True
    )
    print("\nServices started:")
    print("  - Watcher UI:        http://localhost:9002")
    print("  - Baltimore Intel:   http://localhost:8082")
    print("  - AIS Tracker:       http://localhost:8080")


def run_baltimore_intel():
    """Start Baltimore Intel API standalone."""
    print("Starting Baltimore Intel API...")
    subprocess.run(
        [sys.executable, "intelligence_hub.py"],
        cwd=BALTIMORE_INTEL_DIR
    )


def run_tests():
    """Run the test suite."""
    print("Running Baltimore Intel tests...")
    subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--cov=.", "--cov-report=term-missing"],
        cwd=BALTIMORE_INTEL_DIR
    )


def check_deps():
    """Check if dependencies are installed."""
    print("Checking dependencies...")

    # Check Python packages
    try:
        import requests
        import flask
        print("  [OK] Core Python packages")
    except ImportError as e:
        print(f"  [MISSING] {e.name} - run: pip install -r baltimore_intel/requirements.txt")
        return False

    # Check Docker
    result = subprocess.run(["docker", "--version"], capture_output=True)
    if result.returncode == 0:
        print("  [OK] Docker")
    else:
        print("  [MISSING] Docker - required for full stack")

    # Check for API keys
    if os.environ.get("AISSTREAM_API_KEY"):
        print("  [OK] AISSTREAM_API_KEY")
    else:
        print("  [WARN] AISSTREAM_API_KEY not set - vessel tracking disabled")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Baltimore Intel - Critical Infrastructure Intelligence Platform"
    )
    parser.add_argument(
        "command",
        choices=["docker", "api", "test", "check"],
        help="Command to run"
    )

    args = parser.parse_args()

    if args.command == "docker":
        run_docker()
    elif args.command == "api":
        run_baltimore_intel()
    elif args.command == "test":
        run_tests()
    elif args.command == "check":
        check_deps()


if __name__ == "__main__":
    main()

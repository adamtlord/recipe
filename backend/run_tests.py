#!/usr/bin/env python3
"""
Test runner script for the Recipe API application.
Provides convenient commands to run different types of tests.
"""

import subprocess
import sys
from pathlib import Path


def run_command(command: list[str], description: str) -> bool:
    """Run a command and return success status."""
    print(f"\n🔄 {description}")
    print(f"Running: {' '.join(command)}")

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("✅ Success!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Failed!")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False


def main():
    """Main test runner function."""
    if len(sys.argv) < 2:
        print("Usage: python run_tests.py [command]")
        print("\nAvailable commands:")
        print("  unit       - Run unit tests only")
        print("  integration - Run integration tests only")
        print("  all        - Run all tests")
        print("  coverage   - Run all tests with coverage report")
        print("  fast       - Run fast tests (unit tests only)")
        print("  lint       - Run linting checks")
        print("  help       - Show this help message")
        return

    command = sys.argv[1].lower()
    project_root = Path(__file__).parent

    if command == "unit":
        success = run_command(
            ["python", "-m", "pytest", "tests/unit/", "-v"],
            "Running unit tests"
        )
    elif command == "integration":
        success = run_command(
            ["python", "-m", "pytest", "tests/integration/", "-v"],
            "Running integration tests"
        )
    elif command == "all":
        success = run_command(
            ["python", "-m", "pytest", "tests/", "-v"],
            "Running all tests"
        )
    elif command == "coverage":
        # Install coverage if not available
        try:
            subprocess.run(["python", "-m", "pytest", "--version"], check=True)
        except subprocess.CalledProcessError:
            print("Installing pytest...")
            subprocess.run(["pip", "install", "pytest"], check=True)

        success = run_command(
            ["python", "-m", "pytest", "tests/", "--cov=app", "--cov-report=html", "--cov-report=term"],
            "Running tests with coverage"
        )
    elif command == "fast":
        success = run_command(
            ["python", "-m", "pytest", "tests/unit/", "-v", "-m", "not slow"],
            "Running fast tests"
        )
    elif command == "lint":
        success = run_command(
            ["python", "-m", "flake8", "app/", "tests/"],
            "Running linting checks"
        )
    elif command == "help":
        print(__doc__)
        return
    else:
        print(f"Unknown command: {command}")
        print("Use 'python run_tests.py help' for available commands")
        return

    if success:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()

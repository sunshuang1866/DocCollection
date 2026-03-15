#!/usr/bin/env python3
"""
Detects the project root and emits a summary of key manifest files found.
Usage: python3 scripts/detect-project-root.py <directory>
Output (stdout): JSON with detected language ecosystem and manifest paths
Error (stderr): reason if directory is invalid or no manifests found
"""

import sys
import os
import json

MANIFEST_SIGNALS = {
    "node": ["package.json"],
    "python": ["requirements.txt", "pyproject.toml", "setup.py", "Pipfile"],
    "go": ["go.mod"],
    "rust": ["Cargo.toml"],
    "java": ["pom.xml", "build.gradle"],
    "ruby": ["Gemfile"],
    "php": ["composer.json"],
    "dotnet": [".csproj", ".sln"],
}

INFRA_SIGNALS = ["docker-compose.yml", "docker-compose.yaml", "Dockerfile", ".env.example"]

def detect(directory):
    if not os.path.isdir(directory):
        print(f"ERROR: '{directory}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    result = {"root": os.path.abspath(directory), "ecosystems": [], "manifests": [], "infra": []}

    for ecosystem, files in MANIFEST_SIGNALS.items():
        for fname in files:
            fpath = os.path.join(directory, fname)
            if os.path.exists(fpath):
                result["ecosystems"].append(ecosystem)
                result["manifests"].append(fname)

    for fname in INFRA_SIGNALS:
        fpath = os.path.join(directory, fname)
        if os.path.exists(fpath):
            result["infra"].append(fname)

    result["ecosystems"] = list(set(result["ecosystems"]))

    if not result["manifests"] and not result["infra"]:
        print("WARNING: No manifest or infra files found at root. Try a subdirectory.", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, indent=2))
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 detect-project-root.py <directory>", file=sys.stderr)
        sys.exit(1)
    detect(sys.argv[1])

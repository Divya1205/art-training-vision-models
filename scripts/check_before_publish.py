"""Check the repository before publishing.

Looks for:
  - secrets: Hugging Face, GitHub, OpenAI, AWS and Google keys, private keys, hard-coded tokens
  - notebooks that still contain outputs (which may show paintings) or embedded images
  - image files, saved embeddings and large files

Usage:  python scripts/check_before_publish.py        (run from the repository root)
Exits with code 1 if anything needs attention. Uses only the Python standard library.
"""
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", ".ipynb_checkpoints"}
LARGE_BYTES = 20 * 1024 * 1024

SECRET_PATTERNS = {
    "Hugging Face token": re.compile(r"hf_[A-Za-z0-9]{30,}"),
    "GitHub token": re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"),
    "OpenAI-style key": re.compile(r"sk-[A-Za-z0-9_\-]{20,}"),
    "AWS access key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "Google API key": re.compile(r"AIza[0-9A-Za-z_\-]{35}"),
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "hard-coded token or key": re.compile(
        r"(?i)\b(?:hf_?token|api[_-]?key|access[_-]?token|secret|password)\b\s*[:=]\s*['\"][^'\"\s]{12,}['\"]"),
}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tif", ".tiff"}
DATA_EXT = {".npz", ".npy", ".pt", ".pth", ".safetensors", ".ckpt"}


def files():
    for d, dirs, names in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for n in names:
            yield os.path.join(d, n)


def main():
    problems = []
    for path in files():
        rel = os.path.relpath(path, ROOT)
        ext = os.path.splitext(path)[1].lower()
        size = os.path.getsize(path)
        if rel == os.path.join("scripts", "check_before_publish.py"):
            continue
        if ext in IMAGE_EXT and not rel.startswith(os.path.join("docs", "figures")):
            problems.append(f"{rel}: image file (could show a copyrighted painting)")
        if ext in DATA_EXT:
            problems.append(f"{rel}: saved data/model file (should not be committed)")
        if size > LARGE_BYTES:
            problems.append(f"{rel}: large file ({size / 1e6:.0f} MB)")
        if ext in IMAGE_EXT or ext in DATA_EXT or size > LARGE_BYTES:
            continue
        try:
            text = open(path, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue
        for name, pattern in SECRET_PATTERNS.items():
            for m in pattern.finditer(text):
                line = text[:m.start()].count("\n") + 1
                problems.append(f"{rel}:{line}: possible {name}: {m.group(0)[:12]}…")
        if ext == ".ipynb":
            try:
                nb = json.loads(text)
            except json.JSONDecodeError:
                problems.append(f"{rel}: notebook is not valid JSON")
                continue
            n_out = n_img = 0
            for c in nb.get("cells", []):
                for o in c.get("outputs", []) or []:
                    n_out += 1
                    if any(k.startswith("image/") for k in o.get("data", {})):
                        n_img += 1
                for att in (c.get("attachments") or {}).values():
                    n_img += sum(1 for k in att if k.startswith("image/"))
            if n_out:
                problems.append(f"{rel}: notebook has {n_out} outputs ({n_img} images); clear all outputs before committing")
            elif n_img:
                problems.append(f"{rel}: notebook has {n_img} embedded images")

    if problems:
        print("Needs attention before publishing:")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("No secrets, notebook outputs, images or large files found.")


if __name__ == "__main__":
    main()

import os
import re

IGNORED_DIRS = {".git", "venv", ".venv", "node_modules", "__pycache__", "migrations"}
PROJECT_DIR = "."

HTML_FORM_RE = re.compile(r"<form[^>]*method=[\"']?post[\"']?", re.IGNORECASE)
CSRF_TOKEN_RE = re.compile(r"(csrf_token|name=[\"']csrfmiddlewaretoken[\"'])", re.IGNORECASE)

FETCH_RE = re.compile(r"fetch\(([^)]+)\)", re.DOTALL)
HEADERS_RE = re.compile(r"headers\s*:\s*{[^}]*}", re.DOTALL | re.IGNORECASE)
X_CSRF_RE = re.compile(r"['\"]X-CSRFToken['\"]\s*:\s*['\"][^'\"]+['\"]", re.IGNORECASE)

def should_ignore_dir(path):
    return any(part in IGNORED_DIRS for part in path.split(os.sep))

def check_html_forms(filepath):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    problems = []
    for match in HTML_FORM_RE.finditer(content):
        form_block = content[match.start():match.end() + 300]  # немного контекста после
        if not CSRF_TOKEN_RE.search(form_block):
            problems.append(f"❌ Missing CSRF token in <form> in {filepath}")
    return problems

def check_js_fetch(filepath):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    problems = []
    for match in FETCH_RE.finditer(content):
        fetch_block = match.group(1)
        if re.search(r"method\s*:\s*['\"](POST|PUT|DELETE)", fetch_block, re.IGNORECASE):
            headers_match = HEADERS_RE.search(fetch_block)
            if not headers_match or not X_CSRF_RE.search(headers_match.group(0)):
                problems.append(f"❌ Possibly missing CSRF header in fetch() in {filepath}")
    return problems

def scan_project(root_dir):
    html_problems = []
    js_problems = []

    for root, dirs, files in os.walk(root_dir):
        if should_ignore_dir(root):
            continue
        for file in files:
            full_path = os.path.join(root, file)
            if file.endswith(".html"):
                html_problems.extend(check_html_forms(full_path))
            elif file.endswith(".js"):
                js_problems.extend(check_js_fetch(full_path))

    return html_problems, js_problems

if __name__ == "__main__":
    print("🔍 Scanning project for missing CSRF tokens in HTML/JS...")
    html_issues, js_issues = scan_project(PROJECT_DIR)

    if not html_issues and not js_issues:
        print("✅ All HTML forms and JS fetch requests appear to be protected.")
    else:
        if html_issues:
            print("\n[HTML Forms]")
            for p in html_issues:
                print(p)
        if js_issues:
            print("\n[JS Requests]")
            for p in js_issues:
                print(p)
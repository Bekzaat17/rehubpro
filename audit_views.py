import os
import ast

PROJECT_DIR = "."
IGNORED_DIRS = {"venv", ".venv", "__pycache__", "migrations", "tests", ".git", "node_modules"}

# Классы, которые считаются безопасными (наследуют LoginRequiredMixin или защищают view другим способом)
SAFE_BASE_CLASSES = {
    "BaseReferenceView", "BaseReferenceFactory", "CharacterTraitFactory",
}

def should_check_file(filepath):
    parts = filepath.split(os.sep)
    filename = parts[-1]
    return filename.endswith(".py") and (filename == "views.py" or "views" in parts)

def should_ignore_dir(dirpath):
    return any(part in IGNORED_DIRS for part in dirpath.split(os.sep))

class ClassCollector(ast.NodeVisitor):
    """Собирает информацию о классах: их базовые классы"""
    def __init__(self):
        self.class_hierarchy = {}  # class_name → list of base class names

    def visit_ClassDef(self, node):
        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases.append(base.attr)
        self.class_hierarchy[node.name] = bases
        self.generic_visit(node)

class ViewAuditVisitor(ast.NodeVisitor):
    def __init__(self, filename, class_hierarchy):
        self.filename = filename
        self.problems = []
        self.current_class = None
        self.imported_mixins = set()
        self.class_hierarchy = class_hierarchy

    def visit_ImportFrom(self, node):
        for alias in node.names:
            if alias.name == "LoginRequiredMixin":
                self.imported_mixins.add("LoginRequiredMixin")

    def visit_FunctionDef(self, node):
        decorator_names = [
            d.id if isinstance(d, ast.Name)
            else getattr(d.func, 'id', '') if isinstance(d, ast.Call)
            else ''
            for d in node.decorator_list
        ]

        full_decorator_lines = [ast.dump(d) for d in node.decorator_list]

        if self.current_class is None:
            # FBV
            if "api_view" in decorator_names:
                if not any("permission_classes" in d for d in full_decorator_lines):
                    self.problems.append({
                        "file": self.filename,
                        "view": node.name,
                        "type": "FBV(API)",
                        "problem": "Missing @permission_classes"
                    })

            if "csrf_exempt" in decorator_names and "login_required" not in decorator_names:
                self.problems.append({
                    "file": self.filename,
                    "view": node.name,
                    "type": "FBV",
                    "problem": "@csrf_exempt without @login_required"
                })

            if "login_required" not in decorator_names:
                self.problems.append({
                    "file": self.filename,
                    "view": node.name,
                    "type": "FBV",
                    "problem": "Missing @login_required"
                })

            if "LoginRequiredMixin" in self.imported_mixins:
                self.problems.append({
                    "file": self.filename,
                    "view": node.name,
                    "type": "FBV",
                    "problem": "Useless LoginRequiredMixin (in FBV)"
                })

        else:
            # method inside CBV
            if "login_required" in decorator_names:
                self.problems.append({
                    "file": self.filename,
                    "view": f"{self.current_class}.{node.name}",
                    "type": "CBV method",
                    "problem": "Invalid @login_required inside CBV method"
                })
            if "csrf_exempt" in decorator_names:
                self.problems.append({
                    "file": self.filename,
                    "view": f"{self.current_class}.{node.name}",
                    "type": "CBV method",
                    "problem": "Uses @csrf_exempt"
                })

    def visit_ClassDef(self, node):
        self.current_class = node.name
        if not self.has_login_required_mixin(node.name):
            self.problems.append({
                "file": self.filename,
                "view": node.name,
                "type": "CBV",
                "problem": "Missing LoginRequiredMixin (directly or via base)"
            })
        self.generic_visit(node)
        self.current_class = None

    def has_login_required_mixin(self, class_name, visited=None):
        """Рекурсивно проверяет, есть ли LoginRequiredMixin или безопасная база в иерархии"""
        if visited is None:
            visited = set()
        if class_name in visited:
            return False
        visited.add(class_name)

        if class_name in SAFE_BASE_CLASSES:
            return True  # безопасный базовый класс

        bases = self.class_hierarchy.get(class_name, [])
        if "LoginRequiredMixin" in bases:
            return True
        for base in bases:
            if self.has_login_required_mixin(base, visited):
                return True
        return False

def audit_problematic_views(project_dir):
    all_problems = []

    for root, dirs, files in os.walk(project_dir):
        if should_ignore_dir(root):
            continue

        for file in files:
            full_path = os.path.join(root, file)
            if not should_check_file(full_path):
                continue

            with open(full_path, "r", encoding="utf-8") as f:
                try:
                    source = f.read()
                    tree = ast.parse(source, filename=full_path)

                    # Сначала соберём иерархию классов
                    collector = ClassCollector()
                    collector.visit(tree)

                    # Затем — проверим проблемные view
                    visitor = ViewAuditVisitor(full_path, collector.class_hierarchy)
                    visitor.visit(tree)
                    all_problems.extend(visitor.problems)
                except Exception as e:
                    print(f"[!] Ошибка в файле {full_path}: {e}")

    return all_problems

def print_problems(problems):
    print(f"{'File':<45} {'View':<35} {'Type':<15} {'Problem'}")
    print("-" * 120)
    for p in problems:
        print(f"{p['file']:<45} {p['view']:<35} {p['type']:<15} {p['problem']}")

if __name__ == "__main__":
    print(">>> Аудит: только проблемные view")
    problems = audit_problematic_views(PROJECT_DIR)
    print_problems(problems)
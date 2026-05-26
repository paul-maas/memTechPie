#!/usr/bin/env python3
"""Validator for frontmatter schemas in Memory Tech KB vaults.

Walks through specified vault directories, parses YAML frontmatter from each
.md note, validates against type-specific schemas (selected by folder
convention), and reports any issues.

Usage:
    python validate_frontmatter.py kb-knowledge
    python validate_frontmatter.py kb-knowledge kb-clients kb-ops
    python validate_frontmatter.py --all

Exit code:
    0 — all notes pass validation (or no notes found in scope)
    1 — at least one error was found (warnings alone do not fail)

The scope of validation is intentionally folder-based — each subpath under a
vault is mapped to an expected document type. Files that don't fit any known
folder are skipped silently. Templates (`00 Мета/Шаблоны/`), READMEs, and
.gitkeep are skipped explicitly.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    print(
        "ERROR: PyYAML not installed. Install with `pip install pyyaml` "
        "or `uv pip install pyyaml`.",
        file=sys.stderr,
    )
    sys.exit(2)


# ---------------------------------------------------------------------------
# Allowed enum values
# ---------------------------------------------------------------------------

STATUSES = {"draft", "reviewed", "canonical"}
CONFIDENCES = {"low", "medium", "high"}
PARADIGMS = {
    "cognitive", "behavioral", "systemic", "humanistic",
    "psychoanalytic", "constructivist", "existential",
}
SOURCE_TYPES = {"book", "article", "lecture", "transcript", "own_material", "course"}
STATUS_KINDS = {"primary", "retelling", "criticism"}
MASTERY_LEVELS = {"novice", "working", "confident", "integrated"}
TARGET_VAULTS = {"kb-knowledge", "kb-clients", "kb-ops"}


# ---------------------------------------------------------------------------
# Schema definition
# ---------------------------------------------------------------------------

@dataclass
class Schema:
    """A frontmatter schema for one document type."""
    name: str
    required: set[str]
    expected_type: str | None = None  # value of `type:` field
    enums: dict[str, set[str]] = field(default_factory=dict)
    extra_required_when: dict[str, Any] = field(default_factory=dict)
    # extra_required_when: { field_name: required_value } — when this field
    # equals the required_value, the schema applies (e.g. borrowed=true)


# Per-folder schemas (relative path inside vault → schema)
# Order matters: more specific paths first.
SCHEMAS: list[tuple[str, Schema]] = [
    ("cards/concepts/", Schema(
        name="card-concept",
        expected_type="concept",
        required={"id", "title", "type", "school", "paradigm",
                  "status", "confidence", "version"},
        enums={"status": STATUSES, "confidence": CONFIDENCES,
               "paradigm": PARADIGMS},
    )),
    ("cards/techniques/", Schema(
        name="card-technique",
        expected_type="technique",
        required={"id", "title", "type", "school", "paradigm",
                  "status", "confidence", "version"},
        enums={"status": STATUSES, "confidence": CONFIDENCES,
               "paradigm": PARADIGMS},
    )),
    ("cards/frameworks/", Schema(
        name="card-framework",
        expected_type="framework",
        required={"id", "title", "type", "school", "paradigm",
                  "status", "confidence", "version"},
        enums={"status": STATUSES, "confidence": CONFIDENCES,
               "paradigm": PARADIGMS},
    )),
    ("cards/models/", Schema(
        name="card-model",
        expected_type="model",
        required={"id", "title", "type", "school", "paradigm",
                  "status", "confidence", "version"},
        enums={"status": STATUSES, "confidence": CONFIDENCES,
               "paradigm": PARADIGMS},
    )),
    ("cards/exercises/", Schema(
        name="card-exercise",
        expected_type="exercise",
        required={"id", "title", "type", "school", "paradigm",
                  "status", "confidence", "version"},
        enums={"status": STATUSES, "confidence": CONFIDENCES,
               "paradigm": PARADIGMS},
    )),
    ("cards/conflicts/", Schema(
        name="card-conflict",
        expected_type="concept-conflict",
        required={"id", "title", "type", "status", "confidence",
                  "version", "conflicting_paradigms"},
        enums={"status": STATUSES, "confidence": CONFIDENCES},
    )),
    ("cards/borrowed/", Schema(
        name="card-borrowed",
        # type stays concept/technique/framework — distinguished by borrowed=true
        required={"id", "title", "type", "school", "paradigm",
                  "borrowed", "source_school", "mastery_level",
                  "status", "confidence", "version"},
        enums={"status": STATUSES, "confidence": CONFIDENCES,
               "paradigm": PARADIGMS, "mastery_level": MASTERY_LEVELS},
    )),
    ("ontology/schools/", Schema(
        name="school-node",
        expected_type="school",
        required={"id", "title", "type", "paradigm",
                  "status", "confidence", "version"},
        enums={"status": STATUSES, "confidence": CONFIDENCES,
               "paradigm": PARADIGMS},
    )),
    ("ontology/paradigms/", Schema(
        name="paradigm-node",
        expected_type="paradigm",
        required={"id", "title", "type", "client_view",
                  "status", "confidence", "version"},
        enums={"status": STATUSES, "confidence": CONFIDENCES},
    )),
    ("sources/", Schema(
        name="source",
        expected_type="source",
        required={"id", "title", "type", "source_type", "status_kind",
                  "status", "confidence", "version"},
        enums={"status": STATUSES, "confidence": CONFIDENCES,
               "source_type": SOURCE_TYPES, "status_kind": STATUS_KINDS},
    )),
    ("playbooks/", Schema(
        name="playbook",
        expected_type="playbook",
        required={"id", "title", "type", "purpose", "trigger",
                  "status", "confidence", "version"},
        enums={"status": STATUSES, "confidence": CONFIDENCES},
    )),
    ("audit/", Schema(  # for kb-ops/audit/
        name="audit-entry",
        expected_type="audit-entry",
        required={"id", "type", "date", "operator", "action", "target_vault"},
        enums={"target_vault": TARGET_VAULTS},
    )),
]


# Paths to skip entirely
SKIP_DIR_FRAGMENTS = (
    "00 Мета/Шаблоны/",  # templates — they look like notes but are not
    ".obsidian/",
    ".trash/",
    ".git/",
)

SKIP_FILENAMES = {"README.md", ".gitkeep"}


# ---------------------------------------------------------------------------
# Issue model
# ---------------------------------------------------------------------------

@dataclass
class Issue:
    severity: str  # "error" | "warning"
    path: Path
    message: str

    def __str__(self) -> str:
        return f"[{self.severity.upper()}] {self.path}: {self.message}"


# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------

FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---", re.DOTALL)


def parse_frontmatter(content: str) -> tuple[dict[str, Any] | None, str | None]:
    """Return (frontmatter_dict, error_string). Either dict or error.

    None dict + None error means: no frontmatter present.
    """
    m = FRONTMATTER_RE.match(content)
    if not m:
        return None, None
    try:
        meta = yaml.safe_load(m.group(1))
    except Exception as e:
        return None, f"invalid YAML: {e}"
    if meta is None:
        return {}, None
    if not isinstance(meta, dict):
        return None, f"frontmatter is not a YAML mapping (got {type(meta).__name__})"
    return meta, None


# ---------------------------------------------------------------------------
# Schema selection
# ---------------------------------------------------------------------------

def select_schema(rel_path: Path) -> Schema | None:
    """Pick a schema for a note's relative path inside a vault."""
    s = str(rel_path).replace("\\", "/")
    for fragment, schema in SCHEMAS:
        if fragment in s:
            return schema
    return None


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def should_skip(rel_path: Path) -> bool:
    s = str(rel_path).replace("\\", "/")
    if any(frag in s for frag in SKIP_DIR_FRAGMENTS):
        return True
    if rel_path.name in SKIP_FILENAMES:
        return True
    return False


def validate_note(
    file_path: Path,
    rel_path: Path,
    schema: Schema,
) -> list[Issue]:
    issues: list[Issue] = []
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        issues.append(Issue("error", rel_path, f"cannot read file: {e}"))
        return issues

    meta, err = parse_frontmatter(content)
    if err is not None:
        issues.append(Issue("error", rel_path, err))
        return issues
    if meta is None:
        issues.append(Issue(
            "error", rel_path,
            f"missing frontmatter (expected schema: {schema.name})",
        ))
        return issues

    # Required fields
    for field_name in schema.required:
        if field_name not in meta:
            issues.append(Issue(
                "error", rel_path,
                f"missing required field '{field_name}' (schema: {schema.name})",
            ))
        elif meta[field_name] in (None, "", []):
            issues.append(Issue(
                "warning", rel_path,
                f"required field '{field_name}' is empty",
            ))

    # type field consistency
    if schema.expected_type is not None and "type" in meta:
        actual = meta["type"]
        if actual != schema.expected_type:
            issues.append(Issue(
                "error", rel_path,
                f"type mismatch: schema {schema.name} expects "
                f"type='{schema.expected_type}', got '{actual}'",
            ))

    # Enums
    for field_name, allowed in schema.enums.items():
        if field_name not in meta or meta[field_name] in (None, "", []):
            continue  # already flagged above if required
        val = meta[field_name]
        if isinstance(val, list):
            for item in val:
                if item not in allowed:
                    issues.append(Issue(
                        "error", rel_path,
                        f"field '{field_name}': value '{item}' not in "
                        f"allowed set {sorted(allowed)}",
                    ))
        else:
            if val not in allowed:
                issues.append(Issue(
                    "error", rel_path,
                    f"field '{field_name}': value '{val}' not in "
                    f"allowed set {sorted(allowed)}",
                ))

    # Schema-specific extra checks
    if schema.name == "card-borrowed":
        if meta.get("borrowed") is not True:
            issues.append(Issue(
                "error", rel_path,
                "card-borrowed must have borrowed: true",
            ))

    return issues


def walk_vault(vault_dir: Path) -> list[Issue]:
    issues: list[Issue] = []
    if not vault_dir.exists():
        return [Issue("error", vault_dir, "vault directory does not exist")]
    if not vault_dir.is_dir():
        return [Issue("error", vault_dir, "not a directory")]

    for md in vault_dir.rglob("*.md"):
        rel = md.relative_to(vault_dir)
        if should_skip(rel):
            continue
        schema = select_schema(rel)
        if schema is None:
            continue  # not under any validated folder
        issues.extend(validate_note(md, rel, schema))

    return issues


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate frontmatter schemas in Memory Tech KB vaults.",
    )
    parser.add_argument(
        "vaults", nargs="*",
        help="Vault directories to validate (relative to cwd).",
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Validate all default vaults: kb-knowledge, kb-clients, kb-ops.",
    )
    parser.add_argument(
        "--root", type=Path, default=Path("."),
        help="Root directory containing the vaults (default: cwd).",
    )
    args = parser.parse_args()

    if args.all:
        vault_paths = [args.root / v for v in
                       ("kb-knowledge", "kb-clients", "kb-ops")]
    else:
        if not args.vaults:
            parser.print_help()
            return 2
        vault_paths = [args.root / v for v in args.vaults]

    all_issues: list[Issue] = []
    for vp in vault_paths:
        all_issues.extend(walk_vault(vp))

    errors = [i for i in all_issues if i.severity == "error"]
    warnings = [i for i in all_issues if i.severity == "warning"]

    for issue in all_issues:
        print(issue, file=sys.stderr if issue.severity == "error" else sys.stdout)

    print(
        f"\nSummary: {len(errors)} error(s), {len(warnings)} warning(s) "
        f"across {len(vault_paths)} vault(s).",
        file=sys.stderr if errors else sys.stdout,
    )

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

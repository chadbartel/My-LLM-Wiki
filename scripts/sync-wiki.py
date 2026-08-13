#!/usr/bin/env python3
"""
LLM Wiki Auto-Sync: Automated monitoring and wiki updates.

Scans workspace projects, detects changes, and updates wiki pages automatically.
Usage: python scripts/sync-wiki.py [--dry-run] [--verbose]
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import tomllib


@dataclass
class ProjectMetadata:
    """Metadata about a single project."""

    name: str
    path: Path
    language: str
    status: str
    description: str
    file_count: int
    pyproject_exists: bool
    readme_exists: bool
    dockerfile_exists: bool
    dependencies: dict[str, str]
    last_modified: str
    has_tests: bool


class ProjectScanner:
    """Scans workspace projects for metadata."""

    WORKSPACE_ROOTS = [
        Path("/mnt/c/Users/Chaddle/PycharmProjects"),
        Path("/home/thatsmidnight/projects"),
        Path("/mnt/c/Users/Chaddle/Documents/ObsidianVault"),
        Path("/mnt/c/Users/Chaddle/Documents/RawSources"),
    ]

    # Projects to include (from workspace)
    KNOWN_PROJECTS = {
        "UnnamedRPG",
        "TTRPG-AI-RAG-Assistant",
        "AIO Generative AI Solution",
        "Arcane-Scribe",
        "Automated-Taskmaster",
        "brAIniac",
        "my-cache-augmented-generation",
        "GenerateIdeas",
        "my-shared-infra",
        "My-DDNS-Updater",
        "chadbarteldotcom",
        "thatsmidnightdotcom",
        "Cartographers-Cloud-Kit",
        "Homelab-Ansible",
        "Cellophane",
        "Close-Application",
        "MidnightsGitHubActions",
        "FunWithMusic",
        "My-Mini-Projects",
        "TableTopMaestro",
    }

    def __init__(self, verbose: bool = False):
        """Initialize scanner."""
        self.verbose = verbose
        self.found_projects: dict[str, ProjectMetadata] = {}

    def log(self, msg: str) -> None:
        """Print verbose log message."""
        if self.verbose:
            print(f"[SCAN] {msg}")

    def scan_all(self) -> dict[str, ProjectMetadata]:
        """Scan all workspace projects."""
        self.log("Starting project scan...")

        for root in self.WORKSPACE_ROOTS:
            if not root.exists():
                self.log(f"Root {root} does not exist, skipping")
                continue

            for item in root.iterdir():
                if item.is_dir() and item.name in self.KNOWN_PROJECTS:
                    self.log(f"Scanning {item.name}...")
                    try:
                        metadata = self._scan_project(item)
                        self.found_projects[item.name] = metadata
                    except Exception as e:
                        print(f"ERROR scanning {item.name}: {e}", file=sys.stderr)

        self.log(f"Scan complete. Found {len(self.found_projects)} projects")
        return self.found_projects

    def _scan_project(self, project_path: Path) -> ProjectMetadata:
        """Scan a single project directory."""
        # Detect language
        language = self._detect_language(project_path)

        # Count files
        file_count = sum(1 for _ in project_path.rglob("*") if _.is_file())

        # Check key files
        pyproject_exists = (project_path / "pyproject.toml").exists()
        readme_exists = (project_path / "README.md").exists()
        dockerfile_exists = (project_path / "Dockerfile").exists()
        has_tests = (project_path / "tests").exists() or any(
            project_path.glob("test/*.py")
        )

        # Parse pyproject.toml for dependencies
        dependencies = {}
        if pyproject_exists:
            try:
                with open(project_path / "pyproject.toml", "rb") as f:
                    pyproject = tomllib.load(f)
                    if "dependencies" in pyproject.get("project", {}):
                        deps = pyproject["project"]["dependencies"]
                        dependencies = {
                            dep.split()[0]: dep for dep in deps[:5]
                        }  # Top 5
            except Exception as e:
                self.log(f"Error parsing pyproject.toml for {project_path.name}: {e}")

        # Detect status (from README or other indicators)
        status = self._detect_status(project_path)

        # Get description (from README or pyproject.toml)
        description = self._extract_description(project_path)

        # Last modified time
        last_modified = datetime.fromtimestamp(
            max((project_path / f).stat().st_mtime for f in project_path.rglob("*") if f.is_file())
        ).isoformat()

        return ProjectMetadata(
            name=project_path.name,
            path=project_path,
            language=language,
            status=status,
            description=description,
            file_count=file_count,
            pyproject_exists=pyproject_exists,
            readme_exists=readme_exists,
            dockerfile_exists=dockerfile_exists,
            dependencies=dependencies,
            last_modified=last_modified,
            has_tests=has_tests,
        )

    def _detect_language(self, project_path: Path) -> str:
        """Detect primary language from file extensions."""
        extensions: dict[str, int] = {}
        for file in project_path.rglob("*"):
            if file.is_file():
                ext = file.suffix
                extensions[ext] = extensions.get(ext, 0) + 1

        # Map extensions to languages
        python_count = extensions.get(".py", 0)
        typescript_count = extensions.get(".ts", 0) + extensions.get(".tsx", 0)
        yaml_count = extensions.get(".yml", 0) + extensions.get(".yaml", 0)

        if python_count > max(typescript_count, yaml_count):
            return "Python"
        elif typescript_count > yaml_count:
            return "TypeScript"
        elif yaml_count > 0:
            return "YAML"
        return "Other"

    def _detect_status(self, project_path: Path) -> str:
        """Detect project status from README or other indicators."""
        readme_path = project_path / "README.md"
        if readme_path.exists():
            content = readme_path.read_text()
            if "active" in content.lower():
                return "active"
            elif "planning" in content.lower() or "todo" in content.lower():
                return "planning"
            elif "archived" in content.lower() or "deprecated" in content.lower():
                return "archived"
            elif "experimental" in content.lower():
                return "experimental"

        # Default detection
        if (project_path / "main.py").exists():
            return "active"
        if (project_path / "pyproject.toml").exists():
            return "in-progress"
        return "unknown"

    def _extract_description(self, project_path: Path) -> str:
        """Extract description from README or pyproject.toml."""
        # Try README
        readme_path = project_path / "README.md"
        if readme_path.exists():
            lines = readme_path.read_text().split("\n")
            for i, line in enumerate(lines):
                if line.strip() and not line.startswith("#"):
                    return line.strip()[:200]

        # Try pyproject.toml
        pyproject_path = project_path / "pyproject.toml"
        if pyproject_path.exists():
            try:
                with open(pyproject_path, "rb") as f:
                    pyproject = tomllib.load(f)
                    desc = pyproject.get("project", {}).get("description", "")
                    return desc[:200] if desc else ""
            except Exception:
                pass

        return ""


class ChangeDetector:
    """Detects changes between current and last sync state."""

    def __init__(self, verbose: bool = False):
        """Initialize detector."""
        self.verbose = verbose

    def log(self, msg: str) -> None:
        """Print verbose log message."""
        if self.verbose:
            print(f"[DETECT] {msg}")

    def detect_changes(
        self, current: dict[str, ProjectMetadata], last_state: dict[str, Any]
    ) -> dict[str, Any]:
        """Detect changes between current and last state."""
        self.log("Detecting changes...")

        changes = {
            "new_projects": [],
            "removed_projects": [],
            "status_changes": [],
            "dependency_changes": [],
            "modified_projects": [],
        }

        current_names = {p.name for p in current.values()}
        last_names = set(last_state.get("projects", {}).keys())

        # New projects
        for name in current_names - last_names:
            self.log(f"New project: {name}")
            changes["new_projects"].append(name)

        # Removed projects
        for name in last_names - current_names:
            self.log(f"Removed project: {name}")
            changes["removed_projects"].append(name)

        # Status changes and modifications
        for name, metadata in current.items():
            if name not in last_state.get("projects", {}):
                continue

            last = last_state["projects"][name]

            if metadata.status != last.get("status"):
                self.log(f"Status change: {name} ({last.get('status')} -> {metadata.status})")
                changes["status_changes"].append(
                    {"project": name, "old": last.get("status"), "new": metadata.status}
                )

            if metadata.last_modified != last.get("last_modified"):
                self.log(f"Modified: {name}")
                changes["modified_projects"].append(name)

            # Check dependencies
            if metadata.dependencies != last.get("dependencies", {}):
                self.log(f"Dependencies changed: {name}")
                changes["dependency_changes"].append(
                    {
                        "project": name,
                        "old": last.get("dependencies", {}),
                        "new": metadata.dependencies,
                    }
                )

        return changes


class WikiUpdater:
    """Updates wiki pages based on detected changes."""

    def __init__(self, wiki_root: Path, verbose: bool = False, dry_run: bool = False):
        """Initialize updater."""
        self.wiki_root = wiki_root
        self.verbose = verbose
        self.dry_run = dry_run
        self.updates_made: list[str] = []

    def log(self, msg: str) -> None:
        """Print verbose log message."""
        if self.verbose:
            print(f"[UPDATE] {msg}")

    def apply_changes(
        self,
        changes: dict[str, Any],
        current: dict[str, ProjectMetadata],
        old_state: dict[str, Any],
    ) -> dict[str, Any]:
        """Apply changes to wiki pages."""
        self.log("Applying changes to wiki...")

        summary = {
            "pages_updated": [],
            "new_projects_documented": [],
            "status_updates": [],
        }

        # Update entity pages for modified projects
        for project_name in changes["modified_projects"]:
            if project_name in current:
                self.log(f"Updating entity page for {project_name}")
                self._update_entity_page(current[project_name])
                summary["pages_updated"].append(f"entities/{project_name}")
                self.updates_made.append(f"Updated entity: {project_name}")

        # Update status changes
        for change in changes["status_changes"]:
            self.log(f"Updating status for {change['project']}")
            self._update_status(change["project"], change["old"], change["new"])
            summary["status_updates"].append(change)
            self.updates_made.append(
                f"Status changed: {change['project']} ({change['old']} -> {change['new']})"
            )

        # Document new projects
        for new_proj in changes["new_projects"]:
            if new_proj in current:
                self.log(f"Creating entity page for new project {new_proj}")
                self._create_entity_page(current[new_proj])
                summary["new_projects_documented"].append(new_proj)
                self.updates_made.append(f"New project documented: {new_proj}")

        # Update shared infrastructure map if dependencies changed
        if changes["dependency_changes"]:
            self.log("Updating Shared Infrastructure Map")
            self._update_infrastructure_map(changes["dependency_changes"])
            summary["pages_updated"].append("synthesis/Shared-Infrastructure-Map")
            self.updates_made.append("Updated Shared Infrastructure Map")

        return summary

    def _update_entity_page(self, metadata: ProjectMetadata) -> None:
        """Update an entity page with new metadata."""
        entity_path = self.wiki_root / "entities" / f"{metadata.name}.md"
        if not entity_path.exists():
            self.log(f"Entity page {entity_path} does not exist, creating...")
            self._create_entity_page(metadata)
            return

        if self.dry_run:
            self.log(f"[DRY RUN] Would update {entity_path}")
            return

        content = entity_path.read_text()

        # Update modification date in frontmatter
        new_date = datetime.now().strftime("%Y-%m-%d")
        if "date_updated:" in content:
            old_date_line = next(
                (line for line in content.split("\n") if line.startswith("date_updated:")),
                None,
            )
            if old_date_line:
                new_line = f"date_updated: {new_date}"
                content = content.replace(old_date_line, new_line)

        # Update status if mentioned
        if metadata.status and f"**Status:** {metadata.status}" in content:
            content = content.replace(
                f"**Status:** {metadata.status}", f"**Status:** {metadata.status}"
            )

        entity_path.write_text(content)
        self.log(f"Updated {entity_path}")

    def _create_entity_page(self, metadata: ProjectMetadata) -> None:
        """Create a new entity page for a project."""
        entity_path = self.wiki_root / "entities" / f"{metadata.name}.md"

        if self.dry_run:
            self.log(f"[DRY RUN] Would create {entity_path}")
            return

        frontmatter = f"""---
type: entity
date_created: {datetime.now().strftime("%Y-%m-%d")}
date_updated: {datetime.now().strftime("%Y-%m-%d")}
tags:
  - wiki/entity
  - auto-discovered
---

# {metadata.name}

{metadata.description}

## Status
- **Status:** {metadata.status}
- **Language:** {metadata.language}
- **Last Modified:** {metadata.last_modified}
- **File Count:** {metadata.file_count}

## Technology Stack
- **Language:** {metadata.language}
- **Has Tests:** {"Yes" if metadata.has_tests else "No"}
- **Has Dockerfile:** {"Yes" if metadata.dockerfile_exists else "No"}

## Key Dependencies
{self._format_dependencies(metadata.dependencies)}

## Path
{metadata.path}

---

**Note:** This page was auto-discovered by the wiki sync script. Add more details manually.
"""

        entity_path.write_text(frontmatter)
        self.log(f"Created {entity_path}")

    def _format_dependencies(self, deps: dict[str, str]) -> str:
        """Format dependencies as markdown list."""
        if not deps:
            return "- None detected"
        return "\n".join(f"- {dep}" for dep in deps.values())

    def _update_status(self, project_name: str, old_status: str, new_status: str) -> None:
        """Update status in entity page and potentially index."""
        entity_path = self.wiki_root / "entities" / f"{project_name}.md"
        if entity_path.exists():
            self._update_entity_page(
                ProjectMetadata(
                    name=project_name,
                    path=Path(),
                    language="",
                    status=new_status,
                    description="",
                    file_count=0,
                    pyproject_exists=False,
                    readme_exists=False,
                    dockerfile_exists=False,
                    dependencies={},
                    last_modified="",
                    has_tests=False,
                )
            )

    def _update_infrastructure_map(self, dependency_changes: list[dict]) -> None:
        """Update Shared Infrastructure Map with new dependencies."""
        map_path = self.wiki_root / "synthesis" / "Shared-Infrastructure-Map.md"
        if not map_path.exists():
            self.log(f"Infrastructure map {map_path} not found")
            return

        if self.dry_run:
            self.log(f"[DRY RUN] Would update {map_path}")
            return

        # Add a note about what changed
        content = map_path.read_text()
        if "<!-- LAST SYNC UPDATE -->" not in content:
            update_note = "\n\n<!-- LAST SYNC UPDATE -->\n"
            update_note += f"*Last automated sync: {datetime.now().isoformat()}*\n"
            content = content.rstrip() + update_note
            map_path.write_text(content)
            self.log(f"Updated {map_path} with sync timestamp")


class WikiSyncManager:
    """Main wiki sync orchestrator."""

    def __init__(self, wiki_root: Path, verbose: bool = False, dry_run: bool = False):
        """Initialize sync manager."""
        self.wiki_root = wiki_root
        self.state_file = wiki_root / ".last-sync.json"
        self.verbose = verbose
        self.dry_run = dry_run
        self.scanner = ProjectScanner(verbose=verbose)
        self.detector = ChangeDetector(verbose=verbose)
        self.updater = WikiUpdater(wiki_root, verbose=verbose, dry_run=dry_run)

    def run(self) -> dict[str, Any]:
        """Run the full sync process."""
        print(f"🔄 Wiki Auto-Sync starting... (dry_run={self.dry_run})")
        print(f"   Workspace roots: {len(self.scanner.WORKSPACE_ROOTS)}")
        print(f"   State file: {self.state_file}")

        # Step 1: Scan projects
        current_projects = self.scanner.scan_all()
        print(f"✓ Scanned {len(current_projects)} projects")

        # Step 2: Load last state
        last_state = self._load_state()
        print(f"✓ Loaded last sync state ({len(last_state.get('projects', {}))} projects)")

        # Step 3: Detect changes
        changes = self.detector.detect_changes(current_projects, last_state)
        total_changes = sum(len(v) if isinstance(v, list) else 0 for v in changes.values())
        print(f"✓ Detected {total_changes} changes")

        # Step 4: Apply changes to wiki
        if total_changes > 0:
            summary = self.updater.apply_changes(changes, current_projects, last_state)
            print(f"✓ Applied changes: {len(self.updater.updates_made)} updates")
            for update in self.updater.updates_made:
                print(f"   - {update}")
        else:
            summary = {
                "pages_updated": [],
                "new_projects_documented": [],
                "status_updates": [],
            }
            print("✓ No changes detected")

        # Step 5: Update log.md
        self._update_log(changes, summary)

        # Step 6: Save new state
        if not self.dry_run:
            self._save_state(current_projects)
            print("✓ Saved new sync state")
        else:
            print("✓ [DRY RUN] Would save new state")

        print(f"\n✅ Wiki sync complete")
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "changes_detected": total_changes,
            "changes": changes,
            "summary": summary,
            "dry_run": self.dry_run,
        }

    def _load_state(self) -> dict[str, Any]:
        """Load last sync state from file."""
        if self.state_file.exists():
            return json.loads(self.state_file.read_text())
        return {"last_sync": None, "projects": {}}

    def _save_state(self, projects: dict[str, ProjectMetadata]) -> None:
        """Save current state to file."""
        state = {
            "last_sync": datetime.now().isoformat(),
            "projects": {
                name: {
                    "name": p.name,
                    "language": p.language,
                    "status": p.status,
                    "description": p.description,
                    "file_count": p.file_count,
                    "dependencies": p.dependencies,
                    "last_modified": p.last_modified,
                    "has_tests": p.has_tests,
                    "path": str(p.path),
                }
                for name, p in projects.items()
            },
        }
        self.state_file.write_text(json.dumps(state, indent=2, default=str))

    def _update_log(self, changes: dict[str, Any], summary: dict[str, Any]) -> None:
        """Update wiki log with sync results."""
        log_path = self.wiki_root / "log.md"
        if not log_path.exists():
            print(f"Warning: Log file {log_path} not found")
            return

        if self.dry_run:
            print(f"[DRY RUN] Would update {log_path}")
            return

        # Create log entry
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = f"\n## [{timestamp}] AUTO-SYNC | Automated Wiki Monitoring\n\n"
        entry += "- **Type:** Automated sync (Phase 6)\n"

        if sum(len(v) if isinstance(v, list) else 0 for v in changes.values()) > 0:
            entry += f"- **Changes Detected:** {sum(len(v) if isinstance(v, list) else 0 for v in changes.values())}\n"

            if changes.get("new_projects"):
                entry += f"- **New Projects:** {', '.join(changes['new_projects'])}\n"

            if changes.get("status_changes"):
                for change in changes["status_changes"]:
                    entry += f"  - {change['project']}: {change['old']} → {change['new']}\n"

            if changes.get("modified_projects"):
                entry += f"- **Modified:** {len(changes['modified_projects'])} projects\n"

            if changes.get("dependency_changes"):
                entry += f"- **Dependency Changes:** {len(changes['dependency_changes'])} projects\n"

            entry += f"- **Pages Updated:** {', '.join(summary.get('pages_updated', []))}\n"
        else:
            entry += "- **Result:** No changes detected\n"

        entry += f"- **Status:** ✓ COMPLETE\n"

        # Read current log
        content = log_path.read_text()

        # Insert new entry after header
        lines = content.split("\n")
        header_end = 0
        for i, line in enumerate(lines):
            if line.startswith("Format:"):
                header_end = i + 1
                break

        new_content = "\n".join(lines[: header_end + 1]) + entry + "\n" + "\n".join(lines[header_end + 1 :])

        log_path.write_text(new_content)
        print(f"✓ Updated log.md")


def main() -> int:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="LLM Wiki Auto-Sync")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument(
        "--wiki-root",
        type=Path,
        default=Path("/mnt/c/Users/Chaddle/Documents/ObsidianVault/Wiki"),
        help="Path to wiki root",
    )

    args = parser.parse_args()

    manager = WikiSyncManager(
        wiki_root=args.wiki_root, verbose=args.verbose, dry_run=args.dry_run
    )

    try:
        result = manager.run()
        return 0 if result["success"] else 1
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback

            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

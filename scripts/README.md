# Wiki Auto-Sync Script

Automated monitoring and wiki updates. Keeps your workspace projects synchronized with wiki pages.

## Quick Start

### View what would change (safe to run anytime)
```bash
cd /mnt/c/Users/Chaddle/Documents/ObsidianVault
python3.12 scripts/sync-wiki.py --verbose --dry-run
```

### Apply changes
```bash
python3.12 scripts/sync-wiki.py --verbose
```

### Run silently (no output)
```bash
python3.12 scripts/sync-wiki.py
```

## What It Does

1. **Scans** all workspace projects (20+ projects across 4 roots)
2. **Detects** changes since last sync
3. **Updates** wiki entity pages, synthesis pages, and log.md
4. **Saves** new state to `.last-sync.json`

## Change Types Detected

- ✅ New projects (auto-documents them)
- ✅ Project status changes (active → archived, etc.)
- ✅ File modifications (last modified timestamp)
- ✅ Dependency updates
- ✅ Removed projects (logs, doesn't delete wiki pages)

## Files Modified

- `Wiki/entities/*.md` — Project entity pages (status, metadata)
- `Wiki/synthesis/Shared-Infrastructure-Map.md` — Dependency updates
- `Wiki/log.md` — Operation log with summary
- `Wiki/.last-sync.json` — State file (DO NOT EDIT MANUALLY)

## Options

```
--dry-run       Preview changes without applying them (SAFE)
--verbose, -v   Show detailed output
--wiki-root     Custom wiki path (default: /mnt/c/Users/Chaddle/Documents/ObsidianVault/Wiki)
```

## Automated (GitHub Actions)

Runs automatically every Monday at 9 AM UTC.

**Manual trigger:** Go to GitHub Actions → Wiki Auto-Sync → Run workflow → Run workflow

## Troubleshooting

### "No changes detected" (but I know something changed)

```bash
# Remove state file and rescan
rm Wiki/.last-sync.json
python3.12 scripts/sync-wiki.py --verbose
```

### "Error scanning project"

Check the verbose output for which project failed. Fix manually, then re-run.

### "Permission denied"

Ensure `scripts/sync-wiki.py` is readable:
```bash
chmod +x scripts/sync-wiki.py
```

## For More Details

See: `Wiki/synthesis/Phase-6-Automated-Monitoring.md`

---

**Phase 6 Status:** ✅ COMPLETE

# Development Logs

This directory contains timestamped development logs organized by date.

## Structure

```
dev-logs/
├── YYYY/
│   └── MM/
│       └── DD/
│           ├── copilot-HHMMSS-description.md    # GitHub Copilot sessions
│           ├── codex-HHMMSS-description.md      # Codex agent sessions
│           └── mohsin-HHMMSS-description.md     # Human developer sessions
```

## Contributors

| ID | Contributor | Description |
|----|-------------|-------------|
| `copilot` | GitHub Copilot Agent | VS Code integrated AI assistant |
| `codex` | Codex Agent | OpenAI Codex-based agent |
| `mohsin` | Mohsin (Human) | Primary developer |

## Naming Convention

**Format:** `{contributor}-{HHMMSS}-{short-description}.md`

**Examples:**
- `copilot-143022-project-setup.md`
- `codex-161500-pdf-reader-impl.md`
- `mohsin-092030-architecture-decisions.md`

## Rules

1. **Append Only** - Never delete or modify other contributors' logs
2. **Timestamped** - Always include time in filename for ordering
3. **Descriptive** - Use short but meaningful descriptions
4. **Self-Contained** - Each log should be readable independently

## Log Template

Each log file should follow this structure:

```markdown
# {Description}

**Date:** YYYY-MM-DD HH:MM:SS  
**Contributor:** {copilot|codex|mohsin}  
**Duration:** {estimated time}  
**Status:** {in-progress|completed|blocked}

---

## Goals
- [ ] Goal 1
- [ ] Goal 2

## Work Done
### HH:MM - Action taken
Description of what was done...

## Decisions Made
- Decision 1: Rationale

## Next Steps
- [ ] Next action item

## Notes
Any additional observations...
```

## Quick Commands

Create a new log entry:
```bash
# For Copilot
touch "docs/dev-logs/$(date +%Y/%m/%d)/copilot-$(date +%H%M%S)-description.md"

# For Codex
touch "docs/dev-logs/$(date +%Y/%m/%d)/codex-$(date +%H%M%S)-description.md"

# For Mohsin
touch "docs/dev-logs/$(date +%Y/%m/%d)/mohsin-$(date +%H%M%S)-description.md"
```

Create today's folder:
```bash
mkdir -p "docs/dev-logs/$(date +%Y/%m/%d)"
```

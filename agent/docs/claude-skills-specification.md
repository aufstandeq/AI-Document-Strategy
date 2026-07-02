# Claude Native Agent Skills Specification

## Document Status
Approved

## Purpose
Reference guide for formatting, configuring, and executing native Agent Skills.

## Owner
Architecture Team

## Last Updated
2026-07-02

---

See [Glossary](../../glossary.md) for definitions of key terms.

---

## 1. Directory Structure & Discovery

In filesystem-based environments (like Claude Code), native custom skills are defined as directories containing a required `SKILL.md` entry point:

```text
skills/my-skill/
├── SKILL.md                  # YAML frontmatter + main instructions (required)
├── reference.md              # Detailed API specs (loaded lazily)
├── examples.md               # Code examples (loaded lazily)
└── scripts/
    └── helper.py             # Executable script (called from SKILL.md)
```

### Discovery Locations:
*   **Project-scoped:** `.claude/skills/<skill-name>/SKILL.md` (or custom paths specified in the workspace's `.agents/skills/` customizations folder).
*   **Personal-scoped:** `~/.claude/skills/<skill-name>/SKILL.md` (applies to all projects).

---

## 2. YAML Frontmatter Configuration

At the top of the `SKILL.md` file, behavior can be customized using YAML frontmatter properties enclosed by `---` markers:

| Field | Required | Description |
| :--- | :--- | :--- |
| `name` | No | Display name shown in skill listings. Defaults to the directory name. |
| `description` | Recommended | Truncated at 1,536 characters combined with `when_to_use`. Claude uses this to decide when to automatically trigger the skill. |
| `when_to_use` | No | Additional trigger phrases or request examples to assist auto-invocation. |
| `argument-hint` | No | Hint shown during autocomplete (e.g. `[issue-number]`). |
| `arguments` | No | List of named positional arguments for `$name` substitution in the content. |
| `disable-model-invocation` | No | Set to `true` to require manual execution via `/skill-name` (disables auto-invocation). |
| `user-invocable` | No | Set to `false` to hide the skill from the `/` menu (useful for background knowledge skills). |
| `allowed-tools` | No | Tools Claude can run without asking for permission while the skill is active. |
| `disallowed-tools` | No | Tools disabled while active (e.g. `AskUserQuestion` to force non-interactive execution). |
| `model` | No | Model override for the current turn. |
| `effort` | No | Effort level override (`low`, `medium`, `high`, `xhigh`, `max`). |
| `context` | No | Set to `fork` to run the skill in a clean, isolated subagent context. |
| `agent` | No | Subagent executor type to use when `context: fork` (e.g. `Explore` or `Plan`). |
| `paths` | No | Glob patterns limiting activation. Loaded only when working on matching files. |
| `shell` | No | Shell program used for commands (defaults to `bash`, supports `powershell`). |

---

## 3. String Substitutions

Dynamic session variables can be injected into the skill body:

*   `$ARGUMENTS` — The full argument string as typed in the terminal.
*   `$ARGUMENTS[N]` or `$N` — 0-based positional argument (e.g. `$0` is the first argument).
*   `$name` — Named argument declared in the `arguments` frontmatter list.
*   `${CLAUDE_SESSION_ID}` — The active session ID (useful for logging).
*   `${CLAUDE_EFFORT}` — The current effort level (`low`, `medium`, `high`, `xhigh`, `max`).
*   `${CLAUDE_SKILL_DIR}` — Absolute path to the skill directory containing the `SKILL.md` file. Allows referencing local scripts (e.g. `${CLAUDE_SKILL_DIR}/scripts/helper.py`).
*   `${CLAUDE_PROJECT_DIR}` — Absolute path to the project root directory.

---

## 4. Dynamic Context Injection (Shell Execution)

You can execute local shell commands before the skill is sent to the model. The output of the command is injected directly as plain text.

### Inline Command Syntax:
Use the `!` followed by backticks at the start of a line or after whitespace:
```markdown
Here is the active diff:
!`git diff`
```

### Multi-Line Command Block:
Use a fenced code block opened with ````!`:
```markdown
## Environment Info
```!
node --version
npm --version
git status --short
```
```

---

## 5. Forking Execution Context

Setting `context: fork` runs the skill as a one-shot task in a forked subagent (e.g., `agent: Explore` or `agent: Plan`).
*   Forked subagents run in isolation and do not have access to the parent conversation history.
*   The built-in `Explore` and `Plan` agents skip loading `CLAUDE.md` and `git status` to keep context windows small.

---

## 6. Best Practices

1.  **Keep the Body Concise:** Native skills stay in context across turns once loaded. Minimize long descriptions or narration to save token costs.
2.  **Use Paths Scoping:** Restrict skill activation to specific folders (e.g., `paths: ['apps/backend/**/*', 'libs/**/*']` for backend skills) to prevent irrelevant skills from cluttering the context window.
3.  **Defer Documentation:** Store large API specifications or examples in separate files in the directory (e.g. `reference.md`) and reference them with relative links in `SKILL.md`. Claude will load them only when required.

# Codex project instructions — VLM research handoff

This is the **public document-coordination checkout** for floomeer83felix-source/vlm, NOT the local Windows RTX 3090 experimental workspace. The experimental workspace may be a separate non-Git directory. Never upload that workspace or infer its state from this public repository.

## Collaboration roles

- **ChatGPT** owns research review, scientific conclusions, `docs/next-steps.md` (task READY/BLOCKED status), and `docs/research-overview.md` (rolling decisions).
- **Codex** acts only as a bounded local executor for **one authorized task per session**; it uploads sanitized factual evidence under `docs/codex-artifacts/<task-id>/` and appends a task entry to `docs/codex-results.md`.
- **User** decides whether/when to start a Codex session and must explicitly authorize restricted GPU/model, data download, env migration, protected labels, background monitoring, or PR merge actions.
- No GitHub Issue alerts. This document does not authorize continuous Codex background work.

## At the beginning of every NEW Codex session

1. Read the local `AGENTS.md` (this file) and **refresh only the separate document checkout**, not the original experiment directory. If Git is available and this is the docs checkout:
   - `git status --short`
   - `git fetch origin main`
   - `git show origin/main:docs/next-steps.md`
   - `git show origin/main:docs/codex-results.md`
   - `git show origin/main:docs/research-overview.md`
   - If the local checkout is clean and can safely fast-forward, update it to `origin/main` before edits; otherwise STOP and report the conflict. Never reset, rebase, force-push, or discard local changes.
   - Remote task state takes precedence over stale local docs; do not use cached READY assignments.
2. Identify the **exactly one** READY task from the latest task board. Confirm that the same task-ID has **not** already been reported as complete in `docs/codex-results.md`. If no READY task, conflicting instructions, or completed task, STOP without work.
3. Read the task-specific README under `docs/codex-artifacts/<task-id>/` plus any specific source documents named by the task. Do not scan unrelated private research files.
4. State scope and constraints briefly. Only perform the approved task; BLOCKED tasks stay blocked even if current work is fast.
5. Before GitHub upload, review and stage **only** the named permitted sanitized report and append-only `docs/codex-results.md`. Verify `git diff --cached --name-only` and contents for sensitive information. Never alter ChatGPT-owned planning files, historic logs, or PR #1 without a new explicit instruction.
6. Commit/push the results safely to `main` (no force push), then STOP. ChatGPT reviews and writes the next assignment. If push fails, disclose the failure and leave work locally; no silent retries or bypasses.

## Current research controls (higher-priority task rules may be stricter)

- User's Windows RTX 3090 + 64 GiB machine and existing conda `pytorch` environment must be preserved; no new environments, Python/Torch/CUDA changes, paid APIs, cloud GPU or new manual evidence labels.
- Do not re-run already started historic QA forwards; obey persistent ledger and OS lock policy. Never delete lockfiles or kill another job based on uncertainty.
- GPU/model inference, decoding protected video, training, full dataset downloads, and autonomous continuation are **NOT** authorized by this AGENTS.md. Look at `docs/next-steps.md` and user authorization for exact scope.
- Keep source identity and protected scoring answers separate from any observation/selection policy. Errors/invalid answers remain in full planned denominator during approved future experiments.
- Never upload model weights, video, full QA logs, restricted media, raw answer labels, credentials, personally identifying full paths or source reidentification maps to this public repository.
- The initial methodological hypothesis and all novelty claims remain tentative; consult `docs/research-overview.md`, not memory, as the latest signed-off scientific position.
- **Stop when blocked**; write UNKNOWN and return control instead of inventing data or spending quota investigating a closed path.

## Note on watching for new instructions

Codex's repo guidance is loaded **when a new session starts**; simply updating `AGENTS.md` on GitHub does not wake an idle local Codex or update an already open session. There is **no authorized always-on Codex watch** here. A separate ChatGPT periodic check may review new pushed results, but its writes should be verified from GitHub. At the user's next Codex session, fetch/read the latest `docs/next-steps.md` and execute only the new READY task.

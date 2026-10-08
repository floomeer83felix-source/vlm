# Codex project instructions — VLM research handoff

This is the **public document-coordination checkout** for floomeer83felix-source/vlm, NOT the local Windows RTX 3090 experimental workspace. The experimental workspace may be a separate non-Git directory. Never upload that workspace or infer its state from this public repository.

## Collaboration roles

- **ChatGPT** owns research review, scientific conclusions, `docs/next-steps.md` (task READY/BLOCKED status), and `docs/research-overview.md` (rolling decisions).
- **Codex** acts only as a bounded local executor for **one authorized task per execution round (one user message in the SAME long-running Codex chat)**; it uploads sanitized factual evidence under `docs/codex-artifacts/<task-id>/` and appends a task entry to `docs/codex-results.md`.
- **User** normally keeps one Codex conversation throughout the project. After ChatGPT updates the GitHub plan, the user sends a short message in that SAME conversation to start the next round. Restricted GPU/model operations, data download, environment migration, protected labels, background monitoring, and PR merge still require explicit authorization.
- No GitHub Issue alerts. This document does not authorize continuous Codex background work.

## At the start of EVERY execution round (reuse the SAME Codex conversation)

1. **Do not rely on previous chat context or cached task states.** In the existing Codex conversation, when the user says to continue or check for the next task, reread this file if available and **refresh only the separate GitHub document checkout**, never the original experimental directory. If Git is available in the docs checkout:
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

## Optional no-model 30-minute READY check (Windows)

The user approved a **cheap Git/PowerShell gate** to avoid waking Codex on every poll. The Windows script [`tools/watch-ready-task.ps1`](./tools/watch-ready-task.ps1), documented in [`docs/automation/windows-ready-watch.md`](./docs/automation/windows-ready-watch.md), can be run by **Windows Task Scheduler** every 30 minutes after the user sets it up locally. It only fetches and reads `main`, checks whether one READY task is not already reported, and writes a local de-duplicated pending-task note under `%LOCALAPPDATA%\VLMResearch\TaskWatch\`. It **never** invokes a Codex model or starts a GPU experiment.

**Critical:** This lightweight checker cannot inject a turn into an already-open Codex desktop chat. When the user sees a new pending task, they send a short continuation instruction in the SAME Codex chat. A Codex native thread automation can run unattended within the existing conversation, but its half-hourly wake-ups may consume quota even without a new task; do not claim the cheap gate automatically wakes the existing thread. Do not configure a fully autonomous Codex CLI runner or new conversations unless the user separately approves a change in workflow.

## One persistent chat and how to check new instructions

**The user intends to use ONE continuous Codex chat for the entire project. Do not ask them to create a new session.** Initial repository instructions may have been read earlier, but remote edits to `AGENTS.md` or `docs/next-steps.md` do **not** automatically refresh the already-open chat. At each new user instruction, run safe `git fetch origin main` in the separate documentation checkout (or fetch the latest file contents from GitHub when no checkout is available), then reread `docs/next-steps.md`, `docs/codex-results.md`, and the task-specific README. Treat repository `main` as the current authority, not previously pasted or cached text. Only execute the one READY task if no matching completed result already exists; otherwise stop and report why.

The user may paste this minimal message **in the SAME chat**: “继续下一轮：先安全同步 GitHub 文档仓库 main，重新读取 AGENTS.md、docs/next-steps.md、docs/codex-results.md，只执行尚未交付的唯一 READY 任务，按要求上传报告后停止。”

No constant Codex polling or self-waking has been authorized. ChatGPT may check GitHub hourly and revise the plan, but it **cannot send a new message directly into the existing Codex chat**, and changing a GitHub file alone never wakes Codex. The user triggers each next execution round by messaging the existing Codex chat, without resetting the conversation.

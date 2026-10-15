# Codex project instructions — VLM research handoff

This is the **public document-coordination checkout** for floomeer83felix-source/vlm, NOT the local Windows RTX 3090 experimental workspace. The experimental workspace may be a separate non-Git directory. Never upload that workspace or infer its state from this public repository.

## Collaboration roles

- **ChatGPT** owns research review, scientific conclusions, `docs/next-steps.md` (task READY/BLOCKED status), and `docs/research-overview.md` (rolling decisions).
- **Codex** acts as a bounded local executor for **one authorized READY parent task or explicitly defined multi-part task bundle per execution round (one new user message in the currently active Codex chat; a user-initiated, GitHub-synchronized handoff after context compaction is allowed)**. A READY bundle may include multiple named low-risk subtasks, executed consecutively without intermediate ChatGPT approvals only within its exact authorized scope. It uploads sanitized evidence under `docs/codex-artifacts/<parent-task-id>/` and appends one parent-level task result to `docs/codex-results.md`.
- **User** prefers retaining the current Codex conversation while useful, compacting context once when near capacity, and **may move to a new Codex conversation if compacted context fills again**. A new conversation is a handoff, not a reset or a new parent-task authorization. After ChatGPT updates the GitHub plan, the user sends one fresh instruction in the currently active Codex conversation to start the next round. Restricted GPU/model operations, data download, environment migration, protected labels, background monitoring, and PR merge still require explicit authorization.
- No GitHub Issue alerts. This document does not authorize continuous Codex background work.

## At the start of EVERY execution round (active Codex conversation, including after an authorized chat handoff)

1. **Do not rely on previous chat context or cached task states.** In the currently active Codex conversation, including a new one created after context compaction, when the user says to continue or check for the next task, reread this file if available and **refresh only the separate GitHub document checkout**, never the original experimental directory. If Git is available in the docs checkout:
   - `git status --short`
   - `git fetch origin main`
   - `git show origin/main:docs/next-steps.md`
   - `git show origin/main:docs/codex-results.md`
   - `git show origin/main:docs/research-overview.md`
   - If the local checkout is clean and can safely fast-forward, update it to `origin/main` before edits; otherwise STOP and report the conflict. Never reset, rebase, force-push, or discard local changes.
   - Remote task state takes precedence over stale local docs; do not use cached READY assignments.
2. Identify the **exactly one** READY **parent task or task bundle** from the latest task board. Confirm that the parent task-ID has **not** already received a completed, partial, or blocked result entry in `docs/codex-results.md`. If none, multiple READY parents, conflicting instructions, or a previously reported parent, STOP without work. A subtask marked INCLUDED IN BATCH is **not** a separately READY task.
3. Read the parent-task README under `docs/codex-artifacts/<parent-task-id>/` and explicitly referenced sources. For a multi-part bundle, work through its ordered safe subtasks, recording UNKNOWN/BLOCKED if one is unsupported; if the README permits independent work to continue, finish other non-risky subtasks without requiring a new chat message. Do not scan unrelated private research files.
4. State scope and constraints briefly. Perform **only** the approved single task or defined subtask bundle. No follow-on work after the bundle, no GPU/model inference without user approval, and BLOCKED tasks remain BLOCKED even if current work is fast.
5. Before GitHub upload, review and stage **only** the parent README's allowed sanitized subtask reports and append-only `docs/codex-results.md`. Bundle completion needs **one parent-level results entry** with links and status for each subtask, and one safe push when possible. Verify `git diff --cached --name-only` and contents for sensitive information. Never alter ChatGPT-owned planning files, historic logs, or PR #1 without a new explicit instruction.
6. Commit/push the bundle results safely to `main` (no force push), then STOP the **execution round**; normally keep the current Codex chat, but the user may hand off to a new chat when it is full. ChatGPT reviews the entire batch and writes the next assignment. If push fails, disclose failure and leave work locally; no silent retries or bypasses.

## Current research controls (higher-priority task rules may be stricter)

- User's Windows RTX 3090 + 64 GiB machine and existing conda `pytorch` environment must be preserved; no new environments, Python/Torch/CUDA changes, paid APIs, cloud GPU or new manual evidence labels.
- Do not re-run already started historic QA forwards; obey persistent ledger and OS lock policy. Never delete lockfiles or kill another job based on uncertainty.
- GPU/model inference, decoding protected video, training, full dataset downloads, and autonomous continuation are **NOT** authorized by this AGENTS.md. Look at `docs/next-steps.md` and user authorization for exact scope.
- Keep source identity and protected scoring answers separate from any observation/selection policy. Errors/invalid answers remain in full planned denominator during approved future experiments.
- Never upload model weights, video, full QA logs, restricted media, raw answer labels, credentials, personally identifying full paths or source reidentification maps to this public repository.
- The initial methodological hypothesis and all novelty claims remain tentative; consult `docs/research-overview.md`, not memory, as the latest signed-off scientific position.
- **Stop when blocked**; write UNKNOWN and return control instead of inventing data or spending quota investigating a closed path.

## Chat continuity, compaction, handoff, and how to check new instructions

**Prefer one persistent Codex chat, then context compaction when needed. If the compacted chat fills again, the user may create a new chat and paste a GitHub-first handoff instruction.** Do not demand a new chat on every round, but do not reject a genuine context-limit handoff. The new chat must treat the newest GitHub AGENTS/next-steps/codex-results/research-overview/task README as authoritative, not a copied old conversation summary; never inherit completed-task permissions, GPU budgets or media GET allowances. Previously completed/blocked parent IDs remain non-rerunnable. Handoff itself authorizes **no** model, GPU, download, protected QA access or system change. Initial repository instructions may have been read earlier, but remote edits to `AGENTS.md` or `docs/next-steps.md` do **not** automatically refresh the already-open chat. At each new user instruction, run safe `git fetch origin main` in the separate documentation checkout (or fetch the latest file contents from GitHub when no checkout is available), then reread `docs/next-steps.md`, `docs/codex-results.md`, and the task-specific README. Treat repository `main` as the current authority, not previously pasted or cached text. Execute only the single READY parent or its explicitly authorized subtask bundle if no matching parent result exists; otherwise stop and report why.

The user may paste this minimal message **in the currently active chat, including a newly handed-off chat**: “继续下一轮：安全同步GitHub文档仓库main，重新读取AGENTS.md、docs/next-steps.md、docs/codex-results.md，执行唯一尚未交付的READY父任务包；依任务包README连续完成其允许的安全子任务，统一上传报告后停止，不做BLOCKED/GPU任务。”

No constant Codex polling or self-waking has been authorized. ChatGPT may check GitHub hourly and revise the plan, but it **cannot send a new message directly into the existing Codex chat**, and changing a GitHub file alone never wakes Codex. The user triggers each next execution round by messaging their current active Codex chat; if a new conversation was needed after compaction, first synchronize and re-read GitHub, then follow the same one-READY/one-authorized-round discipline.

# Watch for an unreported READY task without invoking Codex or any model.
# Windows PowerShell 5.1+; requires Git and the separate public docs checkout.
# This file never writes to the research workspace or GitHub.
param(
    [Parameter(Mandatory = $true)]
    [string]$DocsRepo,
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Invoke-ReadGit {
    param([string[]]$Arguments)
    $outputLines = @(& git -C $DocsRepo @Arguments 2>&1)
    if ($LASTEXITCODE -ne 0) {
        throw ("git {0} failed (exit {1}): {2}" -f ($Arguments -join ' '), $LASTEXITCODE, ($outputLines -join ' '))
    }
    return ($outputLines -join "`n")
}

try {
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        throw 'Git executable is unavailable.'
    }
    $DocsRepo = (Resolve-Path -LiteralPath $DocsRepo -ErrorAction Stop).Path
    if (-not (Test-Path -LiteralPath (Join-Path $DocsRepo '.git'))) {
        throw 'DocsRepo must be the GitHub documentation checkout, not the non-Git experiment workspace.'
    }
    $remote = (Invoke-ReadGit @('remote', 'get-url', 'origin')).Trim()
    if ($remote -notmatch '^(?i:(https://github[.]com/|git@github[.]com:))floomeer83felix-source/vlm([.]git)?/?$') {
        throw 'origin is not the expected GitHub repo; refusing to fetch.'
    }

    # Fetch remote tracking information only; do not change current branch/worktree.
    [void](Invoke-ReadGit @('fetch', '--quiet', '--no-tags', 'origin', 'main'))
    $sha = (Invoke-ReadGit @('rev-parse', 'refs/remotes/origin/main')).Trim()
    $board = Invoke-ReadGit @('show', 'refs/remotes/origin/main:docs/next-steps.md')
    $results = Invoke-ReadGit @('show', 'refs/remotes/origin/main:docs/codex-results.md')

    $ready = @()
    foreach ($line in ($board -split "\r?\n")) {
        if ($line -notmatch '^\|\s*(VLM-[A-Za-z0-9-]+)\s*\|') { continue }
        $columns = $line.Split('|')
        if ($columns.Count -lt 6) { continue }
        $taskId = $columns[1].Trim()
        $status = $columns[3].Replace('*', '').Trim()
        if ($status -match '^READY($|[\s(（])') { $ready += $taskId }
    }
    $ready = @($ready | Select-Object -Unique)

    if ($ready.Count -gt 1) {
        throw "More than one READY task in main: $($ready -join ', '). Refusing automatic dispatch."
    }

    $stateDir = Join-Path $env:LOCALAPPDATA 'VLMResearch\TaskWatch'
    $stateFile = Join-Path $stateDir 'last-notified.json'
    $pendingFile = Join-Path $stateDir 'pending-task.txt'

    $id = if ($ready.Count -eq 1) { $ready[0] } else { $null }
    if ($id) {
        $completedPattern = '(?m)^###\s+' + [regex]::Escape($id) + '(?:\s|$)'
        if ([regex]::IsMatch($results, $completedPattern)) { $id = $null }
    }

    if (-not $id) {
        if (-not $DryRun -and (Test-Path -LiteralPath $pendingFile)) {
            Remove-Item -LiteralPath $pendingFile -Force
        }
        Write-Output 'NO_NEW_TASK'
        exit 0
    }

    $lastTask = ''
    if (Test-Path -LiteralPath $stateFile) {
        try {
            $saved = Get-Content -LiteralPath $stateFile -Raw | ConvertFrom-Json
            $lastTask = [string]$saved.task_id
        } catch {
            # A corrupted local cache must not authorize repeated execution.
            throw 'Local notification state is unreadable. Inspect it manually before retrying.'
        }
    }
    if ($lastTask -eq $id) {
        Write-Output "ALREADY_NOTIFIED $id"
        exit 0
    }

    Write-Output "NEW_READY_TASK $id at remote main $sha"
    if ($DryRun) { exit 0 }

    New-Item -Path $stateDir -ItemType Directory -Force | Out-Null
    $note = @(
        "New authorized task: $id",
        "Remote commit: $sha",
        "Task board: https://github.com/floomeer83felix-source/vlm/blob/main/docs/next-steps.md",
        'In the EXISTING Codex chat, say:',
        '继续下一轮：安全刷新独立GitHub文档checkout的main，重新读取AGENTS.md、next-steps.md和codex-results.md，只执行尚未交付的唯一READY任务，上传脱敏报告后停止。'
    ) -join "`r`n"
    # Create a local note. No automatic Codex/model invocation.
    [System.IO.File]::WriteAllText($pendingFile, $note, [System.Text.UTF8Encoding]::new($false))
    $stateJson = @{
        task_id = $id
        detected_main_sha = $sha
        first_seen_utc = (Get-Date).ToUniversalTime().ToString('o')
    } | ConvertTo-Json -Depth 3
    [System.IO.File]::WriteAllText($stateFile, $stateJson, [System.Text.UTF8Encoding]::new($false))
    Write-Output "PENDING_NOTE $pendingFile"
    exit 0
}
catch {
    Write-Error ("VLM watcher stopped safely: " + $_.Exception.Message)
    exit 2
}

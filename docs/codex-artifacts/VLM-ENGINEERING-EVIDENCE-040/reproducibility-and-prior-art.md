# 040 reproducibility and prior-art decision

2026-10-24. **NO_DISTINCT_MECHANISM_EVIDENCE.** Strong SQLite B1 matched F's
tested protection/availability goals. These are new self-implemented reference
profiles, not performance substitutes for MLflow, Ray or lmms-eval.

## Standalone public package and scope

Only three Python files are required:

- [auditable_runner_040.py](../../../prototypes/auditable_runner_040.py): shared
  controlled CPU worker, policy/storage/receipts, suspended-before-Job launch.
- [benchmark_auditable_runner_040.py](../../../prototypes/benchmark_auditable_runner_040.py):
  independent fault observer, fixed540 queue, CSV and clean-directory driver.
- [test_auditable_runner_040.py](../../../prototypes/test_auditable_runner_040.py):
  twelve test methods including six real process cells, isolated from formal data.

Actually measured platform:64-bit Python3.12.7 (existing Anaconda distribution),
Windows11 build26200. Standard library only, no installation. Windows Job APIs
and nested Job support are required. Other OS/interpreter/machine combinations
were not tested. No Python/Torch environment was modified.

At process creation the work is suspended, assigned to its owned non-breakaway
Job, then resumed. Descendants inherit that Job. Registered-descendant identity
is verified before querying it; only owned process handles/Jobs are cleaned.
This is process-fault containment, not an adversarial filesystem/network sandbox,
device execution proof or machine-wide immutability guarantee.

## Reproduction commands (new directory, no personal paths)

From a checkout containing the three public files, in PowerShell:

```powershell
$volume = [IO.Path]::GetPathRoot($env:TEMP)
if ([IO.DriveInfo]::new($volume).AvailableFreeSpace -lt (128MB + 2GB)) {
    throw 'Insufficient output quota plus 2GiB headroom'
}
$clean040 = Join-Path $env:TEMP ('VLM040-repro-' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $clean040 | Out-Null
Copy-Item -LiteralPath @(
    'prototypes/auditable_runner_040.py',
    'prototypes/benchmark_auditable_runner_040.py',
    'prototypes/test_auditable_runner_040.py'
) -Destination $clean040
python -I -S -B (Join-Path $clean040 'auditable_runner_040.py') --help
python -I -S -B (Join-Path $clean040 'benchmark_auditable_runner_040.py') clean --root $clean040
```

The `clean` driver itself checks all three help commands, one standalone normal
demo and twelve fixed cells. It loads siblings only by their exact __file__
directory with importlib; no cwd/PYTHONPATH or installed package dependency.
Use a new root per invocation; no overwrite/reset of old claims. A new full
formal dataset is an explicit separate command, not part of the small clean check:

```powershell
python -I -S -B (Join-Path $clean040 'benchmark_auditable_runner_040.py') formal --root (Join-Path $clean040 'formal')
```

These commands describe reproducibility; this040 round did not execute a second
formal dataset. The CLI has per-cell5s and an885s formal loop budget; this round
also used a separate owning Job supervisor with900s formal/120s clean limits.
For strict reproduction of that outer envelope, the public Job/Process API can
supervise the clean CLI as follows, using the same new source directory:

```python
# Supply the newly copied source directory as sys.argv[1].
import importlib.util, sys, time
from pathlib import Path
root = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location('runner040', root/'auditable_runner_040.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
j = r.Job()
p = None
deadline = time.monotonic() + 120
try:
    p = r.Process([sys.executable, '-I', '-S', '-B',
                   str(root/'benchmark_auditable_runner_040.py'),
                   'clean', '--root', str(root)], root/'outer-clean.log', j)
    assert p.wait(deadline-2) == 0
finally:
    if not j.empty(min(deadline-.5, time.monotonic()+.25)):
        j.kill()  # only this newly owned Job
    assert j.empty(deadline)
    if p is not None:
        p.close()
    j.close()
```

Run either clean invocation once in its new root, not both examples in the same
root. New-suite CLI is `python -I -S -B test_auditable_runner_040.py --root NEW_PATH`;
the supplied path must not already exist. CLI help has no actual work entry.

## Actual clean-directory outcome

All three copied source hashes matched the formal seal. No earlier public
research runner, private helper/config, package, model or research asset was
imported/read. The actual check reported forbidden_imports=[] both in its
matrix and its clean-driver result. No GPU/query/model code exists here.

|family|profile|actual work|terminal|legal completion|violations|group0|
|---|---|---|---|---|---|---|
|N1K|B0|1|RETURNED|True|-|True|
|N1K|B1|1|RETURNED|True|-|True|
|N1K|F|1|RETURNED|True|-|True|
|N1K|F-NOBIND|1|RETURNED|True|-|True|
|N1K|F-NOCONSUME|1|RETURNED|True|-|True|
|N1K|F-NOEXIT|1|RETURNED|True|-|True|
|CRASH_AFTER_WORK|B0|2|VIOLATION|False|DUPLICATE_EXECUTION|True|
|CRASH_AFTER_WORK|B1|1|UNKNOWN|False|-|True|
|CRASH_AFTER_WORK|F|1|UNKNOWN|False|-|True|
|CRASH_AFTER_WORK|F-NOBIND|1|UNKNOWN|False|-|True|
|CRASH_AFTER_WORK|F-NOCONSUME|2|VIOLATION|False|DUPLICATE_EXECUTION|True|
|CRASH_AFTER_WORK|F-NOEXIT|1|UNKNOWN|False|-|True|

The additional normal F demo legally completed with one actual work entry,
zero violations and active0. The12 matrix cells had14 work entries because
B0/F-NOCONSUME each repeated work after actual exit17. This is the expected
negative evidence, not a failed comparison to hide. All outcomes were retained.
Clean complete supervised window7.250s; code-copy/help/demo/matrix stayed inside
the120s allowance. This is **same-machine, new-directory reproduction**, not
independent researchers, machine, filesystem, crash-recovery campaign or OS portability.

## Known techniques and candidate contribution matrix

The [protocol](../../research-protocols/engineering-runner-comparison-2026-10-24.md)
records the research owner's official-document reading dated2026-10-24.
The executor did not fetch those sites or install/run the third-party tools in
this round; only ordinary Git networking was authorized. The following is a
document-level comparison based on that supplied reading, not a new empirical
claim about their limitations or a version-pinned reproduction.

| Candidate contribution | Existing primary reference / prior capability |040 evidence | Still missing / decision |
|---|---|---|---|
| Actual input/code receipt consistency | [MLflow Tracking](https://mlflow.org/docs/latest/ml/tracking/), [lmms-eval commands](https://github.com/EvolvingLMMs-Lab/lmms-eval/blob/main/docs/getting-started/commands.md): parameters, artifacts, logs/cache/integrity already exist | Input drift rejects under B1/F and admits under ablated binding; all profiles reject code-receipt mismatch | Controlled worker only; no malicious attestation or actual-tool superiority. Logging/hash comparison is not a new algorithm |
| Durable consumption and crash uncertainty | [SQLite transactions](https://www.sqlite.org/lang_transaction.html), [atomic commit](https://www.sqlite.org/atomiccommit.html); [Ray FailureConfig](https://docs.ray.io/en/latest/tune/api/doc/ray.tune.FailureConfig.html) offers configurable retries | Unique transactional B1 matches file F; both lose completion after consumption/actual work exit17 | No common atomic transaction with external computation, power loss or disk corruption. Not exactly-once, no distinct transaction mechanism |
| Exit-gated scoring and descendants | [Python subprocess](https://docs.python.org/3/library/subprocess.html), [Windows Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects) | Actual direct-alive and descendant-alive admission faults distinguish full/ablated policy; all owned groups finally empty | Existing OS mechanisms; no proof about arbitrary accelerators, other OS or unregistered malicious processes |
| Resource/cost reporting and reproducible contract | [MLflow system metrics](https://mlflow.org/docs/latest/ml/tracking/system-metrics/), standard process/SQLite primitives | Complete540 records, component ablations, actual Job CPU/commit, standalone three-file clean check | No fair installed-tool benchmark, real inference adapter, independent-machine replication or measured usability benefit |

MLflow/Ray URLs use moving `latest`, lmms-eval uses moving `main`; the supplied
access date is not a fixed release ID. No local installation/version measurement
of those tools occurred. B0/B1 are explicitly our reference profiles; results
must not be attributed to those products or prove they cannot implement the gates.

## Paper-value decision and limitations

F and B1 each have normal30/30 plus safe-fault30/30 legal completions, no
admission violations or duplicate work, and ten crash-UNKNOWN cases. F/B1
paired median wall ratios for1KiB/64KiB/1MiB are1.0135/0.9635/0.9968, with
both-signed paired ranges. B1's schema setup is measured separately; F's
extra claim/hash-linked evidence storage is also disclosed. No clear repeatable
advantage across sizes or independent usage benefit was demonstrated.

**NO_DISTINCT_MECHANISM_EVIDENCE.** Ordinary transactions, hashes, atomic files
and OS supervision suffice for these tested goals. The contribution available
for an engineering account is a concrete auditable fault contract, complete
negative comparisons and small reproducible implementation, not a new reliability
algorithm. Stop expanding framework machinery to relabel this as novelty.

Remaining evidence for any stronger engineering-paper claim includes real
inference integration under separately authorized resources, fair comparisons
with actual installed tools, independent machine/filesystem evaluation and a
specific user/cost benefit. This round does not authorize them or task041.
No target-journal acceptance probability, exactly-once guarantee, VLM/GPU
performance gain, natural-video result or novelty pass is asserted.

The work ran only on fresh generated bytes/receipts/processes in two040 roots.
The complete [engineering results](./engineering-results.md) and
[540-row data](./benchmark-rows.csv) preserve UNKNOWN, rejection, invalid
admission and fallback. Existing datasets/locks/permissions/environment remain
untouched. Seven-path delivery, one ordinary safe push then STOP.

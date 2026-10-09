# VLM-BATCH-010｜Charades元数据未完成部分续接：10个有界步骤

**状态由最新 `docs/next-steps.md` 唯一READY授权。** 2026-10-09，用户此前明确授权仅下载一次AllenAI官方约3MB的`Annotations & Evaluation Code`作非商业、独立隔离的元数据资格审查；[BATCH-009](../VLM-BATCH-009/download-integrity-and-schema.md)因Windows路径名称误判**在GET前安全停止**，[BATCH-009-FIX提交](https://github.com/floomeer83felix-source/vlm/commit/dda8481a330c4cfa1e734511ad59e7d8f7571d4f)已改用规范路径/物理目录身份双检查并报告21项合成测试通过。**这只是安全修复，不是已下载、已核验CSV或获GPU许可。** 这次任务是**新父任务010，只执行009尚未完成的真实元数据操作，绝不能重新执行/重写父任务009或其FIX**。

## 启动/权限

仅用户向**同一个原Codex聊天框**发送“执行唯一READY VLM-BATCH-010”时启动。先安全刷新**独立文档Git checkout**的main、确认`AGENTS.md`／`docs/next-steps.md`／`docs/codex-results.md`当前确实仅本父任务READY且不存在`### VLM-BATCH-010 ...`；若有冲突/多个READY/同父历史结果，STOP。阅读[冻结Windows安全协议](../../charades-metadata-safety-protocol-2026-10-09.md)、[009 README](../VLM-BATCH-009/README.md)、[009阻塞收据](../VLM-BATCH-009/download-integrity-and-schema.md)、[009资格未知](../VLM-BATCH-009/qualification-and-science-decision.md)和最新`prototypes/charades_metadata_audit.py`及其合成测试。用户的有限授权仍未消耗：GET0，下载0B，archive SHA UNKNOWN；**只允许执行一次官方小包的后续步骤**。除所列范围外不推定任何新权限。

Windows目标固定：
`%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-Metadata\`
该路径经环境变量解析；只在该根下保存`incoming/Charades.zip`、`extracted/`白名单CSV/类别表/README与许可、`local-audit/`本机审计汇总。**不要输出真实Windows绝对路径**。任务不得在Git文档checkout、RTX3090原研究目录、其parent/child、OneDrive/云同步路径落数据，也不得改目录来绕过校验。

## 十项顺序工作（只完成可安全执行的部分）

**1. 基线和授权核验**：确认数据授权只覆盖本官方小包，非商业许可、用户额外禁令及现有009阻塞／FIX已被登记；不会自动触发二次下载。只读检查旧隔离根和`incoming`现状：若已存在ZIP/.part、聚合收据或身份不明旧文件，停下，不覆盖、不重下。

**2. 修复版目录身份复核**：调用最新版`check_ancestors`检查实际落点、已存在祖先与规范名字、Windows samefile+非零dev/inode一致、两条祖先链reparse拒绝、stable canonical；配合只读PowerShell验证固定LOCALAPPDATA下且不与原研究/公共Git/登记云同步区域重合、disk≥150MiB、目录可写、仅任务自有空子树。若不确定任一安全条件，`BLOCKED_STORAGE`，**绝不**为了让测试过而重新编辑检查器或切目录；新发现代码缺陷直接停止报错。

**3. 官方链接和流量预算预检**：从[AllenAI Charades](https://prior.allenai.org/projects/charades)唯一 `Annotations & Evaluation Code (3 MB)` 官方锚点确认HTTPS S3对象`https://ai2-public-datasets.s3-us-west-2.amazonaws.com/charades/Charades.zip`，别选其它资源。先HEAD，核content type、response final URL/host、Content-Length`≤8MiB`（上次HEAD 3519822B只作历史，不替代现在的读数）；无HEAD可流式limit GET。不能访问镜像/STA/视频。HTTP非200/非zip/重定向陌生域即STOP。

**4. 一次性限额传输**：只用现有Python标准库`urllib.request`（如需临时短脚本，**仅本地任务隔离目录**，不能在公开checkout生成有网络权限的长期runner）；HTTPS，显式拦截任何非官方host跳转；以64KiB块stream写入`incoming/*.part`，接收正文硬上限8MiB，成功后校验ZIP magic/大小/sha256，并仅在任务自己新建且原位置无文件时原子更名`Charades.zip`。网络异常最多一次**额外重试**，不得越过一次成功GET、不得扩大目标；遗留part冲突则STOP。压缩包和本地manifest永不上传GitHub。

**5. ZIP完整性和白名单**：用新工具`safe_members`与`inspect_archive`核中央目录、CRC、成员≤200、声明解压≤64MiB、单成员≤16MiB、绝对/反斜杠/..、Windows特殊名字、大小写碰撞、路径软链接与嵌套压缩等；任何未覆盖的新危险情况STOP。不运行压缩包中的.py/.m/.exe等代码，绝不`extractall`；仅提取train/test CSV、类别表及可允许的README/license，字节仍留隔离目录。

**6. 真实schema和完整分母**：用`csv.DictReader`、类表读取`id,subject,actions,length`，核真实CSV/header/encoding与固定revision/SHA，并按train/test统计视频行、空/重复id、空subject/actions、非法类别、重复区间、非finite/超时长/起止倒序，保留坏数据分母；失败为UNKNOWN/FAIL，不把未检查项写0。不读取/打印描述脚本、原视频/私有标签。

**7. P1实际资格汇总**：仅对合法记录中的`(video,class)`，计至少两段严格不重叠间隔`>0`的组/视频，预定敏感性`>0.5s`和`>1s`，完整歧义/重复/相接/重叠/失败分母。实际计数可公开仅按脱敏聚合与小群抑制，不输出任何video/subject/class组合明细；非零也不能认证物理二次事件或自动造ordinal问答。

**8. P2实际资格汇总**：同视频、不同类有效区间交集`>0`，交集比最短区间`≥0.5`，组/视频/对数与含混/接触/包含分母，**仅宏观聚合**。不声称已观察模型错误或新算法效果。

**9. 来源和时长的保守初筛**：仅本地计算train/test subject ID交集**总数**、唯一subject计数与粗时长直方图，禁止将原始video/subject ID、脚本、可逆细分格子、详细来源映射或ZIP/CSV推上公共GitHub；聚合正小单元`1—9`必须`WITHHELD_LT10`。即便显示可用source数也不证明自然独立session，未处理视频则真实PTS仍UNKNOWN。

**10. 诚实决策与回报**：对前述每项列`DONE/BLOCKED/UNKNOWN`，给官方链接、zip SHA/字节数（若实际下载）、成功GET/重试次数、真实schema是否可解析、P1/P2聚合资格及失败分母、Python合成测试的本轮收据。即使真实元数据字段/计数PASS，科学仍只有**短视频记录层候选**，没有新核心机制retain、没有真实视频PTS、没有自然长视频最终确认、没有GPU许可。问题资格为0或错误过高则明确STOP对应P1/P2。不得自行发布BATCH-011或向用户申请多种数据/视频/GPU的一揽子许可。

## 交付和停机

**唯一允许公共GitHub提交的3处文件**，只写新父任务，不改原009/FIX回报、代码和历史：
1. `docs/codex-artifacts/VLM-BATCH-010/download-and-schema.md`：脱敏的许可/隔离/preflight/官方GET、SHA/size、安全ZIP/schema质量汇总或阻塞原因。
2. `docs/codex-artifacts/VLM-BATCH-010/qualification-and-decision.md`：P1/P2/source/时长**非可逆聚合统计**、失败分母及可证伪停止判断。
3. `docs/codex-results.md`**末尾仅追加一条**`### VLM-BATCH-010 YYYY-MM-DD ...`，十项状态、授权内资源账、是否GET以及安全停止后续建议。

**不得修改、提交或推送** `prototypes/`现有代码、ZIP/CSV、私有本机manifest、真实样本行、视频/subject identity与精确文件路径、原研究工作区、GPT计划总览/README、PR及历史。已发布的两份toy代码仅用于审计，可用现有Python环境运行标准库合成test但**不得为了这次继续下载而修改任何代码**；遇缺陷STOP，让ChatGPT决定是否另设修复任务。

**硬边界**：0 Charades视频（包括13GB）、0 STA/Ego4D数据、0媒体帧/视觉特征、0 GPU/Qwen/SigLIP/模型/QA/训练/评分、0真实视频解码、0原Windows研究代码/conda/CUDA/锁/账本更改、0外部联系/Issue/付费API/人工标签、0 GitHub公开原始数据。Git只stage三处，上载前核差异和脱敏；失败时不得force push/清理用户别的文件。**一次成功提交后停止当前轮，留在原Codex聊天。**

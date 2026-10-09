# VLM-BATCH-009｜用户已批准：Charades官方单包元数据核验（十项、0视频/0GPU）

**创建：2026-10-09。执行权仅源于 `docs/next-steps.md` 上唯一READY父任务和用户本轮明确授权**。用户确认Charades官方非商业许可适用于其研究，**仅授权一个官网“Annotations & Evaluation Code (~3 MB)”标注/评测包**供隔离目录的CSV、时段和来源资格统计；不批准视频、STA、GPU、原科研工作区改动。阅读[固定安全协议](../../charades-metadata-safety-protocol-2026-10-09.md)是**不可跳过**的先决条件。本任务不承诺一定下载成功/发现科学现象。

**同一个已存在的Codex聊天**，收到用户明确“执行BATCH-009”信号才开始。只对独立公共**文档Git checkout**做`git fetch origin main`和安全fast-forward；重读`AGENTS.md`、`docs/next-steps.md`、`docs/codex-results.md`、本README、安全协议、[上一批科学裁决](../VLM-BATCH-008/data-science-go-no-go.md)与[官方README](https://prior.allenai.org/projects/data/charades/README.txt)、[官方license](https://prior.allenai.org/projects/data/charades/license.txt)。若Codex结果文件已有任何`### VLM-BATCH-009 ...`，**不得重做/重新下载**；Git冲突、未提交更改或多READY，STOP。

## 冻结存储根和输入（先做核验，后取得字节）

只允许Windows上`%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-Metadata\`，子树`incoming/`,`extracted/`,`local-audit/`。执行时使用实际解析后的本机路径；**向GitHub报告相对路径或变量形式，不写用户名或绝对隐私路径**。先确认目标/其父目录不是符号链接/junction/reparse point，并且不位于文档Git仓库、原Windows RTX3090研究目录及其上层/子树或同步云目录。未知任何一项则 STOP 报路径风险，不改换到别处，不动旧实验的锁/账本。空余空间≥150MiB，新建本次隔离目录可写，无冲突旧文件。详见安全协议。

唯一可访问数据链接是[Charades项目页](https://prior.allenai.org/projects/charades)的**Annotations & Evaluation Code (3 MB)**对应S3对象，允许1次成功GET（异常最多再试1次），**流式8MiB总量上限**；其余官方文本README/license仅供查阅。不是官网页面其它大型视频、caption-code、feature或RGB/flow链接。不从镜像或STA Drive救援。

## 十项顺序执行（独立安全项遇UNKNOWN可继续；下载/路径/许可违规立即STOP）

**1. 用户授权与数据使用条款前置**：记录用户批准的非商业研究用途、单包、隔离分析、禁止分发；核官网license与对应链接仍一致。许可证不适用/变动或有权利冲突则`BLOCKED_LICENSE`、不下载。

**2. Windows隔离与无侵入证据**：验证`%LOCALAPPDATA%`解析结果的真实路径、与原实验目录和Git checkout不重合、无重解析点/云同步、≥150MiB空余、只写新空任务目录；不打印用户名/绝对路径。把`storage_preflight=PASS/BLOCKED`与失败类别写本地/脱敏报告。不能拿用户未知原目录时做出“已确认隔离”假声明。

**3. 单官方下载预检与一次限额传输**：只从官网页面当前锚点解析唯一目标，HTTPS/S3官方host校验与重定向校验，先只查HEAD元数据（若可用），然后流式GET至`incoming/.part`且严格8MiB，200且ZIP签名后算SHA256/size并原子改名；失败`NO_DOWNLOAD`，不能改下载范围、镜像或换更大包。超时/断线最多额外一次有限重试；异常临时.part只清理本任务文件（不碰用户其它资产）。

**4. ZIP静态安全清单**：只用标准库zipfile列中央目录、路径标准化/大小写重复/drive或../逃逸/绝对路径/symlink/encrypted/ZipBomb/总解压预算；文件数≤200、单CSV≤16MiB、声明总解压≤64MiB、嵌套路径≤4。任何危险成员整包STOP。记录archive SHA与明示官方校验值`UNKNOWN`（如果无），而非假定官方hash验证通过。

**5. 白名单只读解压与真实CSV schema**：仅提取train/test CSV、class/object/verb/mapping TXT及可能的README/license；拒绝scripts、executable、mat/pickle/图片/视频/未知成员。逐个读真实header/编码/分隔规则（csv.DictReader），对照官网id/subject/actions/length，记录缺失/未知/版本修订；只保留本地CSV，**不输出真实行到GitHub**。如果压缩包缺CSV或解码不安全则停止实际统计，保留失败原因。

**6. 全行及区间质量分母**：按train/test统计总行、空ID/subject、重复ID、空actions、未知class、无法解析/非finite数字、负起点、`start≥end`、`end>length`和确切重复区间。禁止修正脏数据后把剩余当全量，绝不使用`script`/`descriptions`做题目。官方秒/timebase的媒体对齐仍UNKNOWN。

**7. P1同类非重叠区间候选资格**：以同视频同class分组，只在数值有效区间中按间隔`>0`事前判定有至少一对**严格不重叠**记录的group/video，另报告`>0.5s`/`>1s`敏感性；区分完全重复/相接/同类重叠歧义、构造失败。只输出总数和分母、没有任何真实ID、小cell匿名化。**即使非0，也不能判定两次物理独立活动或自然语言first/second真值已获证**。

**8. P2异类重叠区间候选资格**：同视频、不同class候选交集`>0s`及`overlap/min(duration)≥0.5`预定阈值，报告pair及涉及视频的安全总数、边界接触/无效/同类不合用分母；不得声称因果/准确定位或视觉感知已有证据。不根据模型结果改阈值。

**9. 保守来源和时长初筛**：仅本地使用`subject`对train/test做去重和交集**总数**（如果subject缺失写UNKNOWN），按split汇总合格video和粗时长段（禁止细粒度身份映射泄漏）；不能以distinct video等于独立participant，也不能认证真实媒体PTS/clip/自然长视频。所有小于10的身份可链接单元公开结果应合并或WITHHELD。

**10. 资格判断与单点结论**：出`DATA_SCHEMA_VERIFIED/FAILED`、`P1/P2_CANDIDATE_COUNTS`、`PROVENANCE_UNKNOWN`、`LONGVIDEO_FAIL`、`NOVELTY_RETAIN_0`与真正下一步缺什么。若P1/P2候选为0或严重不可辨认，则对相应研究问题NO-GO；非零也只建立**短时域记录层资格**，不授权下一步视频/GPU/STA或生成回答问题。为用户给出最多2项具体独立授权需求，不能自动派BATCH-010。

## 限定代码／交付范围（必须精确）

为了可复现并检测泄漏，允许在**公共文档checkout**中新增2份**只含通用逻辑、不含任何Charades真实记录/路径**的标准库Python：

- `prototypes/charades_metadata_audit.py`：可独立运行的安全zip白名单读取／聚合统计工具；从命令行接收隔离目录路径或由协议指定变量解析，默认不输出任何真实行、ID、文本或原始分组。仅本地写聚合统计临时结果在隔离目录内。源文件无HTTP凭据、无绝对私有路径。
- `prototypes/test_charades_metadata_audit.py`：程序内合成虚构数据的unittest，至少8例覆盖正常间隔、P1重复/相接、P2异类重叠、非法时间、重复ID、跨split subject总数、空分母、非法zip路径/超限/可疑成员。执行`python -B -m unittest discover -s prototypes -p "test_charades_metadata_audit.py" -v`；用现有Python标准库CPU，不装依赖/不改环境。

**GitHub最终只允许5处**：
1. `docs/codex-artifacts/VLM-BATCH-009/download-integrity-and-schema.md`：只写任务1—6的脱敏preflight、archive SHA/字节数、官方来源、实际safe header、异常/失败、公开license/README URL；绝不贴用户绝对路径、真实记录、身份证据。
2. `docs/codex-artifacts/VLM-BATCH-009/qualification-and-science-decision.md`：只写任务7—10的P1/P2资格汇总与计数/分母、SOURCE/PTS与长域失败边界、保守统计披露和下步决定。
3. `prototypes/charades_metadata_audit.py`
4. `prototypes/test_charades_metadata_audit.py`
5. 只在`docs/codex-results.md`末尾追加**一条** `### VLM-BATCH-009 ...`，任务1—10分项DONE/BLOCKED/UNKNOWN、实际数据字节预算、单测收据、0视频/0GPU/0原资产修改及两份报告链接。

**严格禁止进入GitHub**：压缩包、源CSV、Zip成员完整敏感内容、任何具体video/subject ID、原始`script/descriptions`行、来源映射、下载凭据、本地绝对账户路径、任何可逆细粒度表。上传前用`git diff --cached --name-only`并核实际正文和`git status`：只stage上面5处。遇冲突不force push、不覆盖/重置别人的工作，不改变ChatGPT控制的`docs/next-steps.md`/`docs/research-overview.md`/`AGENTS.md`和历史；单次安全push后立即停止，保留原Codex聊天。

**再次禁止**：Charades/STA视频、缩略图、RGB、flow、光流、模型、features、13GB链接/70MB代码、网络镜像/外部联系，任何PyTorch/Qwen3-VL/SigLIP训练/推理/GPU/QA或Windows原实验目录/conda/CUDA/锁/账本操作。下载授权**不**意味着真实实验许可。若无法确认本地路径与许可证要求，允许整轮`BLOCKED`且不下载；不可瞒报已执行。


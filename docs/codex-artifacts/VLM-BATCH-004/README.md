# VLM-BATCH-004：G1外部阻碍澄清＋纯合成合同验证（唯一 READY 父任务包）

> 2026-10-08 ChatGPT科研审查后发布。此前 [VLM-BATCH-003](../VLM-BATCH-003/README.md) 的A/B/C静态交付已接受；其科学结论是G1 HOLD。**本包不是数据许可、真实时间戳、独立来源或GPU实验的放行。**

## 0. 调度与输入

用户沿用现有Codex聊天框，一次安全刷新 GitHub 文档checkout `main`，读取 `AGENTS.md`、`docs/next-steps.md`、`docs/codex-results.md`、`docs/research-overview.md`，核对唯一 READY 父任务与是否已有 `### VLM-BATCH-004` 报告。若已有已提交的完成/部分完成/阻塞记录，**不要重复执行**，请ChatGPT审查。

本包源资料仅包括：
- [VLM-002已提交元数据审计](../VLM-002/dataset-metadata-review.md)，其中VES-Bench官方作者/版本及许可仍未知；
- [VLM-BATCH-003 A](../VLM-BATCH-003/timestamp-contract-audit.md)、[B](../VLM-BATCH-003/source-provenance-audit.md)、[C](../VLM-BATCH-003/g1-feasibility-contract.md)；
- [PR #1](https://github.com/floomeer83felix-source/vlm/pull/1) 未合并预注册**草案**，只做假设/场景背景。

避免重新爬取先前23个公开响应、失败404、同一媒体目录。默认无新增外部检索；不访问私有答案或原始数据。

## A. VES-Bench许可与无答案字段请求包（写草案，**不发送**）

**交付**：`docs/codex-artifacts/VLM-BATCH-004/ves-access-request.md`，推荐一页左右。基于既有官方README及已记录的revision，写一封可供用户审阅后**自行决定是否发送**的简短中英双语联系邮件草案；如官方联系方式在本地已确认材料中未显示，标UNKNOWN，**不猜测邮箱**。请求应围绕恰好以下信息：

1. 公开/研究使用的问答注释许可与视频使用许可是否分别允许本地非商业研究及所需结果披露；如果需申请明确资格/流程，不擅自许可推断；
2. 不含答案的schema / 字段字典：视频ID、官方问答split、联合必要参考区间的时间单位/闭开语义/区间数/必要性依据、视频revision及裁剪/转码起点；
3. 是否提供可验证 `video_sha` 或media revision、frame PTS/timebase/clip映射与上游parent视频关系的**元数据**，不请求整套视频/带答案样本；
4. 源组与许可不明时实验保持HOLD，并让用户确认后再发送任何邮件/issue。

不声称已建立作者联系；无需获取新样本，不发送邮件、issue或私信。必须区分“已见官方材料”与“请求对方确认”的事实级别。

## B. CPU纯合成合同原型（可创建少量新公开代码，但不修改实验工作区）

**交付**：
- `prototypes/toy_g1_contract.py`
- `prototypes/test_toy_g1_contract.py`

在GitHub**文档checkout**内用Python **标准库**新建一段小型、显然标注 `TOY ONLY, NOT FOR REAL DATA OR MODEL USE` 的独立原型和 `unittest` 测试；若需要执行，使用已存在的Python解释器，不安装pip包、不更改conda/torch/CUDA。**不得导入或复制受限本地研究源码，也不得访问研究视频、模型、私人manifest、答案/评分标签**。总共尽量控制在约250行可读代码+测试，超过则优先完成核心不变量。

仅使用**程序内生成的虚构变量/小整数**验证：

1. 有理 `PTS × time_base` 时间转换、非零裁剪零点与显式parent offset/scale、边界闭开区间、VFR不规则PTS，未知时间原点/版本/非单调/重复帧时拒绝而非fallback `index/FPS`；
2. 源隔离采用**完全虚构**的source typed ID、content alias、parent边、潜在同源边传递闭包；保护集任一成员污染整组、缺关键证据返回 UNKNOWN，不能用不同SHA保证事件独立；
3. D1/D2各必须恰有12个**互异源帧**；相同且有可核时间与RGB身份的锚点；锚点在参考区间内、背景帧在预先定义的区间保护带外；**不得**把双帧平均标签当成真实覆盖；
4. **混杂门**：同等帧数不保证同等视觉token、时间分布、帧分辨率/预处理或语义干扰机制。如果原型无真实处理器token证据，标 `TOKEN_BUDGET_UNKNOWN`，不能输出公平性PASS。对时间匹配缺失标 `TEMPORAL_MATCH_UNVERIFIED`，该诊断不得归因为“仅问题相似度”；
5. 预定义错误码、拒绝策略与例外路径，避免静默修复或按结果挑样本。只需最小可读示范，不开发真实视频adapter或最终manifest生成器。

**测试必须真的执行**（只运行本toy代码，CPU，无模型/媒体），如 `python -m unittest discover -s prototypes -p "test_toy_g1_contract.py" -v`。若当前Python命令不存在或测试失败，原样回报，不安装依赖、不重试不同环境；修复仅限本包创建的toy文件，不可修改原本地研究资产。用户未授权真实视频解码、GPU实验或旧历史重算。

## C. 实验去留条件＋toy测试报告（审查而非新科学结果）

**交付**：`docs/codex-artifacts/VLM-BATCH-004/g1-decision-and-toy-test.md`，建议约1–2页。

- 准确记录B的命令、解释器主要版本、运行的测试数量、通过/失败/跳过和所有异常；只上传汇总，不贴敏感路径；**不运行时不宣称PASS**。
- 结合A的权限/字段请求和B的toy结果，做 **G1决策树**：当VES等无法确认注释/视频许可或联合必要参考区间时，研究仍HOLD；许可/字典通过后也仍需实际同版PTS和至少40个保守独立来源证明；缺任何项不能申请GPU。
- 明确如果作者无法提供合法、无答案证据区间，**停止以已覆盖“必需区间”为前提的诊断**，提交给ChatGPT选择“另找具有可靠注释的合法数据”或“重新定义不依赖gold区间的可观测科学问题”。不能以MRFS或模型输出估计冒充公开必需真值。
- 列明 D1/D2的潜在时间bin、画质、视觉token混杂，即便toy全部通过，真实处理器token与视频时间坐标仍UNKNOWN。
- 最多3个未来可审查的具体行动，标明哪些需要用户另行批准（实际发送联系邮件、下载有版权媒体、真实视频解码、GPU等）。
- 这份简报由Codex给出建议，不作创新发表性或实验通过宣称。

## 共同红线

- **0新增GPU/模型QA/训练/评分前向**；**0视频解码或媒体/模型/完整标注下载**；不访问受限视频、原始答案、逐题评分、私有身份映射。
- **0原研究资产/conda/CUDA/历史脚本/锁/账本修改**；仅允许在*独立GitHub文档checkout*新建本包指定的两个toy文件、两份Markdown报告与追加Codex结果。
- 允许对两个新建toy文件做**无外部依赖的CPU单元测试**；这不代表真实媒体时间契约或算法性能通过。
- 不发送邮件/Issue，不向外部联系人传输数据，不合并PR，不建GitHub Actions/Windows定时器。
- 公开仓库只提交脱敏、手工审阅后合理的小文件，不公开令牌/绝对个人路径/模型或媒体/数据集原文。
- 如已有同ID结果或任何Git冲突，停止、不force push；A/B部分未知可继续其它独立安全子任务并最终按实情回报。
- 本批不解封 `VLM-003` / `VLM-004`，不声称G1通过，也不以toy作为独立数据来源证据。

## 唯一回报与验收

完成A→B→C后**统一一次提交**，严格stage：
1. `docs/codex-artifacts/VLM-BATCH-004/ves-access-request.md`
2. `prototypes/toy_g1_contract.py`
3. `prototypes/test_toy_g1_contract.py`
4. `docs/codex-artifacts/VLM-BATCH-004/g1-decision-and-toy-test.md`
5. 仅在 `docs/codex-results.md` 最末尾追加一条 `### VLM-BATCH-004 ...` 父任务汇总，链接上述产物与toy测试结果。

不修改 `AGENTS.md`、`docs/next-steps.md`、`docs/research-overview.md`、旧报告或PR。目标是**一个可发送但未发送的合法数据请求、一个可运行的toy技术合同及测试、一个可证伪的去留决定依据**；不是反复堆积静态描述。

上传后停止当前执行轮次、保留同一Codex聊天框，等ChatGPT审查、决定是否值得进一步解除G1数据阻碍。 

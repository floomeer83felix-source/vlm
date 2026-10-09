# TRACE / VES-Bench 官方咨询终稿（待用户批准，未发送）

**状态：DRAFT — NOT SENT.** 用户在2026-10-09选择**路线1**，即继续研究“固定12源帧且以官方gold必要证据区间为覆盖前提”的诊断问题；**只授权起草和核实渠道，并未批准向第三方提交本正文**。本文件保存在项目公开文档仓库中便于本人审阅；**不是已发出的GitHub Issue、邮件、数据申请或许可证**。

## 目标和查证依据

- 官方仓库：[buaa-colalab/TRACE](https://github.com/buaa-colalab/TRACE)；仓库README介绍VES-Bench联合必要区间和[HF数据入口](https://huggingface.co/datasets/buaaplay/VES-Bench)。
- 建议优先审阅的渠道：[TRACE Issues](https://github.com/buaa-colalab/TRACE/issues)。仓库API `has_issues=true`，但**不保证任意账户有创建Issue权限**，也不是经确认的正式申请通道；发出之前先由用户检查新建按钮/仓库规则。
- 目前注释/上游视频研究及发表使用权、联合必要区间的正式**无答案**字段定义、媒体revision和裁剪／PTS对应均未获证据支持，统一保持UNKNOWN/G1 HOLD。
- 原[中英草案](../codex-artifacts/VLM-BATCH-004/ves-access-request.md)是历史输入，本终稿只提出最小必要请求。不得自行填入邮箱、署名、私人实验材料或账号令牌。

## 待确认英文正文（适合公开GitHub Issue）

**Title:** VES-Bench: clarification on data permissions and evidence-interval metadata

Dear TRACE / VES-Bench authors,

Thank you for making the TRACE project and VES-Bench available. We are planning a non-commercial research study of video-language models with a fixed budget of **12 distinct source frames** per question. Our proposed diagnostic would keep frames covering the benchmark's necessary evidence intervals fixed while varying the additional frames. We have **not run this study** or downloaded VES-Bench media for it.

Before proceeding, could you please point us to the relevant documentation or clarify:

1. **Usage rights:** What licenses or permissions apply separately to the QA annotations and underlying/source videos? Would local non-commercial evaluation and publication of aggregate results be permitted? Are there attribution, redistribution, or application requirements?
2. **Answer-free evidence metadata:** Is there a schema or data dictionary (without answer labels or example answers) for QA/video identifiers and splits, jointly necessary evidence intervals, their time units and endpoint conventions, and how interval necessity was established?
3. **Video/time alignment:** Is there a versioned media manifest or documentation for video identities/revisions, cropped or transcoded clips, time origins, and mappings to source-video timestamps? If exact frame PTS/time-base metadata is unavailable, knowing the intended coordinate system would already help.
4. **Official access route:** If these materials or permissions require a request, is there a preferred official process or contact channel?

Pointers to existing public documentation would be sufficient; we are **not requesting video files, full annotations, or answer-bearing records in this issue**.

Thank you for your time and for releasing the benchmark.

## 中文审阅对照（非提交正文）

**标题：** 关于VES-Bench数据使用许可与证据区间元数据的咨询

TRACE/VES-Bench团队您好：

感谢公开TRACE和VES-Bench。我们计划开展固定每题12张互异源帧的非商业VLM研究：固定覆盖官方必要证据区间的帧，改变额外背景帧的组成，诊断答案变化。**该实验尚未开展，尚未为此下载VES-Bench视频。**

希望确认：
1. 问答标注与底层视频分别有什么许可？是否允许本地非商业评测及发表聚合结果？需要哪些署名、再分发限制或申请手续？
2. 有没有不含正确答案的字段字典，说明题目/视频标识、划分、联合必要证据区间、时间单位、端点语义及区间必要性的判定依据？
3. 有没有可追踪的视频版本清单、裁剪/转码关系、时间零点或源视频时间戳映射？如没有逐帧PTS/timebase，能否至少说明标注使用的坐标体系？
4. 如需正式申请，请指明官方渠道与流程。

我们只请求公开文档线索或字段/规则解释，**不在公开Issue索取视频文件、完整标注、答案行**。谢谢。

## 用户确认与发送流程（未实施）

1. 本人阅读英文正文和中文对照；可以删改研究细节、公开程度或问法。**选择路线1本身不是授权公开发帖。**
2. 本人检查 [TRACE Issues](https://github.com/buaa-colalab/TRACE/issues) 当前是否允许自己的账号发帖，以及是否存在更合适的官方申请路径。仓库API开放Issues不等于所有账号可创建；如果受限，**不要绕过权限**。
3. **只有在用户另行明确批准“以所核对的正文发布到TRACE官方Issues”后**，才可以准备实际发帖；没有批准时无人应代发、发送邮件或填写表单。
4. 若以后获授权发布：先检查重复问题；只发表确认过的英文正文，不附带本地日志、私有答案、源身份映射、原实验目录或敏感路径；保留发布后的公开URL、时间及正文SHA以便追踪。
5. 对方回复时再判断哪些是许可、作者声明、文档链接或可验证字段；**不因一条模糊回复把G1由HOLD升级为PASS**，不得未经许可下载媒体或启动GPU。

**科研状态：** 保留路线1；目前等待用户审阅确认咨询正文与是否公开发送；无Codex READY父任务。原VLM-003/004、新GPU、视频下载和正式manifest均HOLD。

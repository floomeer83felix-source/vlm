# VLM-HOURVIDEO-DEV-001｜本机已下载 HourVideo 开发集 JSON：一次离线可评分资格检查

**2026-10-11｜ChatGPT唯一READY父任务｜用户明确要求“还是交给codex吧”。** 目标是交付**实测的、脱敏的标注层资格统计**，不是继续静态文献审查。用户已在浏览器中显示 **HourVideo/HourVideo Hugging Face gated dataset「You have been granted access」**，且明确确认 **`dev_v1.0_annotations.json` 已下载到其 Windows 电脑**。这些用户事实授权本轮在指定本地下载文件上作*只读、无GPU*核验；Ego4D已签署协议但官方数据访问批准仍待确认，**绝不能据此读取/下载 Ego4D 媒体**。

## 0. 授权边界与入口

1. 使用**同一个原Codex长会话**由用户主动发送“继续”命令启动；GitHub main的新READY本身不会唤醒Codex。在独立公有文档checkout中安全`git status --short`、`git fetch origin main`、干净且可快进方可同步；重读`AGENTS.md`、`docs/next-steps.md`、`docs/codex-results.md`、本README、[等待期说明](../../hourvideo-wait-period-lab.md)和[现成Python脚本](../../../tools/hourvideo_dev_preflight.py)。
2. 必须确认**恰好一个READY是VLM-HOURVIDEO-DEV-001**、`docs/codex-results.md`末尾**不存在任何本任务的既有回报**；不满足即STOP，不继续做任何本地文件操作。旧REAL-PILOT-001及BATCH-020全部结案，Charades`FINAL_MEDIA_STOP`；本任务**不是GPU实验READY**。
3. 本轮可运行**仅标准库Python、CPU与普通Git文档操作**。禁止GPU/CUDA模型前向、SigLIP/Qwen、视频解码/ffprobe、原视频/字幕/帧/QA联网下载、Hugging Face token/API、Ego4D登录/凭据、训练与任何媒体访问；禁止触碰现有实验原树的模型、账本、锁、`research_state.json`，禁止激活原历史GPU任务、安装依赖/修改Conda/PATH，不创建自动轮询/后台任务。
4. 保护数据：原JSON可以**就地只读解析**，但不修改/移动/复制原JSON，**绝不移除或修改 HourVideo canary**；不打印/上传题目、选项、答案、正确字母序列、video_uid、qid、视频链接、原JSON片段、样本ID组合、私人文件绝对路径、cookies/凭据/用户邮箱。仅输出**非敏感聚合计数、字段名（不带取值）与PASS/HOLD判据**。原文件只在用户机器上，不带进公有文档checkout或云/聊天。

## 1. 唯一授权的真实本地输入定位

- 优先**精确检查**Windows该登录用户的`Downloads\dev_v1.0_annotations.json`；如果浏览器可能对名称加` (1)`后缀，允许仅在**该用户自己的Downloads目录的顶层**枚举与`dev_v1.0_annotations*.json`相符的文件**名/大小**，选择明确的单个文件；不枚举全部下载记录、不同用户、Desktop、云盘、原实验工作树或全盘。无需提取或发送用户身份/路径。
- 如恰好一个可信文件存在，对其做只读SHA256**只保存于私人内存/内部执行证据，不放到公开报告**；先确认本地文件体量合理（官方截图文件约1.85MB，过大/损坏/同名多份不擅自猜选）。如不存在、多份歧义或不是该文件，`INPUT_NOT_FOUND_OR_AMBIGUOUS`，直接给用户**只要求指出其具体位置**的停止回报；不能扩大扫描范围，也不能把无文件宣称成无数据。
- 允许一次对已选JSON的**结构/标签类型只读检查**：顶层类型/嵌套关键字段名称、元数据时长类型、每video问答结构、答案键存在/有效性（不回显具体值）。只需验证题目有可判正确标签，不要为生成报告列出明文QA/选项/答案；文件里可能含验证canary，必须原样保留。

## 2. 同一轮完成可执行检查，不依赖新审批

A. 在安全同步后先对已有`tools/hourvideo_dev_preflight.py`运行`python -B tools/hourvideo_dev_preflight.py --self-test`；只用虚构样例，需确实得到`SELF_TEST_PASS`。若执行失败，允许在本轮用最小改动修复**已有同一工具**并反复运行**虚构合成自检**，不能因此训练模型、安装依赖或变更原数据。

B. 在本机被授权的真实JSON上运行已有`--annotations`只读检查，默认不写`--private-selection`，不生成新的QA/UID私有清单；读取方式和日志必须防止原始答案泄露。若正式dev标注结构与旧HF卡片示例不同，可以**最小化适配原工具**，但必须事前核字段类型/嵌套，不可臆造/推断标准答案、不可向旧`dev_v1.0.json`或samples回退伪称dev真值。调整后重跑**虚构自检**，再对真实文件**最多一次补充重跑**（加最初一次，真实JSON分析最多2次），不无限调试/重扫。修改脚本代码不可嵌入真实QA片段、文件名真实路径、canary或受限样本。

C. **必须实际回答的六个数/判据**（仅聚合，避免任何UID/题文）：文件是否可解析；识别多少视频记录；其中≥20min且每视频≥2道有效有答案QA的视频数；其中≥30min的视频数；能否选择**12段不同≥20min**且每段≥2题（24对）；满足/不满足时的聚合拒绝原因与工具schema局限。检查题目标签完整性、qid去重和无效数据，但这仍只是**标注层`ANNOTATION_ONLY_CANDIDATE`**，不是实际视频已具备或GT匹配证书。严禁在报告中重现任何独特video UID或题目内容。

D. 安全负结果同样是任务完成：文件未找到、权限不足、json损坏、schema不可识别或无答案则写`ANNOTATION_PREFLIGHT_BLOCKED`、具体可解决的**非敏感原因**、实际执行次数与已知限制；**不要假造**12/24，也不要自行访问其他下载目录或HF资源。原许可限制 benchmark 标注**不能用于训练、蒸馏、训练控制器、检索模型**；本轮只统计，绝不使用标准答案调选帧/调模型。

E. 若工具因字段类型不兼容，需要交付脚本补丁时，新增或修改仅`tools/hourvideo_dev_preflight.py`（而非原科研项目源码）；可加完全虚构、自包含的单元断言在脚本内，确保`--self-test`覆盖真实观察到的**字段类型**，但绝不含真实值。**不要放宽必选字段来凑数量**；确认评分键含真实GT字段才计数。检查原脚本可能把`mcq_test`限制为字符串，不应先猜发布文件的实际类型。

## 3. 交付与精确写权限

公有Git可修改的文件**只限**：
1. `docs/codex-artifacts/VLM-HOURVIDEO-DEV-001/local-annotation-eligibility.md`：一次性真实本地JSON脱敏聚合收据（文件可解析/分母、≥20与≥30分钟数量、每video2题达标数、标注版本或结构能否实际确认、自检是否实际PASS、失败原因、0GPU/媒体/下载），仅公开聚合。
2. `docs/codex-results.md`末尾**仅追加一条**`### VLM-HOURVIDEO-DEV-001`，链接报告及六个关键判据，说明执行事实/未知。
3. **仅如确有适配问题**，允许调整`tools/hourvideo_dev_preflight.py`；测试只用完全虚构数据，禁止输出示例原QA。

不允许修改`docs/next-steps.md`、`docs/research-overview.md`、`AGENTS.md`、历史报告、原实验资产、FAQ或README，不生成受限数据附件。stage前核对允许路径且静态安全审查没有真实视频ID、QA、qid、答案、canary、私有路径、邮箱及访问令牌，**普通push main一次后立即STOP**，不自动放行Ego4D视频、GPU、24题模型实验或下个任务。此批结束只等待ChatGPT验收；若所有必要数已取证，也不自动调用Qwen。报告必须明确：HourVideo访问已由用户截图证实，Ego4D官方媒体批准仍未证实，真实长视频使用许可、版本匹配、GPU锁与成本仍是独立门。

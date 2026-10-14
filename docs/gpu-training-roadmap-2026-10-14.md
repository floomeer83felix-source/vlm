# VLM 真实Ego4D → RTX3090 GPU训练：一次性任务路线（2026-10-14）

**目标：一次性把剩余工作排到真实GPU梯度训练及可选Qwen3-VL LoRA，而不是在每个结果回来后重新起草合同。** 这是规划与任务串联，**不是批量AWS下载/GPU权限**，也不会自动唤醒原Codex会话。严格遵循`AGENTS.md`的**同时仅一个READY**、已结案任务不可重跑、每轮只提交一份匿名收据与`codex-results.md`末尾一条。所有受限制视频、原JSON/QA/UID/答案/凭据、训练中间产物和权重仅留私人本机。

## 完整阶段顺序

| 阶段 | 合同 | 当前状态 | 本阶段真实交付/放行条件 | 新独立授权 |
|---|---|---|---|---|
| 1 | [VLM-EGO4D-AWS-META-006](./codex-artifacts/VLM-EGO4D-AWS-META-006/README.md) | **已结案：完整清单/50 UID PASS，canonical来源HOLD** | 已完成90秒timeout的4,653,141B全文GET且50/50 UID命中；随后canonical来源规则HOLD，媒体HEAD0，未获得视频大小 | 已完成独立许可并安全结案：3/7 S3 attempts；未用4次不继承，0视频GET/GPU |
| 1b | [VLM-EGO4D-AWS-META-007](./codex-artifacts/VLM-EGO4D-AWS-META-007/README.md) | **已结案：45个安全来源候选、2个媒体HEAD200，1段≤3.5GiB** | a85e66a真实执行：50 UID中45个固定官方来源合规、5个隔离；两个媒体HEAD200，身份可锁，恰1个≤3.5GiB；S3 7/7，无媒体GET | 原metadata许可已执行并结案；不得继承旧7次额度，媒体GET/GPU仍未授权 |
| 2 | [VLM-EGO4D-LIVE-MEDIA-002](./codex-artifacts/VLM-EGO4D-LIVE-MEDIA-002/README.md) | **唯一READY，用户已批准单次有限media GET+manifest重取** | 由于META-007未持久化私有UID/URI映射，重取唯一官方manifest并复现前两对象HEAD，择其中唯一≤3.5GiB视频一次条件GET；成功还须验证PTS/发布桥接，未知则只做UNSCORED smoke | 用户已独立批准**≤8次S3总HTTP尝试（含唯一manifest GET≤8MiB及唯一媒体GET）**；单段≤3.5GiB、媒体正文≤4GiB、0 GPU，已批准的A–F阶段无需逐次追问 |
| 3 | [VLM-HOURVIDEO-LIVE-AB-001](./codex-artifacts/VLM-HOURVIDEO-LIVE-AB-001/README.md) | QUEUED | 冻结评测视频和2道dev QA，对照 uniform12 vs query-aware12、最多4次真实Qwen前向，保留配对分母与成本；同版/PTS未知仅UNSCORED | 需另批RTX3090模型推理≤40 GPU分钟 |
| 4 | [VLM-EGO4D-LIVE-TRAIN-MEDIA-001](./codex-artifacts/VLM-EGO4D-LIVE-TRAIN-MEDIA-001/README.md) | QUEUED | 训练集**不同视频/物理来源**，授权可用于训练；已有合法本地训练视频优先，必要时新获取一段，不能训练/测试数据污染 | 若远程取新训练视频，需另批最多6次官方metadata+媒体HTTP、单媒体GET≤3.5GiB、媒体正文≤4GiB |
| 5 | [VLM-HOURVIDEO-TRAIN-PREP-001](./codex-artifacts/VLM-HOURVIDEO-TRAIN-PREP-001/README.md) | QUEUED | CPU只读冻结数据分割、损失和模型资产资格；评测答案只在最终评分用，train上用自监督时序正负对；不做GPU | 需任务READY，**本阶段不含GPU/下载** |
| 6 | [VLM-HOURVIDEO-TRAIN-GPU-001](./codex-artifacts/VLM-HOURVIDEO-TRAIN-GPU-001/README.md) | QUEUED | **实际运行backward+optimizer.step，最多200步，≤60 GPU分钟，训练≤1M参数temporal head**，私有checkpoint，记录真实参数变化/损失/显存；Qwen/SigLIP主干冻结 | 需另批**GPU训练**额度，且CPU preflight PASS |
| 7（可选） | [VLM-HOURVIDEO-TRAIN-LORA-001](./codex-artifacts/VLM-HOURVIDEO-TRAIN-LORA-001/README.md) | OPTIONAL QUEUED / DATA HOLD | 若独立合法train QA及现存可行LoRA依赖/权重全PASS，才在3090上微调Qwen3-VL-4B适配器；否则不得用dev QA补齐 | 需另批具体GPU微调合同（提案：1 run / ≤100 updates / ≤90 GPU分钟） |

**阶段6是实质GPU训练**，不是只跑推理。阶段7是更进一步的Qwen主干适配器训练，数据与3090/Windows依赖前置目前为UNKNOWN，不能保证能跑；不能把阶段6的head训练冒充Qwen LoRA。若只有一个合法评测视频、没有独立训练视频，则必须停在训练数据门，不用评测/dev答案做训练以迎合进度。

## 科学口径与停止条件

- 最新已实证META-007完整官方manifest GET、50/50 UID匹配、45个来源白名单候选、两个canonical媒体HEAD200且1段≤3.5GiB；但**视频正文尚未GET/落盘**，发布/剪辑/PTS桥接与Qwen本机模型资格均未证。另一段>4GiB不可进入单段下载上限；当前`NOVELTY=RETAIN0`，Charades `FINAL_MEDIA_STOP`持续。
- 实验链要可证伪：训练前AB作固定不调参基线，独立训练素材不泄漏dev标签；训练loss下降只证明优化正常，不证明问答提升、泛化、创新、统计意义或论文录用。**需要后续新批准的独立held-out评测**才能比较训练收益，不能看训练结果后挑dev问题和旧历史forward。
- 如无合法额外train QA，优先真实temporal head自监督训练，只能交`REAL_GPU_HEAD_TRAINING_COMPLETED`级别的工程证据；不得叫`REAL_QWEN_LORA_PILOT`。如有训练QA和可行依赖，再走阶段7，仍不承诺3090可容纳。
- 本轮Ego4D批准窗口按用户提供的有效期至2026-10-26，但前述AWS合同更保守地限制北京时间2026-10-25 23:59后不再发送新的数据请求。超过窗口不得凭旧审批重启AWS。
- 各阶段都要求显式上限、当前READY、无旧报告、原Codex会话新的执行消息；任何必要条件UNKNOWN都写`HOLD/NOT_RUN`，不可擅自翻版本、加数据、安装包、拉权重、改环境、重试、转移旧预算，亦不可持续后台执行。公开仓库只做文档交接，不推送原Windows实验工作区。

## 启动方式（不是自动连续执行）

当前META-006、META-007均已结案，**唯一READY=LIVE-MEDIA-002**：用户已明确批准新一轮最多8次官方S3 metadata+media HTTP尝试、唯一CSV GET≤8MiB、单视频GET≤3.5GiB（媒体正文累计≤4GiB）。用户在原Codex长期对话主动发送一次新指令即可在同一已批准父任务内顺序执行A–F全部合规阶段，遇安全门失败即STOP并一次脱敏报告，不必逐请求重新征求同一许可；**这不是GPU授权**。每阶段真实回报审查并转下一个唯一READY后再由用户在同一聊天说“继续下一轮唯一READY任务”；媒体GET、GPU推理、GPU训练和模型LoRA都必须有对应明确授权后方可切READY。该机制避免反复起草后续合同，但不自动跨越权限或数据正确性门槛。

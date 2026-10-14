# VLM 真实Ego4D → RTX3090 GPU训练：一次性任务路线（2026-10-14）

**目标：一次性把剩余工作排到真实GPU梯度训练及可选Qwen3-VL LoRA，而不是在每个结果回来后重新起草合同。** 这是规划与任务串联，**不是批量AWS下载/GPU权限**，也不会自动唤醒原Codex会话。严格遵循`AGENTS.md`的**同时仅一个READY**、已结案任务不可重跑、每轮只提交一份匿名收据与`codex-results.md`末尾一条。所有受限制视频、原JSON/QA/UID/答案/凭据、训练中间产物和权重仅留私人本机。

## 完整阶段顺序

| 阶段 | 合同 | 当前状态 | 本阶段真实交付/放行条件 | 新独立授权 |
|---|---|---|---|---|
| 1 | [VLM-EGO4D-AWS-META-006](./codex-artifacts/VLM-EGO4D-AWS-META-006/README.md) | **已结案：完整清单/50 UID PASS，canonical来源HOLD** | 已完成90秒timeout的4,653,141B全文GET且50/50 UID命中；随后canonical来源规则HOLD，媒体HEAD0，未获得视频大小 | 已完成独立许可并安全结案：3/7 S3 attempts；未用4次不继承，0视频GET/GPU |
| 1b | [VLM-EGO4D-AWS-META-007](./codex-artifacts/VLM-EGO4D-AWS-META-007/README.md) | **已结案：45个安全来源候选、2个媒体HEAD200，1段≤3.5GiB** | a85e66a真实执行：50 UID中45个固定官方来源合规、5个隔离；两个媒体HEAD200，身份可锁，恰1个≤3.5GiB；S3 7/7，无媒体GET | 原metadata许可已执行并结案；不得继承旧7次额度，媒体GET/GPU仍未授权 |
| 2 | [VLM-EGO4D-LIVE-MEDIA-002](./codex-artifacts/VLM-EGO4D-LIVE-MEDIA-002/README.md) | **已结案：网络前LIVE_TRANSFER_ENFORCEMENT_HOLD** | [3ef8559](https://github.com/floomeer83felix-source/vlm/commit/3ef855983c879ac34852ff9382ed57620409fd85)报告0/8 S3，0真实视频、GPU0；合同要求对所有wire/TLS总字节精确hard cap而现有SDK未实现 | 本任务已关闭不可重跑或继承0/8余额；已由下一个新父任务包替代 |
| 2b | [VLM-LIVE-VIDEO-GPU-START-001](./codex-artifacts/VLM-LIVE-VIDEO-GPU-START-001/README.md) | **已结案：S3 8/8、单媒体GET200但只有64–128MiB part，GPU0** | [7cb9c6b](https://github.com/floomeer83felix-source/vlm/commit/7cb9c6b815614e7695be2edc251f87d4b002626c)外层PowerShell UTC时区误算，实际约54min提前终止；不是AWS拒绝或75min真超时，0完整视频 | 本任务STARTED/8次发送预算保留，不退款、不重新GET/Range；GPU训练未运行 |
| 2c | [VLM-LOCAL-GPU-REAL-SMOKE-002](./codex-artifacts/VLM-LOCAL-GPU-REAL-SMOKE-002/README.md) | **已结案：Windows混合GPU C+G上下文过严阻塞，CUDA0** | [8d724a7](https://github.com/floomeer83felix-source/vlm/commit/8d724a7d2d55a05ae178b6640be4bc384107bc51)系统显示3090空闲22,899MiB/3%但30个C+G上下文直接触发HOLD，torch未启动；partial解码未测 | 不重跑；不能把30个桌面混合上下文误称30个训练任务，改为下一任务小CUDA实测 |
| 2d | [VLM-WIN-CUDA-REAL-FRAME-003](./codex-artifacts/VLM-WIN-CUDA-REAL-FRAME-003/README.md) | **已结案：GPU_INFRA_PASS，真视频帧0** | [5ed644e](https://github.com/floomeer83felix-source/vlm/commit/5ed644e51702253539254890e1b62fd4c3a76e8a) RTX3090真实执行2次CUDA backward+optimizer更新，loss1.067→0.671；旧Ego4D.part经ffprobe缺moov，0解码帧 | 不需再做GPU基本兼容性验证；禁止原part续传/恢复 |
| 2e | [VLM-CC0-REAL-GPU-004](./codex-artifacts/VLM-CC0-REAL-GPU-004/README.md) | **已验收：真实公开视频GPU训练80/80步PASS** | [8299653](https://github.com/floomeer83felix-source/vlm/commit/82996532ace47e520f97e2ba7b59130525d4246e) MDN官方实拍视频1,128,375B完整下载，真实75帧/4.938s，RTX3090上24,705参数80个优化步、权重实变；后段同clip准确率0.5417 | 工程技术链证明通过，但无长视频、Qwen或独立科学验证；不能重跑004 |
| 2f | [VLM-PD-LONGVIDEO-005](./codex-artifacts/VLM-PD-LONGVIDEO-005/README.md) | **已结案：HTTP200元数据后仅ValueError，视频0/GPU0** | [490d247](https://github.com/floomeer83felix-source/vlm/commit/490d247fb191a03890d9a4d7daf369416f8f26b8)：Meta GET1/1、3,155B；旧代码未保存明确失败分支；license/derivative字段UNKNOWN，媒体GET0，A/B更新0 | 旧请求额度消耗结案，不能恢复；新一轮先修复分支诊断，不推断美国公有领域页面等于API字段PASS |
| 2g | [VLM-PD-LONGVIDEO-006](./codex-artifacts/VLM-PD-LONGVIDEO-006/README.md) | **已结案：美国PD/license PASS；API没有唯一360p VP9键** | [d5a7677](https://github.com/floomeer83felix-source/vlm/commit/d5a767740a671829ec2021071c1dd6104f89846d) meta GET1/1 HTTP200/3,155B，schema/美国PD PASS，固定360p.vp9.webm匹配计数≠1；视频GET0、GPU0 | 不恢复历史预算、不推断任一低分辨率转码都不存在 |
| 2h | [VLM-PD-LONGVIDEO-007](./codex-artifacts/VLM-PD-LONGVIDEO-007/README.md) | **已结案：240p源身份/美国PD通过，37.3MB整段GET在458,752B发生read timeout** | [bf96378](https://github.com/floomeer83felix-source/vlm/commit/bf963786cb8d9c54dc82ce52c30f311932f7d94d) meta1/1、media1/1 GET200，声明37,316,857B，成功part458,752B；完整视频0、GPU0 | 旧预算预扣全部声明长度不退还，不重跑007或恢复部分媒体 |
| 2i | [VLM-COMMONS-RANGE-008](./codex-artifacts/VLM-COMMONS-RANGE-008/README.md) | **已结案：离线Range21/21 PASS，但官方HEAD强ETag资格HOLD** | [b4896bf](https://github.com/floomeer83felix-source/vlm/commit/b4896bfc218cb17e2af4d65148b4c86d3eb12e14) meta1/HEAD1 HTTP200且身份/长度37,316,857B PASS，强ETag无法认定；Range0、影片0、GPU0 | 旧预算不继承/退款；并不能推断服务器不支持206，停止围绕此CDN反复启新任务 |
| 2j | [VLM-LOCAL-LONGVIDEO-009](./codex-artifacts/VLM-LOCAL-LONGVIDEO-009/README.md) | **已结案：真实24分钟长片GPU A/B各100步，45%对45%，无motion优势** | [b11cb4e](https://github.com/floomeer83felix-source/vlm/commit/b11cb4e9fe49cf57536afc7c8665ce7780d6a05b)完整480p VP9视频1465.597s、真实43,924解码帧、489采样，uniform128/motion128真实各100梯度步、同片验证160对两臂都是0.45 | 训练首末batch loss都升高/并非收敛证据；真实电影技术探索非VLM QA、独立泛化/新颖性 |
| 2k | [VLM-LONGVIDEO-VLM-BRIDGE-010](./codex-artifacts/VLM-LONGVIDEO-VLM-BRIDGE-010/README.md) | **已结案：仅两指定HF模型缓存入口不存在，实际VLM GPU0** | [b295945](https://github.com/floomeer83felix-source/vlm/commit/b29594577fb52ee9a36836c75ca82d4142489499)已确认授权长视频路径存在、torch/transformers模块可用，但Qwen和SigLIP两个准确canonical cache roots均不存在（其他目录未知）；Qwen generate0/4、GPU0 | 不重跑010/空缓存或擅自下载；需用户提供两套完整本地模型目录及新授权 |
| 2l | [VLM-MODEL-ONBOARD-VLM-011](./codex-artifacts/VLM-MODEL-ONBOARD-VLM-011/README.md) | **已验收：Qwen3-VL×SigLIP真实长视频2×2推理成功** | [4d902ef](https://github.com/floomeer83felix-source/vlm/commit/4d902ef870f201cd5b1df7536bd235ab5b6789be) 用户补全Qwen和SigLIP完整safetensors/processor后，48真实电影候选帧、2通用问题×uniform12/SigLIP12，Qwen真正generate4/4，GPU38.906s、torch allocated峰8716.771MiB | 所有4输出达192token上限可能截断，SigLIP P2时间覆盖仅1184.150秒；无正确率、Qwen训练或HourVideo QA |
| 2m | [VLM-HOURVIDEO-MATCHED-QA-012](./codex-artifacts/VLM-HOURVIDEO-MATCHED-QA-012/README.md) | **唯一READY / AWAIT_USER_MATCHED_EGO4D_MEDIA（缺输入不可执行）** | 用户提供合法完整≥20min匹配HourVideo dev video_uid的Ego4D视频、私有标注/映射确切入口，独立核release/clip start/PTS一致后两冻结QA×均匀12 vs SigLIP12，最多4次Qwen、384token检查EOS | 本任务0 AWS/媒体/模型下载；用户需在Codex原聊天提供准确输入+单轮GPU≤40min授权；无同版证据不可报正式QA正确率 |
| 3 | [VLM-HOURVIDEO-LIVE-AB-001](./codex-artifacts/VLM-HOURVIDEO-LIVE-AB-001/README.md) | QUEUED | 冻结评测视频和2道dev QA，对照 uniform12 vs query-aware12、最多4次真实Qwen前向，保留配对分母与成本；同版/PTS未知仅UNSCORED | 需另批RTX3090模型推理≤40 GPU分钟 |
| 4 | [VLM-EGO4D-LIVE-TRAIN-MEDIA-001](./codex-artifacts/VLM-EGO4D-LIVE-TRAIN-MEDIA-001/README.md) | QUEUED | 训练集**不同视频/物理来源**，授权可用于训练；已有合法本地训练视频优先，必要时新获取一段，不能训练/测试数据污染 | 若远程取新训练视频，需另批最多6次官方metadata+媒体HTTP、单媒体GET≤3.5GiB、媒体正文≤4GiB |
| 5 | [VLM-HOURVIDEO-TRAIN-PREP-001](./codex-artifacts/VLM-HOURVIDEO-TRAIN-PREP-001/README.md) | QUEUED | CPU只读冻结数据分割、损失和模型资产资格；评测答案只在最终评分用，train上用自监督时序正负对；不做GPU | 需任务READY，**本阶段不含GPU/下载** |
| 6 | [VLM-HOURVIDEO-TRAIN-GPU-001](./codex-artifacts/VLM-HOURVIDEO-TRAIN-GPU-001/README.md) | QUEUED | **实际运行backward+optimizer.step，最多200步，≤60 GPU分钟，训练≤1M参数temporal head**，私有checkpoint，记录真实参数变化/损失/显存；Qwen/SigLIP主干冻结 | 需另批**GPU训练**额度，且CPU preflight PASS |
| 7（可选） | [VLM-HOURVIDEO-TRAIN-LORA-001](./codex-artifacts/VLM-HOURVIDEO-TRAIN-LORA-001/README.md) | OPTIONAL QUEUED / DATA HOLD | 若独立合法train QA及现存可行LoRA依赖/权重全PASS，才在3090上微调Qwen3-VL-4B适配器；否则不得用dev QA补齐 | 需另批具体GPU微调合同（提案：1 run / ≤100 updates / ≤90 GPU分钟） |

**阶段6是实质GPU训练**，不是只跑推理。阶段7是更进一步的Qwen主干适配器训练，数据与3090/Windows依赖前置目前为UNKNOWN，不能保证能跑；不能把阶段6的head训练冒充Qwen LoRA。若只有一个合法评测视频、没有独立训练视频，则必须停在训练数据门，不用评测/dev答案做训练以迎合进度。

## 科学口径与停止条件

- META-007证实50/50 UID、45个安全候选、两个媒体HEAD200且一段≤3.5GiB；3ef8559仅0/8请求。最新7cb9c6b才实际完成8/8 S3尝试、唯一媒体GET200并私有部分落盘64–128MiB，但**因UTC外层计时错误在约54分钟提前终止，完整视频不存在、GPU更新0**；旧预扣不复活。发布/剪辑/PTS桥接及Qwen本机权重仍未证；当前`NOVELTY=RETAIN0`，Charades `FINAL_MEDIA_STOP`持续。
- 实验链要可证伪：训练前AB作固定不调参基线，独立训练素材不泄漏dev标签；训练loss下降只证明优化正常，不证明问答提升、泛化、创新、统计意义或论文录用。**需要后续新批准的独立held-out评测**才能比较训练收益，不能看训练结果后挑dev问题和旧历史forward。
- 如无合法额外train QA，优先真实temporal head自监督训练，只能交`REAL_GPU_HEAD_TRAINING_COMPLETED`级别的工程证据；不得叫`REAL_QWEN_LORA_PILOT`。如有训练QA和可行依赖，再走阶段7，仍不承诺3090可容纳。
- 本轮Ego4D批准窗口按用户提供的有效期至2026-10-26，但前述AWS合同更保守地限制北京时间2026-10-25 23:59后不再发送新的数据请求。超过窗口不得凭旧审批重启AWS。
- 各阶段都要求显式上限、当前READY、无旧报告、原Codex会话新的执行消息；任何必要条件UNKNOWN都写`HOLD/NOT_RUN`，不可擅自翻版本、加数据、安装包、拉权重、改环境、重试、转移旧预算，亦不可持续后台执行。公开仓库只做文档交接，不推送原Windows实验工作区。

## 启动方式（不是自动连续执行）

截至2026-10-14，[4d902ef](https://github.com/floomeer83felix-source/vlm/commit/4d902ef870f201cd5b1df7536bd235ab5b6789be)已首次在RTX3090实际加载完整Qwen3-VL-4B-Instruct+SigLIP，针对本机24分钟公有电影跑完2通用问题×uniform12与SigLIP12的4/4真实Qwen生成；包含模型load/48真帧图文检索/生成GPU共38.906秒、allocated峰约8.51GiB。SigLIP P2覆盖1184.150秒低于均匀1464.630秒，四次都达到192token输出上限（自然EOS未知）。此项是**无标准答案**的长视频VLM技术可行性，不具有HourVideo得分或策略收益结论。

**唯一READY=VLM-HOURVIDEO-MATCHED-QA-012 / AWAIT_USER_MATCHED_EGO4D_MEDIA（尚不能执行）**。本机两模型与GPU技术障碍已消除，关键缺失是**与现存私有HourVideo dev_v1标注视频UID对应的合法完整官方Ego4D≥20min原片**和同版本/零时刻/PTS可核桥接。旧Ego4D历史.part不完整、来源AWS旧预算不可复用，不能把公有电影作为官方标注视频。请用户按其批准Ego4D权限自行取得**精确配对原片**，在原Codex长聊天提供本机确切视频入口、已获许可的私有标注/发布映射入口并明确授予本轮≤4次本地Qwen generate/GPU≤40分钟。012才可同轮CPU匹配→如果独立证据通过冻结2道答案保密的官方dev QA→uniform12/SigLIP12 paired推理→最后隔离答案评分；提前冻结384-token上限并记录natural EOS/截断。资格不全就HOLD/0模型调用，不重新下载或扫描磁盘。n=1视频/2问题仍非完整benchmark或统计显著，不形成novelty claim；Charades FINAL_MEDIA_STOP、NOVELTY RETAIN0保持。

# VLM-TRAIN-SOURCE-ELIGIBILITY-021｜009 已授权原电影训练资格的有限 CPU 只读复核

**2026-10-17｜唯一 READY / USER_AUTHORIZED_ORIGINAL_009_FILE_CPU_READ_ONLY。**

## 新授权的准确范围

用户在当前 ChatGPT 轮次明确**批准 Codex 对009原先明确指定的单个本地电影进行一次CPU只读资格检查**，只核实**文件是否仍存在、研究训练使用权利、完整性及其与既有HourVideo/Ego4D评测素材的隔离**。此授权不等于对旧009或019/020的新运行许可，不包括运行 TRAIN-PREP-001 的其他模型/环境步骤、GPU训练或真正媒体特征提取。ChatGPT仅把本021设为READY；用户还需在当前活跃Codex聊天发送新单次执行消息。禁止自动唤醒、连做下个父任务。

009公开证据：[009匿名实验回执](../VLM-LOCAL-LONGVIDEO-009/local-long-video-ab-receipt.md)：当年用户明示训练许可的官方美国Public Domain电影，单个WebM/VP9、480p、103,909,467B，container1465.597s，原CPU全解码43,924帧与严格单调PTS，原RTX3090两臂各100步。那些是**2026-10-14旧运行报告**，不自动证明2026-10-17原文件仍在、没有变化、如今权利仍覆盖该用途或独立来源被证实。

### 精确私有入口与禁止搜索

1. 安全同步**独立GitHub文档checkout**至最新main，读AGENTS.md、next-steps.md、codex-results.md、本README、009公开收据；检查020已结案、021唯一READY且无此前021 formal结果。如果任何冲突，停止。
2. 只从009原Codex私人会话或原任务已知的**首个且实际用于009训练**精确文件入口取得路径，不能从用户身份/公开描述猜测名称、不能列出候选或枚举目录、不能使用旧009另外2个候选、不能寻找新媒体、不许全盘/D:\\download/用户桌面/研究视频树/Charades/Ego4D/R1–R6搜索。若活跃Codex聊天不能可靠找回**准确这一个路径**，当即`EXACT_009_ENTRY_UNKNOWN_HOLD`并停止私有访问，等待用户另在私聊提供精确入口，绝不能凭约100MiB/24分钟描述反向发现。
3. 只对已验证的精确单个文件做受限CPU只读检查；核普通文件、非符号链接/重解析点和该路径必要的祖先安全属性；不改原文件、不打开其同目录其他内容、不读受保护QA、金标/题目、开发集私有标注、评测视频或旧实验预测/权重/检查点。只允许读取该文件本身、009原来可访问的**最小许可/来源证明记录**（前提是明确精确记录且不是受保护标注）及已经公开的009/013–018匿名来源组文字。无权利证明时`LICENSE_EVIDENCE_UNKNOWN_HOLD`，不能从“公共领域电影”四字自动推断所有司法辖区许可。
4. **存在性、完整性等级**：只读stat与原009基准字节数比对；以现有本地ffprobe在该具体路径上至多一次探测container/视频流/时长，调用本身最多30秒；如需要验证媒体包顺序/EOF，可在**已安装**现有PyAV中对这一份文件做**至多一次CPU有界video demux（不RGB帧解码）**，持续不超过120秒，检查packet PTS/DTS、EOF/异常，并记录与旧009真实全帧decode之间**方法差异**。若009原私人完整文件SHA可在其原私人可信记录精确恢复，可至多一次对该文件做顺序流式SHA-256比较，≤60秒；不要上传原/新SHA或任何可反推资产信息。没有可信旧SHA不能称immutable-hash-PASS；没有完整decode/远端hash认证不能把ffprobe+demux称为完整逐帧证明。新private值仅用于本机比较，公开报告只报非识别性一致/不一致/UNKNOWN。所有检测作业总单调计时≤**180秒**；安全超时监督器不可得则停在可安全完成的stat/公开证据检查，不启动无界demux/hash。严格按先验固定顺序，不复做旧009训练，也不对失败项重试。
5. **训练/评测来源隔离资格**：只能比对009已有且用户授权的匿名来源/许可证据和013–018已经公开的非身份汇总信息。检查电影素材与当前HourVideo/Ego4D dev/eval来源在实际录制、版本、物理镜头/剪辑及source-group层面是否具有可核独立证据；不同视频类型、UID不同、和“历史未读取Ego4D资产”**单独都不等于物理独立证明**。需要私人QA/eval UID/源映射、扫描/打开评测媒体或访问受限目录才能作出决定时，报告`SOURCE_INDEPENDENCE_UNKNOWN_HOLD`而不是越权检查或假称PASS。既往009该片已被用于训练和同片内部验证，因而不能把009旧同片validation包装成全新独立heldout。禁止根据旧dev gold对电影挑选、调参或来源准入。
6. 对这份明确单电影，仅输出四门三态：`FILE_EXISTS`、`INTEGRITY_EVIDENCE`、`TRAINING_RIGHTS_EVIDENCE`、`TRAIN_EVAL_PHYSICAL_SOURCE_INDEPENDENCE`，各标`PASS/FAIL/UNKNOWN`加来源证据等级；即使文件与许可PASS、物理来源证明UNKNOWN，则结论`TRAIN_SOURCE_021_PARTIAL_HOLD`，不能颁发正式TRAIN_CPU_PREFLIGHT_PASS或GPU训练许可。公开结论必须区分`009_HISTORICAL`与`021_CURRENT_READ_ONLY_OBSERVED`。有真实可验证四门才`TRAIN_SOURCE_ELIGIBILITY_021_PASS_ONLY`，仍非 TRAIN-PREP/GPU 放行。

### 绝对安全边界与交付

- **CPU只读；PyTorch/Torch/模型权重和SigLIP/Qwen推理/视觉特征/梯度训练/GPU/CUDA全部0。** 不使用旧019/020 runner或任何预算，不修conda/环境/pagefile，不安装、媒体下载/HTTP/HEAD/GET/AWS/API，不开云服务，不启动后台工作，不杀其他任务。
- 不转储视频、帧、图像、PTS序列、路径、文件名、source UID/映射、原/新hash、许可凭据或隐私数据到公共Git。不可公布具体电影名称/来源URL；可写抽象的许可证证据等级与匿名一致性。禁止写入旧009和原训练/评测目录任何文件。
- 此轮Codex允许在公共文档checkout中**仅新增** `docs/codex-artifacts/VLM-TRAIN-SOURCE-ELIGIBILITY-021/read-only-source-eligibility-receipt.md`、在`docs/codex-results.md` **末尾恰一条** `### VLM-TRAIN-SOURCE-ELIGIBILITY-021`。不能修改本README、AGENTS、旧009/019/020记录、next-steps和overview。旧合同TRAIN-PREP/GPU继续QUEUED/HOLD。
- 一次正常GitHub main push后STOP，等待ChatGPT审核。若原准确路径不在当前Codex上下文、证明不足或工具不可用，允许直接只写单份匿名HOLD收据并停止；不得重复检查、私下寻找替代媒体或把旧009推断冒充当前实查。

**科学状态始终：NOVELTY=RETAIN0；CLOCK_ZERO_ASSUMED_NOT_CERTIFIED；Charades FINAL_MEDIA_STOP。** 009此前单片时间顺序head梯度更新不是HourVideo问答机制收益，本021是训练来源合规筛选而非新训练运行。

# VLM-HOURVIDEO-MATCHED-QA-012｜从已跑通Qwen+SigLIP进入真实HourVideo标注匹配与条件评分A/B

**2026-10-14｜唯一READY / AWAIT_USER_MATCHED_EGO4D_MEDIA（受限：数据尚未就绪，用户未提供匹配媒体前不得执行本父任务）**。本父任务是为用户尽快做**有标准答案、可核分母的真实长视频VLM对照**而准备的下一阶段，**不是**已自动批准的数据下载或GPU前向。用户只能在原同一Codex长期聊天中**明确提供已经合法本机持有的对应完整Ego4D视频精确入口以及准许核对的本机HourVideo dev标注精确入口/既有私有映射入口**，再在同一消息里授权最多4次本地Qwen推理/合计GPU≤40分钟，才可执行。缺少媒体/合法用途或时间轴证据，STOP而不能把One Week电影或未完整Ego4D.part冒充HourVideo原片。

## 上游实证（严禁重复成功技术烟测）

- [4d902ef](https://github.com/floomeer83felix-source/vlm/commit/4d902ef870f201cd5b1df7536bd235ab5b6789be)已真正用用户本机完整24分26秒`One Week`+Qwen3-VL-4B-Instruct BF16+SigLIP F32，在RTX3090上完成两冻结通用提示×uniform12/SigLIP cosine top12的**4/4次Qwen generate**。模型本地safetensors、processor/tokenizer、图文SigLIP、offline torch2.5.1/transformers4.57.6运行PASS；48候选帧/1464.630s，GPU完整阶段38.906s、torch max allocated 8716.771MiB，**0训练更新**。SigLIP选帧P1/P2跨度1402.301/1184.150s，第二题不到20min；每题只与uniform重合3帧。所有4次Qwen输出都达到192 token上限，是否natural EOS未知（可能截断）。原011已经技术验收并结案，不再重跑4次无答案电影问题，也不能把其结果称为HourVideo正式问答准确率或策略改进。
- 历史CPU官方manifest已验证HourVideo dev约50个UID与Ego4D v2_1 manifest有交集、45个固定来源安全候选、两个S3 HEAD200、有一个≤3.5GiB，但**UID存在交集不等于两发布版视频剪辑/PTS同源同轴**。历史一次媒体GET只有私有64–128MiB `.part`、ffprobe`MISSING_MOOV`，不可解码、不得还原旧预算；本任务**绝不请求AWS、恢复.part或下载任意媒体**。HourVideo dev QA/标准答案和私有UID/map绝不上传公共GitHub。

## 进入真实可评分A/B前的绝对条件

1. **输入与权限**：用户手动取得一段完整、合法研究评测可用、时长实测≥1200秒的官方Ego4D真实源视频，提供其**一个明确本地绝对文件入口**；同时在原Codex聊天指出此前已许可的私有`HourVideo dev_v1.0_annotations.json`及与这段源文件对应的**精确已知**私有映射证据入口（不公开UID/桶/key/S3 URL），或只授权读取原已有任务单一明确入口；禁止扫描整个D盘、Downloads、模型缓存、科研树或重新下载。若用户没有上述完整匹配视频，则保留`AWAIT_USER_MATCHED_EGO4D_MEDIA`、**不应为同一个空媒体门发起新的父任务执行**。模型两目录按011用户确切授权根只读复核必要项，不因已跑成功就假定所有HourVideo问题兼容。
2. **先CPU核配对真实性**：视频容器完整、抽帧PTS有限有序/≥20min，并通过独立证据确认标注视频的video_uid、发布版本/镜头剪裁、零点与原始PTS的可逆映射。只有UID与v2_1清单交集、没有可复核的时钟桥接时，必须`RELEASE_PTS_BRIDGE_HOLD`，**不得做可评分比较**。不以用户手工公有电影、非标注Ego4D同名素材或不完整part替代。前台CPU只读限≤10min/文件路径严格白名单；不将标注文本/答案/UID/局部帧提交公仓。
3. **预先冻结样本**：只有对齐证据PASS才从指定视频对应的HourVideo dev问题中按固定非答案规则选**前2个有参考答案**的问题；先持久私有冻结问题映射、评测答案隔离、数据哈希/版本/PTS审计和2×2比较配置，不能看模型输出后换题或筛掉错题。参考答案永不进入prompt或SigLIP排序，只在全部运行结束后由隔离评分阶段使用；失败/invalid都计入固定分母2。
4. **本机真实配对模型**：同一PTS时轴48候选真实帧、每题uniform12 vs query-aware SigLIP top12、两臂使用Qwen3-VL-4B-Instruct同一safetensors/processor/像素预算/decoding参数（不看答案）、固定AB/BA交错顺序；Qwen genuine generate**≤4次**、no warmup、无训练/LoRA、不加载远程模型。为解决011全部截在192token的问题，可以在本新父任务**预先固定每次`max_new_tokens=384`**、真实EOS与是否截断明确分类，不因为输出内容改预算。每个尝试前fsync；错误不重试，未完成仍保留固定分母。RTX3090 GPU合计≤40min，新增torch allocator peak≤20GiB，父进程wall≤55min，两次free≥8GiB/util≤30%快照与自有互斥/他人已知作业保护；仅time.monotonic独立监护、不能杀别人进程/清他人缓存。
5. **评分前提独立**：只有官方标注和物理视频版次/PTS实际对齐证据已核时，才对实际最多2题×2臂评分，保留正确/错误/invalid/失败的固定分母及配对四格；否则**停止于CPU/HOLD、不允许将“只完成模型生成”记录为正式问答准确率**。这仍是**n=2/单视频极小pilot**，不能声称统计显著、正式整套HourVideo榜单、模型优势、新颖性/发表结果。原No-QA电影011数据不能与此评测混分母。

## 必须严格遵守

- **研究视频/模型/AWS/HTTP下载/云GPU调用=0**，Codex不自动查询下载链接、安装依赖或修改既有本地模型、视频、QA等输入。旧002/005–008/009–011父任务与账本不能重跑、不覆盖。不能用Charades媒体（`FINAL_MEDIA_STOP`），不能将HourVideo dev QA或答案用于训练/挑选/调参；`NOVELTY=RETAIN0`。
- 用户提供完整文件与私有标注/版次证据并明示新模型推理GPU授权后，**一轮**按上述前置门自动完成CPU校验→若科学资格PASS则GPU≤4前向→如果PTS/同版证据PASS才隔离评分。只能新增`docs/codex-artifacts/VLM-HOURVIDEO-MATCHED-QA-012/matched-hourvideo-pilot-receipt.md`和`docs/codex-results.md`最后恰好一条`### VLM-HOURVIDEO-MATCHED-QA-012`。公共回报匿名仅含资格PASS/HOLD分类、实际帧数/PTS时长、Qwen尝试/成功与输出EOS/截断、SigLIP选择差异/计算、GPU时长/峰值显存，以及真正可评分时的固定分母分类统计。严禁上传UID、QA原文/答案、视频、帧、原生成全文、模型/权重、私有路径、哈希/manifest对应表、原始日志。一次正常main push后STOP。

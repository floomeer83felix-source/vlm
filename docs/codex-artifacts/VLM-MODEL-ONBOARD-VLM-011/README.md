# VLM-MODEL-ONBOARD-VLM-011｜本地两模型文件验收→有条件执行真实长视频VLM 2×2 A/B

**2026-10-14｜唯一READY（AWAIT_USER_MODEL_PATHS / NOT_YET_EXECUTABLE）**。只有用户在原Codex长期对话**明确给出两套已经合法取得的本地完整模型目录**，并再次用同一条消息批准以下明示的≤4次本机Qwen生成/GPU累计≤40分钟，Codex才可执行本父任务。**GitHub READY、单独一条旧结果提交或普通“继续”均不得自行变成模型下载/推理授权。** 该父任务不是重新检查旧的两个缺失缓存位置；模型未到位时不应运行、也不应提交第二份相同`ASSET_MISSING`报告。用户如需自行下载，仅从指定官方完整模型仓库以原版本检查文件，不在Codex中自动联网下载/安装依赖。用户若不想下载，可提供此前已存在的其它精确本地模型目录，避免重复占空间。

## 上游验收与模型资产的已知条件

- [b295945](https://github.com/floomeer83felix-source/vlm/commit/b29594577fb52ee9a36836c75ca82d4142489499)验收：本机官方手工视频完整且存在（沿用009有据的1,465.464s PTS）；仅检查一个canonical Qwen缓存根和一个`google/siglip-base-patch16-224`缓存根，**两者该根不存在**，但**绝不能推断全盘均无该模型**。本轮Qwen真实generate 0/4、SigLIP forward0、GPU0。现成torch2.5.1、transformers4.57.6、PyAV15.1、OpenCV4.11、numpy1.26.4是模块存在证据，不表示Qwen完整加载、显存与processor架构兼容已经测试过。
- 官方精确仓库[Qwen/Qwen3-VL-4B-Instruct](https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct/tree/main)，完整仓库文件约8.89GB、两个`model-0000x-of-00002.safetensors`各约4.97GB/3.91GB，必须包含`model.safetensors.index.json`、`config.json`、`generation_config.json`、`tokenizer.json`、`tokenizer_config.json`、`chat_template.json`、`preprocessor_config.json`、`video_preprocessor_config.json`及其余官方文本词表资产等。仅下载`config.json`或Git LFS/Xet指针文本不可用；禁止用户资料推送至公仓库。
- 官方精确仓库[google/siglip-base-patch16-224](https://huggingface.co/google/siglip-base-patch16-224/tree/main)，模型`model.safetensors`约813MB，完整`config.json`、`preprocessor_config.json`、`tokenizer_config.json`、`tokenizer.json`、`special_tokens_map.json`等文本和`spiece.model`词表。需要完整同时包含文本与视觉塔的SigLIP，不能只拿vision-only或CLIP冒充同模型。优先safetensors而不是另外再下载重复体量的`pytorch_model.bin`。
- **推荐仅为示例，不视为已经存在路径**：`D:\models\Qwen3-VL-4B-Instruct`和`D:\models\siglip-base-patch16-224`。用户实际若放在其它私有目录，须提供精确文件夹；Codex严格按该两目录审核，**不得递归扫描Downloads、缓存、个人文件或原科研树**。模型文件不可上传GitHub，公开收据不得包含绝对目录、具体checkpoint哈希、任何视频帧/模型完整回答。
- 本父任务**媒体/模型研究网络GET/HEAD/Range/云API=0**，禁止安装/升级/量化依赖或改变已存在conda/驱动；不提供自动下载授权。用户可以在其个人浏览器/本地可靠下载工具通过官方页面完成下载，需确保至少~12GB模型盘空间（最好预留20GB+以防临时文件与加载缓存），随后仅传路径给既有Codex聊天。视频本身不需要再次下载。

## 同一父任务执行门与预算

### A｜从用户当轮给出的两根目录做一次离线真实性/完整性检查

1. 独立Git文档checkout安全ff-only sync main、重读最新AGENTS、唯一READY和本README、确认`docs/codex-results.md`还无本011结果。当前聊天消息**必须**包含两套目录及本任务GPU范围明确批准；否则**不要启动这个父任务**、不生产新的同质HOLD报告。
2. 两个用户指定且受限的普通目录（非reparse/symlink）内只读**固定标准文件和必要的权重分片/索引清单**，核静态身份、模型配置，单个safetensors header/索引/文件大小及是否为Git LFS小指针、processor/tokenizer配套可用。只能在这两目录下读取索引明确提及的权重分片；不追踪跳出目录的符号链接。存在性≠真正可加载，失败准确枚举MODEL_FILE_INCOMPLETE、PROCESSOR_MISSING、ARCHITECTURE_UNSUPPORTED、DEPENDENCY_MISSING等，GPU0，绝不尝试修复下载。
3. 本地模块spec/必要architecture CPU导入及`local_files_only=True`、`HF_HUB_OFFLINE=1`的from_pretrained白名单载入计划，预估VRAM资源/CPU offload可行性但**禁止自动改bitsandbytes/flash-attn/torch版本**。只有两个模型及配对processor的实际装载有资格后，才可进入B。既有`pytorch`conda/RTX3090+64GiB RAM的可用性不意味着任何4B模型必然能载入给定帧数。

### B｜有条件执行首个真正Qwen3-VL+SigLIP公开长视频选帧配对

遵守已冻结的[VLM-LONGVIDEO-VLM-BRIDGE-010](../VLM-LONGVIDEO-VLM-BRIDGE-010/README.md)科学问题与公平对照，**绝不重跑010历史零GPU检查**。本地官方Commons手动得到的完整`One Week (1920)`480p VP9视频，采用009有据的PTS跨度≥1200秒/样本完整性，无额外视频GET。先在用户前次明确授权的唯一两种确切文件名位置安全读取，禁止列出D盘其它文件。电影未附带有标准答案的QA，固定下列2道自然语言问题用于VLM可运行性：
- P1: `Summarize the main sequence of visible events in this video in chronological order. Mention only details supported by the images, and state uncertainty.`
- P2: `Explain what visibly changes between the beginning, middle and end of this video, and describe evidence from the images without guessing.`

同样48个按真实PTS覆盖≥1200秒的候选实际解码RGB帧。A每题uniform12；B仅用已核合法SigLIP文本/图像双塔计算对应prompt相似度从相同48中确定性选12，再按PTS排序，以**同一个Qwen3-VL-4B-Instruct**和同一输入大小/processor/权重、解码参数做paired推理。固定A/B交错顺序，最多**两题×两臂=四个实际Qwen generate尝试**，最大输出tokens每次192、do_sample=False、默认warmup0，SigLIP对应2条文本prompt的forward在已授权本机GPU预算内。无SigLIP就不能把motion/random采样叫query-aware；任一模型不满足门应在模型generate0时HOLD，不强行先跑A再补B。公开匿名只统计4次attempts/completions、每臂帧实际覆盖时间、总query selection/visual encoding/generate延迟、GPU用时与显存、tokens；不公开用户私人视频的帧、模型答复和私有路径。

**硬预算**：RTX3090本地GPU≤40分钟、一次父任务前台≤55分钟、新增torch framework max_memory_allocated≤20GiB（不包括驱动上下文真实开销）；双GPU状态快照≥2秒间隔各free≥8GiB/util≤30%，自己的命名锁/约定冲突保护，不将Windows C+G图形混合列表非空单独视作训练冲突。所有GPU工作用独立只监督本任务子进程的time.monotonic硬截止，资源不符就STOP，不清缓存/重置系统/杀别人进程，不OOM重试/自动改精度/下载模型。按指定已存在模型文档支持的非训练加载配置运行`eval()+inference_mode()`，若GPU显存不足明确报告`MODEL_GPU_CAPACITY_HOLD`。推理绝不算作训练步数。

## 科学边界、匿名结果与STOP

所有本轮提示**没有标准参考答案**，结果只是公开无QA电影上的VLM技术/计算对照；**不得计算问答正确率、显著性、方法泛化、HourVideo或Ego4D QA得分，也不能称Qwen训练/LoRA**。真正科学评估仍需合规视频+版次/PTS桥接+留出标准QA，Dev答案严格不参与帧排序/训练。现有009的单片uniform与motion各45%并不证明SigLIP检索优越，跨任务不能混作同一分母。

只允许新增`docs/codex-artifacts/VLM-MODEL-ONBOARD-VLM-011/model-onboard-vlm-receipt.md`及在`docs/codex-results.md`末尾一条`### VLM-MODEL-ONBOARD-VLM-011`；包含两模型资产可用布尔、GPU负载资格、Qwen generate实际次数、SigLIP forwards类别、匿名成功数、PTS span/帧数和开销、占用以及精准STOP状态。没有任何完整生成文本、帧截图、路径、散列或模型文件上传。一次正常main push后STOP。保持`NOVELTY=RETAIN0`、Charades `FINAL_MEDIA_STOP`、HourVideo/Ego4D release↔PTS桥接UNKNOWN。本任务不自动排队HourVideo QA/训练或下载其它模型。

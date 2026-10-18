# VLM-HOURVIDEO-TRAIN-PREP-001｜合并训练前CPU只读资格与静态环境预检

**2026-10-18：READY / USER_AUTHORIZED_COMBINED_CPU_READ_ONLY（唯一READY；未执行）。** 用户在本轮ChatGPT会话明确**批准合并的CPU只读TRAIN-PREP检查**。范围限：已公开许可证据、已知且此前获明确访问许可的非保护来源元数据、本机既有模型及processor静态文件/包元数据存在性、训练方案与泄漏门的纸面冻结。**不批准GPU、Torch/DLL import、模型forward或训练、私有保护QA/视频、研究下载、环境修复或其他扩展访问。** GitHub READY不会自动唤起Codex；用户在活跃Codex聊天须新发执行消息。TRAIN-GPU仍非READY。

## 同一父任务的独立四项CPU只读子任务

**先同步安全门：**安全同步独立GitHub文档checkout到main，重读AGENTS.md、next-steps.md、codex-results.md、本合同及009/018/019/020/021/022匿名回执。确认本任务唯一READY且无旧TRAIN-PREP-001结果、无脏checkout冲突，否则STOP。不得修改本地科研工作区Git或旧账本。执行前在本地设**单调累计前台CPU只读调查≤300秒**；无法安全监督则只读现有公开证据并在到达上限前停止。

**A. 许可证据/原训练电影身份**：复用022已实测的单一私有候选**本机文件存在、WebM/VP9 480p、103909467B、1465.597s、43924 packet EOF、PTS/DTS无异常**，绝不再打开或重新stat/probe/demux/decode/hash该媒体。仅审009已公开的用户历史研究训练同意、美国公有领域结构化许可证据及**已经明确授权的精确非保护许可/出处小型文本或元数据入口**，审计作品层权利、相关法域、当地文件与公开来源/转码绑定的证据等级。没有原可获授权的出处记录或可信旧hash则明确分别标RIGHTS_BINDING_UNKNOWN / ORIGINAL_009_IDENTITY_UNKNOWN，不因电影古老/名字和长度匹配直接判PASS。**不访问新外部许可网站或发研究网络请求**；普通GitHub文档协作网络同步例外。

**B. 物理来源隔离与泄漏审计**：仅从009、013–018、022已公开匿名历史收据和已经确切获得授权的**非保护来源分组结构元数据**，核电影录制/镜头/片段/source group是否和保留评测来源不重合；没有证据应标STRICT_PHYSICAL_SOURCE_INDEPENDENCE_UNKNOWN，不能以影片题材/拍摄年代不同或“旧实验未打开QA”代替实际证明。禁止读Ego4D/HourVideo dev/eval电影或QA、gold、题目、UID/私人来源映射、参考时间戳，禁止访问Charades。任何需要受限证据才能核定的条目单独HOLD，继续C/D，不绕过授权。旧009同片后段仅为内部验证，不能当新的heldout；开发集gold不能给优化器/教师损失/超参选择/checkpoint。

**C. 静态模型、processor、软件环境与资源**：只检查009/013–018**之前已获授权且已经确知的单一模型/processor精确位置**，用stdlib只读stat文件存在/必要symlink/reparse属性和小型JSON/processor/tokenizer结构清单；每个实际读入小型配置≤2MiB，不能枚举目录、扫描cache或读取任何权重张量/大模型/私人checkpoint内容，也不新建模型目录。只用Python标准库`importlib.metadata`查已安装包**分发元数据**（torch、transformers、av、必要依赖版本等），**严禁import torch/transformers、DLL加载、torch.cuda、NVML/nvidia-smi/GPU驱动探测**。可读Windows主机RAM/commit及磁盘空闲概况（不输出设备路径），但没有GPU资源实际检查则标GPU_RESOURCE_UNVERIFIED。没有原本明确的资产绝对入口则ASSET_ENTRY_UNKNOWN，不能猜测/搜索替代。静态安装记录不证明runtime能导入或实际RTX3090可运行：019/020 OSError历史保持独立，不重试或修改pagefile/conda/驱动。

**D. 科学协议与未来训练资源纸面预注册**：定义仅在许可与严格源隔离皆合格时才可执行的`TRAIN_HEAD_SELF_SUPERVISED`：仅训练电影内互斥训练/验证时间块和source组、正近时/负远时对、时间PTS/采集零点风险标注、预冻结seed、≤2线性层、≤1,000,000可训练参数、冻结现存视觉主干及Qwen、AdamW、单次最多200 optimizer steps、batch≤8、梯度累积≤4、单个私有checkpoint≤256MiB、新临时产物≤2GiB、**计划GPU时间≤60分钟**。本轮只是设计预算，**非授权GPU、训练、Qwen LoRA或评价**。代理loss优化不能被表述为QA改善、跨源泛化或创新。

**分项不中断原则**：A/B的许可、身份和隔离若UNKNOWN，应如实记证据等级，并继续完成C/D。四项都必须有`PASS / UNKNOWN / HOLD`、证据出处类型（不能公开可识别资料）及下一轮仅最小缺口。综合状态允许`TRAIN_PREP_CPU_STATIC_COMPLETE_WITH_HOLDS`或真实支持的`TRAIN_PREP_CPU_STATIC_COMPLETE`；**即便静态信息全部PASS，也不等于Torch动态就绪、TRAIN_CPU_PREFLIGHT_PASS或GPU准入**，实际执行还需新的安全与权限门。安全冲突/总监控无法成立除外。

## 不可越界及交付

仅CPU只读元数据工作；**GPU和GPU API 0、Torch/Transformers/CUDA运行时import 0、真实电影媒体读取/探测/解码0、模型权重读入0、梯度和更新0、私有QA/gold/eval媒体0、研究数据/网络下载0、安装/环境修改/私有内容写入0、旧实验重跑0**。不可查找多个候选源或其他隐私目录，不能更换安全门。合法非保护小记录具体路径未获明确授权即UNKNOWN而非自动索取访问。

Codex **仅**在公开main新增`docs/codex-artifacts/VLM-HOURVIDEO-TRAIN-PREP-001/cpu-training-readiness-receipt.md`并在`docs/codex-results.md`末尾追加恰一条`### VLM-HOURVIDEO-TRAIN-PREP-001`。匿名报告列A/B/C/D状态、按权限实际读取的最小类别与次数、静态资产和工具版本是否存在、风险与下一项最小必要条件、未来预算为非执行提案；**不得提交**私人媒体路径/文件名/影片名称/许可来源精确URL、模型资产位置、UID或source map、hash、raw日志、权重、checkpoint、受保护QA/gold。不得修改本README、ChatGPT计划、旧历史文件。一次常规fast-forward-safe push main后STOP，等待ChatGPT验收；TRAIN-GPU继续QUEUED/HOLD。NOVELTY=RETAIN0，CLOCK_ZERO_ASSUMED_NOT_CERTIFIED，Charades FINAL_MEDIA_STOP。

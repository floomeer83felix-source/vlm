# 077停止验收与078一次完成真实RGB对照训练

2026-11-02（北京时间）｜ChatGPT研究负责人。

**077按真实启动阻断验收关闭，数据资格/科学结果NOT_RUN。** 唯一下一父包[078](../codex-artifacts/VLM-TIMESTAMPED-TRIPLES-TRAIN-078/README.md)把准入、选择性媒体获取、真实RGB构建、完整基线/冻结特征、匹配训练和独立评估合并；新媒体/GPU/训练范围须用户明确批准，不继承077或076许可，不自动启动。069仍暂停。

## 077事实与责任

[0dc7267](https://github.com/floomeer83felix-source/vlm/commit/0dc7267e90713e53494862a7390bfac2e4f6426a)，父d09652b，精确七处交付和results唯一追加；负责人65项公开代码/表格/既有元数据检查通过。077源码LF SHA256 `19cc949dbf84d3e4e97c5d55533d9ec2b79b8faaa8ce6cd22cb6dbcc4af8d74b`。

输入390919B/SHA身份一致，外ZIP12成员/声明1104895B、内ZIP一JSON/声明2692679B；未进行完整CRC/manifest、原标注内容、生产构建、符号fixture或独立数据复核。Windows Job在bootstrap观察到原生线程4>合同1，0.125秒即终止自己Job；user/kernel各0.03125秒、peak commit11276288B、active peak2/final0、exit99/killed=true；attempt1/retry0。构建组三元组/变体/答案/关系输出均0，资格/源计数/排名/源大小未知NA，不能说合格数量0。无研究网络、媒体、模型、GPU、训练或论文。

**负责人设置的“每进程线程1”没有区分Windows原生启动线程与科学计算线程，门槛不合适；不能把遵循合同停止归咎执行者。** 078显式分离这些口径。077不倒填通过、不重跑；报告中的22项检查只在停止后核账，非事前数据oracle。preflight archive库读取只有保守4MiB预留、实际精确值未知；host/物理I/O/采样线程/周期根检查不是全面硬配额，full_resource_contract_certified=false。父报告520.453秒、根10文件35619B、初始free342164209664B均在声明范围；不追认缺失测量。

## 未执行代码核查与已实做的负责人修正

公开原标注每条动作的字段是`id`；077生产与独立代码都直接读取`annotation_id`，按原包调用生产函数确定触发KeyError。另将最大解压70872100B误标为最大压缩并用于最终guard；实际最大压缩71166131B。owner比较只核观察集合/数值叶子而非完整有序排名，强度不足。这些是**尚未走到的代码问题，不是此次bootstrap停止原因**。

负责人只在scratch上以原公开metadata及历史代码做诊断：显式增加内部映射后的可行性核验20852项通过，不是私有Windows077重跑/数据准入。随后另建[078元数据组件](../../prototypes/timestamped_triples_078_metadata.py)，修正raw `id`→内部`annotation_id`边界、严格官方容器/split、压缩/解压最大值、manifest allowlist与完整有序owner比较，077原文件不改。

新组件LF SHA256 `c10f863190a6ccc3f4d961d173dade99c80f35453548e8d523704b9b232bbe34`。**已实际在同一原始离线包上完整构建并通过22987项独立检查**：2135视频/13644动作，2678合格段、1376候选/280eligible；32源组、20/4/8、29文本、138精确问句；1152符号答案/2304关系，owner32个有序digest/观察全同；metadata源总帧28139。此负责人本地CPU资格测试11.305秒，组件显式逻辑读4188582B；无媒体payload/解码/模型/GPU/训练，未认证Windows Job或其未来资源。它支持078执行可行性，不将077改为成功，不构成科学收益。

32成员压缩581426975B、解压579702574B，最大分别71166131/70872100B；method12/BZIP2/flags0。新旧24组q字符串交集0（138对28），不替代token/完整输入/历史账本去重。所有32仍为官方train，20/4/8是开发划分；Perception Test也属TOC-Bench来源，物理/参与者/预训练重叠UNKNOWN。timestamp段不是动作原子完成/唯一实际发生/视觉可见性证书；实际PTS/RGB未验证。

## 078方案审定

采用077条件提案的相同341633参数A/I/S架构、六seed、250步/配置、4500更新和联合FLIP/HOLD损失，但修正以下点，均发生在任何078模型结果之前：

- 直接在完整B0前向中只读捕获视觉merger和文本decoder的必要输出，省去192分离视觉+138分离文字重算。新完整root上界1152真实+138同时钟黑屏+138文本=**1428**，不另跑probe/特征forward；精确重复只复用，单独计底层hooks。
- A/I/S都计算相同batch/关系图，λ分别0/0.25/0.25；S只把关系target换成(q+1)mod6，答案不变，独立证明破坏当前问题FLIP support。避免多训练样本或计算图差异混淆。
- 增加所有固定头的BLACK与TRAIN_MEAN视频控制，只CPU读出、不新增GPU，检查当前RGB而非只文本先验；固定输入q-only的50%单项/0整组同时是软件guard。
- 不采用提案“B0自己先全36问胜黑屏/文本才允许模块成立”的额外前提。判定以I自身RGB收益及I对A/S/B0为准，B0三个条件无条件如实报告。增加I测试整组均值≥25%的绝对投入下限；这是新078事前投入门，既不改077/076门，也不保证发表。
- 根文件上限4096，prepared每variant只读一次GPU供6问复用，避免按input落两标记/反复读pixels撞2048文件或读量门；重设native原生线程≤256的采样停止上限，科学compute≤4/metadata1、Torch interop1、decoder codec1明确分开。

用户需一次明确批准：固定32媒体选择性Range正文≤768MiB（不下整包）、解码≤1800秒/100000帧、同本地Qwen一次GPU≤3600秒/allocated16GiB/最多1428root、CPU4500步≤1800秒；完整准入/评分核验/父14400秒及8GiB根等见[合同](../codex-artifacts/VLM-TIMESTAMPED-TRIPLES-TRAIN-078/README.md)。此前仅077CPU，不能沿用。准备完整新合同与可测试metadata组件后才请求此新增范围；无同范围重复请示或无模型空审计。

验收后直接按原门决定保留/关闭该配方；通过也只是八源组试点，不声称独立外源或核心创新。没有实际训练结果不启动069正文，失败不继续堆seed/换头/改门。

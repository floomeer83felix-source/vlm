# VLM-HOURVIDEO-NEW-SOURCES-017｜已冻结R1–R3三段合法新视频的完整性验收与条件配对评测

**2026-10-15｜唯一READY / AWAIT_USER_COMPLETE_R1_R2_R3_MEDIA_AND_NEW_GPU_PERMISSION（数据未取得，不可执行）**。本任务不是下载授权，也不是同一个空数据门的下一份报告。用户自行通过已有Ego4D官方账户/许可与先前016本地私人UID命令逐段获取完整官方`v1/full_scale`视频以后，**至少有一段可确切定位的完整媒体**，再在当前/安全交接后的Codex聊天给文件确切私有入口、已授权HourVideo dev带gold标注入口及明确新GPU预算，才执行本父任务一次。缺新媒体时不启动，不上传空HOLD；不自动下载、重试、HEAD旧AWS、扫描磁盘或以013/014旧素材替代。

## 研究依据与冻结样本名单

- [016匿名名单 ae014b4](../VLM-NEW-SOURCE-ROSTER-016/source-roster-anonymous.md)从用户合法私有HourVideo dev(50条)/Ego4D官方release-1 manifest(9645 unique rows)结构联合获得47个元数据候选，固定六个匿名不同来源组候选；**R1优先46.39min/原39题/结构非图像39，R2 73.28min/39，R3 50.05min/原41/显式image排3/结构非图像38**。这116仅是**结构资格数而非最终有正确gold且不依赖外部视觉资产的可评题数**，未读gold值/问题内容，也**不知道文件字节、远程状态、独立物理采集证明或annotation零点映射**。R4–R6为已冻结备用，不得因R1–R3模型结果不佳而改选；若原优先视频不能合法获取，保留`MEDIA_UNAVAILABLE`原因，另立新父任务前不把R4代入017。
- [013 bf5e36a](https://github.com/floomeer83felix-source/vlm/commit/bf5e36ad216c33e6cb04d2493c9e5fce050f7713)同demo：uniform6/37(16.22%) vs SigLIP12/37(32.43%)；[014 e7f654a](https://github.com/floomeer83felix-source/vlm/commit/e7f654a2acb93fed196da0ea4d361cb14bc1725f)不同sample：uniform11/29(37.93%) vs SigLIP9/29(31.03%)，**方向反转**，各自非显著、CLOCK_ZERO_ASSUMED_NOT_CERTIFIED。015审计`NO_GO_SIGLIP_STABLE_ADVANTAGE / GO_REPLICATION_ONLY_IF_NEW_DATA / PAUSE_FURTHER_GPU`。新任务**只是验证既有方法跨新来源结果与资源可靠性；绝非新机制或默认SigLIP优越**。

## 用户手动获取步骤（不属于Codex可执行工作）

1. 仅在已有合法有效Ego4D准入下，先将016私人Codex回复中的R1精确UID代入**本机已安装且`ego4d --help`已核参数**，选择`full_scale`、`v1`以及`--video_uids`单个UID，输出到用户自主指定的私有下载目录；下载每段前先自行确认可用存储/文件预算。**未知远端大小不能承诺最省流量/成功率**；如带宽/空间/权限不足，只获取R1，不许Codex自行补下载缺失媒体。已验证完整后再依次R2、R3，未授权者不碰。命令模板：`ego4d --output_directory "<PRIVATE_DEST>" --datasets full_scale --version v1 --video_uids "<R1_PRIVATE_UID>"`（只是模板，不保证本机CLI相同语法）。
2. 下载完成后，**只在本机Codex聊天传确切绝对MP4路径及对应R1/R2/R3的私有识别信息、完整性/来源合法使用凭据入口**，不在公共GitHub提交真正UID/路径/哈希/媒体、金标文件或下载签名URL；验证对象完整之后保留已下载文件，不自动清除或覆盖旧历史.part。
3. 仅准备R1视频也可以做一次**新视频单来源探索性A/B**，但为了更有研究意义，**优先攒齐R1–R3三条再一次执行017**，避免分三轮重复授权/统计多重窥视。R1缺失，不能用R2或R3的好成绩替代R1的预注册总体；新媒体到位前不要空跑。

## 017实际执行门：一次性CPU核验→条件GPU→条件最终评分

1. **单轮新授权**：用户在本017触发的原/已安全交接Codex聊天明确批准**最多3段已完整合法下载的R1–R3新媒体，最多232次本地Qwen3-VL generate（2×(39+39+38)上界），新GPU累计≤40分钟、torch新增allocated峰≤20GiB、整个执行≤90分钟**，只针对本任务；旧014/013额度均已耗尽/无继承。没有媒体入口或新GPU授权则017不开始。保留模型根与私有题库先前用户授权范围，但当前如无法安全精确识别须询问而非扫描。
2. CPU只读每段用户**确切路径**，不扫描Downloads/私人根、不加载旧part；验证完整非symlink MP4、有合法来源/相同v1 release元数据与对应UID、媒体真实帧PTS≥1200s/有序、video duration与官方对应元数据无异常，并审查是否存在已用013/014同物理采集/裁剪重叠的证据。独立release/剪辑/annotation t0→媒体PTS来源证据未提供则只能用预先冻结的`MEDIA_PTS_DIRECT_WHOLE_VIDEO`名义全片假设，明确`CLOCK_ZERO_ASSUMED_NOT_CERTIFIED`，**不可报官方HourVideo原榜score/时钟认证PASS**；如源与QA的实际对应关系不足、严重不匹配、非法或视频坏则该片**MEDIA_CONTENT_MAPPING_HOLD且GPU0**，不因其他结果好而换片/放宽门。
3. 按013/014**相同nongold资格规则**，在每段视频获准私有gold标注的**隔离资格核验器**里，只用schema确认五个A–E非空选项、gold标签**有效但不传其内容值**给策略或推理线程、显式外部辅助图片/文字外部asset引用真实排除，冻结全部符合资格的题目（各`N<=39,39,38`，**若少于10则报`INSUFFICIENT_QA`，该片GPU0但不能替换新视频**）。按源ID的预固定R1、R2、R3顺序逐片执行，不因旧013/014成绩或新的输出筛题，实验完成前gold只准隔离计分器读取。
4. 技术两臂**绝对冻结原013/014配置**：同完整PTS 48个实际时序RGB候选，A uniform12，B SigLIP图文双塔F32仅对问题文本(不含选项/gold)做cosine top12后恢复PTS，同Qwen3-VL-4B-Instruct BF16+processor/visual grid、同MCQ原题与A–E五选项提示、确定性`do_sample=False`、`max_new_tokens=64`、严格唯一单字母A–E parser。每题双臂AB/BA交错，GPU所有模型load/图文encode/generate计入≤40分钟，显存新增分配≤20GiB，先2次free≥8GiB/util≤30%、已知冲突/自有互斥审查。每个真正generate前私有fsync ledger预扣；不重试失败、不重放013/014已观察题、不训练模型/LoRA/selector。总尝试≤232；CPU受限抽样而不是全量重复解码每片百万帧，任何超时/OOM单次安全STOP，仍保留原题分母与NOT_RUN。
5. 只有全部本轮模型进程退出后才启用独立金标评分器，对每视频各自冻结题集合报告`correct/N`、wrong/invalid/NOT_RUN、两臂paired both/A_only/B_only/neither、选择PTS覆盖、帧重合、realized视觉token/视频处理格、SigLIP开销/Qwen load/processor/generate时间、GPU/VRAM；**每段都是独立统计单位**，不能把全部题数当独立视频数。若≥2条新合格独立来源视频完成，可以报告事先规定的**来源等权macro差**和每片方向，完全禁止基于结果挑只正的来源；即使3条完成，样本源数也不支持显著性/泛化/论文新机制主张。若仅1条新片执行，明确`ONE_NEW_SOURCE_EXPLORATORY`，不将其冒充完全复制完成。旧013/014两个来源只作为看过的历史参照，**不得与新来源N加权混成“官方五视频榜”**。
6. **仅匿名公共结果**：本017只可新增`docs/codex-artifacts/VLM-HOURVIDEO-NEW-SOURCES-017/new-sources-paired-receipt.md`并在`docs/codex-results.md`尾部恰追加`### VLM-HOURVIDEO-NEW-SOURCES-017`一段，正常main push一次后STOP。原题/选项、gold/UID、原模型回复、私有路径、CSV/manifest/原日志、源重新识别映射、权重、任何视频/帧一律不上传；输出仅R1/R2/R3匿名符号与聚合统计/资源。继续`NOVELTY=RETAIN0`、`CLOCK_ZERO_ASSUMED_NOT_CERTIFIED`、Charades`FINAL_MEDIA_STOP`。只有用户具体本轮权限才能执行，GitHub READY与README本身绝不唤醒Codex或授权GPU。

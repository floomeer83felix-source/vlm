# VLM-NEW-SOURCE-ROSTER-016｜一次性冻结新来源HourVideo候选清单与官方单UID人工下载计划

**2026-10-15｜唯一READY / USER_TRIGGERED_LOCAL_METADATA_ROSTER_ONLY**。前一015已否决“已证明SigLIP检索帧稳定比uniform好”；下一科学瓶颈是真正**至少2–3个未使用、合法、同源/发布可匹配的视频来源组**，不是另一轮Qwen推理。该任务**完全CPU、只读、有界**，一次性挑出至多6个新候选并按预注册非答案规则指定优先顺序、给用户官方单UID人工下载步骤（不执行），让用户尽可能一次性准备2–3个可评真实新视频。**不存在已确认可下载、已取得或可认证v1时间轴的候选这一事实基础；本任务不作这种承诺。**

## 已完成事实与范围边界

- [013](../VLM-HOURVIDEO-WHOLEVIDEO-QA-013/whole-video-provisional-qa-receipt.md)：已观察官方demo，N37，Qwen uniform6/37，SigLIP12/37，B−A+16.22pp（同一物理视频、未独立认证零点）。
- [014](../VLM-HOURVIDEO-CROSSVIDEO-014/crossvideo-heldout-receipt.md)：已观察另一个官方public sample，N29，Qwen uniform11/29，SigLIP9/29，B−A−6.90pp（不同canonical UID，但真正物理来源/时间桥未独立认证）。**这两段UID/相同源视频的重新转码或片段均不入新确认候选**。
- [015](../VLM-REPLICATION-DIAGNOSTIC-015/replication-failure-analysis.md)复算全部公共paired表/统计无误，`QUERY_SAMPLING_SUPERIORITY_NOT_ESTABLISHED`、`NO_GO_SIGLIP_STABLE_ADVANTAGE`、`GO_REPLICATION_ONLY_IF_NEW_DATA`、`PAUSE_FURTHER_GPU`。没有私有逐题误差权限，不得冒充机制原因已定位；`NOVELTY=RETAIN0`持续。
- 历史HourVideo dev vs Ego4D v2_1 manifest约50个UID有交集、约45 metadata候选（早期有AWS元数据/下载安全任务）。**UID交集与宣称`v1`或`v2_1`同完整来源、裁剪、annotation t=0/PTS一致不是一回事。** 014第二公开sample是由用户手工`v1/full_scale`单UID取得的，但这不证明任何新dev来源均有同下载许可或完整媒体。

## 仅在用户发送一次新的授权消息后运行一次父任务（用户可选择最少信息）

1. 在Codex当前或压缩交接后的长期会话中，用户明确授权：**只读先前已确认的两个私有小型元数据来源**，即（a）已获准本机HourVideo `dev_v1.0_annotations.json`或它的授权不含答案ID/QA资格摘要，（b）已取得/合法拥有的官方Ego4D release metadata manifest与其中显式版本/容量/时长信息的**确切已知本地入口**；可另授权已已有的`samples_v1.0.json`作为排除已用两个UID之用。必须是先前相同Codex会话已知的精确路径或用户明确新给的确切路径，**不能全盘/Downloads/HF缓存递归搜索**，不读取视频帧/原QA逐题文本/答案字符串。新会话如果找不到精确入口，就向用户只问一次路径而不执行/提交空父任务。过去曾获取/许可的元数据访问不自动升级为无限新访问。严格限制一个已知小文件/既有清单的局部读取、来源互斥记录、不复制敏感标注到公共Git。
2. 首先**静态核真实可用性**：每video UID在合法dev题库中至少10道schema有效的纯文本5选项视频MCQ（只验证gold字段存在和schema，不读取gold内容值/答题答案；不得调用现有Qwen），媒体元数据报告完整时长≥1200秒、预计官方full_scale单文件体量，如果明确存在该指标才排序成本。剔除013/014两条及任何已知同来源转码/片段、此前非法/Charades `FINAL_MEDIA_STOP`项。release版本可用性和下载许可须**显式来自元数据与用户已取得的官方授权**；仅`dev_v1.0`与Ego4D `v2_1`同UID而v1原片未知，应标`VERSION_BRIDGE_UNKNOWN`、**不得承诺可评分正式映射**。
3. **冻结客观排名**（不看答案/过去Qwen预测/具体问题内容）：来源资格优先（优先真正HourVideo关联Ego4D v1/full_scale、且version/clip-length证据较强）、源组独立性证据、可用有金标题数、实际元数据可比体量小者、长度满足20min且较短者、最后对匿名UID使用stable deterministic sort。每条件的UNKNOWN应保持UNKNOWN，不能发起Head/Range/AWS GET来“试试看”。输出最多**6个匿名候选**，其中**最优2–3个建议用户先手动获取**；如果全数都仅v2_1无桥接，明确`NO_SAME_RELEASE_CANDIDATE_VERIFIED`、不得虚构排名PASS或盲下旧part。
4. **单UID下载计划而不是执行**：针对确认合法的每个优先候选，在**用户本地Codex的私人会话中**给官方Ego4D CLI `--video_uids`/指定`--version v1`与`full_scale`的一次UID过滤示例，所有真实UID/具体S3/object key/下载地址只留私有会话；如果该CLI版本参数未经当地`--help`验证，用模板而不是宣称精确可直接运行。无新CLI安装/网络测试/下载，无自动运行。提醒用户核本机存储容量、网络、许可，优先按单文件下载、确认完整后才进行新GPU测试。**不可从已有v2_1 HEAD元数据直接推断v1文件可下载或合法发布对齐**。
5. **隐私/交付**：最多新增`docs/codex-artifacts/VLM-NEW-SOURCE-ROSTER-016/source-roster-anonymous.md`，仅包含metadata资产入口状态、候选数量及匿名资格/排除/有金标题数/预计容量区间、v1/v2_1版本信任等级、缺失门、优先2–3候选匿名索引、建议官方单UID人工下载流程（命令使用`<AUTHORIZED_UID>`占位），严禁真实UID、具体路径、个人登录信息、密钥、视频URL、私有真实QA/答案、源重识别映射或视频帧上传公共GitHub。在`docs/codex-results.md`末尾恰追加一段`### VLM-NEW-SOURCE-ROSTER-016`，正常push一次STOP。若缺元数据/匹配证据仍记录具体原因，只要合法读取了明确授权输入就提供实质候选审查；若压根缺精确入口或用户授权则**不启动、不推空报告**。

## GPU/科研二阶段：尚未授权

- **本016 GPU=0、Qwen/SigLIP forward=0、训练=0、旧视频重解码=0、视频/模型新网络下载=0**；CPU筛选≤10分钟且不改科研环境/缓存/conda/驱动。Github文档安全同步是唯一网络协调例外，用户私有QA标签永不用于训练/检索或公共上传。
- 后续用户**自行**依据合法渠道取得至少2–3条完整新官方视频并提供精确本机路径，先通过真实release/剪辑/源独立性/PTS或明确未认证假设的公平评估门，再由ChatGPT书面冻结新**来源级**效应、强对照/无效与失败分母、power计算和真实GPU调用预算。直到那时`PAUSE_FURTHER_GPU`，旧014剩余额度不继承。未来即使新采样方案更好，也须Q-Frame、DIG、2026RL selector等机制先例核查，不得先称新颖/SOTA。

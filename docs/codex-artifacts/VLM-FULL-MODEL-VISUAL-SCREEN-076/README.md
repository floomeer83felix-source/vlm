> **已于2026-11-02验收关闭，不重跑。** [382ef12](https://github.com/floomeer83felix-source/vlm/commit/382ef1225d9e7916444b8ba979dd2192666c0d53)432项完整；REAL单项76/144低于TEXT97/144、四格均0/55，原门FAIL，停止本入口新适配器训练。[验收](../../research-decisions/post-076-review-and-timestamped-triples-2026-11-02.md)保留codec线程/资源覆盖缺口。当前唯一下一任务[077](../VLM-TIMESTAMPED-TRIPLES-077/README.md)仅CPU离线标注构建，无新媒体/GPU/训练。以下原合同及授权按当时状态逐字保留，旧READY和“暂无结果”均为历史，不构成新授权。

# 076 完整冻结Qwen：32帧真实/同时间戳黑屏/仅文本二选一筛查

2026-11-02（北京时间）｜ChatGPT研究负责人。**唯一READY：APPROVED_076_FULL_MODEL_GPU_SCOPE / AWAIT_FRESH_076_START。** [075验收](../../research-decisions/post-075-review-and-full-model-visual-screen-2026-11-02.md)后不再在当前冻结merger/小头方案上调结构或训练。先补完整主干是否利用当前画面的基础基线；D迁移和070关闭，069暂停。不是新算法或新盲测。

> **当前授权状态：用户已于2026-11-02明确批准本协议GPU600秒/allocated16GiB/最多316次完整前向及现有24视频32帧范围。** [授权回执](./authorization-receipt.md)。第1节的明确授权条件已满足，相同范围不再次请示；本地用户新消息明确076后执行，全部准入/预算/角色隔离/一次父包STOP规则保持。当前仓库尚无076结果，本回执不作为已经运行模型的证据。

## 1 新授权、同步与已有资产

[AGENTS](../../../AGENTS.md)要求新的GPU/model操作明确授权。用户需明确批准**076本地冻结Qwen3-VL一次加载，GPU累计≤600秒、allocated≤16GiB、最多316次完整主干前向**，只用已存24原视频做32帧输入，研究网络/训练/生成/论文0。074剩余额度不继承。未批准只报NEEDS_076_FULL_MODEL_GPU_AUTHORIZATION，不读取媒体/模型payload、不建研究根/append或交空阻断包，不消耗任务。

批准后用户在当前Codex新消息明确076。安全同步独立文档main，读AGENTS/最新看板总览/results、本合同、075验收、074和075闭合/公开实现；确认唯一未交付条件READY。仅由已有明确handoff定位074/075私有根，不扫描磁盘，不改原根/锁/账本/失败或public科学历史。

允许精确只读074：parent/Job/code/model/input/asset seals和必要模型身份catalog、24个已解出原视频及media-manifest、observations/固定144问、评分专用scoring-labels及必要身份绑定。075只读必要parent闭合（不需要其小头state/feature/逐项输出）。沿已登记模型catalog读取同一原Qwen3-VL本地权重/config/processor与封存安装源码身份；若074catalog需精确回指父catalog才能证明模型身份，仅该登记文件，不递归查旧数据或读取旧QA/训练/开发答案。无新模型/依赖安装、环境迁移或远程代码。

先持久父起点（首次Git前）、初始free实际值和全部预算/Job/ledger、预处理/完整前向/评分/独立核验代码，再第一次研究payload读取。所有源码及实际矩阵在任何真实解码/模型STARTED较早者之前封存；后续不改prompt/精度/采样/代码重试已消费输入。

## 2 固定数据与三条件

同074的24视频/144严格before问题/28精确文本与tau，发布者exact-complete-order派生标签。独立核身份及固定观测/标签绑定，不再选样/修答案/换视频/新增标签。来源并非新盲测；严格完成/非重叠/唯一发生、物理录制/参与者/旧源/预训练暴露仍UNKNOWN，真实受控事件重排HOLD。

每视频一次新32帧准备：沿074/068原真实PTS、CFR-clock允许条件、均匀32中点/最近PTS，224RGB，必须32不同帧索引；记录原时长/fps/PTS/实际遍历帧等。若不足，不退回12/复制帧/换样；先保存实际与限额再STOP。重新decode是为新32帧输入，不能重放原12帧/旧头或任何历史QA forward。

同本地processor/默认chat template，唯一用户文本为原问题（已含Answer Yes or No），add_generation_prompt=True；不放原事件完整列表、答案、视频ID/源名/路径或其他问题。不得依据结果增加system措辞/思维链/提示词候选。只在约定assistant首续写位置取下一token分数，预检该位置/模板语义可用；若模板以不兼容thinking前缀开始，不猜位置或在正式调用后改模板。

条件固定顺序REAL32→CLOCK_BLACK32→TEXT_ONLY：

1. **REAL32**：上述真实32RGB帧和对应真实frame metadata/current q。
2. **CLOCK_BLACK32**：32张RGB全黑图，使用**该视频同一份**真实metadata/帧索引/时长/fps/时间戳。独立CPU核每个q的input_ids/attention_mask/video_grid_thw/其他非pixel字段与REAL32逐字节相同；只有pixel_values_videos不同。不用一个统一假时钟替代，否则不能排除真实时长/时间token线索。
3. **TEXT_ONLY**：同chat文本当前q，无视频/视觉placeholder/时钟。按实际token输入精确去重，28文本输入映射144逻辑项，同一q不得依赖当前video/index/label或另一个输出。

最多一次CPU processor-only合成32帧fixture，无权重/真实root前向，核原temporal_patch2/merge2下32帧grid[16,14,14]/pixels[3136,1536]和784视觉占位token等实际接口。真实REAL/BLACK的全部非pixel一致检查及输入封存须在GPU前完成；不把fixture计入研究效果。模型结构/本地来源identity不合即停止，不修改库/分辨率/patch/帧数。

prepared输入采用内容寻址共享pixel张量和每q独立token/metadata引用：REAL每视频一份，黑屏pixels如确切相同则全批只一份（真实时钟留在各条非pixel字段）；pixel落盘用原模型所需bf16，input_ids/mask/grid保持原dtype，转换顺序在正式STARTED前固定。GPU可一次读取已核pixel缓存后供不同完整q调用复用。不为144个q复制相同约9.6MB pixels/将新准备输入读量撑大，任何去重必须核完整实际字节。每完整前向只保存Yes/No两logits、margin和预测，不写全词表/全序列logits或多份中间大feature。

## 3 固定基础模型二选一，不训练/生成

原Qwen3-VLForConditionalGeneration，bf16/SDPA/local_files_only/trust_remote_code=False/eval/所有参数requires_grad=False，batch1、no_grad/inference_mode、use_cache=False，不使用generate/采样/温度/新seed。预检tokenizer对**字面Yes和No（add_special_tokens=False）各恰一token且不同**，否则STOP，不临时换多token评分/候选字符串。

在每个完整prompt的最后有效位置读取lm_head logits，`margin=logit(Yes)-logit(No)`，`margin>0`为Yes、tie为No；两logit/margin须finite。是标准限定二选一基线，不称自由生成正确率，不做答案改写、置信度选择、词表搜索或强制互补，不恢复053/054路线。非有限/软件失败是执行未知，不能补成No或悄悄删除。

矩阵3×24×6=**432计划逻辑答案**。REAL32至多144唯一完整输入、CLOCK_BLACK32至多144、TEXT_ONLY至多28，**新root前向上界316**；116文本别名是预期上界情形，实际依完整inputs+模型身份字节去重，不假填实际数。跨条件或旧CLOSED若完整模型输入/同模型图及权重身份完全相同只能精确复用；未决STARTED/身份冲突STOP，不用新父ID重问。074只有分离特征/旧小头、075只CPU；不得重放已闭合历史完整QA输入。

每唯一root输入先STARTED/累计deadline，成功后CLOSED/输出身份，所有逻辑别名显式映射。模型root/visual/decoder/layer hooks分别记actual，不能把316叫全部底层调用；图内部重复子层不等于再问同一逻辑QA，所有计量如实列出。GPU前非阻塞原共享锁/free≥18GiB、最多一次GPU信息命令；忙即GPU_BUSY，不等/轮询/杀其他进程。单次load/所有调用/卸载均计600秒，allocated峰≤16GiB；失败不重载/换精度/batch/删输入重跑。

## 4 评分：55同问反标签观测四格

输出/全部keys/输入与代码seals及GPU Job exit0/actualactive0后，评分角色才读标签（注册角色仅核派生身份；模型角色不读）。单项分母144，视频六问分母24，反向对72，一致完整顺序/恒定答案作描述；所有失败/未知保持计划分母，条件不完整则相关指标NA，不按已完成子集算分。

四格规则先封，评分时从同一固定标签构造：每组q/tau取UTF8较小q为canonical，原24组恰14canonical问题，7组有两类标签。对每个q取全部label1视频×全部label0视频笛卡尔积，按q UTF8再视频固定索引升序；得到**55个观测四格**，每格含两视频各q/tau。无模型输出参与配对/筛样，全部55报告，不按置信度/正确率抽子集。四格全对要求视频证据区分同一问题的相反标签；TEXT_ONLY同q预测恒同，故其四格正确必须0，否则标记实现/绑定泄漏并停止科学判门。

55四格共享24视频及7问题，不是55独立样本、同原视频反事实或已控制背景/未问事件。黑屏仍含真实时钟，REAL超过它才有超出这些非RGB线索的证据；黑屏分布外和32帧漏事件风险仍保留。未认证物理语义/标签真实性不因基础模型成绩而自动成立。

条件表**3行**，完整保留native144/24/72及quartet55的计划/有效/未知/整数正确数/百分比、actualnew/reused/alias、finite/parse/token状态。配对表**2行**：REAL32对CLOCK_BLACK32、REAL32对TEXT_ONLY，在native单项、六问、四格各给两边独对/都对/都错/unknown/net/pp；不跨方法选冠军、不重算原074/075head/不加bootstrap/p值/子层搜索。

仅完整且软件守卫通过时：REAL32的**四格正确数严格大于两个控制**，且144单项正确数均不低于两控制，才记`FULL_MODEL_RGB_EVIDENCE_PILOT_SIGNAL / NEW_MECHANISM_UNCONFIRMED`；否则`NO_SATISFYING_FULL_MODEL_VISUAL_SCREEN / STOP_NEW_ADAPTER_TRAINING_ON_THIS_ENTRY`。这是已见小头结果后、未见本主干结果前设的投入筛查，不是显著性/发表门。失败不宣称主干对所有时间关系无能；通过也不定位连接器或确立新机制。32帧完整主干与旧12帧小头存在预算/接口差异，旧分数只作背景，不当公平新方法胜出。

独立核验不得import生产scorer或重放Qwen/decoder/visual forward，从固定输入/metadata/seals/最后token位置及Yes-No身份、输出/ledger/别名、原标签独立重建432键、3条件/2配对/55四格/守卫/投入门及资源/Job闭合。CPU只读tensor可核REAL/BLACK非pixel一致/32帧完整性，无第二次decoder/媒体decode或旧QA补证。实际/限额/失败阶段/已完成与剩余先持久化，退出闭合自身Job后停止。

## 5 新预算与一次完整交付

| 范围 | 上限 |
|---|---|
| 新研究网络/下载 | 0；只已有074媒体/本地模型，Git文档同步另计 |
| 新媒体逻辑读/准备 | 身份hash≤128MiB一次+decode输入≤128MiB一次；24媒体实际103041283B，不读整个原ZIP |
| 解码/准备采样 | ≤100000实际帧/监督≤900秒，32真实不同索引/224RGB |
| CPU资产/processor/预检 | 累计≤300秒；精确本地模型hash≤12GiB一次，实际成本单列 |
| GPU | 单次冻结load/累计≤600秒/allocated≤16GiB，最多316新完整root前向；GPU Job RAM≤32GiB |
| CPU评分/独立核验 | 累计≤300秒；Qwen/小头重放0 |
| 旧metadata/新prepared输入读 | 旧必要metadata/labels/闭合累计≤32MiB；新RGB/prepared tensor/hash/核验累计≤1GiB，含所有显式读，按共享内容缓存分别实测 |
| 根/起始free/父 | 新独占≤3GiB/2048文件、free≥4GiB、父≤7200秒，从同步前持久起点算 |
| CPU Job/active/线程 | RAM≤8GiB/同时active≤4/线程≤4，所有阶段累计deadlines和实际闭合 |

宿主/物理I/O/周期磁盘监视覆盖范围如实列，不把逻辑读/快照当全面OS访问或硬配额。无36小头state/新训练/优化/新手工标签/媒体剪接/论文/环境改变/付费或外部模型API。原根/失败/锁账本只读，不杀其他进程。预执行完整核验先封，不能等输出后补审再称原全部通过。

精确8处统一交付，成功/部分/阻断均保留完整计划分母：

1. `prototypes/full_model_visual_screen_076.py`
2. 本目录`execution-receipt.md`
3. `admission-summary.json`
4. `scientific-results.md`
5. `condition-summary.csv`（3行）
6. `paired-summary.csv`（2行）
7. `execution-summary.json`
8. `docs/codex-results.md`只尾增一次本父结果

不改075/074/历史代码或结论、规划、本README/论文。不公开原媒体/问题/事件文本/答案/逐项logits预测正确性、四格成员/词表/IDs/hash/私有路径或映射、features/模型权重；只聚合、固定dataset revision与科学代码LF SHA。精确暂存/results历史前缀核对，一次普通安全push main后STOP，无后台/自动077/复活旧小头路线/扩GPU额度或追加训练。

# 独立数据与强对照：负责人当轮直接实施的阶段结果（非新模型实验）

2026-11-04｜ChatGPT负责人直接执行，响应用户“先做这个”。不交Codex、不启动新父任务/GPU。

**裁决：EXTERNAL_TIMEBLIND_IDENTIFIED / CURRENT_062_INPUT_INCOMPATIBLE / OLD_STRONG_CONTROL_RECHECK_COMPLETE / INDEPENDENT_C_D_N_MODEL_EVALUATION_NOT_RUN。科研READY仍0，不能在论文结果中添加新的独立验证分数。**

## 1. 外部基准核验（真实公开资料）

[TimeBlind正式EMNLP 2026论文](https://aclanthology.org/2026.emnlp-main.1923/)、[原作者GitHub](https://github.com/Baiqi-Li/TimeBlind)、[HuggingFace](https://huggingface.co/datasets/BaiqiL/TimeBlind)、[arXiv正式稿及A.11](https://arxiv.org/html/2602.00288v4)均已读取。公开数据600组×4=2400 QA，1200个视频（约3.98GB），300组yes/no与300组AB二选一，官方I_Acc以四格全部正确为主指标，和本项目的四格问答有结构上的可比之处。

**关键资格问题**：[旧062源码](../prototypes/question_role_contrast_062.py)的`tau(q)`只接受`Does the event "A" happen before the event "B"? Answer Yes or No.`严格模板，外部TimeBlind包含状态、属性、因果、事件顺序和AB选择等其他问题类型。在网上可见的官方按序开头30组（indices0..119，顺序样本而非随机/盲抽）中，严格062模板例数**0/30**；该局部计数不代表全600组覆盖率。不能直接把旧已训练C/D小头拿去完整跑TimeBlind并称“公平迁移”；任何改写/新解析规则、筛选或训练都需事前登记且不能按模型得分选择。

首次30组的网页问题/答案在本次公开审查中已可见，其余570组未在本轮逐条查看/训练；这仅是**本轮内容接触记录**，不证明物理来源或预训练独立。论文A.11明确TimeBlind用于诊断评测，不作为训练/微调数据；其中互联网来源视频另保留原许可，不能因托管站点标示Apache2.0就假定媒体全部可随意改编或再分发。因此只能考虑未来经许可核验的冻结模型外部零样本评测，不用该测试集调参。

## 2. 已经重新计算的真实旧强对照（不是新独立数据）

分别对原[063成对CSV](../codex-artifacts/VLM-ROLE-CONTRAST-REPLICATION-063/paired-summary.csv)、[068成对CSV](../codex-artifacts/VLM-FROZEN-TRANSFER-READMISSION-068/paired-summary.csv)、[070成对CSV](../codex-artifacts/VLM-SEMANTIC-ROLE-FACTOR-070/paired-summary.csv)独立逐行重新求和，保留全部6个指定seed，未调参、删负例或重训练。每池300个实例×seed重复测量，并非300独立拍摄。

| 旧数据池 | 公开比较 | 左侧独对 | 右侧独对 | 净正确例（六seed累计） | 左减右均值pp | 正向seed |
|---|---|---:|---:|---:|---:|---:|
| 50Salads | D−C | 46 | 8 | +38 | +12.67 | 6/6 |
| VIDHALLUC | D−C | 36 | 3 | +33 | +11.00 | 6/6 |
| 50Salads | FACTOR−ANCHOR | 49 | 57 | −8 | −2.67 | 2/6 |
| VIDHALLUC | FACTOR−ANCHOR | 51 | 47 | +4 | +1.33 | 2/6 |

后两强对照与原070一致，`FACTOR−ANCHOR`来源条件区间分别[−8.33,3.67]及[−5.67,8.00]pp，两池原全对照门FAIL；这说明后续路由方法不能以胜过旧D来宣称事件语义特异机制。**FACTOR/ANCHOR并非原D/N相同输入头对照，不能把FACTOR失败写作D彻底无效**。旧D无关文本锚N只在种子19/73测过，新六seed没做全套N对照；现有主稿限定贡献仍成立但不能升级。

## 3. 已经实际运行的CPU检查

负责人当轮生成一份纯stdlib `timeblind_control_check.py`，并运行**3项合成unit tests 3/3 PASS**及对2^4=16种二元四格预测的穷举。对官方[1,0,0,1]金标形态，确定性只看问句不看视频（`p(q,v0)=p(q,v1)`）或只看视频忽略问题（`p(q0,v)=p(q1,v)`）都最多2/4单项正确，**0/1实例四格全对**。这是代数性质，不代表新模型已消除所有非时间捷径。脚本只在未来实际提供2400条经过冻结的外部预测时才允许计算新I_Acc，拒绝缺失/重复/不完整序列；本轮没有外部预测和真实C/D模型前向，未产生新准确率。

纯CPU脚本、强对照聚合JSON和完整阶段报告已在本聊天形成可下载ZIP；此GitHub公共文件仅引用审计事实，不假称本地生成的二进制/ZIP已推送GitHub，也不构造假的Codex回执。

## 4. 接下来唯一能改变证据级别的动作

- 必须先有**已经冻结的C/D/N模型及与外部任务兼容的无标签转换规则**，现有062正则无法直接吞入官方TimeBlind原问句。TimeBlind仅用于未触碰测试，不可训练/根据结果调模型。
- 外部视频版权和源重复、原Qwen3-VL 4B主干与旧冻结head可用性、每个臂完全相同输入/解码预算均须证明；未有这些前绝不提供“35%–50%录用概率”的新声称。
- ChatGPT当前会话没有用户私有Windows训练模型、GPU或可用的视频素材；未执行新下载/解码/模型/GPU，也没有授权越过085封存范围。因此**新独立模型性能验证仍NOT_RUN**。以后若用户直接提供合法非敏感的冻结外部模型预测/合格数据元信息，负责人可继续在当前环境计算匹配来源区间与强对照；不为公开文稿操作开Codex任务。

**论文投稿主线照常**：不删除已有正负结果，不新增未测TimeBlind数字或新算法主张。旧083仍PAUSED、084/085 CLOSED。未为本次公开审查开科研任务编号。

## 5. 2026-11-04续：原063文件存在性待完整核验（不读取私有内容）

用户报告先前指出的063原根中`views.pt`与示例`C_NATIVE-137/final.pt`、`D_NATIVE-137/final.pt`“都在”。这**仅是用户口述的三处样本文件存在，不代表已实证核对六seed共12个头或文件内容身份**。负责人已独立编写仅以明确用户本地选定063根为输入的`vlm_063_asset_check.zip`（四项合成测试4/4通过，ZIP英文ASCII文件名）；检查固定12个`training/{C_NATIVE,D_NATIVE}-{137,263,419,557,733,911}/final.pt`及9个结构辅助文件，使用filesystem stat、无目录枚举/媒体/特征/权重内容读取/网络/GPU，并将脱敏`asset_check_report.json`生成在解压工具目录，**ZIP在当前聊天交付用户，未上传GitHub**。`FILESET_PRESENT_CONTENT_UNVERIFIED`即便全部通过，也仅代表文件存在且非零字节，不是模型身份、外部适配、数据授权或独立验证资格。下一步等待用户自主运行并回传脱敏聚合报告；无执行READY，无新GPU/媒体/模型授权。

## 6. 2026-11-04 用户本地063资产回执验收与下一受控核验

用户直接在会话中提供`vlm_063_asset_check_v1`脱敏JSON：`FILESET_PRESENT_CONTENT_UNVERIFIED`；6个C及6个D的`final.pt`均存在且大小非零（**12/12**），包括`views.pt/train-views.pt/feature-index.json/old-assets.json/code-seal.json/input-seal.json/output-seal.json/training-job.json/prediction-job.json`的**9/9**辅助文件亦均非零，固定21条路径，未读取文件内容/GPU/媒体/模型、未递归枚举，报告没有私有路径。接受该**存在性**结论，但不追认模型内容身份、可加载性、外部数据适配或复现效力。

负责人直接依据已经公开的063源码发现：`output-seal.json`应登记12个`final.pt`和`views.pt/input-seal.json`的SHA256，`input-seal.json`应登记`train-views.pt`。据此直接生成英文ASCII名称的`vlm_063_seal_verify_2026_11_04.zip`，包括纯Python3标准库`check_seals.py`、Windows选择文件夹启动器、说明与7项合成单元测试；**7/7 PASS**，ZIP完整性验证通过。脚本仅在用户本人明确选定单一原063根并自主运行时读取**两份封存JSON＋14个固定模型/视图文件**：SHA256流式比对，累计上限96MiB，单张文件≤24MiB、单封存JSON≤2MiB；不载入torch、不解码视频、不访问私有Q/A/标注/特征、不运行模型/GPU/网络、不扫盘。报告仅输出相对文件名的匹配状态、聚合计数/读取预算，**没有私有路径、原始文件内容或哈希值**。一旦缺封存/摘要冲突/越界/预算不符即BLOCKED，不推断内容可用。

**关键许可区别**：上一次用户只授权了文件存在性stat；下一步摘要检查**会实际读取权重和视图文件的内容字节**，只应在用户阅读README并自主执行后发生，不能当作已经执行的私有内容核验。即使12/12 HASH_MATCH，只能证明本地文件与本地历史封存一致，不能证明封存独立可信、TimeBlind题型兼容、源独立或任何新推理许可。ZIP只在本聊天交付；没有通过GitHub二进制接口提交。科研READY保持0、独立新VLM验证依旧NOT_RUN、未建Codex任务。

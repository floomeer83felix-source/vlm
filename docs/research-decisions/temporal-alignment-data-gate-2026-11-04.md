# 时间对齐路线 DATA_GATE：优先复用已有 Perception Test 原视频，先核连续性，不下载新媒体

2026-11-04（北京时间）｜ChatGPT研究负责人｜用户“继续”后的公开官方来源核对与旧公开回执交叉核对。

**结论：DATA_SOURCE_CANDIDATE_FOUND / LOCAL_CONTINUITY_UNVERIFIED / PRIVATE_METADATA_AUDIT_PROPOSED_NOT_AUTHORIZED / NO_REAL_TRAINING / 0_READY。** 这是一份公开研究决定，不是085执行结果、算法成功或自动授权。此前084仍CLOSED、083仍PAUSED。

## 1. 官方数据资格：单独区分公开许可、可获取、已存在与合格实验

| 来源 | 官方证据/当前限制 | 对新问题H的决策 |
|---|---|---|
| **Perception Test** | [DeepMind仓库](https://github.com/google-deepmind/perception_test)提供train/valid/test，含MP4及相应标注；full train视频zip约26.5GB。README软件Apache2.0，其他材料CC BY 4.0；研究中仍需注明出处、保留归属和公开改动说明。 | **首选train-only原型来源**；既有实验已在官方train中处理32个已封存媒体来源，但该事实不证明现存连续原始视频可合法作为L/M/R复原、也不证明物理录制/参与者独立。不得把既有32个已用来源当未触碰独立test。 |
| **TempCloze** | [论文](https://aclanthology.org/2026.findings-emnlp.651/)、[作者HF](https://huggingface.co/datasets/CedPei/TempCloze)：1,521条、7个来源，HF仅test元数据`source,id,gap_start,gap_end`、约126kB；原始视频不随该表全部交付。 | 仅保留为**将来的外部测试候选**。不得以官方test训练并回报同一测试集，不能将metadata当完整媒体，未核七个原来源许可/下载和录制去重。 |
| **Ego4D** | [官方数据网站](https://ego4d-data.org/docs/)说明持有单独license agreement访问条件；适合长连续第一视角录像，访问方式已迁移Lab22。 | **备选训练来源**：既有对话的访问/下载历史不等于当前合法完整媒体、对应身份/用途已核；不得在本阶段下载/读取，后续须单独验证本地资产和用途授权。 |
| **Something-Something v2** | [Qualcomm官方](https://www.qualcomm.com/developer/software/something-something-v-2-dataset)：168,913 train、24,777 valid、27,157 test，研究用途协议；19.4GB VP9视频、许多短的单动作。 | 本目标优先级低：更适合细粒度动作方向性/分类，未证可构成有左右上下文的原连续中段任务；不下载、不把现有类别标签误当中段连续真值。 |

**许可边界**：代码仓库许可证不能自动扩展到所有外部视频；Perception Test README明确媒体/其他材料CC BY，Ego4D须个别协议、SSv2 research use。复用原实验资产应保留原归属和本地许可记录；不得上传视频/标注/逐条来源映射。

## 2. 已有公开资产与新目标之间的关键差距

旧081公开[README](../codex-artifacts/VLM-TIMESTAMPED-TRIPLES-STREAM-081/README.md)、[科学回执](../codex-artifacts/VLM-TIMESTAMPED-TRIPLES-STREAM-081/scientific-results.md)表明：官方Perception Test train内先有32来源20/4/8划分，32份受控media seal已完整、96 RGB块/192六排列、每单元12帧/3秒统一36帧input。该实验证明**过去所用子任务的视频媒体/输入已处理**，但公有GitHub不是私有Windows实验目录的当前库存证明。旧实验中的三片段组合和重排不等于原始长视频的自然左/中/右衔接；旧test8也已被反复查看，不可称盲测。

问题H需要：单个原始**连续视频录制**的左段L、中段M、右段R；每个候选M及干扰项必须先验证真实同源性、连续时间戳和视觉可辨难度。单纯把081合成的三事件排序按位置拆分，会泄漏排列生成规则，不构成同一科学问题。若现有素材只有预裁切3秒单元、缺完整原录制和真实PTS衔接，则 **DATA_GATE_FAIL_FOR_H**，不要使用该数据为H建立准确率结论。

## 3. 唯一建议的下一实际动作：限定只读本地元数据资格审计（需专门批准）

**提出但尚未READY：PROPOSED_LOCAL_ASSET_CONTINUITY_METADATA_AUDIT。**

目标仅是判断已有081受控32来源，是否仍拥有合法原始连续媒体和足够的时间范围以定义L/M/R。允许核对项必须是**本地已有注册seal/manifest和明确已定位媒体条目的文件系统元数据**（存在性、已封存hash、压缩/原尺寸、媒体时长与已封存PTS区间；无时长封存则UNKNOWN）。完全不读取播放/解码帧、源像素、Qwen特征、权重、答案、保护标签或逐条预测。不得从任意根目录搜索资产，不检查无关联私有项目，不打开远端下载源。

允许报告的**仅聚合**表（不暴露源文件名/标记/绝对私有路径）：已登记sources数、可引用完整原媒体数、仅裁切或拼接数、自然连续L/M/R候选数（严格由既有timestamp证据支持）、不足/UNKNOWN数、各自理由及最小资源统计。不能从帧数/三事件排序推断原始自然邻接；原时间戳未存时必须UNKNOWN而非新decode补证。若要计算视频时长必须解码/索引或触及媒体，另有授权前不得做。

提案后续正式合同时必须核：新用户对读取既有私有元数据的明确许可；准确原081私有root由用户/本地执行者已知且在**本地**提供，不写进GitHub；只在一个已定位白名单root下访问seal/manifest；CPU≤60s、读取上限16MiB、文件≤64、无媒体/标签/特征/模型/GPU/网络、输出≤64KiB、单次停止、不得扩搜索；结果为`GO_METADATA_ONLY`、`HOLD_MISSING_METADATA`或`NO_CONTIGUOUS_ORIGINAL_MEDIA`，通过此关也只表示可再审，不代表数据已能训练或论文方法创新。

当前只读公共GitHub不足以证明连续性和本地存在性，不伪造“32个原始视频目前可用”。**用户通用“继续”仅支持公开审查，未授权新的受控私有元数据读取。**

## 4. 后续条件性实验顺序（均未授权）

1. **许可/资产确认通过**：严格自然连续L/M/R的存在性、同录制时间轴、用时间戳验证三个段真实先后；排除来源重用问题。若失败就STOP/HOLD，不下载新媒体尝试救门。
2. **train-only可学习性**：新用户对有限本地特征/模型CPU运算授权后，先用既存合法来源且严格固定的train-only小样本证明普通双侧时序baseline能够正常拟合；同样测试只有静态外观、单侧边界、固定无关有序视频。数值阈值在首次读取真实输入前预登记；未通过不开放dev/test。
3. **方法近邻创新门**：作者正文+代码比对TimeBridge、EventLens等，提出能排除静态/源/排序捷径的非换名算子；无实质差异就不启动新算法训练。
4. **独立新来源检验**：只有3项通过且有独立媒体许可/去重证据，才提出合理预算的新验证。TempCloze是否可做外部test仍为UNKNOWN。

## 5. 直接决策

**最小成本路线：先查已经真实用过的Perception Test train媒体有没有足够的原始连续视频证据，而不是下载TempCloze测试集或重新下载26.5GB全量train**。如果只是已重排的3秒裁切单元，这个数据不能用来声称新任务H的时序理解。论文投稿仍可单独推进，085仍不自动立项。

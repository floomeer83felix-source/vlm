# 自然视频时间信息候选：素材与接口入口筛查

2026-10-24（北京时间）。**PUBLIC_ENTRY_SCREEN_COMPLETE / EXACT_ASSET_REQUIRED / NOT_READY。**
依据：[贡献定义](natural-video-clock-contribution-brief-2026-10-24.md)与[64格最小设计](../research-protocols/natural-video-clock-feasibility-design-2026-10-24.md)。
本轮是负责人公开入口核查，未创建042任务；未取得原视频、执行解码或运行processor/模型。

## 当前裁决

**将EPIC-KITCHENS列为优先进一步确认的公开来源，而不是已通过的实验来源。**
其官方文档同时提供自然VFR说明、原视频获取路径及已有动作区间schema；
但公开fps/duration表不能确认本方案所需6个高偏移录像，也不能认证具体文件与标签的时间桥接。
8源/16题目前仍未齐。

下一项必须是确切素材入口的交接及有界资格核验，不能再用同类综述、扩大文件列表或修改180–900秒条件代替。没有明确资产/新获取范围，就停止继续下发本候选的执行微包。

| 来源 | 本轮确认到什么 | 尚缺什么 | 当前用途 |
|---|---|---|---|
| EPIC-KITCHENS-55/100 | 官方承认低光自动降帧率；有个体视频路径/校验清单、动作起止时间/帧字段、非商用研究发布说明 | 当前原视频实物、实际PTS/偏移、标注所指版本与时钟、源独立性 | 优先入口候选；未准入 |
| HoloAssist | 官方发布CDLA-Permissive2.0说明；目录列VideoMp4Timing.txt与两个MP4变体；有动作区间schema | 所需会话的确切媒体/时间旁表、原版与压缩版对应、实际时钟桥接；未核到小规模独立资产入口 | 后备候选；未准入 |
| TimeLens2-93K | 官方数据卡列视频分片与既有区间，仓库提供真实视频归档入口 | 可按nongold信息定位的小样本成员/PTS索引、媒体版本与标签桥接、当前资产使用范围 | 本轮不选入 |
| AgentNet | 沿用上一轮工具/截图轨迹入口核查 | 本候选需要的原视频、PTS、事件区间桥接未核到 | 保持未准入 |

## 1. EPIC：实际进展与不得替代的条件

固定[EPIC-55官方README](https://github.com/epic-kitchens/epic-kitchens-55-annotations/blob/63fa7d78eba41a8d2280374061a6b1bab3e7e41d/README.md#video-information)说明，低光时GoPro自动降低帧率会使部分录像具有非均匀帧率，并给出已有恒帧率处理建议。因此“自然源可能存在这种时序”已有直接来源证据，不是本项目新发现，也不说明任何特定录像已超过0.25秒门槛。

[EILeV作者README](https://github.com/yukw777/EILEV#errors-for-epic-kitchens-videos)点名P29_05/P30_08的处理经历；这是研究者经验，不能代替实际PTS核验。两者在本轮读取的官方nongold元数据中分别为1821.736567秒、1122.14秒，**均超出已写180–900秒范围**，所以不能将它们直接充作本64格队列的阳性样本，也不为此改变范围或裁剪凑样本。

独立检查[EPIC_100_video_info.csv](https://github.com/epic-kitchens/epic-kitchens-100-annotations/blob/ea8b40457a400c3fffa1c7f406ef3dc169cc2522/EPIC_100_video_info.csv)：
- 700行，video_id唯一，duration/fps数值有效；字段仅video_id、duration、fps、resolution。
- 333行满足180≤duration≤900，涉及36个公开匿名participant ID。参与者数不是独立原录制数，也不是合格VFR数。
- 此表没有逐帧PTS、显示时长、time_base或媒体文件字节身份；不能从平均fps是59.94或50认证CFR/VFR，不能从duration合格推出时钟合格。
- 本轮只读该nongold表及公开split/checksum元数据；没有打开EPIC动作标签CSV、raw QA/gold、帧或视频。README的schema示例未用于选题或评分。

[EPIC-100文档](https://github.com/epic-kitchens/epic-kitchens-100-annotations/blob/ea8b40457a400c3fffa1c7f406ef3dc169cc2522/README.md)分别描述动作起止秒与起止帧。预提取帧的官方勘误还说明帧版本可能与视频分开修订。因此须单独核当前原文件，不把预提取帧、重新编码副本或帧号/fps计算自动等同于媒体显示时钟。

[官方发布页](https://epic-kitchens.github.io/2025)及注释repo标CC-BY-NC4.0；
[Data.Bris存储记录](https://data.bris.ac.uk/data/dataset/2g1n6qdydwa9u22shpxqzp0t8m)另标Non-Commercial Government Licence。
这里按资源范围保留两项声明，未将代码许可或存储标签泛化为任意新下载/用途已获许可。

已跟到当前[下载脚本仓库](https://github.com/epic-kitchens/epic-kitchens-download-scripts/tree/4f11fb2b579833f360c3c7bb917bf1e24a9787b5)及nongold split/MD5清单。原视频可按单个video_id构造发布路径；它解决定位问题，不解决下载授权、当前可达性、大小与实际时钟问题。本轮未运行下载器，未执行其默认批量、重试或环境设置。

## 2. HoloAssist与TimeLens2：资产存在不等于小样本可用

HoloAssist的[官方说明](https://holoassist.github.io/data_links/README.html)列出了按会话组织的原视频、压缩视频和VideoMp4Timing.txt，但该旁表的存在本身不能证明它与某一MP4、区间标注已同钟。零起点的说明紧随整段Narration schema，不能扩大为所有动作标签与每个导出变体均已认证。应使用已有动作区间，不拿整段摘要充作细粒度定位真值。

[官网实际资产入口](https://holoassist.github.io/)指向整包归档：原视频标184.20GB、压缩视频144.62GB、camera信息10.07GB。文本称链接在清单中，但本轮点开的三个入口实际为tar/zip，读取器返回unsupported content-type，没有返回可用归档正文。**不得将这三次访问写成“HTTP请求0”或“归档已经下载/检查”。** 未继续拉取、解压、打开旁表/标签或读取任何帧。只证明公开端点及目录说明已定位，不证明小规模成员和时间桥接已到手。

[TimeLens2官方目录](https://huggingface.co/datasets/MCG-NJU/TimeLens2-93K/tree/main/videos)可见18个tar，多数约106–107GB，末片约888MB；不能笼统说每个分片都超小预算。当前未核到能在不读标签的前提下定位目标小样本的成员/PTS索引，也未取得媒体。数据卡的Apache2.0声明不替代逐来源媒体与当前用途的登记。本轮没有读取JSONL数据行、视频、tar内容或执行索引获取。

## 3. 接口入口的可证范围

[公开Transformers4.57.6处理器](https://github.com/huggingface/transformers/blob/v4.57.6/src/transformers/models/qwen3_vl/processing_qwen3_vl.py)中，_calculate_timestamps的签名及其原生格式调用点已定位。隔离适配可在该计算入口映射索引至PTS；这仅是实现路径已识别，**不是CPU动态分派、实际timecode或BF16视觉相等门已通过**。
不能因此读取本地权重、修改安装库、伪造frames_indices或手工编辑input_ids。P仍是透明诊断适配，N仍须作为完整计费的现有方法参照。

## 4. 下一输入交接应包含什么

只需明确以下资产引用，完整私人路径留在本地；公开仓库仅存脱敏清单。
1. 原视频的确切本地文件引用，或另行批准的逐文件获取清单；不能给一个盘符后要求自动搜索。
2. 与这些原文件对应的已有区间标注及nongold事件文本入口；原始评分端点保持独立，不提前用gold挑题。
3. 发布版本、原录制关系与现有时钟/帧映射说明；没有说明的条目如实UNKNOWN。

收到明确引用后，才写成一次整包CPU素材资格合同；任何媒体/解码/标签内容访问和拟预算都须重新列明。若没有可提供的资产，也不批准新的有限获取范围，则**暂停这条候选的入口推进**，保留设计而不继续派整理文件/搜路径/扩大综述任务。这是执行条件未满足，不是实验阴性或科研命题被证伪。

当前0 READY，042未立项；本轮不创建Codex父结果、实验根、代码或tests。040/041关闭，原C/D及038–039停止、144格选帧候选/路径交接PARKED、NOVELTY=RETAIN0、NATURAL_VIDEO_EFFECT_UNKNOWN及媒体/训练限制全部保持。

## 公共文件身份

| 文件 | Git blob |
|---|---|
| EPIC55 README | f5d84c7447aa6852549ad11451fba746b98ada8b |
| EPIC100 README | b6cd0f56c744a09589affa280fdb7f7f0385cbcc |
| EPIC100 video_info | be226d778c0c80dd68cddc041fac9f6761949cd2 |
| EPIC100 license.txt | 03889f6757f0b56e5194d4bfcb57dcb66a7abd41 |
| 下载器README / source | 2920da618308a514e26c8c5c978d57a7342ebdf0 / 442123c9a49fa6a839fed520d4bc62443ab98ad3 |
| 下载器split / MD5元数据 | 10563a493bb97f4d173876bf8fb9e04c83faf1fb / 5bfdf8891aa1b52e28a19bc26500504bbb332dd5 |
| HoloAssist release README | a5792032de4d8620205043b290fca01226072890 |

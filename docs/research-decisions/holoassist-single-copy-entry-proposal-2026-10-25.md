# 046新实物入口提案：HoloAssist单个分发副本

2026-10-25（北京时间）。**PROPOSAL_COMPLETE / MEDIA_APPROVAL_REQUIRED / 0 READY。**
用户在045验收后要求“继续下一步工作啊”。负责人已核远端c7eb259、AGENTS及任务/结果/总览，
继续解决确切真实输入缺口，未重开已停止的EPIC直接入口或再发纯受控扩展任务。

## 1. 具体新对象

[046完整合同](../codex-artifacts/VLM-HOLOASSIST-REAL-INPUT-046/README.md)绑定HoloAssist
R015-7July-Switch在lmms-lab/EgoIT-99K的公开分发文件。
[发布者commit dabc7958c501ce7cb7a0e6082e41ffdee547a1b7](https://huggingface.co/datasets/lmms-lab/EgoIT-99K/commit/dabc7958c501ce7cb7a0e6082e41ffdee547a1b7)
明确LFS大小114523050B和SHA256
8ee70b404c996a1c823b65744debc9763564ac6bb5e57835f15be8c07d3bac98；
[文件页](https://huggingface.co/datasets/lmms-lab/EgoIT-99K/blob/main/HoloAssist/video/R015-7July-Switch.mp4)
与三行Raw pointer核对相符。执行必须用完整commit resolve URL，不能跟main变动。
这是不同数据集/分发主机的确切单文件，约109.22MiB，不是EPIC C01/C02镜像、续传或换候选。

[EgoLife/EgoGPT发布者说明](https://github.com/EvolvingLMMs-Lab/EgoLife/blob/7a97157908757cc898c26835b718653055ecc5f5/EgoGPT/README.md)
链接其EgoIT公开视频数据；该README blob56d78d87b6989b12eb7056ffa04572b22485d2ee。
不执行其整库snapshot_download、训练、环境安装或模型指令。
[HoloAssist上游README](https://github.com/Ember-HoloAssist/holoassist-release/blob/f53ad2b5c3889784ef068e11fea10ba4ecf99970/README.md)
bloba5792032de4d8620205043b290fca01226072890明确数据按
[CDLA-Permissive-2.0](https://cdla.dev/permissive-2-0/)发布，列出pitchshift/compress视频和时间文件。
该上游许可依据与分发版本出处分别登记；不把EgoGPT代码的Apache许可移给视频。

## 2. 未认证事项与被否决的小样例

该分发文件是否保持上游完整原视频、是否转码/改速、实际T/PTS与已有标签时钟均UNKNOWN。
有LFS摘要只能核分发版本完整性，不能证明与原发布同字节或标注桥接。
EgoSteer作者[自身数据重建说明](https://huggingface.co/datasets/EgoSteer/EgoSteer-Egocentric/blob/main/README.md)
描述其HoloAssist源帧映射为27.5–30fps可变时序；这只说明验钟有针对性，
不能代替H01的实测，也不是本项目发现VFR或获得创新性的证据。

另外查得pyxploiter/HoloAssistViewer一个33,239,988B样例，
路径R007-7July-DSLR/Export_py/Video_pitchshift.mp4，Git blob1d6e503068cd79b63e4fa43b55c50188c3a3b6cd。
仅其[38B时间元数据](https://github.com/pyxploiter/HoloAssistViewer/blob/7c1a5eb98c832880382421afb1606d47586242d2/data/videos/R007-7July-DSLR/Export_py/Video/VideoMp4Timing.txt)
两项之差按.NET ticks解释约111.296秒；该单位未在本轮独立实物核验，
因未能证明满足180秒门，**不选入、不下载、不放宽时长**。
其标注JSON仅看到文件树元信息，未打开正文。
H01也没有已核时长，必须完整获取后按原180–900秒门判定；不保证成功、不换源补数。

传输接口另核[HF官方当前下载说明](https://huggingface.co/docs/hub/datasets-downloading)的精确HTTPS主机表，
及官方huggingface_hub constants blobec04a7599a8796b5b694e6a83abcb1ce5ce3b038中X-Linked-Size/ETag字段。
manifest只准当前列出的主机及官方员工已说明的历史cas-bridge入口；不使用任意域名后缀或动态加白名单。
这不是主张服务器一定按该路线成功；未接触媒体HTTP，缺头/新跳转即失败。
不使用其SDK默认重试/缓存下载、分块协议或网络配置修改。

本轮只检索公开说明、代码/目录元信息、版本/LFS pointer及上述时间元数据；
没有获取媒体正文、运行decoder/processor/模型或访问Windows/旧私有目录。
部分网页/指针地址初次读取失败，不能写“HTTP请求0”或“全部源已验证可下载”。
HF数据卡页面自动附带其它子集的训练样例预览，本轮未主动取标注文件、不使用或转录这些样例，
不据其选择H01、问题或评分规则；未取得任何本研究合格题目。

## 3. 合并后的实质任务与授权边界

046提案一包包括必要真实传输集成预检、一次固定文件获取、实际显示时钟，
以及条件满足后的真实F/T P适配和强N输入。无需再发纯假传输或找路径微包。
新媒体上限128MiB；获取840/870/900秒；CPU累计1800秒；Job4GiB/4线程；
最多两遍解码，processor≤5次、正式B0/P/N各一次；父5400秒。
CFR/OTHER/时长或时钟未知均如实停止该副本的后续输入比较，不调整门槛凑高漂移。

**本轮先冻结完整提案，当前0 READY，未授权本地执行。**
AGENTS明确要求“Restricted GPU/model operations, data download ... still require explicit authorization.”
这次是新的HoloAssist媒体与CPU解码，042/044已消费许可不能继承。
用户批准本已冻结范围后，只需登记一次授权并设唯一READY，不再对子步骤反复确认。
模型/GPU、标签/QA、其它媒体和旧资产访问均不在批准范围。
即使CPU输入门通过，也不能自动宣布原片科学资格、6+2/64格或模型收益成立。
045和044关闭保持，NOVELTY=RETAIN0，NATURAL_VIDEO_EFFECT_UNKNOWN。

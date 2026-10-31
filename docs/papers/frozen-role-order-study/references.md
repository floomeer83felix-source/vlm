# 文献核实与使用范围

编号与正文一致。以本任务已核文献简表为起点，2026-10-31只读一手摘要或书目信息：共12次页面打开请求、8个不同入口；没有PDF、数据下载或模型调用。下列前七条本轮返回一手页面，第八条CVF返回403，沿用负责人简表中的已核书目，不声称本轮重新核实全文。未使用外部公开成绩作不等协议数值比较；所有条目均为背景，均未在本项目按原方法复现为对照。

<a id="r1"></a>
## [1] 冻结模型来源

Shuai Bai, Yuxuan Cai, Ruizhe Chen, et al. **Qwen3-VL Technical Report**. arXiv预印本，2025，2511.21631。[一手页面](https://arxiv.org/abs/2511.21631)。

本轮核实题目、作者及预印本身份。支持模型家族与架构背景；本文具体12帧、merger及末位置特征的依据为项目实现记录，不由技术报告的总体能力推断。未对模型报告中的基准作本地复现。

<a id="r2"></a>
## [2] DyBench与反事实监督背景

Dazhao Du, Jian Liu, Jialong Qin, et al. **Learning Spatiotemporal Sensitivity in Video LLMs via Counterfactual Reinforcement Learning**. arXiv预印本，2026，2605.21988v2。[一手页面](https://arxiv.org/abs/2605.21988v2)。

本轮核实书目及摘要中的CRPO、DyBench背景。支持时空变化敏感性和反事实视频监督已有研究；不声称重新核验附录的逐样本构造。本项目发布者QA层的使用依据另见060记录。没有运行CRPO，也不作同协议性能比较。

<a id="r3"></a>
## [3] 时间信息流诊断

Peitao Han, Fei Cheng, Lis K. Pereira, Qianying Liu, Shigeru Kitazawa. **Tracing the Arrow of Time: Diagnosing Temporal Information Flow in Video-LLMs**. arXiv预印本，2026，2605.07568。[一手页面](https://arxiv.org/abs/2605.07568)。

本轮核实题目、作者与摘要范围。支持编码器至语言模型的时间信息传递已有诊断工作；播放方向任务不等同动作片段次序交换。没有运行TIMEFLOW或层间分析，不能以本文小头结果定位相同模块。

<a id="r4"></a>
## [4] 互补问题与视频配对

Baiqi Li, Kangyi Zhao, Ce Zhang, Chancharik Mitra, Jean de Dieu Nyandwi, Gedas Bertasius. **TimeBlind: A Spatio-Temporal Compositionality Benchmark for Video LLMs**. EMNLP，2026。[ACL一手页面](https://aclanthology.org/2026.emnlp-main.1923/)。

本轮核实书目与摘要。支持最小视频对、互补问题和组合能力诊断的先例。TimeBlind在本项目未运行；不能称本稿有第二个独立外部基准，不能引用其分数充作本地实验。

<a id="r5"></a>
## [5] 文本表示的组合信息

Amita Kamath, Jack Hessel, Kai-Wei Chang. **Text encoders bottleneck compositionality in contrastive vision-language models**. EMNLP，2023，4933–4944。[ACL一手页面](https://aclanthology.org/2023.emnlp-main.301/)。

本轮核实作者、题目、会议与页码。支持对比式模型文本向量的组合信息可恢复性研究背景；不能直接套用到Qwen纯文本末位置hidden，或声称同一因果瓶颈已被本文证明。

<a id="r6"></a>
## [6] 等变与不变视频问答

Yicong Li, Xiang Wang, Junbin Xiao, Tat-Seng Chua. **Equivariant and Invariant Grounding for Video Question Answering**. arXiv预印本，2022，2207.12783。[一手页面](https://arxiv.org/abs/2207.12783)。

本轮核实题目、作者与摘要；按预印本形式引用，不额外补写未核会议页码或DOI。支持问题关键变化与无关变化的敏感性原则已有先例；未运行EIGV，不能将差分操作本身申报原创。

<a id="r7"></a>
## [7] 随机运行的分布报告

Nils Reimers, Iryna Gurevych. **Reporting Score Distributions Makes a Difference: Performance Study of LSTM-networks for Sequence Tagging**. EMNLP，2017，338–348。[ACL一手页面](https://aclanthology.org/D17-1035/)。

本轮核实作者、题目、会议及页码。支持报告多随机运行分布的动机；该序列标注研究不能为本文视频任务的显著性、种子数量充分性或来源独立性提供直接认证。

<a id="r8"></a>
## [8] 组合式成组评估

Tristan Thrush, Ryan Jiang, Max Bartolo, Amanpreet Singh, Adina Williams, Douwe Kiela, Candace Ross. **Winoground: Probing Vision and Language Models for Visio-Linguistic Compositionality**. CVPR，2022，5238–5248。[CVF一手入口](https://openaccess.thecvf.com/content/CVPR2022/html/Thrush_Winoground_Probing_Vision_and_Language_Models_for_Visio-Linguistic_Compositionality_CVPR_2022_paper.html)。

本轮入口返回403，书目沿用本任务reference-brief的负责人已核材料，不宣称重新读取论文。仅用于成组视觉语言组合评估已有先例这一窄背景；没有运行Winoground，不能将四格全对指标归为本项目原创。

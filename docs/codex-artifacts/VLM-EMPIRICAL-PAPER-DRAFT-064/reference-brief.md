# 064一手文献核实简表

2026-10-31｜ChatGPT研究负责人在线核对论文作者页/arXiv、ACL Anthology、CVF页面。以下是写作输入，不是本项目已运行的对照；不用外部结果数字作同协议比较。摘要层核对只支持列出的窄范围，不能据此写未读正文的细节或宣称查新穷尽。原始DyBench数据/许可边界仍以055/060记录为准。

| 键 | 已核作者、题目、年/来源 | 一手入口 | 可支持的相关工作位置及限制 |
|---|---|---|---|
| QWEN | Shuai Bai, Yuxuan Cai, Ruizhe Chen, et al. Qwen3-VL Technical Report. 2025, arXiv:2511.21631 | https://arxiv.org/abs/2511.21631 | 冻结基础模型来源；本项目特征接口/抽帧细节来自060实际实现，不把报告泛论替代实际接口 |
| CRPO | Dazhao Du, Jian Liu, Jialong Qin, et al. Learning Spatiotemporal Sensitivity in Video LLMs via Counterfactual Reinforcement Learning. 2026, arXiv:2605.21988v2 | https://arxiv.org/abs/2605.21988v2 | DyBench/反事实变化与不变监督已有先例；本项目未复现CRPO，不称首次反事实时间学习 |
| TIMEFLOW | Peitao Han, Fei Cheng, Lis K. Pereira, Qianying Liu, Shigeru Kitazawa. Tracing the Arrow of Time: Diagnosing Temporal Information Flow in Video-LLMs. 2026, arXiv:2605.07568 | https://arxiv.org/abs/2605.07568 | 编码器/投影器/LLM的时间信息传递已有研究；其AoT任务与本项目事件片段交换判断不同，本项目未查明同一层因果瓶颈 |
| TIMEBLIND | Baiqi Li, Kangyi Zhao, Ce Zhang, Chancharik Mitra, Jean De Dieu Nyandwi, Gedas Bertasius. TimeBlind: A Spatio-Temporal Compositionality Benchmark for Video LLMs. EMNLP 2026 | https://aclanthology.org/2026.emnlp-main.1923/ | 配对视频/互补问题诊断已有先例；本项目TimeBlind模型评估NOT_RUN，不称已跨基准验证。页面页码43801–43822与DOI可自行按原页核对，不必为填格式引入未经再次核对的项 |
| TEXT | Amita Kamath, Jack Hessel, Kai-Wei Chang. Text encoders bottleneck compositionality in contrastive vision-language models. EMNLP 2023:4933–4944 | https://aclanthology.org/2023.emnlp-main.301/ | 组合信息的文本侧可恢复性已有研究；对象为contrastive VL/CLIP，不能直接推定Qwen纯文本hidden的同一缺陷或本项目层级成因 |
| EIGV | Yicong Li, Xiang Wang, Junbin Xiao, Tat-Seng Chua. Equivariant and Invariant Grounding for Video Question Answering. 2022, arXiv:2207.12783 | https://arxiv.org/abs/2207.12783 | 问题关键变化等变/无关变化不变已有先例；本次按arXiv引，不仅凭二手检索填会议/DOI，不称此原则原创 |
| SEEDS | Nils Reimers, Iryna Gurevych. Reporting Score Distributions Makes a Difference: Performance Study of LSTM-networks for Sequence Tagging. EMNLP 2017:338–348 | https://aclanthology.org/D17-1035/ | 多次随机运行/分布报告的重要性已有研究；原任务为序列标注，不借其p值认证本项目六seed |
| WINO | Tristan Thrush, Ryan Jiang, Max Bartolo, Amanpreet Singh, Adina Williams, Douwe Kiela, Candace Ross. Winoground: Probing Vision and Language Models for Visio-Linguistic Compositionality. CVPR 2022:5238–5248 | https://openaccess.thecvf.com/content/CVPR2022/html/Thrush_Winoground_Probing_Vision_and_Language_Models_for_Visio-Linguistic_Compositionality_CVPR_2022_paper.html | 双图双句组合诊断已有先例；不是本项目视频训练基线，不将组指标本身当新贡献 |

DyBench发布入口：https://huggingface.co/datasets/ddz16/DyBench 。本项目固定revision与自建划分来自060，不用当前main替代旧版本；不因名称/文件SHA不同而认定与TimeBlind物理独立。正文按需要选用上述8项及数据入口，不为凑数量编造文献。引用号由最终正文决定，必须与references.md一一对应。中英文题名、作者、会议、年份按上述官方来源核对；未核的卷期/DOI宁缺勿编。

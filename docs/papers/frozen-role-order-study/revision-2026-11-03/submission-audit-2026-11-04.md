# 投稿版三方面修订与待办核查（2026-11-04）

**主审稿**：[manuscript-submission-review-2026-11-04.md](./manuscript-submission-review-2026-11-04.md)。
**独立实验协议**：[independent-validation-preregistration-2026-11-04.md](./independent-validation-preregistration-2026-11-04.md)。

本次只用公开GitHub稿件、既存聚合数据和正式出版机构的公开文献核对；**没有新训练、推理、视频读写、标签、单项预测或新的统计重采样**。原2026-11-03 Markdown、Word/PDF、原结果/图表和build脚本均不覆盖；本次主审稿和附录供后续作者/导师审阅，**不是已经套好正式模板的投稿docx/PDF**。

## A. 摘要、格式与参考文献

目标候选期刊：[《安阳工学院学报》官方投稿指南](https://xbbjb.ayit.edu.cn/info/1006/1367.htm)，[期刊新采编系统](https://ayxb.cbpt.cnki.net/portal)，[投稿模板入口](https://ayxb.cbpt.cnki.net/portal/journal/portal/client/news/ayxb_011127bd-74c1-48b3-bed7-30349045a7d4)。官方机构指南要求：
- 中文题目一般≤20字；自然科学摘要包含目的、方法、结果、结论，中文200—300字为宜，英文与中文意义对应，关键词3—8个；不夸大“首次”与原创性。
- 正文宜采用0引言、1相关工作等数码标题；图表按出现顺序编号、正文先引，Word表格可编辑；公式建议原生Word公式。
- **至少10篇正式发表的文献**，GB/T 7714—2015顺序编码；未正式发表的预印本不列为正式参考文献，需有真实论文页码范围。
- 真实作者及机构（含省市邮编）、中图分类号、简介和基金如实填报；不能凭项目聊天假定作者身份或伪造基金。尚缺作者、单位、通讯、分类号核定与用户确认的原始研究伦理/数据使用陈述。
- 2026-05-07启用新版采编系统；在官方模板确认后以*.docx提交，不使用非官方链接。**投稿前需下载期刊当期模板、由作者在Word中逐项套用并目视校对**；当前稿不是排版终稿。
- 旧CNKI页面与机构最新版文字在摘要限字和引言标题上存在版本差异；本修订优先采用可见的院校编辑部2024页面的200—300字、0引言要求，提交前以下载的最新版模板为准。

已做：
1. 新标题缩短为`冻结特征视频问答中的角色差分效应`，不再暗示创造新算法；增加中英标题与双语摘要并明确四层信息。
2. 摘要保持已封存两池各50实例、六指定seed、C→D四格5.00→17.67%与1.33→12.33%、验证−1.52pp、原事前门失败，未删除负结果；英文摘要覆盖对应结论而非宣传改进主干。
3. 将原稿含纯arXiv预印本的8篇参考文献改为**11篇可以查到正式会议/出版记录的论文**，按正文首次出现重新编号；2026 CRPO及Tracing the Arrow of Time、Qwen3-VL技术预印本**未列为正式文献**。Qwen模型身份只通过发布者模型卡链接核对，不将网页冒充出版论文。
4. 引入与主张直接相关的已发表强近邻：VideoComp、Invariant Grounding、Counterfactual VQA、TOGA、NExT-QA/NExT-GQA、TimeBridge等，不把“只要算子写法不同”作为新方法贡献。

### 11篇正式文献一手出版入口

| [序号] | 正式发表来源及页码 | 一手查证入口 |
|---|---|---|
| [1] | EMNLP 2026:43801–43822 | https://aclanthology.org/2026.emnlp-main.1923/ |
| [2] | CVPR 2022:5238–5248 | https://openaccess.thecvf.com/content/CVPR2022/html/Thrush_Winoground_Probing_Vision_and_Language_Models_for_Visio-Linguistic_Compositionality_CVPR_2022_paper.html |
| [3] | CVPR 2025:29060–29070 | https://openaccess.thecvf.com/content/CVPR2025/html/Kim_VideoComp_Advancing_Fine-Grained_Compositional_and_Temporal_Alignment_in_Video-Text_Models_CVPR_2025_paper.html |
| [4] | CVPR 2022:2928–2937 | https://openaccess.thecvf.com/content/CVPR2022/html/Li_Invariant_Grounding_for_Video_Question_Answering_CVPR_2022_paper.html |
| [5] | CVPR 2021:12700–12710 | https://openaccess.thecvf.com/content/CVPR2021/html/Niu_Counterfactual_VQA_A_Cause-Effect_Look_at_Language_Bias_CVPR_2021_paper.html |
| [6] | ICCV 2025:23593–23603 | https://openaccess.thecvf.com/content/ICCV2025/html/Gupta_TOGA_Temporally_Grounded_Open-Ended_Video_QA_with_Weak_Supervision_ICCV_2025_paper.html |
| [7] | EMNLP 2023:4933–4944 | https://aclanthology.org/2023.emnlp-main.301/ |
| [8] | CVPR 2021:9777–9786 | https://openaccess.thecvf.com/content/CVPR2021/html/Xiao_NExT-QA_Next_Phase_of_Question-Answering_to_Explaining_Temporal_Actions_CVPR_2021_paper.html |
| [9] | CVPR 2024:13204–13214 | https://openaccess.thecvf.com/content/CVPR2024/html/Xiao_Can_I_Trust_Your_Answer_Visually_Grounded_Video_Question_Answering_CVPR_2024_paper.html |
| [10] | CVPR 2026:39647–39658 | https://openaccess.thecvf.com/content/CVPR2026/html/Wang_TimeBridge_Self-Supervised_Video_Representation_Learning_via_Start-End_Joint_Embedding_and_CVPR_2026_paper.html |
| [11] | EMNLP 2017:338–348 | https://aclanthology.org/D17-1035/ |

期刊最终对GB/T 7714中会议主办地、出版机构、标点、大小写、页码符号有自己的模板细节；本次标准化为**可核题录草稿**，正式投稿前应以版式校样逐条复核，而非声称通过编辑部格式预检。

## B. 科学论证及复现透明度

| 风险 | 本次修订 | 仍需作者确认 |
|---|---|---|
| D收益可能被包装成原创算法 | 明确定位为问题输入视图的有限实证观察；删除“提出新机制”暗示 | 标题、摘要和贡献是否满足目标栏目的学术性 |
| 验证−1.52pp、development seed733负差 | 摘要、表1与讨论一并保留 | 与源数据表重新核对全部分母/表图 |
| 六seed重复/数据多次使用 | 写明不能当6倍独立来源；两条条件bootstrap轴不能合并成独立泛化区间 | 来源family和真实拍摄/参与者独立性是否有更高质量证据 |
| 无关锚只两seed、顺序HASH保留部分时序 | 将强对照范围明确为有限 | 不把历史未执行条件写成完整消融 |
| 现有代码+聚合可复核但媒体/特征等未公开 | 将复现等级界定为“部分可复核”；保留封存代码指向和计算规则 | 原始实验材料及数据许可披露边界，伦理与个人信息审查 |
| 081普通头train约50%、085时间戳缺失 | 只作为不同构造的后续限制，不与主C/D结果合并排名 | 是否在正文简化篇幅；不可称“模型总体不可学” |

需要自动化核对旧`tables.json`不变：train68、validation11、development54、50Salads50、VIDHALLUC50；原六seed`137,263,419,557,733,911`；50Salads C`[3,6,1,1,2,2]` D`[10,10,10,6,8,9]`；VIDHALLUC C`[1,0,0,0,1,2]` D`[8,7,6,2,7,7]`。这些在新主稿与旧稿没有重新运行或修改。

## C. 额外独立数据验证与强对照

见[单独预注册设计](./independent-validation-preregistration-2026-11-04.md)：以同任务C/D四格验证为对象（不是另造085的L/M/R补段成绩），设置数据许可与原录制来源独立的DATA_GATE；train-only ordinary C拟合门；C/D/N/强时间基线/纯文本/固定视频/时间破坏/真实完整Qwen成本分离；来源级配对效应与事前阈值；一次盲测及失败即停。

**现状：NOT_RUN / NOT_AUTHORIZED。** 新独立来源未取得资格证明、没有新增原始结果、没有任何新 GPU 或受限数据授权，故**不能把这一段写作已证实第三档实验，也不能沿用先前主观“35%–50%接收”情景描述来保证稿件。**

## 投稿前最终判据（待人完成）

- [ ] 真实作者署名顺序、完整单位、邮编、作者简介与通讯作者已确认；基金有则据实填，无则按期刊规则处理。
- [ ] 中图分类号经正规分类工具核实，未使用猜测值。
- [ ] 从官方最新模板生成并目视核对完整Word，中文/英文题名摘要、目录标题、公式、两图两表、可编辑三线表、页眉页码等无缺损。
- [ ] 原发表数据使用权限、引用归属、媒体/个人信息与作者贡献声明经导师核实。
- [ ] 文献11篇逐一核版式；Qwen/DyBench资源身份不被误填成已正式出版论文。
- [ ] 用原封存公开表再次核算两表和两图（不调用模型、不重算统计区间）；核新稿与旧`tables.json`完全对应。
- [ ] 导师审核“弱创新、验证负差、开发已用数据、来源独立未知、未跑TimeBlind”的结论边界。
- [ ] 若无新增独立数据结果，摘要和结论仍维持受限实证稿，不改为“强泛化新算法”。
- [ ] 作者最终决定目标刊物、合法投稿账户和是否投稿；不一稿多投。

当前任务结论：**文字与文献层已形成可审阅修订稿；投稿Word与真实独立数据验证尚未完成**。不通过编辑部模板QA，不称已经正式投稿。

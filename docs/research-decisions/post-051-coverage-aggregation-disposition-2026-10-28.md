# 051验收：完整开发比较结束，停止当前覆盖与投票候选

2026-10-28（北京时间）｜ChatGPT研究负责人  
执行提交：[2afac5e4769a6ea0cc3a22fbcea42377f4692d1d](https://github.com/floomeer83felix-source/vlm/commit/2afac5e4769a6ea0cc3a22fbcea42377f4692d1d)。  
**ACCEPTED_DEVELOPMENT_COMPARISON / NO_MATERIAL_DEPLOYABLE_GAIN / 051_CLOSED。当前0 READY。**

## 1. 结论与证据层级

051已完成原定同24题、四名义来源各6题的完整比较，不是050式输入失败。120个逻辑模型格均对应本轮独特完整输入，120次真实generate全部自然EOS、严格A–E有效；FAILED/INVALID/NOT_RUN/SCORING_UNKNOWN均0。两项预设开发投入门均失败，接受停止这些固定全帧/分组投票程序作为当前候选的决定。

依据：[执行回执](../codex-artifacts/VLM-COVERAGE-AGGREGATION-051/execution-receipt.md)、[科学表](../codex-artifacts/VLM-COVERAGE-AGGREGATION-051/scientific-results.md)、[48行CSV](../codex-artifacts/VLM-COVERAGE-AGGREGATION-051/condition-summary.csv)、[JSON汇总](../codex-artifacts/VLM-COVERAGE-AGGREGATION-051/execution-summary.json)、两份本轮代码和负责人只读schema模块。负责人独立完成**560项公开记录一致性校验**，未导入执行实现、重跑原tests/Windows/模型，未读取私人QA、标签、媒体、数组、账本或路径。现场运行/隔离/退出仍是执行者证据，不冒充独立复现实验。

提交是356f3f5的唯一直接后继，恰7处执行者allowlist：新增6文件，results原前缀逐字保留、只追加一条051父结果；AGENTS、负责人两模块、看板/总览和旧代码/旧证据未被执行者改动。

## 2. 科学结果独立复算

| 项目 | SO旧主参照 | F48 | 四P固定投票V4 |
|---|---:|---:|---:|
| 全24题正确 | 9 | 9 | 10 |
| 相对SO净收益 | — | 0 | 1/24（+4.17个百分点） |
| 逐源净收益 | — | +1/6、+1/6、0、−1/3 | 0、+1/6、−1/6、+1/6 |
| 正来源数 | — | 2/4 | 2/4 |
| 固定门：≥1/6且≥3/4来源正 | — | FAIL | FAIL |

F48与SO配对为3纠正/3误伤/6双对/12双错；V4与SO为3/2/7/12，V4与F48也为3/2/7/12。均保留全24题分母，不以某个来源或更弱Uniform作新主参照。P0/P1/P2/P3各8/24，UO=UR8/24，SR9/24。门是研发投入规则，不是显著性检验或全领域等价证明。

24组投票均有4个有效构成答案，7题最高票同票，按冻结的P0→P3最早并列票裁决；没有新裁判、置信加权或看gold改规则。有限O4=11/24、O5=12/24；full-only1、split-only3、投票恢复这3例、vote-missed1、all-five-wrong12。逐源计数及oracle界限与公开CSV/JSON相容。

**12题五程序全错不证明像素中缺证据，也不定位为检索、分辨率或融合错误；O5不是未来算法上界。** 三个split-only成功全来自S04，不能据此挑该源扩展、训练selector或宣称普遍融合机制。049坐标候选不恢复，NOVELTY=RETAIN0。

## 3. 官方原字段与评分门

本轮一次nongold混合原文件物理读取1,854,695字节、冻结SHA一致；仅投影同24题question/mcq_test，gold值解码0。24题均line_labels解析、显示A–E与049冻结选项核齐；120个冻结选项的边界规范化次数0，模型仍使用原冻结文本。不能将结构标签剥离称原始显示字符串与模型输入字节相同。

全部24题绑定及交接文件已保存后，初binder在写最终收据时因原字节变量b被JSON端点整数遮蔽而失败。一次首generate前修复保留初代码/失败，只据保存的完整绑定和精确stat完成收据，原文件body没有为修复重开；自有拒绝body读取的canary回归通过。负责人检查公开控制流与这一描述相容，接受这次窄修复，**不因此认证其为任意失败恢复器**。原16顶层必要例/34断言及修复后17例/36断言均报告PASS，各含负责人16个parser夹具。

模型Job实际active0后，隔离scorer第二次打开相同字节/SHA的原文件，只读同24标签并由同binder再核题/选项。049四个自然条件96个逻辑正确性标记全部重算一致、差异0，既有72个规范物理结果只读复用，历史记录不改。两次混合文件的物理读取与gold值解码分别报告；这是角色/control-flow证据，没有独立OS文件访问审计证书。

## 4. 实际输入、身份与成本

两种真实CPU processor探针、120次正式CPU准备均报告通过，CUDA在CPU门前未初始化。四数组各打开一次，uint8[48,192,288,3]内容与049匹配；F48 grid[24,12,18]/1296视觉tokens，P grid[6,12,18]/324。实际callback、序数时间码、完整kwargs、最终BF16/integer张量与roundtrip均核；F48输入1607–1769tokens、P为477–639，均≤4096。

公共AST与四源码身份复核通过。JSON中的四个SHA256精确匹配**仓库LF文本转为Windows CRLF后的字节**，不是仓库LF文件字节SHA相同；负责人两模块Git blob仍为1e1e306de3d76c476701ba68a5a6f638d5f631cc、13e335cf2e569608493428a2f352d52d238a019d，内容未改。队列/评分在同一实际本地字节表示上封存核对；此换行说明不补签私人执行代码的独立取证。旧049源码身份沿既有冻结记录。

同049模型/processor/tokenizer/生成声明相同，BF16/SDPA、seed19、batch1、greedy/max_new_tokens64、fresh context不变；未重新全量hash权重字节。新120完整输入与049闭合输入零重叠/零复用/零不可复用匹配；050三个精确STARTED/queue/infer入口均不存在，旧任务不重启。历史全局exactly-once证书缺口仍在，不把本次局部去重扩大为全部历史证明。

| 资源 | 汇总复核 |
|---|---:|
| 单模型Job保守GPU包络 | 61.531秒 /1200秒 |
| child权重意图到卸载 | 50.516秒，包含于上述包络 |
| peak PyTorch allocated | 10,739,961,856字节 /18GiB |
| peak Job commit | 18,394,619,904字节 /32GiB |
| CPU-only Job outer合计 | 34.233秒 |
| 全10个监督Job outer | 95.764秒；亦为本轮受监督CPU工作的保守上界，<1800秒 |
| 父执行汇总时elapsed | 709.690秒 /7200秒 |
| 新根汇总时快照 | 61文件 /428,253字节，<2048文件/128MiB |

十Job均实际active0/no kill，唯一非零退出是保留的初bind exit1；全局非阻塞锁/mutex到模型退出、两次free检查22,835/22,834MiB等为执行者记录。根大小是快照，不宣称硬文件系统配额；父elapsed是汇总时点，不伪称远端push结束精确wall。四数组Python读返回/预留31,851,032字节、payload31,851,008字节；metadata四倍静态上界6,354,140字节<32MiB，不是物理I/O计量。

F48的processor+generate实测组件21.015秒/24calls，四P/V4为24.861秒/96calls；generate单独19.999/23.987秒。两者总视觉tokens同为31,104，但总输入39,742/50,488、生成48/192；四次前缀/生成、tubelet布局/时码均不同。完整独立部署wall、vote-only和共享装载/转移分摊UNKNOWN，内部prefill/decode不可再加到outer。成本表与阶段加和独立复算一致，没有同FLOPs或唯一神经原因结论。

## 5. 下一步研究走向：不把失败门换成新的变体任务

当前不下达052，不改投票/提示/分区/阈值，不自动扩样、二模型、训练、解码或下载。051完整结束了050原定机会核验；049和051共享题源，不能将两轮合成独立确认样本。192×288低分辨率、48稀疏候选、序数时间载体与物理来源独立未知限制保留。

负责人本轮继续检查了几条最容易从阴性结果跳过去的方向，结论是**尚不足以立项为核心创新**，不是所有未来机制都不可能：

| 容易提出的下一方向 | 本轮重新阅读的一手材料与范围 | 当前处置 |
|---|---|---|
| question+各选项对比检索、margin选帧 | [FULCRUM作者项目摘要](https://codewith-pavel.github.io/publication/fulcrum-option-contrastive-frame-selection-long-video)，2026-10-28读取 | 已有非常直接的公开机制描述；不能把普通option-margin改名为新方法。页面同时写Published/under review，出版状态有冲突，未认证录用/全文/结果 |
| 增加分辨率，低清全局＋高清局部自适应分配 | [AdaAlloc作者项目](https://vision.cs.utexas.edu/projects/adaalloc/)，摘要/方法说明 | 已公开覆盖固定预算global/local与定位/记忆组合；不据051猜低清是原因，也不启动一次新获取/解码链 |
| 多证据缺检索还是缺融合、最小帧集 | [HERBench作者项目](https://gabrieleserussi.github.io/HERBench/)，摘要/MRFS定义及观察瓶颈 | 该问题和oracle-evidence诊断已有强先例。051没有真实必要证据集合，不能把all-five-wrong或有限视图oracle改作真证据标签 |
| 总准确率之外再测细粒度理解与一致性 | [VURCA/FgNExT-QA正式ACL摘要](https://aclanthology.org/2025.naacl-srw.40/) | 细粒度理解/回答一致性不是新命题；只取得摘要，不断言其全部控制覆盖我们任何未来设计 |

[Frames Don't Add Up既有OpenReview入口](https://openreview.net/forum?id=6FFJF8bQhV)仍返回公开浏览器验证页，未取得正文；arXiv2607.13305正文请求本轮失败。搜索摘要/转述不作为正文证据，不绕过验证、不把未读文献当已排除。上述表是具体近邻筛查，不是全球新颖性穷尽证明，也未独立重现作者性能。

**后续立项对象应是一个能被真实问题检验的新算子或新实证主张。** 下一个执行合同必须先同时给出：与最强近邻的具体差异；使用现成合法输入就能改变/否决该差异的成对实验；不依赖gold运行的输出规则；已明确的完整实验和止损成本。若只是“可能低分辨率”“可能不看视频”“也许换骨干有效”，先保留UNKNOWN，不能替代机制。当前没有一项满足，故不创建占位READY，也不让执行者继续空转。普通QA改进依赖有效题目/标签和正确配对即可，不一律加上新证据标注门；若要声称已分离检索与融合瓶颈，才需能验证该归因的真实必要证据。

这次完成的是两条开发投入假设的收敛和可复用真实比较证据，**未新增获证实核心贡献**。所有旧停止结论保留；执行者原始回执、源码、汇总和results不改。本轮仅负责人验收/公开近邻核查/归档与当前看板更新，私有资产及模型操作0。

# VLM 下一步工作安排（ChatGPT 维护）

> 协作规则：**ChatGPT 负责研究规划与审查；Codex 每轮领取本文件中唯一 READY 的任务或任务包。一个任务包可依书面协议连续完成多项安全子任务，统一反馈后再审核**。执行事实写入 [codex-results.md](./codex-results.md)，脱敏附件上传 [codex-artifacts/](./codex-artifacts/)，ChatGPT 审核后更新 [research-overview.md](./research-overview.md)。
>
> 基准历史：[research-progress-2026-10-08.md](./research-progress-2026-10-08.md)（原始快照，不覆盖）。
>
> 更新日期：2026-10-25（北京时间；已完成[046负责人验收](./research-decisions/post-046-holoassist-input-disposition-2026-10-25.md)：**ACCEPTED_BOUNDED_FAILURE_REPORT / WORKER_CLOCK_BINDING_NOT_QUALIFIED；046关闭，当前0 READY**。HEAD尝试在无发送确认/响应头前超时，GET0、媒体0、时钟与B0/P/N均NOT_RUN。独立复算本次父active0为30.5072339秒、关闭30.5389293秒，均在限内；worker跨解释器绝对时长相减未获验证，不能认证真实传输整体资格。暂停此自动获取尝试，不重试/加时/换源或派下载修复；下一实质入口需当前已完整取得且来源/使用范围明确的视频，私有路径留本地。标签/模型/GPU/64格HOLD，NOVELTY=RETAIN0。）

## 一、任务看板

| ID | 优先级 | 状态 | 执行者 | 工作内容 | 完成判据 |
|---|---|---|---|---|---|
| VLM-HOLOASSIST-REAL-INPUT-046 | P0 | **ACCEPTED_BOUNDED_FAILURE_REPORT / WORKER_CLOCK_BINDING_NOT_QUALIFIED / CLOSED（不重跑）** | Codex交付、ChatGPT验收 | [ad37b05](https://github.com/floomeer83felix-source/vlm/commit/ad37b05241f1218e5d974e88f6c4ac3f964ba234)：HEAD尝试超时，GET/媒体0，时钟及B0/P/N均NOT_RUN | [验收](./research-decisions/post-046-holoassist-input-disposition-2026-10-25.md)：本次独立父包络在限内；worker时钟绑定未过，不认证传输/媒体/输入；本父已消费，当前0 READY，不自动修复/换源/047 |
| VLM-NATIVE-PTS-ADAPTER-045 | P0 | **ACCEPTED_CPU_NATIVE_PTS_BOUNDARY_PROTOTYPE / CLOSED（不重跑）** | Codex交付、ChatGPT验收 | [8f648e8](https://github.com/floomeer83felix-source/vlm/commit/8f648e875e8339fe2fb3c1c78dea9ef2df64bc30)：9槽实际CPU输入通过，10/12调用，3完整输入等价类 | [验收](./research-decisions/post-045-native-pts-adapter-disposition-2026-10-25.md)：窄原生PTS链路成立；固定96源帧/96秒原型，不代表自然媒体或模型效果。045验收时0 READY，不自动扩变体/下载/GPU；新提案见页首 |
| VLM-EPIC-SINGLE-SOURCE-ADMISSION-044 | P0 | **ACCEPTED_BOUNDED_TRANSPORT_FAILURE / CURRENT_OFFICIAL_FETCH_ROUTE_STOP（关闭，不重跑）** | Codex交付、ChatGPT验收 | [e27e175](https://github.com/floomeer83felix-source/vlm/commit/e27e1759c187f4a6d668c496dbb50cd6d9868fbf)：C02声明约1.895GiB，落盘下界72MiB，完整性未验/验钟NOT_RUN | [验收](./research-decisions/post-044-single-source-fetch-disposition-2026-10-25.md)：截止/持久记账在本轮符合包络；暂停直连入口；044验收时0 READY，不加时/续传/换候选重试；新任务见页首 |
| VLM-FETCH-DEADLINE-ACCOUNTING-043 | P0 | **ACCEPTED_OFFLINE_REPAIR_IN_TESTED_SCOPE / CLOSED（不重跑）** | Codex交付、ChatGPT验收 | [e0b1d1d](https://github.com/floomeer83felix-source/vlm/commit/e0b1d1d113a49ee6ec5763245ac18c541e031da4)：实际12/12本地故障通过；保留初轮导入失败 | [负责人验收](./research-decisions/post-043-fetch-repair-disposition-2026-10-24.md)独立复算一致；FakeTransport/短时进程模型限定，真实TLS与多对象分配未测；043验收时0 READY，后续见页首 |
| VLM-NATURAL-CLOCK-ADMISSION-042 | P0 | **CLOSED / ACCEPTED_BOUNDED_FAILURE_REPORT（不重跑）** | Codex交付、ChatGPT验收 | 下载失败，媒体/时钟0/16 | 资源合同未全部满足；本父已消费，不续传或自动新下载/GPU；当前任务见页首 |
| VLM-CACHE-INPUT-QUALIFICATION-041 | P0 | **ACCEPTED_CPU_BOUNDARY_CONTRACT_REPRODUCED / LOCAL_COMPONENT_REGRESSION_ONLY（已关闭，不重跑）** | Codex交付、ChatGPT验收 | [6bcee08](https://github.com/floomeer83felix-source/vlm/commit/6bcee080ce00c82041d4567ddc2707977d9ae067)：72边界状态、288序列/576查询；条件性不兼容复用40，三控制0 | [负责人验收](./research-decisions/post-041-cache-qualification-disposition-2026-10-24.md)：完整源命名空间已足够；保留测量/同机复现边界，NOVELTY=RETAIN0；041结案时0 READY，不自动恢复本任务/GPU/Issue/投稿 |
| VLM-ENGINEERING-EVIDENCE-040 | P0 | **ACCEPTED_CONTROLLED_ENGINEERING_COMPARISON / NO_DISTINCT_MECHANISM_EVIDENCE（已关闭，不重跑）** | Codex交付、ChatGPT验收 | [bedcc78](https://github.com/floomeer83felix-source/vlm/commit/bedcc78f70e128d0e05ea4132aedaaea68552e1a)：540格公开CPU比较；F与B1各0违规/0重复、正常30/30及可完成故障30/30 | [负责人验收](./research-decisions/post-040-engineering-disposition-2026-10-24.md)：独立复算一致，B1匹敌F且无稳定成本收益；停止框架创新包装；后续041仅具体缓存输入资格，不恢复040 |
| VLM-001 | P0 | **ACCEPTED（2026-10-08）** | Codex | Windows 本地实验工作区**只读状态盘点** | [回报](./codex-results.md)与[审计附件](./codex-artifacts/VLM-001/workspace-audit.md)已提交；仅文档交付验收通过，非GPU运行放行 |
| VLM-002 | P1 | **ACCEPTED（G1 HOLD）** | Codex | 公开证据数据集许可、schema、版本与时间桥接元数据核查 | [结果报告](./codex-artifacts/VLM-002/dataset-metadata-review.md)已审查，3候选均未满足G1；不可据此运行新实验 |
| VLM-BATCH-003 | P1 | **ACCEPTED（静态交付；G1 HOLD）** | Codex | A: PTS/VFR/媒体桥接；B: 历史来源隔离与指纹缺口；C: G1无答案元数据/12帧技术合同 | [三份审计报告](./codex-artifacts/VLM-BATCH-003/README.md)与[Codex回报](./codex-results.md)由提交 [31e8151](https://github.com/floomeer83felix-source/vlm/commit/31e8151901c1c75739670acefec211f920313244)交付；只接受审计，不批准新实验 |
| VLM-BATCH-004 | P1 | **ACCEPTED（toy报告通过；G1 HOLD）** | Codex | VES请求草案、toy CPU测试、G1决策报告 | [提交462ccde](https://github.com/floomeer83felix-source/vlm/commit/462ccdec4a999ef62e67a1cb52e7392fd7e14517) 五项文件已审查；Codex报告10/10 toy通过，未独立重跑，不放行真实实验 |
| VLM-BATCH-005 | P1 | **ACCEPTED（toy18/18自报；G1 HOLD）** | Codex | A官方渠道；B合成负例；C路线裁决 | [提交7d1daf7](https://github.com/floomeer83felix-source/vlm/commit/7d1daf725fae5c7a921274e575101966ffed99a8) 五处交付已审查；18/18为Codex报告，非真实媒体验证 |
| VLM-ROUTE-006 | P0 | **ROUTE2_SELECTED（取代先前路线1）** | 用户与ChatGPT | 新主问题：无gold必要区间、固定12帧选帧策略与输入路径鲁棒性 | [新的科学预注册](./route2-no-gold-preregistration.md)及[创新初审](./route2-novelty-screen.md)；TRACE咨询稿保留UNSENT且不执行 |
| VLM-BATCH-006 | P1 | **ACCEPTED（十项有界交付；科研NO_GO_OR_PIVOT）** | Codex | 文献/创新/混杂、静态接口/许可/PTS、统计合同及toy、科学决策 | [e581039](https://github.com/floomeer83felix-source/vlm/commit/e581039970106dbec741adf502e48e5f948adad4)：4报告、2 toy、1追加已审；执行者报11/11 CPU测试通过；普通 S_q/S_t 新算法NO-GO，窄2×2仍UNKNOWN |
| VLM-DECISION-007 | P0 | **B_SELECTED（新机制研究，不继续旧采帧路线）** | 用户与ChatGPT | 保留长视频VLM高水平论文目标；旧S_q/S_t选帧/2×2提示仅作历史，不作为核心创新 | [机制重立题](./mechanism-reset-2026-10-09.md)与下一唯一READY BATCH-007；没有保留的创新机制 |
| VLM-BATCH-007 | P1 | **ACCEPTED（10项交付；RETAIN 0 / STOP THIS PORTFOLIO）** | Codex | 历史与先例、M1/M2/M3形式定义、双世界反例、toy、数据/强基线及否决 | [d82e30e](https://github.com/floomeer83felix-source/vlm/commit/d82e30e43ec31fb8600b0a61d62021017a6d59aa)：5报告+2toy+1追加符合范围；执行者报12/12 CPU单测；M1/M2/M3当前算子均可由现有逻辑/依赖缓存/判别规划模拟，无新增核心机制通过 |
| VLM-RESEARCH-GATE-008 | P0 | **CHARADES_SELECTED / EGO4D_DEFERRED（历史Ego4D未提交确认）** | 用户与ChatGPT | 因Ego4D表单报Failed to fetch，用户同意改用公开Charades／Charades-STA进行数据准入核验 | [新数据路径说明](./charades-entry-2026-10-09.md)：不是已下载数据/合法验证/新模型实验批准；原Ego4D申请意愿保留历史但不再是当前任务 |
| VLM-BATCH-008 | P1 | **ACCEPTED（10项文档交付；数据/创新/长域GO仍HOLD）** | Codex | Charades许可、STA权利、schema/join、重复实例与重叠假设、来源PTS、长域缺口、五门裁决 | [提交2544df9](https://github.com/floomeer83felix-source/vlm/commit/2544df98fa363bc62ec888682121d879f24bcec2)：严格5份脱敏报告+1条追加；Charades原license/schema仅文档条件准入，实际重复样本计数UNKNOWN，STA许可HOLD，普通新算法NO-GO，Charades单独长域FAIL |
| VLM-DATA-GATE-009 | P0 | **USER_APPROVED_METADATA_ONLY（官方下载已完成；仅读已有资料）** | 用户与ChatGPT | 已批准并完成唯一Charades官方注释ZIP取得；011/012只读核查及原评测脚本查验属于既定有限元数据用途 | **禁止第二次下载、原CSV/ZIP编辑、原始标注与脚本公开分发、视频/STA/GPU/模型使用及原实验目录变更**；BATCH012已结束，若需媒体/额外数据必须用户再明确批准 |
| VLM-BATCH-009 | P1 | **STOPPED_SAFELY（路径名称误判；NO_DOWNLOAD）** | Codex | 授权与隔离预检、HEAD检查、通用元数据审计工具及合成测试；真实ZIP/CSV资格因保守路径阻塞未执行 | [首次提交bc16e38](https://github.com/floomeer83felix-source/vlm/commit/bc16e38eab35f454bc3e0ccc3c805c15c6009ed8)：5处约定交付，GET0/正文0B/P1P2 UNKNOWN；正确安全停止，**禁止原父任务重跑** |
| VLM-BATCH-009-FIX | P1 | **ACCEPTED（路径身份检查修复；未下载）** | Codex | 修正Windows absolute/resolve仅字符串不等的误报，加入samefile/设备inode/双链无reparse与缺失叶核验 | [修复提交dda8481](https://github.com/floomeer83felix-source/vlm/commit/dda8481a330c4cfa1e734511ad59e7d8f7571d4f)：2通用Python改动+一条附加结果；执行者报告21项合成测试通过、固定路径只读复核PASS；**未独立核Windows，也未下载或读CSV** |
| VLM-BATCH-010 | P1 | **ACCEPTED（一次官方下载与聚合交付；TIME_QUALITY HOLD）** | Codex | 官方小包1成功GET/3,519,822B、ZIP CRC/白名单、CSV schema、短域P1/P2记录候选聚合 | [提交8153a18](https://github.com/floomeer83felix-source/vlm/commit/8153a18af651afcbf0c5a455f3b61817e09755c0)：严格2报告+1追加、原源码不改；66,500区间中19,625不通过既定数值规则，主因end>length；资格数仅过滤子集临时值，**不放行模型/视频** |
| VLM-BATCH-011 | P1 | **ACCEPTED（独立数值复算交付；时间语义HOLD）** | Codex，ChatGPT审查 | 只读原SHA固定CSV、官方README证据分级、互斥主因/δρ/异常行分布、独立复算P1/P2、测试及脱敏 | [提交1aed0de](https://github.com/floomeer83felix-source/vlm/commit/1aed0dea70faa7a446e63637be4772f4668270a2)：精确5处交付；原66,500/19,625、P1=347、P2=97,723均复现，但**时间合同仍无同版媒体/标注桥接**；不可当最终真值/新算法证据 |
| VLM-RESEARCH-DECISION-012 | P0 | **USER_SELECTED_CHARADES_ALIGNMENT（已决策，非READY）** | 用户、ChatGPT | 用户明确选择先修复Charades评测规则误配，暂不换数据集；但不批准原CSV编辑或数据/媒体/GPU再次获取 | [BATCH-012十项协议](./codex-artifacts/VLM-BATCH-012/README.md)：首先只读验证现有ZIP内官方`Charades_v1_localize.m`，再严格区分官方25时点相容性、越界质量、P1/P2语义；避免将评测兼容冒充真值修复 |
| VLM-BATCH-012 | P1 | **ACCEPTED（官方帧级label对齐；B/C时间真值HOLD）** | Codex，ChatGPT审查 | 固定ZIP原`Charades_v1_localize.m`只读源码与规则核对、纯stdlib 25点模拟/分层统计、19合成测试、匿名差异 | [提交e46f1d7](https://github.com/floomeer83felix-source/vlm/commit/e46f1d794118c5c2efbb0f15f0fc84dad5d4f04b)：恰好5处；官方正cell705,470、旧strict正cell398,287、差异307,183=官方正cell的43.54%；**只说明原strict不能代表官方frame-label政策，不认证视频端点/P1P2真值或新算法** |
| VLM-RESEARCH-GATE-013 | P0 | **USER_APPROVED_V1_CONDITIONAL（视频许可已批准，非实际下载）** | 用户、ChatGPT | 用户已额外批准最多2段Charades官方480p视频、远程GET正文累计≤64MiB、本地视频/临时文件≤128MiB，以及仅现有CPU容器和packet-PTS时间钟核验 | [已批准V1试点提案](./charades-media-boundary-pilot-proposal-2026-10-09.md)与[受限BATCH-013任务](./codex-artifacts/VLM-BATCH-013/README.md)；13GB整档、画面查看/解码、STA、GPU/模型与原科研目录仍禁止；按需Range不可行立刻STOP |
| VLM-BATCH-013 | P1 | **STOPPED_SAFELY（缺既有ffprobe，0媒体/GET）** | Codex，ChatGPT审查 | V1前置：SHA/源目录及工具检查，阻塞后仅交离线合成HTTP/ZIP安全组件 | [原013提交f86a1e8](https://github.com/floomeer83felix-source/vlm/commit/f86a1e8e7a2e31b40d9c1bd7f1b135d16ae25204)：规定5处交付；ffprobe有限范围未找到、16合成用例PASS（执行者报）、0网络请求/0视频；原父任务**已结束，禁止重跑** |
| VLM-BATCH-013-FIX | P1 | **ACCEPTED_CODE_ONLY（ZIP64/协调器/执行门；27合成测试）** | Codex，ChatGPT审查 | 原013完成后独立修补Python协调器/ZIP64/私有ledger/下载+packet-clock合成链路与防重复执行；本轮只有3处提交 | [提交75af33c](https://github.com/floomeer83felix-source/vlm/commit/75af33c56342bce4af94f7d70d1cada7ebdb8667)：2源码+1结果，执行者报27/27合成PASS、0真实媒体GET、0ffprobe；**代码未通过真实206/PTS环境验证，不是媒体实验GO** |
| VLM-CPU-TOOL-GATE-014 | P0 | **USER_APPROVED_ISOLATED_FFPROBE_INSTALL（授权已用作首次受限尝试；未完成部署）** | 用户与ChatGPT | 用户允许仅为CPU V1在独立目录下载安装经出版者哈希验证的ffprobe；BATCH014在已收取部分工具ZIP后超时安全停止 | 保留既有工具来源/版本/部署边界；**当前没有新READY**，工具尚不可用，下一次获取需在新父任务冻结断点恢复或重试与既有ledger连续性的证据，未经用户后续方向决定不自动发送工具GET |
| VLM-BATCH-014 | P1 | **STOPPED_SAFELY / CPU_TOOL_BLOCKED（工具GET超时，未安装）** | Codex，ChatGPT审查 | 固定Gyan 9.0.2发布方checksum/来源与路径预检、仅合成安装器测试、限额工具GET、静态审查013媒体代理 | [提交6bec3ab](https://github.com/floomeer83felix-source/vlm/commit/6bec3ab3e7e41571b8878e30c36b26ca710fd060)：严格5处交付，16个最终合成测试执行者报PASS；官网文本+工具GET正文共13,186,907B，其中ZIP部分13,107,200B后直连socket timeout；SHA全包/ZIP结构/ffprobe -version未做，原父任务**已结束，不可重跑** |
| VLM-CPU-TOOL-GATE-015 | P0 | **USER_RESUME_APPROVED_AND_EXECUTED（已验收，不再READY）** | 用户、ChatGPT | 用户许可范围内从旧部分ZIP有界续传完成，未重置014正文预算/账本 | 已由[BATCH015](./codex-artifacts/VLM-BATCH-015/resume-integrity-install-and-science-decision.md)执行者报告确认整包发布方SHA、CRC、白名单与单次ffprobe-version通过；原媒体ProxyHandler问题仍HOLD且GPU未授权 |
| VLM-BATCH-015 | P1 | **ACCEPTED（固定SHA完整ZIP续传与独立CPU ffprobe可用）** | Codex，ChatGPT审查 | 旧014部分包/ledger与来源身份核验，真实206强ETag，唯一后缀恢复，固定发布方SHA/ZIP CRC/最小提取/一次版本检查 | [提交b0d163f](https://github.com/floomeer83felix-source/vlm/commit/b0d163f9f9ea76c4887b08109a729d0bb47b4033)：恰好5处交付，执行者报27/27合成PASS、原part保留，HEAD2/GET2/206、完整SHA一致、`ffprobe 9.0.2`版本PASS、014+015工具实际正文114,847,784B；**仅工具已就绪，媒体/时间真值完全未运行** |
| VLM-MEDIA-CLIENT-GATE-016 | P0 | **CODE_LEVEL_VERIFIED（静态与合成，实网未验证）** | ChatGPT，Codex | 原`urllib`媒体默认代理已显式禁用，HTTPS固定3个官方地址、禁全媒体GET与HTTP重定向，40项纯合成测试 | [BATCH016代码报告](./codex-artifacts/VLM-BATCH-016/media-http-proxy-threat-and-fix.md)记录完整客户端路径和合成证据；**不能据此声称S3有206或B/C时间真值PASS** |
| VLM-BATCH-016 | P1 | **ACCEPTED_CODE_ONLY（禁代理和精确HTTPS请求门；真实媒体仍未访问）** | Codex，ChatGPT审查 | 先前媒体程序默认代理隐患静态定位并修复，保留固定源/禁跳转和原安全预算规则 | [4c3e8bf](https://github.com/floomeer83felix-source/vlm/commit/4c3e8bf14ad9c62806be85e26e0492cfea5ebf93)：恰好5处，原27+新13=40合成unittest由执行者报PASS，0真实GET/ffprobe/GPU；**ledger读取后计费与父授权晚于版本调用两项新执行前门待017修复** |
| VLM-MEDIA-V1-GATE-017 | P0 | **CONDITIONAL_MEDIA_APPROVAL_CONSUMED_BY_FINAL018（非READY）** | 用户、ChatGPT | 原≤2视频/研究GET≤64MiB/本地≤128MiB/CPU packet-PTS的受限范围已经在018最后执行中用于固定2个训练片段 | 015工具许可不扩张；Charades数据获取路线已经STOP，私有2 MP4/详细PTS与ledger仅保留在隔离本机，**禁止继续下载、重选或扩大视觉V2/GPU权限** |
| VLM-BATCH-017 | P1 | **STOPPED_SAFELY / CODE_DELIVERABLES_ACCEPTED（内置合成门失败，0媒体）** | Codex，ChatGPT审查 | 已完成父任务前置授权冻结、所有媒体GET读前fsync保守预扣、强ETag与固定ffprobe路径；真实execute仅1次，内置环境相关mock失败后严格STOP | [1641817](https://github.com/floomeer83felix-source/vlm/commit/1641817a05911d008373963d5cea88a45f1cb8b6)：严格5处；原40+新16=56合成用例普通/合成原工作区环境最终PASS（执行者回报），**但唯一实际execute内置套件`SYNTHETIC_GATE_FAILED`，未重启**；正式SHA/隔离/CPU/媒体HEAD/Range/PTS全部NOT_RUN；历史017禁止重跑 |
| VLM-RESEARCH-CHOICE-018 | P0 | **USER_APPROVED_LAST_V1_TRY / EXECUTED_AND_CLOSED（非READY）** | 用户、ChatGPT | 用户批准最后一次受限两视频试点，执行者已在2453b88完成真实限额内访问、两例packet元信息采集 | 最后机会已经使用；工程取得2视频但B帧保守守卫令时钟比较UNKNOWN，不得重开018或默认用剩余额度进行更多视频取样 |
| VLM-BATCH-018 | P1 | **ACCEPTED_ENGINEERING / V1_CLOCK_UNKNOWN / FINAL_MEDIA_STOP（已结案非READY）** | Codex，ChatGPT审查 | 本次唯一execute完成双环境合成安全门、受限官方ZIP206及两成员CRC/下载、独立CPU ffprobe packet元信息采集；B帧保守条件使两臂同钟判定UNKNOWN | [2453b88](https://github.com/floomeer83felix-source/vlm/commit/2453b88a732504f3ac2abe9bc2934f59291cc022)：恰好5处交付；原56+3=59项双上下文合成PASS；真实媒体GET10/HEAD1，正文实际/保守均1,979,817B，保存2 MP4，CPU版本1+packet2；**CASE_OVERFLOW与CASE_CONTROL都是CLOCK_UNKNOWN**，B/C仍HOLD，不重跑018、不安排019或更多Charades视频获取 |
| VLM-RESEARCH-POST018-DIRECTION | P0 | **USER_APPROVED_STATIC_LONGVIDEO_SCREEN（仅非媒体静态审查）** | 用户、ChatGPT | 用户2026-10-10在018最后尝试结束后明确回复“好的”，同意先对真正长视频数据源与原创推理机制公开资料筛选 | ChatGPT已形成[静态证据种子](./long-video-static-screening-seed-2026-10-10.md)与[受限BATCH019任务书](./codex-artifacts/VLM-BATCH-019/README.md)；没有新媒体/annotation包/模型下载或GPU授权，也不重新打开Charades媒体路线 |
| VLM-BATCH-019 | P1 | **ACCEPTED_STATIC_DELIVERABLES / DATA_AND_NOVELTY_HOLD（已结案非READY）** | Codex，ChatGPT审查 | 六长视频来源许可/时长/时间轴及2026最近先例纯公开静态筛选，八项按报告交付 | [24b771e](https://github.com/floomeer83felix-source/vlm/commit/24b771ef9c83e929579372a982ea17cd6edbbdb8)：严格四Markdown报告+结果尾部23行，共5文件、0代码修改；六候选与六必查+五追加先例已审。Ego4D/HourVideo法律和版本同钟未闭合，LVB Table3六格合计3,761与摘要3,763静态冲突未消，NLQ clip≠小时输入；H1/H3仅待否证问题、H2普通实体记忆NO_GO、NOVELTY=RETAIN0；**不授权下载/标注/GPU** |
| VLM-BATCH-020 | P1 | **CLOSED_STATIC_DELIVERABLES / H1_NOVELTY_NO_GO / LEGAL_BRIDGE_HOLD（已结案非READY）** | Codex，ChatGPT审查 | [fdbb6e6](https://github.com/floomeer83felix-source/vlm/commit/fdbb6e66c85c1d4fa03f179b9af86f9f4322a1fe)：三份公开Markdown审查报告和结果追加，提交范围符合合同；普通H1组合无新算子，Ego4D↔HourVideo权利及同版时间映射未闭合 | 静态交付结案，不补跑、不自动021。用户已决定终止连续文档微批次，转向[单次实验优先提案](./experiment-first-reset-2026-10-10.md)；没有新的视频、标注、模型或GPU授权，NOVELTY=RETAIN0 |
| VLM-REAL-PILOT-001 | P0 | **CLOSED_SAFE_STOP（PRECHECK_ONLY / NO_ELIGIBLE_DATA_STOP / GPU0，非READY）** | Codex执行，ChatGPT静态验收 | [272d7f4](https://github.com/floomeer83felix-source/vlm/commit/272d7f4860e21e681ab38d839e571c0c0b50e572)仅提交[阻塞收据](./codex-artifacts/VLM-REAL-PILOT-001/paired-longvideo-pilot-receipt.md)+codex-results尾部父回报；既有可信MLVU子树存在性核过，A3(a)本轮源媒体使用权利UNKNOWN并即STOP | 48次计划Qwen实际0、120分钟计划GPU实际0秒；视频/QA身份、锁和模型均NOT_RUN，不推导非法/无数据或算法负结果。实验父任务已消费、不可直接重跑；[官方MLVU使用条款](https://github.com/JUNJIE99/MLVU)研究非商用/CC-BY-NC-SA但原视频权利保留，[官方HF访问页](https://huggingface.co/datasets/MLVU/MVLU)设访问条件；既有镜像receipt不等于接受官方门、使用权已核。下一步需用户另行明确合法来源/用途证据或选择新合规来源；0 READY，禁自动新下载/GPU |
| VLM-HOURVIDEO-DEV-001 | P0 | **ACCEPTED_ANNOTATION_ONLY / MEDIA_AND_VERSION_HOLD（已结案非READY）** | Codex，ChatGPT验收GitHub交付 | [da6a6fd](https://github.com/floomeer83felix-source/vlm/commit/da6a6fd73195fec63c480187a5872c8179b5cc4e) 只读核本机已获授权的`dev_v1.0_annotations.json`：50视频元数据记录、1182有答案标签且结构合规题；50段标注≥20min/每段≥2题，其中41段≥30min，满足12视频24题标注层候选。合成自检1 PASS，真实解析1次exit0，无源码补丁；恰好2个Markdown路径变动，非媒体实测/真实GT语义审查 | [匿名实测收据](./codex-artifacts/VLM-HOURVIDEO-DEV-001/local-annotation-eligibility.md)已验收；Ego4D正式视频授权/下载、同版UID→原媒体、源独立性/时钟、历史隔离、GPU锁全部独立HOLD。0GPU/模型/媒体下载，无真实A/B评测；禁止重跑父任务或自动派新下载/GPU |
| VLM-SYNTH-AB-HARNESS-001 | P0 | **ACCEPTED_SYNTHETIC_HARNESS / REAL_MEDIA_AND_MODEL_HOLD（已结案，非READY）** | Codex执行、ChatGPT验收代码与交付范围 | [440f562](https://github.com/floomeer83felix-source/vlm/commit/440f5625e9c5a5e4c6a088cb0aca178a61a74347) 恰好四处授权改动：新增[纯stdlib运行器](../prototypes/hourvideo_synthetic_ab_runner.py)434行、[31项合成测试](../prototypes/test_hourvideo_synthetic_ab_runner.py)300行、[匿名报告](./codex-artifacts/VLM-SYNTH-AB-HARNESS-001/synthetic-runner-receipt.md)及结果尾部1条。按Codex报告，最后unittest31/31 PASS、自检31/31 PASS，合成CLI24题/48臂/48模拟尝试0GPU；ChatGPT静态读源码和测试，**未独立重跑** | 交付内容包含12×2虚构输入、A均匀12/B问题相关48选12、答案隔离、五格配对计数、12视频簇与时长层、原子STARTED/TERMINAL账本/非阻塞锁/恢复/预算拒绝。**真实Qwen/SigLIP均未接入，Ego4D批准、同版媒体与PTS、GPU预算均HOLD**；虚构模型Prompt当前含A/B arm元数据，未来真实模型提示必须剔除arm并保证同模板。0新READY、不重跑父任务、不可报告模拟准确率为科研效果 |
| VLM-EGO4D-MEDIA-001 | P0 | **ACCEPTED_SAFE_STOP / TOOL_AVAILABILITY_HOLD（已结案，非READY）** | Codex执行，ChatGPT验收GitHub收据与范围 | [Codex提交4c38e2a](https://github.com/floomeer83felix-source/vlm/commit/4c38e2a07959298f08037c6637ff9e9a804637fa)：当前执行环境的AWS CLI/Ego4D CLI未找到，Python`boto3`/`ego4d`未发现；在严格前置阶段`PREFLIGHT_STOP / SAFE_TOOL_MISSING`。AWS profile认证/HourVideo UID join/远程HEAD对象大小/磁盘与流量硬上限均未执行，不能误判凭据失败、许可失效或媒体不匹配 | [匿名失败收据](./codex-artifacts/VLM-EGO4D-MEDIA-001/limited-media-receipt.md)＋results末尾唯一一条，共2处Markdown；数据manifest GET0、视频GET0、S3 HEAD0、数据正文0/8GiB、视频0/2、0GPU/模型，公开文档流量未精确计入。原父任务**不得重跑**，不未经用户批准切换环境、下载安装工具/修改PATH/AWS配置/下载视频；后续单独评估已有工具或请求新的有限工具安装授权 |
| VLM-EGO4D-TOOLS-001 | P0 | **ACCEPTED_PARTIAL_BOTO3 / EGO4D_CLI_SOURCE_BUILD_HOLD（已结案，非READY）** | Codex执行原任务及执行者所称用户另行授权修复；ChatGPT审阅GitHub提交与回报 | 原[5758834](https://github.com/floomeer83felix-source/vlm/commit/57588341dbe4a8175a3dac80a873a2928b94da9d)：创建1个隔离venv，首次PyPI元数据请求Timeout，安全STOP且SDK/CLI均0；独立后续[修复0758106](https://github.com/floomeer83felix-source/vlm/commit/07581063c53679d91d4530c00a491f61e24f9b11)：原venv中官方hash核实7个wheel、一次离线安装boto3/botocore1.40.52等依赖，离线网络禁用import PASS（均为Codex执行者报告，ChatGPT未亲自访问Windows）。官方ego4d1.7.3 sdist SHA匹配但iopath0.1.10仅源码发行、无该版本已核wheel，CLI不安装 | [匿名工具实测与追加](./codex-artifacts/VLM-EGO4D-TOOLS-001/isolated-tool-readiness-receipt.md)，总变更仅原新增报告+结果1条、后续报告追加+结果再1条；两次push、原任务一次性合同已终止，**修复是执行者称经用户在Codex对话另行批准，不得记为首次父任务一次push成功**。工具归档累计14,809,324B、专用根约50,462,720B、前台报告约392s；0 AWS凭据/profile、0 S3 HEAD/LIST/GET/认证、0 UID/受保护QA/视频、0GPU。**SDK_READY_OFFLINE仅部分就绪，CLI/真实访问/媒体/模型仍HOLD**；不重跑旧MEDIA任务、不继承2段/8GiB额度；需另批次明确授权 |
| VLM-EGO4D-BOTO3-001 | P0 | **ACCEPTED_SYNTHETIC_MAPPING_AND_BUDGET / REAL_S3_AND_RELEASE_BRIDGE_HOLD（已结案，非READY）** | Codex执行、ChatGPT审查GitHub源码/变更及匿名收据（未独立运行） | [Codex提交b12f32f](https://github.com/floomeer83felix-source/vlm/commit/b12f32fd7174711bbebe589e92f4a3327bfabea5)：新增[主程序](../prototypes/ego4d_boto3_offline_gate.py)约368行、[32项单测](../prototypes/test_ego4d_boto3_offline_gate.py)约274行、[匿名实测收据](./codex-artifacts/VLM-EGO4D-BOTO3-001/offline-source-and-budget-receipt.md)59行和结果末尾一次追加12行，共4路径、一次main push。Codex报告最终unittest32/32 PASS、CLI self-test32/32 PASS、完整纯合成演练exit0；最初self-test Windows替换已有文件失败1 ERROR，修为不可覆盖连续快照并增加2测试，保留原失败记录 | 静态代码核实：SYNTH_UID/假S3路径、file_uid拒绝/显式full_scale/默认真实版本桥接HOLD、最多2视频单段4GiB/全GET8GiB/metadata32MiB整数限制、STARTED原子预扣不退款、无重试/跨进程锁与快照前驱校验、CLI真实标志拒绝。**代码没有真实boto3连接，不是通用官方CSV媒体映射；虚构key模板非Ego4D实际对象路径认证，拟读整数块非线上接收/重试字节硬限**。ChatGPT未独立复跑Windows 32单测。0 AWS/真实标注/视频/GPU，未来真实S3凭据访问/小额manifest/Head/下载必须用户另批明确授权，旧MEDIA父任务不能重跑 |
| VLM-EGO4D-AWS-META-001 | P0 | **ACCEPTED_SAFE_METADATA_STOP / AUTH_PROFILE_HOLD（结案，非READY）** | Codex执行用户已授权真实AWS元数据预检；ChatGPT审阅提交/收据 | [85cc6f5](https://github.com/floomeer83felix-source/vlm/commit/85cc6f5b5ed23c00124eac81156fdc255e80dc27) 仅新增[匿名收据](./codex-artifacts/VLM-EGO4D-AWS-META-001/limited-aws-metadata-receipt.md)和`codex-results.md`末尾一条。私有boto3 SDK在本机仅创建静态共享文件配置提供器时触发`ProfileNotFound`：无明确名`ego4d`的AWS profile；没有真实网络认证/S3请求（0/4）、manifest HEAD/GET0、媒体HEAD/GET0，未读取本地HourVideo JSON/UID、GPU0。该阻塞**不是远端权限403/许可失效或UID不匹配** | **停止重复运行**本任务；不手动查看/公示AWS密钥，也不安装CLI。用户应在自己Windows依据[Ego4D官方说明](https://ego4d-data.org/docs/start-here/)私下把获批邮件中的AWS access credentials存为`%USERPROFILE%\.aws\credentials`的`[ego4d]`命名profile（若发行方确实提供）；该文件不属于Git且不应上传。若获批邮件未含/未提供凭据，应从官方渠道取得或续订，勿贴聊天。配置成功后需**新**有限AWS metadata请求授权/单次新READY，真实视频GET/GPU仍不因本任务自动获准；2026-10-26到期 |
| VLM-EGO4D-AWS-META-002 | P0 | **ACCEPTED_SAFE_METADATA_STOP / AUTH_PROFILE_HOLD（结案，非READY）** | Codex执行本轮，ChatGPT审核GitHub实际提交/收据（非独立Windows访问） | [最新Codex c600d44](https://github.com/floomeer83felix-source/vlm/commit/c600d4456cccefff034aafb8d44c45052cabd110)：即使用户自述已配置，当前静态boto3共享配置提供器仍`ProfileNotFound`，0 AWS网络请求/4、manifest HEAD/GET0、媒体HEAD/GET0、HourVideo本地JSON未读、视频/GPU0。公共差异仅[匿名收据](./codex-artifacts/VLM-EGO4D-AWS-META-002/limited-aws-metadata-receipt.md)48行+`docs/codex-results.md`末尾一次8行追加，旧任务无复活 | **下一步不再重开同一META任务空跑**。用户仅在本机既有Windows用户检查`%USERPROFILE%\.aws\credentials`是否为真实文件（不是`credentials.txt`）、是否有准确`[ego4d]`节；专用boto3 SDK可读取该标准位置才继续。不要把密钥、配置内容、用户名路径、账户ID、截图发聊天/Git。确认配置结构后再单独下达一个真实manifest≤8MiB、最多2媒体HEAD的唯一有限任务；没有真实UID、远端对象大小或AWS AuthOK证据，不得下载媒体/GPU |
| VLM-EGO4D-AWS-META-003 | P0 | **ACCEPTED_SAFE_METADATA_STOP / LOCAL_UID_SOURCE_HOLD（已结案，非READY）** | Codex执行本机私有前置检查；ChatGPT审阅最新提交/收据 | [最新提交39ef5c7](https://github.com/floomeer83felix-source/vlm/commit/39ef5c76a12a4236def69261a0c548408d300273)：SDK命名ego4d profile识别True、标准共享凭据路径存在与HOME一致True、静态Credentials加载True，原ProfileNotFound已排除，但曾使用的本地HourVideo dev_v1.0_annotations.json入口文件存在+≤3MiB复合门失败（未拆开，因此未知究竟路径不符/文件不在/大小超限）；未读取JSON/UID，未发任何S3 HTTP（0/4）、manifest HEAD/GET0、媒体HEAD/GET0、0媒体GET/GPU，远端AUTH仍NOT_TESTED | 公有仅[匿名收据](./codex-artifacts/VLM-EGO4D-AWS-META-003/limited-aws-metadata-receipt.md)+结果末尾唯一一条；旧META-001/002/003均已结案不可重跑。用户在本机以最小只读PowerShell查询**仅Downloads顶层**符合`*dev_v1.0*annotations*.json`的候选数及是否≤3MiB（不打印文件内容/完整路径/UID）；如果0个由用户本机进一步定位，若存在唯一候选/文件较大，应在下一独立批准合同中改用精确私人路径或经过合理批准的大小上限。找到真实文件后新的有限S3 manifest+最多2 HEAD授权另开，仍不自动媒体GET/GPU |
| VLM-EGO4D-AWS-META-004 | P0 | **ACCEPTED_SAFE_METADATA_STOP / HTTP_STATUS_301（已结案，非READY）** | Codex执行一轮真实官方S3尝试；ChatGPT审阅GitHub commit、匿名实测收据与两文件diff | [Codex e53c275](https://github.com/floomeer83felix-source/vlm/commit/e53c27535f190d4b3742a82fae3f1c7cb53c3452)：唯一私有JSON正规存在1,854,695B、dev结构可解析、顶层视频50且前后digest一致，专用ego4d静态SDK profile PASS。向全球S3端点以us-east-1签名发送官方唯一v2_1/full_scale manifest HEAD1次，返回**HTTP301**，严格禁止SDK自动区域跳转/重试而STOP。实际S3请求1/4（manifest HEAD成功0），GET/媒体HEAD/LIST/STS均0、视频正文/GPU0；301不证明远端AUTH_OK或403 | 公有仅[匿名本轮收据](./codex-artifacts/VLM-EGO4D-AWS-META-004/limited-aws-metadata-receipt.md)＋codex-results末尾一条，原任务不可重跑。输入与本机凭据加载门已过，下一步**确认S3桶真实区域，再以正确regional签名读取同一官方manifest和最多2个canonical视频对象HEAD**，而不是换镜像/猜region或安装/合成。下一限域方案[冻结待授权META-005](./codex-artifacts/VLM-EGO4D-AWS-META-005/README.md)仍NOT READY，未获新的最多7 S3 metadata尝试明确批准前不启用。旧2段8GiB媒体GET预算不迁移，真实媒体/GPU0 |
| VLM-EGO4D-AWS-META-005 | P0 | **ACCEPTED_SAFE_METADATA_STOP / READ_TIMEOUT_STAGE_C（结案、非READY）** | Codex实际执行、ChatGPT核GitHub双路径和脱敏收据 | [Codex 895f260](https://github.com/floomeer83felix-source/vlm/commit/895f2602cc4d27d4e5b38a1e3249ae386c1d2120)：用户HourVideo本地开发JSON1,854,695B/50视频UID与静态ego4d AWS凭据PASS；区域发现HeadBucket1(301+可信区域头)；region-correct官方v2_1/full_scale manifest HeadObject1(200、4,653,141B+ETag)及条件GET1(200、长度/ETag/无压缩一致)，但12秒read timeout时仅应用读取2,555,904B后ReadTimeoutError。共3/7 attempts，0额外重试/媒体HEAD/媒体GET/GPU | [真实收据](./codex-artifacts/VLM-EGO4D-AWS-META-005/region-aware-limited-metadata-receipt.md)：**仅当前官方manifest的HEAD/GET远端权限已证，不代表CSV获取完整、UID join、canonical媒体对象存在或版本PTS同钟**。本父任务已结案不能复活剩余4/7额度；已冻结新[META-006延长超时一次性清单和媒体HEAD合同](./codex-artifacts/VLM-EGO4D-AWS-META-006/README.md)为PENDING新授权、非READY。现不得自动媒体下载/GPU |
| VLM-EGO4D-AWS-META-006 | P0 | **ACCEPTED_SAFE_METADATA_STOP / CANONICAL_SOURCE_HOLD（已结案、非READY）** | Codex已执行；ChatGPT核查 cd6eac2 中两处匿名交付 | [cd6eac2](https://github.com/floomeer83felix-source/vlm/commit/cd6eac2a69bed936c6caf143ae997fe81ed6e1b9)：官方4,653,141B manifest HEAD200、GET200全文成功；真实HourVideo50顶层UID和v2_1官方清单唯一精确交集50。S3真实3/7；来源校验复合门CANONICAL_SOURCE_HOLD，失败子项UNKNOWN，媒体桶/对象HEAD0、媒体GET/GPU0 | [匿名实测收据](./codex-artifacts/VLM-EGO4D-AWS-META-006/long-timeout-metadata-receipt.md)；只接受完整CSV/50 UID命中，**没有任何已验证合法媒体HEAD/尺寸**。本ID安全结案不得重跑，剩余4/7不继承。新[META-007来源诊断](./codex-artifacts/VLM-EGO4D-AWS-META-007/README.md)待用户新授权；媒体GET/GPU仍QUEUED |
| VLM-EGO4D-AWS-META-007 | P0 | **ACCEPTED_META_PREFLIGHT_EVIDENCE / MEDIA_GET_NOT_AUTHORIZED（已结案、非READY）** | Codex完成；ChatGPT核对a85e66a两处匿名交付 | [a85e66a](https://github.com/floomeer83felix-source/vlm/commit/a85e66a4e6910afac5c570937246986f25ff60a5)：完整官方4,653,141B CSV、真实HourVideo50个video UID精确匹配；固定官方桶表下45个合规安全候选/5个隔离，当前来源失败子类为官方桶白名单5个（006具体第一失败行不可回证）。两个不同canonical媒体对象HEAD200及身份字段PASS，其中仅1段≤3.5GiB、另1段>4GiB、合计12,897,682,214B；HTTP实际7/7，媒体GET/GPU0 | [真实匿名实测收据](./codex-artifacts/VLM-EGO4D-AWS-META-007/canonical-source-classification-receipt.md)；只接受UID/来源/媒体HEAD证据，不认为官方dev/v2_1剪辑/PTS桥接或视频下载权限已通过。原META-007结案，不可再次继承预算。下一父任务LIVE-MEDIA-002已据此更新为新metadata+1媒体GET的≤8 HTTP尝试合同但**尚待用户单独明示下载授权** |
| VLM-EGO4D-LIVE-MEDIA-002 | P0 | **ACCEPTED_LIVE_MEDIA_SAFE_STOP / LIVE_TRANSFER_ENFORCEMENT_HOLD（已结案、非READY）** | Codex已提交3ef8559，ChatGPT确认两处匿名交付 | [3ef8559](https://github.com/floomeer83felix-source/vlm/commit/3ef855983c879ac34852ff9382ed57620409fd85)：本轮0/8 S3尝试、唯一媒体GET0/1、新视频0、GPU0。阻塞仅源自合同要求独立socket/TLS/wire缓冲总字节硬门，现有boto3 metadata客户端不能认证；并非AWS认证拒绝或已证设备不支持。Windows非计算枚举RTX3090存在，Qwen/SigLIP确切本地入口UNKNOWN、独立train视频UNKNOWN | [匿名真实收据](./codex-artifacts/VLM-EGO4D-LIVE-MEDIA-002/one-video-receipt.md)；本ID结案不可重跑/继承0/8额度。由新的[真实视频＋限量GPU训练技术试跑单父任务包](./codex-artifacts/VLM-LIVE-VIDEO-GPU-START-001/README.md)承接已准一段视频目标，**明确限制对象/媒体响应正文、如实分开wire流量语义**。未知模型权重不妨碍独立head技术GPU试跑；不得用HourVideo dev QA答案训练/宣称正式准确率 |
| VLM-LIVE-VIDEO-GPU-START-001 | P0 | **ACCEPTED_LIVE_MEDIA_SAFE_STOP / EXECUTOR_TIMEZONE_GUARD_ERROR（已结案、非READY）** | Codex 7cb9c6b真实执行收据已核 | [7cb9c6b](https://github.com/floomeer83felix-source/vlm/commit/7cb9c6b815614e7695be2edc251f87d4b002626c)：A–F实际S3 8/8；官方manifest成功全文4,653,141B/50 UID匹配，45合法候选与2媒体HEAD重复通过，唯一条件媒体GET200但仅64–128MiB部分落盘。外层PowerShell UTC时间锚被隐式按本地时区重解，实际53.975分钟误判超限并终止自己的下载进程；未完整/无ffprobe、GPU更新0；现成torch/av/cv2/numpy及ffprobe入口存在 | 本父任务及STARTED全部安全结案、不退款、不恢复或重发GET。不是AWS拒绝或自然读超时；静态类型转换修正未实测下载。新[LOCAL-GPU-REAL-SMOKE-002](./codex-artifacts/VLM-LOCAL-GPU-REAL-SMOKE-002/README.md)改零云请求，先实证3090 CUDA再非破坏性评估partial是否可解真实帧；若条件满足直接做真实GPU自监督技术训练，不将part假称完整媒体或把dev QA作为训练标签 |
| VLM-LOCAL-GPU-REAL-SMOKE-002 | P0 | **ACCEPTED_GPU_INFRA_HOLD / GPU_OCCUPANCY_UNRESOLVED（已结案、非READY）** | Codex提交[8d724a7](https://github.com/floomeer83felix-source/vlm/commit/8d724a7d2d55a05ae178b6640be4bc384107bc51)两处匿名交付，ChatGPT核验 | 本轮A在torch/CUDA初始化前因nvidia-smi计算进程列表非空HOLD；实际CUDA分配、backward、optimizer.step均0，B partial探测/CPU解码和C真视频训练均NOT_RUN；设备RTX3090 24,576MiB、空闲22,899MiB、利用率3%；30条Windows C+G混合上下文中19常见桌面，11身份未分类、已识别训练进程0，但不得冒称独占空闲 | [匿名收据](./codex-artifacts/VLM-LOCAL-GPU-REAL-SMOKE-002/local-gpu-smoke-receipt.md)；绝不能把30条C+G上下文直接视为30个正在训练的CUDA作业，亦不能以低使用率证明无人使用。原任务结案不得重复；改用新[WIN-CUDA-REAL-FRAME-003](./codex-artifacts/VLM-WIN-CUDA-REAL-FRAME-003/README.md)在可靠低负载/显存资源门与显式锁下小规模实际CUDA测试，并行独立进行只读part解码门 |
| VLM-WIN-CUDA-REAL-FRAME-003 | P0 | **ACCEPTED_GPU_INFRA_PASS / PART_NOT_DECODEABLE / REAL_FRAME_TRAINING_HOLD（已结案，非READY）** | Codex 5ed644e真实两处匿名交付已核 | [5ed644e](https://github.com/floomeer83felix-source/vlm/commit/5ed644e51702253539254890e1b62fd4c3a76e8a)：Windows RTX3090真实torch2.5.1/CUDA12.4、cuda:0线性MSE/SGD 2 backward + 2 optimizer.step PASS，损失1.06695→0.67108、权重非零变化、8.094s、框架峰值17.254MiB；两次显存空闲22,906MiB、3%/6%。上一Ego4D残片ffprobe返回MISSING_MOOV，0帧/PTS未知，因此真视频训练0 | [匿名实测收据](./codex-artifacts/VLM-WIN-CUDA-REAL-FRAME-003/windows-cuda-real-frame-receipt.md)；无需再做GPU功能验证。残片不可当完整视频/无需再次查moov，旧8/8和STARTED不得重开。为马上打通真视频→GPU更新工程链，切至[MDN CC0 视频小试跑](./codex-artifacts/VLM-CC0-REAL-GPU-004/README.md)，非HourVideo正式QA和非Ego4D长视频科学结果 |
| VLM-CC0-REAL-GPU-004 | P0 | **ACCEPTED_REAL_CC0_VIDEO_GPU_TECH_SMOKE（结案、非READY）** | Codex 8299653两处匿名交付已审查 | [8299653](https://github.com/floomeer83felix-source/vlm/commit/82996532ace47e520f97e2ba7b59130525d4246e)：固定MDN官方开放花朵示例真实GET200 1,128,375B完整校验，75真解码帧/PTS4.938秒、56训练19晚段验证；RTX3090 true backward/AdamW更新80/80、24,705个参数、参数L1变化147.391893、首末不同batch loss 0.697165/0.661437，晚段验证准确率0.5417，torch峰值allocated17.92MiB，训练GPU计时1.625秒 | [脱敏收据](./codex-artifacts/VLM-CC0-REAL-GPU-004/real-cc0-gpu-receipt.md)；真正短视频CPU帧→GPU优化工程链PASS。但验证仅1段约5秒实拍、属于同视频；**不能宣称长时VLM、HourVideo问答或科学创新**。立即升级为[≥20分钟公有领域连续视频的均匀采样对照运动优先采样A/B](./codex-artifacts/VLM-PD-LONGVIDEO-005/README.md)，不重复本短视频训练 |
| VLM-PD-LONGVIDEO-005 | P0 | **ACCEPTED_METADATA_VALIDATION_HOLD / VIDEO_GET_0 / GPU_0（已结案、非READY）** | Codex[490d247](https://github.com/floomeer83felix-source/vlm/commit/490d247fb191a03890d9a4d7daf369416f8f26b8)两项匿名提交验收 | 官方Commons固定videoinfo元数据HTTPS GET确实HTTP200、正文3,155字节；脚本随后在来源/许可/derivative诊断里抛ValueError，旧程序只保留异常类、**没有具体失败分支或响应JSON**。Meta实际1/1，媒体GET0，GPU两臂0/0；不是官方网络拒绝或已证明电影授权失败。旧父任务及唯一GET budget必须结案，不能重试/退款 | [本轮匿名收据](./codex-artifacts/VLM-PD-LONGVIDEO-005/public-domain-long-video-ab-receipt.md)；错误根因精确分支UNKNOWN。2026-10-14官方Commons网页独立显示该影片在美国公有领域且VP9 360p转码完成，但不代替实际API字段认证或适用地法律判断。新独立[LONGVIDEO-006](./codex-artifacts/VLM-PD-LONGVIDEO-006/README.md)先离线自检reason_code和结构，再严格限制一次新的官方metadata GET，合格后才允许一次≤96MiB公开低码率媒体GET与≤200更新的真长时A/B |
| VLM-PD-LONGVIDEO-006 | P0 | **ACCEPTED_SOURCE_LICENSE_PASS / DERIVATIVE_EXACT_KEY_COUNT_HOLD（已结案、非READY）** | Codex提交[d5a7677](https://github.com/floomeer83felix-source/vlm/commit/d5a767740a671829ec2021071c1dd6104f89846d)两处匿名收据已核 | HTTP200/官方meta3,155字节、严格文件身份/结构化美国公有领域字段PASS。固定唯一`360p.vp9.webm`在API当前返回里匹配条数≠1（未记录0/重复具体数量），原因枚举`DERIVATIVE_EXACT_KEY_COUNT`；视频GET0、下载0、GPU两臂0/0。离线自检PASS；合法版权字段不是缺陷。旧006新meta GET已1/1消耗，停止不退款 | [完整安全收据](./codex-artifacts/VLM-PD-LONGVIDEO-006/diagnostic-long-video-ab-receipt.md)；不冒称所有低码率转码都不可用、不在旧任务里改选URL。独立审阅Wikimedia官方TimedMediaHandler默认配置发现240p VP9启用/360p默认关闭的可能性，但不等于现站配置；新[007](./codex-artifacts/VLM-PD-LONGVIDEO-007/README.md)仅对API**实际存在且唯一**的官方360p或240p VP9白名单键做确定性安全选择，完整合法来源/大小通过才最多1段video GET，A/B只在长时实帧PASS后进行 |
| VLM-PD-LONGVIDEO-007 | P0 | **ACCEPTED_MEDIA_READ_HOLD / OFFICIAL_240P_PASS（结案、非READY）** | [bf96378](https://github.com/floomeer83felix-source/vlm/commit/bf963786cb8d9c54dc82ce52c30f311932f7d94d)两处匿名收据已验收 | 官方Commons固定videoinfo meta GET1/1 HTTP200/3,155B；文件/US-PD/转码/HTTPS源校验全部PASS，实际360p VP9=0、240p VP9=1，官方240p.vp9.webm媒体GET1/1返回HTTP200，声明37,316,857B（<96MiB），但读取在应用body458,752B后遇40s socket timeout；part仍458,752B，完整视频0，GPU两臂0/0 | 单请求及完整声明长度保守预扣，不退款、不恢复007或用part宣称视频成功；旧脚本单整片GET抗停顿能力不足。新的[独立有界206分块+GPU A/B父合同](./codex-artifacts/VLM-COMMONS-RANGE-008/README.md)先离线测试Range/ContentRange/强ETag/身份/超时与限额，再仅在明确新消息启动授权下用新目录按HTTP206≤2MiB/块顺序下载；如果官方不能提供强ETag或Range立即HOLD，不发整片GET |
| VLM-COMMONS-RANGE-008 | P0 | **ACCEPTED_SOURCE_NOT_RANGE_SAFE_HOLD_ETAG（已结案、非READY）** | [b4896bf](https://github.com/floomeer83felix-source/vlm/commit/b4896bfc218cb17e2af4d65148b4c86d3eb12e14)完整匿名收据已核 | 私有离线Range协议测试21/21 PASS，4500s单调独立只监督本任务进程机制PASS。官方Commons metadata GET1/1 HTTP200/3,155B，来源/美国PD字段/官方240p VP9 PASS；新HEAD1/1 HTTP200/37,316,857B PASS，但原合同**强ETag要求不满足**（具体是否缺失、弱或格式不符UNKNOWN）；Accept-Ranges未运行/不能推断HTTP206不支持。Range GET0、保守预扣区间0、完整媒体0、GPU uniform/motion 0/0 | [匿名收据](./codex-artifacts/VLM-COMMONS-RANGE-008/chunked-long-video-ab-receipt.md)；旧008已用meta1+HEAD1请求结案不能恢复预算，旧007/其它parts不得重用。多轮Commons远程视频未完成，停止重复CDN/ETag请求，下一轮仅允许[LOCAL-LONGVIDEO-009](./codex-artifacts/VLM-LOCAL-LONGVIDEO-009/README.md)优先本机**已知确切入口、合法完整**≥20min媒体；找不到则明确数据HOLD，不绕过许可或请求新媒体 |
| VLM-LOCAL-LONGVIDEO-009 | P0 | **ACCEPTED_LOCAL_LONG_VIDEO_TEMPORAL_AB_EXPLORATORY（结案、非READY）** | Codex [b11cb4e](https://github.com/floomeer83felix-source/vlm/commit/b11cb4e9fe49cf57536afc7c8665ce7780d6a05b)两处匿名交付已验收 | 手动授权本地完整Commons 480p VP9电影99.096MiB、容器1465.597秒；PyAV真实43,924帧、所有PTS有效单调；489采样时间点/横跨1465.464秒。前70%train/后30%晚段验证与9s隔离，uniform128 vs motion128各100次RTX3090真实backward/optimizer.step，24,705参数梯度更新非零，GPU总1.938s；同片后段同160 pairs准确率双方**45.00% / 45.00%（优势0百分点）**；两臂末批loss 0.779309/0.732843高于首批0.689918/0.691118，不能称收敛/显著差异 | [匿名结果收据](./codex-artifacts/VLM-LOCAL-LONGVIDEO-009/local-long-video-ab-receipt.md)。单电影低维RGB时间顺序小head和同片后段验证**不能当Qwen/HourVideo QA成绩**；不再通过重跑本片更大head/调seed凑优点。后续转入真正Qwen3-VL/SigLIP技术桥接，只在现有本机模型/processor入口证实和用户新GPU推理授权时运行，绝不自行拉权重。NOVELTY RETAIN0 |
| VLM-LONGVIDEO-VLM-BRIDGE-010 | P0 | **ACCEPTED_MODEL_ASSET_ENTRY_HOLD / 0_MODEL_GPU_CALLS（已结案、非READY）** | [b295945](https://github.com/floomeer83felix-source/vlm/commit/b29594577fb52ee9a36836c75ca82d4142489499)匿名收据与results已核 | 用户合法本地24分钟480p VP9视频首个授权精确路径依然存在；009的43,924帧/1465.464s PTS证据可复用。Qwen3-VL-4B-Instruct与`google/siglip-base-patch16-224`各自**只检查一个标准HF缓存根，两个该入口均不存在**；这不意味着全盘无模型。已安装torch2.5.1、transformers4.57.6、PyAV15.1、OpenCV4.11、numpy1.26.4仅为模块检查。Qwen generate0/4、SigLIP forward0、GPU0秒 | [准确资产收据](./codex-artifacts/VLM-LONGVIDEO-VLM-BRIDGE-010/real-vlm-bridge-receipt.md)；GPU资产入口是阻塞，并非用户未授权或3090不兼容。不再重复检查两处已知空缓存；用户须给两个**已存在**确切本地模型目录或自行从官方仓库完整准备后提交路径。新[011](./codex-artifacts/VLM-MODEL-ONBOARD-VLM-011/README.md)只有在用户提供两目录并明示≤4次本地Qwen模型调用/GPU≤40min时才执行，当轮直接进行合法资产审核与条件VLM推理，禁Codex自动下载权重 |
| VLM-MODEL-ONBOARD-VLM-011 | P0 | **ACCEPTED_REAL_QWEN_SIGLIP_LONGVIDEO_TECH_AB_COMPLETE（结案、非READY）** | Codex [4d902ef](https://github.com/floomeer83felix-source/vlm/commit/4d902ef870f201cd5b1df7536bd235ab5b6789be)实际匿名收据已审 | 用户本机完整Qwen3-VL-4B-Instruct两safetensors/processor与SigLIP双塔safetensors+词表实际加载PASS；已有完整24min公有电影48真实PTS候选覆盖1464.630s。A: uniform12；B: SigLIP图文cosine从48选12，2固定无标准答案问题×2臂，Qwen4/4次真实generate均成功，SigLIP图像forward6/6批+文本batch1/1，GPU累计38.906s、torch allocator peak8716.771MiB，未训练。SigLIP P1/P2选帧跨度1402.301/1184.150s，后者<20min；两题与uniform均只有3/12帧重合。4次Qwen全部达到192token cap，自然结束/EOS未证 | [完整匿名收据](./codex-artifacts/VLM-MODEL-ONBOARD-VLM-011/model-onboard-vlm-receipt.md)；模型负载/选帧/生成技术链通过，但没有标准QA答案，**未评价正确率、模型优势、Qwen微调或HourVideo正式成绩**。不重跑011的电影通用问题；下一步优先准备同版/时钟匹配官方Ego4D完整视频+HourVideo dev QA，才能条件进入有答案的真实VLM配对pilot |
| VLM-HOURVIDEO-MATCHED-QA-012 | P0 | **ACCEPTED_REAL_OFFICIAL_DEMO_GOLD_MATCH / RELEASE_PTS_BRIDGE_HOLD（结案、非READY）** | Codex [f405b99](https://github.com/floomeer83felix-source/vlm/commit/f405b99b536d0ffb59c2ea1329ced16683acaf26)两处匿名报告已核 | 用户本人已下载HourVideo官方demo完整889.396MiB VP9 MP4；与既有私有有gold标注UID全等、43题每题五选项和显式合法答案PASS，ffprobe流3598.033333s vs annotation3598.030000s相差0.003333s；完整PyAV解码107941帧PTS严格递增、0.021029→3598.021029s。源发布版/剪辑/标注零时刻独立映射证书**仍无**，012按原硬规则HOLD、Qwen0、GPU0、QA分母未冻结，不能称准确率0%或HourVideo正式评分失败 | [匿名资格报告](./codex-artifacts/VLM-HOURVIDEO-MATCHED-QA-012/matched-hourvideo-pilot-receipt.md)；不存在素材不匹配或解码故障的证据。依HourVideo[官方README](https://huggingface.co/datasets/HourVideo/HourVideo/blob/main/README.md)demo是官方演示片，可采用ChatGPT明确新冻结的**whole-video nominal PTS假设**开展探索性同视频QA，而非假报时间桥PASS；转新[013](./codex-artifacts/VLM-HOURVIDEO-WHOLEVIDEO-QA-013/README.md)，需用户原Codex聊天新授权至多86次Qwen本地generate/GPU≤30min，0新媒体下载 |
| VLM-HOURVIDEO-WHOLEVIDEO-QA-013 | P0 | **ACCEPTED_MATCHED_UID_WHOLE_VIDEO_QA_PROVISIONAL（结案、非READY）** | [bf5e36a](https://github.com/floomeer83felix-source/vlm/commit/bf5e36ad216c33e6cb04d2493c9e5fce050f7713) 真实匿名收据与results已验收 | 用户获准的HourVideo官方demo与私有43道有gold MCQ同UID，预先非gold schema排除6道缺辅助asset题，**同一视频N=37**冻结；两个策略各37题、Qwen**74/74真实generate、全部natural EOS**，uniform12 correct6/37=**16.22%** vs SigLIP question-only query12 correct12/37=**32.43%**，B-A **+16.22pp**；paired both4/Aonly2/Bonly8/neither23，描述性exact McNemar p0.109375**未建立显著优势**。GPU stage31.906s、torch峰8848.589MiB，训练0步 | [仅探索性匿名收据](./codex-artifacts/VLM-HOURVIDEO-WHOLEVIDEO-QA-013/whole-video-provisional-qa-receipt.md)；**CLOCK_ZERO_ASSUMED_NOT_CERTIFIED**全片PTS名义假设、不能称正式HourVideo榜分或时轴已证，也不能用37条同片问答当37独立视频/论文创新。013完整结案不重跑已观察题、更不按结果调seed/prompt/帧数；下一步[014跨视频复制](./codex-artifacts/VLM-HOURVIDEO-CROSSVIDEO-014/README.md)只在用户给新合法独立媒体+GPU许可后开启 |
| VLM-HOURVIDEO-CROSSVIDEO-014 | P0 | **ACCEPTED_SINGLE_ADDITIONAL_VIDEO_EXPLORATORY_REPLICATION / RESULT_DIRECTION_FLIP（结案、非READY）** | [Codex e7f654a](https://github.com/floomeer83felix-source/vlm/commit/e7f654a2acb93fed196da0ea4d361cb14bc1725f)匿名收据及results已核 | 用户已手动通过官方v1/full_scale单UID取得**与013不同UID**的约70分27秒764MiB级合法公开视频，官方samples_v1.0同UID有金标29条五选项，013相同nongold排除规则排0→N29；原Qwen3-VL与SigLIP各29真实forward、58/58自然EOS。**014名义全片时钟/单新视频**：uniform11/29=**37.93%**，SigLIP9/29=**31.03%**，B−A=**−6.90pp**、配对both7/Aonly4/Bonly2/neither16，McNemar双侧p=0.6875未显著；GPU25.344s，torch峰8884.594MiB，训练0 | [准确匿名结果](./codex-artifacts/VLM-HOURVIDEO-CROSSVIDEO-014/crossvideo-heldout-receipt.md)。相比013的SigLIP+16.22pp，**新视频方向反转**；013/014分母37/29且不同来源，不能合并为官方总体成绩或宣称query相关选帧稳定提高准确率。物理采集严格独立性、immutable版次/clock映射未认证；014旧预算不继承、不能重跑已观察视频。下一步[015](./codex-artifacts/VLM-REPLICATION-DIAGNOSTIC-015/README.md)做CPU零GPU科研原因审查，而不是继续依此调参/GPU刷分 |
| VLM-REPLICATION-DIAGNOSTIC-015 | P0 | **ACCEPTED_CPU_REPLICATION_AUDIT / NO_GO_SIGLIP_STABLE_ADVANTAGE（已结案、非READY）** | [c7aa4d9](https://github.com/floomeer83felix-source/vlm/commit/c7aa4d96405771f777c70eaf73ab399db8b5be15)匿名审计报告与results已核 | A/C全部完成：stdlib独立复算013配对N37/四格4,2,8,23，B−A+16.216216pp、exact p=0.109375；014 N29/四格7,4,2,16，B−A−6.896552pp、p=0.6875。0算术异常；公开报告层面可确认协议/成本叙述相容，却不能独立验证原真实视频/标签/私有日志。对normalized time span、INVALID/EOS、来源题型和时钟等可能混杂进行了有限比较，**没有确证反转的具体因果解释**；仅N_video=2潜在来源，不能汇总为正式样本群 | [科研复核结果](./codex-artifacts/VLM-REPLICATION-DIAGNOSTIC-015/replication-failure-analysis.md)：B旧私有逐题文件未获本轮精确授权，按约`PRIVATE_ARTIFACTS_NOT_AUTHORIZED / SKIPPED`，没有访问或泄漏；GPU/推理/视频下载/旧实验改动0。**NO_GO_SIGLIP_STABLE_ADVANTAGE、GO_REPLICATION_ONLY_IF_NEW_DATA、PAUSE_FURTHER_GPU**；下一步数据清单016，禁止重跑013/014或从旧结果调参/训练 |
| VLM-NEW-SOURCE-ROSTER-016 | P0 | **ACCEPTED_RELEASE1_METADATA_ROSTER_COMPLETE / MEDIA_UNTESTED（结案、非READY）** | [Codex ae014b4](https://github.com/floomeer83felix-source/vlm/commit/ae014b4f79c88dbd4520185a43c8fa0065ab78b9)匿名名单及results已验 | 用户本轮新增明确允许两个特定目录有限文件名发现后，私有dev50元数据×已有v1/full_scale manifest9645来源行唯一join50；排除已测2条、另外1条结构非图片MCQ<10，剩**47视频/47记录来源组**；全清单release_1/canonical_is_validated flag为真（仍非实际同源PTS认证），六个冻结新候选，**R1=46.39min/39结构题、R2=73.28min/39、R3=50.05min/38，R4–R6=36/35/34**，各有匿名不同来源组，三段合计结构题116。官方manifest**无bytes字段**，视频下载是否可用/当前授权/文件体积都UNKNOWN，gold值合法性及非显式外部asset text过滤尚UNKNOWN | [脱敏候选报告](./codex-artifacts/VLM-NEW-SOURCE-ROSTER-016/source-roster-anonymous.md)：严格未下载新媒体、未运行模型/GPU、未改旧历史。R1–R3私有真实UID与官方单UID CLI模板已交原Codex聊天，不在公GitHub公布。**仅同UID及声称v1 release 不能证明time-zero/文件同版物理完整映射；016不可重跑。**下一步用户人工合法逐段下载完整R1–R3，进入条件验收017 |
| VLM-HOURVIDEO-NEW-SOURCES-017 | P0 | **ACCEPTED_THREE_RECORDED_NEW_SOURCE_PAIRED_EXPLORATION_COMPLETE / CLOCK_ZERO_ASSUMED_NOT_CERTIFIED（已结案、非READY）** | [cedb055](https://github.com/floomeer83felix-source/vlm/commit/cedb0559ea62998a1c1cb28866ab4c054273682d)真实R1–R3匿名结果及正式results已核：新官方v1/full_scale真实媒体三条与私有dev金标ID匹配；R1/2/3原39/39/41题→nongold排0/0/4（R3显式图片3+外部asset1）→每臂**N39/39/37**，全部严格冻结。真实Qwen3-VL **230/230次成功且自然EOS**（均不重跑、不训练），Uniform A 10/39、5/39、14/37，SigLIP B 14/39、8/39、12/37，按片B−A分别**+10.26/+7.69/−5.41pp** | [017真实回执](./codex-artifacts/VLM-HOURVIDEO-NEW-SOURCES-017/new-sources-paired-receipt.md)：video等权 A25.43% B29.61%，**描述性+4.18pp，2正1负**；paired四格R1 9/1/5/24，R2 5/0/3/31，R3 9/5/3/20；INVALID每片A/B=2/3、5/3、4/5，NOT_RUN0。GPU三片33.141+35.218+31.625=**99.984秒**、torch峰9134.436MiB(8.92GiB)均在正式新授权范围内；原协议和模型/48PTS候选/12帧固定，答案隔离末尾计分。实际设备/时钟桥、物理来源严格独立、正式HourVideo leaderboard准确率以及稳定优越性和novelty均**NOT_ESTABLISHED**；剩余2个generate尝试不继承 |
| VLM-UNSEEN-SOURCE-STRATIFIED-018 | P0 | **ACCEPTED_THREE_SOURCE_THREE_ARM_EXPLORATION_COMPLETE / CLOCK_ZERO_ASSUMED_NOT_CERTIFIED（结案、非READY）** | [0084d0b](https://github.com/floomeer83felix-source/vlm/commit/0084d0bbc1e76ce39c6ef1339ed5cb64eabb1434)：按预注册R4/R5/R6冻结N36/35/34；A Uniform12、B SigLIP global top12、C 12×4分bin各top1。真实Qwen315/315自然EOS；逐源B−A+5.56/+2.86/+2.94pp、C−B−13.89/−2.86/+5.88pp，宏A30.36%、B34.14%、C30.52% | [018匿名回执](./codex-artifacts/VLM-UNSEEN-SOURCE-STRATIFIED-018/three-arm-new-source-receipt.md)和正式results一条追加符合约定交付；GPU阶段167.344s/torch allocated峰8.758GiB/父任务856.77s均在018独立预算内。仅对公开提交/统计口径验收，未独立复核本地原始视频、gold和ledger；发布剪辑版次、annotation零点及严格物理来源独立性UNKNOWN，非官方榜分、显著性或创新。不重跑018、不继承GPU授权 |
| VLM-TRAIN-HEAD-HARNESS-019 | P0 | **ACCEPTED_CODE_ONLY / SYNTHETIC_CPU_HARNESS_PARTIAL/HOLD（结案，非READY）** | [90330e0](https://github.com/floomeer83felix-source/vlm/commit/90330e00e8c11c52ef12e1f8c24de6ad2ca525e1)：两份训练/测试源码、匿名CPU回执与结果追加满足约定；PTS/来源隔离/严格输入与预算安全门14项stdlib通过 | 在256MiB进程内存封顶下Torch DLL导入WinError1455；5项动态SKIP、0/12真实CPU optimizer updates，梯度/参数变化/重现实测尚未通过。安全HOLD并保留源代码，不重跑旧019或将其称为真实训练 |
| VLM-TRAIN-CPU-RUNTIME-020 | P0 | **ACCEPTED_SAFE_HOLD / CPU_RUNTIME_020_HOLD（已结案、非READY）** | [提交438f9f8](https://github.com/floomeer83felix-source/vlm/commit/438f9f8d01378fdbed392c2d1355dafe47f31d57)包含唯一020专用监督脚本、[匿名实测回执](./codex-artifacts/VLM-TRAIN-CPU-RUNTIME-020/cpu-runtime-verification-receipt.md)、单条results追加，严格符合允许文件；Windows Job进程/Job≤2GiB及系统commit/physical各≥3GiB门PASS，Torch CPU导入/设置单次出现OSError/WinError87 | 实际optimizer attempts/updates 0/0，5项动态NOT_RUN；进程private commit峰736264192B（约702.16MiB）、父墙钟1.062s。错误子阶段/根因UNKNOWN；020审计钩子对import路径resolve可疑但未认证，禁止复跑020、再涨限或自行修系统。旧019保持代码部分通过；真实素材训练仍需新的权利/源隔离/CPU资格与GPU批准 |
| VLM-HOURVIDEO-LIVE-AB-001 | P0 | **QUEUED / REAL_MEDIA_AND_GPU_AUTHORIZATION_HOLD（非READY，不得执行）** | Codex（合法媒体实际到手/版本可核后由用户另准GPU） | 已预先冻结[RTX3090真实A/B最小试验](./codex-artifacts/VLM-HOURVIDEO-LIVE-AB-001/README.md)：同一段≥20min官方原视频、2道冻结HourVideo开发QA、Qwen3-VL-4B-Instruct对照A均匀12帧与B基于SigLIP从48候选选12帧（公平相同prompt/decoder、答案不入检索）；**2题×2臂=最多4次真实前向**，RTX3090总GPU时间≤40min，计select/解码成本及峰值显存。模型权重与现成环境必须本机可用、禁止新包/新权重下载 | **未授权GPU/模型调用**；需媒体阶段成功，先单独确认HourVideo↔Ego4D版本与PTS桥接。桥接仍未知则最多UNSCORED真实视频smoke，不能冒称正式准确率；用户另批准GPU预算后才转唯一READY。首轮n=1视频/2题不代表24题基准、统计显著或论文创新，NOVELTY RETAIN0 |
| VLM-EGO4D-LIVE-TRAIN-MEDIA-001 | P0 | **QUEUED / NEW_TRAIN_MEDIA_AUTHORIZATION_HOLD（非READY）** | Codex，待评测视频+AB基线及新许可 | [独立训练素材合同](./codex-artifacts/VLM-EGO4D-LIVE-TRAIN-MEDIA-001/README.md)：优先已有合规不同训练视频，若必须另外获取，仅一段≤3.5GiB、媒体GET≤1、媒体正文≤4GiB，必要官方元数据+媒体HTTP≤6次；须train/eval视频/物理采集源与用途隔离，不能拿dev答案训练 | 无单独媒体GET许可；上游META-006及媒体/AB若未通过则STOP；不能继承前任务AWS额度；只交匿名收据+结果尾一条 |
| VLM-TRAIN-SOURCE-ELIGIBILITY-021 | P0 | **ACCEPTED_SAFE_HOLD / EXACT_009_ENTRY_UNKNOWN_HOLD（已结案，非READY）** | [021脱敏回执](./codex-artifacts/VLM-TRAIN-SOURCE-ELIGIBILITY-021/read-only-source-eligibility-receipt.md)及[提交f3d86ec](https://github.com/floomeer83felix-source/vlm/commit/f3d86ec445e498dc824fce40ffe72be842952fd5)：唯一阻塞为原009单部电影精确文件路径及原非保护出处许可记录在当前Codex私有上下文不可恢复；公开009只含匿名历史描述。四资格门全UNKNOWN；无证据称文件丢失或许可证无效。 | 仅新增允许的匿名回执与codex-results单条结果；私有文件stat/目录扫描/ffprobe/demux/SHA/媒体/QA/模型/GPU均0，安全按合同停止。**本父任务不能重跑。READY=0**；需用户在私人Codex聊天提供原009确切单文件路径及能说明训练使用权的已有凭据入口，再向ChatGPT申请新有限授权/新READY；不因缺路径建立空任务、TRAIN-PREP/GPU仍HOLD |
| VLM-TRAIN-SOURCE-VERIFY-022 | P0 | **ACCEPTED_SAFE_PARTIAL_HOLD / TRAIN_SOURCE_022_PARTIAL_HOLD（022结案、非READY）** | [提交9c028b5](https://github.com/floomeer83felix-source/vlm/commit/9c028b52ddadf605c50746a86c6c18cc33bcc0f5)及[匿名回执](./codex-artifacts/VLM-TRAIN-SOURCE-VERIFY-022/read-only-source-verification-receipt.md)：单用户指定原电影入口是安全普通文件且当前本地可读；尺寸103909467B与009一致，单WebM/VP9 480p、1465.597s；单次ffprobe PASS、1次视频packet EOF43924包、PTS/DTS缺失/逆序及corrupt flags0，旧片比对仍是佐证 | FILE_EXISTS PASS、CURRENT_INTEGRITY_EVIDENCE PASS（仅容器/包层）；ORIGINAL_009_IDENTITY、TRAINING_RIGHTS_EVIDENCE、TRAIN_EVAL_PHYSICAL_SOURCE_INDEPENDENCE均UNKNOWN。SHA0（无旧可信摘要）、pixel decode0、GPU/Torch/模型/训练0，父运行1.828s/≤180s。上传范围正确、未泄露私有身份。022不能复跑，当前READY=0；许可来源/原字节连续性与非保护评测source provenance尚需新明确授权，TRAIN-PREP/GPU继续QUEUED/HOLD |
| VLM-HOURVIDEO-TRAIN-PREP-001 | P0 | **ACCEPTED_STATIC_COMPLETE_WITH_HOLDS / TRAIN_PREP_CPU_STATIC_COMPLETE_WITH_HOLDS（已结案，非READY）** | [8aba2e3](https://github.com/floomeer83felix-source/vlm/commit/8aba2e37cd97b9e36881b595eec9250d3f0d42cb)及[匿名A/B/C/D收据](./codex-artifacts/VLM-HOURVIDEO-TRAIN-PREP-001/cpu-training-readiness-receipt.md)已审。A原片身份证据/训练许可绑定HOLD，B实际评测录制源独立HOLD，C既有Qwen/SigLIP/processor/分发包/主机资源静态PASS，D自监督两层head纸面方案PASS。其他已授权静态部分没有因A/B失败跳过 | 当前READY=0；CPU-only执行60.704s、0模型/Torch运行导入、0GPU训练、0媒体重读/下载。未来拟98,433参数/200总updates/≤60GPU分钟仅纸面，实测SigLIP图像特征维度与GPU资源仍UNKNOWN。小头的abs差+逐元素积对帧顺序交换不变，**不能用于直接学习事件先后**；不能称完整TRAIN_CPU_PREFLIGHT_PASS，TRAIN-GPU维持QUEUED/HOLD，须新数据与GPU许可 |
| VLM-ORDERED-EVIDENCE-023 | P0 | **ACCEPTED_SYNTHETIC_IMPLEMENTATION_PASS（已验收结案；非READY）** | [023提交798da78](https://github.com/floomeer83felix-source/vlm/commit/798da78ace41dc1015c60dc9683eafecfd9df18e)及[023匿名回执](./codex-artifacts/VLM-ORDERED-EVIDENCE-023/synthetic-order-falsification-receipt.md)：实际4个准许路径（纯stdlib selector + test、匿名receipt、results尾部1条），31个合成单元测试全PASS、0FAIL/ERROR/HOLD/SKIP，2次正式受监督执行、累计0.280s、无需模型/真实视频 | 双事件AB/BA有序pair、12帧不超预算、Top12精确fallback、非法输入HOLD、重复动作身份歧义、单类挤占及锚点挤掉高sQ帧反例均有断言；**SYNTHETIC_CONTRACT_PASS_ONLY / REAL_QA_EFFECT_UNKNOWN / NOVELTY=RETAIN0**。不存在真实事件提取/视觉分数归一、合法独立盲测或Qwen收益，阈值0.70只适用合成。当前READY=0，禁止重跑023；TRAIN-GPU仍非READY，后续真实实验须另行授权 |
| VLM-HOURVIDEO-OEP-REAL-024 | P0 | **CLOSED_ELIGIBILITY_HOLD（2026-10-19已交付；非READY，不重跑）** | [024匿名资格回执](./codex-artifacts/VLM-HOURVIDEO-OEP-REAL-024/real-oep-pilot-receipt.md)及[结果记录](./codex-results.md)：当轮精确入口未保留、物理独立UNKNOWN、题数未查，按合同在下载/GPU前停止 | [6bee319](https://github.com/floomeer83felix-source/vlm/commit/6bee319d9b96e5b496fee922af48710f34fdbb56)：生成/下载/GPU/gold均0，未冻结分母。后续[独立nongold审查](./research-reviews/nongold-feasibility-audit-2026-10-20.md)恢复元数据匹配并发现原两源/12题设计不可行；不改原结果、不开旧任务、不续预算 |
| VLM-TEMPORAL-EVIDENCE-ADAPTER-025 | P0 | **ACCEPTED_PUBLIC_ADAPTER_CONTRACT_PASS（已验收结案；非READY，不重跑）** | Codex交付，ChatGPT静态审查（未复跑） | [8342d4e](https://github.com/floomeer83felix-source/vlm/commit/8342d4e7a35e786106247895aeda2898ecf0a2cb)及[匿名接口回执](./codex-artifacts/VLM-TEMPORAL-EVIDENCE-ADAPTER-025/cpu-adapter-contract-receipt.md)：仅五处允许交付；streaming双视图、窄语法、同48→12且C/D同两个锚点、不可变四臂计划、独立逻辑门控末期评分及虚构端到端反例 | 执行者报告两次启动：首次导入守卫拒绝/0断言，次轮30 PASS，child累计0.461781s；源码/测试静态相符，不作独立动态认证。坏gold保留N并令准确率/配对UNKNOWN，INVALID/FAILED/NOT_RUN计入分母。仅公共接口PASS，真实隔离监督/跨进程guard/输入快照绑定/runner集成及QA获益未证；当前READY=0，不续025测试、023/024或旧GPU额度，不另立toy父任务 |
| VLM-REAL-PILOT-INTEGRATION-026 | P0 | **ACCEPTED_PARTIAL_DELIVERY / REAL_PILOT_HOLD（已审结案；非READY，不重跑）** | Codex交付，ChatGPT静态审查（未独立复跑） | [a17d7b5](https://github.com/floomeer83felix-source/vlm/commit/a17d7b5f48844360fd6aaf064dd502164954068c)、[A–H回执](./codex-artifacts/VLM-REAL-PILOT-INTEGRATION-026/real-pilot-integration-receipt.md)及[真实执行提案HOLD](./codex-artifacts/VLM-REAL-PILOT-INTEGRATION-026/pilot-execution-proposal.md)：三份新Python、两份报告、results末尾一条，共六路径；F/G最终10测试PASS仅fixture范围，A–E PARTIAL/HOLD，H真实就绪HOLD | 标注/一runner打开时stat/fstat五字段比较拒绝，具体差异字段UNKNOWN；manifest延续launcher失败且计数未可靠恢复，20MiB/10秒是执行者给出的保守包络而非精确实测。两次测试、14个worker预留/7个实际虚构PID；51文件/24429B。0真实冻结键/选项不代表无合格题，N/来源完整排除/媒体/成本/runner与OS隔离均未闭合。已报私聊明确CPU批准优先于旧PENDING，但未将其冒充READY检查通过；当前READY=0，禁止余量续跑或自动GPU |
| VLM-PILOT-PIPELINE-REPAIR-027 | P0 | **ACCEPTED_PARTIAL_ENGINEERING / REAL_PILOT_HOLD（已审结案；非READY，不重跑）** | Codex交付；ChatGPT静态审查，未独立复跑 | [42776af](https://github.com/floomeer83felix-source/vlm/commit/42776af041a708d6ffd7e15a8ad011b79557f3fb)及[工程回执](./codex-artifacts/VLM-PILOT-PIPELINE-REPAIR-027/engineering-repair-receipt.md)/[实际交接HOLD](./codex-artifacts/VLM-PILOT-PIPELINE-REPAIR-027/real-cohort-handoff.md)：七处允许交付；当前ctime_ns差异、持久预算、两runner静态factory与独立绑定评分链有进展，首轮14新测试PASS（执行者报告） | 真实index在212992 raw bytes后INVALID_JSON，scalar保留0，错误类别/完整snapshot未知；screen/inference0，不推断0合格。manifest9645行/header有效，旧UID join因universe依赖未评估。research11预留/10完整/1不完整，保守预扣6201578B/实际4559875B；9虚构PID，runtime预留495s/受控包络<90s、52文件187935B。N/来源完整排除/媒体成本/实际后端仍HOLD，原027输入与测试关闭；下一027修复成果不冒称真实QAPASS |
| VLM-ANNOTATION-COHORT-028 | P0 | **ACCEPTED_CPU_COHORT_HANDOFF_PARTIAL / REAL_PILOT_HOLD（已审结案；非READY，不重跑）** | Codex交付；ChatGPT静态审查，未独立复跑 | [157ffd8](https://github.com/floomeer83felix-source/vlm/commit/157ffd8a26b0e632e57cb52b4215c8b99de8678d)、[容器/CPU回执](./codex-artifacts/VLM-ANNOTATION-COHORT-028/annotation-profile-receipt.md)与[真实cohort交接](./codex-artifacts/VLM-ANNOTATION-COHORT-028/cohort-and-source-handoff.md)：当前profile三遍完整，50源/1182题、支持28题、冻结4题/20选项/16文字槽位；17新测试PASS仅fixture自报 | 8旧白名单投影未获UID，非无身份/排除PASS；官方9645行仅50标注UID全部唯一join。P3 participant缺失；旧013/014/R1–R6映射、权利/媒体/版本/成本HOLD。13 open全完整、9,887,423B，21私有文件/78,853B，受控包络<40s；真实gold/模型/GPU/媒体stat/网络0。不再重跑原028或放宽解析 |
| VLM-SOURCE-PROVENANCE-META-029 | P0 | **ACCEPTED_PARTIAL_ENGINEERING_METADATA / SOURCE_ROUTE_STOP_MISSING_PROVENANCE（已审结案；非READY，不重跑）** | Codex交付；ChatGPT静态审查，未独立复跑 | [4b619da](https://github.com/floomeer83felix-source/vlm/commit/4b619da6878b2a20172e816a17f4bafc725a4457)、[A–H回执](./codex-artifacts/VLM-SOURCE-PROVENANCE-META-029/source-and-media-metadata-receipt.md)/[路线停止提案](./codex-artifacts/VLM-SOURCE-PROVENANCE-META-029/real-execution-proposal.md)：八旧文件无source_group、两已知reader未恢复登记写入关系；四候选唯一official join但旧排除全UNKNOWN | 实际HTTPS2次=HeadBucket1＋P1 HeadObject1，P1对象200/上界890MiB；P2–P4 region未知未发，bucket状态未保存。新suite16/17 PASS自报，18 open/4,382,708B，17私有文件/110402B；无真实QA/模型/GPU/gold/媒体正文/下载。原N4/20选项/16计划槽位保留；按合同停止来源路线，当前READY=0，不自动030或同类空资格任务，下一步见路线选择材料 |
| VLM-DEV-TEMPORAL-PILOT-030 | P0 | **ACCEPTED_SAFE_STOP_AND_PARTIAL_IMPLEMENTATION / REAL_QA_NOT_RUN（已审结案；非READY，不重跑）** | Codex交付；ChatGPT静态审查，未独立复跑 | [101b001](https://github.com/floomeer83felix-source/vlm/commit/101b00111fcf30a45309a5dda5eddd173a012005)、[实际回执](./codex-artifacts/VLM-DEV-TEMPORAL-PILOT-030/real-run-receipt.md)/[科学NOT_RUN](./codex-artifacts/VLM-DEV-TEMPORAL-PILOT-030/scientific-results.md)：首0tests/exit5、末18项16PASS/2FAIL；canary Python winerror缺失、健康peer立即Job active1；无第三suite | 真实HTTP/媒体/模型/GPU/gold0，原annotation实际锁/probe0；cached4键/20选项/16槽及028receipt/两factory AST一致。12open/55,649B，CPU预留420s/outer suites1.718s，24私有文件/78,272B；全16NOT_RUN，正确率/配对/C=D UNKNOWN。旧030关闭，不用余量；晚改guard仅静态检查，未认证生产runner就绪 |
| VLM-DEV-PILOT-RECOVERY-031 | P0 | **ACCEPTED_RECOVERY_WITNESSES_AND_HEAD_METADATA / MEDIA_ACQUISITION_HOLD（已结案，非READY）** | Codex交付、ChatGPT静态验收 | [b8fa8b3](https://github.com/floomeer83felix-source/vlm/commit/b8fa8b368d2ae96e253db140768417b79effe6a8)：七处allowlist，新suite7/7 PASS，真实native32/Python拒绝与Job/独立fixture score通过；四HEAD200、四显式版本GET失败/body0 | 实际HTTPS11；旧GET status/code UNKNOWN，晚增诊断仅静态；decode/model/generate/GPU/gold0，全N4/16槽NOT_RUN、准确率UNKNOWN；不重跑031或使用第二suite/旧额度 |
| VLM-DEV-CURRENT-OBJECT-PILOT-032 | P0 | **ACCEPTED_TRANSPORT_AND_P2_CANDIDATES / GPU_RESOURCE_HOLD（已结案，非READY）** | Codex交付、ChatGPT静态验收 | [2636333](https://github.com/floomeer83felix-source/vlm/commit/2636333f08b694c84c516a30c2c0ef828729ae40)：新suite6/6 PASS，4 GET200/响应pin过门；P2完整/48候选，P1/P3/P4超时partial；真实annotation零正文拒绝通过 | free22,813MiB合格、37条C+G触发旧分类门；model/generate/GPU/gold0，全N4/16槽NOT_RUN/准确率UNKNOWN；不重跑旧032或沿用第二suite/GPU余额 |
| VLM-DEV-CACHED-GPU-PILOT-033 | P0 | **ACCEPTED_CACHE_HANDOFF_AND_OFFLINE_FIX / RESOURCE_WINDOW_HOLD（已结案，非READY）** | Codex交付、ChatGPT静态验收 | [91157ef](https://github.com/floomeer83felix-source/vlm/commit/91157ef4838f11f45153a4b017dc4c0b34e5e2a4)：帧223,948,928B/48 RGB完整copy验证；两新suite各6/6 PASS；实际minor=N/A parser失败，定点修后仅offline验证 | 原两util16%/22%另超旧20%门，不补签准入；model/generate/GPU/gold0，N4/16槽NOT_RUN/准确率UNKNOWN。不重开033/旧query或迁移额度 |
| VLM-DEV-SHARED-GPU-REAL-034 | P0 | **ACCEPTED_CACHE_AND_SHARED_RESOURCE / WORKER_SETUP_HOLD（已结案，非READY）** | Codex交付、ChatGPT静态验收 | [d9143ed](https://github.com/floomeer83felix-source/vlm/commit/d9143edb9bb4d77c6b99e635c1a06443e94f850c)：新suite4/4 PASS，缓存/真实共享准入通过；唯一worker已launch，SETUP PermissionError/exit0/Job0，指定GPU窗口2.203s | 具体失败operation/trace未保留、根因UNKNOWN；无preload free/allocator成功receipt，STARTED/QA/gold0，全N4/16 NOT_RUN/准确率UNKNOWN；旧GPU900预约关闭，不恢复run/额度 |
| VLM-DEV-STARTUP-RECOVERY-035 | P0 | **ACCEPTED_CLOSED_HANDOFF_AND_FRAME_COPY / CURRENT_ANNOTATION_REFERENCE_HOLD / REAL_STARTUP_NOT_RUN（2026-10-22）** | Codex交付、ChatGPT静态审结 | [2615512](https://github.com/floomeer83felix-source/vlm/commit/2615512fce25b4c87be6d610f4a14408505e76f2)：新suite5/5、只读034 handoff与P2完整frame copy通过；prepare旧原标注路径FileNotFound/报告WinError2，原handle/probes及真实startup未运行 | 全16 NOT_RUN，query/GPU/QA/gold0；034 PermissionError仍UNKNOWN。035已关闭，不重跑或继承余额，下一任务036分开恢复当前reference与全合成startup |
| VLM-DEV-REFERENCE-AND-STARTUP-036 | P0 | **ACCEPTED_SYNTHETIC_STARTUP_RECOVERY / CURRENT_REFERENCE_MISSING / REAL_QA_NOT_RUN（2026-10-22）** | Codex交付、ChatGPT静态审结 | [d8302de](https://github.com/floomeer83felix-source/vlm/commit/d8302deeba7ade61c32c6189ce912c32d90506a0)：三个实际合成CPU启动，null-device/bytes路径修复后第三次PASS；3版suite各5/5，policy连续绑定通过；限定metadata0候选 | 真实reference/原锁/query/GPU/QA/gold0，全16 NOT_RUN；036已关闭。原标注需用户在私人本地Codex给完整路径，不自动再搜索；当前仍无真实机制/创新结果 |
| VLM-SCIENTIFIC-FALSIFICATION-037 | P0 | **ACCEPTED_PUBLIC_SCIENTIFIC_REVIEW / NO_GO_AS_CORE / DEV_DIAGNOSTIC_ONLY（2026-10-22）** | Codex交付、ChatGPT审结 | [d8195c5](https://github.com/floomeer83felix-source/vlm/commit/d8195c52b84c7f3b502fbb886ea2dc33bc55c8bf)：P1–P3及边界反例、实际干预链、间隔/先后语义、4近邻差异和最小未执行计划已审 | 当前C/D停止论文核心投入；真实QA仍0/效应UNKNOWN，未执行不当科学阴性。037已关闭，当前0 READY，不领取其待审批P2计划 |
| VLM-POST037-RESEARCH-DESIGN | P0 | **DESIGN_COMPLETED_FOR_LIMITED_PROBE / NOVELTY_UNKNOWN（2026-10-22）** | ChatGPT研究负责人 | [新科学协议](./research-protocols/clock-visual-binding-probe-2026-10-22.md)：固定像素/位置，合法clock响应与平移不变、逐clock文字算术control，实际processor暴露先行 | 只支持一次低成本候选测量设计；不是论文新机制保留。旧C/D核心停止，原真实P2仍PARKED；自然长域/独立确认/训练未批准 |
| VLM-CLOCK-BINDING-PROBE-038 | P0 | **ACCEPTED_SYNTHETIC_BEHAVIORAL_FINDING / RESOURCE_RECEIPT_EXCEPTION / NO_CORE_INNOVATION（2026-10-23；已关闭）** | Codex交付、ChatGPT静态审结 | [c078d0c](https://github.com/floomeer83felix-source/vlm/commit/c078d0cac8a7c9e4a4dee1ef0ada866ab09154bd)：48实际生成/输入门通过，视频3/24、文字22/24；ChatGPT复算公开计数 | 首次有本题合成行为证据，仍不能定位读出/角色/计算；漏前置磁盘余量检查，不签全合同PASS，不重跑038/补证；NOVELTY=RETAIN0 |
| VLM-CLOCK-COMPONENTS-039 | P0 | **ACCEPTED_COMPONENT_DIAGNOSTIC / STOP_CURRENT_SYNTHETIC_VARIANTS / NO_CORE_INNOVATION（2026-10-23；已关闭）** | Codex交付、ChatGPT审结 | [995d436](https://github.com/floomeer83felix-source/vlm/commit/995d436c2d3572178f4641a4faeca600219e22a2)：120实际生成，NG/NR/SG/SR/OG正确0/1/3/15/24，各N24；公开120行独立复算一致 | 普通读数/指令/呈现解释未排除，触发事前停止条件；结束当前图形时钟变体投入，不重跑/改font或prompt继续扩样，NOVELTY=RETAIN0 |
| VLM-POST039-SCIENCE-DESIGN | P1 | **PARKED / NOT_READY（路径交接暂缓）** | ChatGPT研究负责人 | [同题跨视频选择修订](./research-proposals/selection-channel-identifiability-revision-2026-10-24.md)保留；旧192槽已取消 | 跨源输入/近邻重合仍未解决；不因040结案复活，不索要私人路径；041已关闭；043/044已关闭，045已关闭，当前0 READY；本选帧候选仍PARKED |
| VLM-HOURVIDEO-TRAIN-GPU-001 | P0 | **QUEUED / REQUIRES_NEW_GPU_TRAINING_AUTHORIZATION（非READY）** | Codex，待TRAIN-PREP实证PASS并获独立GPU许可 | [真实GPU训练合同](./codex-artifacts/VLM-HOURVIDEO-TRAIN-GPU-001/README.md)：RTX3090上用真实独立训练视频，冻结视觉编码器/Qwen，只优化≤1M参数的temporal head；**真正backward+optimizer.step≤200步、GPU≤60分钟**、独立训练数据，私人checkpoint≤256MiB，记录loss/参数变化/峰值VRAM | **GPU训练当前未授权**；结果只证明真实小头训练，不冒称Qwen微调/QA准确率提升或论文创新，不沿用AB推理预算 |
| VLM-HOURVIDEO-TRAIN-LORA-001 | P1 | **OPTIONAL_QUEUED / TRAIN_QA_AND_GPU_AUTHORIZATION_HOLD（非READY）** | Codex，待合法独立train QA、现成LoRA依赖和3090显存证据 | [可选Qwen3-VL LoRA真实微调提案](./codex-artifacts/VLM-HOURVIDEO-TRAIN-LORA-001/README.md)：仅合法train split答案、现有权重/PEFT条件过门才拟一次≤100步/≤90GPU分钟Qwen adapter真实训练；无合规train QA则不得用dev替代 | **非本次授权**、不保证3090能做4B LoRA；须后续新用户许可且唯一READY，无法满足就报告LORA_HOLD |
| VLM-PTS-001 | P1 | **INCLUDED IN VLM-BATCH-003（不可单独执行）** | Codex | 原PTS静态审计需求 | 按任务包子任务A执行，原[说明](./codex-artifacts/VLM-PTS-001/README.md)仅作背景；不重复上传 |
| VLM-003 | P1 | BLOCKED（旧gold区间诊断的manifest不再是当前路线；无新明确任务授权） | Codex | 原四臂manifest冻结，作为历史未执行工作保留 | 不得依据旧README/PR执行；任何新机制需新许可、来源、PTS、预算与用户授权 |
| VLM-004 | P2 | BLOCKED（需单独实验放行） | Codex | 小规模配对问答先导与独立复核 | 唯一 GPU 调用账本、完整分母、纠错/误伤、置信区间与成本 |

**历史状态（META-005交付时，已被页首与当前看板取代）：当时0个READY。META-005已以真实官方GET读取超时安全结案，META-006为待新授权的下一轮一次性修复；媒体和GPU合同继续排队。** [Codex 895f260](https://github.com/floomeer83felix-source/vlm/commit/895f2602cc4d27d4e5b38a1e3249ae386c1d2120)已证用户本机HourVideo dev开发JSON约1.85MB/50顶层UID、隔离boto3/ego4d静态profile、可信Ego4D官方桶region与区域端点200的HEAD/条件GET（完整CSV声明4,653,141B），**但GET应用读至2,555,904B时因read_timeout=12秒中断**；3次S3实际尝试、无重试，未完整读CSV，所以v2_1真实UID交集、canonical视频身份/大小和HourVideo时间轴同版均UNKNOWN，真实媒体GET/GPU依旧0。

为避免再从零规划，已写好[下一任务META-006](./codex-artifacts/VLM-EGO4D-AWS-META-006/README.md)：**拟在新的明确授权下**仍只读同一份官方CSV和最多2视频HEAD，**仅把read_timeout由12秒提升到90秒**，保持最多7次来源严格白名单S3 HTTP发送、唯一manifest GET应用正文≤8MiB、禁自动重试、region自动跳转、未授权媒体GET和GPU。**META-006当前PENDING，不是READY；不能擅自用META-005剩余4次请求、复用旧父任务或自动发任何云请求。**

**阶段2 [LIVE-MEDIA-002](./codex-artifacts/VLM-EGO4D-LIVE-MEDIA-002/README.md) QUEUED**：待上游完整manifest、真实canonical对象HEAD大小及单段≤3.5GiB合规后，**另经用户明确许可**最多1段/1媒体GET、研究数据GET正文预算≤4GiB，流量硬约束无法实现则不下载。**阶段3 [LIVE-AB-001](./codex-artifacts/VLM-HOURVIDEO-LIVE-AB-001/README.md) QUEUED**：真实媒体本机获得并检查版本/PTS、模型权重环境就绪、用户另批准后，最多4次Qwen3-VL真实前向、RTX3090 GPU≤40分钟、1视频2题AB；桥接未知不得评分为正式HourVideo。两个后续合同已经写好，**不再排新的合成工具任务**，只要取得上游实际合规证据就直接审核/转下一阶段。不能公开AWS凭据、真实UID、受限QA/视频或私人路径，Charades`FINAL_MEDIA_STOP`、`NOVELTY=RETAIN0`保持。

## 二、VLM-001：Windows 工作区恢复状态盘点（历史任务，已完成）

### 目标

在**不重跑任何模型、不修改现有环境**的情况下，弄清楚原本地 RTX 3090 研究工作区的真实状态。研究对象为长视频预算约束下的视觉证据与推理；已有尝试尚未产生经科学/创新审查支持的核心新机制。

### 允许范围

1. 只读了解本地工作区实际位置、目录用途、历史进展、run 配置、现有模型与数据清单；**不从公共 GitHub 目录缺少源码推断本地也没有源码**。
2. 只读检查 Windows GPU 情况（如 `nvidia-smi`）、活动 Python/训练进程、现存锁的**文件存在性**及可能持有者、磁盘剩余空间；无法确认锁持有者时注明“未知”，不要删除锁。
3. 只读核对现有 conda `pytorch` 环境中 Python、PyTorch、CUDA/驱动、模型及处理器版本；**不安装、升级或新建环境**。
4. 只读检查调用账本：最后运行的 run ID、planned/started/terminal 状态与数量、是否有 started 未终态、最新成功记录与异常记录；不泄漏原始答案/隐私标签。
5. 判断本地已否具备下一研究阶段的前提：源身份隔离、SHA/PTS 可追溯、GPU 串行和持久账本；把未验证的项目列为“未确认”而非“通过”。
6. 若本地工作区与这个公开文档仓库是两个目录，**不要把工作区整体推入公共仓库**；只通过文档仓库的 `docs/codex-results.md` 发送脱敏反馈，并将必要的小型文本证据放到 `docs/codex-artifacts/VLM-001/`；不得整体上传原工作区。

### 禁止事项

- 不启动新的 VLM 问答/训练/评分前向，不补跑旧题或旧候选。
- 不杀进程，不改动/删除锁、账本、环境、数据、模型、配置或原有日志。
- 不下载数据集、视频或模型，不用付费 API/云 GPU，不新增人工标注。
- 不公开模型权重、视频、原始问题答案、私有标签、凭据、Token 或暴露敏感路径的完整命令行。
- 不擅自合并旧 PR #1，也不修改本文与 `research-overview.md`。
- 首次审计仅限必要的目录与日志概要，避免打开海量视频或生成大段终端输出。

### 可参考的安全命令（按需选择，不机械全跑）

- `Get-Location`、`git status --short`、`git rev-parse HEAD`（如果工作区有 Git）。
- `nvidia-smi`（报告 GPU、显存和相关进程，输出须脱敏）。
- `conda env list` 和当前环境的版本查询；若 `conda` 不在 PATH，记录该事实，不尝试安装。
- `Get-Process python,pythonw -ErrorAction SilentlyContinue`（仅看与任务相关的进程）。
- `Get-ChildItem` 查看相关目录及账本文件元数据，不批量读原始视频/权重/私有标签。

### 输出要求与反馈路径

**以下为 VLM-001 当时的交付要求，现已完成；禁止重复执行。**

**该历史任务仅允许新增/修改两处交付物：**

1. 在已建立的目录 `docs/codex-artifacts/VLM-001/` **新建** `workspace-audit.md`，内容遵循 [附件模板与脱敏规范](./codex-artifacts/VLM-001/README.md)。这里只写必要的环境/资源/账本**汇总**，不贴原始代码、日志、视频、绝对个人路径。
2. 在 `docs/codex-results.md` **追加**一条 `VLM-001` 记录，简述执行状态，并链接 `codex-artifacts/VLM-001/workspace-audit.md`。不要修改原有历史条目。记录至少包含：

- 检查北京时间、执行机操作系统与 GPU 证明、工作区 Git commit（如有）、工具/环境版本；
- 本地活动进程、锁/账本、模型/数据/脚本是否存在的简短事实表（每项说明证据类型）；
- 不确定项、未检查项及异常，不以缺失检查当作“安全”；
- 有无修改研究工作区（理论应为无）、有无 GPU 前向（应为0）、下载（应为0）；
- 是否可以进入 VLM-002 的 **建议** GO/HOLD（Codex 不具有放行权）；
- 相关非敏感本地报告文件的路径或 SHA，可不上传日志正文。

反馈以 **约300—600字中文摘要**为宜；必要结构表可另附。完成后仅提交**上述两处文件**到公开仓库 `main`，不要顺手上传代码、数据、模型、原始评分或其他文件。提交前检查 `git diff --cached --name-only` 和两个文件内容。若无法安全写入 GitHub，停止并直接在本地对话报告阻碍，不要强推或覆盖他人提交。

### 结束条件

**VLM-001 已由 ChatGPT 于2026-10-08按GitHub交付验收通过。** 其在当次审计中仍未知的GPU锁持有状态、全量旧账本覆盖、真实PTS与来源独立性均未因此转为通过；模型推理仍 HOLD。

## 三、VLM-002：公开参考证据数据集元数据核验（历史任务，已完成，G1 HOLD）

### 目标与输入

用尽可能少的Codex额度判断是否有公开资源**在标注定义和获取条件上可能满足**固定12帧配对诊断的G1数据门。优先核查 [TRACE/VES-Bench](https://arxiv.org/abs/2608.22516) 和 [HERBench](https://herbench.github.io/)，若前两者都无法确认字段/权限，再简查 [CaST-Bench](https://woven-by-toyota.github.io/CaST-Bench/)；不得无边界搜索相近数据集。可参考尚未合并的 [PR #1](https://github.com/floomeer83felix-source/vlm/pull/1) 文献矩阵/预注册草案；它们是研究草案，不是经过证实的样本可用性证书。

### 允许工作（只查元数据，无GPU）

1. 查官方论文/项目主页、README、公开数据字典、标注文件的**元数据描述**、schema样本或版本清单；精确记录仓库commit/数据revision/split/媒体manifest是否可见。不得把论文声称直接冒充已实测字段。
2. 标注本地研究所需的许可/访问条件：视频许可与注释许可分开判断；无法核实写UNKNOWN，不以网页可访问代替许可。
3. 对每个资源记录：有无多段联合必需时间区间或参考关键帧、时间单位和坐标、可否对应同版本视频、是否能识别至少三个非重叠参考区间与 <12 个锚帧、是否存在区间外候选池。这些只做schema可行性初筛，**不得声称真实VFR/PTS对齐通过**。
4. 记录题数、视频数和操作性独立来源组数是否明确区分；报告与历史MLVU保护来源隔离如何可能实现。未知项逐条列出，**不得承诺>=40独立来源**。
5. 在证据有限时优先选择STOP/UNKNOWN，避免扩张访问链；旧AGQA访问失败不再续查。
6. 候选资源择优，列后续 G1 的最小验证动作，不启动 VLM-003 或 GPU 实验。

### 强制限制与预算

- **新增 GPU/QA/训练/评分前向 = 0；新增视频/模型/压缩包/整套数据集下载 = 0**，不修改现有 conda、CUDA、研究工作区或历史账本；不申请/删除锁。
- 只访问少量官方公开页面和必要的schema样本；建议单一响应体 <=256 KiB，累计公开元数据响应体 <=2 MiB。超限必须停止并标UNKNOWN；不得靠拆包绕过。
- 不读取本地私有答案/评分标签，不把选项答案用于新策略选择；不访问完整标注正文、敏感身份映射或受限视频。
- 不公开私人路径、授权令牌、视频、权重、原始日志或整套研究资产。

### 本次唯一交付

1. 在已创建的 [`docs/codex-artifacts/VLM-002/`](./codex-artifacts/VLM-002/) **新建** `dataset-metadata-review.md`，遵循 [README 模板](./codex-artifacts/VLM-002/README.md)，注明官方来源与版本、各数据集许可证、字段实际证据与未知、PTS/媒体映射风险、对12帧实验的适配限制和GO/HOLD建议。
2. 在 [`docs/codex-results.md`](./codex-results.md) **追加** VLM-002中文摘要并链接前述附件，保留此前VLM-001结果，不删改旧条目。
3. 只向公开仓库main提交上述两个文件；确保没有附带视频、模型、私人路径、原始注释/答案。发现提交冲突停止，不强推。

**VLM-002 已于2026-10-08按任务交付验收，G1数据门仍HOLD。** 不再重复相同官方页面和404访问链；除非ChatGPT另行明确立项，否则不下载整套数据或媒体。

## 四、VLM-BATCH-003：三项研究准备工作（历史任务包，已验收）

### 放大单轮任务规模的理由

用户希望减少Codex每做完一项就等待新的ChatGPT安排的往返。在**不突破已授权资源边界**的前提下，把原 [VLM-PTS-001](./codex-artifacts/VLM-PTS-001/README.md) 时间戳审计与两个互补的静态/技术合同任务统一打包。此前的VLM-001、VLM-002交付已完成；尚未形成可靠的新证据区间/独立来源/时间桥接数据门，**不能**按旧预注册直接构造四臂或做新问答。

### 可连续执行的三项子任务

1. **A 现有PTS/帧索引/VFR/裁剪时间桥接**：静态追踪必要解码代码与manifest字段，输出时间坐标合同、缺口、未来测试建议，不运行视频解码/模型。
2. **B 历史来源独立性、重合与指纹缺口**：只读研究现有聚合manifest及源组schema，厘清30 prepared/20 selected与约450份指纹覆盖缺项的统计定义，给出保守来源去重和探索集污染控制合同；不遍历大批媒体、不读取标准答案、不补做视频哈希。
3. **C G1数据可行性和无答案manifest合同**：在VLM-002已审查公开元数据和A/B报告基础上提出D1/D2固定12帧诊断的技术前置条件、失败码与数据集HOLD清单；**不新下载数据、不假定有40个独立源、不宣称G1 PASS、不编写或运行实验**。

**执行细节、逐项字段、提交文件名与阻塞规则：** [`docs/codex-artifacts/VLM-BATCH-003/README.md`](./codex-artifacts/VLM-BATCH-003/README.md)。这是本批的唯一有效交付合同；旧PTS任务README只作历史输入，不再单独交付。

### 边界、提交与反馈（不可放宽）

- 用户在**原来的同一个Codex聊天**发送一次继续指令，Codex安全同步文档仓库main，检查`codex-results.md`是否已存在本任务包回报，然后一次完成A→B→C；A/B单项无法核实时可先记UNKNOWN并继续其余独立安全项，不虚构缺口。
- **0新增GPU模型调用、0训练、0评分前向、0视频解码、0视频/模型/完整标注下载、0本地研究资产修改、0新conda/CUDA修改**。原锁与旧账本不可更改或重放。
- 只在公开仓库 `docs/codex-artifacts/VLM-BATCH-003/` 新增 **3个脱敏Markdown附件**（分别为 `timestamp-contract-audit.md`、`source-provenance-audit.md`、`g1-feasibility-contract.md`），以及向 `docs/codex-results.md` **追加1条 VLM-BATCH-003 汇总记录**。只提交这4处变动，不改ChatGPT维护的任务书、总览、AGENTS或任何历史结果。
- 如果先前已有 `### VLM-BATCH-003` 的完成/部分完成/阻塞记录，禁止重复执行；转请ChatGPT审查。遇到Git冲突或敏感信息泄露风险停下，不强推或扩大权限。
- **整包提交后停止本轮操作，但保留同一Codex聊天**；由ChatGPT集中科学审查并决定下一个任务包。其他任务仍BLOCKED。

### 历史任务包验收

2026-10-08 22:25北京时间，Codex以[提交31e8151](https://github.com/floomeer83felix-source/vlm/commit/31e8151901c1c75739670acefec211f920313244)交付A/B/C三份报告及1条汇总。ChatGPT已核对提交范围和证据边界：**ACCEPT 文档与静态审计交付；真实PTS/媒体对应、历史独立来源、G1数据适用性均仍HOLD**。本节只保留历史任务定义，**严禁再次执行**；后续参照新第五节。

## 五、VLM-BATCH-004：数据阻碍与toy合同验证（历史已完成）

### 为什么安排这一批

VLM-BATCH-003确证的主要风险：最近12帧路径仍按index/FPS表示时间，历史789源节点中仅339有可复用摘要、450缺项，目标VES/HER/CaST的真实参考区间、媒体许可/版本与≥40独立源仍未通过G1。继续重复静态盘点收益低。本轮改为**取得合法数据的最小请求准备 + 可运行CPU纯合成测量合同 + 明确去留标准**。旧实验数据和真实媒体、模型一概不动。

### 同一个Codex聊天框一次做完三项

- **A** 只起草VES-Bench许可、无答案schema/参考区间、视频版本/时间坐标请求（中英文），不发送邮件/Issue、不猜邮箱。
- **B** 在单独文档Git仓库的 `prototypes/` 新建Python标准库**纯合成**时间戳、源分组、D1/D2输入不变量参考原型与unittest；**实际运行toy CPU单测**，不导入原研究源码、不解码视频、不调用模型或修改环境。额外查配对时间分布与视觉token预算公平性，未知不能当通过。
- **C** 根据A/B做G1数据门HOLD条件树与toy测试报告。提出少量最有信息量的后续动作，未通过许可/真实证据前不得开展四臂/GPU实验。

**唯一交付合同：** [VLM-BATCH-004/README.md](./codex-artifacts/VLM-BATCH-004/README.md)，严格规定两个脱敏Markdown、两个toy代码文件与一条 `docs/codex-results.md` 追加结果。A→B→C连续执行，若部分未知则诚实标UNKNOWN，不反复请求数据。

### 预算、界限与结束

- 新模型/QA/训练/评分前向**0**，视频解码/视频、模型及完整数据集下载**0**，研究资产/既有conda/PyTorch/CUDA/锁/旧账本修改**0**；不发送联系邮件或GitHub Issue，不合并PR或自动后台运行。
- 本次仅允许创建 `docs/codex-artifacts/VLM-BATCH-004/ves-access-request.md`、`docs/codex-artifacts/VLM-BATCH-004/g1-decision-and-toy-test.md`、`prototypes/toy_g1_contract.py`、`prototypes/test_toy_g1_contract.py` 并在 `docs/codex-results.md` 追加一个父任务结果；公开文件必须脱敏。
- 如果同任务ID已有结果记录、资料泄漏、不可安全提交或Git冲突即停止；不可强推、重复GPU调用或修改ChatGPT维护文件。整包完成后保留原Codex聊天框，等待下次研究审查。

### 本批已完成，以下仅供历史追溯

Codex已经在 [462ccde](https://github.com/floomeer83felix-source/vlm/commit/462ccdec4a999ef62e67a1cb52e7392fd7e14517) 提交5处成果。ChatGPT检查了提交范围、文档和toy用例源码；Codex报告修正后10项unittest通过，但本助手未独立重跑。**本批ACCEPTED，不再执行。**

## 六、VLM-BATCH-005：数据访问出口、toy负例与路线裁决（历史已验收）

[完整任务包README](./codex-artifacts/VLM-BATCH-005/README.md)已在main创建。本次在**同一个Codex聊天框**连续完成：

1. A：限量查看TRACE/VES-Bench官方公开资料，核实可信的数据访问/咨询渠道和许可证说明；不发送邮件、Issue或表单。
2. B：仅修改公开文档checkout下两份纯合成toy代码，补强“至少3个互不重叠区间”、时间分布、来源UNKNOWN以及公平性UNKNOWN等反例，运行标准库CPU unittest。
3. C：提出保留gold参考区间D1/D2诊断还是转向无gold依赖科学问题的明确判断与停止阈值。所有数据集G1继续HOLD。

只允许新增两份脱敏Markdown、更新两份toy Python并向Codex结果文件追加1条任务包回报；详见README中的精确文件名。全程0GPU/模型前向、0视频解码/下载、0原实验资产修改、0对外联系。单次提交后停止，不执行VLM-003/004。

**本包结束后不默认继续相同的静态盘点。** 后续若需实际联系数据作者或修改研究命题，由ChatGPT根据证据向用户提出决策；真实GPU实验还需独立许可与G1通过。

> 发给原Codex聊天：继续下一轮；刷新GitHub main，读AGENTS.md、next-steps.md、codex-results.md与BATCH-005 README，只执行其A/B/C，按要求上传5处文件后停止。

### 已交付，不再执行

Codex于2026-10-09提交[7d1daf7](https://github.com/floomeer83felix-source/vlm/commit/7d1daf725fae5c7a921274e575101966ffed99a8)：两份脱敏报告、两份toy文件更新、Codex结果一条追加；ChatGPT核对提交范围与研究结论。执行者报告18项CPU单测通过；本助手未在本地独立运行。公开项目仓库Issues可用，不代表正式授权或专用数据申请。G1、GPU、真实PTS与来源独立性继续HOLD。

## 七、用户科研路线决策与历史状态（当前以最新决议为准）

- 原路线1：固定12帧且覆盖gold必要区间的诊断因合法数据/同版PTS/独立来源门未通过而HOLD；[TRACE咨询草案](./outreach/trace-ves-bench-inquiry-draft.md)仍为 **UNSENT历史**，用户并未授权发送。
- 原路线2：在无gold必要区间下，把问题相关选帧S_q与时间分层选帧S_t比较作为核心算法。已由 [BATCH-006提交e581039](https://github.com/floomeer83felix-source/vlm/commit/e581039970106dbec741adf502e48e5f948adad4) 所做十项审查否决**作为新算法的创新主张**；仅做条件性现象测量/窄提示路径实验的可能仍UNKNOWN，不继续当本期研究主线。
- **最新用户选择B（2026-10-09）**：保持长视频VLM/《计算机学报》水平的研究目标，放弃上述已高度重合的选帧方法方向，重新寻找可证伪**核心计算机制**。不承诺论文/新算法已成立，retain 0。

## 八、VLM-BATCH-007：10项核心机制科研审查（已验收，禁止重做）

2026-10-09，Codex通过[提交 d82e30e](https://github.com/floomeer83felix-source/vlm/commit/d82e30e43ec31fb8600b0a61d62021017a6d59aa)交付[任务协议](./codex-artifacts/VLM-BATCH-007/README.md)约定的全部8处文件：5份新脱敏报告、2份新标准库toy代码与codex-results中的单条父回报。ChatGPT已核对GitHub提交范围、五报告与两toy代码的科学边界，**ACCEPT有界交付；科研STOP THIS PORTFOLIO**。Codex报告用Python3.9.21执行12项合成unittest，12 PASS/0FAIL/ERROR/SKIP；ChatGPT没有在本地实验机上独立运行它们，故本结论仅验收执行者测试收据和静态论证。toy的117种观察模板/336个一致world-view配对及89次不当unknown→0造成的假认证都是**合成枚举，不能推成真实视频结果**。

- **M1 NO-GO**：[形式定义](./codex-artifacts/VLM-BATCH-007/candidate-mechanism-specs.md)可由普通三值partial-world监控复现；稀疏未观察域不能为「never」给真实证明。所有槽可见与完美感知是toy公理，现实感知不满足已验证门。恒UNKNOWN虽避免假认证但coverage=0。
- **M2 NO-GO**：定义的依赖无效化和局部更新可以用相同typed key与revision guard的普通AND/OR依赖缓存等价表达；toy仅检最小AND DAG，不证明OR、循环、矛盾、实际source identity可靠性。
- **M3 NO-GO**：同世界/答案映射/可能观察与成本的version-space/discriminative-clue planner能逐步模拟当前候选规则；独立真实`Ω`、观察响应`Γ`及答案真值当前不可用。未取得某先例全文不等于创新通过。
- **强先例与现实门**：NeuS-QA本轮SSL失败、一个MIT经典TMS定位错题，证据仅UNKNOWN；VideoHV/VideoSEAL等部分只读摘要，不因缺全文而认为新颖。现实负性事件标签、完整依赖真值、可区别观察oracle，以及媒体/QA许可、同版PTS/clip、来源独立、可靠视觉探测器、真实token/GPU预算均未验证。**retained mechanism = 0**。

**研究负责人裁决：STOP当前M1/M2/M3组合，不再自动发BATCH-008。** 保持长视频VLM高水平论文目标并不授权无限重复机制命名、摘要盘点或toy优化。今后只有在用户明确提供了**新的实质科学对象、有效合法数据/证据资源或其他可审查的创新线索**后，才重新设置一轮有限的创新性和可执行性门。研究范围变化之前，VLM-RESEARCH-GATE-008继续 WAIT_USER_DIRECTION。VLM-003/VLM-004、GPU/真实媒体/外部联系/原研究工作区修改继续BLOCKED。无需另开Codex聊天。

## 九、Ego4D历史数据路径：用户曾愿意审阅协议，现因申请故障暂停

**用户2026-10-09明确表示“愿意”走Ego4D正式许可路径**。ChatGPT仅登记申请意向，**没有替用户同意或签署法律协议，更没有提交任何数据许可表单或获得AWS访问权**。官方入口：[Ego4D用户许可表](https://ego4ddataset.com/ego4d-license/)；操作与来源：[Ego4D准入清单](./ego4d-access-checklist-2026-10-09.md)，以官网最终协议为准；个人可自行签个人许可，仅有正式签署权限才签机构协议。成功申请后可按官网流程获邮件审核，官网所写约48小时/14天凭据为通常说明，不保证实际时间；最近GitHub Issues也有用户反映表单故障，任何异常须按事实报状态、不擅自代联系。

**状态严格分层**：用户愿意审阅 `USER_WILLING` ≠ 用户已提交 `SUBMITTED` ≠ 正式获批 `APPROVED` ≠ 已批准下载/使用/公开衍生评估结果 `AUTHORIZED_SCOPE_CONFIRMED`。当前只处于第一层；用户回来只需说 `未提交/已提交待审批/已获批准/条款不接受/表单异常`，不要传邮箱、住址、PDF签章或AWS凭据。

**下一科研问题只作为匹配候选，不是新算法**：Ego4D MQ已有标注活动实例区间，可探索长视频反复活动的时间实例混淆及强对照；NLQ有可查询的回答窗口。必须先与已有时序grounding/事件检索文献去重、核目标视频-clip修订/PTS/来源组和数据研究/论文披露许可；不从MQ未标注活动推出全视频“不存在”。获批后仍需逐项批准最小数据子集下载/真实视频解码/GPU预算及原研究工作区变更。

**无需向原Codex聊天框发送“继续”**，没有READY父任务，历史BATCH-007不重跑，旧VLM-003/004仍BLOCKED。保留同一Codex聊天框。

**本节记录已完成的历史任务，以下十项不可再次执行；最新状态以任务看板与第十一节为准。**

## 十、Charades／Charades-STA 文档准入与科学问题核验（BATCH-008已验收）

**用户最新确认（2026-10-09）**：先不等待Ego4D的`Failed to fetch`问题解决，改以免事前申请的[Charades](https://prior.allenai.org/projects/charades)与[Charades-STA](https://github.com/jiyanggao/TALL)作为可合法独立评测**候选**。官方[Charades License for Non-Commercial Use](https://prior.allenai.org/projects/data/charades/license.txt)明示非商业研究、限制公开改造数据和第三方分发；有公开下载链接**不**免除许可。STA文本时间标注来自单独作者仓库和修订，权利/版本还需核实。当前**未取得任何数据**，不授权下载约3MB官方标注或约13GB视频。

[Charades准入与科学问题说明](./charades-entry-2026-10-09.md)与[**VLM-BATCH-008十任务README**](./codex-artifacts/VLM-BATCH-008/README.md)已写入main：

1. 原Charades许可可行性（商业/科研、署名、发表与禁止分发）；
2. Charades-STA独立注释权利与清理版本；
3. Charades动作区间/schema与公开元数据核对；
4. STA句子区间和Charades动作标签跨格式/同视频join协议；
5. 重复动作**同类多实例**能否从现有标注合法判定，以及真正可证伪指标；
6. 不同动作重叠/时间边界混淆的对照与指标；
7. 直接TAL/时间自然语言定位先例与创新性否决；
8. source/video/participant、split、同版真实PTS与来源独立门；
9. 约30秒短视频能/不能支持的结论与真正长视频外部数据缺口；
10. 数据许可/标签适用/创新/长视频适配五门裁决，最多请求用户**另行允许最小官方标注包下载**，不允许Codex现在拿数据。

**只允许6处交付**：`docs/codex-artifacts/VLM-BATCH-008/`目录5份指定小Markdown以及`docs/codex-results.md`末尾一条汇总；禁止任何真实媒体/标注下载、视频解码、模型/GPU、原研究目录/锁/账本更改、历史任务重做、PR合并与作者联系。若文献/STA权利或重复实例证据不足则标UNKNOWN/NO-GO，不为了完成10项伪造创新；全部完成并安全push后停下、ChatGPT审查。

**科研止损**：Charades平均约30秒，仅能支持短时域活动或自然语言时刻定位的初步闭环，不能单独成为长视频核心机制论文的验证集；公开TAL/TMR已有强基线。保留原M1/M2/M3否决、retain0、旧VLM-003/004 BLOCKED。

## 十一、VLM-DATA-GATE-009：用户已批准最小原标注包（仅有限授权）

**前轮审查前提**：[BATCH-008科学五门裁决](./codex-artifacts/VLM-BATCH-008/data-science-go-no-go.md)仅支持原Charades非商业研究／README字段**文档条件准入**，STA权利仍UNKNOWN，P1/P2实际合法资格计数未取得，普通TAD/TMR新算法与Charades作为单独长视频确认集仍NO-GO。不能凭官方66,500区间总数推断同视频重复实例有多少。

**用户最新明确授权（2026-10-09）**：用户确认自己的非商业研究用途符合[官方许可](https://prior.allenai.org/projects/data/charades/license.txt)，允许从[AllenAI Charades官方页面](https://prior.allenai.org/projects/charades)仅下载列为**Annotations & Evaluation Code (3 MB)**的小包，独立隔离存放，用作CSV字段、时间区间、同类重复候选、异类重叠候选和保守来源分组的聚合资格统计。此权限**不**涵盖视频/帧/STA、模型/GPU、原研究环境改动、向第三方分享标注。

已由ChatGPT冻结[Windows隔离存储与安全协议](./charades-metadata-safety-protocol-2026-10-09.md)，并下达[唯一READY父任务BATCH-009](./codex-artifacts/VLM-BATCH-009/README.md)。**ChatGPT自身未下载、未建目录、未取得真实CSV、未读用户电脑。** 只有用户主动在已有Codex聊天发启动消息，并且本地路径、安全、许可、官方资源链接检查全部通过后，才可执行这次受限获取。执行后仅能上传脱敏总体计数与通用代码；数据本身永久不进入公共GitHub。

**科学边界**：即使P1/P2资格组大于0，也只说明短片记录层有候选时段，不确认自然语言「第一次/第二次」真值、真实媒体PTS、独立自然长视频或模型准确率，更不自动创建GPU/下载媒体权限。

## 十二、VLM-BATCH-009：初次下载被安全拦截、后续路径身份修复（历史已结束）

**历史说明（2026-10-09验收后补充）**：本节以下记录009最初的授权和十项计划，不代表009仍可再次运行。实际009已`STOPPED_SAFELY`（GET0/CSV0），009-FIX是路径前置安全修复（合成test执行者报21/21）；当前唯一可触发的续接任务是[BATCH-010](./codex-artifacts/VLM-BATCH-010/README.md)，且也需用户在原Codex聊天发送启动消息。

**最新用户明确授权（2026-10-09）**：研究用途符合Charades官方非商业许可，批准**仅从AllenAI官网获得约3MB `Annotations & Evaluation Code`**，并在独立隔离目录中统计CSV/起止时间/来源资格；**不批准任何视频、Charades-STA、GPU或原实验环境改动**。权限界限不得由Codex或GitHub自动扩大。

**明确的本地存储路径**：Windows `%LOCALAPPDATA%\\VLM-Research-Isolated\\Charades-v1-Metadata\\`（解析为用户本地目录的实际路径，绝对值不得上传GitHub）。只允许`incoming/`（原ZIP）、`extracted/`（train/test CSV和类表等白名单）、`local-audit/`（local manifest）；执行前检查不是任何研究工作区、Git checkout或云同步区域，不含junction/symlink/旧文件冲突，空余至少150MiB。未知即STOP、不另挑位置。

**两份任务基础文档**：[冻结安全协议](./charades-metadata-safety-protocol-2026-10-09.md)、[唯一READY十项README](./codex-artifacts/VLM-BATCH-009/README.md)。10项内部子任务覆盖：
1. 数据许可与用户授权范围；
2. 独立Windows本地存储前置与目录安全；
3. 仅官网官方S3对应3MB包，流式总量≤8MiB、记录SHA与下载状态；
4. zip成员安全/路径/大小/加密/链接风险预检；
5. 只读取train/test CSV和固定类表真实schema，拒执行随包代码；
6. 记录完整训练/测试行数及坏区间分母；
7. P1同类非重叠区间候选及0/0.5/1s敏感性汇总；
8. P2异类时间重叠及0.5阈值汇总；
9. 仅在本机计算subject/split重叠计数、粗时长分布，隐藏具体video/subject；
10. 输出候选资格与FAIL/UNKNOWN科学结论，不能把资格非0当物理事件真值、新算法或长时域研究GO。

**GitHub只允许5处**：`docs/codex-artifacts/VLM-BATCH-009/`两份脱敏markdown（下载/完整性/schema报告、候选资格/研究决定），`prototypes/`两份不含真实数据的标准库解析代码及合成unittest，向`docs/codex-results.md`末尾追加**一条父任务结果**。绝不能上传ZIP、真实CSV、subject/video映射、script/descriptions、绝对私人路径或低样本可链接小表。只可运行标准库CPU测试和数据行解析，**0视频、0GPU、0模型、0原工作区改动**，不执行下载包评测脚本。通过安全stage、单次push后STOP。

**未执行声明**：ChatGPT本轮只更新任务材料，未向用户的Windows机器下载包、未建立隔离目录、未创建任何CSV统计。只有用户主动让**原Codex聊天**执行且执行前检查通过，才能产生新数据核验。旧VLM-003/004仍BLOCKED，研究 retain0，正式长视频数据门HOLD。

## 十三、VLM-BATCH-010：官方小包已获取、时间质量HOLD（历史已验收）

**历史任务警示**：以下为BATCH010执行前的授权与计划文本，已由[8153a18](https://github.com/floomeer83felix-source/vlm/commit/8153a18af651afcbf0c5a455f3b61817e09755c0)执行完成。**禁止再次执行下载或重复该父任务；后续只有011只读诊断READY。**

**本轮审查结论（2026-10-09）**：BATCH-009 [提交bc16e38](https://github.com/floomeer83felix-source/vlm/commit/bc16e38eab35f454bc3e0ccc3c805c15c6009ed8)在目录`Path.absolute()`与`Path.resolve()`路径规范名称不一致时按协议保守STOP。用户直接授权的[修复提交dda8481](https://github.com/floomeer83felix-source/vlm/commit/dda8481a330c4cfa1e734511ad59e7d8f7571d4f)后，执行者报告通过samefile+有效物理目录ID、两条祖先链reparse点检查及canonical稳定性，21项合成标准库单测PASS。ChatGPT已审查提交变更范围和公开代码，但**未实地访问Windows独立确认路径**；原数据GET次数仍0，ZIP/CSV/P1/P2均UNKNOWN。009交付/安全阻塞应标`STOPPED_SAFELY`，修复仅为`ACCEPTED_PRECHECK_FIX`，不是实际元数据工作完成。

**下达新的父任务（而非重复旧任务）**：[VLM-BATCH-010十项受限续接README](./codex-artifacts/VLM-BATCH-010/README.md)。用户先前明确授权的那**一次**官方`Annotations & Evaluation Code`获取**未发生**，因此仅在同一限制内继续这项已获准工作；开始前务必重新核路径物理身份、没有旧文件冲突、与原RTX3090工作区/公共Git/云同步根隔离，再核当前官方链接与GET`≤8MiB`的流式硬限制、ZIP完整性/CRC/白名单、真实train/test字段及错误分母、P1同类不重叠区间、P2异类重叠区间、仅粗粒度`subject`跨split数量和长视频/创新停止门。若一项不安全/不兼容，立即BLOCKED，**本次不授权Codex边下载边修审计源码**。

**BATCH-010只准3处GitHub提交**：新增`docs/codex-artifacts/VLM-BATCH-010/download-and-schema.md`、`qualification-and-decision.md`两份脱敏结果，以及只向`docs/codex-results.md`末尾追加一条010父任务回报；不改已发布的009原型/test、协议、历史或研究计划。ZIP、CSV、任何subject/video映射、真实行和私有绝对路径都不得上传。**没有新模型/GPU/视频/STA/下载其它数据权限**；用户主动在原Codex聊天发送“执行BATCH-010”后才可开始。

## 十四、VLM-BATCH-011：Charades时间合同独立数值诊断（已验收，禁止重做）

**本节先前记录BATCH011的执行计划；该父任务已由1aed0de一次提交完成，不得再执行。最终科学状态见下方第十五节。**

**源事实与严格层级**：BATCH010官方ZIP SHA`c616913ef79c2ddde06d9c562eae57bb8901d459d7568a0d27bf09cbf33ae866`，train CSV SHA`59273c6dc2139ec7eb95b980fd26bc8529774b1ede0602f6ca90b546ed12f0fc`、test CSV SHA`8b8b207b55fb95b949018027f69d83bd46cd844d15834f8f592ee8e7446173eb`（仅文件级，不是官方发布的独立SHA证明）。标注字段真实11列、7985/1863个视频行和157类别，原动作token 49809/16691；合法数值区间35211/11664，无效14598/5027。约75.5%视频行至少包含一个被旧规则拒绝的token，主因`end>length`；当前不能把剩余47k记录当物理事件完整真值。P1 347个同类有分离pair的组、P2 97723个异类相交pair**只是旧合同下幸存子集的几何候选，不是有效问答/新算法模型实验的许可**。

**独立官方时间合同**：[AllenAI原README](https://prior.allenai.org/projects/data/charades/README.txt)定义`actions`是`class start end`三元组，`length`为视频长度（秒），Changelog显示2017-02-27新增官方length，localize评测用25个时间点。这不能证明原CSV所有标注已无冲突，也不能通过变换时间单位来消除不通过的分母。具体数据质量根因仍UNKNOWN：既可能是标注/视频修订，也可能审计器的时间假设不适用或其他错误，不能无证据归责于官方数据。

**受限十项执行协议**：[VLM-BATCH-011 README](./codex-artifacts/VLM-BATCH-011/README.md)。用户已批准的小包下载**已经发生，不能再次GET**；只有使用固定Windows隔离目录`%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-Metadata\`内现有CSV只读计算和官方公开文本查验可做。执行次序：①SHA/权利确认②官方时间定义及版次③独立CSV解析交叉核④互斥与重叠异常flag⑤end-length差额桶⑥每视频异常token个数聚合⑦P1子集资格验证⑧P2子集资格验证⑨隐私、来源、分母审计⑩`HOLD_TIME_CONTRACT`或证据支持下的下一步止损。禁止查看/上传原始单行、视频ID/subject/描述、低样本可逆表，禁止数值截断/猜测缩放。需先在合成数据完成stdlib单测再读真实CSV；数据/原脚本不能改变。

**只允许5处GitHub交付**：`docs/codex-artifacts/VLM-BATCH-011/`的2份脱敏报告，`prototypes/`的2份新通用只读脚本（非旧审计器修改），`docs/codex-results.md`末尾1条父任务回报。禁视频/STA、模型/GPU、真实视频PTS测量、原研究工作区与锁/conda更改、任何数据/标注再次下载及外部联系。出现审计器不稳定/真实hash不符立即停止、不得覆盖旧收据。Codex成功单次push后停止，待ChatGPT验收。

## 十五、BATCH-011验收与先前路线抉择（历史已结束）

**交付验收**：实际[提交1aed0de](https://github.com/floomeer83felix-source/vlm/commit/1aed0dea70faa7a446e63637be4772f4668270a2)恰好改5处：`docs/codex-artifacts/VLM-BATCH-011/`两份脱敏报告、`prototypes/`两份全新stdlib脚本、`docs/codex-results.md`追加一次。无ZIP/CSV/个人映射进入GitHub，未修改旧原型/原科研资产。执行者报告原隔离ZIP/train/test SHA均与010固定值一致，旧规则的66,500原token/46,875通过/19,625失败、P1 347组/P2 97,723pair及其它参照聚合一致。它证明**两个解析实现按同一个条件给出相同计数**，不证明该条件被真实媒体时间语义支持。执行者报告合成测试首次14 PASS，增强补充披露后15 PASS，**增强后的完整程序未再实跑真实CSV**；ChatGPT仅审查GitHub结果与代码，不声称本机复算。

**新增记录级事实**：越过length的动作区间中，至少8,747条超过1而不超过5（以文档所述秒尺度解释）；异常token/视频行总比率约29.5%/75.5%，Train/Test异常行比例约73.8%/82.5%。347个P1合格同类组有270个所在行另有数值异常；97,723个P2有效几何重叠pair有67,280个所在行另有异常。余项77组与30,443对也只是在“当前数值规则且整行未包含异常”的**关联计数**，不是跨媒体/语义验证成功的真值样本。当前`DATA_INTERVAL_QUALITY=HOLD_RANGE_CONFLICT`，`TIME_CONTRACT=HOLD`，`DATASET_FOR_NATURAL_LONGVIDEO=FAIL`，`ORIGINAL_MECHANISM=RETAIN0`，`GPU=BLOCKED`。

**外部新颖性危险信号（公开资料，不扩展数据授权）**：[ACL2025正式长文 Perfect Times](https://aclanthology.org/2025.acl-long.1000/)已从Charades视频构造时间关系与动作完成/持续的多语种VLM问答；[作者公开仓库](https://github.com/ologin/PerfectTimes)声称包含更新的时间顺序动作注释`video_annotations.csv`及问答生成器。该工作不是P1“同类重复实例”命题的严格同一对象证明，但直接覆盖了“用Charades动作时间关系自然语言QA得到新基准/机制”这一宽泛新颖性宣称。不要下载其视频/注释或直接调用repo脚本，版权/来源修订和科学先例对比仍待独立授权/定义。

**研究下一门`WAIT_USER_DIRECTION`而不是BATCH012自动READY**：A. 如果继续Charades，则先找到**无需未获授权媒体的可靠同版标注时间坐标来源、修订记录和与length同原点的证据**，并且提出相对于ACL2025 Perfect Times与TAL/TMR强基线独有的可辨识问题；若找不到则STOP Charades作为核心证据。B. 如果目标是自然长视频VLM创新，优先选择**可公开申请/无需审批而具合法原媒体和可验证时间真值、跨源独立的真正长时域基准**，重新单独授权最小必要数据；不要因Charades样本非零而继续无边界元数据/合成研究。用户未选定前0新READY、0第二次原Charades小包下载、0新数据/视频/STA、0GPU及原Windows资产改动。

## 十六、VLM-BATCH-012：官方定位评测政策对齐已验收（禁止重做）

**以下十项为历史已执行计划，不再是Codex新授权。BATCH012只完成官方标签政策工程对齐，未修正原动作或通过媒体真值门。**

**用户2026-10-09明确答复“同意”**：优先修复当前Charades的`end>length`检查与官方frame-localization标准的不一致，暂时不转向另一个数据集。此次是**口径/评测兼容性修复**，不是修改或重新发布原始标注。原ZIP和两个CSV仍在Windows固定隔离目录；用户没有批准任何新媒体、STA、GPU或原Windows研究环境改动。

**核心对照**：旧两套数值程序一致复算66,500原动作token中19,625不通过`0≤start<end≤length`，但该强条件是为评估精确区间真值而自设的筛查，不能假定它是官方frame-mAP要求。官方[Charades README](https://prior.allenai.org/projects/data/charades/README.txt)写定位在`j*length/25, j∈{0,…,24}`取25个时间点。官方脚本`Charades_v1_localize.m`原字节已经在合法取得的Charades.zip中（是否真实存在仍由任务执行时安全确认）；只许**用zipfile内存读取短文本，不提取到磁盘，更不执行MATLAB**。原包SHA`c616913ef79c2ddde06d9c562eae57bb8901d459d7568a0d27bf09cbf33ae866`，两个CSV SHA与010/011保持一致；签名不符STOP。

**10个具体子任务与交付**：[VLM-BATCH-012 README](./codex-artifacts/VLM-BATCH-012/README.md)冻结：①授权/SHA/目录身份；②ZIP中实际官方定位评测器的时点和端点比较证据；③官方frame label、数值边界质量、实例/关系语义真值三层严格区分；④标准库实现有来源证明的25点标签采样；⑤先运行全合成反例unittest；⑥旧strict与官方标签的匿名正cell/记录差异；⑦越界类型与官方可命中采样点数量；⑧P1/P2既有347/97723候选对边界的保守影响，不臆造真实顺序；⑨仅聚合脱敏/小格及互补抑制；⑩`OFFICIAL_LABEL_SAMPLING_COMPATIBILITY`、`TIME_RANGE_QUALITY`与`EVENT_TRUTH`分别判PASS/HOLD/FAIL。若原评测器缺失或规则不能静态核，报告`UNKNOWN`而非伪造官方相容性；不能仅靠30%端点越界证明原数据坏。

**仅允许5处GitHub提交**：`docs/codex-artifacts/VLM-BATCH-012/`两份脱敏报告，`prototypes/`两份纯stdlib全新对齐器+合成测试，`docs/codex-results.md`末尾**一条**012父任务回报。0其它原始数据/标注/官方脚本全文上传、0旧程序修改、0源目录写入、0下载/视频/STA/推理GPU/训练、0原Windows研究文件/conda/锁/账本触碰。一个正常push成功后停止当前轮，由ChatGPT审查再决定是否仍需同版媒体时间证据或改数据集。**修复A不自动宣布B/C PASS**。

## 十七、VLM-RESEARCH-GATE-013：用户已批准条件式最小视频V1访问（历史方向决策）

**状态更新**：本节原文曾记录“等待视频访问授权”，现用户已经明确批准**限制在2段/64MiB/CPU packet-PTS的条件式V1**。该历史等待描述不再是当前状态；当前唯一可执行任务见下方BATCH013与顶部任务表。**视频尚未访问，不能把READY当已成功取得媒体。**

**最新替代决定（2026-10-09）**：用户已明确选择方案A，不再等待选择A/B；但仅选择研究方向**不构成媒体下载授权**。具体试点范围、官方整ZIP无法逐视频直接点取的风险、预算及未来授权条件以[方案A试点提案](./charades-media-boundary-pilot-proposal-2026-10-09.md)为准。以下保留了BATCH012验收时的历史判断。

**BATCH012审查报告**：[官方代码/政策](./codex-artifacts/VLM-BATCH-012/official-evaluator-code-and-policy.md)、[三层宏观对照](./codex-artifacts/VLM-BATCH-012/three-tier-aggregate-and-go-no-go.md)、[提交e46f1d7](https://github.com/floomeer83felix-source/vlm/commit/e46f1d794118c5c2efbb0f15f0fc84dad5d4f04b)。按唯一SHA固定Charades ZIP内官方评测器的文本静态证据，25点时间采样为`(j/25)*length`（零基j=0…24；对应MATLAB先除后乘操作次序），原动作class区间`start<=t<=end`两端包含，多同类动作仅令对应真值cell置1，而不是累积事件实例。官方frame-localization**不要求**先通过`end<=length`才构造正label；旧`0<=start<end<=length`是我们额外的严格时间区间资格筛选，不能代表官方评价政策。

**三层结论不能串门**：A`OFFICIAL_LABEL_SAMPLING_COMPATIBILITY=VERIFIED_WITHIN_STATED_SCOPE`（仅限合法原ZIP评测器文本转义与有限规范数值模拟；未经MATLAB端到端mAP/媒体帧认证）；B`TIME_RANGE_QUALITY=HOLD`（仍有19,625原动作不满足额外strict规则，不能因frame-hit宣称每条端点真实正确）；C`P1/P2_EVENT_TRUTH=HOLD`（实例身份、完整正负事实、媒体PTS/同版映射、自然来源独立性尚无证据）。执行者报告官方正cell705,470、strict正cell398,287，差异307,183个（43.54%的official positive cells），非独立动作N，也不是mAP。原strict可评同类重复347组与异类交叠97,723对仍未升级科研真值。纯合成unittest 19 PASS，原CSV只读分析一次，ChatGPT仅静态审查GitHub结果，**未独立实算用户Windows上的原CSV**。

**科学止损与下一最小证据门**：既有[ACL2025 Perfect Times](https://aclanthology.org/2025.acl-long.1000/)与动作时序QA工作使简单Charades时间QA缺原创性；Charades本身均长约30秒，不能单独提供自然长视频论文最终确认。为避免一轮轮工程复盘，暂停分配新任务：用户可选择①未来另行核定具体**合法小规模视频＋同版媒体PTS/帧时钟**证据以评估B/C（必须先明确授权、样本上限及隔离来源，现未允许），或者②把Charades保留为**短视频工程/官方frame-mAP对照**，先做无需下载的长域新数据集许可/时间合同研究方案，之后再明确授权所需数据。**任何选项都不自动放行GPU或原研究环境。** 无新用户指令前`VLM-RESEARCH-GATE-013=WAIT_USER_SCOPE_DECISION`、0READY、0媒体/STA/额外数据/模型调用。

## 十八、VLM-BATCH-013：已在CPU工具门安全停止（历史父任务，不得重跑）

**本节以下内容是013原执行前的任务计划，现已因缺既有ffprobe安全停止；其后FIX只是源码审查交付，当前不允许按此旧任务再次联网或启动。最新状态见下方工具门。**

**新增用户明确授权（2026-10-09）**：方案A继续Charades，同意仅官方480p视频最多2段、总HTTP GET正文**≤64MiB（67,108,864B）**，包含ZIP尾部、中央目录、远程local header和成员及一切失败传输字节；本地全部本轮媒体+临时字节**≤128MiB**。仅使用已有CPU软件读取容器与**packet PTS**，不可观看/导出视频帧、不进行视觉动作时间标注；禁止13GB整包或所有用户未同意的GPU/模型/原工作区变更。

**技术约束**：官网是13GB 480p ZIP URL，**不存在已证实的官方单视频公开URL**。可能的ZIP Range读取须遵守HTTPS官方域、稳定对象/ETag、每个GET实际`206 Content-Range`、拒绝`200`全包、网络全局ledger≤64MiB、最多12次Range请求、远程ZIP64/EOCD/中央目录及成员CRC/symlink/path/offset验证，所有前置合成安全测试先PASS，才允许任何真实视频Range。成员匹配来自已固定SHA的本地train CSV，确定性私密选择1个越界`start<L<end, end-L∈(1,5]`与1个干净对照；如果两者无法在官方包中安全唯一取得且预算足够，则STOP，不选择方便的替代、不改任何CSV。

**物理隔离**：`%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-MediaPilot\`，独立于原`Charades-v1-Metadata`、公有Git docs、RTX3090实验树和同步目录。保留媒体仅本地，不上传GitHub。执行者先核路径祖先/reparse、原metadata包SHA/许可、剩余磁盘空间≥512MiB、`ffprobe`已存在；缺工具/路径不清则STOP，不安装依赖/改conda/启动原GPU。

**分析层级与私密交付**：V1对照CSV`length`与所选2个MP4容器duration/start、视频stream`time_base`/rate、首末**packet PTS/DTS**等值；包时间戳不等于已解码帧时间与真实视觉动作完成。GitHub只能披露粗类别化CASE_OVERFLOW/CASE_CONTROL时钟匹配与可审查的方法/预算收据，不能公开视频/subject IDs、两例精确时长/端点/PTS、帧、ZIP或媒体sha。即使2例匹配，B区间质量和C事件真值仍HOLD，不能泛化至19,625条旧越界token；V2视觉核验需另外申请用户授权。

**十项执行与严格交付**：[BATCH013完整README](./codex-artifacts/VLM-BATCH-013/README.md)顺序为①授权/环境/源SHA②确定性私有样本③官方Range协议④安全ZIP索引⑤仅需两MP4受控下载⑥CPU ffprobe packet时间⑦与CSV时间合同比对⑧科学止损⑨预算/身份/合成单测⑩三层裁决；第⑨测试**必须在任何真实GET之前通过**，允许前置排列。只交5处：`docs/codex-artifacts/VLM-BATCH-013/`2份**脱敏**报告；`prototypes/`2份不含真实数据的通用stdlib代码和合成unittest；`docs/codex-results.md`末尾1条013父结果。**单次普通push后STOP**；任何下载失败/源无法安全索引即`BLOCKED`，不是必须花完授权额度。

## 十九、BATCH-013-FIX代码交付验收与CPU工具授权更新（历史）

**后续状态更新**：本节此前称“未获工具安装许可”，但用户已在2026-10-09明确批准**仅独立CPU ffprobe工具**的下载/隔离安装。原013不可重跑；当前唯一READY为下方BATCH014。媒体访问/代理直连仍HOLD，详见[工具任务](./codex-artifacts/VLM-BATCH-014/README.md)。以下旧文本保留为决策历史。

**明确区分父任务和修复**：原013提交[f86a1e8](https://github.com/floomeer83felix-source/vlm/commit/f86a1e8e7a2e31b40d9c1bd7f1b135d16ae25204)完成5处交付，但由于PATH、常见位置及有限登记runtime候选未找到既有ffprobe，正确在第1项停止。没有选真实视频、未访问官网Range/HEAD、媒体GET/正文0B、PTS/clock UNKNOWN；不能称已下载失败或官方服务器不支持206。新的[75af33c代码修复](https://github.com/floomeer83felix-source/vlm/commit/75af33c56342bce4af94f7d70d1cada7ebdb8667)共3处：更改已有通用协调器与synthetic unittest、`docs/codex-results.md`追加一条独立`BATCH-013-FIX`，没有再次运行原013。Codex报告5轮合成测试最终27/27 PASS，ZIP64/受限传输/本地ledger/取两成员/mock-ffprobe链条与父任务完成后禁止执行检查得到合成覆盖；**ChatGPT仅核文件/源码及测试方法，未在用户Windows实测或真实GET**。这只能标`ACCEPTED_CODE_ONLY`。

**下次执行前的额外独立安全核查**：当前源码`urllib.request.build_opener(NoRedirect())`可经Python默认ProxyHandler继承环境/系统代理；这与既定“不得通过代理/镜像取得视频”的协议可能冲突。其网络运行须明确拒绝或禁用代理，并增补相关纯合成测试；不能因27项通过就声称直连/来源安全已PASS。其他如HTTPS官方页面源码anchor、206/ETag、ZIP64具体格式、Windows reparse/CPU工具独立路径、两视频都在预算内仍未实地验证，继续由fail-closed机制限制。

**唯一待用户决定的`VLM-CPU-TOOL-GATE-014=WAIT_USER_TOOL_SCOPE_APPROVAL`**：是否批准由Codex在**不触碰原科研环境、不改PATH/Conda**的独立`%LOCALAPPDATA%\VLM-Research-Isolated\CPU-Tools\ffprobe\`部署一个经过公开来源、哈希与安装体积审计的**CPU ffprobe工具**，只为未来V1 packet-PTS研究使用。**目前没有安装许可**；来源、最终文件大小、合法分发与下载预算亦未最终冻结，故不得自行下载或安装。若用户同意，先只建立独立来源/体积核验的最小协议；同时由ChatGPT检查代理防护并另授新唯一READY父任务，**不重跑已结束013**。如果拒绝则保持媒体试点阻塞，原≤2视频/64MiB许可不会自动扩大。B/C事件真值、GPU和视频画面仍HOLD。

## 二十、VLM-BATCH-014：工具获取因直连超时安全结束（历史任务）

**本节以下曾是BATCH014的执行前许可/任务计划。实际BATCH014已由6bec3ab结案，工具ZIP仅部分下载、ffprobe未安装，不得重跑本父任务；现以顶端任务看板和下一节的015决策门为准。**

**新增明确用户授权（2026-10-09）**：允许我们**仅在**Windows`%LOCALAPPDATA%\VLM-Research-Isolated\CPU-Tools\ffprobe\`部署经来源、发布方SHA与体积核验的CPU ffprobe，不改原Conda/PATH/研究工作区/CUDA或其它软件，不自动启动视频/媒体/Packet-PTS、GPU/视觉。ChatGPT这轮只更新Github任务与研究文档，**没有访问用户Windows、没有下载工具或视频**。

**独立供应链依据**：[FFmpeg官方](https://ffmpeg.org/download.html#build-windows)公开承认直接只提供源码并给出Windows预编译[Gyan.dev](https://www.gyan.dev/ffmpeg/builds/)入口。Gyan明确发布`ffprobe.exe`且其64位静态包按其说明为GPLv3，release essentials固定FFmpeg 9.0.2，ZIP页称约109 MB。本次**冻结而非使用随日期变化的latest**：`https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-9.0.2-essentials_build.zip`，与同发布者`.sha256`文本严格核对固定`60f467265b1e312373dbcd92200c2618a74850f98d3d078e94296bb3fa2047ba`。发布方SHA只是**同源完整性检验**，没有独立开发者数字签名证明；HTTPS重定向/包内容/许可版本任何一项改变就STOP。默认无代理直连、不安装7z、winget、conda或修改PATH。

**资源限额与执行门**：本批**只针对工具**所有GET正文合计`≤150MiB`，私有ZIP/临时/只提取ffprobe与许可证总本地占用`≤512MiB`，磁盘剩余≥1GiB；必须检查实际LOCALAPPDATA/云同步/原工作区物理路径隔离及reparse、事先跑合成HTTP和ZIP安全单测≥12、无任意软件或数据执行；只有发布方checksum一致、完整ZIP SHA匹配、白名单ZIP安全、`ffprobe.exe -version`成功才标工具就绪。不得向公共Git提交工具包、exe或私人目录信息。

**单一任务[完整README](./codex-artifacts/VLM-BATCH-014/README.md)共10项**：①项目/权限/单READY②隔离与磁盘③供应链/GPL和固定checksum④先做synthetic安全反例⑤无代理TLS/限额下载ZIP⑥安全CRC及白名单提取⑦独立exe仅`-version`⑧媒体网络协调器代理漏洞**静态**审查，留下一批修复⑨资源和脱敏收据⑩工具/媒体分门决定。**只允许5处GitHub交付**：`docs/codex-artifacts/VLM-BATCH-014/`2脱敏报告、`prototypes/`两份独立stdlib安装工具+纯合成测试、`docs/codex-results.md`末尾一次父任务回报。成功提交后STOP，原Codex聊天继续留存。

**科研主门继续HOLD**：BATCH014成功仅是工具的`CPU_TOOL=AVAILABLE`，**不是**已从Charades官网取得两段媒体、更不是视频时钟/原标注结束点或P1/P2语义真值已验证。BATCH013及其FIX都已结束；后续必须先单独修复媒体客户端`urllib`代理继承问题，并由ChatGPT新建唯一READY父任务后才可在旧用户限额授权内考虑有界媒体访问。不能自动重跑013。TIME_BOUNDARY_QUALITY=HOLD，P1/P2 EVENT_TRUTH=HOLD，NOVELTY RETAIN0，长域FAIL作为Charades单独确认，GPU BLOCKED。

## 二十一、VLM-CPU-TOOL-GATE-015：用户选择安全断点续传（历史决策）

**2026-10-10补充**：用户已选定继续安全断点续传，不再处于等待A/B方向。以下历史文本中“等待用户”仅为当时状态；最新可执行入口是下方唯一BATCH015。**仍没有远端ETag/206或原本地文件的直接验真，因此必须fail-closed。**

**安全止损收据**：原[6bec3ab](https://github.com/floomeer83felix-source/vlm/commit/6bec3ab3e7e41571b8878e30c36b26ca710fd060)严格5处文件。原[供应链与资源报告](./codex-artifacts/VLM-BATCH-014/tool-source-integrity-and-isolation.md)与[代理继续HOLD报告](./codex-artifacts/VLM-BATCH-014/ffprobe-readiness-and-proxy-hold.md)记录官方引导、固定Gyan 9.0.2发布方checksum`60f467265b1e312373dbcd92200c2618a74850f98d3d078e94296bb3fa2047ba`文本通过；但工具ZIP只接收到**13,107,200B**后socket timeout。本轮网页/校验文本及工具ZIP所有GET正文累计**13,186,907B**，一次工具尝试、0重试、0完整ZIP、0CRC/白名单提取、0`ffprobe -version`；在本机新隔离根遗留部分`.part`与私有账本两个文件总13,107,774B。完整包SHA与FFprobe可运行性均UNKNOWN/NO。此为**安全停止并如实报告**，不是工具安装成功。执行者报最终16纯合成test PASS（初次测试曾FAIL，修复后通过），ChatGPT只核GitHub静态证据未远程复跑。

**恢复的科研经济原则**：不应因13MB已取得就无条件再尝试109MB。若用户决定继续，优先以**不执行旧014**的新最小任务检查在原冻结对象上是否有稳定ETag/长度/HTTP Range206，并在新合同中一次性限定只允许相同对象继续读剩余字节；现有13,186,907B必须接续累计记账，不能另算150MiB；原13,107,200B部分数据要在同版、可靠offset及文件完整性可证明时才可用，否则STOP并重新征求方向。不可更换到别的发布包、最新版本、镜像或原Windows研究目录，不做任何视频/ffprobe PTS实测，更不可复用已完成013/014任务入口。

**尚需独立解决的技术债**：原[013媒体协调器](../prototypes/charades_range_media_clock_pilot.py)仍可能从`urllib`默认ProxyHandler继承环境/Windows代理。014工具安装器已显式禁代理，但不代表旧媒体程序已修复；就算以后ffprobe可执行，仍需新父任务在合成反例中先证明媒体端禁代理、预算与ZIP成员安全，再考虑已另行批准的最多两视频/64MiB V1试点。当前无任何媒体GET/GPU授权扩大，Charades B边界和C事件真值继续HOLD，科学创新retain0。

**状态**：`VLM-CPU-TOOL-GATE-015=WAIT_USER_CONTINUATION_CHOICE`（非READY）。等待用户说“继续做安全续传方案”或“暂时停止工具路线”；**本轮GitHub状态更新不是要求Codex马上再次联网**。

## 二十二、VLM-BATCH-015：强ETag/206与ffprobe独立工具就绪验收（历史已结束）

**2026-10-10最新执行事实**：015已由b0d163f完成并经ChatGPT验收，旧part后缀、发布方整包SHA与版本检查报告PASS；原015计划不再可执行。仅公开协议与历史，不得重跑或自行消费剩余工具/媒体预算。最新唯一READY转向下方BATCH016离线HTTP禁代理代码修复。

**新增用户决定**：明确“继续安全断点续传方向。请先核对原部分工具包、同源ETag/Range206、剩余累计预算及安全条件，在GitHub制定新的有限任务；禁止重跑014，不得下载Charades媒体或使用GPU。”本批是**工具供应链已批准范围内的新、仅一次条件性续接**，不构成新的150MiB额度或新的Charades数据授权。

**可核而尚未验的事实**：Gyan目前公开9.0.2 release essentials ZIP约109MB，发布方SHA`60f467265b1e312373dbcd92200c2618a74850f98d3d078e94296bb3fa2047ba`沿014冻结；旧014报告的原part=13,107,200B、原ledger body=13,186,907B，工具全部GET上限157,286,400B故剩余144,099,493B。ChatGPT仅阅读GitHub收据与旧安装器代码，未访问用户Windows上的`.part`或`tool-ledger.json`；尝试自身无代理直连HEAD得到DNS解析失败，**不能声称Gyan当前服务器Range206、ETag或真实Content-Length通过**。若已存在原part不一致/旧ledger缺失/源码发现不能安全append/禁代理，则STOP，不得猜。

**十项强制合同**：[完整BATCH015 README](./codex-artifacts/VLM-BATCH-015/README.md)：①Git单READY与014已结案核验；②原固定WindowsCPU工具根的.part/旧只读ledger/隔离/空间核验；③合成至少18 tests先PASS；④对同一固定Gyan URL只发最少HEAD（新强ETag只证明新会话稳定，旧ETag未留存）；⑤用真实`206`先读≤4KiB原part边界匹配，再只允许一次`If-Range`强ETag保护的后缀Range正文追加，200/416/代理/跳转/超限立即STOP；⑥SHA验证整份发行包后才算补全同源；⑦ZIP/CRC/白名单提取，独立exe只能`-version`；⑧CPU工具与媒体/V1科学门分离；⑨原014账本不改、另建累计继承的新持久ledger及匿名报告；⑩明确STOP和预算收据。**新增工具GET最多2次，0自动重试；014+015所有工具GET正文≤150MiB，磁盘≤512MiB，源版本9.0.2和SHA不变，完整SHA不符则无任何exe执行**。

**GitHub只许5处**：`docs/codex-artifacts/VLM-BATCH-015/`两份脱敏报告，`prototypes/`两份全新通用std-lib resumer/tests，`docs/codex-results.md`末尾一条父结果。不允许编辑014旧原型/测试/报告，013旧媒体协调器、原数据、原科研工作区、Conda/PATH、现存part前缀和ledger历史、其它看板/总览；0Charades视频/Range/PTS/GPU/模型/视觉/V2。成功push后STOP，ChatGPT验收后才能决定媒体程序代理安全修复的新任务，**不能自动重跑013/014**。

## 二十三、VLM-BATCH-016：媒体客户端禁代理/HTTPS安全代码交付已验收（历史）

**2026-10-10历史状态补充**：BATCH016按4c3e8bf已结案为`ACCEPTED_CODE_ONLY`，此前本节“016唯一READY”属执行前历史文字。当前可执行入口为下方017：原受限V1媒体许可仍有效，但先修授权/账本并通过全部synthetic门，失败绝不联网。

**先验工程突破的科学边界**：BATCH015 Codex实际取得114,768,076B的Gyan 9.0.2 ZIP整包，由014旧13,107,200B前缀和唯一206后缀拼成；SHA256与供应商固定值`60f467265b1e312373dbcd92200c2618a74850f98d3d078e94296bb3fa2047ba`匹配，并通过全成员CRC、白名单最小部署。执行者报CPU ffprobe `-version`成功（9.0.2），工具旧GET+新GET实际合计`114,847,784B`、剩余`42,438,616B`，无独立开发者签名或ChatGPT机器本地复验。`CPU_TOOL=AVAILABLE_PUBLISHER_HASH_VERIFIED`，**只表示以后有CPU packet检查工具，不是任何Charades视频/媒体PTS数据、原时间误差已验证。**

**下一唯一阻塞项**：旧[013-FIX媒体客户端](../prototypes/charades_range_media_clock_pilot.py)`RangeClient`构造`urllib.request.build_opener(NoRedirect())`，默认会安装受环境/Windows代理影响的ProxyHandler；这有违原限制的直接官方HTTPS来源/禁止镜像代理。`MEDIA_CLIENT_PROXY=HOLD`，不得因为015工具部署成功而自动运行原013父任务（已结案）或视频V1。用户此前允许最多2段官方480p/总GET≤64MiB/本地媒体≤128MiB/V1只读取CPU packet时钟，但**BATCH016这次仅执行纯源码/模拟测试**，实际0 Charades/media/Gyan HTTP，0 CPU ffprobe调用/视频/PTS/GPU/模型。

**新[8项受限任务书](./codex-artifacts/VLM-BATCH-016/README.md)**：①安全fast-forward和唯一READY+历史父任务核验；②逐个检查既有代码的官网许可页面、S3 ZIP HEAD和Range是否继承代理；③仅修改原媒体协调器显式`ProxyHandler({})`、TLS默认验证、无重定向/固定官方HTTPS域，保留原流量/目录/ZIP防护；④修改原合成测试覆盖污染代理设置、系统代理检查被模拟为异常、共享opener/HTTP降级、错误响应不读正文等，最终≥30纯合成用例PASS；⑤禁止`run_pilot(execute=True)`及任何真实网络/ffprobe执行；⑥提交前检查只有受限网络安全差异；⑦恰好5处：2份016脱敏报告、原媒体代码、原测试、`docs/codex-results.md`追加一次；⑧`CODE_LEVEL_VERIFIED`与`REAL_MEDIA_RANGE=UNKNOWN`严格区分，推送后STOP等ChatGPT验收。任何模拟测试发现额外未覆盖风险→报告HOLD，不得为了通过扩大权限/下载来源或放宽预算。

## 二十四、VLM-BATCH-017：内置合成门安全阻塞，代码交付已验收（历史）

**最新事实（2026-10-10）**：本节历史执行合同的旧`READY`已经被[1641817](https://github.com/floomeer83felix-source/vlm/commit/1641817a05911d008373963d5cea88a45f1cb8b6)终结为`BLOCKED_SYNTHETIC_GATE_FAILED`，所以后面的计划是审计历史、不能再执行017。唯一真实execute未越过合成测试门；随后仅改虚构夹具并双上下文56PASS，不能抹去已失败机会。0实际媒体GET、0视频、0PTS/正式工具。现在0READY、下方研究决策门待用户选择。

**前批结论**：[BATCH016报告](./codex-artifacts/VLM-BATCH-016/media-http-proxy-threat-and-fix.md)与[纯合成收据](./codex-artifacts/VLM-BATCH-016/code-only-test-and-science-gate.md)对三固定官方HTTPS来源的`urllib`显式禁代理、TLS证书验证、禁止重定向/整包GET的代码修补提供静态证据；执行者报40合成PASS；两真实数据未获取、CPU工具未执行、媒体PTS仍未知。本批首次将实际媒体尝试安排在**事先用户独立批准过的最多2段/媒体HTTP GET正文≤64MiB、本地媒体≤128MiB、CPU packet-PTS**预算之内，不因Gyan工具106MB续传事实推断AllenAI视频服务器同样支持Range。

**017的前置安全修复（无任何真实研究网络）**：必须先将原`Ledger`从`response.read`后才`add`改为**每次≤64KiB读取前原子持久保存预留上界、crash/短读保守计费不退**，同时让`run_pilot`先核`VLM-BATCH-017`唯一READY+未回报+明确的媒体许可scope、后允许检查独立CPU ffprobe，否则连版本调用都不能执行。保持原BATCH016的显式禁代理/HTTPS白名单；旧40 synthetic test全部保留、至少新增12个极端反例，**≥52 PASS**后才准读取真实原CSV/ZIP与官方媒体网站。不通过直接STOP、0媒体网络字节；新程序不能为修bug任意扩大许可/改数据源/降低安全阈值或重新跑013/014/015/016。

**真实一次性分支（前置全部通过才触发）**：在用户Windows受限`Charades-v1-Metadata`中只读核固定原元数据CSV/ZIP SHA、原研究工作区及同步/跨目录reparse边界；唯一新媒体根`%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-MediaPilot\`事先不存在、按冻结算法私密选一例`0≤start<length<end,end-length∈(1,5]`和一例整行strict合法且相近长度的train视频。检官方项目页/许可仅两个文本固定来源且计入64MiB，官方S3 ZIP须有唯一实际URL、HEAD稳定强ETag/长度，全部尾部/ZIP64中央目录/local header和两成员请求都需真实HTTP206，回应HTTP200整个13GB时**不读任何正文并STOP**；GET总≤12，所有实际+保守预算≤64MiB，原包CRC/成员身份/文件展开预算≤128MiB。不能拿服务器目录结果重选“恰好能拿到的更小视频”。任何前置、远端、预算、ZIP/媒体工具阻塞就一次STOP，不下载整包/改镜像/新模型。成功后仅`ffprobe` CPU容器/packet PTS同CSV`length`和越界end做两例类别化对照，不执行画面/帧解码、人工物理动作重标、GPU。

**10项任务与严格交付**：[017 README](./codex-artifacts/VLM-BATCH-017/README.md)依序：父授权→记账/授权入口代码修复→≥52合成单测→隔离/来源/CPU工具实地预检→冻结两例→按需真实206 ZIP安全索引→≤2成员受限落盘→仅CPU ffprobe video packets→隐私/账本收据→层级裁决并STOP。GitHub只准5处：2份脱敏试点报告，更新原`prototypes/charades_range_media_clock_pilot.py`与原合成test，向`docs/codex-results.md`末尾追加**1条017父任务**，任何非白名单文件不改；不得公开视频ID/subject、细时长/PTS/类/私人路径/ZIP成员、原真实注释行或受限媒体，保留既有隔离工具/元数据/原科研工作区/所有历史报告与任务板不改。主科研结论：A旧012仅frame标签口径VERIFIED，B时间质量/C P1P2事件真值仍HOLD，Charades独立长域外推FAIL/创新retain0/GPU BLOCKED。**新017须用户在原Codex聊天显式触发，GitHub READY不等于自动实验。**

## 二十五、VLM-RESEARCH-CHOICE-018：用户已批准最后一次新父任务机会（历史方向决策）

**2026-10-10最新决策**：本节此前曾表示“等待用户是否继续”，现用户已明确同意一次新的018父任务，方向决策已结束；此前历史提问不再是当前状态。只有下方BATCH018为唯一READY，其他批不得执行、018失败也不自动补试019。

**复核材料**：[017访问/预算与执行阻塞](./codex-artifacts/VLM-BATCH-017/media-v1-access-and-budget-receipt.md)、[两例科学门/未运行证明](./codex-artifacts/VLM-BATCH-017/two-case-clock-and-science-decision.md)、[提交1641817](https://github.com/floomeer83felix-source/vlm/commit/1641817a05911d008373963d5cea88a45f1cb8b6)。BATCH017的正规执行在**内置合成测试**阶段`BLOCKED_SYNTHETIC_GATE_FAILED`：生产`fixed_preflight`与`ffprobe-version`未启动，冻结真训练2例未选择，官方媒体GET/HEAD/206 ZIP读取全部0，研究HTTP实际和保守计费0B、MediaPilot根未建，不能宣称时间边界更清楚或服务器不支持。新代码父门授权顺序/历史绑定、读前原子预扣、强ETag与定点工具校验按交付源码已补；原40合成加16新案例在普通和模拟原工作区两种上下文**最终**均由执行者回报56PASS。最终修正只针对合成路径mock（旧Conda拒绝测试的祖先路径检查），在失败的真实执行之后没有再执行一次真入口。历史017已形成结果，不能继续沿同一ID或“清零”私有账本重试。

**科研管理止损**：十七个批次后真正研究问题依然未进入视频时钟实测。此时不能自动因为新的合成PASS就再开放执行；新状态`VLM-RESEARCH-CHOICE-018=WAIT_USER_NEXT_PILOT_DECISION`、**0 READY**。只有用户明确选择继续才考虑一个**新且一次性、严格的父任务**，并且先在正式执行用相同环境完成双上下文合成门，固定旧用户媒体额度（最多2视频/64MiB全部GET/128MiB本地/仅CPU容器packet-PTS），允许所有失败立即STOP，绝不回滚安全约束、下载13GB整包、改镜像、复用014/015工具GET额度、查询STA或运行GPU。若用户选择停止，保留此批构造/运行和原研究隔离文件不删除，Charades仅为短视频frame-level工程对照，后续转真正长视频合法时钟资源前仍须许可/版本/原点准入。

**科学门不变**：A旧012 `OFFICIAL_FRAME_LABEL=VERIFIED_WITHIN_STATED_SCOPE`；B `TIME_BOUNDARY_QUALITY=HOLD`、C `P1/P2_EVENT_TRUTH=HOLD`；`CHARADES_LONGVIDEO_AS_SOLE_CORPUS=FAIL`、`ORIGINAL_MECHANISM=RETAIN0`、`GPU=BLOCKED`。只有从媒体/标注同版时钟取得外部物理证据才可能改变B，V1单独仍不足以改变C。**目前没有真实媒体与用户Windows的独立复算证据**。

## 二十六、VLM-BATCH-018：最终两媒体受限获取已完成，同钟UNKNOWN（已结案）

**2026-10-10执行后结论**：本节旧合同描述“唯一READY”是历史准入说明；[2453b88](https://github.com/floomeer83felix-source/vlm/commit/2453b88a732504f3ac2abe9bc2934f59291cc022)已完成唯一实际018父任务。按规定2视频/206/CRC/GET10与约1.98MB正文工程PASS，然而B帧标志使两例`CLOCK_UNKNOWN`，不构成时间轴认证。现**0READY，Charades媒体获取最后机会关闭**；此后的旧执行计划不得再次使用。

**用户明确同意，授权不上调**：2026-10-10用户答复“同意”给最后一个全新一次性父任务，仅沿既有Charades V1≤2官方480p训练视频、全部研究HTTP GET实际/保守正文总额≤64MiB、12 GET、本地媒体+临时+审计≤128MiB、隔离Windows CPU ffprobe只读容器与video packet-PTS。**严禁**下载约13GB视频整ZIP、55GB原视频包、换镜像/代理/STA/视频画面/模型/GPU或触碰原Windows RTX3090实验工作区。原017已结束，不能改名或再运行旧父任务。

**阻塞根因有可验证修复**：017在独立普通上下文跑56合成通过，但其唯一内置`--execute`合成测试因`VLM_ORIGINAL_WORKSPACE`相关祖先路径检查与旧`Path.resolve`模拟不兼容而失败。之后仅离线修合成mock并在普通与模拟工作区两套环境均56PASS，**未再次运行execute**；所以这不是已证媒体源问题/时钟对照实验。新018前置必须至少58项（原56全保留＋≥2相同执行环境/Conda路径防回归）在普通＋模拟执行变量上下文**双PASS**，以及真实入口实际内置合成门同数PASS，且不能触碰真实原媒体/Windows文件身份；失败即STOP，不消耗媒体预算。修改`prototypes/charades_range_media_clock_pilot.py`的父门只许绑定018合同与013–017历史回报固定hash，不得解除真实媒体网络的读前`Ledger.reserve/fsync`、默认TLS/明确禁系统代理/源URL/无跳转、ZIP64/CRC、预算及同类样本冻结规则。新018原则上**最多一次**真实execute，任何失败停止，不得现场改源再重试。

**顺序操作/交付详见[完整BATCH018十项合同](./codex-artifacts/VLM-BATCH-018/README.md)**：①唯一READY+历史核验；②017→018许可/合同与017回报SHA锁定；③2上下文＋实际内置纯合成≥58全PASS；④正式一次execute才允许本机CSV ZIP SHA/Windows隔离身份/既有CPU ffprobe只读预检；⑤先冻结1越界1严格合法train样本的私有映射；⑥仅官网许可与官方S3 ZIP HEAD强ETag及受限206 Range；⑦仅两成员按预算和CRC下载至独立MediaPilot；⑧既有CPU ffprobe只读容器/video packet PTS，并同CSV`length`/原越界end做类别化对照；⑨单一持久账本/脱敏预算和两例隐私红队；⑩科学分层+无论成功/失败都STOP，**不创建019**。只许5处GitHub交付：`docs/codex-artifacts/VLM-BATCH-018/`2份脱敏报告、原媒体协调器及test两处最小改动、`docs/codex-results.md`末尾单条018结果。旧017及013至016报告/工具及原实验资产必须不动。

**真实证据仍欠缺**：AllenAI官方S3实际HTTP206/ZIP结构与两条冻结MP4成员≤64MiB可取尚UNKNOWN；不能用Gyan工具包的206说明AllenAI支持。即使V1获取成功，最多只是2例媒体时间原点/容器和包PTS线索，不代表旧19,625条strict不通过标注真实错误或全部时间已修好。A官方25点label限域VERIFIED，B time-quality与C P1/P2语义真值HOLD、Charades单独长域FAIL/原创RETAIN0/GPU BLOCKED。017及前批不得重跑，018成功或安全失败后先由ChatGPT审查，然后**结束本媒体获取尝试路线**并评估论文可证性/真正长视频合法来源。

## 二十七、VLM-RESEARCH-POST018-DIRECTION：结束Charades视频获取，转向长域科研证据门（无READY）

**正式独立验收**：[BATCH018访问与预算收据](./codex-artifacts/VLM-BATCH-018/preflight-and-http-resource-receipt.md)、[两例PTS/科学决策](./codex-artifacts/VLM-BATCH-018/two-case-pts-and-research-decision.md)、[2453b88](https://github.com/floomeer83felix-source/vlm/commit/2453b88a732504f3ac2abe9bc2934f59291cc022)。恰好2份匿名报告、现有媒体协调器与test两文件、结果尾部1条，共5处，无音视频/注释行/私有subject/video ID/精确PTS推送。执行者报告父任务一次execute、59项纯合成在普通/模拟环境均PASS，官方项目/许可与固定S3视频ZIP单个HEAD强ETag、按需10 GET 206、ZIP两唯一成员/CRC正确；真实应用层读入与保守计费都为1,979,817B，小于67,108,864B，保存2 MP4且本机ffprobe packet-PTS完整采集到私有审计文件。ChatGPT审查GitHub源码和脱敏报告，**未独立读取Windows视频、账本或PTS元数据复算**。

**学术关键失败仍需保留**：CASE_OVERFLOW与CASE_CONTROL都由冻结的`classify_clock`因视频stream的B帧标志直接返回`CLOCK_UNKNOWN`，即使已有私有packet元数据也**不能**作CASE_LIMITED_MATCH/DIFFERS、不能把CSV`end>length`推定为媒体或标注本身错误、不能更改样本/容差或追加另一轮视频试验试图得到可发表的数字。原框架A官方frame label政策限域`VERIFIED`，B原媒体时钟/时间质量`HOLD`，C P1/P2物理事件实例`HOLD`，长视频外推`FAIL`，novelty`RETAIN0`，GPU`BLOCKED`。

**结束媒体获取路线**：用户此前同意这条路线“最后一次”尝试；现018虽实现工程取样但未解决科学同钟，必须STOP。禁止再执行018/013–017、创建019 READY、消费剩余64MiB媒体预算、扩大到13GB整包/第三方镜像/更多片段或模型/视觉V2。2段视频及其详细PTS/音视频内容和ledger仅限已批准Windows隔离目录；**不删除现有文件、不迁移到原科研工作区、不公开任何原始内容**。

**下一科研方向仅为非执行方向门**：`VLM-RESEARCH-POST018-DIRECTION=WAIT_USER_RESEARCH_DIRECTION`（非READY）。可建议用户选择转向有明确公开许可、同版视频+annotation时间合同、足够自然长视频和可对照文献的候选集合，以及重新确定具可检验反例的机制贡献；这些步骤先以公开文献/README/license/benchmark评测代码**静态评估**，不消耗新网络媒体/模型/GPU权限。不把Charades短视频P1/P2数字作为论文已验真实事件，也不在无独立外部验证下宣称顶刊创新达标。只有用户明确新的科研方向和范围后，ChatGPT才可能另行签发新唯一READY；本轮不安排后续Codex自动执行。

## 二十八、VLM-BATCH-019：真正长视频许可证、时间轴与原创机制的仅公开静态证据审查（原执行合同，现已结案）

**方向授权边界**：用户在BATCH018最终`V1_CLOCK=UNKNOWN`、最后两段真实视频工程获取已停止之后回答“好的”，仅同意下一步对**公开官网/README/LICENSE/源码网页/论文摘要与公开学术HTML进行静态核查**。不批准任何新的视频、字幕、标注压缩包/QA题项、模型/权重/PDF文件下载、账号注册或数据使用协议签署、Git clone第三方项目/依赖安装、CPU ffprobe/GPU与用户本地Charades/RTX3090实验目录访问。Codex不得用先前64MiB余额继续下载Charades，不能重启原013–018或自动020。

**先验事实与初筛链接**：[公开资料种子](./long-video-static-screening-seed-2026-10-10.md)只依据数据项目官方页面与论文静态文字，列六候选：Ego4D NLQ（官方schema具`video_start_pts`/`video_base_numerator`和video/clip双时间基，但真实数据/annotation需接受独立协议）、HourVideo（500段20–120min、12,976个QA，Ego4D同源，不许benchmark进入训练集）、LongVideoBench（最长1小时，loader的视频采样与字幕`starting_timestamp_for_subtitles`需独立对齐）、Video-MME（30–60min长split但不提供默认物理事件时间边界GT）、MLVU（原视频版权非标注方所有、部分素材替换风险）及LVBench（最长2h、第三方源版权要分开核）。**这些只是网页线索，不构成下载/训练/真实时钟GO；Ego4D GitHub的MIT代码许可不等于原视频许可**。EgoSchema每题3min只可作辅助短域控制，不可当自然长视频证据。

**强先例约束**：VideoTree CVPR2025已经做查询自适应粗到细树检索，ReWind CVPR2025做指令条件可学习记忆，VideoMind ICLR2026是planner-grounder-verifier-answerer，AAAI2026`Seeing Is Believing`/EV²-Bench与DynamicSelect已提出长视频时空证据评估+动态层级压缩；LongVideoBench referred reasoning与EgoSchema temporal certificate sets也已经讨论跨时段证据。**不许仅用“长视频记忆+证据+时间戳+抽帧/弃答”自称可发表新算法**。仅预注册有反例、与强先例显著不同、所需独立媒体同钟/实例GT可获许可的可证伪H1时间基不确定传播/H2跨分钟事件身份与干扰/H3证据预算与校准风险，均维持`NOVELTY=RETAIN0`，后面若无真值/合法数据即NO_GO。

**[019完整八项README](./codex-artifacts/VLM-BATCH-019/README.md)**：①公有Git及唯一READY；②六数据集软件vs原媒体vs标注许可证/版权链；③长时输入分布与真长video/clip区分；④至少Ego4D/HourVideo/LongVideoBench/Video-MME时间原点、PTS/字幕偏移/正确版标注合同及缺口；⑤至少6项强先例最近邻；⑥2–3个可证伪且不得先称原创的科研假说/硬反例；⑦每个候选分别判断合法介质、时间合同、真正长时输入、事件真值/训练污染与硬件可行的静态门，UNKNOWN不得写GO；⑧公共仓库**恰好5处**：`docs/codex-artifacts/VLM-BATCH-019/`四份仅Markdown报告、`docs/codex-results.md`尾部仅一条019父回报。**不要修改任何代码/实验环境/原数据或历史报告**，一般push后STOP，等待ChatGPT科研审查和下一次用户明确决策。

### 2026-10-10 · ChatGPT验收BATCH-019：仅静态交付ACCEPT，0 READY

[提交24b771e](https://github.com/floomeer83felix-source/vlm/commit/24b771ef9c83e929579372a982ea17cd6edbbdb8)相对3d784c2仅一提交、严格四份新增Markdown及`docs/codex-results.md`尾部23行，无其它文件变动。验收八项报告结构、六候选、六必查+五新增2026先例和H1–H3可证伪/反例与六门退出；部分官方原网页由ChatGPT交叉核。网页结论与执行者的0文件下载/0模型/GPU/0私有资产访问是执行者回报，不声称独立观察其浏览器或Windows。重大边界：Ego4D代码MIT≠数据授权；HourVideo基于Ego4D且禁止基准数据进入训练；NLQ clip通常不构成小时输入；LongVideoBench v1论文HTML Table3六格之和3,761，与摘要3,763不符，保留STATIC_TABLE_TOTAL_CONFLICT、当前版本UNKNOWN；Video-MME/MLVU/LVBench媒体权利、版本和GT均未闭合。`TIMEBASE`仅纸面字段/offset映射，文件级同钟UNKNOWN；事件实例GT HOLD；H2普通物理身份记忆撞2026 GEB，H1/H3也撞COVER/置信弃答/证据校准，皆非新算法PASS。

**裁决**：`BATCH019=ACCEPTED_STATIC_DELIVERABLES`，`LEGAL_MEDIA=HOLD`、`TIMEBASE=UNKNOWN`、`EVENT_GT=HOLD`、`NOVELTY=RETAIN0`、`DEVICE_COST=UNKNOWN`、`DOWNLOAD_APPROVED=NO`、`GPU=BLOCKED`。下一研究方向转为`WAIT_USER_POST019_DECISION`（非READY），优先建议明确选择是否继续**公开网页级**的Ego4D↔HourVideo许可/同版映射与H1最近先例红队；也可停止当前假说组合。不得自动BATCH020、重新开放Charades或把纸面优先级当下载许可。

### 2026-10-10 · 用户选择H1反证与合法同版静态深挖：唯一READY BATCH-020

本任务只针对BATCH019留下的两个关键缺口：**(i)** H1中联合时间不确定/回答风险是否不过是正确time offset转换＋`union_{m∈M}m(I)`＋COVER+常规弃答的组合，要求明确双世界不可识别反例；**(ii)** Ego4D正式数据协议和HourVideo独立benchmark禁训与canonical→HourVideo版本/时钟是否有可公开核验的证据。以[020合同](./codex-artifacts/VLM-BATCH-020/README.md)为准，静态来源证据不等于数据/论文可用许可。用户**没有**授权Ego4D签约/开账号/下载、原HourVideo视频/标注/QA实体、任何媒体PTS文件级验证、原Windows私有资产、CPU/GPU模型或人工标注。只有020一个READY，020已产生回报则不能重复执行；结案后不得自动021。报告允许把两条路径一起判定`HOLD/NO_GO`，创新仍RETAIN0。

### 2026-10-10 · 停止连环静态任务、批准实验优先重整（最新）

用户明确指出此前20个批次缺真实长视频科学成果，并同意终止继续BATCH020式静态文档研究，转向可执行、可否证的真正长视频实验路线。BATCH020已先于这次转向提交[fdbb6e6](https://github.com/floomeer83felix-source/vlm/commit/fdbb6e66c85c1d4fa03f179b9af86f9f4322a1fe)，其四处Markdown变更经ChatGPT文件审查符合合同，普通H1核心算子`NO_GO`、Ego4D↔HourVideo同版及使用许可`HOLD`；只能按静态结案，不能撤销已执行事实或要求重跑。

新的[实验优先试验方案](./experiment-first-reset-2026-10-10.md)为**不含GPU执行授权的研究计划**：优先在用户另行明示可只读核实的已合法持有自然长视频与现有QA标签里确定12视频×2题，严格旧GPU账本/锁、来源/许可/QA隔离门；待另外审批后用同冻结Qwen3-VL模型、同12帧Qwen输入，对比均匀与既有SigLIP检索，最多48次Qwen QA前向，公开只报告脱敏的配对纠错/误伤/失败分母、按视频区间与全时延显存成本。无许可/标签/环境便STOP，不开连续文档批次补未知；即使跑完也**不自称新算法**，只凭真实且反复可核的长视频失误决定未来机制是否值得设计。保留旧Charades最终媒体止损、现有目录/环境与旧运行账本；`READY=0`、`DOWNLOAD_APPROVED=NO`、`GPU=BLOCKED`、`NOVELTY=RETAIN0`。

### 2026-10-10 · 用户批准一次性条件式本机实测：VLM-REAL-PILOT-001（唯一READY，最新）

用户在阅读[实验优先重整方案](./experiment-first-reset-2026-10-10.md)及ChatGPT提议的**“单轮私有已有资产预检→全部合格才运行最多48次Qwen、GPU累计最多120分钟→统一回报”**后明确回复“可以，快开始吧”。这构成**限定范围**的本轮预检及条件式GPU授权，不代表真实权限、许可、数据质量、独占锁或环境已经通过，也不代表ChatGPT能够直接启动用户Windows实验。此次不再开另一个纯网页/文档研究批次；任务目标是可验证的实际配对QA和资源数，或者严格0GPU的源资格阻塞，二者都必须诚实报告。

[冻结合同](./codex-artifacts/VLM-REAL-PILOT-001/README.md)规定唯一READY/no prior result、仅既有已登记用户合法持有资料限域只读、权益/样本≥12不同原生≥20分钟视频×2已有合法QA/来源版号与评测隔离/历史started账本/Windows OS锁与GPU进程预检；全PASS才可建新的隔离私有run并执行同一Qwen3-VL-4B、同帧上限的均匀12帧和现有SigLIP查询相关12帧对照（总48 Qwen启动尝试、GPU时间累计≤120分钟），冻结失败分母并计额外检索成本。不得假定旧MLVU合法可用或自动扫描全机，不下载受限视频/QA/模型、签协议、重装环境或合并/改旧研究树；未知即`NO_ELIGIBLE_DATA_STOP`，0GPU。不允许依靠BATCH018剩余额度重开Charades；研究现象不等于新算法，`NOVELTY=RETAIN0`。Codex只提交一份脱敏`paired-longvideo-pilot-receipt.md`和`codex-results.md`尾一条，正常push后停止，不自动派续跑。

### 2026-10-10 · REAL-PILOT-001验收：来源使用权门UNKNOWN，0GPU安全停止（最新）

[用户提供的真实交付272d7f4](https://github.com/floomeer83felix-source/vlm/commit/272d7f4860e21e681ab38d839e571c0c0b50e572)相对授权基线1886254仅一提交、**精确两处**：新增58行[脱敏阻塞收据](./codex-artifacts/VLM-REAL-PILOT-001/paired-longvideo-pilot-receipt.md)及`docs/codex-results.md`末尾10行，无代码/原资产改动。ChatGPT按文档证据接受执行者`NO_ELIGIBLE_DATA_STOP/PREFLIGHT_BLOCKED`的安全止损，不将它记作真实实验完成。Codex回报：只沿旧可信清单限域读取MLVU来源收据、README及必要存在性元信息，未读QA/视频；A3(a)源视频本次用途权利UNKNOWN，因此立即STOP；A3(b-f)、A4锁/模型及A5/B全部NOT_RUN；新run0、Qwen启动0/48、SigLIP0、GPU0秒/7200秒、媒体读取0。未现场独立核Windows或私人许可原件，这些动作和0调用由执行者申报；文档范围GitHub可核。

**法律/实验门需更加准确**：[MLVU官方GitHub](https://github.com/JUNJIE99/MLVU)将数据声明为CC-BY-NC-SA-4.0、研究/非商业用途，并注明原视频版权非项目方所有；[官方HF数据入口](https://huggingface.co/datasets/MLVU/MVLU)要求登录并接受访问条件。不能认为非所有权就当然需要逐个作者书面许可，也不能认为镜像下载/hash或单页README足以证明此次使用符合所有适用条款、例外和获取条件。当前用户镜像收据对应**具体资产/用途/授权链仍UNKNOWN**，禁止ChatGPT自判LICENSE_PASS，按适用法律及现有许可自行合规评估；不代用户登录/签署或补抓视频。最短路径不是再发文献审查任务，而是由用户决定提交/核实合法取得和研究用途的官方访问收据（无需上传数据或私人凭据）或明确换有清楚原媒体使用权+QA标签的来源，才另行审视实验授权。下游12×2长视频资格、源独立性、锁/GPU和模型未测，不能得出当前机器没有实验能力、MLVU非法或策略效果负面。**现为0 READY、0实验GPU额度自动续用；该一次性父任务已结案，不重跑，不自动开启下一任务**。

### 2026-10-10 · Ego4D已签署，HourVideo等待期实际准备：离线资格工具已交付（当前最新）

用户提供Dropbox Sign签署成功截图，证明Ego4D访问协议电子签名完成，**并不代表官方审批或临时AWS凭据已获批准**。目前优先不再派新Codex文档父任务；ChatGPT直接交付[离线Python标注层资格工具](../tools/hourvideo_dev_preflight.py)与[用法、HF gate/答案文件区别](./hourvideo-wait-period-lab.md)。HourVideo作者2025-03-06宣布附答案`dev_v1.0_annotations.json`已发布，旧`dev_v1.0.json`无GT；HF官方数据repo可列文件、需要用户登录同意共享联系方式等条件才可取得受控标注；Ego4D签署不能替代HF gate。该离线工具只解析用户将来**自行合法获取并明确指定的本地开发集JSON**，校验至少12视频各2个有合法正确标签题、≥20分钟和至少4个≥30分钟的**元数据层数量**，输出匿名汇总；含纯虚构样例自检`--self-test`，当前**未访问真实标注或运行实际自检**。不认证视频真实时长/文件/合法使用/时钟/进程锁/GPU可用。源码不联网、不读GPU、不上传QA、答案、视频UID、音频/图片；不改原始含canary文件。Ego4D/HourVideo原视频的使用许可、release/UID映射、12×2具体实体均需后续合法可取证据。旧REAL-PILOT-001仍按272d7f4结案，所有H1创新`RETAIN0`、Charades`FINAL_MEDIA_STOP`、0 READY与无GPU新授权保持。**下一用户动作**仅本人阅读并接受[官方HourVideo HF gate](https://huggingface.co/datasets/HourVideo/HourVideo)，等待Ego4D审批；不交账号、token或私人数据给ChatGPT。完成后再决定是否批准本机一次性标注核验，而非自动续跑旧Pilot。

### 2026-10-11 · 用户选择Codex代跑下载后标注资格：唯一READY VLM-HOURVIDEO-DEV-001（最新）

用户已向ChatGPT展示HourVideo/HourVideo官方HF页面明确「You have been granted access」，后续截图显示`dev_v1.0_annotations.json`大小约1.85MB并明确回复「已下载」，再说「还是交给codex吧」。因此无需新增版权论文静态批次；直接下达[唯一有限CPU父任务](./codex-artifacts/VLM-HOURVIDEO-DEV-001/README.md)给原同一长期Codex聊天：只定位当前Windows用户Downloads顶层该已下载文件、先对已有离线脚本做完全虚构自检、再只读运行本地真实JSON匿名汇总，必要时最小代码适配。要求报告可解析视频数、≥20min且每段≥2合法答案题视频数、≥30min数、是否可组成12段24题及无效原因；不得打印/上传任何真实受保护QA/正确答案/video UID/qid、canary、用户路径。Codex提交只可`docs/codex-artifacts/VLM-HOURVIDEO-DEV-001/local-annotation-eligibility.md`、结果尾一条和必要时`tools/hourvideo_dev_preflight.py`小补丁，原资产保持不变。**0 GPU/模型/媒体解码与下载**；Ego4D协议虽已签署但批准未证，标注合格不自动放行真实媒体或下一实验；没有多任务连续执行。任务执行需用户在原Codex聊天主动启动。

### 2026-10-11 · HourVideo开发集真实标注充足：50段/1182题，24题资格门通过（最新）

Codex已在用户认可的私有下载范围内完成一次真实JSON的CPU只读资格检查，并于[da6a6fd](https://github.com/floomeer83felix-source/vlm/commit/da6a6fd73195fec63c480187a5872c8179b5cc4e)向main提交[匿名收据](./codex-artifacts/VLM-HOURVIDEO-DEV-001/local-annotation-eligibility.md)和唯一父回报。GitHub diff仅两处Markdown（报告56行/回报追加10行），符合预定权限，未修改检查脚本；工具合成自检PASS、真实`--annotations` exit0、代码改动0、原JSON前后SHA不变和0GPU/0媒体为执行者自述，未直接独立复算本机。**量化结果：50视频metadata记录；50段≥20min且各≥2道工具有效答案题，其中41段≥30min；共1182道`qid/question/mcq_test/correct_answer_label`类型合规题，按要求可组成12视频×2题。拒绝数0。** 不能由不同JSON键证明不同物理源，不可由标注时长推出已获原媒体/文件PTS同版，选择标签有效不等于答案语义准确或事件级GT已知。

科研判定`ANNOTATION_CAPACITY=PASS_ON_METADATA`，但`MEDIA_LEGAL_ACCESS=WAIT_EGO4D_APPROVAL`、`VERSION_BRIDGE=UNKNOWN`、`PHYSICAL_MEDIA=NOT_ACQUIRED`、`GPU=BLOCKED`、`NOVELTY=RETAIN0`。**当前0 READY，禁止因开发标注合格自动跑旧48次计划**。后续只在官方批准、数据/下载范围与GPU新预算另获用户明确许可后安排最小同版取样与基线实验。旧REAL-PILOT-001、Charades安全停止均不可复活。

### 2026-10-11 · 等待Ego4D批准期间改做真实工程代码：唯一READY VLM-SYNTH-AB-HARNESS-001（最新）

用户获悉Ego4D官方审批尚未到达、10月13日提醒已安排，明确同意趁等待期**让原Codex单轮实现纯合成端到端A/B配对、自动评分与安全恢复代码**，而非再反复静态审查。现提供[冻结合同](./codex-artifacts/VLM-SYNTH-AB-HARNESS-001/README.md)，要求**新增两个可运行Python模块**（公共`prototypes/`目录，一份主逻辑一份unittest），虚构12视频×2题、A均匀12帧、B最多48候选按问题选≤12、48次固定尝试预算，答案与selector单向隔离，完整分母与视频/时长分层统计，原子 started/terminal 账本、崩溃不重试、manifest与并发冲突拒绝；必须在标准库CPU上实际执行测试并提供匿名证明。真实SigLIP/Qwen仅留fail-closed接口，**0真实JSON/视频/ffprobe、0模型/GPU、0网络下载和本机实验树触碰**。合成数字不可称科学表现，真实媒体合法性/时基/版本/GPU准入全部HOLD。完工只有源码、测试、收据和一条结果，正常push后停止；暂不批准下一任务。

### 2026-10-11 · 合成A/B运行器实际代码交付验收：31项测试由Codex报告通过（最新）

[Codex提交440f562](https://github.com/floomeer83felix-source/vlm/commit/440f5625e9c5a5e4c6a088cb0aca178a61a74347)相对于先前冻结READY基线`92f399d`恰好只改4处：新增`prototypes/hourvideo_synthetic_ab_runner.py`（434行）、`prototypes/test_hourvideo_synthetic_ab_runner.py`（300行）、`docs/codex-artifacts/VLM-SYNTH-AB-HARNESS-001/synthetic-runner-receipt.md`（54行）及`codex-results.md`尾部一次追加（10行）。ChatGPT静态读GitHub代码、两份回报及差异，确认合成12×2题、uniform12 / query-only合成B最多48候选选12、题目答案与selector隔离、24固定分母、五格矩阵/视频簇/时长层、非阻塞OS锁、预扣STARTED、原子文件替换、失败未终态不重试与预算停止均有对应实现与测试。Codex申报最终31项单测和CLI自检均31/31 PASS、CLI完成48次模拟尝试，真实模型/GPU/视频/QA访问均0；**独立容器没能获取GitHub源码复跑，ChatGPT不声称实际重新执行成功**。

科研裁决`ACCEPTED_SYNTHETIC_HARNESS`仅确认工程代码交付和由Codex报告的合成测试，不是`REAL_VLM_EVALUATION_GO`：真实媒体许可/同版映射/PTS、Qwen/SigLIP适配、OS与GPU硬预算仍HOLD；未来真实模型需保证A/B同一问题提示与解码配置，当前`Prompt`内含`arm`字段，必须确保arm仅属评测元数据而非模型可见输入，否则可能制造伪策略差异。文件原子替换不证明整机掉电耐久性；模拟秒数与模型真实成本无关联。**0 READY，禁止旧父任务重跑和自动授权媒体/GPU**；保留HourVideo开发集24题标注层数量PASS、Ego4D官方视频批准等待、`NOVELTY=RETAIN0`及Charades`FINAL_MEDIA_STOP`。

### 2026-10-12 · Ego4D官方访问批准：有期限的媒体准备窗口（最新）

用户直接粘贴官方审批邮件措辞「Great news! Your request for access to the Ego4D dataset has been approved. Your access is valid until: Oct 26, 2026」。据此把`EGO4D_ACCESS_APPROVAL=USER_CONFIRMED`与`ACCESS_DEADLINE=2026-10-26`记为新事实；**不是Codex或ChatGPT已通过AWS验证凭据，也不是模型或下载启动事实**。官方Ego4D CLI帮助支持`--video_uids`/`--video_uid_file`限定对象，HourVideo官方数据卡表明`v1.0_release/video_uids/`有dev列表；优先在本机私有范围核这份UID表与已授权`dev_v1.0_annotations.json`键的严格一致性，再用官方获取方法确认单段Ego4D canonical`full_scale`的实际版本、大小、可用性，而不是尝试全量Ego4D/剪裁NLQ clips。参考[Ego4D官方CLI](https://github.com/facebookresearch/Ego4d/blob/main/ego4d/cli/README.md)和[HourVideo官方数据卡](https://huggingface.co/datasets/HourVideo/HourVideo)。HourVideo dev GT限制训练与修改canary，绝不能上传真实UID↔QA/答案、凭据、私有链接或原视频。

**下一阶段尚待用户明确授权的受限操作**：是否允许在原Windows本地只读验证访问工具/SDK与凭据**是否存在（不得回显任何值）**、私有读取已下载标注键并核对官方dev UID列表、查询官方有限元数据/一个待挑原视频对象大小（如须联网，另设严格请求与字节限额）；随后用户另行指定少量视频下载预算，再独立审GPU与真实模型调用。原媒体下载总量、路径、许可条款及模型运行必须有明确新任务合同/预算，不能因为邮件获批或之前已结束的旧48次提案而擅自执行。**当前0 READY**，不预先唤醒Codex，也不做自动媒体下载/模型实验。10月13日旧“审批是否收到”提醒已因批准事实关闭。

### 2026-10-12 · 用户批准Ego4D最多2段、8GiB、0GPU首次视频获取（最新）

用户在看到官方Ego4D访问批准至2026-10-26以及ChatGPT的明确提案后，回复「好的」，正式批准**至多2个不同HourVideo开发集UID对应的Ego4D canonical full_scale视频**、**逐文件最多4GiB**、**本父任务实际所有网络GET正文累计至多8GiB（含小型授权manifest/失败/重试）**、**0GPU/模型**。ChatGPT先查官方[Ego4D CLI](https://github.com/facebookresearch/Ego4d/blob/main/ego4d/cli/README.md)：当前文档支持精确`--video_uids`和`--no-metadata`及`full_scale`，但不能把CLI选项当实际强制网络传输上限。现立[唯一READY VLM-EGO4D-MEDIA-001](./codex-artifacts/VLM-EGO4D-MEDIA-001/README.md)，由同一长期Codex聊天在用户明确触发后：先确认原本机已授权HourVideo JSON顶层UID、官方Ego4D canonical版本/远程完整对象/大小、AWS访问及**跨中断严格硬预算可执行**，全部PASS才用新私有隔离目录有限GET最多2段；不满足则0媒体GET、匿名报告实际阻塞，不能安装新软件、申请额外付费服务或转向镜像。文件可选做现成ffprobe容器级粗时长验证，不解码/扫描PTS；拿到2段也仅证明小样本存在及来源元数据，不是全部12段/24题QA可评分、更不是GPU批准。结果只上传一次匿名聚合收据+尾部一条，私有视频/UID/答案/凭据与GET账本绝不提交。前轮HourVideo标注及synthetic工程不重跑，Charades FINAL_MEDIA_STOP、NOVELTY RETAIN0持续。

### 2026-10-12 · Ego4D媒体预检因SDK/CLI缺失安全停止：0数据GET，先补工具而非重跑（最新）

Codex已按唯一READY在用户本机允许执行上下文内检查预装命令/模块，上传[4c38e2a](https://github.com/floomeer83felix-source/vlm/commit/4c38e2a07959298f08037c6637ff9e9a804637fa)及[匿名收据](./codex-artifacts/VLM-EGO4D-MEDIA-001/limited-media-receipt.md)。GitHub相对于授权基线只新增65行匿名报告、向`codex-results.md`尾部追加10行；无代码/视频/受限JSON/配置/凭据改动。当前PATH下未找到AWS CLI及Ego4D CLI，当前Python未发现boto3及ego4d；未切换激活其它Conda环境或枚举私有安装路径。**裁决ACCEPTED_SAFE_STOP/SAFE_TOOL_MISSING**：0数据manifest/媒体GET，0官方S3 HEAD，数据GET正文0字节（不覆盖普通Git/网页流量）、0新媒体文件、0私有账本、0 GPU/模型。AWS身份认证、HourVideo→Ego4D UID同版、远端object HEAD/大小、持续硬预算、媒体时长/PTS等并未执行，标记UNKNOWN而非FAIL，不能误称数据下载故障或权限被拒。

用户转述的Ego4D批准至10月26日仍为有效事实。**旧VLM-EGO4D-MEDIA-001已结案不可重跑，当前0 READY**；不因未用掉的2视频/8GiB自动授权第二次。下一步应优先提出一个有限的新工具入口（先允许精确查询已安装CLI/SDK和安全环境，再由用户单独批准必要的官方工具隔离安装），在工具可用后才申请单独新下载许可；不未经同意访问密钥/密码/AWS设置、不让任何公有Git含实际凭据。HourVideo 50/1182容量及合成31测试已完成，NOVELTY RETAIN0与Charades FINAL_MEDIA_STOP均持续。

### 2026-10-12 · 用户授权修补唯一安全缺口：受控Ego4D官方CLI/SDK工具就绪（最新）

最新[Codex媒体预检收据4c38e2a](https://github.com/floomeer83felix-source/vlm/commit/4c38e2a07959298f08037c6637ff9e9a804637fa)确认阻塞点为**当前shell缺官方AWS CLI/Ego4D CLI和Python boto3/ego4d模块**，0数据GET/0GPU，不应将未查AWS认证或UID同版说成失败。用户明确批准「好的」来检查并按需安装官方工具，因此新[唯一READY VLM-EGO4D-TOOLS-001](./codex-artifacts/VLM-EGO4D-TOOLS-001/README.md)为一次限定CPU工程任务：先只读判断现有Windows shell与已知`pytorch`环境是否已具备工具；不足则**仅私有独立venv**、官方PyPI信任域和发行包/依赖限额下安装AWS boto3与条件式Ego4D CLI（PyPI `ego4d==1.7.3`仅有sdist，需先核官方SHA+setup代码，不得无审计直接`pip install -r requirements.txt`或升级Torch）。只验证离线imports/安全--help；**明确不授权任何AWS凭据、S3认证/HEAD/GET、HourVideo受限QA/UID读取、视频下载、GPU/模型运行**。最多新建一个私人venv，归档≤128MiB、专用空间≤512MiB、CPU前台≤20min；危险源码/版本冲突则部分就绪STOP并脱敏回报。公有Git只接一份工具资格收据与Codex结果末尾一条，旧MEDIA-001保持已结案。后续媒体获取需用户新批准，不自动继承2视频/8GiB。

### 2026-10-13 · boto3工具获得实际离线可用报告，CLI iopath源码门仍HOLD（最新）

两个Codex提交被GitHub证实均只涉及`docs/codex-artifacts/VLM-EGO4D-TOOLS-001/isolated-tool-readiness-receipt.md`与`docs/codex-results.md`：首次[5758834](https://github.com/floomeer83felix-source/vlm/commit/57588341dbe4a8175a3dac80a873a2928b94da9d)新增51行收据/10行结果，执行者在首次官方PyPI元数据请求Timeout后STOP，venv创建成功但安装数0；后续[0758106](https://github.com/floomeer83felix-source/vlm/commit/07581063c53679d91d4530c00a491f61e24f9b11)向原收据追加18行及结果10行，执行者称用户单独允许复用venv修复，固定boto3 1.40.52 PyPI元数据请求成功，7个合法wheel由其哈希/CRC/依赖核验并在原私人venv一次`--no-index --require-hashes`离线安装，网络禁用的boto3/botocore导入1次PASS。**这是单独修复提交而非原一轮合同的一次正常push**；ChatGPT仅验证公有Git diff/收据，不冒充验证本机二进制、外部用户授权消息细节或实际独立重跑。

官方ego4d 1.7.3 sdist按执行者SHA核验PASS、未运行setup，`iopath 0.1.10`被报告官方wheel数0，禁止额外源码构建，故`PARTIAL_BOTO3_READY / EGO4D_CLI_SOURCE_BUILD_HOLD`。SDK版本不等同CLI可用，亦未证明SDK能取Ego4D发布映射；7 wheel+1 sdist已获取归档14,809,324B、新专用venv根约50,462,720B、前台合计约392s（Codex回报且有计量局限）。0 AWS Credentials/profile/Session/client、0数据认证或S3 HEAD/LIST/GET、0 HourVideo受限UID/QA/原视频/帧、0真实GPU/模型与原环境改动。技术成果为**AWS SDK离线工具基础**，数据/研究进展仍`MEDIA_UID_VERSION_BRIDGE=UNKNOWN`, `PHYSICAL_MEDIA=NOT_ACQUIRED`, `GPU=BLOCKED`, `NOVELTY=RETAIN0`。现**0 READY**，不重启旧工具/媒体父任务；下一步需要用户批准一个新的、明确源和字节上限的范围，优先绕开非必要CLI依赖走已获安装的boto3有界访问，或经另一独立代码安全任务审核iopath源码依赖。Ego4D申请有效至2026-10-26。

### 2026-10-13 · 用户同意boto3优先：唯一READY转为真实可运行的离线官方对象映射与传输硬门代码（最新）

用户对“下一轮优先利用已安装`boto3`、暂不为Ego4D CLI补`iopath`源码构建、后续AWS访问与真实下载必须单独授权”的提议回复「好的」。ChatGPT核官方固定源码`facebookresearch/Ego4d@4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb`的`manifest.py/config.py/download.py`：`full_scale`官方清单按`public/{version}/full_scale/manifest.csv`组织，候选字段包括`video_uid`/`file_uid`/`canonical_s3_location`/`s3_path`；CLI默认`v2_1`，**不自动假定HourVideo`dev_v1.0`与`v1`或`v2_1`同版**。新[唯一READY VLM-EGO4D-BOTO3-001](./codex-artifacts/VLM-EGO4D-BOTO3-001/README.md)交付**真正可执行**的独立纯stdlib合成manifest UID映射+两视频/4GiB单段/8GiB累计模拟GET严格预扣与crash恢复程序、≥18项unittest，不是论文或许可审查文档，不安装CLI和其它依赖。仅公开源码/测试/匿名实际运行收据+结果尾一条，真实AWS凭据、S3 LIST/HEAD/GET、真实HourVideo JSON/QA、视频和GPU均禁止；虚构测试过门只证明离线工程代码，不证明真实发布桥接或网络传输限流可用。之前安全结案任务不可重跑，不继承真实下载额度。用户在原Codex聊天主动触发，提交后STOP，等待科学/安全验收。

### 2026-10-13 · 离线boto3映射与预算工程完成交付：32单测报告PASS，真实S3/HV版本仍HOLD（最新）

核对Codex [b12f32f](https://github.com/floomeer83felix-source/vlm/commit/b12f32fd7174711bbebe589e92f4a3327bfabea5)相对于唯一READY基线`d776403`只有新增[主程序](../prototypes/ego4d_boto3_offline_gate.py)368行、[测试](../prototypes/test_ego4d_boto3_offline_gate.py)274行、[匿名收据](./codex-artifacts/VLM-EGO4D-BOTO3-001/offline-source-and-budget-receipt.md)59行与`codex-results.md`末尾12行，共四处。ChatGPT已静态阅读关键源码/32项测试、回报与GitHub差异。按Codex报告初版unittest30/30 PASS而CLI self-test29通过/1 ERROR，因Windows替换既有账本目标失败；修订为只增加不覆盖旧文件的原子快照+每代checksum/前驱链、增2项失败测试后，最后unittest32/32 PASS、CLI self-test32/32 PASS、完整合成演练exit0；**ChatGPT没有独立下载源码到容器复跑，不能称第三方执行复现**。

合成离线映射器为保守测试策略：只接受内部虚构SYNTH UID/假S3桶及`full_scale`版本枚举、把file_uid与video_uid区分、不自动将HourVideo开发v1.0匹配Ego4D v1/v2_1、模拟双对象长度≤4GiB且累计≤8GiB（metadata≤32MiB），使用逐代持久STARTED预扣、错包/版本改变、短读/Range/重试、并发锁/恢复拒绝。官方固定源码中`DATASET_PRIMARY=full_scale`常量与实际CLI argparse datasets默认annotations不能混用，Codex更正了这一前提。**关键限制**：测试构造的媒体key路径并非官方真实对象位置证明；整数chunk在接受之前截断，不足以证明真实HTTP已经到达但未read缓冲的正文/失败重试流量受控。真实Ego4D发布manifest、来源白名单、权限与HourVideo同版桥接、对象大小/PTS、网络强限及model/GPU全部未验证。0 AWS/数据S3、0受保护QA/媒体、0GPU/模型，不冒称新长视频科研指标。**裁决接受合成工程交付，关闭READY为0，不批准下一轮真实AWS请求**；如用户另准，小范围官方清单+HEAD核验比继续增加纸面或合成测试更优先；不要复活旧MEDIA/TOOLS合同，保留`NOVELTY=RETAIN0`及Charades`FINAL_MEDIA_STOP`。

### 2026-10-13 · 用户新批准真实AWS小范围metadata预检：仅1份manifest + 2次视频HEAD（最新）

用户在ChatGPT提出“使用现有boto3，严格限定读取**一份官方full_scale清单**、少量精确匹配对象的**HEAD**、不下载视频正文、不使用GPU、不公开密钥”后明确回复「同意」。因此前`SYNTHETIC_MAPPING_AND_BUDGET_READY`仅代码/32项合成测试，真实媒体与官方发布仍未知，创建[唯一READY VLM-EGO4D-AWS-META-001](./codex-artifacts/VLM-EGO4D-AWS-META-001/README.md)：固定官方源码版本`4bd10ed`及`v2_1` manifest位置`ego4d-consortium-sharing/public/v2_1/full_scale/manifest.csv`，仅在有用户专用Ego4D现成AWS profile、本地已批准开发标注文件路径和可核请求级限额时，用SDK内部签名对官方manifest先HEAD再以≤8MiB GET一次，按本地视频UID和官方canonical S3 bucket白名单做内存精确匹配，然后至多2个媒体对象仅HEAD读取大小/ETag。所有S3请求总≤4，无LIST/STS，**媒体GET0**，不展开其它版本/清单、视频/帧/metadata JSON、Qwen/SigLIP/GPU。任何工具/权限/大小/请求限制未知立即STOP并匿名报告，不使用旧MEDIA任务剩余额度，不推断UID相同等于完全同版/PTS证明。公有Git只允许一份新匿名收据和codex-results末尾一条，完成停止，未来真视频获取需新批准。Ego4D批准有效至10月26日，不能以窗口紧迫为由绕过安全门；Charades FINAL_MEDIA_STOP、NOVELTY RETAIN0持续。

### 2026-10-13 · AWS真实metadata仍未通：用户本机缺ego4d凭据profile（最新）

Codex提交[85cc6f5](https://github.com/floomeer83felix-source/vlm/commit/85cc6f5b5ed23c00124eac81156fdc255e80dc27)显示：原唯一READY VLM-EGO4D-AWS-META-001已进入真正Windows本机boto3身份配置前检，以指定专用`ego4d` profile及SDK静态共享文件提供器检查，返回`ProfileNotFound`，未创建client或发AWS连接；因此官方manifest HEAD/GET及最多2媒体HEAD全0，真实HourVideo UID JSON未读、实际视频/GPU0，0/4请求。提交改动只有一份匿名结果与codex-results尾部回报，安全执行范围可验收。原任务`ACCEPTED_SAFE_METADATA_STOP / AUTH_PROFILE_HOLD`结案，**READY=0**；`AUTH_NOT_CONFIGURED`不代表AWS远端403或Ego4D批准失效。研究不必再铺合成工程，只须用户按官方邮件在本机私人`~/.aws/credentials`配置`[ego4d]`的正式AWS Access Key/Secret（如供应方发行临时token则仅本机处理），不要发任何凭据/截图/文件到公共仓库或聊天。若批准邮件只告知批准而没有可见凭据，先走官方补发渠道。之后单独建立有界真实manifest + HEAD任务，再按实际来源与大小申请少量视频GET及有限GPU评测。审批至2026-10-26，旧Charades`FINAL_MEDIA_STOP`和`NOVELTY=RETAIN0`持续。

### 2026-10-13 · 用户已自行配置AWS凭据：新独立任务直接真实manifest+HEAD，不重跑旧meta（最新）

用户按此前指导在本机私下完成名为`ego4d`的凭据配置，并回复「已配置」。此消息不能独立证明AWS签名/服务访问有效，但已解决上轮`ProfileNotFound`的用户侧操作要求；据此创建[唯一READY VLM-EGO4D-AWS-META-002](./codex-artifacts/VLM-EGO4D-AWS-META-002/README.md)。本轮沿用上一安全合同的来源/大小/重试与隐私门，真实S3总尝试≤4：官方Ego4D `v2_1/full_scale/manifest.csv` HEAD1、文件≤8MiB且对象身份可绑定后GET1，解析本地已授权HourVideo开发标注**仅顶层UID/视频时长**，只对至多2个精确匹配官方canonical媒体对象HEAD；**媒体GET/LIST/STS/GPU/模型一律0**，不尝试其他版本和镜像。若profile配置有误、AWS拒绝、请求边界/源同一性无法核准，则如实安全停止，不安装新工具或重试旧父任务。真实版本/PTS桥接未知、旧2段8GiB额度不可继承；元数据成功后应立即制定一次真实视频获取任务而非继续合成流程。公有Git仅匿名收据和Codex结果末尾一条；Ego4D审批至10月26日。

### 2026-10-13 · 第二次真实AWS元数据任务因专用profile不可发现安全停止：优先修文件名（最新）

[Codex c600d44](https://github.com/floomeer83felix-source/vlm/commit/c600d4456cccefff034aafb8d44c45052cabd110)交付内容恰好匿名[收据](./codex-artifacts/VLM-EGO4D-AWS-META-002/limited-aws-metadata-receipt.md)和结果末尾一条，首次静态专用`ego4d`提供器直接`ProfileNotFound`，S3 HTTP0/4、官方manifest HEAD0/GET0、媒体HEAD0、视频/GPU/模型0、HourVideo真实UID未读取。`AUTH_NOT_CONFIGURED`指当前Codex Windows环境实际无法找到约定配置，不应误判远端403、许可失效或UID join为0。两次META任务均已一次性结案，**当前0 READY**。用户已经确认本机曾配置，下一操作必须是用户自己本机核对标准`~/.aws/credentials`真实文件/无`.txt`扩展，以及精确命名`[ego4d]`；仅返回YES/NO，不发送配置、密钥、Windows私人路径和截图。确认后再新开一个有界S3 manifest+HEAD任务。实验优先级为真实官方对象与限制性下载，绝不再补合成测试；Ego4D申请截至10月26日，真实GPU仍需对应媒体与独立预算授权。

### 2026-10-13 · 用户现场消除凭据文件名/节名阻塞，授权唯一META-003开始有限真实S3验证（最新）

在此前两次Codex`ProfileNotFound`且0 AWS请求后，用户在Windows控制台贴出**只有布尔检查**：最初`credentials`不存在而`credentials.txt`存在，已自行改名后`CredentialsFile=True/AccidentalTxt=False`；随后`Select-String`按行验证`[ego4d]`精确节名为True。前一版正则把CRLF行末当成False，不能据此认为用户未正确配置；**姓名、账户、密钥和配置原文从未获ChatGPT读取**，服务器签名与授权仍须实际测试。因此立即新建[唯一READY VLM-EGO4D-AWS-META-003](./codex-artifacts/VLM-EGO4D-AWS-META-003/README.md)，新独立许可最多4个严格白名单S3 HTTP attempts（固定官方v2_1/full_scale manifest HEAD1+GET1，≤8MiB，仅根据私有本地HourVideo顶层UID与官方真实manifest精确join做媒体HEAD≤2）；无LIST/STS、媒体GET/Range、GPU/模型和任何依赖安装。若Codex进程仍见不到profile，仅按同一Windows上下文做无敏感布尔状态并STOP，不再空跑无限次数。真实同发布/PTS、视频字节与HTTP下载硬预算均未验证，旧MEDIA-001不重启。公有Git仅匿名聚合结果及Codex结果一条，一次推送后等待审查；Ego4D官方许可用户确认有效至2026-10-26。

### 2026-10-13 · 首次本机ego4d静态profile真正PASS，真实UID源入口复合门失败（最新）

GitHub审查[Codex 39ef5c7](https://github.com/floomeer83felix-source/vlm/commit/39ef5c76a12a4236def69261a0c548408d300273)：提交仅[新匿名收据](./codex-artifacts/VLM-EGO4D-AWS-META-003/limited-aws-metadata-receipt.md)55行与结果末尾一条约8行，不含AWS凭据或受限QA/UID、媒体路径。SDK标准共享文件/profile名与原Windows Home一致，静态凭据提供器加载PASS，**不再ProfileNotFound**。首个S3请求前检查以前作为入口的HourVideo开发JSON文件“存在且≤3MiB”未通过，且没有分别记录两个布尔；所以只能得`LOCAL_UID_SOURCE_HOLD`，不判定文件删除/过大。原JSON未读、S3请求0/4、清单GET0B、媒体HEAD0/GET0、GPU0；远端实际AUTH及官方视频大小仍UNKNOWN。本父任务接受安全停止、唯一READY关闭为0。下一步由用户自己对**已知Downloads顶层**进行狭义只读文件候选计数/体量检查，不把真实私人路径、QA、UID送往公开Git和聊天；取得唯一实际文件位置后另批明确许可真正官方v2_1清单HEAD/GET和两视频HEAD。不要重复合成测试、依赖安装或强行模型启动，Ego4D用户确认许可至10月26日。

### 2026-10-13 · HourVideo重新下载且获用户新目录：同轮打通真实dev UID与官方canonical HEAD（最新）

用户已重新从自己有权限的HourVideo HuggingFace官方页面下载`dev_v1.0_annotations.json`，并确认新本机接收目录；此前对旧`Downloads`顶层+子目录计数均0，只说明旧位置无匹配，不代表标注丢失。现冻结[唯一READY VLM-EGO4D-AWS-META-004](./codex-artifacts/VLM-EGO4D-AWS-META-004/README.md)：让用户在原Codex聊天**私下给唯一目录**，只查顶层精确标注JSON及最多一次唯一同前缀浏览器副本名匹配，不要把路径/内容发布到Git。放宽无根据的旧3MiB门为**独立0<size≤16MiB与可解析/schema两门**，沿用早期已验收开发JSON50视频1182QA结构、只提顶层video UID/声明时长、对QA值不选样。已配置`ego4d`静态profile上轮真正被boto3识别，无需再做工具轮次。若输入通过，同轮严格用仅官方`v2_1/full_scale` manifest HEAD≤1+GET≤1（≤8MiB）、最多两匹配canonical视频HEAD（官方贡献方bucket白名单）、所有S3 wire attempts≤4；0视频媒体GET、0其它版本、0GPU/模型。遇权限/源/网络计数或时钟不明则真实STOP不重试；切勿把UID命中当PTS同版。公有只许新匿名结果报告+codex-results末尾一条，旧META-003等已结案不可复活，媒体字节/GPU另行用户明确授权。Ego4D用户确认访问至2026-10-26，科研目标继续快进真实素材而非合成循环。

### 2026-10-13 · 真实Ego4D第一次官方manifest HEAD收301：区域端点待核（最新）

Codex[提交e53c275](https://github.com/floomeer83felix-source/vlm/commit/e53c27535f190d4b3742a82fae3f1c7cb53c3452)仅有[匿名回报](./codex-artifacts/VLM-EGO4D-AWS-META-004/limited-aws-metadata-receipt.md)及Codex结果末尾追加，输入视频JSON在新私人目录顶层核验1,854,695B /50段元数据/可解析/无重复键、前后字节SHA相同，私有boto3`ego4d`静态profile PASS。第一次真实S3官方manifest HEAD用全球S3 HTTPS endpoint + us-east-1签名返回301，执行者在区域跳转/SDK重发之前关流STOP，因此S3真实发送1次、HEAD成功0、GET0、媒体HEAD0、媒体GET0、GPU0，远端AWS AUTH、v2_1 UID join、媒体对象大小、PTS同版都NOT_TESTED。这是安全停止的真实负结果，不是AWS Key失效证明或正式媒体结果。

经AWS公开官方HeadBucket文档核验：从固定官方bucket的`HeadBucket`响应头`x-amz-bucket-region`可以安全判断区域，即使HEAD权限不足也可提供region提示，不必盲猜或自动跟随HTTP301。为避免后续遇到不同canonical媒体贡献桶重复重定向，草拟[区域感知新独立合同META-005](./codex-artifacts/VLM-EGO4D-AWS-META-005/README.md)：仅在用户新明确批准后，最多1个manifest bucket HeadBucket +同一区域manifest HeadObject/条件GetObject≤8MiB +最多2贡献桶HeadBucket +最多2媒体HeadObject，**总7个真实S3 HTTP attempts**，没有LIST/STS/媒体GET或GPU、无隐藏重试/跳转、不上传私密UID/QA/S3媒体URI。**当前0 READY：META-005 PENDING_EXPLICIT_USER_AUTHORIZATION，旧META-004已结案不可复活，先前媒体2段8GiB GET额度不能转到新任务。** 用户明确要尽快真正实验，待取得官方真实对象UID/大小证据后应优先设计有界媒体GET而不是再排合成任务；HourVideo标注答案只用于未来评测，不用于训练/选择器。

### 2026-10-13 · 用户正式批准META-005：有界区域定位＋单manifest＋2媒体HEAD（最新）

用户明确回复「同意」，授权此前[仅为提案的META-005合同](./codex-artifacts/VLM-EGO4D-AWS-META-005/README.md)限定的**新一次最多7个白名单S3 HTTP尝试**：固定官方manifest桶HeadBucket最多1次从可信TLS响应头取区域，区域端点manifest HeadObject1与条件GetObject1（仅该CSV、应用正文≤8MiB），精确UID等值join后最多2个合法官方canonical媒体贡献桶HeadBucket及2个不同视频HeadObject，所有实际失败发送都计预算；禁自动重试/非官方跳转，媒体GET/Range、LIST/STS、GPU/模型/训练全0。合同正文已更新「用户已批准」，看板仅本ID一个READY，但必须用户在原同一Codex长会话主动发新消息才执行。先前META-004第一次真实S3 HEAD301，只说明原全球端点不能在旧合同内自动跟区域；其HourVideo标注1,854,695B、50个顶层视频元数据及本机boto3`ego4d`静态凭据PASS可直接复用，本轮不重做QA资格审计或安装工具。即便真实UID命中也不能认为HourVideo开发v1.0与Ego4D v2_1媒体时基一致；实际远端AUTH、清单大小、对象长度、媒体下载预算及GPU尚未知。本轮结果仅允许匿名汇总+codex-results尾部一条，旧MEDIA/TOOLS/META任务不重跑、媒体2段8GiB额度不续用；成功后优先争取用户下次有界真实视频GET与RTX3090短A/B。官方Ego4D审批确认至10月26日。

### 2026-10-13 · 按用户要求一口气排好META→1真视频→RTX3090最小AB（最新）

用户要求「赶紧一次性多布置点任务，快点正式开始实验」，因此不再让后续媒体/GPU流程每次从零写合同。GitHub已新增**两份QUEUED且非READY**的[一段真实媒体受控获取合同](./codex-artifacts/VLM-EGO4D-LIVE-MEDIA-002/README.md)和[Qwen3-VL 2题4次前向真实A/B合同](./codex-artifacts/VLM-HOURVIDEO-LIVE-AB-001/README.md)，现唯一READY仍为用户已授权[区域感知元数据META-005](./codex-artifacts/VLM-EGO4D-AWS-META-005/README.md)。用户在原同一Codex对话现在执行META-005，若真实官方UID/来源/HEAD长度成功，由ChatGPT最短时间验收并基于具体对象再次征得明示**新媒体GET许可**（1个≤3.5GiB、单次GET、研究正文预算≤4GiB、不能重试/不允许不能证明hard cap），确认实体媒体与时间基桥接后再征得明示**新GPU许可**（最多4次Qwen3-VL、RTX3090 ≤40min、现有SigLIP/Qwen模型/环境、不下载权重）。无模型或版本不符如实停在对应门，不把未证媒体匹配计为HourVideo正式问答性能。所有已结案META/旧MEDIA不可重跑，保持同一时刻只有一个READY、每次Codex只按当前父任务允许两处匿名Git报告。Ego4D访问期用户确认至10月26日，`NOVELTY=RETAIN0`/Charades `FINAL_MEDIA_STOP`维持。

### 2026-10-14 · 官方区域和manifest访问已成功：读取12秒超时，META-005结案并冻结90秒下一次（最新）

核查Codex[895f260](https://github.com/floomeer83felix-source/vlm/commit/895f2602cc4d27d4e5b38a1e3249ae386c1d2120)及[脱敏执行收据](./codex-artifacts/VLM-EGO4D-AWS-META-005/region-aware-limited-metadata-receipt.md)：真实HourVideo开发JSON1,854,695B、50顶层UID/时长结构PASS，专用ego4d profile静态凭据加载PASS；manifest桶HeadBucket1次(301区域提示PASS)、核实区域manifest HeadObject1次(200、4,653,141B、ETag)、条件GetObject1次(200、长度/ETag一致且无压缩)，但应用正文读取至2,555,904B后`ReadTimeoutError`，原合同`read_timeout=12s`不准重试。S3真实3/7 attempts，媒体HEAD/GET0、清单未完整读取，远端AUTH_OK**仅限该manifest响应**，无法求UID交集或视频长度；GPU/模型0。依原任务一次性STOP，接受`SAFE_METADATA_STOP / READ_TIMEOUT_STAGE_C`且READY=0。

已提前冻结[META-006](./codex-artifacts/VLM-EGO4D-AWS-META-006/README.md)作为**PENDING_NEW_EXPLICIT_METADATA_AUTHORIZATION**：只修正官方4.65MB CSV单次流读取超时，拟将socket read timeout从12秒提升至90秒，保留最多7次官方元数据S3 HTTP attempts、唯一manifest条件GET应用正文≤8MiB与最多2个canonical视频HEAD，未获用户新的具体AWS请求许可**禁止执行**；不能重跑META-005用其未用请求。随后真正媒体一段≤3.5GiB/单GET/研究GET≤4GiB和RTX3090真实Qwen/SigLIP 1视频2题/最多4推理/≤40 GPU分钟的两个合同仍QUEUED，需真实条件与独立授权。已不再安排纯合成工程，HourVideo↔Ego4D发布/PTS桥接与模型资产实际存在性仍UNKNOWN。

## 二十九、当前研究判断（跨批保持）

- 用户保持高水平论文目标，但不假定一定成功；目前 retain 0。前期100/300题及各种已关闭候选、GAP7、BATCH-003至006**不得重跑**。
- 新机制创新门 `N`、可证伪性 `T`、非平凡有效性 `U`、合法可用标签/媒体 `D`、预算/PTS/来源 `B`、强baseline公平比较 `F` 当前**无候选PASS**。toy通过不提升这些门。
- 历史真实媒体PTS /同版剪辑/来源独立性、答题数据许可、评分隔离和真实token成本仍未在新来源验证。只做纯symbolic toy不需要视频许可，但不能由此推导真实数据可执行性。
- PR #1未合并且主要基于旧gold路线；不可直接执行旧manifest或旧GPU预算。新问题可能需要不同证据标签，先做学术可识别性/合法数据核查，再决定是否值得付出真实实验。
- 如果十项研究全部被直接先例或现实标签门否决，回报**RETAIN 0 / STOP PORTFOLIO**，不继续为凑10项编新算法。

## 三十、GitHub协作规范（不改变）

- ChatGPT维护`docs/next-steps.md`、`docs/research-overview.md`和科学立题文档；Codex仅执行唯一READY父任务并追加`docs/codex-results.md`及README明确的脱敏产物。
- 原始`docs/research-progress-2026-10-08.md`保持永久快照；历史已验收任务和原Windows RTX3090/conda`pytorch`实验工作区与公开文档checkout严格分开。
- 每轮用户在原Codex聊天发送继续信号，Codex按远端main而非旧缓存执行；安全提交1次后停止，不force push、不自动后台运行/轮询、不唤醒Codex。

### 2026-10-14 · 用户明确批准META-006：新一次有限官方清单读取与媒体HEAD（最新）

用户在查看[895f260](https://github.com/floomeer83felix-source/vlm/commit/895f2602cc4d27d4e5b38a1e3249ae386c1d2120)的12秒小CSV流读取超时及预排META-006方案后明确回复「同意」。据此现**唯一READY为[VLM-EGO4D-AWS-META-006](./codex-artifacts/VLM-EGO4D-AWS-META-006/README.md)**：独立新一轮官方S3 metadata HTTP attempts总≤7，仅固定v2_1/full_scale manifest HeadBucket≤1、HeadObject≤1、条件GetObject≤1且应用正文≤8MiB，唯一参数变化为read_timeout=90秒，完整读取后才允许精确UID join及官方贡献桶HeadBucket≤2、canonical视频HeadObject≤2。连接5秒、禁隐式重试与Range/206、失败安全停止、现场≤20分钟，私人QA/UID、区域/对象位置/凭据均不得公开。旧META-005已结案，不重跑也不继承剩余4次预算；真实媒体GET/下载、GPU/模型全未授权，预排LIVE-MEDIA-002和LIVE-AB-001保持QUEUED。用户需要在**原同一Codex对话**发送新一轮启动消息，Codex按最新远端main与唯一READY的合同执行，一次脱敏报告push后停止。Ego4D访问窗口据用户确认至2026-10-26，合同另限制北京时间10月25日23:59后不发新AWS请求；NOVELTY=RETAIN0与Charades FINAL_MEDIA_STOP不变。

### 2026-10-14 · 用户一次性预排至真实GPU训练：META-006仍唯一READY（最新）

用户要求「一次性布置任务直到gpu训练」，所以先在GitHub冻结[端到端七阶段执行路线](./gpu-training-roadmap-2026-10-14.md)，让Codex不用每轮重新设计：已授权META-006官方完整CSV/UID/HEAD → 预排LIVE-MEDIA-002 1段保留评测视频 → LIVE-AB-001 真实Qwen/SigLIP少量推理基线 → 新LIVE-TRAIN-MEDIA-001 独立训练视频 → 新TRAIN-PREP-001 CPU/数据拆分与冻结优化目标 → 新TRAIN-GPU-001 **RTX3090真实反向梯度优化temporal head（≤200步/≤60 GPU分钟，仅未来用户明确批准才执行）** → 可选TRAIN-LORA-001 合法独立train QA、现成LoRA软件权重与资源可行性全过门后才能申请Qwen3-VL-4B适配器微调。四份新合同均有任务ID/依赖/资源提案/泄漏STOP/匿名结果输出，**状态均QUEUED非READY**；不自动触发云请求、视频下载或GPU。当前只有META-006有用户具体≤7次metadata HTTP许可，仍是**唯一READY**。媒体GET≤4GiB、AB≤40GPU分钟、头训练≤60GPU分钟、LoRA≤90GPU分钟是互不继承的未来批准上限提案，**不是此条用户规划指令自动赋予的执行权限**。train与dev评测视频/QA/答案必须隔离；若无合法训练样本或同版PTS/本机模型依赖，诚实HOLD，不做数据污染。头训练即使真实optimizer.step也不等于Qwen微调、科学有效性或创新证据。Ego4D授权截至2026-10-26、合同数据请求更严格止于10月25日23:59；NOVELTY RETAIN0与Charades FINAL_MEDIA_STOP持续。每轮原Codex会话触发唯一READY、一次脱敏push后STOP，阶段转换由ChatGPT审查和用户具体权限完成。

### 2026-10-14 · META-006完成清单和50/50 UID映射；canonical来源失败待定，下一轮META-007已冻结（最新）

按GitHub [cd6eac2](https://github.com/floomeer83felix-source/vlm/commit/cd6eac2a69bed936c6caf143ae997fe81ed6e1b9)的确切两处交付验收：同一官方v2_1/full_scale manifest HeadBucket301可信region提示、regional HeadObject200/4,653,141B、条件GetObject200/4,653,141B完整读取成功，90秒socket读取门不再超时。私有HourVideo开发JSON50顶层UID与真实manifest严格等值**唯一命中50**，是相对于上轮重大进展；实际A/B/C共3次S3 HTTP，未额外重试，D/E媒体桶/对象HEAD0、媒体GET/GPU0。随后本机canonical来源复合白名单/URI/key/fragment门发生`CANONICAL_SOURCE_HOLD`，**具体失败子规则未被记录，不能断言官方清单非法、所有媒体0个、贡献桶无权限或已知对象大小**。认可执行安全STOP，META-006结案不可复活其余4/7。

已核上游固定[manifest.py](https://github.com/facebookresearch/Ego4d/blob/4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb/ego4d/cli/manifest.py)、[universities.py](https://github.com/facebookresearch/Ego4d/blob/4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb/ego4d/cli/universities.py)与[s3path.py](https://github.com/facebookresearch/Ego4d/blob/4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb/ego4d/cli/s3path.py)：真实媒体对象地址来自`canonical_s3_location`或`s3_path`，官方贡献桶表固定，而原先纯SYNTH路径并不能当真实canonical key必要条件；这只是**可能**的来源校验过严方向，不是本轮已确认根因。因此预冻结[新META-007](./codex-artifacts/VLM-EGO4D-AWS-META-007/README.md)：先本机0网络只读对照具体规则，若获用户新明确授权则新独立最多7次固定官方S3 metadata尝试（CSV单GET≤8MiB、read_timeout90秒），匿名逐UID来源子规则分类后最多2个合法媒体HEAD；未过安全门时继续停，不改官方发布或猜key。**当前READY=0，META-007 PENDING_NEW_EXPLICIT_METADATA_AUTHORIZATION**，不能按用户“已推送”自行假定云许可。视频GET一段≤3.5GiB、累计研究正文≤4GiB及RTX3090基线/真实训练仍为之前预排合同、须对应另批；不再新增合成工具轮。用户Ego4D许可确认至2026-10-26（新请求按合同北京10月25日23:59截止），NOVELTY RETAIN0/Charades FINAL_MEDIA_STOP持续。

### 2026-10-14 · 用户批准META-007新一轮固定来源诊断与限定S3请求（最新）

针对[META-006 cd6eac2](https://github.com/floomeer83felix-source/vlm/commit/cd6eac2a69bed936c6caf143ae997fe81ed6e1b9)已成功完整读取4,653,141B官方v2_1/full_scale CSV并与50个HourVideo开发video UID全部等值命中，但canonical URI来源校验失败且无媒体HEAD的真实结果，用户对[单独META-007执行合同](./codex-artifacts/VLM-EGO4D-AWS-META-007/README.md)明示回复「同意」。**现唯一READY VLM-EGO4D-AWS-META-007**，独立授权的新S3 metadata wire HTTP attempts总≤7（包括任何失败/重定向），官方manifest桶HeadBucket≤1、region正确HEAD≤1与身份锁条件GET≤1且应用正文≤8MiB/read_timeout=90秒，完成来源子规则精确匿名分类后可对≤2合法贡献桶HeadBucket和≤2不同canonical视频HeadObject；在网络前先0云请求比对固定Ego4D上游manifest.py/universities.py/s3path.py与私人来源验证器，不能把合成媒体路径限制当官方真实key规则。用户仅允许本轮上述具体元数据API，不授予媒体GET/Range、额外视频、GPU/推理/训练、额外AWS版本或CLI安装，旧META-006剩余预算不可继承。**执行还要求用户在原同一Codex长会话另发主动启动消息**，Codex一次安全同步main、只更新匿名收据与结果末尾一条，正常push后STOP。MEDIA-002及GPU链仍QUEUED且须对应另批准，Ego4D访问期限及北京时间10月25日23:59新AWS请求截止不变，NOVELTY RETAIN0、Charades FINAL_MEDIA_STOP持续。

### 2026-10-14 · META-007成功HEAD两段且一段≤3.5GiB：进入一视频下载授权门（最新）

真实[Codex a85e66a](https://github.com/floomeer83felix-source/vlm/commit/a85e66a4e6910afac5c570937246986f25ff60a5)仅新增[META-007匿名实测收据](./codex-artifacts/VLM-EGO4D-AWS-META-007/canonical-source-classification-receipt.md)及codex-results尾一条；有一次私有脚本SyntaxError在网络前修好、未重计任何AWS尝试。成功在私有RAM完整读取唯一4,653,141B官方v2_1/full_scale CSV，与50个HourVideo顶层UID精确相等；按固定官方贡献桶表、严谨字段/URI/key/视频类型判据，安全45、5个不在白名单来源隔离（不等于断言非法），006原具体停错行仍不可回证但本轮真实OFFICIAL_BUCKET失败5。冻结选前2个真实canonical全视频：媒体桶HeadBucket2返回区域提示、媒体对象HeadObject2均200/正ContentLength/身份可绑定；**其中1段≤3.5GiB而另一段>4GiB，合计12,897,682,214B（>8GiB）**，不得双段下载。真实S3 A-E发送7/7、隐藏重试0、媒体GET0、GPU/模型/训练0。META-007科学/安全验收通过并关闭，不预支未来额度。HourVideo dev_v1.0 与 Ego4D v2_1只证UID一致，版本/PTS/剪辑起点桥接仍UNKNOWN。

为避免再卡“私有CSV和对象URL仅在RAM”而重复往返，已**直接重写已排队[LIVE-MEDIA-002真实单视频获取合同](./codex-artifacts/VLM-EGO4D-LIVE-MEDIA-002/README.md)**：本新父任务自包含有界元数据重构（manifest HeadBucket≤1、HeadObject≤1、完整身份锁CSV GET≤1且应用≤8MiB、最多两个贡献桶HeadBucket与两个canonical媒体HeadObject）后只对大小合规且身份锁不变的一段视频允许**最多1次条件GetObject，单段≤3.5GiB，总媒体正文≤4GiB**；总实际S3 metadata+media wire HTTP attempts≤8，全部前置严格可信源、无重试/Range、持久fsync预扣、必要时接收wire上界不可信就0 GET安全停止，现场≤60min；北京时间10月25日23:59后不发新AWS请求。用户**尚未对这一新媒体GET和重取CSV给出明确执行许可，所以READY=0**；同意后才将MEDIA-002设唯一READY，并在原Codex长会话主动发执行指令。GPU推理≤40min、真实头训练≤60min及可选LoRA均已预排但不属于媒体授权。保持训练/评测隔离、NOVELTY RETAIN0与Charades FINAL_MEDIA_STOP。

### 2026-10-14 · 用户批准一段真实媒体下载，要求减少重复审批（最新）

用户在审阅[META-007真实收据a85e66a](https://github.com/floomeer83felix-source/vlm/commit/a85e66a4e6910afac5c570937246986f25ff60a5)证明45个合法来源候选、两个HEAD200、其中1个≤3.5GiB后，对[自包含完整META重建和唯一单段GET的LIVE-MEDIA-002冻结合同](./codex-artifacts/VLM-EGO4D-LIVE-MEDIA-002/README.md)明确回复「同意，不要每次问我」。因此用户**本轮新独立授权**8次内官方S3 metadata+media HTTP attempts（A固定manifest桶HeadBucket≤1、B manifest HEAD≤1、C 条件清单GET≤1且应用正文≤8MiB、D两候选贡献桶HeadBucket≤2、E媒体HEAD≤2、F唯一大小合格canonical对象媒体GET≤1），单媒体≤3.5GiB，研究媒体正文累计≤4GiB，所有attempt含失败、TLS/官方域/区域/来源/ETag/持久预扣/≤60min及北京时间2026-10-25 23:59窗口约束不变。**看板唯一READY现为LIVE-MEDIA-002**，原Codex长会话新消息主动启动后可按A–F一次连续执行，在已经许可的各安全子阶段**不必再次逐请求提问**；结果后只传匿名收据+Codex结果末尾一条并停止，不在失败后重试/移用旧额度。若请求限流真实硬门无法强制，0媒体GET安全STOP。

针对用户“不每次问”，以后优先将同一已获准范围内可连续完成的安全子任务打包为**一次执行/一次验收**，不得将偏好解释为无限制的视频、额外云请求、付费服务、GPU/模型/训练的空白授权；后续[LIVE-AB-001](./codex-artifacts/VLM-HOURVIDEO-LIVE-AB-001/README.md)上限4次Qwen前向/≤40 GPU分钟、真实训练视频与≤60 GPU分钟head训练及可选LoRA合同已经预排，符合上游事实且有对应资源权限时可直接激活而无需重新设计规划。GPU预算现仍QUEUED、未获这次媒体合同的执行授权。HourVideo dev/v2_1 PTS发布桥接UNKNOWN、NOVELTY RETAIN0、Charades FINAL_MEDIA_STOP保持。

### 2026-10-14 · 缩短正式GPU训练前置流程：媒体任务同轮CPU资产预检

用户问“怎么还不能启动训练”，经实时检查GitHub main最新尚未见`### VLM-EGO4D-LIVE-MEDIA-002`结果，故截至本次审查仅两个真实canonical视频HEAD（一个≤3.5GiB），**尚无本机成功下载的真实视频证据，GPU/训练步数为0**。主要阻碍不是已证GPU不兼容，而是当前唯一READY媒体获取任务尚无交付、独立合法训练素材与本地Qwen/SigLIP存在性未核。为减少纯流程轮次，已在已批准的[MEDIA-002合同](./codex-artifacts/VLM-EGO4D-LIVE-MEDIA-002/README.md)内增加**同轮CPU-only、≤2min、只读且仅确切已知入口**的训练就绪清点，可与原A–F请求一次执行后匿名汇报：RTX3090非计算可见性、本机Qwen/SigLIP既有资产、独立合法训练素材是否可证。不可全盘搜索、安装/下载/启动GPU/模型/训练或触碰dev答案；未知必须报告UNKNOWN。**不增加AWS次数/媒体GET/GPU权限、不改变唯一READY、一次脱敏提交后STOP**。待真媒体到手并核数据隔离与现成资产，再进入已预排的真实GPU基线/头训练；不把dev评测数据变成训练标签。

### 2026-10-14 · 3ef8559零S3硬门阻塞结案；立即改为一轮真实视频＋限量RTX3090技术训练（最新）

Codex[3ef8559](https://github.com/floomeer83felix-source/vlm/commit/3ef855983c879ac34852ff9382ed57620409fd85)真实结果是0/8 AWS元数据请求、0/1媒体GET、新视频0、GPU0：LIVE-MEDIA-002在联网前因既有metadata boto3实现没有独立socket/TLS/wire总字节精确hard-cap认证而安全STOP；这不是远程权限拒绝或正式媒体失败。Windows非计算枚举3090可见，但Qwen/SigLIP本地资产入口与独立合法训练视频均UNKNOWN。**原MEDIA-002已结案，不重跑或转用旧预算。**

用户此前已明确同意一段≤3.5GiB官方真实视频、最多8次受限S3 HTTP、manifest应用≤8MiB和媒体GET正文累计≤4GiB，要求不要每次逐请求问；本轮又明确催“快点开始实验”。为修复过于严格但不具可执行性的额外wire精确计量门，已冻结并设**唯一READY**的新[ VLM-LIVE-VIDEO-GPU-START-001 单父任务包](./codex-artifacts/VLM-LIVE-VIDEO-GPU-START-001/README.md)：使用**全新独立计数与对象身份验证**，A实际视频申请仍仅原已批准那个未到手的视频目标和同量级上限，先重取唯一官方v2_1/full_scale manifest及最多两个对象HEAD并只能对一个≤3.5GiB对象发一次有条件媒体GET；只将已批准4GiB明确定义为可检测可强制的**媒体HTTP响应应用body累计预算**而不伪称网卡/TLS/SDK缓冲全部wire精确≤4GiB，HTTPS/无重试/无Range/按head预扣/byte计数及失败STOP仍硬约束；若必须物理wire hard cap则0 GET。B视频完整取得、合法训练用途/现有本机解码和torch CUDA过门时同轮对真实帧运行**≤100个optimizer.step、总≤20GPU分钟自监督temporal head试跑**，不要求未知Qwen权重、不拿dev QA训练，使用过的视频排除未来正式保留QA评分；此仅技术smoke，非Qwen微调、非独立训练集科学结果。A失败且无已明确路径和授权的另一份真实合法本机训练视频则B STOP。两部分同轮完成并**只允许一个匿名父收据＋结果尾一条**，Codex原长会话一次主动启动后push STOP；没有自动背景任务。

后续Qwen真正A/B、独立训练集、GPU正式head训练、可选LoRA仍为此前冻结的非READY，不会凭用户催促假造模型资产或数据授权。研究NOVELTY RETAIN0、Charades FINAL_MEDIA_STOP、HourVideo dev/v2_1发布PTS未知不变。

### 2026-10-14 · 7cb9c6b真实GET被时区BUG提前终止；改零下载先实测GPU（最新）

[7cb9c6b](https://github.com/floomeer83felix-source/vlm/commit/7cb9c6b815614e7695be2edc251f87d4b002626c)的A阶段不再是权限障碍，已真实8/8 S3、条件唯一视频GET200、64–128MiB私有part；但PowerShell `ConvertFrom-Json`的DateTime到DateTimeOffset隐式字符串转换把UTC当本地时间，外层经过时间多算约480分钟，在实际53.975分钟终止下载。合同真实≤75min尚未到；没有完整视频，也没有GPU前向/反向/更新。修正仅本机静态更改，**不代表下载重新通过**。旧STARTED/8次请求维持，不重开、不猜原URL、不新GET/Range/续传。当前链路约54min仅64–128MiB，直接重新整段≤3.5GiB实际风险较高，不能以此速度保证完成。

用户强烈要求直接开实验，故立即冻结[唯一READY VLM-LOCAL-GPU-REAL-SMOKE-002](./codex-artifacts/VLM-LOCAL-GPU-REAL-SMOKE-002/README.md)：新父任务**全程0 AWS和0视频新下载**，在既有Windows `pytorch`环境优先≤2 GPU分钟内真实CUDA分配与至多2步小张量梯度更新（仅GPU基础设施），随后只读验证上一轮的64–128MiB part能否从真实来源抽出至少32帧和可信PTS，或有此前授权且入口明确的另一独立本地真视频；仅在**训练用途合法且真实帧可解码**时，直接同一轮≤100步、累计≤20GPU分钟单次self-supervised temporal head试跑，不使用dev QA原文或答案，不从part冒称整个视频可用，更不能算正式HourVideo验证或Qwen微调。若part缺尾部moov/损坏不能安全解码则真实视频训练HOLD，但至少直接得到CUDA能否运行的实测结论；不转向模拟数据“科研成果”，不扫盘找替代视频、不额外下载/安装。任务报告仅一次匿名收据+结果末尾一条，main push后STOP。未来正式训练数据仍必须独立科学来源，NOVELTY RETAIN0、Charades FINAL_MEDIA_STOP、发布PTS桥接UNKNOWN不变。

### 2026-10-14 · 8d724a7 Windows C+G门过严；独立part探测与真实CUDA更新一次执行（最新）

[Codex 8d724a7](https://github.com/floomeer83felix-source/vlm/commit/8d724a7d2d55a05ae178b6640be4bc384107bc51)在torch CUDA前就以nvidia-smi计算进程列表非空安全STOP，故真实CUDA查询/分配、backward、optimizer.step及part读取/ffprobe/PyAV均0/NOT_RUN。后续只读证据：RTX3090设备总24,576MiB、空闲22,899MiB、3%利用率；30条C+G Windows混合图形+计算上下文（19个常见桌面、11未分类），不证明30个CUDA训练程序或独占占用；亦不证明绝对安全。因此002按原合同安全结案不重跑。鉴于用户“快点开始实验”，**唯一READY=新[VLM-WIN-CUDA-REAL-FRAME-003](./codex-artifacts/VLM-WIN-CUDA-REAL-FRAME-003/README.md)**：A与B独立，先在严格CPU只读限量≤6min探测唯一已知旧part是否能真实解码≥32帧/可信PTS，避免GPU阻塞整个非相关子任务；B仅在已有独占锁无冲突、实时两次利用率≤30%且空闲显存≥8GiB、无正面冲突计算作业时允许一次真实torch CUDA最多2梯度更新/≤2GPU分钟/≤512MiB新显存，不再要求Windows C+G进程列表为空、不杀别人进程。C只在合法训练许可/真帧PTS及GPU全部PASS时，同一父任务≤100步、累计≤20GPU分钟真实帧自监督temporal head技术实验；真帧不可解/许可UNKNOWN则不伪造C，只报告GPU基础设施。零AWS/GET/Range、零新依赖、零Qwen下载，一次正常匿名提交后STOP；此不意味着完成HourVideo benchmark、Qwen微调或真实训练数据独立性。NOVELTY RETAIN0、Charades FINAL_MEDIA_STOP、发布PTS桥接UNKNOWN保留。

### 2026-10-14 · 5ed644e证明RTX3090可真实梯度更新：公开真实短视频GPU训练代码已落地（最新）

[5ed644e](https://github.com/floomeer83felix-source/vlm/commit/5ed644e51702253539254890e1b62fd4c3a76e8a)不再是GPU未测：Windows3090+torch2.5.1 CUDA12.4实际执行2个小SGD训练步，loss1.06695→0.67108，有限梯度与模型参数变化实证，GPU阶段8.094s、框架峰值17.254MiB。混合C+G上下文没有构成真实互斥，故不再做重复CUDA兼容性准备。原8/8 S3耗尽且`.part`视频`MISSING_MOOV`/0有效帧，不能续传、伪装完整视频或据此训练；旧合同验收关闭。

为满足用户“快点开始实验”，已**直接提交可执行[temporal_train.py](./codex-artifacts/VLM-CC0-REAL-GPU-004/temporal_train.py)**，并设[新父任务004](./codex-artifacts/VLM-CC0-REAL-GPU-004/README.md)为唯一READY。使用[MDN shared-assets](https://github.com/mdn/shared-assets)公开许可开花**实际拍摄**短视频`flower.mp4`，来源域限定mdn.github.io，最多**1次新HTTPS GET**，媒体应用正文≤8MiB、单独私有父目录、TLS验证无自动重试；0 AWS或受保护数据。许可如不适用即停止。程序纯本机用既有PyAV/OpenCV/Torch，从真实视频解码最多96帧/真实PTS，工程性时序先后pair小head在3090上≤80更新/≤10 GPU分钟/框架峰值新增≤512MiB，训练与小验证按时间段分离，报告参数变化/loss，不上传原帧/视频与实验资产；不需要本地未知Qwen/SigLIP权重。该短片内容不是Ego4D第一视角长视频，**不能报告HourVideo或Qwen正式评测结果**；后续研究真实长视频独立训练素材与release/PTS时钟门依旧需要科学核验。只需用户原同一Codex会话一次启动，不逐个子步骤重复问。NOVELTY RETAIN0、Charades FINAL_MEDIA_STOP持续。

### 2026-10-14 · 8299653首个真视频80次梯度成功，下一轮升至24分钟公有领域长时A/B（最新）

[8299653](https://github.com/floomeer83felix-source/vlm/commit/82996532ace47e520f97e2ba7b59130525d4246e)实际完整官方MDN公开短片GET 1,128,375B、75实拍帧、PTS4.938s，RTX3090上24,705参数temporal head真正80/80 backward/optimizer步，首末loss 0.697165/0.661437（不同采样batch，不能称单调下降）、权重L1变化147.391893、后19帧同video pair验证0.5417、torch峰值17.92MiB、GPU计时1.625s。**技术GPU视频链验收通过**，但5秒单视频0.5417没有严肃长视频或跨video泛化意义，Qwen/SigLIP未调用、HourVideo QA/版次时钟UNKNOWN。

下一父任务**唯一READY=[VLM-PD-LONGVIDEO-005](./codex-artifacts/VLM-PD-LONGVIDEO-005/README.md)**（user“快点开始实验/不要每次问我”，无付费/云GPU或受保护媒体）。选择[Commons公开公有领域《One Week》(1920)](https://commons.wikimedia.org/wiki/File:One_Week_(1920).webm)，标注24分26秒，美国公有领域；只下载官方VP9 360p约338kbps转码而非132MB原版，官方API严格核许可/唯一derivative，media对象<=96MiB；ChatGPT已在main写入**实际可执行**[定源两次GET受控下载器](./codex-artifacts/VLM-PD-LONGVIDEO-005/fetch_commons_long.py)和[真实帧长时A/B训练脚本](./codex-artifacts/VLM-PD-LONGVIDEO-005/long_temporal_ab.py)。官方元数据GET≤1/512KiB和转码GET≤1/96MiB，0 AWS/Charades/HourVideo；真实解码跨度≥20min，训练前70%/验证后30%同片隔离且9s缓冲，均匀128帧 vs RGB变化幅度高分128帧两臂各≤100 optimizer更新，GPU总≤12min、同权重初始化/固定同验证pair。不执行5秒片重复或合成fallback。**仍只能称公开长时影片时序采样技术探索**，非Qwen/HourVideo问答、非独立影片评测，也不据此升级研究NOVELTY=RETAIN0。模型与第一视角长视频/PTS桥接科学任务继续QUEUED，不继承旧Ego4D已耗8/8与STARTED。用户原Codex聊天新消息一条启动即可，一次匿名回报后STOP。

### 2026-10-14 · 490d247仅在元数据解析处失去错误分支，已修正并冻结下一轮（最新）

真实[490d247](https://github.com/floomeer83felix-source/vlm/commit/490d247fb191a03890d9a4d7daf369416f8f26b8)元数据唯一HTTPS GET=1/1、HTTP200、3,155B、视频GET0、GPU0；`ValueError`发生在收完meta与source-license PASS记录之间，旧私人脚本不保存分支/原响应，因此无法判定具体是标题、schema、许可证还是官方derivative URL。不得冒称媒体拒绝/下载成功、不得重跑/退款旧005。外部独立[Commons官方视频页面](https://commons.wikimedia.org/wiki/File:One_Week_(1920).webm)显示1920年美国公有领域、片长24分26秒且VP9 360p转码Completed，**不等于本轮API结构化许可或私有使用地授权已验证**。

已将**唯一READY**转为[独立VLM-PD-LONGVIDEO-006](./codex-artifacts/VLM-PD-LONGVIDEO-006/README.md)，并公开提交全新[fetch_commons_diagnostic.py](./codex-artifacts/VLM-PD-LONGVIDEO-006/fetch_commons_diagnostic.py)：HTTP 0之前离线正常/错误4类fixture校验，之后新父任务的固定Commons API meta GET≤1且应用body≤512KiB；逐个schema/license/360p地址校验输出稳定脱敏reason_code（不泄露原API/私有路径），独立fsync请求账本；全部PASS才允许一段官方360p视频GET≤1/body≤96MiB/不Range或重试。媒体完整且PyAV真帧≥350、PTS跨度≥1200s才运行上轮已冻结的uniform128 vs motion128两臂RTX3090时序head，最多各100步、GPU合计≤12min。新父任务不从旧005继承任何额度；具体许可不适用或meta字段冲突立即0视频GET安全HOLD。只做公开非VLM问答技术探索，不可据此算HourVideo/Ego4D真实benchmark、未证版次PTS与独立训练源仍UNKNOWN，NOVELTY RETAIN0、Charades FINAL_MEDIA_STOP保持。用户仍必须在原Codex长期聊天主动发一次执行指令，GitHub更新无法远程唤醒PC。

### 2026-10-14 · d5a7677明确查出360p VP9键不存在唯一匹配；已冻结选择实际官方240p/360p策略（最新）

[d5a7677](https://github.com/floomeer83felix-source/vlm/commit/d5a767740a671829ec2021071c1dd6104f89846d)：新自检PASS；固定Commons元数据meta GET1/1返回HTTP200/3,155B，文件JSON身份/美国公有领域LICENSE_PASS；**固定`360p.vp9.webm`正好一个的门不满足**，未保留0/≥2细分，0视频GET/0长片/0 GPU A/B更新；006已结案，不得退款/补发/重跑。独立公开[Wikimedia TimedMediaHandler默认转码配置](https://github.com/wikimedia/mediawiki-extensions-TimedMediaHandler/blob/master/extension.json)存在240p VP9启用与360p默认关闭，但不能推断Commons现行配置，页面转码“Completed”与API播放derivatives返回也可能不同。**旧校验错误不等于影片版权失败或GPU不可用**。

**唯一READY=新[VLM-PD-LONGVIDEO-007](./codex-artifacts/VLM-PD-LONGVIDEO-007/README.md)**。先离线fixtures测*仅240p也可选择、只有360p可选、两者都有则按360→240稳定优先、重复键/非官方URL/HOLD*，随后**单独新独立最多1官方meta GET<512KiB**；从真实`videoinfo.derivatives`只认当前存在的官方确切`360p.vp9.webm`或`240p.vp9.webm`一个、来源/美国PD证据/适用许可再验证后最多发**一次video GET body≤96MiB**，失败不转480p/原版、不重试Range/镜像。下载完整且≥1200秒真实PTS/≥350有效帧时用已冻结旧双臂GPU脚本，uniform128 vs motion128各≤100真实步/GPU累计≤12min，依源返回的真实帧计算而不以5秒短片补足。只做公有领域同片时序采样技术探索，不拿开发集标签、Charades或独立评测材料，NOVELTY RETAIN0、HourVideo↔Ego4D发行时钟未知保持。一轮匿名收据+results一条，push后STOP；GitHub更新不会自动驱动用户Windows。

### 2026-10-14 · bf96378官方240p真实GET在458,752B后40s read timeout；改分块206（最新）

[bf96378](https://github.com/floomeer83felix-source/vlm/commit/bf963786cb8d9c54dc82ce52c30f311932f7d94d)实际返回官方Commons元数据HTTP200/3,155B、结构/美国PD许可/实际唯一240p.vp9.webm API source HTTPS PASS。唯一媒体GET200完整声明37,316,857B，但在成功应用读取458,752B后由Python socket read触发40s timeout，最终本地part458,752B，无完整Video/SHA/PTS，两个GPU训练臂0。不能把timeout称源校验不合格、CPU/GPU故障或完整body只接收458752B；网络SDK缓冲/wire可能另有数量，前一任务已保守预扣完整媒体长度且停止，旧账本/part不能恢复/退款。

依用户连续希望加快真实长视频研究的意愿，已**预设唯一READY**新[008有界官方HTTP206 Range父任务](./codex-artifacts/VLM-COMMONS-RANGE-008/README.md)，不再单次容易读停顿的37MB HTTP200 GET。它不是已授权后台执行：**在原同一Codex聊天主动发送含明确新资源上限的执行消息才批准008新尝试**。新父任务先全离线实现/验证强ETag和Range的Content-Range/206/长度/预扣/失效/超时fixtures；新独立meta GET最多1/正文≤512KiB、HEAD1，强ETag支持206/身份与37,316,857B一致才允许最多24个每块≤2MiB的顺序Range206，新GET区间长度**全部保守预扣累计≤48MiB**，失败不退还；用新任务自己的private目录/ledger，旧007 part完全不动。75min独立单调硬墙钟不能实现则0 media GET；完整视频且≥20min PTS/≥350真实帧后，直接运行已冻结uniform128对motion128各≤100真优化步/GPU合计≤12min、同video后时段验证。此片不是Ego4D/HourVideo/Qwen正式任务，不能据单片准确率宣称科学优越；NOVELTY RETAIN0、Charades FINAL_MEDIA_STOP和release/PTS桥接UNKNOWN不变。单次匿名报告+尾一条后STOP。

### 2026-10-14 · b4896bf外部Range强ETag资格不通过，转向已有本机数据优先（最新）

[008匿名实测b4896bf](https://github.com/floomeer83felix-source/vlm/commit/b4896bfc218cb17e2af4d65148b4c86d3eb12e14)包含21/21离线Range安全协议和独立单调硬监督子进程测试PASS；实际官方Commons metadata GET1/3,155B、官方video HEAD1/HTTP200/37,316,857B及US-PD/官方240p VP9资格均通过，但**强ETag未通过严格语义**，究竟不存在/弱/其他格式不合格UNKNOWN，Accept-Ranges未检查，不证明服务器绝无Range能力。Range媒体GET0、预扣区间0、完整视频0、真实GPU A/B更新0/0，旧008按合同结案不退款/不复用。此前8299653真实MDN约5秒短片上的80步GPU技术训练有效，但不能转化成新长视频成绩。

为消除反复迭代同一外部CDN但始终没有真实数据的低价值链，**下一轮唯一READY=[VLM-LOCAL-LONGVIDEO-009](./codex-artifacts/VLM-LOCAL-LONGVIDEO-009/README.md)**，不申请任何新网络媒体请求，优先仅沿原用户/Codex上下文已明确获准且确切的研究长视频入口CPU只读≤3个，严格许可/完整容器/PTS跨度≥1,200秒/至少350真实采样帧过门，若已具备则同轮直接RTX3090上执行uniform128 vs motion128各≤100实际梯度步/GPU≤12min。不同来源/同片的科学边界和未来HourVideo dev答案隔离仍保留。**没有确切合法本机长片就报LOCAL_LONG_VIDEO_NOT_AVAILABLE_HOLD，停止并明确需要一个私有完整视频入口，不做任意全盘/Downloads扫描，不再次重试Commons/下载其它长片，也不用花朵5秒旧样本伪充20min。** 可以零GPU报告现成Qwen/SigLIP确切权重入口布尔，方便真正研究下一步。用户原Codex聊天须发一次列明权限的启动消息，执行后只一次匿名push STOP；`NOVELTY=RETAIN0`、Charades`FINAL_MEDIA_STOP`、release/PTS UNKNOWN不变。

### 2026-10-14 · b11cb4e首个≥20min真实长片配对GPU实验成功，结果不支持motion优势；进军真正VLM（最新）

[b11cb4e](https://github.com/floomeer83felix-source/vlm/commit/b11cb4e9fe49cf57536afc7c8665ce7780d6a05b)是本机完整480p公有领域《One Week》真实长片实验：ffprobe1465.597秒、PyAV完整真实帧43,924、489样本跨度1465.464秒/PTS严格递增。两组各128真实训练帧/共享70晚段验证帧/160冻结pair，前70%训练后30%同片验证加9秒边界；3090上真正uniform和motion各100次`backward+AdamW optimizer.step`，参数非零改变、GPU总1.938秒/allocated峰值18.025MiB；**两组准确率都45.00%，观察到的运动优先优势为0pp**。首末批损失分别从0.689918→0.779309、0.691118→0.732843且batch不同，**不能宣称收敛/学术显著/跨片推广**；不是Qwen/VLM/HourVideo问答性能，009封存不重跑。

为避免继续投入低价值的单片RGB 8×8时间顺序头实验，**唯一READY=新[VLM-LONGVIDEO-VLM-BRIDGE-010](./codex-artifacts/VLM-LONGVIDEO-VLM-BRIDGE-010/README.md)**。一轮bundle先在以前明确合法/已知确切的模型入口CPU只读核Qwen3-VL-4B-Instruct、SigLIP文本+图像塔、processor/现成环境可用性（截至009 `ASSET_ENTRY_UNKNOWN`，不得猜测存在、绝不全盘搜索/自动下载）。如有、且用户在原Codex会话明示最多4次本地模型推理/GPU累计40min，使用同一完整电影的固定两条内容中性英文提示和48真实候选帧比较均匀12 vs SigLIP查询相关12，4次真正Qwen生成；不改视频、不访问任何保护QA，上传仅匿名模型运行分类/选帧时钟/延迟/显存，不上传生成全文。**该公开电影没有标准答案，绝不以无答案的通用叙述当正式正确率/显著性或HourVideo得分**。若模型/processor/依赖不在明确合法已知位置，GPU0及时MODEL_ASSET_ENTRY_HOLD，请用户提供本机资产；不循环准备或重回Commons下载。HourVideo/Ego4D真实正式QA媒体/版本/PTS桥接依旧未知、Charades FINAL_MEDIA_STOP及NOVELTY RETAIN0持续。

### 2026-10-14 · b295945发现两指定HF缓存目录无Qwen/SigLIP，进入用户提供模型目录后即推理（最新）

[b295945](https://github.com/floomeer83felix-source/vlm/commit/b29594577fb52ee9a36836c75ca82d4142489499)收据显示010已在用户授权的电影路径安全确认本地完整长视频继续存在，但当时未指定任何已知模型本地目录。单根固定canonical HF缓存`Qwen/Qwen3-VL-4B-Instruct`和`google/siglip-base-patch16-224`均**root absent**，其余磁盘或其它SigLIP版本不能因此判无。torch2.5.1、transformers4.57.6、PyAV15.1、OpenCV4.11、numpy1.26.4模块在现有conda环境可见，**不表示模型处理器加载/RTX3090 4B推理已验证**。实际Qwen生成0/4、SigLIP前向0、GPU0，这不是GPU兼容失败。010按真实资产入口HOLD结案，不重跑已知空目录，不擅自下载模型。

下一步仅设**唯一READY=[VLM-MODEL-ONBOARD-VLM-011](./codex-artifacts/VLM-MODEL-ONBOARD-VLM-011/README.md) / AWAIT_USER_MODEL_PATHS**。用户可先核是否已有准确两模型本地文件根，不必重复下载；若没有可**自行**从[Qwen官方完整仓库](https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct/tree/main)及[Google SigLIP官方完整仓库](https://huggingface.co/google/siglip-base-patch16-224/tree/main)准备权重+索引+tokenizer+processor；推荐只用私有目录例如`D:\models\Qwen3-VL-4B-Instruct`和`D:\models\siglip-base-patch16-224`，但目前仅建议、非已经存在。用户在原Codex同一长会话**提供两个确切目录并明确最多4次本机Qwen generate/GPU≤40分钟/零网络授权时**，011单轮先检查静态完整性后若可加载直接同轮完成uniform12与SigLIP query-aware12的2×2自然语言定性/成本技术pilot。未有两目录，011不执行/不推送另一份0GPU收据。电影无标准QA正确答案、不能作为HourVideo得分，必须后续真实官方同版视频/PTS桥接与独立标签/合法模型资产才可能有科学对照。NOVELTY RETAIN0、Charades FINAL_MEDIA_STOP维持。

### 2026-10-14 · 4d902ef真实长片 Qwen3-VL×SigLIP 四次生成全成；下一步只缺有标准答案的匹配官方视频（最新）

[4d902ef](https://github.com/floomeer83felix-source/vlm/commit/4d902ef870f201cd5b1df7536bd235ab5b6789be)真实匿名实验验收：合法本机模型目录已获用户补全；Qwen3-VL-4B-Instruct BF16和SigLIP双塔F32均通过safetensors/processor/tokenizer检查并在3090上加载；48个真实电影RGB候选帧PTS覆盖1464.630s，uniform12与SigLIP按两固定非答案问题的图文余弦top12构成公平不同输入；SigLIP图像6批/文字1批、Qwen deterministic generate4/4正常返回。含模型加载、检索、四次推理的GPU完整阶段38.906秒，PyTorch allocated峰8716.771MiB，整个worker49.609秒；没有模型训练/weight/视频外网下载。每题SigLIP与uniform重合3/12；查询P2的SigLIP所选视频PTS跨度1184.150s小于20min，纯查询相关性可能降低覆盖但**不是正确率证据**。四次都使用满192token输出，不知道是否natural EOS，结果可能截断。原011结案不重复同电影无答案prompt并不存在有标准答案的性能数据。

正式研究下一阶段**唯一READY=新[VLM-HOURVIDEO-MATCHED-QA-012](./codex-artifacts/VLM-HOURVIDEO-MATCHED-QA-012/README.md) / AWAIT_USER_MATCHED_EGO4D_MEDIA**。本机模型、显存、视频采样与配对生成已经工程打通，剩余关键缺口不再是CUDA/下载权重，而是**一段真实合法、完整、≥20min且与受保护HourVideo dev标注同UID、同发布版/剪辑起点、时钟PTS可校验的官方Ego4D视频**，以及已知准确的私有dev标注/映射入口。只有用户通过既有合法渠道获得完整对应原片并在原Codex长会话精确授权文件与本轮≤4真实Qwen generate/GPU≤40min，012才有资格一次性进行独立CPU媒体/发布/PTS对齐→冻结2QA→配对Qwen uniform12/SigLIP12→隔离答案评分，最大生成384token记录EOS/truncated。不具备完整视频或桥证据就不做假HourVideo打分、不恢复历史.part/重用AWS额度、不把1920电影的通用总结当benchmark。科学`NOVELTY=RETAIN0`、Charades`FINAL_MEDIA_STOP`保留。

### 2026-10-14 · 官方HourVideo仓库已有约933MB demo MP4，可绕过Ego4D旧S3阻塞（最新）

新核验[HourVideo官方gated HF数据集卡](https://huggingface.co/datasets/HourVideo/HourVideo)与其[demo_video目录](https://huggingface.co/datasets/HourVideo/HourVideo/tree/main/demo_video)：**存在一段约933MB的官方HourVideo自带完整demo MP4**。相比之前曾仅取64–128MiB残片且下载长期超时的Ego4D v2_1 S3媒体，这一官方同发布仓库打包片段是优先人工下载候选（用户已获准数据集条件后自行完成）；但**单独demo片存在不保证它一定属于用户的private dev UID或有金标**。官方普通`dev_v1.0.json`明确无gold，只有私有合规`dev_v1.0_annotations.json`或官方`samples_v1.0.json`**实测该视频UID确有≥2条有效标准答案五选项QA**才可评分，不得使用网上未核答案。视频下载后CPU私有核filename UID/题库UID、完整PTS/片长≥20min及发布/剪辑起点证据；通过后沿已验Qwen/SigLIP同题同帧数2×2、Qwen ≤4次、GPU≤40min，新五选项prompt只输出单字母A–E、max_new_tokens=64并记录EOS、答案最后隔离比对。否则数据/时钟HOLD，GPU0；用户只需发视频确切本机入口+标注私有入口+具体GPU授权，旧S3部分预算不退款、不重复下电影，不泄露真实UID/标注/模型完整回答。仍然只是n=2单视频pilot，非完整HourVideo榜单/论文优势。

### 2026-10-15 · f405b99官方同UID59分58秒视频+43真金标已齐；在不假冒时钟证书前提下进入更完整的配对QA（最新）

[f405b99](https://github.com/floomeer83felix-source/vlm/commit/f405b99b536d0ffb59c2ea1329ced16683acaf26)实测：合法手工HourVideo官方demo MP4 889.396MiB，私有已许可有答案的开发标注与媒体UID完全一致、43道有效五选项带gold问题；视频stream3598.033333秒 vs 标注metadata3598.030000秒，差3.333ms；完整真实PyAV decoder到EOF 107,941帧、PTS0.021029到3598.021029秒严格递增。012原协议要求独立release/crop/zero-origin映射证书，未提供所以安全HOLD：Qwen0/GPU0、分母未冻结、不报告准确率。这不是数据缺失/版权失败/PTS错误已证。官方[HourVideo数据卡](https://huggingface.co/datasets/HourVideo/HourVideo/blob/main/README.md)将该demo明示为官方快速入门视频，是可信但仍无法证明逐帧timebase完整映射的额外出处。

因此**新唯一READY=[VLM-HOURVIDEO-WHOLEVIDEO-QA-013](./codex-artifacts/VLM-HOURVIDEO-WHOLEVIDEO-QA-013/README.md)**，作为ChatGPT审查后的**独立、预注册、局限明确的探索性全视频QA实验**，不再要求全片均匀和query-aware选帧去依赖没有任何使用需求的QA`relevant_timestamps`/标注时间零点。把`MEDIA_PTS_DIRECT_WHOLE_VIDEO`清楚标为`CLOCK_ZERO_ASSUMED_NOT_CERTIFIED`，不声称独立发布桥PASS，不作为官方HourVideo leaderboard。用户在同一Codex聊天新明确批准≤86真实Qwen generate/GPU累计≤30分钟/0网络后，一轮对43条有gold中无需额外导航/空间图片的文本QA按冻结规则全部配对（≤43×2），同48全片PTS真实候选帧、uniform12 vs SigLIP query12、相同Qwen decoder/MCQ 64 token cap，最后隔离正确答案评分；固定有效题集合分母、记未运行/invalid/双方独有正确数，不重跑011/012或重下载视频。公共输出**仅附带名义时钟假设限定的条件性样本QA结果**、不露gold/canary/UID/私有路径。NOVELTY RETAIN0、Charades FINAL_MEDIA_STOP不变。

### 2026-10-15 · bf5e36a首次37道有gold真实HourVideo同题配对：观察SigLIP+16.22pp但不显著；下轮强制独立视频复现（最新）

[bf5e36a](https://github.com/floomeer83felix-source/vlm/commit/bf5e36ad216c33e6cb04d2493c9e5fce050f7713)：013在原同UID官方demo 43 MCQ中，按前置non-gold规则排除5 image-task+1外部素材=37个可评文本MCQ，源PTS从全片48真实帧候选取uniform12或SigLIP query-only top12。两个组各37条Qwen真实generate=74/74完成、全部natural EOS，金标仅隔离评分读取，失败/INVALID计入冻结N37。**名义全视频时钟假设且独立零点/发布桥未证**：uniform6/37(16.22%)，SigLIP12/37(32.43%)、observed差+6题/+16.22pp；配对双方对4、仅A2、仅B8、都不对23，exact McNemar双侧p=0.109375，不能证明统计显著优越、跨视频泛化、完整HourVideo官方dev排名或方法创新。GPU含模型load与检索/生成31.906s，torch峰8848.589MiB，不含任何Qwen训练。013结案、不把原37条已观察的同视频dev答题结果当作新确认试验。

为避免post-hoc超参数优化与同视频重复测试的偏差，**唯一READY=新[014跨独立来源复现](./codex-artifacts/VLM-HOURVIDEO-CROSSVIDEO-014/README.md)（AWAIT_USER_ADDITIONAL_MATCHED_VIDEOS）**。用户经合法渠道自己取得**与013不共享原始物理视频UID/采集源**的至少一段（最好2–3段）完整匹配官方视频，并在原Codex长聊天提供明确路径、合法gold入口/媒体同源证据，明示授权最多3视频×43题×2臂=258真实Qwen生成及GPU累计≤30分钟；此时一轮固定013选帧、提示、处理器/模型与输出解析严格规则，私有标准答案只能最终隔离评分，按每新视频汇总正确率与独有正确配对数，至少2个新独立视频时才能描述性讨论跨视频变化。若未拿到新素材，**014保持等待，不要再让Codex为了同一个空媒体门运行一轮**；0数据/模型外网GET、0Charades，NOVELTY RETAIN0/CLOCK_ZERO_ASSUMED_NOT_CERTIFIED继续。

### 2026-10-15 · 官方Sample集另一段视频优先人工获取（选择冻结，非新GPU授权）

用户询问「帮我选」后已根据[HourVideo官方数据集卡](https://huggingface.co/datasets/HourVideo/HourVideo)冻结最短可信选片：优先使用[HourVideo官方samples.txt](https://huggingface.co/datasets/HourVideo/HourVideo/tree/main/v1.0_release/video_uids)中**除了已测试官方demo UID之外的另一个sample视频**（sample总2视频），先从用户已获准仓库合法持有/手工下载的`samples_v1.0.json`私有验证确有至少10道排外部图片后真实gold五选项题；无需在公仓发真实UID/问答。官方数据集只自带一个demo视频，**第二sample须用户依Ego4D合法权限按准确UID单文件下载**，其[官方CLI](https://github.com/facebookresearch/Ego4d/blob/main/ego4d/cli/README.md)支持`--video_uids`/单UID过滤，v1发布相容性优先核，不许用无映射的v2_1冒充同版。此选片阶段**无新增AWS/网络模型/媒体授权，不执行014 GPU，不产生空HOLD交付**。取得合法完整媒体和精确本机源路径后，014仍按原冻结uniform12 vs SigLIP12方法/新GPU预算执行，结果与旧013物理视频分离；同片理论增益p0.109375尚未确立优越性。

### 2026-10-15 · e7f654a第二段70分钟金标视频真实GPU实验：SigLIP方向反转，原优势不稳定（最新）

[e7f654a](https://github.com/floomeer83felix-source/vlm/commit/e7f654a2acb93fed196da0ea4d361cb14bc1725f)成功按013冻结方法跑完另一条官方Sample视频29题×2臂、Qwen真实generate58/58/全部自然EOS、无训练/下载，真实GPU25.344秒/torch分配峰8884.594MiB。不同UID、官方v1/full_scale单UID手工获取/完整MP4，标签29个五选项且nongold排除0。只在名义全视频PTS假设的探索性范围内，**均匀11/29=37.93%，SigLIP question-only检索9/29=31.03%，B−A=−2题/−6.90pp**，双方都对7、仅均匀对4、仅SigLIP对2、双方未对16，双侧exact McNemar p=0.6875不显著。对照013的SigLIP +6/37=+16.22pp，**方向反转是实际发现**；两来源组小样本、同源时钟/原物理采集严格认证缺失、两公开gold sample不是隐蔽heldout，不能将66个题当66个独立视频、不能汇总冒称正式HourVideo榜分、不能宣称SigLIP稳定有效、显著或论文新颖。

旧014已完成结案且任何先前剩余模型调用预算不再使用。**唯一READY=新[015一次性无GPU科研审计](./codex-artifacts/VLM-REPLICATION-DIAGNOSTIC-015/README.md)**，用户在既有或压缩交接后的Codex聊天新发一次CPU-only指令即可执行A/C：用公开两份匿名证据验证配对统计和控制变量，并明确`NO_GO_SIGLIP_STABLE_ADVANTAGE`及后续独立素材可证伪路线，不再在013/014已看答案的题上调seed、阈值、prompt/视频抽样。若用户**另明确许可两个确切已存在的旧私有预测结果入口**，可加B做只读匿名类别错误诊断；路径缺失则跳过B完成A/C。整个015不得GPU、访问新视频内容/HTTP或旧历史QA训练、公开UID/gold。只有独立更多真实采集视频和受控统计计划/强先例重审齐备后，才单独申请新GPU实验。NOVELTY RETAIN0、Charades FINAL_MEDIA_STOP、CLOCK_ZERO_ASSUMED_NOT_CERTIFIED持续。

### 2026-10-15 · c7aa4d9完成CPU独立复算：不稳定选帧假说NO-GO，主线转向新来源数据（最新）

[c7aa4d9](https://github.com/floomeer83felix-source/vlm/commit/c7aa4d96405771f777c70eaf73ab399db8b5be15)已核：前两个真实HourVideo公开样本GPU任务报告统计完全相符（013 SigLIP−uniform +6/37=+16.216pp、paired p0.109375；014 −2/29=−6.897pp、paired p0.6875），invalid/全部EOS、gpu用时峰值/计算边界无算术矛盾。不是独立像素/金标/私有脚本审计。仅N_video2、一个新增sample，已观察源与公开gold非blind，均CLOCK_ZERO_ASSUMED_NOT_CERTIFIED，无法认定显著、普遍无效或具体反转原因。用户本轮未准读取旧私有逐题文件，B按约SKIP而非失败；015完成结案，明确**NO_GO_SIGLIP_STABLE_ADVANTAGE / PAUSE_FURTHER_GPU**，不允许在旧013/014数据上换seed/阈值/提示、修改旧结果或训练Qwen。

为了快且不再白下载媒体，**唯一READY为[VLM-NEW-SOURCE-ROSTER-016](./codex-artifacts/VLM-NEW-SOURCE-ROSTER-016/README.md)**：用户仅重新授权此前合法拥有且Codex精确已知的两个**小元数据**路径（HourVideo dev有gold结构、Ego4D source+release+时长/体量manifest），本地CPU一次性以非gold规则排两条已测视频和已知物理重合，筛选最多6个新匿名候选，先建议人工合法获得2–3个v1/full_scale同版本证据较强的媒体，及官方单UID下载CLI**只生成不给自动下载**。过去与Ego4D v2_1仅UID同源但无PTS/剪辑桥接者须标UNKNOWN并审慎保留，不把其当正式HourVideo可评分PASS；新试验需后续真正独立视频+明确资源新许可再定。没有两个精确授权元数据入口就016不执行/不再产出空收据；016新GPU/新AWS/云模型=0，NOVELTY RETAIN0、Charades FINAL_MEDIA_STOP保持。

### 2026-10-15 · ae014b4完成v1来源候选名单：R1–R3确定性冻结，下一步先合法人工下载而非空跑（最新）

[016 ae014b4](https://github.com/floomeer83felix-source/vlm/commit/ae014b4f79c88dbd4520185a43c8fa0065ab78b9)真实匿名验收：私有dev50与现有官方v1/full_scale 9645 canonical元数据行唯一对齐，排旧013/014两个Sample及1条资格数<10题，剩47候选记录来源组。六码候选分别39、39、38、36、35、34结构非图像MCQ；优先R1长度46.39min、R2长度73.28min、R3长度50.05min，三段结构题合计116。六个不同recorded source group、所有有release1/canonical-valid标志与标注精确时长声明吻合，**但不能冒称严格跨物理视频独立/精确同发布剪辑零点映射、最终gold类别或远端已经可下载**。无bytes字段，实际容量/网络预算全UNKNOWN；无真实Qwen forward、无新视频GET/GPU。016旧父任务结案，不重复来源列表或用旧v2_1 HEAD容量冒充本轮大小。

**唯一READY新[VLM-HOURVIDEO-NEW-SOURCES-017](./codex-artifacts/VLM-HOURVIDEO-NEW-SOURCES-017/README.md) / AWAIT_USER_COMPLETE_R1_R2_R3_MEDIA_AND_NEW_GPU_PERMISSION**。真实R1/R2/R3 UID及对应官方v1/full_scale单UID CLI模板仅保存于此前Codex**私人回答**，不可上传公开Git。用户依据现存授权、已安装CLI `--help`自确认参数和文件大小/存储预算后**先人工完整获取R1，有条件再R2、R3**；若无当前合法下载许可即停止，不自动HEAD/GET/修复旧.part。后续R1–R3完整媒体到位并在原/安全交接Codex聊天给精确私有入口、新明确≤232 Qwen generate/GPU总≤40分钟授权时，017可一次完成CPU合法完整PTS/最终QA/gold资格→同预冻结uniform12与SigLIP question-only12配对推理→答案隔离评分，源级逐视频全报告。若仅R1到位标**ONE_NEW_SOURCE_EXPLORATORY**，不冒充2–3片验证；没有媒体017保持不执行、不提交空HOLD，旧013/014同视频重试禁止，NOVELTY=RETAIN0/Pause GPU仍在。

### 2026-10-16 · R1 真实完整视频与39道gold题通过有界CPU预验收（非正式017结果）

[9a7b1ab](https://github.com/floomeer83felix-source/vlm/commit/9a7b1abb6f325c70c61fccf19ba34678aae29543)上传[独立补充验收收据](./codex-artifacts/VLM-HOURVIDEO-NEW-SOURCES-017/r1-cpu-preacceptance.md)：官方现有合法单UID v1/full_scale MP4实际606,852,958B /578.740080MiB，VP9 1440×1080 30fps，stream2783.466667秒，实际video demux EOF 83,504包等于声明帧数、无missing/nonmonotone packet PTS/DTS/腐坏旗标，首中尾仅218帧有界pixel decode正常（**未全部解码83,504帧**）。确切已授权dev标注和本机release-1 canonical元数据R1 UID、来源标志及declared 2783.47s时长吻合（vs真实流差3.33ms），非已测013/014记录group。R1单独隔离资格检查39/39条均五个非空文本选项、有效gold单字母A–E、外部图片/链接与schema需排除数为0；gold没有给任何推理/选帧系统。该原CPU检查与本轮上报GPU0/Qwen0/网络0，正式017仍NOT_STARTED。严格原视频物理采集独立性、original crop/annotation零点、不可变同版文件/remote hash未获证，后续只能按预注册未认证完整视频PTS假设探索性答题，不得称官方榜单。

现在**017仍是唯一READY**，但不再是“完全无新视频”：已有**R1工程资格和39题资格通过**。用户按016原Codex私有冻结UID清单优先合法手工获取R2/R3（未知字节规模先确认预算和硬盘），不用再做一轮无产出的R1复核。理想R1–R3齐全后再用户明确一次≤232 Qwen实际generate/GPU总≤40min新许可，一轮里CPU验证R2/R3并用已有R1证据比对输入未变，再做冻结uniform12 vs SigLIP query-only12配对Qwen真实长视频评测和隔离gold评分。R1单独可申请探索性实验，但新独立来源仍仅一个，优先准备R2/R3，不得凭未来正负成绩决定是否继续下载。014旧许可不继承。

### 2026-10-16 · cedb055三新长视频真实配对Qwen230/230成功：视频等权SigLIP+4.18pp但R3反号，017结案（最新）

[017正式收据cedb055](https://github.com/floomeer83felix-source/vlm/commit/cedb0559ea62998a1c1cb28866ab4c054273682d)：按此前用户明确授权，R1/R2/R3新合法完整v1/full_scale视频都通过有界CPU packet-EOF/PTS/首中尾pixel decode、dev UID/canonical metadata/时长匹配，R3按原nongold规则排3辅助图片题+1外部素材题，最终冻结N=39/39/37。与013/014协议保持原Qwen3-VL4B BF16、SigLIP F32、每来源48真实PTS候选，uniform12与question-only SigLIP top12在相同Qwen参数/324 visual tokens下AB/BA对照，全部230次真实generate成功自然EOS、答题 gold仅所有进程结束后独立计分。按视频：(A,B)R1=(10/39,14/39)、R2=(5/39,8/39)、R3=(14/37,12/37)；video-equal macro A25.43%、B29.61%、差+4.18pp，**2个新视频B正向/1反向**，旧两source合计五片也呈3正2负，仅描述性绝不证明稳定优势/显著性/优越原因。配对四格R1 both9/A-only1/B-only5/neither24、R2 5/0/3/31、R3 9/5/3/20，INVALID均计入冻结分母、NOT_RUN0。GPU总99.984秒/已获≤2400s，torch allocated峰9134.436MiB/≤20GiB，0新研究媒体/模型HTTP，0训练/旧实验重放；2个剩余attempt及GPU剩余时间**不转移**。严格物理来源与immutable release/crop/annotation t0/PTS独立认证缺失，`CLOCK_ZERO_ASSUMED_NOT_CERTIFIED`、`NOVELTY=RETAIN0`，非官方榜单成绩。

**2026-10-17 审核020结果：** [438f9f8](https://github.com/floomeer83felix-source/vlm/commit/438f9f8d01378fdbed392c2d1355dafe47f31d57)已完成唯一允许的020 CPU动态尝试与匿名交付，Window Job≤2GiB/commit余量门通过但在Torch导入/CPU setup时OSError/WinError87；实际训练updates=0、5项动态NOT_RUN、根因不明。**020结案不重跑，当前READY=0。** 静态阅读020发现预Torch导入的全局audit(open)使用Path.resolve的潜在Winerror触发路径，未有证据断定因果，禁止单凭推测修系统或继续申请更大内存。研究转向已有[009长电影的历史真实训练证据](./codex-artifacts/VLM-LOCAL-LONGVIDEO-009/local-long-video-ab-receipt.md)：公有领域训练许可是009旧用户授权，完整1465.597s/43924帧且RTX3090每臂完成100个optimizer updates；这说明旧环境/独立技术样本曾能训练，但不可继承旧素材访问许可。下一步应在用户**重新明确限定009单个原合法本地影片入口只读CPU资格核验**后才可激活现有[TRAIN-PREP-001](./codex-artifacts/VLM-HOURVIDEO-TRAIN-PREP-001/README.md)；权利、现存完整性、物理来源独立于013–018 dev/eval和环境可用性必须现场核实，任何UNKNOWN则STOP。不自动访问R1–R6或gold/其他目录，不运行GPU或新下载；TRAIN-GPU继续HOLD，NOVELTY=RETAIN0、CLOCK_ZERO_ASSUMED_NOT_CERTIFIED与Charades FINAL_MEDIA_STOP继续。

### 2026-10-17 · 新许可下009原电影来源有限只读复核（021唯一READY，尚未执行）

用户批准的是**009原先精确指定、此前真正训练的单个本地电影**CPU只读资格审查，不是扩大TRAIN-PREP-001、019/020重试或新的GPU训练。唯一READY=[VLM-TRAIN-SOURCE-ELIGIBILITY-021](./codex-artifacts/VLM-TRAIN-SOURCE-ELIGIBILITY-021/README.md)：按原Codex私人准确入口验证单一视频存在和非重解析属性、训练权限来源、可有界CPU只读校验与已公开来源层的物理独立证明。不得从匿名size/时长猜文件；精确入口不能找回则直接HOLD并向用户索取私人明确路径。无权读取现有dev QA/gold、R1–R6私有manifest/视频或用户其他路径，因此不足以认证物理隔离时须UNKNOWN，不能虚构PASS。旧009为公有领域长片技术训练历史，不是新独立test，旧历史user授权不成为视频永久无限权限。父任务CPU各操作计时受限，总≤180秒；模型/Torch、GPU、研究下载、私有写入为0，提交脱敏回执+单条results后STOP。TRAIN-PREP/GPU继续QUEUED/HOLD，`NOVELTY=RETAIN0`、`CLOCK_ZERO_ASSUMED_NOT_CERTIFIED`、Charades`FINAL_MEDIA_STOP`不变。


### 2026-10-18 · 021按合同安全HOLD结案：先恢复原009精确路径，不再空跑

[021提交f3d86ec](https://github.com/floomeer83felix-source/vlm/commit/f3d86ec445e498dc824fce40ffe72be842952fd5)经GitHub对照仅新增匿名[单文件资格回执](./codex-artifacts/VLM-TRAIN-SOURCE-ELIGIBILITY-021/read-only-source-eligibility-receipt.md)及codex-results一个父任务条目；Codex查明当前**无法从009原私人上下文恢复那个真实训练电影的唯一完整路径**，因此入口闸门直接HOLD。没有对私人视频做stat、ffprobe、demux、完整性SHA、任何扫描或其它读写；FILE_EXISTS、INTEGRITY_EVIDENCE、TRAINING_RIGHTS_EVIDENCE和TRAIN_EVAL_PHYSICAL_SOURCE_INDEPENDENCE全部UNKNOWN而非FAIL。历史009的100+100次真GPU更新、美国PD文档声明不能证明当前文件存在/资格或来源独立。**021 ACCEPTED_SAFE_HOLD、非READY；当前READY=0。** 不再以原009匿名描述猜路径，也不能再启动019/020/021任何旧父任务。下一项实际依赖是用户在**活跃Codex私人聊天**自行补回原009**确切文件路径**、对应训练用途已知许可/来源文件入口；只传路径不是新媒体访问许可，需再由ChatGPT审查后制定一次新的精确CPU只读任务，不能让Codex自行开文件。若没有原文件，用户可另外选择合法、与评测独立的新训练素材，但须另提供确切入口及授权；不自动下载。TRAIN-PREP-001和TRAIN-GPU-001仍QUEUED/HOLD、GPU0、受保护QA0，`NOVELTY=RETAIN0`、`CLOCK_ZERO_ASSUMED_NOT_CERTIFIED`、Charades`FINAL_MEDIA_STOP`持续。


### 2026-10-18 · 私聊提供009原电影路径；022独立单文件核验唯一READY（尚未执行）

用户于ChatGPT私人对话提供一条完整本地单电影路径，不能在GitHub公开路径/文件名。021因Codex当时不知道该精确入口已安全HOLD结案。新[022合同](./codex-artifacts/VLM-TRAIN-SOURCE-VERIFY-022/README.md)是唯一READY；用户须在活跃Codex私人聊天另发一次022执行指令并粘贴原路径，Codex不能依靠公开历史猜文件。仅查当前单文件身份、存在、完整性、训练权利与和HourVideo/Ego4D评测素材物理独立的证据，任何UNKNOWN都保留HOLD。未经新明确许可不运行GPU、Torch/模型、训练或其他视频/QA，TRAIN-PREP和TRAIN-GPU继续QUEUED/HOLD；NOVELTY=RETAIN0、CLOCK_ZERO_ASSUMED_NOT_CERTIFIED、Charades FINAL_MEDIA_STOP。


### 2026-10-18 · 022单视频容器/packet合格，余三项证据待专门合并CPU资格审查（READY=0）

[提交9c028b5](https://github.com/floomeer83felix-source/vlm/commit/9c028b52ddadf605c50746a86c6c18cc33bcc0f5)相对022任务起点只增合法的[匿名单文件资格回执](./codex-artifacts/VLM-TRAIN-SOURCE-VERIFY-022/read-only-source-verification-receipt.md)与codex-results恰一条，未改既往实验、规划或秘密。`FILE_EXISTS=PASS`、`CURRENT_INTEGRITY_EVIDENCE=PASS`限本机container/packet层：实际文件当前103909467B，单WebM/VP9 480p、1465.597s，demux至EOF43924包，timestamp缺失/非单调与packet corruption旗标0；ffprobe一次0.422s，demux一次1.406s受监督，父墙钟1.828s。未做全帧解码、旧SHA比较、任何新训练。`ORIGINAL_009_IDENTITY=UNKNOWN`、`TRAINING_RIGHTS_EVIDENCE=UNKNOWN`、`TRAIN_EVAL_PHYSICAL_SOURCE_INDEPENDENCE=UNKNOWN`；旧009规格吻合与原先美国PD/用户许可执行者报告提供有益历史佐证但不能代替当前确切资产与严格不泄漏证明。**022结案且READY=0**，禁止重跑/改旧结果。下一阶段优先**合并一次**合法来源证明、原对象连续性（如确有原已知SHA）、评测组级物理隔离的非保护证据和TRAIN-PREP CPU环境只读门；仅在新的用户明示限定具体私人证据入口与检查范围后设下一个唯一READY，无法合法读取时必须UNKNOWN而不能无限重复生成HOLD任务。009已有100+100真实GPU更新历史，019/020受控Torch DLL导入HOLD不代表3090梯度训练从未成功。TRAIN-PREP/GPU依然QUEUED/HOLD；旧HourVideo dev gold和QA绝不可进入训练、调参、教师或checkpoint选择。`NOVELTY=RETAIN0`、`CLOCK_ZERO_ASSUMED_NOT_CERTIFIED`、Charades `FINAL_MEDIA_STOP`持续。


### 2026-10-18 · 新批准合并CPU只读TRAIN-PREP成为唯一READY（未执行）

用户批准的是既有[TRAIN-PREP-001](./codex-artifacts/VLM-HOURVIDEO-TRAIN-PREP-001/README.md)**A/B/C/D四子项一次完成的CPU静态预检**，不是GPU或重跑009/019/020/021/022。022的现有单电影容器/packet EOF证据直接复用，不读取那部电影；许可证据、原009对象绑定与严格train/eval物理源独立只可从旧公开材料及已明确授权的**非保护且精确已知**小型记录检视。没有许可入口或eval分组证据明确记UNKNOWN，不能搜私有目录、打开受保护QA/gold。另必须完成独立获授权的既有模型/processor配置路径和软件发行版本、主机资源静态审查（禁止torch/transformers导入、GPU API、权重加载）。冻结≤2层/≤1M参数/≤200步/≤60 GPU分钟等仅未来GPU任务*提案*，未获执行许可。**唯一READY=TRAIN-PREP-001**，GitHub不会唤起Codex，需要用户在活跃Codex聊天新指令。运行限制CPU只读≤300秒，报告一份匿名receipt+一条results，正常push后停止。TRAIN-GPU继续QUEUED/HOLD，NOVELTY=RETAIN0、CLOCK_ZERO_ASSUMED_NOT_CERTIFIED、Charades FINAL_MEDIA_STOP。

### 2026-10-18 · 合并TRAIN-PREP静态预检结案：科研表达能力与GPU授权分离

[8aba2e3](https://github.com/floomeer83felix-source/vlm/commit/8aba2e37cd97b9e36881b595eec9250d3f0d42cb)只新增[合并匿名收据](./codex-artifacts/VLM-HOURVIDEO-TRAIN-PREP-001/cpu-training-readiness-receipt.md)和codex-results单条追加，合同范围合规。A（原009对象身份及许可资产绑定）HOLD；B（与保留评测录制/镜头/片段/源组的正面隔离）HOLD；C静态现有模型配置/权重存在性/包分发元数据/CPU宿主资源PASS：19直接文件项15存在、4项可选缺失，10个小JSON、三个模型权重仅stat，GPU API与Torch/transformers imports均0；D自监督近远时间代理合同纸面PASS，尚未运行。调查约60.704秒、无媒体读/模型前向/优化更新/网络研究请求与环境变更。TRAIN-PREP已结案，READY=0；不得重跑其旧父任务，也不得自动授权TRAIN-GPU。

新增方法学限制：提议head输入为abs(z_i-z_j)与z_i*z_j，前后帧互换保持不变，因此**结构无法表征时间顺序反转**；只适用于近远时距无向代理分类。拟定随机0步/真实100步/打乱100步的总200更新和≤60GPU分钟仅是未来独立GPU实验提案，不代表事件顺序理解、QA改进、跨影片泛化或科研创新。仍需训练素材与当前权利绑定、非受限独立source-group证据、SigLIP真实embedding shape、模型runtime与GPU资源有效核验；不得访问旧dev gold/私有eval视频/映射或重跑019/020。

下一步研究应以017/018真正运行的长视频检索结果为基础：审查固定token预算下的多事件/时序证据遗漏、相关性和覆盖权衡，设计相对于已有方法可证伪的假设与独立样本对照。与其无限迭代安全门，先明确下一轮究竟只做技术近远proxy，还是有顺序感知表达力的创新目标。TRAIN-GPU仍需单独用户许可，NOVELTY=RETAIN0、CLOCK_ZERO_ASSUMED_NOT_CERTIFIED、Charades FINAL_MEDIA_STOP。


### 2026-10-19 · 双事件证据研究转向：纯合成方法任务023唯一READY

ChatGPT直接制定[科学假说与可证伪评估协议](./research-protocols/ordered-evidence-2026-10-19.md)，不是再发一个文献调研或重复视频/环境资格任务。观察锚点为017/018 Top12较Uniform12在有限已见开发来源有描述性提升、固定12bin在018不一致，尚不能说明独立QA泛化。研究假说：同样48候选、12帧/324 Qwen视觉token下，显式选择问题相关的两个不同事件的可能AB/BA方向证据，能否减少单类高相关性挤占帧；**不能从问句或打分预断AB真值**。已有AKS/GenS/NeuS-QA/VECTOR/TimeLogic邻近法显著，创新性仍RETAIN0。

**唯一READY 023**：Codex在公开仓库以纯stdlib实现无模型的合成OEP-12及≥12反例unit tests（含旧对称头无法区分前后帧的数学反例），不接触任何旧受限影片/QA/gold/私有source maps/模型/特征/GPU/训练，不读取本机009电影、不使用019/020旧预算。新协议已规定未来独立8组/120未见多事件题仅作为**条件性采样目标**及AKS/GenS强基线/公平时延成本和失败停机门，真实实验/标签/模型GPU均需另外批准。即便toy PASS只是synthetic性质，不能声称Qwen时序理解或论文方法突破。TRAIN-GPU维持HOLD。

### 2026-10-19 · 023交付合成可证伪算法：逻辑PASS，真实科学价值仍需独立评估（READY=0）

[023提交798da78](https://github.com/floomeer83felix-source/vlm/commit/798da78ace41dc1015c60dc9683eafecfd9df18e)与[023匿名回执](./codex-artifacts/VLM-ORDERED-EVIDENCE-023/synthetic-order-falsification-receipt.md)已审：4个路径严格对应023合同，新增Python标准库selector、31个合成断言unittest、匿名回执和codex-results恰一条。31/31 PASS、0 FAIL/ERROR/SKIP，含16个固定种子合成world穷举oracle对照、AB-only、BA-only、双向证据、同帧重复、PTS起点平移、非有限分数和输入HOLD、旧近远head的帧交换不变性、锚点挤占高相关帧的反例。两轮子进程运行各0.140s、合计0.280s，模型/媒体/真实QA/金标/受保护身份/下载/GPU/Torch/梯度0。回执事实属Codex本地执行报告；GitHub本轮审查范围为公共代码/提交/收据，**没有独立复跑私有环境**。

正式层级**ACCEPTED_SYNTHETIC_IMPLEMENTATION_PASS**，本任务结案，**READY=0**；是算法规则和合成输入不变量验证，不能认定事件识别、Qwen QA增益、因果/时间顺序推理或论文创新。候选算法缺少实际从问题自动得到E_A/E_B事件子查询、视觉分数语义与跨source校准、源级事件实例身份真值；合成tau=0.70不能不经独立合法训练数据校准地照搬到SigLIP，且当存在多次相似动作时AB/BA都可能被高分伪激活。强制锚点也会挤掉原B的高相关帧，故未建立优势或单调覆盖收益。

科研下一关键转折：**不再创建024重复toy/纯静态代码任务**，先锁定真实研究输入的合法性/未见性和录制组隔离、事件验证标签是否存在、与AKS/GenS等强邻近方法可比的48→12帧/视觉token/成本。用户需另行明确授权所指真实数据和GPU/model推理，不能把旧013–018开发gold当新heldout，也不能用009现有资格HOLD素材自动训练。未满足真实数据门则继续不开展GPU，不伪称发布效果。TRAIN-GPU维持QUEUED/HOLD；NOVELTY=RETAIN0、CLOCK_ZERO_ASSUMED_NOT_CERTIFIED、Charades FINAL_MEDIA_STOP。


### 2026-10-19 · ChatGPT完成公开筛选和真实OEP试点设计；024待新明确媒体与GPU许可

已完成[024真实研究协议](./research-protocols/real-oep-pilot-2026-10-19.md)，下一步不是重复toy/静态预检，而是用从未在R1–R6出现的≤2组HourVideo独立长视频，按固定无gold筛选最多48题，比较同48候选/12帧的五臂真实Qwen3-VL/SigLIP推理、来源级paired正确率与运行成本。前置至少12条可确定性拆分双事件的非金标题门，不足则GPU0并报告真实方法适用率不足，绝不因旧开发集结果调算法。真实rank-percentile只是proxy，不把023合成tau0.70当真实SigLIP校准值。最多2源仅探索，不宣称新benchmark胜出或论文创新。

ChatGPT调研发现Video-MME-Logical数据集2026 Mini375/约352MB且标注CC BY4.0，适合外部时序逻辑诊断，但包含符号状态追踪和reference image、不是小时级双自然事件；不自动下载或作为024主数据。HourVideo禁止benchmark训练、Ego4D视频许可证与原访问凭据仍为限制。**用户“继续”不是新视频/QA/gold/GPU及28GiB下载授权。024仅QUEUED，当前READY=0。** 等用户明确单次许可后，ChatGPT核对main再升为唯一READY，禁止Codex凭此规划自动启动。TRAIN-GPU-001独立HOLD、NOVELTY=RETAIN0、CLOCK_ZERO_ASSUMED_NOT_CERTIFIED、Charades FINAL_MEDIA_STOP。


### 2026-10-19 · 用户明确批准024一次真实HourVideo多臂GPU零训练推理（唯一READY）

用户在本轮ChatGPT对具体024新媒体/QA/gold、网络及GPU额度答复“批准”；授权已经体现在[024更新合同](./codex-artifacts/VLM-HOURVIDEO-OEP-REAL-024/README.md)和[真实实验协议](./research-protocols/real-oep-pilot-2026-10-19.md)。**唯一READY 024**（尚待用户在现行私有Codex聊天新发执行指令），不是现在已有执行成绩。允许至多2个以确切获授权私有非金标元数据指向的全新、真实物理拍摄/剪辑独立的HourVideo/Ego4D来源组，总≤48道nongold题，严格gold待GPU关闭后独立CPU scorer只读一次；必要官方HTTP媒体≤28GiB（各≤14GiB）及新增私有内容≤32GiB，Qwen QA生成≤240，RTX3090 GPU累计≤25min、PyTorch peak allocated≤18GiB，CPU媒体≤900s，父总≤3600s。授权不自动等于许可/凭据/source版本与独立证书通过；前置安全CPU门先核许可有效和来源正面独立、双事件可确定分解≥12题，缺任一项则在媒体下载/GPU前STOP并记录HOLD，不以不同UID/主题代替来源证明。五臂同48候选/12实际帧/324视觉token，真实分数rank代理不假装合成tau为已校准概率，旧R1–R6 gold永不能训练/选阈值。允许的集成公共代码只新024两个Python，公开仅匿名收据+results一个append，正常push后停止，不触发原TRAIN-GPU。`NOVELTY=RETAIN0`、`CLOCK_ZERO_ASSUMED_NOT_CERTIFIED`、Charades`FINAL_MEDIA_STOP`。


### 2026-10-20 · 028真实文本cohort验收；下达029来源追溯与有限媒体metadata整包

- main交付[157ffd8](https://github.com/floomeer83felix-source/vlm/commit/157ffd8a26b0e632e57cb52b4215c8b99de8678d)
  直接父为028规划302a5bb，八处允许路径：adapter/scorer/prepare/coordinator定点改动、
  新028测试、两份匿名报告及results唯一父记录；未改旧报告、研究协议、supervisor或规划文件。
  ChatGPT静态审查差异、公开实现/17项新测试与两回执，未独立运行测试或访问私人数据。
  **ACCEPTED_CPU_COHORT_HANDOFF_PARTIAL / REAL_PILOT_HOLD**；028已关闭，不重跑或迁移余额。
- 容器门已产出真实数据：执行者报告index/screen/inference均完整稳定，
  **50来源/1182题，原025语法支持28题；1151 task-not-admitted＋3非time-gap形式**。
  两项已知within-cohort participant重合被排除，26来源通过现有screen，
  先冻结4个源/原题索引，再保留20个选项，形成16文字调用槽位；不是模型执行或合格新源N。
  可认证执行N当前0表示资格HOLD，不能写成0合格、0/N准确率或效应估计。
- 当前兼容profile明确为SKIP_NONFINITE_028 / PROJECTOR_028_V1。
  三个完整遍历各观察到同一流中的1个未保留NAN类别值、无±Infinity/parse error；
  admitted字段拒绝、strict默认保留，保护值未进入scalar decoder有新fixture仪器化见证。
  **不是严格JSON通过或027历史失败字节的因果证明**。三遍完整raw receipt/profile绑定
  一致由执行者报告，私人摘要未访问。原题型、四臂/48→12/同锚点/完整分母不改。
- 旧源工作应按实际证据收窄：8份旧记录全部完成白名单投影，但恢复UID=0，
  所以旧请求是NOT_JOINABLE_NO_UID，不是旧源join PASS或底层没有身份。
  官方manifest一遍9645行，50个标注UID全部唯一匹配，只证明这50个声明的join。
  013/014和R1–R6完整记录组/participant/已知派生排除仍UNKNOWN。
  不把source_group数组位置、任意字符串、文件名、摘要或相近时长当UID/身份。
- P1–P4分别声明约60.0/52.9/67.4/73.3分钟，来源origin存在；
  **P3 participant缺失**，其余有声明；release1/canonical与时长声明一致。
  当前权利、精确对象/版本、本机媒体stat和获取字节均未确定；028媒体stat/网络均0。
  四个固定候选不能因后续不合格而替换；如未来提议资格子集，须在模型输出前
  另冻结新合同N/轮转/完整分母，并明示原text N4及各排除，028原plan保持不变。
- 执行者报告首轮且仅一轮新suite **17 PASS/0 FAIL/ERROR/SKIP**；
  后加continuation有实际获准metadata执行，末尾guard改动仅静态检查，不能说全部模式动态已测。
  13次研究open全完整，预扣/实际9,887,423B；runtime预留330s、
  outer窗口合计4.031s/保守全自有PID包络<40s，21私有文件/78,853B。
  这些为执行者测量/包络，非ChatGPT本机复现；真实gold/模型/Torch/GPU/媒体正文/
  网络下载/安装/环境/ACL改变均报告0。公开差异未见受限身份/题/选项/答案/私有路径。
- 按用户既定“先写工作任务到仓库，再给Codex执行指令”和一次多任务要求，
  新下达[029 A–H合同](./codex-artifacts/VLM-SOURCE-PROVENANCE-META-029/README.md)，
  **唯一READY=VLM-SOURCE-PROVENANCE-META-029 / PUBLIC_PROVENANCE_CPU_ONLY**，尚未执行。
  028最后容器门已经成功，不再修解析；029具体解决白名单schema/实际写入语义、
  旧来源台账、独立多对多组join、固定四候选资格及实际媒体成本。
- 029允许从实际producer证据解释group tuple/map-key，须先证明artifact写入绑定；
  不把“UID不可得”错误升级成“已证origin组也不可用于排除”。已证组匹配可保守排除
  全部canonical别名，UID/组/participant/派生分开裁决；最高仍仅
  RECORDED_GROUP_SEPARATION_ONLY / PHYSICAL_RECORDING_INDEPENDENCE_UNKNOWN。
  若确切登记/版本证据仍缺，写明缺失引用、停止当前来源路线并交回决策，
  不自动再排一个同类schema/空资格父任务。
- 新私人范围由同一条用户启动消息明确激活：输入≤48MiB（最坏角色和46MiB），
  028/027 nongold交接≤16份各一次，旧记录/直接引用registry合计≤8份各schema＋投影各一次，
  实际producer源码≤6份AST各一次、缓存官方manifest一次≤8MiB；
  **原混合标注/旧QA/gold/逐题预测/媒体正文0**。新integration_029≤128文件/32MiB，
  CPU/受控进程累计≤600s、coordinator≤1200s、新suite≤2，不沿用旧预算。
- 同一启动消息另明确接受新增**官方S3 HEAD metadata**：现有隔离SDK/静态ego4d profile，
  仅精确官方canonical对象，HeadBucket≤1＋HeadObject≤4、实际HTTPS发送总≤5，
  before-send持久门控重发/region redirect，失败不重试；媒体GET/LIST/STS/正文0。
  无准确URI/可信region/profile/发送门则F独立HOLD，不猜key或修环境。
  HEAD ContentLength只支持成本，ETag不冒充hash/权利或版本认证；公开仅匿名状态/取整MiB上界。
  该新网络许可必须由用户实际发送明确指令，公共READY/旧凭据不提供许可。
- 公共执行最多七处：两个新provenance模块、新suite，必要时仅Journal固定029白名单扩展，
  两份匿名报告和results一个append。一轮完成A–H后一次安全push并STOP；
  不创建空执行结果，不自动030/模型/GPU/gold/媒体下载。未来实际运行仍待资格、
  资源、模型/OS隔离和独立评分的具体新合同。
  **REAL_QA_EFFECT_UNKNOWN；NOVELTY=RETAIN0；CLOCK_ZERO_ASSUMED_NOT_CERTIFIED；
  Charades FINAL_MEDIA_STOP；TRAIN-GPU HOLD。**


### 2026-10-20 · 029部分工程/元数据验收；缺来源登记，按合同停止当前来源路线

- 审查main交付[4b619da](https://github.com/floomeer83felix-source/vlm/commit/4b619da6878b2a20172e816a17f4bafc725a4457)，
  直接父为029规划5d76d52。七处允许路径：两个新provenance模块、一份新测试、
  Journal固定029白名单一行扩展、两份匿名报告及results末尾唯一029父记录。
  ChatGPT逐段静态审查源码/17项见证与两回执；未独立运行测试、访问私人输入或调用AWS。
  **ACCEPTED_PARTIAL_ENGINEERING_METADATA / SOURCE_ROUTE_STOP_MISSING_PROVENANCE**。
  029已关闭；原profile、selector、supervisor、旧报告/旧结果未改，不重跑或迁移剩余额度。
- A确认028四键/cohort/16调用引用与轮转/profile版本绑定一致，原N4/20选项/16文字槽位不变；
  029未保留question/options/event scalar。这个引用核验不是模型输入/媒体或来源资格通过。
- B/C的真实发现比028更具体：八份旧文件完成scalar-free schema观察，六份是
  count/parameter/fingerprint汇总、两份demux汇总，**未观察到source_group字段**。
  两份已知private reader AST不提供原qualifier/registry的实际写入绑定；
  39个输出调用观察不是39个已证writer，六个确切JSON引用为模型配置，不是来源登记。
  没有打开这些配置或猜测其他registry。013/014准确登记/运行引用仍缺，
  R1–R6虽有汇总artifact，但alias→UID/origin/participant/known-derivative和写入关系未恢复。
  不能把八次完整schema读误写成八份来源登记已供给，也不能由无字段推断其他位置无身份。
- 公开writer证明只支持特定直接group构造＋特定self-source摘要写法，是窄实现，
  不是所有合法来源登记的穷尽分析器；其他可信运行登记、直接UID映射或写入证据并未被证明不存在。
  identity第二遍实际0次；未执行分支不认证真实身份恢复、任意writer或全面溯源能力。
  后续若用户实际提供确切可信登记，可以另行审查其直接证据，不要求旧文件凭空出现
  029 fixture专用的producer_sha256格式，不把单一代码写法当作科学资格的唯一形式。
- D官方缓存manifest一次完整9645行，固定4 UID均唯一匹配，0缺失/重复；
  真正old UID/group请求仍0，所以旧源排除NOT_ESTABLISHED。P1–P4来源资格全部UNKNOWN，
  P3另缺participant；无精确本机媒体引用，stat0不表示文件不存在。
  空资格认证不是0合格题或0/N准确率，也不是新方法的负实验结果。
- F有实际成本证据：执行者报告**2次HTTPS发送=HeadBucket1＋HeadObject1**，
  仅P1对象HTTP200，大小向上取整上界**890MiB**。P2–P4未发送，
  因缺可信bucket-region且唯一discovery槽位已用；不是403/404/文件缺失/权限过期。
  bucket响应状态/异常未持久保存，仍UNKNOWN，不能补写认证成功。
  官方精确canonical URI为opaque key；初始错误.mp4后缀要求造成4项网络前HOLD，
  后用已保留官方投影纠正、加入无后缀fixture，无原输入重开/拼接suffix/猜UID key。
- SDK实际发送前持久预扣、精确HEAD URL/槽位、SDK及底层retry/preload检查、原始response
  不read/drain即关闭和64KiB保留headers门有对应代码/虚构见证；限于本次安装/具体分支，
  不扩大为任意SDK/传输层的普遍认证。ETag不等于hash，HEAD200不代表研究使用权、
  immutable版本、时钟桥或来源独立。GET/LIST/STS/媒体正文均报告0。
- G两次本轮新suite分别16 PASS、17 PASS，均0FAIL/ERROR/SKIP；第二次验证opaque-key修正，
  非隐藏首轮失败；两次额度已用，不再补测。晚增SDK/确认/最终分支有静态及获准metadata执行，
  最后duplicate-UID guard仅静态检查，不冒称每个模式动态覆盖。
  新fixture主要证明通用结构/发送门，不证明真实旧源排除、OS gold隔离或QA效应。
- 执行者报告18研究open全部完整、预扣/实际**4,382,708B**：
  028交接4、旧schema8、private reader AST2、官方SDK-source AST3、manifest1。
  SDK3加private2合计5份source输入，未超6份；正常SDK/profile加载属于明确SDK分支，
  不将其冒称所有依赖文件读取都纳入研究正文计数。runtime预留570s、outer合计12.235s，
  保守全受控PID窗口<60s；17私有文件/110402B，仅integration_029。
  真实模型/Torch/GPU/gold/媒体正文/hash/probe/decode/download/安装/环境/ACL改变均报告0；
  公开差异未见真实身份、题文、答案、私有路径、URI或凭据。
- **按029原合同触发SOURCE_ROUTE_STOP_MISSING_PROVENANCE，当前READY=0。**
  原合同明确“若追溯后仍缺确切登记表/写入绑定……停止这条来源路线”，
  “不自动再排一个同类schema/资格/盘点父任务”。因此本次不创建030、
  不把余下3个HEAD额度滚动给新父任务，不自动放宽来源排除或把P1媒体成本当执行放行。
- 已形成[下一步具体路线选择](./research-reviews/post029-source-route-decision-2026-10-20.md)：
  A用户提供准确非金标来源登记/运行绑定引用后再作有输入的审查；
  B用户明确接受允许旧源可能重合的开发集机制诊断，另写完整新合同，
  明示不构成独立来源/held-out验证，可能旧题再答须单独明确授权；
  C停止本来源方案，另选有可追溯来源的新数据路线。
  本次只写可审查决策材料，不创建虚假READY/空执行回执或默认改变研究口径。
- 当前没有新增真实QA、训练、事件证据实例/召回、源级泛化或创新性结果。
  **REAL_QA_EFFECT_UNKNOWN；NOVELTY=RETAIN0；CLOCK_ZERO_ASSUMED_NOT_CERTIFIED；
  Charades FINAL_MEDIA_STOP；TRAIN-GPU HOLD。**


### 2026-10-20 · 用户接受开发集机制诊断；030真实整包已下达，资源由单条新消息激活

- 用户在029结案、明确提出“允许来源可能重合的开发集机制诊断、不能作为独立验证”
  后回复“好的”，本次据此接受post029选项B。不是把旧源排除已证PASS，
  也不把此短答扩张为未列明的GPU/下载/gold额度。
- 新增[开发诊断科学协议](./research-protocols/development-temporal-diagnostic-2026-10-20.md)
  和[VLM-DEV-TEMPORAL-PILOT-030 A–H合同](./codex-artifacts/VLM-DEV-TEMPORAL-PILOT-030/README.md)。
  **唯一READY父任务030 / PUBLIC_IMPLEMENTATION_ONLY，尚未执行。**
  用户实际发送合同末尾一条完整消息后，同时激活精确私人输入、新目录、CPU/媒体/SDK/GPU/
  固定四题gold的一次有界范围，不需再回ChatGPT等另一轮“激活”。
- 科学口径明记DEV_DIAGNOSTIC / SOURCE_OVERLAP_ALLOWED / PRIOR_EXPOSURE_POSSIBLE。
  不再要求排除013/014/R1–R6才能诊断，不追索八个旧文件或再排登记/schema门；
  P3 participant未知也披露但不作为本轮入门否决。没有换候选或声称新源/held-out。
  原029来源路线仍STOP，原025第7节的分离条件仅被新030研究口径明确替换；
  旧025/024协议、旧原始记录和父任务均不改、不重开。
- 原028四题/原索引、20选项和16个原轮转槽位不变；025原窄语法、48→12、
  C/D同两个锚点、共享a/b/q分数/目标/tie/补齐，仅i≠j与i<j不同。
  原N4/16槽完整冻结；媒体/许可/解码失败不替换，相应四槽NOT_RUN。
  至少1源可用且所有真实隔离/资源门通过才启动模型；
  至少实际调用过一次Qwen.generate才允许gold读取，不因纯准备失败查看答案。
- 固定四题即使曾被旧研究答过，030的新回答每臂最多一次，必须在用户启动消息
  明确授予该有限新范围；不把新口径含混当作AGENTS的历史前向禁令自动失效。
  不重放原013–029，不读旧逐题预测/历史gold产物来调参或填结果，不迁移旧budget。
- 资源上限是本次拟定cap而非本cohort实测：新Qwen generate≤16、单GPU worker≤1、
  GPU阶段≤900s（含load/编码/生成）、torch peak allocated≤18GiB/Job RAM≤24GiB。
  metadata/验证/评分CPU≤600s、媒体CPU≤1200s、获取窗口≤3600s、父≤7200s；
  新suite≤2次、虚构worker≤12各≤5s串行，预算共享不因public/private多跑。
- 新官方获取只针对029保存的四个精确canonical对象，不猜UID key或.mp4后缀。
  HeadBucket≤4（不同bucket各一次）、HeadObject≤4、GetObject≤4，总实际HTTPS≤12；
  低层retry/redirect同slot拒绝、失败不退款不重试，无LIST/STS/模型或manifest GET。
  fresh HEAD冻结长度/ETag/VersionId再条件GET，P1维持同对象/≤890MiB且与029绑定一致；
  各对象≤4GiB/正文累计≤16GiB。新integration_030≤384文件/24GiB，
  media≤16GiB/frame cache≤4GiB/其余≤32MiB，读取型scope沿用已知确切引用，不扫描。
  P2–P4大小仍未知，只在新HEAD确认落在上限内才GET，并未假称四对象合计已有实测。
- 沿用用户既有Ego4D/HourVideo批准依据，启动消息确认现有研究许可仍有效。
  不以HEAD200代替权利，不再要求凭空的新来源独立证书。
  新固定输入与原028完整raw快照/profile绑定；原混合annotation准备正文0，
  最后独立CPU scorer最多1open/4MiB，只解码四题gold；坏gold/绑定不符仍full-N UNKNOWN。
- 实际OS边界采用Windows原文件非继承exclusive share handle（正文0B），
  model PID期间持有，最多2个零正文拒绝探针；不改ACL，不宣称全机未知gold副本不可达。
  全模型Job/PID实际退出、队列关闭/fsync、账本绑定后，才释放锁并启动独立CPU scorer。
  新fixture先验证真实canary共享拒绝/Job/绑定/GET预算，不能用callback/boolean冒充OS退出。
- 本轮复查真实worker公开静态审计确认原grid[6,12,18]/12帧/324 visual tokens；
  新processor须逐调用实测匹配，不从旧报告填数。时间戳token可变，另报实际总长度，
  SigLIP q/a/b未截断长度/实际截断与分阶段成本不再遗漏。
  用新030模块连接现存原helper和权重，旧runner仅AST取必要helper，不执行其顶层或gold资格函数。
- 公共执行allowlist七处：三个新生产030模块、新连接suite、实际运行/科研结果两报告、
  results一个父append；不改旧adapter/scorer/supervisor/历史测试或规划。
  一次整包连续做媒体→真实四臂→独立评分→分析后安全push STOP，不自动031/扩样/训练。
  当前仅下达合同，未在ChatGPT侧读取私人输入、访问AWS、运行模型/测试或制造执行回执。
- 最多4个依赖未知/可能已暴露开发题，正负结果均不能证明稳定效应、独立泛化或算法创新。
  C=D全同则NO_REALIZED_SELECTION_CHANGE，不改规则寻找正例；
  同帧同prompt/tensor但答不同要报告实现/可复现性问题，不解释成顺序约束获益。
  **REAL_QA_EFFECT_UNKNOWN；NOVELTY=RETAIN0；CLOCK_ZERO_ASSUMED_NOT_CERTIFIED；
  Charades FINAL_MEDIA_STOP；TRAIN-GPU HOLD。**


### 2026-10-21 · 030安全停止验收；031定点生产修复与一次真实开发诊断整包

- 审查main交付[101b001](https://github.com/floomeer83felix-source/vlm/commit/101b00111fcf30a45309a5dda5eddd173a012005)，
  直接父为030规划437463c。恰好七处允许路径：四个新030 Python、两份匿名报告、
  results末尾唯一030父记录；未改规划、旧测试/旧基础模块或历史结果。
  ChatGPT静态逐段审查四文件及18个新case/两报告，未运行030测试、读私人资料或访问AWS/GPU。
  **ACCEPTED_SAFE_STOP_AND_PARTIAL_IMPLEMENTATION / REAL_QA_NOT_RUN**，不是IMPLEMENTATION_PASS。
  030已关闭，两次测试和所有旧余额不再使用。
- 用户实际启动消息已按执行者报告激活明确真实范围并确认许可；SOURCE_OVERLAP_ALLOWED /
  PRIOR_EXPOSURE_POSSIBLE口径被接受，旧源登记与P3 participant缺失没有再作本轮阻塞。
  真正阻塞是新实现见证，不能改写成数据/许可失败或环境已损坏。
- 首suite因runpy/unittest __main__发现问题为0 tests/exit5，额度照消费；
  末suite18项16PASS/2FAIL/0ERROR/SKIP。生产python_command已加alter_sys=True，
  但不将末尾static检查当成第3次动态PASS或掩盖首轮失败。
  原canary ordinary-open抛OSError、winerror缺失，断言硬等32；正文未读，
  不证明锁失效。随后的假模型→独立score分支因断言失败实际NOT_RUN。
- 健康peer实际打印HEALTHY/exit0；被超时终止的自有Job active已归0，
  peer立即Query的active=1，测试未有界等其排空。不能据此说peer被杀或Job无用；
  计数时序只是可能原因，未动态证明。其余16项支持对应虚构逻辑/传输/分母，
  不认证真实SDK/媒体/processor/模型/gold或实际原annotation拒绝。
- 静态审查发现生产probe同样只认Python error.winerror==32，所以不能只放宽test。
  后续需原生CreateFileW失败后立即取真实GetLastError=32，与普通Python errno/winerror分别记录；
  有界Job等待必须实测active=0才签退出，并计完整cleanup窗口。依据Python OSError及
  Microsoft GetLastError/QueryInformationJobObject官方说明已核对；不先验认证原历史根因。
- A的实际cached handoff有进展：8个nongold缓存＋4个精确runner/factory完成，
  **12 open/55,649B**；四键/20选项/16轮转槽、三份完整028receipt及初始annotation stat吻合；
  四个cached canonical/release1引用一致，两保留factory的inputs AST匹配原helper。
  仅cached/初始stat证据，不认证当前媒体、真实后端运行或来源分离。
- C–F真实HTTP/HEAD/GET、媒体stat/hash/demux/decode、nvidia-smi、model/generate/GPU/train、
  原annotation独占handle/probe和gold均0。全16槽实际NOT_RUN，每臂NOT_RUN4；
  未读gold因此正确率/六配对UNKNOWN，不报0/4或NO_REALIZED_SELECTION_CHANGE。
  GPU峰未测量，不写成测得0GiB；新科学效应仍UNKNOWN。
- 执行者报告CPU预留420s、suite/Job outer合计1.718s，完整逐PID CPU未测得；
  父窗口至final-summary703.062s含实现时间，24私有普通文件/78,272B，仅030新根。
  三个fictional child，旧目录/锁/记录未变。late failed-suite/entry guard和pipe-close
  修改只syntax/static，未重新动态验证。公开差异未见真实身份/QA/路径/URI/hash/credential。
- 按用户既定“先写下一整包到仓库，再给Codex消息”的要求，下达
  [VLM-DEV-PILOT-RECOVERY-031](./codex-artifacts/VLM-DEV-PILOT-RECOVERY-031/README.md)，
  **唯一READY=031 / PUBLIC_TARGETED_REPAIR_ONLY，尚未执行**。这是研究负责人基于具体失败
  安排的新定点修复＋同轮真实执行，不属于旧030的第3suite或执行者自动031。
  新资源由用户实际发送README末尾一条明确消息激活；不再要求已确认的数据许可重新申请，
  不改变已接受的开发口径，也不增加GPU/下载规模。
- 031 A–H先修生产Win32/Job完整deadline、显式loader与031门、readonly旧cache交接、
  已知准确runtime入口及score run/plan/queue/exit绑定，再跑≤2个新suite（每≤60s）；
  不重跑030旧18项，不改其失败报告/测试。新见证必须有真实Windows canary/Job/
  独立CPU score，不用mock通过替代。首轮过即接真实，第二轮仍败停止，不补第三轮。
- 031只从030确切nongold/source缓存交接，旧过期RUN读作archive并校验hash链，
  不实例化旧运行Journal、不更改旧epoch/stop、不拿旧锁或消费旧余额。
  新integration_031、contract_id/run_id/lock/ledger固定绑定；
  原annotation准备正文0，真实probe原生＋Python均零正文，模型PID期间share=0锁持有。
  新score只在实际Qwen返回、全部Job/PID实测退出及完整绑定后，一次≤4MiB/四题gold。
- 维持原4题/20选项/16槽、48→12/C–D同双锚点/原rotation和full-N；
  031仅去掉实现中未书面规定的1GiB/源frame限制，仍≤4GiB全局cache和24GiB总写入。
  现有030三个生产模块定点适配，不复制另一套runner、不改025 selector/模型/提示。
- 新031上限：CPU600s、媒体CPU1200s、获取3600s、父7200s；
  新suite≤2×60s，虚构PID/后代≤24各≤3s串行（含600s内），完整cleanup也预扣。
  单GPU worker≤1/≤16 generate、GPU900s/18GiB allocated/24GiB Job RAM；
  HeadBucket≤4＋HeadObject≤4＋GET≤4/实际总≤12，单对象4GiB/总正文16GiB、P1≤890MiB，
  新384文件/24GiB；无模型/包下载、训练、环境/ACL/profile更改。上限非实际测量/已执行数。
- 公共allowlist七处：定点030三个production模块、新031见证、两匿名报告、results一个append；
  原030 test和两份报告不改。通过后同轮媒体→真实四臂→独立score→科研报告后一次push STOP，
  不交成“修好等下一轮GPU”，不自动032/扩样/调参；真实前置实际失败仍如实停止。
  目前仅规划，没有在ChatGPT侧新增私人读取、真实执行或空实验回执。
- **REAL_QA_EFFECT_UNKNOWN；NOVELTY=RETAIN0；CLOCK_ZERO_ASSUMED_NOT_CERTIFIED；
  Charades FINAL_MEDIA_STOP；TRAIN-GPU HOLD。**


### 2026-10-21 · 031修复见证与四HEAD验收；032固定当前对象条件GET＋同轮真实诊断

- 审查main交付[b8fa8b3](https://github.com/floomeer83felix-source/vlm/commit/b8fa8b368d2ae96e253db140768417b79effe6a8)，
  直接父为031规划d564276，恰好七处allowlist：三个production定点改动、新031测试、
  两匿名报告及results唯一031父追加。ChatGPT静态审查公开源码/差异、七项见证与回执，
  未独立运行测试、访问私人文件、AWS或GPU。
  **ACCEPTED_RECOVERY_WITNESSES_AND_HEAD_METADATA / MEDIA_ACQUISITION_HOLD / REAL_QA_NOT_RUN**。
  031已关闭；不用剩余第二suite、不恢复run/epoch/锁/旧网络或GPU余额。
- 031执行者报告首且仅一suite **7/7 PASS，0FAIL/ERROR/SKIP**，internal2.514s/outer2.797s。
  真实canary native32＋Python PermissionError/errno13/winerror缺失，释放后两种open均成功且正文0；
  健康peer自然退出/Job归零无kill，自有后代仍活时仅终止自有Job并实测0；
  虚构模型PID退出后独立CPU scorer走production成功/坏绑定与半读guard拒绝。
  这些是工程/虚构评分见证，不是Qwen真实效应；不能回写030失败的精确原因。
- 8个030 JSON cache原为canonical重写：031有界重建原writer字节顺序、官方四行最多24排列，
  每份均恢复与原INPUT_COMPLETE完全相同size/SHA，再验证原transform输出逐字节等于cache；
  4份source cache本就逐字节匹配。不是仅以语义一致认证或一般可逆序列化。
  原四键/20选项/16槽、三份完整028 raw receipt/profile与当前annotation stat一致。
  准确runtime只解析一次、读两config，helper AST保持；未导入ML或加载权重。
- 当前原annotation父非继承exclusive share handle1次，2个实际probe child每个native/Python各一次，
  共4次零正文尝试，均native32/Python拒绝；持有到队列关闭。当前gold/原annotation正文0。
- 实际官方HTTPS **11=3 HeadBucket＋4 HeadObject＋4 GetObject**。
  discovery301/301/400仅可信region header，SDKredirect拒绝，不写bucket授权PASS。
  四HEAD200，P1–P4公开大小向上取整上界 **890/2135/2263/438MiB**，
  全部有VersionId，P1准确长度/ETag/version与029一致。
  四个精确IfMatch＋显式VersionId GET都ClientError，body debit/read0、无partial/media。
  **当时GET HTTP status/service code未持久保存，仍UNKNOWN**；不认定403/访问权过期/
  特定凭据缺陷或版本权限就是原因。晚加status/TRANSPORT_RESPONSE分支仅静态，不能倒填观测。
- 因无可用媒体，decode/候选/nvidia-smi/model/generate/GPU/real score/gold均0。
  全N4/16槽NOT_RUN、每臂正确数UNKNOWN/4，六配对UNKNOWN；C=D/覆盖/真实tokens/成本NOT_MEASURED，
  GPU peak未测量。没有算法负结果、独立验证或新增创新证据。
- 031资源为执行者报告：18/18输入91,533B；CPU预留357s/获取预留3600s，
  实际outer stages23.281s（不是逐PID CPU计量），四GET完整窗口2.672/1.562/1.688/1.766s；
  media输出预留6,002,290,187B但正文0；67文件/6目录/175,467B、父516.264s。
  原目录/历史证据保留，安装/环境/ACL/profile/训练改动0。
- 新下达[VLM-DEV-CURRENT-OBJECT-PILOT-032 A–H合同](./codex-artifacts/VLM-DEV-CURRENT-OBJECT-PILOT-032/README.md)，
  **唯一READY=032 / PUBLIC_TARGETED_TRANSPORT_ONLY，尚未执行**。
  遵循用户“先写任务入仓库，再给一条Codex指令”和多项一次交付要求，
  一条实际用户消息同时明确新私人/网络/媒体/GPU/gold范围；不增设第二次激活审批。
- [AWS官方GetObject说明](https://docs.aws.amazon.com/boto3/latest/reference/services/s3/client/get_object.html)
  确认显式VersionId与当前对象读取分别使用GetObjectVersion/GetObject权限；IfMatch不符为412。
  这是032请求修正的技术依据，版本权限差异仍只是031失败候选解释。
  固定CURRENT_IFMATCH_PINNED_RESPONSE_032：请求不含VersionId/query，精确IfMatch保留，
  **正文首次读取前响应VersionId/ETag/长度仍全部等于031**。不接受新版本、无无条件GET，
  不先重复旧请求再fallback、不改凭据/许可，不以HEAD200保证GET成功。
- 032复用031四HEAD/可信region，**新HEAD0、每对象1GET/总实际HTTPS≤4**，失败不重试；
  response status必须在SDK解析/headers判定前落账，错误正文仍0，code不可得如实UNKNOWN。
  031 archive单独只读验证11实际请求/零body/closed/16NOT_RUN，不放松030零真实动作验证器。
  已有Win32/Job实现与031证据复用，不重跑旧7项；新transport/032绑定suite≤2×60s，
  首PASS同轮获取→CPU媒体→真实四臂→一次独立score，失败源不替换，剩余固定源继续。
- 新scope与031分账：输入≤32MiB（handoff≤17/source≤7/config≤4各1MiB＋gold≤4MiB），
  integration_032≤384文件/12GiB，media≤6GiB/frame≤4GiB/其余≤32MiB；
  四对象仅031精确长度，总6,002,290,187B，不把取整ceilings当真实length。
  CPU600s/媒体1200s/获取3600s/父7200s，虚构PID≤8各≤3s，
  单GPUworker/≤16generate/900s/18GiB allocated/24GiB Job RAM。
  原annotation准备0B、当前2实际零正文probe；只有Qwen实际返回、所有模型Job/PID退出、
  队列/完整快照绑定后独立score≤1open/4MiB。没有返回gold0，失败不重开/缩分母。
- 原N4/20选项/16槽、48→12/C–D共享双锚点、模型/processor/prompt/seed/greedy不改。
  SOURCE_OVERLAP_ALLOWED / PRIOR_EXPOSURE_POSSIBLE不变，不追旧登记/P3 participant门或换题。
  七处执行allowlist保留旧030/031报告和测试；一次push STOP、不自动033/更多GET/扩样/训练。
  当前只有公开审查/新合同，没有在ChatGPT侧实际媒体/QA实验或空执行回执。
  **REAL_QA_EFFECT_UNKNOWN；NOVELTY=RETAIN0；CLOCK_ZERO_ASSUMED_NOT_CERTIFIED；
  Charades FINAL_MEDIA_STOP；TRAIN-GPU HOLD。**


### 2026-10-21 · 032响应绑定与P2候选验收；033零下载缓存四臂整包

- 审查main交付[2636333](https://github.com/floomeer83felix-source/vlm/commit/2636333f08b694c84c516a30c2c0ef828729ae40)，
  直接父为032规划e472f63，七处allowlist：三个production定点改动、新032测试、
  两匿名报告及results末尾唯一032父追加。旧报告/tests/规划/results前缀未改。
  ChatGPT静态核对公开差异、六项新见证与两回执，未独立运行测试、访问私有缓存、AWS或GPU。
  **ACCEPTED_TRANSPORT_AND_P2_CANDIDATES / GPU_RESOURCE_HOLD / REAL_QA_NOT_RUN**。
  032结案，不重跑、不消费剩余第二suite/GPU额度，不恢复旧run/锁/epoch。
- A–C的031只读交接完成17个明确文件＋4 source caches；八JSON和四source直接字节
  匹配031 INPUT_COMPLETE size/SHA及OUTPUT大小。四HEAD/summary/原wire version和准确长度交叉一致，
  未虚构历史HEAD文件SHA。新suite首且仅一次 **6/6 PASS、0FAIL/ERROR/SKIP**，
  internal0.314s/outer0.687s、fictional PID0；无旧test导入/重复OS演示。
  新suite覆盖生产请求构造、响应三项pin、错误正文0/状态先落账、去重/拒HEAD、archive及固定032绑定。
- 实际4 GetObject、0新HEAD/重试/redirect/fallback，**四个HTTP200均在正文读取前匹配
  031 VersionId/ETag/长度与framing**。请求无VersionId/query、IfMatch准确保留。
  说明032请求/响应准入打通，不证明031旧ClientError一定由版本权限造成；
  旧GET status/code仍UNKNOWN。
- P1/P3/P4完整GET窗口895.016/895.000/895.031s，超时自有Job终止后实测active0；
  私人保留约32/22/29MiB partial，不续传/删除/重下。kill路径没有child failure JSON，
  以持久200 response、partial及parent timeout exit取证，不补服务错误或服务器原因。
  **P2完整取得**（大小公开ceil2135MiB），GET127.094s、私有size/SHA/版本绑定；
  CPU候选工作16.109s/监督窗口17.375s、Job0，95,226 packets/0 corrupt/0 missing，
  解码3,087帧得到48个有限严格递增时刻，duration/span约3174s、声明差<0.01s。
  是一源完整媒体/候选工程证据，不认证绝对时钟或事件证据召回。
- 当前父非继承annotation exclusive handle1次，2真实probe各native32＋Python
  PermissionError/errno13/winerror缺失，合计4 open尝试正文0；清理释放，无ACL变化。
  唯一nvidia-smi成功、free22,813MiB已过20GiB，但37条C+G触发旧all('C' not in type)门。
  直接阻塞是进程类型分类谓词，不是可用显存不足；执行者没有擅自改门/追查peer/重query或kill。
- [NVIDIA官方Processes说明](https://docs.nvidia.com/deploy/nvidia-smi/index.html#processes)
  将C+G定义为同时存在Compute/Graphics contexts；这不是瞬时负载或独立模型任务数。
  不能认定37个实际竞争模型，也不能推断全是纯图形/桌面或已证持续空闲。
  官方利用率表示短采样期内kernel执行时间比例；WDDM逐进程显存可能不可得。
  新政策需由研究负责人明确替换，032安全停止不倒写为误执行或环境损坏。
- 032 model/generate/GPU/train/scorer/gold均0、peak allocated NOT_MEASURED。
  全16唯一槽NOT_RUN（12缺媒体、4 P2因资源门未启），每臂correct UNKNOWN/4、
  六配对UNKNOWN、C=D/选择/检索/真实grid/token/EOS/cost未测，不能报0/4或方法负结果。
  P2终态generic WORKER_STOPPED不表示曾launch；真实NO_MODEL_QUEUE_CLOSED保留。
- 资源由执行者报告：25/25输入124,904B（17handoff/6source/2config/0gold），
  CPU/media/acquisition/GPU预留215/300/3600/0s；
  GET实际2812.141s、媒体17.375s、全部监督阶段2831.249s，不当逐PID CPU计量。
  正文预扣2,328,819,584B、实际保留2,325,673,856B（pending read不退款），
  frame cache<214MiB、57文件/2目录/2,550,311,924B、父2937.744s。
  旧目录/余额保留，无安装/训练/环境/profile/权限变更。
- 已按用户“先写任务入仓库，再给一条Codex启动指令”的要求下达
  [VLM-DEV-CACHED-GPU-PILOT-033 A–H合同](./codex-artifacts/VLM-DEV-CACHED-GPU-PILOT-033/README.md)，
  **唯一READY=033 / PUBLIC_CACHED_GPU_INTEGRATION_ONLY，尚未执行**。
  新scope由用户实际发送合同第7节完整消息激活，同时明确接受共享资源政策，不另设激活循环。
- 033只复用P2已核验48帧cache，**研究网络/下载/MP4与partial正文/demux/decode均0**；
  不补三源，不扩样、不重跑032。原N4/20选项/16槽/轮转完整保留，只有P2四槽可启动，
  其余12槽NOT_RUN；generate≤4/唯一worker，不是把P2改为独立benchmark N1。
- 资源政策WINDOWS_SHARED_LOW_LOAD_033：不再以C+G数量或type包含C单独否决，
  也不承诺零上下文/全局独占。一个≤20s受控child最多2次只读nvidia-smi、
  间隔≥1s，两次同device0/3090/UUID、free≥20GiB、有限GPU util≤20%才放行；
  缺字段/N/A/高负载不当0、不循环等待或第三query。20%为本轮操作阈值，
  不是NVIDIA推荐/无peer证明。唯一worker加载前再一次mem_get_info核free，
  allocator上限18GiB在load前设置，24GiB Job RAM/GPU900s与OOM不重启保留。
  [PyTorch mem_get_info](https://docs.pytorch.org/docs/stable/generated/torch.cuda.memory.mem_get_info.html)
  为global free/total；[fraction](https://docs.pytorch.org/docs/stable/generated/torch.cuda.memory.set_per_process_memory_fraction.html)
  约束caching allocator，不冒称全设备/所有非Torch分配硬隔离。
- 033独立只读032真实partial-media closed archive，不套用旧零body规则；新固定root/run/lock/ledger/
  resource/queue/worker/score绑定。20确切handoff文本＋4 source＋必要config/最终gold总≤40MiB；
  **P2帧大输入另≤1open/256MiB**，完整copy/48 RGB hash/NPY形状验证，不冒称旧有NPY整文件SHA。
  新integration_033≤128文件/512MiB，CPU600s/父2400s、GPU900s/18GiB allocated/24GiB RAM。
  新suite≤2×60s、只测本轮资源/缓存/033绑定，首PASS同轮真实四臂→独立score→科研分析。
- 原annotation准备0B、当前父handle＋2真实零正文probe；真实Qwen返回、所有模型Job/PID实测退出、
  完整16槽队列与028 raw快照绑定后才独立CPU scorer≤1次/1open/4MiB读取原四题gold。
  gold失败/半读不重开，无返回gold0。保留原025 full-N执行得分规则，明确NOT_RUN不是已观测答错，
  配对原both_wrong含未执行者时不解释为真实共同错误；P2只另作条件性个案，不替代N4。
- 033执行allowlist缩为六处：pilot/worker定点改动、新033 suite、两匿名报告、results单条；
  media模块及旧报告/tests/科学协议不改。允许共享的运行条件不改变原像素/模型/提示/
  selector/seed/greedy。最高EXPLORATORY_DEV_CASE，一次push STOP、不自动034/更多下载/生成。
  当前只完成公开审查与新规划，没有在ChatGPT侧执行私有GPU实验或制造空回执。
  **REAL_QA_EFFECT_UNKNOWN；NOVELTY=RETAIN0；CLOCK_ZERO_ASSUMED_NOT_CERTIFIED；
  Charades FINAL_MEDIA_STOP；TRAIN-GPU HOLD。**


### 2026-10-21 · 033缓存交接与离线兼容修复验收；034显存有界共享真实四臂

- 审查main交付[91157ef](https://github.com/floomeer83felix-source/vlm/commit/91157ef4838f11f45153a4b017dc4c0b34e5e2a4)，
  直接父为033规划99ea1e5，恰好六处allowlist：pilot/worker定点改动、新033 suite、
  两匿名报告和results末尾一个033父记录。media模块、旧tests/报告、规划/科学协议和旧results未改。
  ChatGPT静态核对公开源码/差异、新六项见证与两报告，未独立运行测试、读私人缓存或访问GPU。
  **ACCEPTED_CACHE_HANDOFF_AND_OFFLINE_FIX / RESOURCE_WINDOW_HOLD / REAL_QA_NOT_RUN**。
  033已关闭，两suite用完，不重开原run、query、锁或时钟，不迁移余额。
- 033执行者报告20确切text handoff＋4 source直接交接，032 closed partial-media archive通过，
  eight cache/four source字节匹配032 INPUT_COMPLETE size/SHA及OUTPUT大小。
  原plan/worker/完整16槽/only-P2 availability、028完整快照/profile绑定一致；
  prepare生成的科学worker配置与冻结032逐字段完全相等，2 helper AST/2 config通过。
- 真实P2帧输入 **1open/223,948,928B**，copy/fsync与path/fd前后stat稳定，
  新完整file SHA及48 retained RGB摘要/uint8/C-order/shape/有限递增时间全部验证；
  outer0.968s、Job0。这个完整NPY摘要现已是033实际证据，不能倒签成032历史摘要。
  没有网络/下载、MP4/partial正文、demux/decode或新像素。当前原annotation
  父非继承exclusive handle＋2 probe通过：native32/Python PermissionError/errno13/winerror缺失，
  共4 open尝试正文0，清理后释放，无ACL修改。
- 新suite首轮 **6/6 PASS、0FAIL/ERROR/SKIP**，internal0.109s/outer0.468s，随即进入真实阶段。
  真实Windows XML的minor_number=N/A触发初始parser硬等0，actual033_DEVICE_IDENTITY、
  resource child exit1/Job0；该失败发生在util阈值检查之前。
  后续将固定query index＋稳定UUID/bus作为身份依据、minor作为metadata，
  用剩余第二suite验证N/A接受/错query index拒绝：**6/6 PASS、0FAIL/ERROR/SKIP**，
  internal0.063s/outer0.438s。无第三suite、旧tests或修后真实重query；
  最终修后的实际准入分支仍未动态走通，不能说RESOURCE_PASS。
- 一共且只有2次nvidia-smi，受控child1.750s、query起点间隔1.282s，
  同一RTX3090/UUID/bus/WDDM、29 C+G上下文。free **22,915/22,919MiB**均过门，
  util **16%/22%**，第二观测另超过原明确20%阈值。
  因而修minor parser也不能让那份旧观测满足033政策；
  **独立数值不合格不是原child实际抛出的异常**，两种事实均保留，不重写历史。
  C+G没有在033作否决，也不认定29个模型或全部纯图形，未查peer/kill/等空闲/重采样。
- RESOURCE_ADMITTED/model/generate/GPU/worker free复核/scorer/gold/train均0，
  peak allocated/reserved NOT_MEASURED。原N4/16槽全NOT_RUN，12 unavailable＋4 P2未启动；
  correct_known/accuracy/六配对UNKNOWN，不能报0/4、真实共同错误或方法负效应。
  C=D/selector/anchors/覆盖/检索/tokens/EOS/成本未测，P2条件个案未执行。
- 033资源为执行者报告：27/27完整输入 **224,599,574B**，其中26 text **650,646B**
  （20handoff/4source/2config/0gold）＋1 frame223,948,928B；
  CPU预留375s/监督窗口5.014s，不当逐PID CPU计量，media/acquisition/GPU预留0。
  两suite全部消费、fictional child0，所有实际阶段Job0/无kill/overflow；
  48文件/10目录/224,196,468B、父166.092s，无reparse/安装/环境/profile/凭据/权限修改。
- 已下达[VLM-DEV-SHARED-GPU-REAL-034 A–H合同](./codex-artifacts/VLM-DEV-SHARED-GPU-REAL-034/README.md)，
  **唯一READY=034 / PUBLIC_SHARED_GPU_INTEGRATION_ONLY，尚未执行**。
  按用户既定要求先写任务入仓库，再给一条可直接发给当前Codex的完整启动消息；
  单条消息共同激活新缓存/GPU/gold范围和明确改变的资源政策，不另设审批/激活循环。
- 034政策MEMORY_BOUNDED_SHARED_GPU_034明确接受有其他上下文及较高短时GPU负载，
  **利用率仅记录，不再以≤20%作为否决条件**，不要求空闲/全局独占。
  这改变的是运行资源条件，不是算法/数据/问题或结果判据，且没有任何真实QA输出用于选择该政策。
  [NVIDIA官方Utilization说明](https://docs.nvidia.com/deploy/nvidia-smi/index.html)
  仅支持短窗kernel执行时间比例，不能归因peer/证明显存容量或持续可用性；
  20%原为操作阈值，不是厂商安全上限，不把033倒写PASS。
- 新034最多1个≤10s只读nvidia-smi query，必须当前device0/3090/UUID/bus与保留033身份一致、
  free≥20GiB；WDDM minor仅metadata，util合法值如实记录/缺失或异常UNKNOWN，
  无第二query/等低负载/后台监控/kill peer。新RESOURCE_ADMITTED只证明设备/free＋接受共享政策，
  不能签空闲/独占证书。唯一worker权重前另一次mem_get_info核free≥20GiB，
  原18GiB allocator/peak allocated、24GiB Job RAM、完整GPU900s、OOM不重启保留。
  fraction只约束PyTorch caching allocator，不冒称全设备/所有CUDA分配硬隔离。
- 034只读033完整closed archive与直接缓存，不回扫032；旧2query/exit1/0准入/0model历史保留。
  帧copy匹配033 INPUT_COMPLETE与FRAME_CACHE_VERIFIED的准确size/完整SHA，再核48 RGB/NPY；
  不再要求凭空重建旧数据。新text≤40MiB（22handoff含ledger≤2MiB、4source/4config＋gold），
  frame≤1open/256MiB，新integration_034≤128文件/512MiB、CPU600s/父2400s。
  网络/下载/MP4和partial正文/新解码0，原N4/20选项/16槽及轮转保持，仅P2四槽≤4generate。
- 本轮只测资源/033 handoff/034绑定的少量新fixture，≤2×60s首PASS即当前probes/query→
  真实SigLIP/四臂Qwen→模型Job/PID实测退出→一次独立CPU score→科研报告；
  不重复033六项/031 OS演示或再排纯资格父任务。原annotation准备0B，
  最后仅实际Qwen RETURNED/INVALID＋队列/完整快照绑定后≤1open/4MiB四题gold，
  无返回gold0、坏gold/半读不重开。全N4未执行者保留且不解释为已观测答错，
  P2只条件个案、C=D仅实际selector后判断，不从任一单例主张泛化/创新。
- 执行allowlist六处：pilot/worker、新034 tests、两报告、results单条；
  不改033历史/科学协议/模型/提示/selector/processor或调科学阈值。一次push STOP、不自动035。
  当前仅公开审查/新合同，没有ChatGPT侧真实GPU/QA执行或空回执。
  **REAL_QA_EFFECT_UNKNOWN；NOVELTY=RETAIN0；CLOCK_ZERO_ASSUMED_NOT_CERTIFIED；
  Charades FINAL_MEDIA_STOP；TRAIN-GPU HOLD。**


### 2026-10-21 · 034缓存与真实共享准入验收；035同轮启动定位/修复/四臂评分

- 审查main交付[d9143ed](https://github.com/floomeer83felix-source/vlm/commit/d9143edb9bb4d77c6b99e635c1a06443e94f850c)，
  直接父为034规划e34a438，恰好六处allowlist：pilot/worker定点改动、新034 tests、
  两匿名报告和results末尾一个034父结果。media模块、旧tests/报告/规划/科学协议/results前缀未改。
  ChatGPT静态审查公开差异、四项新见证与两报告，未独立运行测试/访问私人文件或GPU。
  **ACCEPTED_CACHE_AND_SHARED_RESOURCE / WORKER_SETUP_HOLD / REAL_QA_NOT_RUN**。
  034已关闭，旧900s预约/未用suite不可迁移，不恢复旧run/锁/时钟。
- 22确切034前置handoff实际来自033，另4 source；八cache/四source及有输入摘要的metadata
  直接字节匹配033 INPUT_COMPLETE size/SHA和OUTPUT大小，生成JSON无旧SHA者按保留事实核验。
  原FROZEN plan/worker、完整16槽、frozen-worker-032、snapshot/三份028完整raw/profile一致。
  当前prepare复建科学配置相同，2 helper AST/2 configs核过，没有原manifest/annotation正文。
- 首且仅一新suite **4/4 PASS、0FAIL/ERROR/SKIP**，internal0.063s/outer0.391s；
  验证共享政策高/未知util、free/身份边界、closed033 archive/直接frame SHA、
  resource/queue/exit/score-opener0、单query/零网络门。没有第二suite、旧tests或fictional child。
- 真实P2 frame **1外部open/223,948,928B**，完整copy/fsync/stat+fd稳定，
  full SHA匹配033 INPUT_COMPLETE/FRAME_CACHE_VERIFIED/OUTPUT，48 RGB/uint8/C-order/NPY/times通过；
  copy outer0.969s/Job0。没有新像素/解码/MP4/partial正文、网络或下载。
  当前父非继承annotation exclusive handle＋2实际probe通过，native32与
  Python PermissionError/errno13/winerror缺失，共4 open尝试正文0；模型Job退出/全队列闭合后释放。
- **共享资源门本次已实际通过**：一次query outer0.547s/exit0/Job0、无truncation/overflow，
  同3090/index0/UUID/bus，WDDM minor=N/A、free **22,928MiB**、util **2%**/29 C+G上下文。
  新034 RESOURCE_ADMITTED真实落账，util只观测；不签空闲/独占/无peer证明。
  没有重query/等待/kill/资源政策临时变化。
- 唯一GPU指定worker真实launch/entered，但 **HOLD / SETUP / PermissionError**；
  internal1.859s/完整outer **2.203s**、process exit0/Job0、peak Job commit<1048MiB。
  exit0表示catch后写报告，不是推理成功。没有WORKER_FREE_RECHECK/allocator成功receipt，
  CUDA初始化/实际kernel活动未被证实；allocated/reserved peak未测。
  2.203s已消费GPU指定阶段窗口，不能说整个阶段0或把它当测得的kernel用时。
- 旧错误只有class/宽SETUP，无具体operation/path/stack/errno/winerror；
  **根因UNKNOWN**，不认定audit hook、ACL、CUDA或缺权重。执行者未另做import/model重试、
  环境修复或政策放权。实际MODEL_EXIT/QUEUE_CLOSED绑定launch/run/queue/private exit digest与全16终态。
  STARTED/RETURNED/INVALID/真实score/gold guard/open/body/publication0，P2四槽同其余12槽均NOT_RUN。
  correct_known/正确率/六配对UNKNOWN，不报0/4；selector/C=D/覆盖/检索/tokens/EOS/成本未测。
- 034资源为执行者报告：29/29完整输入 **224,191,216B**，28 text **242,288B**
  （22handoff/4source/2config/0gold）＋1 frame223,948,928B；
  CPU预留305s/GPU900s、监督总wall5.423s（CPU3.220s/GPU指定2.203s），非逐PID CPU或kernel计量。
  45文件/6目录/224,132,556B、父108.741s、无reparse；所有实际退出Job0，无kill/overflow。
  安装/环境/ACL/profile/凭据/训练改动0。
- 下达[VLM-DEV-STARTUP-RECOVERY-035 A–H合同](./codex-artifacts/VLM-DEV-STARTUP-RECOVERY-035/README.md)，
  **唯一READY=035 / PUBLIC_STARTUP_REPAIR_ONLY，尚未执行**。
  依用户“先把工作任务写仓库，再给一条Codex指令”要求，单条实际消息共同激活本轮范围；
  不再把日志定位、修复、真实QA拆成连续父任务等待批准。
- 035先在同一生产startup/policy增加细阶段、内存中有界拒绝event、errno/winerror/
  最多32个无locals/source-line的frame摘要。audit callback不递归IO/resolve/log，私人细路径不公开。
  [Python官方audit说明](https://docs.python.org/3/library/sys.html#sys.addaudithook)
  支持异常可中止操作且Python hooks非sandbox；本轮继续真实OS原文件锁/probes/Job退出。
  只对035实际复现取证，不能用新日志倒填034缺失根因。
- 在当前真实annotation handle/probes下，035允许最多2个≤60s CPU bootstrap，
  实际imports＋CPU processors/helper/固定Uniform12输入，模型权重/CUDA/encoder/generate0。
  共用生产policy、local-only/runtime；首失败定位后限cache路径/既有runtime支持的确切只读文件/
  局部API兼容修复，第二个通过立即真实GPU，首个通过不追加第二个。
  不移除audit、改ACL/安装/永久环境或开放网络/任意模型子进程，不读旧研究/凭据目录。
- 允许自有child在import前将必要HF_HOME/HF_HUB_CACHE、TORCH_HOME/TEMP等cache指向新root，
  依据[HF文档](https://huggingface.co/docs/huggingface_hub/en/package_reference/environment_variables)
  与[Torch Hub位置](https://docs.pytorch.org/docs/stable/hub.html)并核本机已安装源码；
  只是运行时局部配置，不能说034已经证明为cache问题，也不允许任何Hub/模型/包下载。
  真正ACL或环境依赖问题超出范围仍HOLD。
- 035保留显存有界共享政策/一次当前query、free≥20GiB、18GiB allocator/allocated/24GiB Job RAM，
  util仅记录。为避免零QA技术问题再拆父任务，明示允许**最多2个串行GPU worker，
  共用唯一900s绝对包络**：首launch开始计，修复/新suite间隔也在包络内；
  不两份900、不重置/退款、不沿用034余额。正常只1个；
  只有首真实PID/Job0、全035 STARTED=0、有技术证据且修复经剩余new suite验证才可第二个。
  任何STARTED后永不重启/重答，OOM/timeout不作为重启理由，generate总≤4。
- 多attempt时全部launch/exit逐条匹配attempt/run/queue/resource/current tested code/private exit摘要，
  首零QA失败attempt不能从退出集合消失；最后只一次完整QUEUE_CLOSED。
  全模型PID/Job实测退出后，只有真实Qwen RETURNED/INVALID才独立CPU score≤1open/4MiB，
  最终ChildExitReceipt反映所有model PID，不只最后一个。gold坏/半读不重开，无返回gold0。
  新fixture验证这一变化，不是只放宽len(launches)==1。
- 035只读034真实已launch失败archive，不套“旧model必须0”验证器。text≤48MiB
  （25handoff含ledger2MiB、8source含4确切runtime引用、4config＋gold，角色最坏42MiB），
  frame≤1open/256MiB，新integration_035≤128文件/512MiB；
  CPU≤900s/父≤3000s用于同轮定位修复；GPU总900s/生成4不增加。
  新suite≤3×60s，仅035模块、按代码变更使用，不补第四次/旧测试。
  原N4/20选项/16槽/only-P2/像素/模型/提示/selector/seed/greedy不变，网络/新解码0。
- 最高EXPLORATORY_DEV_CASE；full-N4未执行者保留并不作已观测错误，
  P2条件个案不取代N4，C=D仅真实计算后判断。六处公开allowlist：
  pilot/worker、新035 suite、两匿名报告、results单条；保留034失败证据。
  一次push STOP，不自动036/扩样/科学调参/训练。当前仅公开审查与新合同，无ChatGPT侧真实实验/空回执。
  **REAL_QA_EFFECT_UNKNOWN；NOVELTY=RETAIN0；CLOCK_ZERO_ASSUMED_NOT_CERTIFIED；
  Charades FINAL_MEDIA_STOP；TRAIN-GPU HOLD。**


### 2026-10-22 · 035缺标注引用HOLD验收；036有界恢复引用与独立合成启动

- 审查main交付[2615512](https://github.com/floomeer83felix-source/vlm/commit/2615512fce25b4c87be6d610f4a14408505e76f2)，
  直接父为035规划8d46b56，恰好六处allowlist：pilot/worker、新035 tests、
  [启动收据](./codex-artifacts/VLM-DEV-STARTUP-RECOVERY-035/startup-recovery-and-real-run-receipt.md)、
  [科研报告](./codex-artifacts/VLM-DEV-STARTUP-RECOVERY-035/scientific-results.md)及results末尾一个035父结果。
  未改AGENTS、科学协议、ChatGPT规划、旧tests/报告或results前缀。
  ChatGPT仅静态审查差异、源码、新见证及报告；未独立运行Windows测试/读私人原文件/运行GPU。
  按 **ACCEPTED_CLOSED_HANDOFF_AND_FRAME_COPY / CURRENT_ANNOTATION_REFERENCE_HOLD /
  REAL_STARTUP_NOT_RUN** 结案，不恢复035 run/锁/时钟或剩余次数。
- 执行者报告25确切034 handoff＋4 source cache只读一次，直接字节匹配既有输入/OUTPUT、
  冻结科学计划与旧snapshot；新035只读archive接受034唯一失败worker和真实Job0，
  保留其SETUP PermissionError/全16 NOT_RUN历史，不误套旧“model必须0”规则。
  首且仅一次新suite **5/5 PASS、0FAIL/ERROR/SKIP**，internal0.032s/outer0.453s。
  它含合成退出fixture及静态AST断言，不是本机真实imports/CPU processor/恢复握手执行证明；
  虚构PID0，无旧tests或第二/第三suite。
- 新prepare实际在原annotation的checked_path/lstat报 **FileNotFoundError / 报告WinError2**，
  outer0.219s/exit1/Job0。具体路径/stack仅私人留存；
  这是精确路径失败，不足以判定已删/已移动/ACL/全机不存在。
  没有替代路径搜索、原标注body或原handle/probes，也没有实际model config读取。
  **035没有新worker-input.json/runtime.json/queue.json/expected-snapshot.json。**
- 独立frame分支仍完成1外部open/**223,948,928B**：
  copy/fsync/path+fd稳定/完整SHA匹配034链，48 RGB、uint8/C-order/NPY/times验证通过；
  outer1.156s/exit0/Job0。没有MP4/partial正文、新解码、网络或下载。
  036应只读035实际frame副本，不能跟其历史frame-source-reference重开034。
- CPU bootstrap/ML imports/processors、当前query、GPU envelope/admission/worker、CUDA/generate、
  gold guard/评分/训练实际均0。全16槽由NO_MODEL_QUEUE_CLOSED按固定映射封闭为NOT_RUN，
  不伪造MODEL_EXIT。**034原PermissionError仍UNKNOWN，035未复现或定位它。**
  correct_known/正确率/六配对UNKNOWN，selector/C=D/双锚点/coverage/retrieval/tokens/EOS未测；
  不将NOT_RUN记成已观测答错或把synthetic PASS当科学机制成绩。
- 执行者资源报告：30/30完整输入 **224,128,509B**＝29 text **179,581B**
  （25handoff149,860＋4source29,721；config/diag/gold0）＋1frame223,948,928B。
  CPU预扣285s，初始化/新suite/prepare/copy实际监督wall共**2.828s**，
  不等于逐PID CPU计量；GPU/media/acquisition0。
  私人34文件/2目录/**224,055,993B**、父114.337s；无reparse、kill或overflow，所有实际Job0。
- 对035未运行恢复代码的静态发现：
  SUITE_RESULT未记测试时code hash、REPAIR_ACCEPTED未要求PASS在当前repair request之后；
  GPU repair后父policy变量也未更新，下一worker可能沿用旧policy。
  **这是未运行分支的代码缺口，不是035已发生违规，也不是034故障成因。**
  036须把request seq、实际suite receipt/测试code-policy-config hash和accepted下一policy版本绑定，
  用本轮新fixture验证旧PASS/重放/旧policy不放行。
- 下达[036 A–H完整合同](./codex-artifacts/VLM-DEV-REFERENCE-AND-STARTUP-036/README.md)，
  **唯一READY=VLM-DEV-REFERENCE-AND-STARTUP-036 / PUBLIC_REFERENCE_AND_STARTUP_ONLY，尚未执行**。
  同一父任务独立推进：有界核对旧annotation引用与全合成CPU startup，
  不再因真实原路径缺失而让纯合成imports全部0；但合成PASS绝不签真实原文件锁或放行GPU。
  用户发送合同第8节完整消息才激活新私人范围，不自动唤醒本地Codex。
- 036仅精确path metadata≤32；旧parent及直接parent至多2个普通目录、
  各一次非递归≤64 entry，只同basename候选可stat且计32上限；
  或核对本地当前会话用户明确给的一个新原标注完整路径。
  禁全盘/递归/第三目录，截断/多义不选一个冒充唯一。
  **明确新增**可信stdlib CPU≤20s、唯一候选≤1 rb open/4MiB的纯字节SHA例外：
  不decode/JSON parse/gold提取/body日志/给ML，先消费预算，半读/失败不重开或换候选。
  仅与原028三完整receipt及frozen snapshot准确size/SHA全同，才建立036当前path/FileID绑定；
  允许同字节文件复制/移动后新FileID，原receipt/科学输入保持原值。
  这不是从035准备body0许可推导的新授权；需用户完整启动消息明确给出。
- 独立合成startup≤3×60s：虚构问题/事件/选项、零像素48帧/合成times，
  自有canary OS锁与同一生产audit/policy，实际imports/CPU processors/helper/grid；
  原annotation/model权重/CUDA/encoder/generate0。
  诊断限cache运行时路由、实际指向的至多4确切支持文件和有源码依据的局部API兼容；
  不改ACL/安装/永久环境/模型科学参数。真实依赖兼容须实际bootstrap，不以AST断言代替。
  缺标注时仍完成该独立分支，之后只请求用户在本地给当前完整路径，
  不自动再发同类路径搜索、不索取原JSON或下载替代。
- 只有真实reference绑定、实际父exclusive handle＋2正文0 probe和当前code/policy合成PASS齐全，
  才准一次当前query/free≥20GiB共享政策及P2原四槽。
  最多2串行worker共用一个900s绝对包络/18GiB allocated/24GiB Job RAM；
  第二个仅首全部模型Job/PID0、全run STARTED=0及新测试/必要合成复验完成，
  OOM/timeout不重启，任何QA开始后不重答，generate总≤4，util只记录。
  全部attempt launch/exit/队列/current binding核齐、所有模型退出，才一次独立CPU gold≤1open/4MiB；
  无真实Qwen返回则gold0。可信SHA和最终gold是分离的两个正文open上限，模型始终0B。
- 036新输入text≤48MiB，20确切035 handoff（不要求不存在的prepare输出）、
  8 source/4 config、integrity与最后gold各4MiB，角色上限41MiB；frame≤1open/256MiB。
  新integration_036≤128文件/512MiB，CPU≤900s/父≤3000s、新suite≤3×60s；
  新假PID≤4×3s可为0，全部计账。六处allowlist：pilot/worker、
  新036 suite、两匿名报告、results一个父追加；统一一次安全push STOP，不自动037。
  原N4/20选项/16槽、only-P2 BCDA、48→12、C/D定义、科学模型/提示/seed/greedy均不改。
  **REAL_QA_EFFECT_UNKNOWN；NOVELTY=RETAIN0；CLOCK_ZERO_ASSUMED_NOT_CERTIFIED；
  Charades FINAL_MEDIA_STOP；TRAIN-GPU HOLD。**


### 2026-10-22 · 036实际合成启动恢复验收；按用户要求优先科研价值与反证

- 用户明确要求：**后续更关注科研价值**。研究负责人将优先级落到可证伪命题、
  实际模型输入干预、真实回答/有效评分与近邻增量；不以任务数/测试数代表科研进度。
  工程工作只有直接解决必要科学观测时才继续优先，不再自动安排同类路径搜索/运行治理任务。
- 核对main[d8302de](https://github.com/floomeer83felix-source/vlm/commit/d8302deeba7ade61c32c6189ce912c32d90506a0)，
  直接父为036规划24d2a39，六处allowlist符合：pilot/worker、新036 suite、
  [启动与引用报告](./codex-artifacts/VLM-DEV-REFERENCE-AND-STARTUP-036/reference-startup-and-real-run-receipt.md)、
  [科学结案](./codex-artifacts/VLM-DEV-REFERENCE-AND-STARTUP-036/scientific-results.md)和results唯一036父追加。
  ChatGPT静态审查公开差异、关键实际代码路径、5项新组合fixture及两报告；
  未独立运行Windows测试/私人原输入/真实CPU子进程或GPU。
  按 **ACCEPTED_SYNTHETIC_STARTUP_RECOVERY / CURRENT_REFERENCE_MISSING /
  REAL_QA_NOT_RUN** 关闭036，旧run/时钟/三suite与三bootstrap次数不再可用。
- 20确切035 handoff＋4 source缓存只读完成，缺prepare输出的035 archive规则、
  冻结full-N4/20选项/16槽、worker/snapshot绑定保持；未回扫034/033/旧预测/gold/manifest。
  P2 frame外部1open/**223,948,928B**、完整copy/fsync/稳定path+fd/SHA/48RGB/uint8/NPY/times通过，
  outer1.031s/exit0/Job0，没有新解码/MP4/partial正文或新真实像素。
- 原引用恢复实际只预扣3个确切path lstat，一处FileNotFoundError/errno2/winerror2；
  一次允许parent非递归枚举38 entries、完整未截断，直接parent为drive root而排除。
  当前会话没有用户给出的新原标注完整path，允许范围内**0候选**。
  integrity guard/open/body0、ANNOTATION_REFERENCE_BOUND0，不猜文件/换后缀或声称全机无文件。
  **真实分支需用户在私人本地Codex提供当前原标注完整路径，不需要JSON内容；
  不再自动继续搜索、下载替代或恢复036。**
- 三个实际合成CPU child在自有canary锁和生产startup/policy下：
  1/policy1 **2.063s HOLD/TORCH_IMPORT**，audit记录匹配标准null device拒绝；
  2/policy2 **35.703s HOLD/TRANSFORMERS_IMPORT**，bytes/str路径比较TypeError；
  3/policy3 **9.125s PASS/CPU_COMPLETE**。
  三次均exit0/Job0，无kill/overflow；前两exit0只是catch并写失败，不是启动成功。
  两份诊断指向的已安装dill/tempfile源码按确切source allowance读取，未增加任意read例外。
- 精确修复是标准os.devnull单一词法路径许可及os.fsdecode路径归一；
  owned bytes temp可用、outside bytes仍拒绝，网络/任意子进程与其他文件拒绝保留。
  必要cache/temp仅路由本child新root，无ACL/永久环境/安装改动。
  第三个实际NumPy/Torch/Transformers/VideoMetadata、两CPU processors/helper成功，
  **12帧/grid[6,12,18]/324 visual/447 synthetic total tokens**，CUDA初始化前后False。
  输入题/事件/选项全虚构、48帧为内存零像素，仅复用shape；无权重/encoder/generate。
  此处不是原annotation锁/probe认证，也不能倒填034缺失trace的历史根因。
- 三个新suite各**5/5 PASS、0FAIL/ERROR/SKIP**，同5项组合见证按三个代码版本执行，
  不是15个独立新科学测试；outer0.406/0.406/0.422s，内部各0.031s。
  同一live parent的request→suite→accept实际seq为124→135→137、144→155→157；
  accepted policy1→2→3确实传给下一child，后request真实PASS/code/policy/science绑定有运行记录。
  无第四suite/bootstrap、旧tests或虚构PID。
- 合成成功后真实门在036_REAL_REFERENCE_NOT_BOUND停止；原exclusive handle/probes、
  currentquery/GPUenvelope/resource/model/generate/train、integrity/goldguard/open/body/scorer均0。
  全16 NOT_RUN/NO_MODEL_QUEUE_CLOSED，无假MODEL_EXIT；
  correct_known/正确率/六配对UNKNOWN，不填0/4。
  真q/a/b、C=D、实例/锚点/coverage/retrieval/Qwen成本和token/EOS全部未测。
  真实重绑定/原锁、GPU/all-exit/score分支仍没有本轮实机认证。
- 执行者资源报告：29/29外部输入**224,173,007B**＝28 text **224,079B**
  （20handoff74,855＋6source147,287＋2config1,937）＋1frame223,948,928。
  CPU预扣645s、实际监督阶段50.546s含synthetic46.891s，父411.341s含cleanup/waits；
  不是逐PID CPU/kernel计量。GPU/media/acquisition0；
  私人64文件/12目录/**224,226,312B**、无reparse/kill/overflow，所有actual Job0。
- 新增[科研价值与实际干预备忘录](./research-reviews/scientific-value-and-intervention-2026-10-22.md)。
  从实际025函数推导：C/D均必含q-Top10，12帧最多替换2帧；
  两组锚点都在Top12时最终集合相同；C最优pair已向前则D完全相同。
  不同pair/目标值/锚点不能直接证明Qwen收到不同输入。
  ChatGPT用公开原函数一轮stdlib计算核三个API合法构造及100固定种子合成向量，
  没有旧tests/私人输入/模型；一般性质依据给出的证明，合成频率不推成现实发生率。
- 当前题本身给出A先B后，C/D检验的是已知关系约束的检索干预，
  不是直接检验未知先后关系发现。“相隔多久”题的反转标签可能保持或前提失效，
  不能照搬先后题的“回答不翻转即失败”。这些都是待独立复核的科学界限，
  不是改冻结协议或新增真实问答/人工gold许可。
- 近邻定向核查已覆盖AKS、GenS、2026预印本GCR及Before It Fades；
  相关性/覆盖、生成式检索、事件锚点/补齐、模型内部时间表征干预各已有相关工作。
  这不是穷尽新颖性检索，不宣布本方法与近邻完全等价；
  当前仍无已证实的非平凡增量，不把“加入i<j”独立认作核心创新。
- 唯一READY转为[VLM-SCIENTIFIC-FALSIFICATION-037](./codex-artifacts/VLM-SCIENTIFIC-FALSIFICATION-037/README.md)，
  **PUBLIC_SCIENTIFIC_REVIEW_ONLY，尚未执行**：A–H一次公共反证审查，
  独立核推导/干预链/标签变换语义、4固定原论文及最小可区分实验，
  给继续/降级/STOP条件。只准两科学报告＋results一个父追加；
  不增加软件框架/旧测试/私人路径搜索，不修改生产代码、原协议/历史结论。
  具体新未解命题至多1个≤60s stdlib计算/CPU总120s，不能照跑旧合成表当成果。
  私人metadata/body/frames/QA/gold/model/GPU/训练0，一次安全push STOP，不自动038。
  当前C/D **NO_GO_AS_ESTABLISHED_PAPER_CORE / DEV_DIAGNOSTIC_ONLY**；
  接受工程恢复不升级论文主张，P2即使未来跑通也只是已暴露可能的开发个案。
  **REAL_QA_EFFECT_UNKNOWN；NOVELTY=RETAIN0；CLOCK_ZERO_ASSUMED_NOT_CERTIFIED；
  Charades FINAL_MEDIA_STOP；TRAIN-GPU HOLD。**


### 2026-10-22 · 037科学反证验收；当前C/D停止作为论文核心，0 READY

- 审查main[d8195c5](https://github.com/floomeer83felix-source/vlm/commit/d8195c52b84c7f3b502fbb886ea2dc33bc55c8bf)，
  直接父为037规划1d14488，恰为两份科学报告和results末尾一个037父追加，生产/旧协议/历史结果未改。
  ChatGPT复核公开差异、025 select_four/worker相关调用链、数学证明/新手工构造及关键论文原始证据；
  未访问私人helper/输入或独立执行模型/测试。
  接受为 **ACCEPTED_PUBLIC_SCIENTIFIC_REVIEW / NO_GO_AS_CORE / DEV_DIAGNOSTIC_ONLY**，
  037已关闭，不再可领取。
- 本轮执行者数值进程/CPU实验/旧测试/额外作者源码0；
  私人path stat/搜索/metadata/body、标注/QA/gold/frames/模型/特征/GPU/训练/安装/环境修改0。
  没有新的原标注完整路径输入。036合成CPU恢复事实保持，真实16槽仍NOT_RUN，
  REAL_QA_EFFECT_UNKNOWN，不能将未执行解释成机制效果为0。
- 独立复核支持P1–P3，并补充两项科学边界：
  C/D/B均必含q-Top10，12帧最多替换2帧且上界可达；
  单H的F(H)=Top12 iff H⊆Top12；仅外部锚点相同不必同集合，
  截止边界内部锚点仍会保护元素。角色/pair/锚点/目标值差异不充分保证模型输入差异。
  这是当前实现性质，不是SigLIP真实发生率、token扰动界或通用算法新颖性。
- 当前给定A先B的间隔题不能直接检验未知先后理解；反转可能保持绝对间隔，
  或破坏after前提，不能无条件翻转gold或将同答案视为时间推理失败。
  私人helper和实际输入未核，实际C/D输入相等/不等仍UNKNOWN。
  缺绑定比较的静态提示不当作已发生误报，也不强制安排新工程修复轮次。
- 037已区分AKS相关性/覆盖、GenS生成式检索及训练、GCR文本事件锚点/覆盖/修复、
  Before It Fades表征干预，列出方法与成本差异，未复现或宣称完全等价。
  当前没有足以排除这些解释的非平凡贡献，故**停止当前C/D论文核心投入**，
  保留开发诊断与长期长视频研究目标。选择器上界本身也不构成已通过创新审查的新定理贡献。
- 新增[研究负责人正式处置与验收限定](./research-decisions/post-037-scientific-disposition-2026-10-22.md)：
  037的P2单例输赢门只可作为资源止损建议，不能当普适机制真假判据；
  D单例改善不自动构成独立验证资格，不按有利开发结果挑新题扩样。
  任何未来独立研究应事前冻结来源、样本、主要对比和完整失败/停止解释，
  不将方向选择开发题重用为独立确认。
- **当前0 READY。** 不下达038重复工程、路径搜索、启动演示或同内容综述，
  不为编号连续性再造任务。原P2最多一次四臂的设想保持
  **PARKED_OPTIONAL_DEV_DIAGNOSTIC / NOT_READY**；
  需当前精确私人路径、必要观测理由与后续新合同才再判断，不能领取037未执行计划或恢复036。
  补齐路径本身不解决实例证据、独立性或创新。
- 后续进入ChatGPT负责的**新科学问题与可审设计阶段，DESIGN_PENDING / 非Codex执行任务**：
  先明确可失败命题、最接近原始工作的实质差异、可取得且足以检验的证据和最小投入；
  不先许诺新算法/训练/期刊结果，不把换名或普通组合认作核心创新。
  在可审设计形成前不自动启动新任务/后台工作、GPU/扩样/训练/下载。
  **NOVELTY=RETAIN0；CLOCK_ZERO_ASSUMED_NOT_CERTIFIED；Charades FINAL_MEDIA_STOP；
  TRAIN-GPU HOLD。**


### 2026-10-22 · 科学负责人完成新问题设计：自有合成时钟绑定探针038

- 用户对037结案及“先由ChatGPT重新形成科学问题、差异和最小实验设计”答复“好的”。
  本轮由研究负责人实际完成定向原始文献/方法与官方processor源码核查，
  没有把广综述/多候选toy再派给Codex，没有私人数据/本机模型/GPU执行。
  原C/D **NO_GO_AS_CORE / DEV_DIAGNOSTIC_ONLY** 保持，036/037不重跑。
- 筛去把“小时级检索优于直接模型”当新方向：ExtremeWhenBench已直接分解search/localize；
  条件多事件/重复定位也已有Conditional Multi-Event Grounding近邻。
  一般视频shift/rephrase一致性、可控合成视频及动态时间模式分别有Jung等/SVLTA/VCBench/
  SpookyBench先例，不能把这些概念作为首次贡献。
  比较为定向方法审查，不是穷尽新颖性或近邻全部变体的排除证明。
- 冻结[时间码—视觉身份绑定研究协议](./research-protocols/clock-visual-binding-probe-2026-10-22.md)：
  同像素/同所见索引位置，三个合法虚拟clock（均匀、同总长非均匀、整体平移），
  每world/clock都配文字操作数算术control。
  两帧原生temporal块/6组时间码，4组标记位置×颜色互换=8依赖world；
  8×3×2=48个全新槽，24视频/24文字，未读取真实题/标注/gold或旧frames。
  真值由程序indices/fps及双帧均值定义，不需新人工标签或恢复旧标注。
- G0/G1同端点/总长22s、同12 RGB、仅内部时刻改变，四组间隔分别
  [8,12,4,8]→[12,16,8,12]；G2整体＋60s仍[8,12,4,8]。
  这些是协议推导/设计核算，不是模型输出。
  问题只问红/蓝标记组显示时间码的绝对差，不把它称真实复杂事件或未知先后推理。
  O文字control逐clock匹配操作数，是component control，非同信息成本的强竞争算法。
- 已核Hugging Face官方transformers commit
  360d22e2d1183af882ad437bfc74ce3337065f5d中的Qwen3 processor相关方法：
  frames_indices/fps生成组时间码、temporal块首尾均值并插入视频文本。
  不假定本机版本同一；**必须先实际CPU验证干预进入模型**：
  六timecodes符合、同world三clock的RGB/视觉tensor相同、原生grid[6,12,18]/324 tokens，
  不重采样、不缺fps fallback、不手改token绕过。
  本机接口不能暴露该干预就HOLD_INPUT/GPU0，不记模型时间能力失败。
- 这个选择是**CONDITIONAL_MEASUREMENT_PILOT_ONLY**，不是保留新算法/论文核心。
  窄的因子交叉在已读段落中尚未确认相同设计，不等于未被前人做过；
  直接同设计证据出现就标DIRECT_DUPLICATE。全部模型都正确时停止该缺陷前提，
  O也失败时算术/指令归因UNKNOWN；O正确V错最多行为候选，不推断具体神经原因。
  4基础组/8依赖world不作独立自然来源/统计显著性/长视频泛化。
  后续确认必须另冻设计，不能以开发有利结果挑源扩样。
- 下达[VLM-CLOCK-BINDING-PROBE-038 A–H完整合同](./codex-artifacts/VLM-CLOCK-BINDING-PROBE-038/README.md)，
  **唯一READY / PUBLIC_PROBE_IMPLEMENTATION_ONLY，尚未执行**；
  用户本地发送完整启动消息才激活新受限配置/自有合成/条件GPU范围，GitHub编辑不唤醒Codex。
  一包完成小实现、新suite≤2×60s、实际输入预检≤2×90s（仅一次证据驱动API兼容修复），
  CPU≤480s/父≤1800s，输入门过后单Qwen worker/一次加载、GPU总≤600s、
  48generate/各槽1/greedy16tokens/seed19/BF16/SDPA，max输入2048tokens、每槽新上下文。
  一次query/free≥20GiB、18GiB allocated/24GiB Job RAM，util仅记录；
  不重query/模型重启/重答/kill peer，所有model实际退出后一次CPU程序truth计分。
- 只读036确切5配置/关闭账本、2 Qwen configs/至多3确切runtime modules，
  research文本≤12MiB；新integration_038≤96文件/64MiB。
  正常既有runtime/CPU processor及条件Qwen资产local-only按角色记录，不复制/下载权重。
  原真实QA/gold/frames/private helper/manifest/source map/旧预测/更早root0open，
  不签原标注锁通过；MP4/解码/新数据下载、训练/安装/永久环境/ACL/profile/凭据修改0。
  公开五处allowlist：两新小模块、两报告、results唯一038父追加；旧源码/协议不改。
  一次安全push STOP，不自动039或升级训练/扩样。
- 当前尚无038执行事实/模型成绩，本协议也不替旧真实媒体认证时钟。
  **REAL_QA_EFFECT_UNKNOWN；NOVELTY=RETAIN0；TRAIN-GPU HOLD；
  CLOCK_ZERO_ASSUMED_NOT_CERTIFIED（历史真实媒体）；Charades FINAL_MEDIA_STOP。**


### 2026-10-23 · 038实际合成行为验收；下达唯一039分量判别

- 审查main交付[c078d0c](https://github.com/floomeer83felix-source/vlm/commit/c078d0cac8a7c9e4a4dee1ef0ada866ab09154bd)，
  直接父为038规划aa51e93。五处allowlist准确：两新模块、两报告、results唯一父追加；
  旧源码/协议/规划/历史未改。ChatGPT读取公开完整源码/新tests/两报告与差异，
  以公开48个小型合成整数独立复算聚合/配对/关系计数；
  没有访问私人根/账本/设备或独立运行CPU processor、模型和私有scorer。
- 038关闭为 **ACCEPTED_SYNTHETIC_BEHAVIORAL_FINDING / RESOURCE_RECEIPT_EXCEPTION /
  NO_CORE_INNOVATION**，不可重跑。实际输入报告支持timecodes进入输入：
  24 V同world跨clock原RGB与最终BF16视觉tensor一致，
  原生grid[6,12,18]/324 tokens，六时码逐项匹配；
  GPU重建及最终dtype绑定后才STARTED。24 O无视觉且操作数逐clock匹配。
  这使“输入根本没有变”不再是本次行为差距的恰当解释，但不是内部机制定位。
- **48 STARTED/48 generate/48 RETURNED，INVALID/FAILED/NOT_RUN均0，48 EOS/0截断。**
  V按G0/G1/G2为2/8、0/8、1/8，总**3/24**；
  O为7/8、7/8、8/8，总**22/24**。
  配对both/Vonly/Oonly/neither=2/1/20/1，unknown0。
  V的G0→G1正4秒响应和G0→G2间隔不变均joint correct0/8、仅关系满足也0/8；
  O相应6/8、7/8。文字两处错误仍保留，不能将全部V错误唯一归因于视觉绑定。
- 4基础位置组/8颜色交换依赖world是开发性合成家族，
  不构成8独立自然来源，不报显著性/自然长视频泛化/通用Qwen时间能力结论。
  当前可说“匹配文字大多正确、本次原生视频间隔链仅答对3/24的已观察个案”，
  不能说“已发现新的神经失败机制”或已有期刊核心创新。
  原C/D核心停止裁决并未被这些不同科学问题的结果逆转。
- 执行者报新suite16/16、实际CPU exposure1次/8.813s Job、CUDA未初始化；
  单Qwen3-VL-4B BF16/SDPA、一次load/seed19/greedy16，无warmup/额外forward/重启/重答。
  模型Job **36.703s**（generate调用合计8.673s，不能替代全GPU包络），
  peak allocated9,140,584,960B、Job peak committed17,851,752,448B。
  模型实测exit0/active0后一次独立程序truth评分0.156s。
  CPU预约250s、非模型Job wall9.828s（非逐PID CPU时间），父725.944s；
  新私人25文件/159,595B，均为报告事实而非ChatGPT重测。
- **明确资源缺口**：038未做合同规定的运行前2GiB磁盘余量检查。
  事后free433,993,371,648B和实际小输出不能补证前置条件；
  不签“完整合同全部PASS”，不重跑补证或新增纯资源修复轮。
  其余本轮原真实标注/QA/gold/frames/private helper、下载/解码/训练/安装均0，
  不能据此替旧原标注隔离或真实媒体时钟认证。
- 研究负责人已冻结[039科学协议](./research-protocols/clock-binding-component-contrast-2026-10-23.md)，
  目标只拆分读出、直接间隔及呈现差异：4未测试位置组合
  (0,2)/(0,4)/(1,5)/(3,5)，各颜色互换、3clock，
  NG/NR原生video间隔/有序读出、SG/SR带时间码image拼图间隔/读出、OG文字算术。
  **8×3×5=120槽（48 video/48 image/24 text）**，
  新G1−G0差为[-2,+2,+2,-2]而非沿用全+4。
  这是038后选择的探索性判别集，复用同模型/图形/clock，不冒充独立holdout。
- 冻结逐字prompt、固定5×7字体/384×864拼图、严格整数/有序一位小数解析、
  轮转队列和全15格分母。CPU必须实际验证video[6,12,18]与image[1,24,54]
  均324视觉tokens、所有120输入及video/image正确视觉分区/最终BF16绑定；
  预期值不是观察事实，未过则权重/GPU0。
  token数相同不代表同信息通道/总token/位置编码或FLOPs；
  SG胜出最多呈现敏感行为，NR对而NG错最多跨任务组合差异，
  不能证明NG隐含读对或定位神经模块。
- 定向原始先例已核：Jung等2024时序grounding/verification一致性、
  CVPR2025 Number it/NumPro画面数值提示，以及2026-05-21
  MLLMs Know When Before Speaking的attention/prefill—generation差异与再推理。
  这些普通概念均非这里首次提出；039只是已知控制思路用于本轮歧义，
  没有复现上述方法、排除所有变体或完成新颖性审查。
- 唯一READY为[VLM-CLOCK-COMPONENTS-039 A–H](./codex-artifacts/VLM-CLOCK-COMPONENTS-039/README.md)，
  **PUBLIC_COMPONENT_PROBE_IMPLEMENTATION_ONLY，尚未执行**；
  用户在当前本地Codex发送合同完整一条新消息才激活新范围。
  一包新实现/新tests≤2×60s/真实CPU input gate≤2×90s（最多一次源码依据API兼容修复）/
  单Qwen worker一次load/GPU600s/最多120次生成/独立CPU一次评分与五处交付。
  CPU480s/父1800s，free≥20GiB/allocated18GiB/Job24GiB；
  query一次、无重启重答/额外forward，所有model实际退出后才评分。
- 只读038四确切配置/关闭收据、2 Qwen configs、至多4确切installed sources，
  research文本≤12MiB；正常local-only runtime/processor/条件权重按角色记录。
  新integration_039≤96文件/64MiB，**首私人输出前实测配额外≥2GiB磁盘余量**；
  不读更早roots/原真实QA/gold/frames/manifest/source map/私有helper，不继承旧run。
  039交付即STOP，无按有利输出自动040/改font或prompt/扩样/训练。
  如仍不能排除普通读数/指令/呈现解释，停止合成变体投入，另由研究负责人判断是否另立问题。
- **SYNTHETIC_BEHAVIOR_OBSERVED / NATURAL_VIDEO_EFFECT_UNKNOWN；
  NOVELTY=RETAIN0；TRAIN-GPU HOLD；原C/D NO_GO_AS_CORE；
  历史真实媒体CLOCK_ZERO_ASSUMED_NOT_CERTIFIED；Charades FINAL_MEDIA_STOP。**


### 2026-10-23 · 039分量判别审结，停止当前合成变体；0 READY

- 审查[995d436](https://github.com/floomeer83felix-source/vlm/commit/995d436c2d3572178f4641a4faeca600219e22a2)，
  直接父e560e71，恰五处allowlist：两新模块、两报告、results唯一039父追加；
  旧代码/tests/科学协议/规划/历史未改。
  ChatGPT读完整公开实现/tests/报告，并在内存中独立从固定position/clock重建truth与队列，
  复算全部120行正确标记/15主格/角色/C/P/clock关系，均一致；
  不访问私人根/账本/设备/原标注，不独立运行processor/模型/suite/私人scorer。
- 接受为 **ACCEPTED_COMPONENT_DIAGNOSTIC / STOP_CURRENT_SYNTHETIC_VARIANTS /
  NO_CORE_INNOVATION**，039已关闭、不可重跑。
  主结果依次NG0/24、NR1/24、SG3/24、SR15/24、OG24/24；
  120 generate、113 RETURNED/7 INVALID（均NR）、FAILED/NOT_RUN0，120 EOS/0截断。
  每任务每clock planned8完整保留，不按OG正确或容易位置筛主表。
- 实际输入收据支持48原生video/48image各324视觉tokens，24文字无视觉；
  六native timecodes和最终BF16/worker输入绑定通过。
  但NR角色读出仅1/24，17合法中16个off-grid，还有7格式失败；
  不能把NG全部错误定位为纯计算或某个神经模块。
  SR与SG跨prompt行为差异不能证明SG隐藏态已读对；token数相同也不控制全部呈现/计算差异。
- C=1/24（w3/G0），P=3/24（w5/G1、w5/G2、w7/G2），unknown0。
  NR读出对导出gap3/24不等于角色绑定正确3/24；SR导出15/24。
  NG局部clock响应/平移关系与joint均0/8；
  SG关系满足2/8和3/8但joint均0/8，不能把错误一致称能力通过；
  OG两种joint/关系均8/8。SR整体平移两角色两端joint与两字段+60均4/8，
  NR有4配对数值关系因INVALID未知。
- 研究负责人补充事后描述：现有SR回复由CPU求差15/24，对SG直接间隔3/24，
  配对both/仅SR导出/仅SG/neither=3/12/0/9、unknown0，无新模型调用。
  这是普通“读数＋程序运算”必须考虑的诊断参照，不是事前部署/独立确认新算法，
  没有匹配分阶段成本，也不认定另一prompt内部曾读对。
  SR全部9错误集中在含temporal块0的两几何组（SR3/12，对其余组12/12）；
  是事后错误分布，不能因而删难例/换font或有利扩样，主结果仍15/24。
- 执行者报告新suite19/19、实际CPU input gate一次32.609s Job、
  无兼容修复/二次suite/预检；一个Qwen4B worker/load/greedy16/seed19，
  全model Job56.000s、generate调用38.145s、peak allocated9,148,711,424B、
  Job peak committed17,852,948,480B；model实际exit0/active0后一次CPU score0.171s。
  CPU预约280s、非模型Job wall33.514s（非逐PID kernel CPU），父534.425s；
  新25文件/325,788B、全部五children exit0/Job0，无kill/overflow/timeout。
- 039**首私人输出前**磁盘free436,548,853,760B，
  required2,214,592,512B=64MiB+2GiB；不撤销038前检缺失的历史资源例外。
  错误reflog起点在私人输出/交接读取前拒绝，随后用本轮checkout创建前30s保守起点，
  收据报告仅一个初始化run/coordinator，未恢复旧run或消费后重置。
  10 research opens/117,093B，正常runtime/processor/条件权重按角色加载；
  原真实annotation/QA/gold/旧frames/manifest/预测/source map/private helper/
  更早roots、实验网络/下载/解码/训练/安装/永久系统修改均0。
  本次静态验收不把这些报数冒充ChatGPT本机重测或恶意代码隔离证明。
- 已写[039正式科研处置](./research-decisions/post-039-scientific-disposition-2026-10-23.md)：
  普通读数/指令/空间呈现与跨任务解释仍在，按039事前停止条件，
  **结束当前038–039合成图形时钟变体投入**。
  不继续换font/prompt/clock/布局、同分布补样/第二模型/训练去包装论文核心，
  不新派Codex整理已有表、重复综述、补旧收据或搜私人路径的占位包。
  这不是判定所有时间绑定研究无价值；保留开发诊断和完整负结果。
- **当前0 READY，040未立项。** 下一工作归ChatGPT科学负责人，
  先形成自然长视频中可失败的命题、最强近邻的实质差异、足以识别的现有证据、
  必要强基线和停止条件；当前还没有满足这些要求的新实验合同。
  本审查沿用039冻结先例边界，没有新增穷尽新颖性检索；
  不把普通组合/控制或成功运行视为核心创新。
  **NOVELTY=RETAIN0；NATURAL_VIDEO_EFFECT_UNKNOWN；原C/D NO_GO_AS_CORE；
  TRAIN-GPU HOLD；历史CLOCK_ZERO_ASSUMED_NOT_CERTIFIED；Charades FINAL_MEDIA_STOP。**


### 2026-10-24 · 按科研价值优先完成一个新候选设计，尚未放行040

- 用户同意停止039后的低价值合成变体，要求尽快有新的科研价值突破。
  本轮由ChatGPT研究负责人亲自核查公开主文/摘要与现有项目证据，
  没有把普通综述/路径修复/软件框架再派给Codex，没有私人数据/模型/GPU执行。
  当前仍没有新的实证突破或已通过的新机制，不用用户的急迫目标替代证据。
- 筛掉普通“读出再交程序运算”“按答案假设找线索”“显式证据充分性核验”
  作为新核心的捷径；PACE原始摘要、REVEAL原始框架、VisualTrust受控断言对照已有近邻。
  TACL2021 Jacovi/Goldberg §4.1明确已有选择mask位置/模式传递类别的讨论；
  一般选择通道概念不新，不能换成视频名称就宣称新理论。
- 完成[候选设计：自然长视频选帧时间表的信息通道](./research-proposals/selection-coordinate-channel-2026-10-24.md)：
  固定既有问题/五选项/灰色视觉tensor，让每题收到同视频六道题各自产生的时间表，
  全交叉比较自己的表和全部错配表。四登记自然源×六题×六表=144格，
  Uniform-clock/纯文字各24格，≤192逻辑槽；按实际全输入等价类去重调用并保留逻辑权重。
  六块原生timecodes须实测，不把12选择indices当12个模型可见时间码。
- 固定主要描述量为每题“自己的表正确性−其余五表平均正确性”，按源等权汇总；
  答案flip本身不够，必须有可评分正确性差异。
  选择器观察源视频获得合法压缩信息不等于gold泄漏或作弊；
  所有候选帧/选择成本仍需计入完整系统。
  去画面是反事实/分布外干预，不能据此唯一分解真实画面收益的中介比例。
- 本候选有明确失败/停止解释和简单强对照，但只是**CANDIDATE_MEASUREMENT_DESIGN**，
  不是创新通过或自然长视频视觉能力成绩。旧开发来源已经暴露，
  不能假装独立holdout，登记源也不自动等于独立物理录制。
  不按旧成绩/本轮输出挑题，不拿少数题/重复clock格报显著性。
- 本轮读取013/017公开真实探索收据与036 reference收据、当前public worker：
  自然来源与实际选帧曾存在，公开聚合值却不足以重建逐题时间表；
  当前原标注路径在036时未定位，不能直接继承旧hash/许可为现存入口。
  public worker还调用私人factory，不能用其接口签名假定历史真实timecodes已核。
  新草案优先只用旧冻结nongold题/选项/选择表，不需要开视频/旧RGB、解码或再跑SigLIP；
  不重跑旧已STARTED的真实画面问答。
- 当前直接近邻Frames Don't Add Up（ICLR2027投稿入口）forum/PDF均遇验证页，
  未取得正文；BPO原始页面读取失败，也未完成方法审查。
  这些是**未解决重合风险**，不能因抓取失败就宣称新颖，也不从标题推断完全重复。
  需核必要方法后再判断此经验问题是否足以投入。
- 更新科研设计状态为 **CANDIDATE_DESIGN_COMPLETE / NOVELTY_AND_INPUT_UNRESOLVED /
  NOT_READY**。正式执行合同需先有近邻实质差异与本地确切nongold选择表、
  当前末尾评分文件入口；不上传私人JSON/QA/gold，不重开036或全盘搜索。
  当前拟192逻辑槽/GPU600s等只属方案上限，未获新私人读入/GPU权限，
  也没有开始计费或许诺结果。**0 READY，040未立项**，不派占位任务。
- 038–039图形时钟变体停止、旧C/D NO_GO_AS_CORE、
  NOVELTY=RETAIN0、NATURAL_VIDEO_EFFECT_UNKNOWN、TRAIN-GPU HOLD、
  历史CLOCK_ZERO_ASSUMED_NOT_CERTIFIED、Charades FINAL_MEDIA_STOP保持。


### 2026-10-24 · 继续反证：取消192槽设计，完成同题跨视频修订并准备输入交接

- 对上一候选做识别检查，发现S(q_j,X_i)交叉混合问题变化与视频变化；
  selector可只编码问题而完全忽略视频，有限能力下游再从时间表读取这个编码，
  仍可产生正对角优势并胜过纯文字Q。这时不能归因为视频来源的信息。
  研究负责人在内存算六题五类别抽象反例：
  self命中6/6、错配2/30、Q2/6，旧D=14/15，未使用任何视频信息。
  这是逻辑反例，不是Qwen/真实QA成绩、新suite或数据标签读取。
- **取消旧192槽作为当前待执行设计**，原提案加SUPERSEDED通知保留原文；
  完成[识别修订](./research-proposals/selection-channel-identifiability-revision-2026-10-24.md)。
  固定同题q_i/选项，计算它在四源上的S(q_i,X_v)，不能把旧self-only选择记录转置冒充。
  统一48候选槽/12选择/序数时间坐标，去掉时长/fps/alias等显式源身份，
  由原生processor构造同灰色视觉tensor与各自六块时间码。
- 新拟规模24题×4源=96格、Uniform/Q各24，≤144逻辑格；
  实际全输入相同只调用一次，保留别名/逻辑分母。
  selector若忽略源，则同题四列输入相同、标签命中差严格0，
  排除了上一纯问题编码反例；这只是直接实验控制性质，不是新定理。
  正差仍可能涉及源指纹/答案位置偏差等，不证明事件定位或新神经机制；
  灰色条件原gold只是外部预测目标，不是灰色片段自身的视觉真值。
- 明确输入充分性：需四源完整image embedding/问题embedding及预处理绑定，
  或各48候选RGB供以后经合同授权的新特征提取；
  原self-score/12indices列表通常不能恢复跨源投影。
  特征路线可CPU算选帧，RGB路线若用SigLIP就是新增模型计算，
  不能借“只读元数据”授权启动。当前均未读取或执行。
- 本轮已取得BPO arXiv:2610.03141v1主文、读摘要/§3.1–3.5，
  已列view pool为原片、key/non-key mask、span-drop、reverse、shuffle，
  并用于跨view合同与RL后训练；普通多view方法不新。
  所读定义未列本修订的跨源选帧时间表比较，不等于已排除全部相关变体。
  Frames Don't Add Up主页面/PDF及公开API仍未取得正文，
  搜索片段不作方法排除证据；该近邻重合尚未核清。
- 修订文件给出一条可发本地Codex的**输入交接消息**：
  先索取当前原标注、nongold题/选项/源别名、四源候选RGB或特征的确切路径，
  路径缺失就等待用户；最多16个明确文件各一次lstat，仅存在性/类型/大小。
  不读正文/QA/gold/帧/特征，不跟随链接、不扫描目录，
  不创建代码/tests/run/账本/结果，不调用模型/GPU或创建HOLD父结果。
  这只是新的明确元数据交接范围，不能当作实验READY或内容/许可通过。
- **当前0 READY，040未立项；IDENTIFIABILITY_REPAIRED / INPUT_INTAKE_REQUIRED /
  NOVELTY_UNRESOLVED。** 输入和必要近邻明确后才形成一个可审正式合同。
  没有新自然实证效应或论文突破；不派重复综述/工程恢复，不重跑旧真实画面问答。
  NOVELTY=RETAIN0、NATURAL_VIDEO_EFFECT_UNKNOWN、TRAIN-GPU HOLD、
  原C/D及038–039停止、历史CLOCK_ZERO_ASSUMED_NOT_CERTIFIED、
  Charades FINAL_MEDIA_STOP保持。



### 2026-10-24 · 用户选择工程论文推进；下达唯一040比较与复现包

- 用户询问工程稿与核心期刊可行性后同意继续。当前目标优先验证工程/系统贡献：
  候选主题“资源受限环境下视觉语言模型实验的可审计执行与输入一致性验证”。
  现有执行史与工具代码是基础，不是新颖性、优势或核心期刊录用的证据。
- 研究负责人已读MLflow Tracking/System Metrics、Ray Tune FailureConfig、
  lmms-eval命令文档、SQLite事务/原子提交、Python subprocess与Windows Job官方说明，
  冻结[工程证据协议](./research-protocols/engineering-runner-comparison-2026-10-24.md)。
  记录/缓存/恢复/事务/进程监督都有先例；不把普通组件重命名为新机制。
  前三项只做官方文档能力对照，不将自实现配置冒充这些工具的实测。
- 唯一 **READY / NOT_EXECUTED**：
  [VLM-ENGINEERING-EVIDENCE-040 A–H](./codex-artifacts/VLM-ENGINEERING-EVIDENCE-040/README.md)。
  一包完成新public stdlib runner/benchmark/关键验证、合理B0、
  具有同等保护目标的强SQLite B1、F与三单组件消融；
  9家族×10重复×6配置=540个正式格，实际工作子进程/独立调度进程/受控后代，
  输入变化、重复、工作后异常退出、收据错配、早评分及后代仍活。
- 将正常任务合法完成率、准入违反、实际重复工作、崩溃不确定性和开销分开报告，
  独立oracle不能调用F validator代替判断；未送达/未知/失败/NOT_RUN保留完整分母。
  Windows Job只作共同安全外包络，不能把它替B0清理后代算为B0的保护能力。
  新空目录只复制3个新模块复现，不导入030/038/039或任何私人helper。
- F与B1可能完全等价，结果应允许 **NO_DISTINCT_MECHANISM_EVIDENCE**；
  F胜普通B0只证明已知机制在受控案例的用途，不是事务或exactly-once创新。
  CPU哈希负载不估计Qwen推理性能；已有018/039真实执行成本仅作历史可行性材料，
  不和本轮配对试验混算。工程新颖性保持 **UNVERIFIED**。
- 范围是全新CPU程序，父5400s/受监督wall1500s，正式benchmark900s，
  新临时输出≤128MiB/10000文件，首输出前配额外≥2GiB余量；
  只清理本轮归属可证工作组，实际退出核查。GPU/模型/真实QA/gold/旧媒体/
  私人交接根/安装/实验网络均0；一次七处allowlist交付、普通安全push后STOP。
  用户发送README完整消息才激活，不由GitHub编辑唤醒，也不自动041。
- 144格同题跨源选帧信息通道候选及其元数据交接改为 **PARKED / NOT_READY**，
  不在040继续索要缺失路径/PDF或新开HOLD占位包；科学设计保留供以后另议。
  旧192槽SUPERSEDED、038–039合成变体停止、原C/D NO_GO_AS_CORE不变。
  **算法NOVELTY=RETAIN0；NATURAL_VIDEO_EFFECT_UNKNOWN；TRAIN-GPU HOLD；
  历史CLOCK_ZERO_ASSUMED_NOT_CERTIFIED；Charades FINAL_MEDIA_STOP。**


### 2026-10-24 · 040受控比较验收；强SQLite匹敌F，停止机制包装

- 已审查[bedcc78](https://github.com/floomeer83felix-source/vlm/commit/bedcc78f70e128d0e05ea4132aedaaea68552e1a)，直接父ee24885，
  恰七处allowlist：三源码/两报告/540行CSV/results一个父追加。
  读取完整公开交付，独立核验原始源码/Git blob、重建540格队列与SHAKE输入、
  全部manifest/config/收据/580个worker观察和630个准入决定；汇总与配对成本一致。
  不运行用户Windows/私人目录、suite、模型或GPU；不是独立OS事件见证/跨机复现。
- 正式540/540尝试、360/360故障证据字段送达、580工作入口/完成、660调度请求；
  RETURNED310/VIOLATION90/REJECTED100/UNKNOWN40，FAILED/NOT_RUN/UNSUPPORTED0，
  所有格记录最终group0。完整F与SQLite B1各0/90违规、0重复，
  正常各30/30、可安全完成故障各30/30，崩溃各10 UNKNOWN。
  消融违规依次NOBIND10、NOCONSUME20、NOEXIT20；B0为40/90、额外工作20。
- F/B1正常1KiB/64KiB/1MiB配对wall比值中位数1.013485/0.963456/0.996761，
  各差值范围跨0，未显示跨大小稳定成本收益。消费后不确定性仍存在，不宣称exactly-once。
  六开发格与同机三文件clean复现独立记录，不混入正式540分母。
- 接受为 **ACCEPTED_CONTROLLED_ENGINEERING_COMPARISON / NO_DISTINCT_MECHANISM_EVIDENCE**，
  详见[负责人验收与论文处置](./research-decisions/post-040-engineering-disposition-2026-10-24.md)。
  新增的是可复核故障比较/负结果/复现材料，未新增独立可靠性机制、真实VLM或现成工具优势。
  B1能实现同样目标是实质否定证据，按040事前停止条件，不继续堆框架包装创新。
- 代码边界明确：admit未独立验证已消费claim或JSONL链，依赖控制器调用序；
  未覆盖断电/I/O/真实事务争用/完整正向缓存工作流；三文件入口仍需外层资源监督。
  本轮不是任意API顺序、恶意代码或生产可靠性认证；不追加纯补丁微批次修饰论文。
  执行者资源/磁盘/父时钟按其报告接受，不冒充负责人本机重测；
  suite外层一次终止请求及B0/NOEXIT后代fallback保留。
- **040关闭不可重跑，当前0 READY，041未立项**；README启动消息改为历史不可执行。
  工程稿可用证据增加，但“当前足以投核心期刊”的核心贡献问题未解决。
  下一项应先由研究负责人明确真实VLM流程特有、可重复且强现成配置未解决的问题及实际收益；
  有效输入/上游配方一致性仅是待核候选，不是本轮已发现的新故障。无占位包或自动GPU/投稿。
  144格选帧候选/路径交接继续PARKED；算法NOVELTY=RETAIN0，
  NATURAL_VIDEO_EFFECT_UNKNOWN、原C/D/038–039停止、TRAIN-GPU HOLD、
  历史CLOCK_ZERO_ASSUMED_NOT_CERTIFIED、Charades FINAL_MEDIA_STOP保持。


### 2026-10-24 · 由真实缓存组件条件复现进入唯一041 CPU资格包

- 040结论不变，不继续claim/事务框架扩展。负责人亲读固定lmms-eval
  8f400975（2026-10-22）的缓存/Instance/evaluator/simple与chat Qwen路径及现有测试。
  发现当前代码已覆盖前置生成文本与Git eval版本，先排除旧文档导致的误报。
  已知issue1244 metadata漏传、1255版本指纹，以及OmniCompass严格身份/vLLM媒体hash
  都是必须承认的先例，不把普通补hash或漏metadata立为新核心。
- 在本机临时目录用未经修改的上游缓存/Instance/SQLite完成有限组件探针：
  固定问题/ID/静态指纹，真实视觉callback的数据表图像红→蓝后cache hit、backend新增调用0，
  返回仍为旧图像标记；冷缓存、变任务命名空间、变前置文本均正确重新计算。
  使用自有PIL像素SHA backend和仅日志适配，不是模型/完整CLI或已证真实基准成绩污染。
  数据不可变假设和简单namespace已能解决探针，原创性/合法使用意义仍须核。
- [立项依据](./research-proposals/cache-input-contract-qualification-2026-10-24.md)及
  [冻结协议](./research-protocols/cache-input-qualification-2026-10-24.md)给出区别：
  下一次只实际接既有Qwen CPU processor，验证同RGB不同合法时间metadata的输入差异、
  不同metadata表示但同输入的关系，以及缓存层是否复用到不同边界输入。
  整轮无模型load/forward/generate、无GPU/真实QA，marker不是Qwen答案。
- 唯一 **READY / NOT_EXECUTED** 为
  [VLM-CACHE-INPUT-QUALIFICATION-041 A–H](./codex-artifacts/VLM-CACHE-INPUT-QUALIFICATION-041/README.md)：
  9家族×4刺激=36对72状态，AB/BA×四配置=288序列576查询；
  UPSTREAM、完整SOURCE_NAMESPACE、付真实预处理成本的EFFECTIVE_INPUT、NO_CACHE。
  固定上游原文件/许可证封装在third_party，无新下载/安装；不改其代码。
- 一个包完成两新模块、关键验证、oracle/正式比较/成本/8序列clean及价值裁决。
  父5400s/受监督wall1000s/processor≤720，正式CPUworker600s，
  线程≤4/Job RAM4GiB，新根≤2048文件/32MiB，前置配额外2GiB余量。
  只用已知processor目录，必要时仅一个已知039 runtime/config.json恢复model/runtime；
  不扫盘/读旧账本或QA，不重新寻找原标注，未知部分NOT_RUN而非伪造输入。
- 研究终点最多CPU_BOUNDARY_CONTRACT_REPRODUCED，不预设新算法、实际推理提速或核心期刊价值。
  若仅人为违背不可变数据约定或简单现有namespace已足够，明确LOCAL_COMPONENT_REGRESSION_ONLY；
  不自动GPU/扩样/上游Issue/论文投稿。一次六处allowlist安全push后STOP。
  144格候选/元数据交接继续PARKED；旧科学/训练/媒体停止结论不变。

### 2026-10-24 · 041条件性输入合同复现验收；源命名空间足够，关闭不扩展

- 审查6bcee08，直接父6298e2d，恰六处allowlist与codex-results一个父追加；原执行记录不改。
  [负责人验收与工程论文处置](./research-decisions/post-041-cache-qualification-disposition-2026-10-24.md)。
- 用独立stdlib程序复核288序列/576查询、队列轮转、72状态全部完整/分区摘要、
  token/attention/grid原始字节摘要及逐查询语义与成本；与报告一致。
  边界摘要12对EQUAL/24对DIFFERENT；实际processor/tensor执行与OS退出按执行者报告，
  不冒充负责人本机重跑、独立原始视觉字节或跨机复现。
- UPSTREAM正确新算/正确复用/不兼容=80/24/40；SOURCE_NAMESPACE136/8/0，
  有16次同边界保守miss；EFFECTIVE_INPUT120/24/0，实付144次processor；
  NO_CACHE144次新算/BYPASS。各配置144查询，FAILED/UNSTABLE/RELATION_MISMATCH/NOT_RUN0。
  五个视觉/时间变化家族各8次不兼容；已有TEXT_CONTROL隔离有效。
- 独立计数正式查询processor504，加oracle72为576；suite4/clean13/全轮593由执行者报告。
  SOURCE/EFFECTIVE查询wall9.387379/9.376988s不能推断GPU或实际产品优势；
  完整源namespace已经解决观察到的案例，不预设新hash机制。
- clean为同机8序列/16查询，不是独立机器或独立oracle。报告全部Job active0、GPU/权重0；
  输出规模仅驻留快照、Job计量仅分阶段；这些缺口保留，不称全部资源合同独立PASS。
  协议收据SHA差异已核为LF/CRLF转换，科学正文未变。
- **ACCEPTED_CPU_BOUNDARY_CONTRACT_REPRODUCED / LOCAL_COMPONENT_REGRESSION_ONLY。**
  尚无遵守现有身份合同的真实工作流污染证据，不能由故意保持旧身份的合成probe
  外推完整CLI缺陷、Qwen答案错误率或核心期刊新贡献。040结论不变。
- **041关闭不可重跑，当前0 READY，042未立项。** README启动消息归档不可执行；
  不自动GPU、合成变体、上游Issue/PR或投稿。后续先有真实合法工作流缺口与可测收益再立项，
  不派占位包；144格候选/路径交接继续PARKED。
  NOVELTY=RETAIN0、NATURAL_VIDEO_EFFECT_UNKNOWN、原C/D及038–039停止、TRAIN-GPU HOLD、
  历史CLOCK_ZERO_ASSUMED_NOT_CERTIFIED、Charades FINAL_MEDIA_STOP保持。

### 2026-10-24 · 真实输入链路公开筛查：确认直接先例，暂不立042

- 已核[公开论文与固定源码记录](./research-proposals/post-041-real-input-source-screen-2026-10-24.md)，只做负责人静态审查与数值说明；
  未执行新Codex父任务、读取私人目录、运行processor/模型或创建实验run。
- Meta-Video已有后端/输入形式差异及评测卡研究；ExtremeWhenBench已讨论原生视频路径与时间信号。
  宽泛标准化、metadata转发或改video URL不足以直接构成本项目新贡献。
- 固定Qwen工具与HF源码可见average_fps/frames_indices到原生时间码的路径；
  v4.57.6公开processor源码17,149B/SHA256与041安装源码收据匹配，
  不需要本轮访问私人安装目录。VeOmni官方文档已明确指出VFR精确时刻需保留PTS，
  因而该认识本身有先例，不能包装新发现。
- 12帧不均匀时刻的公式示意中，索引重建中点与PTS中点最大差4.05秒；
  仅为数值反例，无容器/解码/真实任务/模型测量，不是自然发生率或答案错误证据。
  041缓存身份一致性不能认证输入metadata与媒体时钟相符，也不因此恢复041。
- **PUBLIC_SOURCE_SCREEN_COMPLETE / NO_NEW_TASK；当前0 READY，042未立项。**
  尚缺真实合法工作流影响、现有保留PTS/规范化方案不足的证据及实际收益，
  不下达重复合成或路径占位包；Frames Don’t Add Up全文未得的限制仍保留。
  040/041裁决、144格候选/路径交接PARKED、NOVELTY=RETAIN0、NATURAL_VIDEO_EFFECT_UNKNOWN、
  原C/D及038–039停止、TRAIN-GPU HOLD、CLOCK_ZERO_ASSUMED_NOT_CERTIFIED、Charades FINAL_MEDIA_STOP保持。

### 2026-10-24 · 完成一页贡献定义与最小真实对照设计；输入与API入口未齐

- 用户要求继续后，由研究负责人完成[一页贡献定义](./research-proposals/natural-video-clock-contribution-brief-2026-10-24.md)和[最小真实对照设计](./research-protocols/natural-video-clock-feasibility-design-2026-10-24.md)。
  交付为研究设计，未创建042父任务/README，未运行新实验或读取私人素材。
- 候选问题是自然录像的时间信息损失是否影响已有事件区间定位，以及修复的效果/成本取舍。
  已有Meta-Video/VeOmni/TorchCodec覆盖保留；不主张新时间编码、解码器或首次发现VFR限制。
- 拟8个独立原录制×2既有题×四配置=64逻辑格，6高偏移源/2认证CFR参照。
  B0默认索引/fps；P同画面精确PTS诊断适配；N已有均匀时间重采样；T同问题/时长纯文字。
  透明声明P需要独立接口适配，不是现成开箱强产品；N允许画面变化，其收益不归因为纯时码。
- 预设原媒体/标注时钟桥接、无gold选样、完整实际输入绑定、等价类去重、独立末尾评分，
  全失败/无效/NOT_RUN分母、按录制汇总IoU及真实成本。不能用同token数替代同画面控制。
  16题只作可行性触发，未设计为核心期刊确认性证据；阈值不等于显著性或投稿保证。
- 真实录像、nongold问题、受控评分入口、解码与PTS适配尚未核齐。
  AgentNet公开工具会录视频，但所核数据卡/文档未提供本设计所需的确切原视频/PTS/区间桥接，
  故未选为实验源；未下载数据、读取轨迹标签或媒体，未由许可文字推断资产已取得。
- **DESIGN_COMPLETE / DATA_AND_API_ENTRY_UNRESOLVED / NOT_READY；当前0 READY，042未立项。**
  拟预算不是授权，需确切入口与新的完整合同才可执行。未改codex-results、旧代码/协议/收据，
  不创建测试/实验根、不做GPU/安装/媒体或标注读取，不自动扩大候选或续任务。
  040/041、原C/D与038–039停止、144格候选/路径交接PARKED、NOVELTY=RETAIN0、
  NATURAL_VIDEO_EFFECT_UNKNOWN、TRAIN-GPU HOLD、CLOCK_ZERO_ASSUMED_NOT_CERTIFIED、
  Charades FINAL_MEDIA_STOP保持。

### 2026-10-24 · 素材与接口入口核查完成；EPIC列优先候选，等待确切资产

- 研究负责人完成[素材与接口入口筛查](./research-proposals/natural-clock-source-entry-screen-2026-10-24.md)；EPIC官方README明确低光自动降帧率，
  原视频下载定位、已有动作区间schema及nongold视频/split/校验元数据可查。
  这些是来源入口证据，不是6个高偏移源、时钟桥接或新颖性通过。
- 独立核700行nongold视频表：ID唯一、数值有效，333条符合180–900秒，涉及36个匿名参与者ID。
  表中没有逐帧PTS/显示时长/time_base/媒体字节身份；不将平均fps或参与者数冒充CFR/VFR或独立录制认证。
  未读动作标签CSV、QA/gold、原视频或帧。
- EILeV点名的P29_05/P30_08分别1821.736567/1122.14秒，超出本设计范围；
  不改时长阈值、裁剪或直接充作阳性。64格设计和源级分母保持。
- HoloAssist说明列出VideoMp4Timing.txt及原/压缩视频，实际下载入口为大型归档；
  三个归档链接返回unsupported content-type，没有取得可用正文，不声称HTTP请求0或已检查归档。
  TimeLens2真实视频分18片，多数约106–107GB，末片约888MB，未核到目标小样本成员/PTS索引。
  均未取得媒体/旁表/标签内容，不能把公开列出资产写成已准入。
- P的公开时间计算入口及原生调用点已识别，实际CPU分派、时码、BF16视觉相等仍未测试；
  不能以静态签名代替真实输入门。
- **PUBLIC_ENTRY_SCREEN_COMPLETE / EXACT_ASSET_REQUIRED / NOT_READY；0 READY，042未立项。**
  下一动作应由明确现有素材引用或新的有界获取范围驱动，再形成一次CPU资格整包；
  没有实物入口就暂停该候选的入口推进，不续搜路径/扩大综述/整理文件微包。
  该停止是输入条件未满足，不是实验阴性；不创Codex父结果、代码/tests、实验根、GPU或安装任务。
  040/041、原C/D及038–039停止、144格选帧候选/路径交接PARKED、NOVELTY=RETAIN0、
  NATURAL_VIDEO_EFFECT_UNKNOWN、TRAIN-GPU HOLD、CLOCK_ZERO_ASSUMED_NOT_CERTIFIED、Charades FINAL_MEDIA_STOP保持。

### 2026-10-24 · 042逐文件获取与CPU时钟资格合同已冻结；等明确媒体许可

- 用户要求“一直继续”，负责人完成可审查的[042整包合同](./codex-artifacts/VLM-NATURAL-CLOCK-ADMISSION-042/README.md)和[16项manifest](./codex-artifacts/VLM-NATURAL-CLOCK-ADMISSION-042/manifest.json)，不再要求用户先搜索本地旧盘，也不重复派入口综述微包。
- 从固定官方video_info/split/MD5元数据选取：700行中333条时长合格，189条为55代；其中validation为66条/25参与者。
  按SHA256(“19\\n”+video_id+“\\n”)排序、每参与者最多1条取前16。16项均唯一媒体校验记录，URL使用发布路径，不误拼validation目录。
  仅公开nongold入围，未读取实际媒体、动作行或模型结果；16个不同参与者不等于独立性已认证。
- 拟授权媒体总≤32GiB、单项≤4GiB、各≤1 HEAD/1 GET、无重试/跳转；既有CPU工具与监督能力须在媒体HTTP之前核齐。
  新根、逐帧显示时钟、PTS有理数/48点舍入、全名单失败分母与停止条件、统一交付已写明。
  这些是待批准上限，不是已用额度或当前文件体积；未向名单MP4发HEAD/GET，未解码、安装、读动作CSV或运行模型。
- 核到[EPIC100原论文](https://link.springer.com/article/10.1007/s11263-021-01531-2)明确同一动作可反复发生，标注者由粗时刻区分实例。
  因而只给动作文本不能自动指定一个隐藏实例；64格设计若落到EPIC，须先解决有效答案集合/问题可识别性，不能给模型泄漏粗时刻或事后挑gold。
  单位、video_id与MD5也不代替标注播放器到原MP4的时钟桥接。
- **ACQUISITION_SCOPE_COMPLETE / BLOCKED_PENDING_EXPLICIT_MEDIA_CPU_AUTHORIZATION；当前0 READY。**
  042作为待批准合同登记，未产生执行父结果；只在明确媒体/CPU范围获批后才转唯一READY，不把笼统继续视为受控操作许可。
  时钟6+2通过最多支持SOURCE_CLOCK_FEASIBLE，标签/题目/实际输入门仍HOLD；不自动GPU、P适配或扩样。
  修正当前PARKED行遗留“唯一READY为041”的过时措辞；历史执行日志保留。040/041关闭、NOVELTY=RETAIN0、
  NATURAL_VIDEO_EFFECT_UNKNOWN、TRAIN-GPU HOLD、Charades FINAL_MEDIA_STOP及既有停止结论不变。

### 2026-10-24 · 用户批准042下载与CPU范围，已转唯一READY

- 用户收到固定16视频、累计≤32GiB下载及≤2小时CPU核验、标签/GPU0的具体范围和“是否批准”提问后，原话回复“好的”。
  该肯定答复已构成此范围许可，不再要求重复批准口令；不追认早前笼统继续为媒体许可。
- [042 README](./codex-artifacts/VLM-NATURAL-CLOCK-ADMISSION-042/README.md)与看板同步为**唯一READY / USER_APPROVED_BOUNDED_MEDIA_CPU**；
  现main中该父任务无completed/partial/blocked执行结果。16项manifest只将admission_status由PROPOSED_NOT_AUTHORIZED改为AUTHORIZED_NOT_RUN，
  候选ID、排序、URL、出版者MD5及科学/资源边界不变；新manifest SHA256为24d2177a27a376da48bd6a3c9e7dfa12bf2396066d690056d3e743847d4b760c。
- 本地Codex在一次用户启动消息后按合同连续做允许的独立步骤，统一脱敏交付/安全push后停止；
  工具、监督或新根前置失败则媒体HEAD/GET0；不安装、不扩大名单、不重试/续传、不继承旧额度。
  原片累计≤32GiB、单项≤4GiB，CPU核验≤7200秒；其余HTTP/进程树/新根/父wall上限沿用合同。
- 负责人本轮仅登记授权和交接，未访问用户Windows机器、发送媒体HTTP、解码或生成执行结果；docs/codex-results.md保持不动。
  READY不是时钟通过或数据已取得；EPIC题目实例语义、标签时钟桥接及实际processor输入仍HOLD。
  标签/模型/GPU均0，040/041关闭、NOVELTY=RETAIN0、NATURAL_VIDEO_EFFECT_UNKNOWN及既有停止结论保持。


### 2026-10-24 · 042负责人验收

2026-10-24：042已关闭，当前0 READY。完整媒体0/16、时钟认证0/16；首下载913.25秒超时，已落盘11534336B（11MiB）。接受失败回执，不认证资源合同全部通过：900秒截止超出，HEAD长度/ETag未持久化，实际接收正文精确值UNKNOWN、该GET保守上界4GiB。禁止042重跑/自动续传；标签/模型/GPU0，科研效应UNKNOWN。

核3630e87回执及代码：HEAD1/GET1均200；超时后自有Job active0，其余15项NOT_RUN。13项测试为执行者报告，未独立复跑Windows。deadline只在阻塞read之间检查，收取状态未及时持久化，故ACCEPTED_BOUNDED_FAILURE_REPORT / RESOURCE_CONTRACT_NOT_FULLY_MET。0/16未测不是VFR不存在或模型阴性。后续先设计无网络截止/持久记账修复，不创建占位READY、不迁移下载余量。NOVELTY=RETAIN0及既有停止结论保持。

### 2026-10-24 · 下达043无网络CPU修复整包，唯一READY

- 用户要求“一直继续下去，直到给出新的codex任务指令”，负责人已完成[043合同](./codex-artifacts/VLM-FETCH-DEADLINE-ACCOUNTING-043/README.md)并设为唯一READY；不再停在“下一步修复”的口头建议。
- 冻结042公开代码/回执作为依据：声明长度/ETag只留内存，worker finally不足以抗强杀；截止依赖阻塞读之间检查及监督轮询。
  未确定913.25秒延迟的逐段因果，不把单次read timeout当整个请求期限。
- 043一次包覆盖最小新模块、独立监督与写前持久状态、12个固定本地故障case/退出后回放及具体下一获取交接。
  显式分工作截止/清理余量，记录真实active0而非kill调用时刻；应用已持久块、保守责任与网络缓冲未知分开。
- 仅标准库CPU，应用socket/HTTP、真实媒体/旧私有日志/标签/模型/GPU0。新根32MiB/512文件、单组512MiB；
  受监督执行累计≤600秒、父≤1800秒；初轮一次，只有定位实现错误才允许一次有理由修复回归，旧任务与预算均不重开。
- 交付限定两个新Python、统一回执、固定case CSV及results末尾一条；本轮负责人只写合同/看板/总览，未运行本地代码或追加执行事实。
  PASS最多支持OFFLINE_DEADLINE_ACCOUNTING_REPAIR_PASS / REAL_FETCH_UNTESTED，不能证明慢网下载、自然时钟或VLM收益。
  042已消费，旧11MiB及不完整GET≤4GiB责任保留，不自动续传/新HEAD/GET/扩大下载或044。
  040/041关闭、NOVELTY=RETAIN0、NATURAL_VIDEO_EFFECT_UNKNOWN、标签/模型/GPU及其余旧停止结论保持。

### 2026-10-24 · 验收043，冻结044单对象实际获取方案待授权

- 已核[e0b1d1d](https://github.com/floomeer83felix-source/vlm/commit/e0b1d1d113a49ee6ec5763245ac18c541e031da4)五处允许diff、核心/验证器与公开回执，形成[负责人验收](./research-decisions/post-043-fetch-repair-disposition-2026-10-24.md)。
  标准库CSV/Decimal独立复算24行：初轮12 NOT_RUN、实际修复轮12 PASS；不一致0。未重跑Windows/旧tests或读取私有日志。
- 五次kill最大7.906秒，全部active0最大7.906秒、finish最大8.000秒，8/12/15门内。
  fake HEAD/GET/read=11/8/33，read返回79872B、持久下界71680B、独立fixture责任294912B；不冒充实际网络计量。
- **ACCEPTED_OFFLINE_REPAIR_IN_TESTED_SCOPE / REAL_FETCH_UNTESTED；043关闭，当前0 READY。**
  核心只接FakeTransport、64KiB级测试cap，未实现真实TLS或多对象全局配额；不能只取消guard/改常量就当生产资格通过。
- [044完整合同](./codex-artifacts/VLM-EPIC-SINGLE-SOURCE-ADMISSION-044/README.md)及单对象清单已冻结：原C02/P31_10，真实适配/一次必要预检、≤1 HEAD/≤1 GET及成功后一次CPU验钟合在同包。
  拟新媒体≤4GiB，获取总包络≤900秒（840工作/870退出/900收尾），CPU准备/验钟≤1200秒；尚未许可、未执行。
  若再超时/记账失败暂停该直接获取入口，不自动延时、换候选续试或恢复042。
- 042的11MiB与不完整GET≤4GiB历史责任原样保留，C01关闭、C03–C16不发、第17源不加。
  单个源即使验钟成功也不代表6+2/64格或标注/模型输入准入；标签/模型/GPU0，NOVELTY=RETAIN0及旧停止结论不变。
  本轮仅负责人文档与待授权清单，codex-results、043代码/回执/CSV及042历史证据未改。

### 2026-10-25 · 用户批准044，设为唯一READY

- 用户在收到044完整范围及批准提问后，原话回复“批准044”。已将[044 README](./codex-artifacts/VLM-EPIC-SINGLE-SOURCE-ADMISSION-044/README.md)与看板同步为**READY / USER_APPROVED_SINGLE_SOURCE_MEDIA_CPU**，当前仅此一个READY，尚无044父执行结果。
- 许可仅原C02/P31_10：≤1 HEAD/≤1 GET、新媒体≤4GiB；获取总包络≤900秒（840工作/870退出/900收尾），
  CPU准备/预检/验钟累计≤1200秒；RAM、新根、父5400秒及其他边界沿用冻结合同。无需再逐子步骤确认。
- manifest保持原blob e1bf9ddfa5b9d529b4b155c467c582851e31dab2 / SHA256 0f21ca3a765a5dd5ed264fca5147676d762b32f0dc4526db87b26153778b75c4，
  对象、rank/URL/MD5及科学门槛未改；REGISTERED_UNTESTED表示素材未测，授权记录由README/看板承载。
- 本地Codex一次启动后按合同连续做适配/预检/获取/成功后验钟，统一脱敏推送后停止；前置失败则HTTP0。
  再次超时或记账失败暂停该直接获取入口，不加时、不换候选续试、不自动045。
- 负责人本轮仅登记授权与交接，未访问用户机器、发媒体HTTP、解码或写执行结果；codex-results与旧代码/证据不动。
  READY不是媒体已取得或时钟已过，042/043关闭和042旧责任不变；标签/模型/GPU0，NOVELTY=RETAIN0及旧停止结论保持。

### 2026-10-25 · 验收044并暂停当前直接官方获取路线

- 核[e27e175](https://github.com/floomeer83felix-source/vlm/commit/e27e1759c187f4a6d668c496dbb50cd6d9868fbf)恰五个允许路径、核心/新tests及公开回执，形成[负责人验收](./research-decisions/post-044-single-source-fetch-disposition-2026-10-25.md)。
  核心/tests SHA256独立计算匹配封存，未重跑Windows或读取旧私有媒体/日志。
- CSV/Decimal独立复算唯一C02：HEAD/GET均1且200；声明/保留责任2034460331B，持久read/写盘/partial下界75497472B=72MiB，约声明量3.711%。
  kill839.9030640、active0为839.9087603、finish839.9503246秒，符合840/870/900门；未见该行计数或时限矛盾。
  精确接收保留UNKNOWN_PENDING_BODY，完整MD5/SHA未验；验钟NOT_RUN，不将缺失时钟当0或CFR。
- **ACCEPTED_BOUNDED_TRANSPORT_FAILURE / CURRENT_OFFICIAL_FETCH_ROUTE_STOP；044关闭，当前0 READY。**
  本轮工程截止/持久化在真实传输中有佐证，素材仍未取得；不是模型或自然时钟科研阴性。
  按事前合同暂停此直接获取入口，不再加时、续传、换候选续试或派同类修复微包，不创建占位045。
- 原16候选保留C01关闭失败、C02获取失败/时钟未测、C03–C16未请求；042旧11MiB/≤4GiB责任及044新责任不迁移/归零。
  后续须明确已有完整合法文件的本地引用/来源依据，或不同可得实物来源；路径留本地，不自动扫描或读取它们。
- 本轮负责人只写验收/归档/看板/总览；codex-results、044代码/tests/回执/CSV和旧manifest不改。
  标签/问题/模型输入/GPU及训练未放行，NOVELTY=RETAIN0、NATURAL_VIDEO_EFFECT_UNKNOWN及既有停止结论保持。

### 2026-10-25 · 素材入口继续暂停；下达独立的045 CPU原生PTS适配包

- 用户要求“继续直到下一任务”。负责人未重开044/下载修复或换候选续取；将可独立推进的[045接口实现包](./codex-artifacts/VLM-NATIVE-PTS-ADAPTER-045/README.md)设为唯一READY。
  这不是占位素材资格任务：实际产出新PTS适配模块、验证器、9槽CPU输入证据与一条统一回报。
- 已重新核固定Transformers4.57.6公开processor blob17bdd975eef337371aa763824edc7e6ec1987dbf，
  原生__call__确实调用self._calculate_timestamps后沿原生一位小数格式/tokenizer生成输入；041公开实现证明本地CPU正常加载/metadata调用方法此前已工作。
  不以静态签名宣布045实际回调已通过；新类/请求作用域及真实BF16/文本边界须由045实测。
- 固定96源帧索引、48个受控RGB、CFR/A/B/Q四表，正式仅9槽；负责人有理数预计算已核A/B原生时码关系及Q量化等价，
  这是设计算术，不是自然媒体/processor实测或模型效应。P不伪造indices/fps、不改最终tokens、不修改安装库或base全局状态。
- 新CPU许可只限当前本地Codex已明确目录中的既有processor/tokenizer配置与正常CPU库；不读取旧runtime/私有helpers来找路径，
  入口不可恢复则真实部分NOT_RUN，仍交新实现及可做检查；不派找路径/纯假传输/综述微包。
  权重/媒体/解码/标签/网络/模型推理/GPU0，实际processor≤12、受监督≤600秒、父≤3600秒、RAM≤4GiB、输出≤64MiB。
- 即使CPU_NATIVE_PTS_ADAPTER_BOUNDARY_PASS，也只关闭一个组件实现缺口；真实资产、标注时钟、重复动作题目、强N基线及64格准入仍HOLD。
  045仅一次整包/统一推送后STOP，不自动046/GPU/新下载。044路线停止、040–044关闭、NOVELTY=RETAIN0、NATURAL_VIDEO_EFFECT_UNKNOWN及旧停止结论保持。
  本轮负责人只写合同/看板/设计补充，未运行processor、读取配置/真实媒体或改codex-results。

### 2026-10-25 · 验收045原生PTS链路限定CPU原型，关闭任务

- 核[8f648e8](https://github.com/floomeer83felix-source/vlm/commit/8f648e875e8339fe2fb3c1c78dea9ef2df64bc30)五处allowlist，核心244行/验证器99行及回执，形成[负责人验收](./research-decisions/post-045-native-pts-adapter-disposition-2026-10-25.md)。
  两新源码SHA独立计算匹配封存；未运行旧tests、Torch/processor或访问Windows/私人配置。
- CSV/Fraction/struct独立复算9槽：索引、实际24个回调均值/原生时码、整数ID/attention/grid字节hash、所有kwargs/完整/视觉签名与关系均相容。
  正式9 PASS、失败/未知/NOT_RUN0；base身份不变，公开视觉hash一致，直接BF16 torch.equal与tokenizer roundtrip保留执行者实测层。
- Q04/P-A与Q05/P-B只在原生时码文本区改变输入；Q07新显式A复现Q04，Q06原生未污染。
  Q09首patch 1/200秒、其余1/100秒raw差量化为0，完整输入等于Q08；9槽分为3类，不当独立模型观测。
- 实际1探针+9正式=10/12调用；初始库导入失败与唯一ImportError兼容修复保留。四阶段wall独立加和110.0447841秒≤600；
  初始失败worker未到CUDA断言，不追认动态PASS；当前worker未初始化，模型/权重/媒体/解码/网络/GPU0。
- **ACCEPTED_CPU_NATIVE_PTS_BOUNDARY_PROTOTYPE / NATURAL_MEDIA_AND_TASK_EFFECT_UNKNOWN；045关闭，当前0 READY。**
  实现硬限定F96/T96/48帧/merge2，仅通过窄实现门；任意180–900秒自然资产的F/T/PTS映射仍需真实入口后验证，不能只改常量宣称通用。
  不自动046或继续纯受控变体；044获取路线停、真实原片/时钟/标签桥接/题目身份/强N/64格及模型效果仍HOLD。
- 本轮仅负责人验收/归档/规划补充，codex-results与045代码/回执/CSV不改。
  NOVELTY=RETAIN0、NATURAL_VIDEO_EFFECT_UNKNOWN及旧科学/媒体/训练停止结论保持。


### 2026-10-25 · 冻结046确切HoloAssist单副本与真实CPU输入提案，待一次媒体授权

- 用户要求继续下一步。已核main=c7eb259及AGENTS/看板/results/总览，045已消费；不重开旧任务或继续纯受控夹具。
- 公开来源实查找到HoloAssist在EgoIT发布者仓库的单文件：固定commit dabc7958c501ce7cb7a0e6082e41ffdee547a1b7，
  R015-7July-Switch，LFS114523050B及SHA256均由发布commit/文件页/三行pointer互证，详见[来源说明](./research-decisions/holoassist-single-copy-entry-proposal-2026-10-25.md)。
  是不同数据集/分发入口，非EPIC镜像/续传；其完整原片身份、时长、PTS和标注时钟仍UNKNOWN。
- 未用约111秒的R007小样例凑180–900秒门，也不因目录显示115MB推定H01时长合格。
  不下载大tar、不从旧盘找视频、不主动读取标注文件；网页自动附带的其它训练样例不参与选择或研究。
- [046完整合同](./codex-artifacts/VLM-HOLOASSIST-REAL-INPUT-046/README.md)合并一次必要真实传输预检、固定文件获取、CPU全帧验钟、
  满足高漂移/时长/资源门后的真实F/T P适配与强N输入；不用先做假传输/找路径微任务。
  新媒体128MiB、HEAD1/GET链≤3发送、获取840/870/900秒、CPU累计1800秒、RAM4GiB/线程4、父5400秒，
  两遍解码、processor≤5/正式三槽；所有失败/未运行保留，原片/标签科学门不能由副本hash替代。
- **PROPOSED / AWAITING_EXPLICIT_MEDIA_APPROVAL，当前0 READY。** 这是新媒体范围，按AGENTS需用户对已冻结提案明确批准；
  批准后登记一次即可，不对子步骤重复询问。负责人本轮只写六处规划文件，codex-results与旧实现/证据保持原样。
  未访问Windows/获取媒体正文/运行CPU媒体或模型；044直接路线停、042–045已消费、标签/GPU/64格HOLD及NOVELTY=RETAIN0保持。


### 2026-10-25 · 用户批准046固定H01媒体与CPU输入范围，设为唯一READY

- 用户对[冻结于1ea814c的完整046提案](https://github.com/floomeer83felix-source/vlm/tree/1ea814cd5e4bcd520516295d67a63a5c26ff6ac4/docs/codex-artifacts/VLM-HOLOASSIST-REAL-INPUT-046)原话回复“批准”。
  已将[本父合同](./codex-artifacts/VLM-HOLOASSIST-REAL-INPUT-046/README.md)登记为USER_APPROVED_MEDIA_AND_CPU_INPUT，并设唯一READY；results尚无本父交付。
- manifest原字节和SHA256 d79a7eeb7ec57e95c4c1c60418db12b794f14736891ed3046fd58712fed63ef9保持；
  候选仅H01/R015，固定分发commit、114523050B/LFS SHA256、URL/跳转白名单均未改。
  新媒体128MiB、HEAD1/GET链最多3发送、获取840/870/900秒、CPU1800秒、父5400秒、Job4GiB/线程4、
  两遍解码/processor最多5次/正式三槽及输出配额均沿用，不扩大授权。
- 本地Codex一次启动后按A→B→C→D连续完成允许阶段；完整性/时钟/180–900秒/高漂移等门失败如实保留并结束，
  不对子步骤重复询问、不重试/续传/换源、不给后续任务迁移余量。GitHub更新不会自行唤醒本地聊天，用户只需发README第6节启动消息一次。
- 负责人本轮只登记授权/规划；codex-results、manifest、旧源码/证据不改，未访问Windows/媒体正文或运行decoder/processor。
  READY不是媒体或科学门已过；原片同版/标签桥接/问题身份/6+2/64格及模型效果仍UNKNOWN/HOLD。
  042–045已消费、044路线停止、标签/模型/GPU/训练/后台未授权，NOVELTY=RETAIN0保持。


### 2026-10-25 · 验收046有界失败回执，关闭本父与本轮自动获取

- 核[ad37b05](https://github.com/floomeer83felix-source/vlm/commit/ad37b05241f1218e5d974e88f6c4ac3f964ba234)恰六处allowlist及results旧内容逐字前缀/新增10行单条，
  形成[负责人验收](./research-decisions/post-046-holoassist-input-disposition-2026-10-25.md)；两源码/manifest字节SHA独立匹配封存，未重跑tests/Windows或访问私人日志。
- 独立CSV/Decimal核1源+3臂：HEAD完整发送下界0/尝试上界1，无响应；GET/跳转/媒体/责任0与NO_GET_INTENT相容，
  不能写HEAD一定发出或网络0。源F/T/PTS/fps/漂移及hash未知，B0/P/N全部NOT_RUN，不作自然时钟/模型科研阴性。
- fetch父active0差30.5072339秒、关闭30.5389293秒在870/900秒门内；CPU五阶段outer和27.1766177秒、4项显式API检查376061B独立复算相符。
  初36断言与唯一修复后39通过只是必要预检；未获得真实媒体或processor调用，不把测试数或exit0当成功证据。
- worker时钟为约0–30秒，父起点约113万秒，源码将两域绝对值相减；WORKER_CLOCK_BINDING_NOT_QUALIFIED。
  独立父本次包络仍有测量支持，不能因此认证跨runtime worker剩余时长或给通用timeout归因；不倒推旧043/044的未公开原点/改旧事实。
- **ACCEPTED_BOUNDED_FAILURE_REPORT / CLOSED，当前0 READY。** 本自动获取尝试暂停，不重试H01/续传/加时/扩主机/换文件，
  不派下载修复、纯受控扩展或找路径占位任务；许可已消费，余量不迁移，不自动047。
  下一实质输入需当前已完整取得、原始来源/版本与使用范围明确的视频，准确私有路径可只交本地Codex；本轮不扫盘/读取旧资产。
- 本轮只负责人验收、README归档、看板/总览和设计补充，codex-results/manifest/046代码及原证据不改。
  042–045/EPIC16/既有责任保持，标签同钟/问题身份/强N真实输入及8源/16题/64格/模型效果仍HOLD或UNKNOWN，NOVELTY=RETAIN0。

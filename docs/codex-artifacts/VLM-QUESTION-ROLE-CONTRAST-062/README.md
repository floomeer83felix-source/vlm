# 062：问题角色差分与普通标准化的同参数训练对照

2026-10-31（北京时间）｜ChatGPT研究负责人。**READY，唯一尚未交付新父任务；CPU_CACHED_TRAINING。**

用户本轮要求继续；收到本次本地启动指令后，一轮完成准备、6配置真实训练、单格预测、隔离评分、核验和推送，不另拆准备轮。研究问题与近邻见[定向检验决策](../../research-decisions/post-061-question-role-contrast-2026-10-31.md)。旧057联合损失、059结构、060扩样配置保持关闭，本任务不是复活它们或继续盲换头。

## 1. 读取与固定数据

安全同步独立文档仓库main，完整读AGENTS、本合同、定向决策与[061验收](../../research-decisions/post-061-response-audit-disposition-2026-10-31.md)。next-steps/overview只读最新页首和062/061段，results全文检索062并读唯一060/061条目；确认唯一READY是本ID且未有任何既往结果。旧父ID不重跑。

从当前明确handoff/运行登记定位060/061精确私有根，不递归扫盘。060只读闭合登记/相关Job、两seal、data-bindings、四split observations/labels、feature-index、training-config、`plan-19.pt`/`plan-73.pt`及indexed366V[6,2560]/220q[2560]。这些计划包含A/P1初始状态，**只使用A及sequence**，不实例化/训练P1；旧最终checkpoint及主模型权重不读。061只读其闭合/汇总/覆盖及seal、访问清单，用于身份/固定分层核对，不运行旧main。按060索引解析旧057特征路径，不遍历旧根。

来源/成员/标签/特征与060/061封存逐项一致：133 Breakfast＋50 Salads；split68/11/54/50、组25/4/20/25；数据证据PUBLISHER_COMPOSITE_QA不变。保留所有原索引/视频/原题/标签与发布者交换关系，来源组无交叉，50Salads25编号family各两试次。准备者可核标签绑定，训练角色只读train68标签及所需训练输入；不读评估标签、旧A68/B0预测/正确性或来源映射。程序角色不认证OS访问。

只验证本次实际读取文件的封存/前后身份，不重哈希整个旧根/ZIP/模型权重。CPU tensor均weights_only/map_location='cpu'，有限float32；特征单文件≤2MiB、两旧计划单文件≤4MiB；全任务累计特征读取≤256MiB，元数据/旧预测≤32MiB，旧初始计划读取另计并披露。新根不复制视频/帧或全部旧特征。

## 2. 三个固定问题变换，不改变视觉输入

令h(q)为已有纯文本末token特征。只针对原模板`Does the event "A" happen before the event "B"? Answer Yes or No.`，从**当前问题字符串**严格解析A/B，生成tau(q)为交换两个原事件字符串的同模板。核它与已有缓存精确匹配；不依赖original/reversed标记、问题0/1编号、源ID或标签。解析歧义/缺缓存为BLOCKED，不重写文本或新跑Qwen。

Q_train为train68两个问题的**84个去重原字符串**，按UTF-8字节升序，必须对tau闭合。定义训练锚a(q)：计算`SHA256(b'VLM062/anchor/'+q.encode('utf-8'))`前8字节按big-endian转整数mod84，从该位置在Q_train循环前进，取首个不等于q或tau(q)的字符串。对所有split使用同一训练锚名单和规则；不按来源/答案/分数/seed改配。

| 臂 | 原始向量z_j(q) | 作用 |
|---|---|---|
| C_CENTER | h(q) | 普通标准化主强对照 |
| D_ROLE | (h(q)−h(tau(q)))/2 | 匹配当前问题的角色差分 |
| N_UNMATCHED | (h(q)−h(a(q)))/2 | 无关训练问题差分负控制 |

三臂各自只以Q_train拟合`mu_j=mean z_j(q)`、`s_j=sqrt(mean_{q,d}(z_j(q)[d]−mu_j[d])^2)`。统计/减法用float64，固定输入`T_j(q)=float32((z_j(q)−mu_j)/s_j)`。s_j须有限且>1e−8，否则BLOCKED；不另加epsilon、调系数、逐向量单位化、白化、裁剪或选择维度。没有可训练的normalizer参数，不能用测试q拟合均值/尺度或锚名单。

V六时间单元完全不变。D只在输入表示上读当前问题派生文本的缓存特征，**不读取它的预测或标签、不硬编码输出符号或互补答案**；输出仍是普通A一次forward。N锚为训练文本常量，不是另一视频或答案来源。外部推理接口只接收当前V和当前原问题；内部由原文构造所需文本并查无标签缓存。当前试验没有新文本编码调用；从原始文本部署时D需额外派生编码，不宣称冷启动端到端等成本。

准备角色可预先生成所有无标签变换输入，但mu/s/锚严格train-only。对训练84问题独立核均值近0、RMS近1、D原始差的交换反号及锚排除规则；这些是输入数学核验，没有头forward或优化。若新视图与旧raw A68配置完全等同则BLOCKED，不能改任务ID重训旧配置。

## 3. 六次真实CPU训练

复用[056普通A](../../../prototypes/question_temporal_056.py)的TemporalHead/pack/optimizer，不改旧源码或使用其I/V/S损失；每臂356673参数全部参与计算。每seed直接用060 `plan-{seed}.pt`的A初始state和原sequence[250,8]，核seed19/73、n68索引和68成员覆盖，与060实际计划逐张量一致；三个新臂同seed初始state/采样计划完全相同。不能从旧末期权重继续或重新抽计划。

固定顺序seed19 C_CENTER/D_ROLE/N_UNMATCHED，再seed73同序；各250次真实forward/BCE/backward/AdamW step，共1500步，batch8四格/32cell，每配置8000cell曝光，总48000。CPU float32、4线程/interop1；原AdamW lr1e−3、wd0.01、betas(.9,.999)、eps1e−8、clip1，只有第250步末期checkpoint。每步loss有限、每参数张量grad非None且有限，记录前后实际state/有限loss轨迹/步数与最终参数变化。

不作软件warmup/额外头forward/fixture optimizer、额外epoch/seed、早停或验证挑选。A68旧头不载入/forward/重训，P1/I/R1/H不运行。CUDA_VISIBLE_DEVICES在import torch前置空，确认CUDA未初始化。完成训练Job actualactive0后才运行独立预测角色；训练角色不持有非train标签/旧结果。

## 4. 单格预测、缓存与次要分层

新3臂×2seed×183实例×4cell＝**4392新独立单V/当前q预测**，每cell一次，不利用另一个cell输出。先封存新代码、输入变换、全部末期checkpoint及4392新输出；训练/预测Job均actualactive0后，评分角色才读取060 all-outputs，严格投影**A68的1464项＋单次B0的200项**，不重新forward。正式总**6056=4392新头+1664缓存**。

33条件：A68_CACHED/C_CENTER/D_ROLE/N_UNMATCHED×seed19/73×四split＝32，另B0/NA仅source_holdout50一行。每行全N、cached/new/complete/valid/INVALID/FAILED/NOT_RUN/unknown、单项/视频对/问题对/四格正确数及准确率，另有061五类响应、K0..K4、question_invariant/率。缓存9行的所有原正确数/分母须复现060/061；B0不复制成两个seed，INVALID留分母按错，失败/未知不当错冒充完整。

另作32行固定development54覆盖子层：4头方法×2seed×PAIR_SEEN28/BOTH_EVENTS_SEEN_PAIR_NEW19/ONE_EVENT_SEEN7/NO_EVENT_SEEN0。归一化与train68参考严格同061，成员预先封存，不按得分选层。报告N、单项/四格正确与问题不敏感；空层n0计数0/率NA/status EMPTY，不当执行失败。各层合计原development54，不能把这些再加进6056或当独立确认。50Salads仍为50/50 NO_EVENT_SEEN；名称未见不等于动作语义/预训练未见。

## 5. 配对区间与固定判据

source_holdout固定8行配对：每seed D_ROLE−C_CENTER（主）、D_ROLE−N_UNMATCHED（负控）、D_ROLE−A68_CACHED、D_ROLE−B0（后两锚点）。每行四格左右独对/都对/都错/unknown、净例数/pp与95%区间，并列两臂question_invariant数、差pp及其区间。正的问题不敏感差表示更差，不当答题改善。

JSON公开**200行匿名family×seed×比较**聚合，F01..F25字典序映射一致、各n2，含上述四种正确性计数/unknown及left/right_question_invariant；不含实例级数据/预测/标签或反查映射。全部8个答题差与8个问题不敏感差，共16区间，从这些行可独立复算。Random55062初始化一次，共10000次choices(range(25),k=25)，所有统计用公共抽样；簇内两个实例均保留，实际抽样N，线性2.5/97.5%分位。

**答题门**：两个seed的D_ROLE各四格≥10/50，且各净胜C_CENTER≥3、N_UNMATCHED≥2。**响应门**：两个seed的C_CENTER.question_invariant−D_ROLE.question_invariant都≥10/50（下降20pp）。只在全部6056完整且有可评分标签时判门，否则INCOMPLETE/UNKNOWN。

| 答题门 | 响应门 | 完整比较结论 |
|---|---|---|
| PASS | PASS | ROLE_CONTRAST_DEVELOPMENT_SIGNAL，尚非新机制/独立确认 |
| FAIL | PASS | QUESTION_RESPONSE_WITHOUT_REQUIRED_ANSWER_GAIN，停止此差分 |
| PASS | FAIL | ANSWER_GAIN_WITHOUT_TARGET_RESPONSE_EVIDENCE，不保留该响应解释/差分机制 |
| FAIL | FAIL | NO_SUPPORT_FOR_THIS_ROLE_CONTRAST，停止此差分 |

即使响应改善或N很差，也不能代替胜C的答题门；C/N好seed不改称新主方法，不调mu/s、锚、系数、层、lr、步数或seed继续搜。区间为已使用来源上的描述性证据，不引入新显著性门。此门在061结果已知、062新执行前设置，不是独立预注册确认或纯词汇因果效应。

## 6. 预算、封存与独立核验

父elapsed≤7200秒；训练＋新预测＋评分CPU监督外层累计≤1200秒/JobRAM≤8GiB/4线程，其他准备/数学fixture/只读独立复核累计≤600秒；active-process≤4。新根≤128MiB/512文件，头initial/final/plan副本≤32MiB、起始free≥256MiB。只用原conda pytorch，不装依赖/新模型/改环境；Qwen/视觉encoder/processor/tokenizer/新文本编码/GPU/nvidia-smi/媒体RGB/ZIP读取/解码/研究数据网络/TimeBlind均0。

独占新062根和持久账本，自有Job监督/计时/active0先行，不删旧锁或杀他人进程；步骤/预测用固定几份append-only JSONL，不按每cell创建独立文件。首个新配置STARTED/训练forward（较早者）前封存全部代码、mu/s/锚规则、成员/子层、初始化/sequence、公式/门和预算。允许必要修复只在此前，留失败成本并重封；研究开始后失败不重启/续步/改名。缺输入/身份/预算/锁则有界BLOCKED，失败表保留完整计划分母/NA，不改成员或隐藏难例。

独立核验不导入被测分析/评分模块、不重复任何头/Qwen forward或optimizer；可只读CPU torch检查真实mu/s、84训练文本/锚、view输入、原初始化/sequence、6个末期state和1500步账本，以及4392新记录与1664缓存投影。独立从标签/预测重建33/8/32表、200匿名来源行与16区间，核所有positive/negative/unknown、门结果、旧实际使用资产前后身份和成本；不进行原模型/媒体全量哈希。程序角色不是OS访问或物理独立认证，报告真实边界。

## 7. 八处交付，随后停止

只新增以下七文件及向results追加唯一062父结果：

1. `prototypes/question_role_contrast_062.py`
2. 本目录`execution-receipt.md`
3. `scientific-results.md`
4. `condition-summary.csv`（33行）
5. `paired-summary.csv`（8行）
6. `subset-summary.csv`（32行）
7. `execution-summary.json`（6配置/1500步/200来源行/16区间、门与全部成本/未知）
8. `docs/codex-results.md`仅一次append

不上传原题/事件文本、标签、逐项预测/正确性、数据/模型身份hash、私有路径/映射、normalizer/特征/权重或媒体；公共源码自身LF SHA可报。AGENTS/README/规划/旧源码/旧results不改。核八处allowlist，普通安全commit/push main后STOP。本地执行者不自动领取063；负责人验收时按用户新偏好同回合给出下一条具体指令，额外受控资源仍需相应明确范围，不继承旧GPU/下载余额。

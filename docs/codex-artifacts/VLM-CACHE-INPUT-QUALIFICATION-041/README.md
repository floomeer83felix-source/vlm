# VLM-CACHE-INPUT-QUALIFICATION-041 — 真实缓存组件与Qwen CPU输入资格测试

2026-10-24（北京时间）。**READY / CPU_PROCESSOR_COMPONENT_BUNDLE / NOT_EXECUTED**。
权威：[冻结协议](../../research-protocols/cache-input-qualification-2026-10-24.md)；
[负责人已做组件复现与先例筛查](../../research-proposals/cache-input-contract-qualification-2026-10-24.md)。

040已关闭，SQLite匹敌F的裁决不变。041验证一个具体的第三方缓存—processor接口条件，不扩事务框架，也不恢复038–039问答/图形时钟变体。用户发送第6节完整新消息后才执行整包，不由远端文档唤醒。

## 1. A–H连续包（均INCLUDED，不另设READY）

| 子项 | 交付与边界 |
|---|---|
| A 源码与契约 | 核固定上游夹具/许可证/四文件hash；核Instance→ResponseCache→callback/backend顺序。区分数据不可变假设、命名空间控制、组件执行和完整CLI。 |
| B 新CPU bridge | 新cache_input_contract_041.py：加载原封缓存组件与自有CPU processor backend，按协议生成72状态和288序列；复用040公开Job/Process，不改040或创建通用新runner。 |
| C 关键验证 | 新test_cache_input_contract_041.py，关键真实SQLite hit/miss/已有文本隔离/强namespace控制、实际processor边界验证；套件≤2次，正式前至多一次源码依据的API兼容修复。 |
| D 72边界oracle | 已有Qwen3-VL处理器实际CPU预处理，自造RGB/metadata，完整kwargs/最终BF16签名；72预期关系与实际关系都报告，不做任何模型推理。 |
| E 正式比较 | UPSTREAM、SOURCE_NAMESPACE、EFFECTIVE_INPUT、NO_CACHE；36对×AB/BA×四配置=288序列/576查询，真实缓存组件，无手填命中；所有失败分母保留。 |
| F 成本与复现 | 实测processor次数、内容hash、序列化、SQLite/端到端成本；新目录8指定序列16查询同机复现，强hash不能免费借oracle。 |
| G 研究价值 | 报条件性合同风险、强现有解决措施、真实使用场景是否成立及先例；不以普通hash、新增测试或marker差异宣布科研创新。 |
| H 安全交付 | 六处allowlist、一条041父结果，一次普通安全push main后STOP，不自动042/GPU/上游Issue/投稿。 |

若processor入口缺失/不支持，只把相应部分NOT_RUN，仍交付可完成的上游组件与控制；不扫旧盘、问原标注路径或伪造有效输入。若新组退出归属不明则停止全部执行并报告，不影响用户进程。

## 2. 固定范围与实际组件

源码夹具在third_party/lmms_eval_cache_8f400975/，已由负责人按固定提交封装；本轮无需外部源码下载或pip安装。上游文件禁止编辑；保持完整LICENSE。运行时只允许namespace导入隔离及可选日志适配，不改key/Instance/SQLite算法。

自有backend响应是“INPUT_SHA256:”加当前实际CPU边界hash，不是Qwen回复。请求callback从当前自造doc取数据，不把backend模型参数变动冒充媒体变动。强控制按协议真实支付计算。
不得调用ResponseCache.create或OmniCompass下载/模型全量hash；不声称测试了完整lmms-eval CLI或其Qwen适配器。

本轮最多读取一个**已知039 runtime/config.json**恢复model/runtime定位（≤1MiB），除此不读任何旧私人根。也可直接用当前聊天已经明确的Qwen3-VL-4B processor目录。正常本地processor/tokenizer配置读取允许，权重正文不允许；不按后缀猜测去读权重、不递归查找模型目录。

允许读当前GitHub协作文档、041两文件、固定夹具、新实现、040公开runner中的Job/Process及039公开make_input用法。最多4个确切已安装processor相关源文件合计4MiB可定位API；不可遍历site-packages或旧研究目录。

## 3. 资源与停止（整个包一次新授权）

- 父任务≤5400s；受监督wall总≤1000s。新suite≤2×60s/processor≤16次，正式CPU worker≤600s，clean≤90s/processor≤16次，初始化/清理预留190s。
- 全轮实际processor调用≤720，包含72oracle、正式各查询应付的计算、suite/clean/API检查。模型load/forward/generate、GPU、CUDA初始化均0。
- 一个正式CPU worker/一次processor加载，所有tensor CPU，视觉最终BF16；线程≤4、Job RAM≤4GiB，临时CUDA_VISIBLE_DEVICES为空。只可检查is_initialized不触发设备查询；不nvidia-smi。
- 新临时根与clean根合计≤2048文件/32MiB；首个输出前实测配额外≥2GiB磁盘余量。不上盘RGB/整块tensor/模型文件。
- 所有child执行前纳入本轮所属Job，不能breakaway。只清理本轮可证归属CPU进程；实际active0后结案。禁止动旧锁、kill peer或改变系统配置。
- 队列/源码/参数封存后正式只一次，坏例不重跑，剩余NOT_RUN。无metadata漏传、字体/问答变体、真实QA/gold、原标注/帧/预测、私人helper、媒体解码/下载、训练、安装/新环境或实验网络；仅Git同步/push联网。

## 4. 两报告与完整数据

cache-input-results.md：
72输入状态实际kwargs key/shape/dtype、视觉/文本/完整hash、native时码和预期/实际关系；
288序列/576查询汇总及四配置分家族完整分母；
不兼容复用/正确复用/合法保守miss/正确新算/失败/不稳定/NOT_RUN；
所有实际processor调用计数与成本，free/Job/CPUwall/峰值/输出/退出及实现缺口。
公开小型自造输入/时码/token IDs可用，不公开配置正文或私人路径。

reproducibility-and-value.md：
固定上游来源/许可证与完整组件边界、日志/namespace适配细节；
已安装processor版本/配置身份的匿名收据及复现命令、clean8序列实际结果；
与旧issue1244/1255、OmniCompass、vLLM既有hash的实质关系；
数据不可变假设、简单namespace能否充分解决、是否只有人为违规案例；
按协议分级裁决，不能把marker当准确率/把CPU当GPU提速/把已知hash当新方法。

cache-input-rows.csv：
恰288行，每行两次查询的规范化JSON，能重算576查询；72oracle可在报告附紧凑表。
来源/profile/order等字段及每次调用/缓存决策/错误齐全；不筛掉关系不符和NOT_RUN。

## 5. 公共allowlist（恰六处）

1. prototypes/cache_input_contract_041.py
2. prototypes/test_cache_input_contract_041.py
3. docs/codex-artifacts/VLM-CACHE-INPUT-QUALIFICATION-041/cache-input-results.md
4. docs/codex-artifacts/VLM-CACHE-INPUT-QUALIFICATION-041/reproducibility-and-value.md
5. docs/codex-artifacts/VLM-CACHE-INPUT-QUALIFICATION-041/cache-input-rows.csv：完整288行/576查询。
6. docs/codex-results.md末尾恰一个041父结果。

CSV单独交付并在报告链接；新源码提供导出与重算命令，不只上传聚合表。

不改README/冻结协议/负责人提案/固定第三方夹具、040或更早代码、AGENTS/next-steps/overview、旧结果。只stage这六处；脱敏、普通安全push main后STOP，不自动042/发布Issue或PR/联络作者/投稿。push冲突按AGENTS停止，不force/reset/rebase。

## 6. 用户完整启动消息

以下整段作为一条新消息发送当前本地Codex；上下文已满可GitHub-first交接，不继承旧任务余额。

~~~text
继续041：安全同步独立GitHub文档仓库main，重读AGENTS.md、docs/next-steps.md、docs/codex-results.md、docs/research-overview.md，及VLM-CACHE-INPUT-QUALIFICATION-041 README、cache-input-qualification-2026-10-24冻结协议和cache-input-contract-qualification-2026-10-24立项依据。确认041是唯一尚未交付的READY父任务，连续完成A–H。

我明确授权本轮用固定上游ResponseCache组件、现有Qwen3-VL-4B processor/tokenizer和Torch/Transformers/NumPy仅做CPU输入处理。可直接用当前聊天已知模型目录；若需定位，只准读一个已知039根runtime/config.json（≤1MiB），只取model/runtime，不扫盘、不读旧账本/预测/原标注。正常本地配置/分词文件加载和最多4个确切installed processor源文件合计4MiB允许，权重正文0，local-only、trust_remote_code=False。

按冻结9家族×4刺激生成36对/72个真实CPU边界状态；UPSTREAM、SOURCE_NAMESPACE、EFFECTIVE_INPUT、NO_CACHE四配置，AB/BA两序，共288序列576查询。响应仅为INPUT_SHA256标记，无模型回答。先封存源码/夹具/参数/队列；强有效输入hash每次真实支付预处理，不免费借oracle。保留全部失败、不稳定、关系不符、NOT_RUN，不按有利输出重跑或改条件。实际入口缺失就部分NOT_RUN，继续能完成的组件与控制，不搜私人路径凑完整结果。

父≤5400s，受监督wall≤1000s；suite≤2×60s/processor≤16次，正式CPU worker≤600s，clean≤90s/processor≤16次，全轮processor≤720。Job RAM≤4GiB、CPU线程≤4，临时禁用CUDA可见设备并确认未初始化。两个新根合计≤2048文件/32MiB，首输出前记录配额外≥2GiB余量。只监督/清理本轮归属可证进程，实测active0，不动旧锁或其他进程。

完成两个新模块、实际输入/缓存/成本报告、独立完整288行CSV、clean复现与价值裁决及results一个041父追加。明确组件执行并非完整lmms-eval/Qwen适配器或真实推理，不预设新算法/论文突破；现有namespace足够解决也如实记录。GPU、模型权重、forward/generate、真实QA/gold/旧媒体、训练、安装、下载/解码和实验网络均0。只按六处allowlist一次普通安全push main后STOP，不自动042/GPU/上游Issue/投稿。
~~~

# 066固定公开入口

2026-10-31｜负责人为准入任务核对的一手元数据入口。仅说明入口/格式，未实施066完整数据审计、媒体或模型验证，不应把本简表计作新实验。

| 材料 | 固定版本与可读文件 | 当前已知及不能外推 |
|---|---|---|
| DyBench | revision `fc9a9e8dbd11107fa47f953f1367c0bcd2dbb405`；[event_sequence.json](https://huggingface.co/datasets/ddz16/DyBench/blob/fc9a9e8dbd11107fa47f953f1367c0bcd2dbb405/json/event_sequence.json)、[数据卡](https://huggingface.co/datasets/ddz16/DyBench/blob/fc9a9e8dbd11107fa47f953f1367c0bcd2dbb405/README.md) | 旧记录814行/407名义配对、元数据388049B；Breakfast/50Salads已使用，VIDHALLUC/TempCompass为本次准入候选。不是已证独立来源，未核其实际合格量 |
| TimeBlind数据 | HF revision `bafceda3a2bd0e5128c390ec25fdc54e470a743d`；[data.jsonl](https://huggingface.co/datasets/BaiqiL/TimeBlind/blob/bafceda3a2bd0e5128c390ec25fdc54e470a743d/data.jsonl)、[README](https://huggingface.co/datasets/BaiqiL/TimeBlind/blob/bafceda3a2bd0e5128c390ec25fdc54e470a743d/README.md) | 文件树显示JSONL约559kB，视频约3.98GB不属本包读取范围；数据卡列索引/视频路径/问题/答案/题型，未由此取得原录制链或判定关系兼容 |
| TimeBlind代码/标签 | GitHub `03129551918c0830f3ee727485eb9cfb437e21e5`；[README](https://github.com/Baiqi-Li/TimeBlind/blob/03129551918c0830f3ee727485eb9cfb437e21e5/README.md)、[tags.json](https://github.com/Baiqi-Li/TimeBlind/blob/03129551918c0830f3ee727485eb9cfb437e21e5/tags.json)、[utils.py](https://github.com/Baiqi-Li/TimeBlind/blob/03129551918c0830f3ee727485eb9cfb437e21e5/utils.py) | tags的Temporal_Relation含432行索引，按原四索引块为108个完整名义组；不是432个实例，也不是已核严格before样本。官方代码只能静态读，不运行其LLM judge/模型/抽取服务 |
| 近邻关系/数据使用说明 | 既有TimeBlind论文/数据卡及055/060研究决策中的已核构造说明 | 成对/互补不等于角色交换；新数据集名称和不重复文件名不证明与DyBench物理独立。卡中研究用途说明不能被扩张为所有原视频权利证明；媒体准入仍待另立范围 |

若固定版本无法获取，不替换main继续，而是给出该分支UNKNOWN并完成另一分支。不要执行作者README的git clone数据集命令。仅准入所需文字/JSON/API目录元数据，禁止视频文件的GET/HEAD/Range/ZIP访问。

当前062 tau的唯一文法见[固定源码](https://github.com/floomeer83felix-source/vlm/blob/be8076782d2a813af131eff6d8dddb9fc0450e9d/prototypes/question_role_contrast_062.py)。TimeBlind公开页面预览已被负责人阅读且包含答案；后续不得写“标签从未被见过”。066须隔离答案字段，不以其值筛样本；无模型分数/新推理，未形成有利结果选择。

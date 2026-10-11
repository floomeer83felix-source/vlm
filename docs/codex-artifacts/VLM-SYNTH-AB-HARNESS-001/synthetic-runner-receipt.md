# VLM-SYNTH-AB-HARNESS-001：可执行合成配对工程收据

2026-10-11（北京时间）；状态 **SYNTHETIC_HARNESS_PASS**。这份交付证明标准库合成程序及恢复测试可运行，不是自然长视频研究结果或REAL_VLM_EVALUATION_GO。Ego4D媒体批准仍HOLD，NOVELTY=RETAIN0，旧Charades及REAL-PILOT任务不重开。

## 范围与可复现命令

公有docs checkout原工作树干净，安全同步main `92f399d`，确认本父任务唯一READY、无既有结果，重读AGENTS、任务板、总览、结果、合同、实验重整/旧REAL-PILOT合同及旧toy兼容参考。独立新增[运行器](../../../prototypes/hourvideo_synthetic_ab_runner.py)和[测试](../../../prototypes/test_hourvideo_synthetic_ab_runner.py)，未修改旧原型或工具。

在文档checkout运行，不需要安装依赖：

```powershell
python -B -m unittest prototypes/test_hourvideo_synthetic_ab_runner.py -v
python -B prototypes/hourvideo_synthetic_ab_runner.py --synthetic --self-test
python -B prototypes/hourvideo_synthetic_ab_runner.py --synthetic
```

CLI只支持synthetic及合成自检，无真实输入/输出根参数；默认输出scope、固定分母、尝试预算计数和真实调用0，不把模拟准确率放到默认科研输出。内存评测API可供测试检查虚构成绩，但不作为研究效应。

## 实际执行次数和结果

| 执行 | 用例/结果 | 边界 |
|---|---|---|
| 首次unittest | 30/30 PASS，0失败/错误/跳过，退出0，测试框架用时4.348秒 | 纯虚构CPU测试 |
| 加入代码指纹恢复约束后的最终unittest | 31/31 PASS，0失败/错误/跳过，退出0，用时4.346秒 | 最终源码测试结果 |
| 指定CLI self-test | 同一最终31项全部PASS，退出0，用时3.506秒 | 独立入口实际载入测试，不是空壳自检 |
| 完整CLI synthetic dry-run | 退出0，24 planned pairs / 48 planned arms / 48 reserved attempts；真实GPU秒数0、真实模型调用0 | 不发布模拟准确率或答题明细 |

合计3次suite执行、92次测试方法执行；指定unittest命令执行2次、CLI自检1次、完整CLI演练1次。测试框架用时是CPU工程验收wallclock，不是虚构模型成本或GPU时延。两次额外短命子进程路径在各suite内测试实际退出和锁冲突；没有后台监控、睡眠或常驻进程。修改代码后才复验最终suite，没有失败被隐藏或免费重试真实模型。

## 端到端契约

内存生成12个SYNTH虚构视频、每个2题，共24道五选一题；8段声明1400秒、4段声明1900秒，均为虚构metadata。不可变manifest绑定policy/seed、题目与选项、独立评分键digest、24/48分母、视频间交替AB/BA顺序及运行器源代码指纹。恢复时版本、seed、候选策略或评分键绑定不一致拒绝，代码变化也不能继续旧账本。

A用全抽象duration内12个bin centre，唯一、递增、不含右端点。B最多48个候选，用只看问题、duration、候选位置及policy/seed的SyntheticScorer打分，确定性去重/排序选择12点。选帧接口不接收选项、正确标签、模型响应或评分，stub提示含虚构问题/选项/所选位置但不含评分键；答案只由下游evaluate访问。测试改变评分键不改变选择或stub生成。

固定24题分母下各臂独立计correct/wrong/invalid/failed/unfinished/not_started。四种有效配对互斥；任何一臂不是可评分终态归invalid_pairs，五格合计恒为24。每视频形成2题簇，共12簇，另有20至不足30分钟/至少30分钟两个互斥分层；未实现可选bootstrap，不给合成置信区间科学意义。

B的候选评分操作单独统计：完整运行每题48次，共24×48次虚构候选打分；同视频不同问题分别评分，不能误报只编码一次或总成本相同。每臂模拟预扣1个秒单位，B另预扣候选数×0.01的虚构单位，均显式称simulated seconds；不对应任何SigLIP/Qwen测量。真实媒体读取、预编码和GPU预算始终0。

## 持久性、预算与中断测试

每个新run只能创建于程序自己tempfile生成的专用目录，所有manifest、snapshot及锁均为合成对象；无外部数据输入路径或旧研究账本加载。snapshot先写临时文件、flush/fsync后os.replace；checksum用于发现普通损坏，不是对恶意本地篡改的签名认证。

在持有非阻塞OS锁时，先把STARTED和累计尝试/模拟费用预扣保存，再执行选择器及stub；异常不退款。TERMINAL响应不可覆盖，STARTED未终态不可重试。正常部分运行后resume与完整运行报告相同；测试实际子进程在stub入口os._exit，父进程恢复后该臂保持unfinished，另一未开始臂可依原合同/剩余预算继续。全48额度包括此未终态，而不是额外再调用一次。

模拟尝试总额硬限制48，可冻结更低额度用于测试；模拟时间预算最多7200秒单位，不够即停止并保留所有未开始项。它不实现真实模型任务超时、进程管理或GPU计时。磁盘全局停电/Windows文件系统目录落盘语义、恶意修改snapshot、跨机器共享盘锁和真实推理中断尚未认证；遇未完成.pending文件保守失败关闭，不自动清理后重试写入。只能释放自身OS锁，不删除别人锁；清理限本次拥有且检查独占的临时目录。

31项测试覆盖12×2、A/B帧/候选约束及query变化、答案隔离、完整分母/五种配对、失败/无效、恢复等价、STARTED异常和实际进程退出、尝试与模拟时间预算、manifest/seed/policy/评分键/代码pin、ledger损坏、终态不可改、同进程/跨进程锁冲突、真实输入flags及adapter拒绝、非法时间/重复题/label/候选/预算、已有run与外部根拒绝、AB/BA顺序。只用虚构对象，没有真实数据片段或历史run。

## 安全与停止

0 GPU/CUDA、真实Qwen/InternVL/SigLIP/Torch/transformers、真实媒体/视频头/PTS/解码/ffprobe、真实QA/HourVideo JSON/Downloads访问，0视频/权重/标注下载、HF/AWS/Ego4D API、凭据或付费服务；0原研究工作区/模型/ledger/锁/状态访问，0依赖/环境修改。仅公有Git、新标准库代码、自己生成的临时合成对象及文档提交检查。

真实scorer/model adapter明确NOT_INTEGRATED，媒体时间基只是duration抽象。后续需独立授权和媒体许可/批准、版本映射、真实模型接口、历史去重、GPU锁/计费/限时合同，才能另行考虑接入；本轮不新增任务、不申请媒体或GPU。仅四处允许产物，正常push一次后停止、保留聊天等待ChatGPT验收。

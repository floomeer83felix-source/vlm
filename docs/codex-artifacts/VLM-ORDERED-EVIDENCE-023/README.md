# VLM-ORDERED-EVIDENCE-023｜CPU纯合成有序事件证据选择器与反例测试

**2026-10-19：READY / SYNTHETIC_STDLIB_ONLY / 单轮结束STOP。**

用户同意下一步从反复资产准备转为可证伪的时序证据研究；本轮只在公开GitHub文档/源码checkout实施[ChatGPT预设研究协议](../../research-protocols/ordered-evidence-2026-10-19.md)里**无需真实数据或模型的纯合成算法**。不是GPU训练、视频/模型推理、protected QA或新素材权限。

1. 安全fast-forward同步文档checkout的GitHub main，读AGENTS.md、next-steps.md、codex-results.md、本README、研究协议和017/018**公开匿名**成果。要求唯一READY=023且无旧023回报、无冲突，否则STOP；不修改实际研究工作区Git或账本。
2. 新增`prototypes/ordered_evidence_selector_023.py`（Python标准库，纯函数，无任何真实输入/私有file open）：实现OEP-12的AB/BA两方向可信有序帧对、无证据/无可分解时B精确fallback、12帧固定唯一PTS排序、非法输入HOLD、阈值与tie固定，并提供unordered消融。任何数组仅由调用方给定**合成ID、相对时间戳及数字分数**，不能接收/访问金标、答案、现实题目、真实媒体或隐私路径。
3. 新增`prototypes/test_ordered_evidence_selector_023.py`：≥12个独立`unittest`，至少覆盖两种方向真假、同分、重复实例风险、一个事件过度相关挤占帧、无事件证据时精确Top12、非法PTS/NaN/重复ID、排序/帧数和旧TRAIN-PREP无向abs差/元素积交换不变反例。测试应有反例、断言和可见失败解释，不能只做self-confirming happy paths。
4. 只对本task新Python模块运行最多**2次**有界stdlib unittest（优先1次，一次静态代码修订后可再测1次）；每次owned child≤60秒，全部父CPU执行≤240秒。没有可靠watchdog则只静态交付并注明NOT_RUN。禁止import torch/numpy/transformers/av或任何模型/依赖安装。
5. 公开结果只新增`docs/codex-artifacts/VLM-ORDERED-EVIDENCE-023/synthetic-order-falsification-receipt.md`和在`docs/codex-results.md`末尾追加恰一条`### VLM-ORDERED-EVIDENCE-023`。**合计只准4处变更**（上述两份Python、一份匿名receipt、一条append）。收据必须记测试PASS/FAIL/HOLD数、算法输入前提、显式失败/能力界限、`REAL_QA_EFFECT_UNKNOWN`与`NOVELTY=RETAIN0`，并强调合成结果不能判断Qwen多事件QA、时序推理原创性或真实泛化。不得修改ChatGPT研究协议、任务README、next-steps、overview或任何旧结果。

**硬STOP**：受限 HourVideo/Ego4D/Charades媒体及QA/gold、旧source map/历史真实候选、009本地电影、模型特征/权重/Torch、GPU/CUDA、研究网络或下载、运行环境更改、私有文件写入、旧任务重跑全部0。GitHub普通协作网络除外。一次非强制常规main push后即停，待ChatGPT审查；TRAIN-GPU始终QUEUED/HOLD，未来任何真实实验/GPU需要独立新授权。NOVELTY=RETAIN0、CLOCK_ZERO_ASSUMED_NOT_CERTIFIED、Charades FINAL_MEDIA_STOP。

# VLM-TRAIN-CPU-RUNTIME-020｜CPU PyTorch 导入与合成动态验证

**PENDING_FRESH_CPU_MEMORY_AND_TEST_AUTHORIZATION / NOT_READY（2026-10-16）**。
本任务为新父任务预案，不许可立即执行。前任019在[90330e0](https://github.com/floomeer83felix-source/vlm/commit/90330e00e8c11c52ef12e1f8c24de6ad2ca525e1)安全停止：256MiB私有进程内存封顶下PyTorch导入报WinError1455；14个stdlib PASS、5个Torch SKIP、0 optimizer updates。失败分配大小、系统pagefile作用未知，不可推断为Torch不存在或内存上限是唯一原因。

## 必须另行授权

只有用户明确同意**一个全新的独立CPU验证**，硬封顶单子进程private-commit **2GiB = 2147483648 bytes**、父任务单调墙钟 **120秒**、真实CPU optimizer更新总 **12步**，且同意一次本地Torch DLL加载，ChatGPT才能把020改成唯一READY；用户再在当前Codex对话触发。仅上传019结果不代表授权。不得继承019或者旧训练/GPU/媒体预算。

## 020条件成立后的单轮顺序

1. 安全同步GitHub文档checkout，复核唯一READY与020无历史结果。只读检查系统可用commit/物理内存余量和自有进程监督能力；结果未知、硬Job Object无法事前生效、冲突或者受控脚本无法避免GPU时立即STOP。不得修改系统paging、环境、conda、Torch/CUDA、驱动、安装依赖、杀任何他人进程。
2. 新建专用 prototypes/test_vlm_train_cpu_runtime_020.py。新托管子进程在Torch加载前完成Windows Job Object process-memory硬限制2GiB和自有进程120秒deadline，明确CPU-only，禁止CUDA，记录真实峰值private commit、实际updates、wall time及错误类型。仅发起**一次**受控Torch import +合成动态套件；WinError1455/OOM/资源不足直接HOLD，不提高上限、不重试。
3. 复用019已冻结的16行匿名合成特征、PTS窗口/来源隔离与随机种子、真正的visual-only forward、NaN及异常fail-closed验证、random0 + trained4 + fixed-seed replay4 + shuffled4对照。整个020全部训练调用共享**12**个updates上限，真实参数变化/梯度/输出可重复性必须来自实际CPU计算，不能只打印源代码预设值。
4. 原019训练代码及原256MiB预算合同不改。若新2GiB运行确需新隔离预算适配，须仅在020专用监督脚本中显式记录并严格执行，不得伪装019原环境/预算已经通过；若不修改旧019就无法实现动态测试，则安全STOP并报告接口阻塞，不能越权改旧代码。
5. 交付仅新增该020监督脚本和 docs/codex-artifacts/VLM-TRAIN-CPU-RUNTIME-020/cpu-runtime-verification-receipt.md、在 docs/codex-results.md 末尾追加恰一条020结果。公开报告必须列明CPU import PASS/HOLD、5个动态检查状态、实际12步上限内updates、loss/梯度/参数变化/随机与打乱标签、峰内存、错误及未证科学项；普通push main一次后STOP，不能自动进入TRAIN-PREP或TRAIN-GPU。

**本任务绝对禁止**：真实媒体/QA/gold/UID、模型Qwen/SigLIP加载和推理、研究网络/AWS/下载、GPU/CUDA实际计算、环境安装修复、checkpoint、训练旧013–019素材或其dev数据。不能称此合成结果为真实HourVideo训练或科学创新，维持 CLOCK_ZERO_ASSUMED_NOT_CERTIFIED、NOVELTY=RETAIN0、Charades FINAL_MEDIA_STOP。

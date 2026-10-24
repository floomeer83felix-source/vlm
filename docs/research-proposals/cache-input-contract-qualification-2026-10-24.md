# 041立项依据：评测响应缓存与有效多模态输入身份

2026-10-24（北京时间），ChatGPT研究负责人。**COMPONENT_REPRODUCED / CPU_PROCESSOR_QUALIFICATION_READY / NOVELTY_UNVERIFIED**。

040保持NO_DISTINCT_MECHANISM_EVIDENCE。本轮不扩展其事务/claim框架，改查一个具体第三方组件条件：上游评测响应缓存命中后，实际视觉回调/processor未被调用；下游即使有媒体内容哈希，也没有机会重新核验输入。

## 1. 已读先例与否决项

固定源码为 [lmms-eval 8f40097532a7bf4db6123713f1a905e02c8f5971](https://github.com/EvolvingLMMs-Lab/lmms-eval/tree/8f40097532a7bf4db6123713f1a905e02c8f5971)（所查main提交日2026-10-22），不是漂移main：
- [response_cache.py](https://github.com/EvolvingLMMs-Lab/lmms-eval/blob/8f40097532a7bf4db6123713f1a905e02c8f5971/lmms_eval/caching/response_cache.py) 的 execute 每次使用前置连续字符串、doc_id/idx、生成参数、任务/模型指纹与eval_version。固定代码的内容摘要已覆盖生成任务前置文本；不能按旧文档“只覆盖loglikelihood”误报文本漏洞。
- evaluator.evaluate把请求交给该缓存；simple Qwen3适配器在其后调用doc_to_visual，chat适配器在其后调用doc_to_messages并构造processor输入。缓存命中会跳过backend，不仅仅是跳过某个文件读取。
- [已关闭issue1244](https://github.com/EvolvingLMMs-Lab/lmms-eval/issues/1244) 已报告Qwen3 simple路径丢失metadata造成timestamp问题；当前所读simple代码已传递metadata。**普通“时间码漏传”不是新发现，本任务不人为漏传metadata再包装该旧问题。**
- [已关闭issue1255](https://github.com/EvolvingLMMs-Lab/lmms-eval/issues/1255) 已讨论代码提交变化后的缓存身份。当前get_lmms_eval_cache_version优先Git commit，不能误报“完全没有代码版本隔离”。
- [OmniCompass现有说明](https://github.com/EvolvingLMMs-Lab/lmms-eval/blob/8f40097532a7bf4db6123713f1a905e02c8f5971/lmms_eval/tasks/omnicompass/README.md) 已有选择/采样/运行时与本地模型内容身份措施。它是强近邻，不把完整指纹当成新思想，也不运行其数据下载或全权重hash。
- [vLLM Multimodal Inputs](https://docs.vllm.ai/en/stable/features/multimodal_inputs/#cached-inputs) 已有媒体内容哈希。推断：若更上游响应缓存直接返回，则下游哈希不会被调用；本轮未运行vLLM，不能把这个调用图推断称为vLLM漏洞/性能结果。

故“再加hash”“普通输入收据”“版本指纹”“时间码存在”均不立为新核心。拟资格测试关注**特定组件接口上的输入身份条件与误复用观测**，不是证明所有缓存/所有默认CLI都错误。

## 2. 负责人已经完成的有限组件复现

在本机临时目录从固定提交取得未经修改的Instance、fs_detect、ResponseCache；仅隔离包namespace以免导入整个ML环境。loguru未安装，用标准logging作日志适配；没有修改缓存函数、key生成、SQLite或响应有效性规则。backend是自有PIL像素SHA标记程序，按实际Instance视觉callback从doc中取图，**不是VLM模型**。

确认性探针使用同一个backend类/配置、问题、task/doc_id/idx、版本和任务指纹；将其数据表中32×32自造图像从红换蓝：
- 第一次调用backend1次，写入响应；
- 第二次cache hit1、backend新增调用0，仍返回原图标记，与当前图像SHA不符；
- 同一当前图像在冷缓存重新调用backend1次并匹配；
- 同一DB改任务命名空间、或改前置问题文本，对照均重新调用1次并匹配。

此前另有一个以backend直接持有像素的探索探针，方向相同；上述确认性探针改为真实Instance callback/data表取图，避免把模型参数变动伪装成数据变动。两者都不是正式041数据，不混入其分母，不构成发生率/显著性。

这个现象的前提是**数据/回调实际内容变化，但缓存身份保持不变**。许多评测任务假定数据不可变，显式更新命名空间已经能解决观测案例。因此这里只称条件性身份合同风险，不声称新安全漏洞、未被报道的全工具bug或核心期刊贡献。是否映射实际合法工作流、是否应由上游数据版本契约承担，需要041报告说明。

## 3. 为什么值得再做一次有界验证

与040自造监督方案相比，这次调用真实第三方缓存组件；下一步用既有Qwen3-VL处理器CPU边界输入，验证同题/同RGB但合法时间元数据变化是否产生实际token差异并仍被响应层复用，同时用不同表示却相同边界输入的对照记录保守重算代价。

强对照包括完整原始内容/元数据命名空间、有效输入全量hash及关闭缓存；不再发明一种必定优于它们的新机制。组件指纹标记只是验证准入的探针响应，不是Qwen答案；processor输出是CPU边界输入，不等于一次真实generate已发生。

唯一下达 [VLM-CACHE-INPUT-QUALIFICATION-041](../codex-artifacts/VLM-CACHE-INPUT-QUALIFICATION-041/README.md)，[冻结协议](../research-protocols/cache-input-qualification-2026-10-24.md)。CPU预处理、实际组件命中/未命中、强对照、完整记录和干净目录复现一包；GPU/权重/真实QA0。

最高可能结论是“具体缓存-processor组合的条件性输入合同问题已复现”，仍非新算法或工程论文创新通过。若只剩人为违背不可变数据约定且没有真实工作流意义，或强现有配置已经以简单措施充分解决，则保留LOCAL_COMPONENT_REGRESSION_ONLY并停止该线，不自动GPU/扩样/投稿。算法RETAIN0及040处置不变。

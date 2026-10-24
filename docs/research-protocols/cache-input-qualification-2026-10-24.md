# 041冻结协议：缓存响应身份与Qwen CPU边界输入

日期2026-10-24（北京时间）。**FROZEN / NOT_EXECUTED / NOVELTY_UNVERIFIED**。
父任务：[VLM-CACHE-INPUT-QUALIFICATION-041](../codex-artifacts/VLM-CACHE-INPUT-QUALIFICATION-041/README.md)。
依据：[负责人组件复现与先例排除](../research-proposals/cache-input-contract-qualification-2026-10-24.md)。

## 1. 命题与组件边界

检验条件命题：固定前置问题、task/doc_id/idx、生成参数、模型/任务/评测版本身份时，视觉callback实际输入变化是否被固定上游ResponseCache区分；若缓存命中跳过backend，返回的输入标记是否仍属于当前Qwen处理器边界输入。

本轮调用未经修改的上游ResponseCache构造器/execute/close和真实Instance，配合自有CPU processor backend。**不是完整安装/运行lmms-eval CLI，不是执行其Qwen适配器，不是模型推理或Qwen准确率。** 不从组件结果外推默认所有CLI任务失败；任务假定数据不可变、用户负责变更命名空间的解释必须讨论。

使用仓库内固定[源码夹具](../../third_party/lmms_eval_cache_8f400975/README.md)，不下载最新版，不改上游函数。允许在独立child内创建三个包namespace定位这三份源文件；若现有loguru不可用，仅以stdlib logging适配日志，不stub缓存/SQLite/Instance/processor。直接ResponseCache构造器用于精确控制固定指纹；不运行create()、OmniCompass或其模型hash/下载路径。所有这些边界写进报告。

040 Job/Process可作已公开平台包络复用；不执行040 claim/admit/benchmark或扩展它的框架。

## 2. 冻结刺激：36对、72个CPU边界状态

s=0..3，每个自造视频12帧、192×288、RGB uint8：
pixel[t,y,x,c]=(17*t+3*y+5*x+29*c+37*s)%256。
A默认metadata为total_num_frames48、fps整数4、duration12.0、width288/height192、
frames_indices=[0,4,8,12,16,20,24,28,32,36,40,44]。每次调用都新建array/metadata，不复用被processor修改过的对象。

系统文本固定“You are a helpful assistant.”。
视频问题A固定“Describe the video.”；image家族固定“Describe the image.”。
用processor.apply_chat_template，system/user中type video或image占位及问题，tokenize=False/add_generation_prompt=True。
视频processor调用沿已验证公开039接口：
text=[rendered]、videos=[array]、video_metadata=[VideoMetadata(...)]、
do_sample_frames=False、do_resize=False、return_tensors='pt'。
image家族用第0帧、images=[array]、do_resize=False。
所有输出留CPU，仅视觉浮点tensor转BF16，整数tensor不变。不传文件/URL、不开媒体、不解码。

| 家族（按此顺序） | B相对A | 事前边界关系 |
|---|---|---|
| EXACT_VIDEO | 完全相同的新对象 | EQUAL |
| EQUIVALENT_TIMELINE | indices×2、fps8、total96，duration仍12.0 | EQUAL：物理时刻不变 |
| FPS_NUMERIC | fps4改4.0，其余相同 | EQUAL |
| VIDEO_PIXEL | 全部RGB变255−RGB | DIFFERENT |
| VIDEO_ORDER | 12帧RGB倒序，metadata不变 | DIFFERENT |
| VIDEO_FPS | fps8、duration6.0，indices/total不变 | DIFFERENT |
| VIDEO_SHIFT | indices全部+2，其余不变，仍在0..47范围内 | DIFFERENT |
| IMAGE_PIXEL | 两边都为第0帧image，B为255−RGB | DIFFERENT |
| TEXT_CONTROL | 视频/RGB/metadata不变，B问题“Describe this video briefly.” | DIFFERENT |

每家族4个s，共36对，预计12 EQUAL/24 DIFFERENT。四刺激及这些家族是开发性合成控制，不是独立自然视频或真实故障率样本，不报自然基准泛化/显著性。预计关系不是结果：必须实测所有tensor key、shape/dtype/连续原始字节，以及非tensor传入值。记录input_ids/attention_mask、像素/网格、原生timecodes、分区hash与完整hash；不只比较视觉tensor或token总数。目标video grid[6,12,18]/324、image[1,12,18]/54，仅作为接口核验预期；不手改token/网格制造相等。每状态总input≤2048、视觉tokens≤512。

有效身份H为：全部规范化边界kwargs（key/shape/dtype/CPU连续bytes，BF16按byte view序列化）、固定generation声明、processor/tokenizer配置身份和已记录runtime版本/已声明模型ID。它不含未读取的权重hash，不是完整模型执行证明。null/列表等非tensor值也规范化，不能静默丢键。

先独立做72个oracle状态，仅由新数据经实际processor生成，不调用缓存key/validator作真值。重复相同状态若不稳定或关系不符，完整标UNSTABLE/RELATION_MISMATCH；不得根据有利输入删家族、改metadata或重抽s。没有稳定实际输入的格只能报告组件层结果，不能代填VLM输入结论。

## 3. 四项真实比较配置

前置Instance采用上游simple布局：
(context,gen_kwargs,visual_callback,doc_id,task,'test')；context为原始问题，不是已经插入时码的rendered输入。
doc_id=4*family_index+s，idx0，task='vlm_cache_input_041'；callback从当前doc取本轮array/metadata。
源配置/模型声明/评测版本和生成条件固定；gen_kwargs为temperature0、do_sampleFalse、max_new_tokens16。processor/backend输出“INPUT_SHA256:”+当前H作为探针响应，**无模型调用**。

| 标识 | 配置及应付的真实计算 |
|---|---|
| UPSTREAM | 原封不动ResponseCache的现有key，固定静态任务/模型指纹；只有miss时backend实际调用processor。 |
| SOURCE_NAMESPACE | 同一上游组件，任务指纹加入完整原始RGB内容摘要、全部metadata、问题、生成/processor配置/版本；每次支付内容身份计算，miss才processor。它是明确强保守控制，不故意遗漏fps/indices或版本。 |
| EFFECTIVE_INPUT | 同一组件，任务指纹加入当前实际H；**每个查询都真实processor/序列化后才查缓存**，miss可复用该次已计算边界输入，不可免费借oracle预计算。属于已知强全输入hash参照，不是新方法。 |
| NO_CACHE | 不调用缓存查表，每次都真实processor并返回当前H。 |

每配置/序列独立新SQLite文件，序列内两次查询共享该DB；两个请求间可close/reopen同一DB以更新构造器task_fingerprints，三个缓存配置均采用相同生命周期，不偷换miss/hit口径。SOURCE/EFFECTIVE的命名空间更新是明确实验干预，不冒称上游默认配置自动完成；不以此伪造已安装产品速度排名。

每对按AB及BA两种顺序，各跑四配置：36×2×4=**288序列，576查询**。主队列依family表序、s0..3、order[AB,BA]，配置基础序[UPSTREAM,SOURCE_NAMESPACE,EFFECTIVE_INPUT,NO_CACHE]左轮转(family_index+s+order_index)%4。
正式前封存源码、夹具hash、刺激/72状态、队列与配置。一个正式CPU worker/load processor，全部本轮新存储，不借旧缓存。正式开始后源码/配置/队列不变，不因结果重跑。

另计：72 oracle processor调用；正式每查询最多1次、最多576；全部suite/clean/API检查合计预留72，**全轮实际processor调用≤720**。这不是模型forward额度，模型forward始终0。

## 4. 独立指标与完整记录

每个查询公开case/family/s/order/profile、A/B侧、是否尝试、当前oracle H、实际准备的H（若有）、缓存返回标记、hit/miss、实际processor/内容hash调用次数、终态/错误、输入关系、各阶段wall/Job CPU/peak commit/输出字节。身份hash包含自造资料，不上传完整私有路径或tokenizer文件。

核心指标：
1. **不兼容复用**：hit且返回H不等于当前稳定oracle H；完整288/576分母，不把标记当Qwen错误答案。
2. **可复用机会未命中**：同序列两侧实际H相等而第二请求miss。命名空间保守隔离可能是有意契约，不称其为正确性bug。
3. 正确新算/正确复用/不兼容复用/失败/不稳定/NOT_RUN分别列出；拒绝所有请求或关闭全部缓存不能称最优。
4. 报真实processor次数、key计算/序列化/SQLite/端到端CPU成本。EFFECTIVE必须计每次预处理；内容hash参照也付读取/计算成本。marker backend的miss次数不是GPU调用/节省GPU秒，CPU成本不推算真实推理提速。
5. 图像/视觉像素变化与同RGB不同timecodes分别归因；TEXT_CONTROL应验证已有前置文本隔离。实际关系不符、API不支持、未运行不得缩分母。

独立oracle不调用上游缓存函数，不用“新hash比旧hash不同”替代actual tensor比较。所有源码/记录足以重算288序列及576查询汇总，72边界记录可公开key/shape/dtype/hash/自造时码和规范化token IDs。

## 5. 执行、复现与停止

只用已有Qwen3-VL-4B processor/tokenizer、本地Torch/Transformers/NumPy，CPU，local_files_only=True/trust_remote_code=False；不加载模型类/权重，不调用generate/forward、不init CUDA、不nvidia-smi、不安装/升级。
实际processor目录取当前本地Codex对话中已知确切位置；若需恢复定位，仅允许读**一个已知039根的runtime/config.json**（≤1MiB，只取model/runtime定位），不读039账本/预测/external-reads或扫目录找根。不要求用户重找原标注。正常processor配置/分词文件加载与最多4个确切installed processor相关源文件（合计≤4MiB）按角色记录，权重正文0。
若这些确切入口不可用，CPU边界部分NOT_RUN；仍完成有依据的上游组件、强控制、公开实现/报告，不用伪张量补齐，不新开私人路径HOLD微包。

每个CPU ML子进程临时CUDA_VISIBLE_DEVICES为空、CPU tensor/assert torch.cuda.is_initialized()==False，线程≤4、Job RAM≤4GiB；环境不永久改变。
可直接复用040公开Job/Process，首输出前记录输出配额外≥2GiB余量；新root≤2048文件/32MiB，不存RGB/tensor大副本。
父5400s；受监督wall总≤1000s，其中suite≤2×60s/processor≤16次，正式worker≤600s，clean≤90s/processor≤16次，初始化/清理预留190s。processor调用硬总数720，不按run重置。
只结束本轮归属可证的CPU组并实测active0，异常时剩余NOT_RUN。一次正式运行，不补跑坏序列。仅正式前允许一次有已安装源码依据的API形状兼容修复，不改变科学刺激/参数。

clean另一个新目录，复制两个新模块、040公开平台模块、固定夹具与LICENSE；只用这些公共依赖和同一已知processor。固定s0、EXACT_VIDEO及VIDEO_FPS、AB顺序、四配置=8序列16查询，processor≤16次，沿用正式oracle收据作公开比较参考但各配置应付的processor仍实付。记录是同机复现，不能称独立机器验证。

最终只能分级：
- COMPONENT_ONLY：只验证key/SQLite行为，没有实际CPU边界；
- CPU_BOUNDARY_CONTRACT_REPRODUCED：稳定边界确实不同却被复用，强控制正确；
- NO_REPRODUCTION或INCOMPLETE：按实际保留，无有利修复重抽。
即使第二级成立，仍不证明Qwen答案改变、实际自然基准分数污染、完整CLI/其他版本发生率、新哈希算法或核心期刊创新。
如现象只来自人为改变不可变数据且无合法工作流意义，或简单现有namespace已充分解决，明确LOCAL_COMPONENT_REGRESSION_ONLY，不自动GPU/扩大/投稿/发上游Issue。

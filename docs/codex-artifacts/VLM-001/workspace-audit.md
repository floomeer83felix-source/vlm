# VLM-001 Windows 工作区只读审计

## 执行概况

- 检查时间：2026-10-08 20:27—20:29，北京时间。
- 状态：**审计完成；建议仅对 VLM-002 元数据核查 GO，等待 ChatGPT 审查；新模型实验 HOLD。** 此建议不改变任务状态、不授权下一任务。
- 本轮依据：`docs/next-steps.md` 中唯一 READY 的 VLM-001，以及研究总览、原历史快照、结果模板和两级附件 README。
- 文档仓库检查基线：`main`，commit `7a9751b9b952c597fe5b3f6f74cfe20f1c8baaed`，编辑前工作树干净。
- 原研究工作区存在，与文档仓库分离；没有 `.git`，无法提供研究工作区 Git commit。通过小型代码及 manifest 哈希标识局部版本，不把文档仓库 commit 当实验代码版本。
- 不修改原研究目录的状态、环境、锁、账本、脚本、数据或日志。Python 仅以 `-B` 进行元数据、静态文件及聚合账本读取；未导入模型、执行 CUDA 运算或视频解码。

## 环境与资源

| 项目 | 本次实测／静态确证 | 证据与边界 |
|---|---|---|
| OS | Windows 11 专业版，10.0.26200，build 26200 | CIM操作系统属性 |
| 内存 | 63.82 GiB | CIM物理内存总量 |
| GPU | NVIDIA GeForce RTX 3090，24576 MiB，WDDM | `nvidia-smi` 查询 |
| GPU瞬时使用 | 使用1259 MiB、空闲23068 MiB，利用率7% | 单次查询快照，不能解释为整机空闲或未来可用保证 |
| 驱动 | 610.47；CUDA UMD 13.3 | `nvidia-smi`；驱动能力不是PyTorch构建版本 |
| conda | PATH中可找到；24.11.3 | 只执行版本查询 |
| 既有环境 | `pytorch`；Python 3.9.21 | 既有解释器版本及环境目录角色，个人路径未公开 |
| PyTorch | 2.5.1；构建CUDA 12.4 | 已安装distribution元数据及 `torch/version.py` 静态字段；未执行GPU兼容性测试 |
| Transformers／配套 | 4.57.6；huggingface-hub 0.36.2；tokenizers 0.22.2；numpy 1.26.4；safetensors 0.5.2 | `importlib.metadata` 读取安装元数据 |
| 所在磁盘空闲 | 359369867264 bytes，约334.69 GiB | 盘符级快照，超过50 GiB保留值；未统计全缓存总量，不能确证180 GiB缓存上限合规 |

## 资产概况

| 类别 | 存在性／概况 | 证据类型 |
|---|---|---|
| 源码与入口 | `active_vlm/`、`configs/`、`tests/`；`resume100.py`、`resume300.py`、四臂runner/scorer存在 | 目录和文件元数据；没有执行实验入口 |
| 环境记录 | `environment/` 存在，6个直接条目 | 仅目录元数据，不推定恢复操作已验证 |
| 主模型 | `models/Qwen3-VL-4B-Instruct/`：2个权重文件，共8875719344 bytes | 文件stat及config；处理器、视频预处理器和tokenizer配置存在 |
| 第二模型 | `models/InternVL3-2B/`：1个权重文件，4177999192 bytes | 文件stat及config；存在不等于跨模型实验完成 |
| 检索模型 | `models/siglip-base-patch16-224/`：1个权重文件，812672320 bytes | 文件stat及config；预处理／tokenizer配置存在 |
| 数据与索引 | `data/annotations/mlvu_dev/` 及索引文件存在 | 目录／文件存在性；未读取题文、答案或私有标签 |
| 历史视频资产 | `data/videos/` 中251个MP4，合计52979812482 bytes；最新固定源池缓存30个MP4，2447336676 bytes | 仅文件stat，两处计数不能当独立视频数；未读视频内容 |
| 实验与审计材料 | `runs/` 39个直接条目、`research/` 及多阶段manifest、状态和审查记录存在 | 必要目录／聚合状态；不是全部历史run的内容审计 |
| 最新问答代码版本 | 最新manifest的11项小型代码哈希全部匹配 | 仅小代码文件SHA复算；未批量哈希模型／视频 |

模型config分别声明 `qwen3_vl`、`internvl_chat`、`siglip`。Qwen配置中的历史 `transformers_version=4.57.0.dev0` 是保存配置的字段，不能覆盖当前安装的4.57.6，也不能据此单独判定不兼容。本轮未加载模型或实测处理器。

## 进程与锁

- CIM快照有6条Python进程，命令可读，但均未匹配本研究目录或已核查的主要研究入口。**未发现可归属于本项目的作业**；相对路径启动等情形仍可能漏匹配，不声称这些进程全部无关或整机无训练。
- GPU进程查询列出桌面／浏览器等应用，部分名称权限不足，逐进程显存为N/A。本轮无法完整辨识所有GPU占用者；未发现查询列表中的PID与上述6条Python PID相交。
- `runs/global_gpu.lock`、`runs/setup/download.lock`、最新问答及源准备的 `driver.lock` 均存在，大小均1 byte。**持有者与是否正在持有OS锁均 UNKNOWN**。
- 本轮仅检查锁文件存在性，没有打开锁作写入、申请锁、删除锁或根据旧PID文件推断所有权。
- `active_vlm/jobs.py` 静态源码具有Windows `msvcrt.locking` 非阻塞串行机制；存在实现不等于此刻锁状态已通过测试。
- 本地 `research_state.json` 记录 `paused_by_user_after_progress_publication`，自动续作 `PAUSED`。它是历史状态记录，不替代现场进程／锁检查；本轮未恢复调度。

## 持久问答账本

只读取本次找到的4个 `QA_ledger.jsonl` 并聚合状态，不公开键、题目、后验、答案或逐题评分。结果不是对所有旧格式账本的全局证明。

| run ID | reserved事件 | started事件／唯一开始键 | terminal事件 | started未终态 | 末终态error／解析错误 |
|---|---:|---:|---:|---:|---:|
| `gap_directed_defusion_fresh20` | 80 | 80／80 | 80 | 0 | 0／0 |
| `native_video_natural30_engineering_v2/validation_amendment1` | 60 | 60／60 | 60 | 0 | 0／0 |
| `natural_sampling_feasibility24` | 72 | 72／72 | 72 | 0 | 0／0 |
| `weak_binding_dev24_engineering_v2` | 120 | 120／120 | 120 | 0 | 0／0 |

最近可识别的VLM问答run是 `gap_directed_defusion_fresh20`：manifest计划80行，阶段 `complete`，计数80次QA，预算会话检查点为空，累计活动账本6993.491秒。20个实际输入组文件存在。这里只确证账本状态；本次没有重算准确率、执行评分器或重复问答。

随后还有非模型元数据run `reference_point_coverability_final_micro4`：追加大小门记录为 `terminal_pre_body_HOLD`。它是最新可追溯的访问异常／终止材料，不能当成未完成GPU前向。原生输入等早期工程故障及恢复历史存在于既有资料，本轮未逐项复核全部旧故障。

## 前提、风险与下一步建议

| 前提 | 审计结论 |
|---|---|
| 源身份隔离 | 有固定组件报告：30源prepared、20源selected；最新manifest仍记录450份历史指纹覆盖缺项，真实事件独立性未证明。新数据需要自己的隔离协议。 |
| SHA可追溯 | manifest及代码pins存在，11项代码匹配；本轮未复算全部模型／视频哈希，不能宣布全部资产完整。 |
| 时间／PTS | 当前稀疏解码器按帧索引／FPS给时间戳，源码明确VFR需PTS-aware后端。未确证新标注与同版本视频桥接，也未验证逐帧PTS；不能宣称精确PTS就绪。 |
| GPU串行 | OS锁实现存在，但现场持有状态UNKNOWN；新GPU任务前需独立获准的实际锁检查。 |
| 调用恢复 | 已检查4账本无started未终态；其他格式、遗漏run和系统级所有占用者未完整核验。 |
| 历史执行偏差 | 原历史快照报告最后形式审查合并保守耗时约677秒超过600秒；这是历史报告，本轮未重新测量。 |

**建议 GO：仅对 VLM-002 的许可／schema／时间映射元数据核查，在ChatGPT接受VLM-001并更新任务书后进行。** 该任务不要求本轮先恢复GPU或重跑历史实验。**HOLD：任何新推理、训练、视频下载或BLOCKED任务自动执行。** 新模型阶段仍缺确证锁状态、目标数据许可／同版本证据桥接、来源隔离及新的预算与输入合同。

## 资源与追溯

- 本轮新增模型调用、训练、GPU QA／评分前向、视频解码、数据集／模型下载：均0。仅获取GitHub任务文档并建立独立文档checkout，不属于研究数据下载。
- 原研究资产修改：0；未改环境、锁、账本或 `research_state.json`。开始／结束两次状态文件SHA一致。没有生成新研究run或写回历史结论。
- 仅在独立文档checkout新增本附件，并向 `docs/codex-results.md` 追加摘要；不修改任务书、总览、历史快照或PR #1。完成提交后停止。

安全可披露版本索引：

| 本地相对材料 | SHA256 |
|---|---|
| `gap_defusion_fresh20_runner.py` | `1cd7dc448725b5d188c9a7e2a71b9cb42a0911a3314a8407104a320d4ddea39b` |
| `gap_defusion_fresh20_scorer.py` | `e7d6eebf6956e31b7020c0f73ca442ff7d6704401f16dc7c32750d1ea8fdba17` |
| `runs/gap_directed_defusion_fresh20/manifest.json` | `352a9eb6722edba0672bf87bb21cfc20d25b923d106c8238a8ffa56fbcda851e` |
| `runs/reference_point_coverability_final_micro4/scope_size_gate_metadata_addendum.json` | `e7dd2016eeb31c0511c2ac5e9b5054631b05998fb6de56097adde1fa91ee7f15` |

未上传任何原始日志、模型、视频、私有标准答案、完整账本、保护身份映射、个人路径或命令行。以上是执行者只读审计，不是ChatGPT已核实的科学结论。

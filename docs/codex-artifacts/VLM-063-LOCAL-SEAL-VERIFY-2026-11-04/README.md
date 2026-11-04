# VLM-063-LOCAL-SEAL-VERIFY-2026-11-04 | 原063旧模型封存SHA只读核验

2026-11-04｜ChatGPT负责人制定｜**唯一READY父任务**｜执行者：Codex。
用户最新说明“这类任务还是交由codex吧”，系在明确呈现了下一步**本地指定权重/视图文件SHA核对**后作出的执行方式调整；本父只涵盖已向用户说明的**≤96MiB读、12个训练头及2个视图、两份封存JSON**，没有扩展到训练、GPU、模型加载、头forward、媒体、受保护标签或其它实验。旧063已关闭，不重跑原063；083仍PAUSED、084/085仍CLOSED。用户上次通过`vlm_063_asset_check_v1`提供了12/12 final.pt和9/9辅助文件非空的**stat-only**结果；存在性不代表SHA一致。

## 0. 领取与安全同步

1. 在**当前Codex会话收到用户新消息**后，先在独立文档checkout读取最新`AGENTS.md`，安全`git status --short`、`git fetch origin main`，工作树干净才能fast-forward；如不干净/冲突，STOP不reset、不删工作、不猜。
2. 重新读`docs/next-steps.md`唯一READY、`docs/codex-results.md`是否已有**本父**完成记录及本README；若任一不满足，STOP。**旧063交付记录不等于本新父已执行，但本新父只可消费一次。**
3. 本任务只针对用户本地**精确一处**旧063执行根（必须包含本地原始`training/C_NATIVE-137/final.pt`、`training/D_NATIVE-137/final.pt`、`views.pt`、`input-seal.json`、`output-seal.json`）。可使用当前用户已授权的063根或由用户在Codex私有会话直接选择/提供；**禁止从工作目录、环境变量或整个盘猜根**，禁止目录枚举、递归搜索、使用封存JSON中的任意绝对路径去找文件。根不存在、身份无法核对则`BLOCKED_REGISTERED_ROOT_UNKNOWN`，零私有读取并安全交付。
4. 既有本地`vlm_063_seal_verify_2026_11_04.zip`如存在，可作为只读技术参考，但不是受信执行证据；**不依赖该ZIP存在、不上传ZIP或权重**。Codex须用本合同明确列出的固定白名单核对，不从ZIP自动获得新权限。

## 1. 固定白名单（总共16个内容文件）

只允许读下列**精确**路径的内容，列表由本README事先冻结：

- 封存JSON 2份：`input-seal.json`、`output-seal.json`；单文件≤2MiB，严格JSON纯数据解析。不得执行任意JSON内容当代码或把含私人绝对路径的记录原样打印/提交。
- 训练头12份：`training/{C_NATIVE,D_NATIVE}-{137,263,419,557,733,911}/final.pt`。
- 视图2份：`views.pt`、`train-views.pt`。

**权限：只做SHA256流式原始字节读取，不调用`torch.load`、PyTorch、pickle、不加载权重的任何层、不开模型或processor/tokenizer、不导入现有模型包。** 单个`.pt`文件≤24MiB，封存JSON≤2MiB，合计已实际读取的内容字节≤96MiB（100,663,296 bytes）；已触达失败尝试也累计，断续重读累计计费、不得规避。只允许文件存在性/`stat`和这16个白名单文件流式读取；**其他063或062、060根一律禁止**，特别是`feature-index.json`（可能含私有路径）、`train-views`以外的张量、`old-assets.json`、`code-seal.json`、`training-job.json`、`prediction-job.json`、视频、QA/GT、日志、特征、optimizer状态，不读。可以只根据本根固定相对路径构造文件名，不用`glob/rglob/os.walk/dir`枚举。

- 校验`output-seal.json`内**预存**登记的12个`final.pt`、`views.pt`与`input-seal.json`的SHA256；校验`input-seal.json`内**预存**登记的`train-views.pt`。期望字面SHA来自本地封存，**不得用本次新计算值回填或覆盖封存**。如某条封存路径是旧的Windows绝对路径，只把它作为已登记项的**相对后缀标识**来匹配上述固定路径，不访问其原绝对位置；针对重复`final.pt`必须匹配完整训练方法/seed/文件的三级后缀、验证唯一性并拒绝任何歧义或重复。采用pathlib/PureWindowsPath和固定允许集合，拒绝反斜杠与大小写绕过、越界、符号链接/junction或封存条目数据结构异常。
- 本次检查只证明“与同一本地封存SHA是否相符”，**不对原封存的外部可信性或是否被同时修改作新担保**。若`input-seal.json`由`output-seal.json`登记可验，其哈希也应验以保证两个封存之间的内部链；`output-seal.json`本身没有另一份独立受信第三方封存就只能自述。

## 2. 资源、隔离与软件自测

- 执行总wall ≤1800s；这次私有SHA阶段CPU ≤120s，进程RAM≤512MiB；stream chunk≤1MiB；最多一次安全实现修正，记录首次失败及字节消耗。
- **先写stdlib checker和合成测试，并先通过**：固定白名单成功、篡改单字节拒绝、漏sha/重复项拒绝、封存引用外路径不跟随、超额预算阻断、路径转义/符号链接阻断、子模型重复basename不误配。测试使用合成临时根，不能混入真实63源；测试不产生“科学正确率”。
- 私有校验脚本不得读取环境变量里寻找模型、不得网络访问/下载/软件安装、不得CUDA或GPU调用、不得命令`nvidia-smi`、不得做任何模型forward、训练或外部TimeBlind视频访问。不能把SHA一致当成TimeBlind输入兼容、来源隔离或可泛化性证明。
- 实际计量`content_files_opened`、`unique_content_files`、`bytes_read`、`hashed_data_files`、`sha_match`、`sha_mismatch`、`missing_expected_entries`、`unsafe_references_refused`、CPU/wall、测试结果与未能核查的事项。预算中断时保持UNKNOWN/STOP，不宣称后续没查过的文件匹配。

## 3. 唯一输出与停止

允许的**4份新/只限本父文件 + 一次results append**：
1. `prototypes/verify_sealed_063.py`（纯Python stdlib可审计SHA脚本，必须可显式传root但不能自动定位）
2. `prototypes/test_verify_sealed_063.py`（纯合成单元测试）
3. `docs/codex-artifacts/VLM-063-LOCAL-SEAL-VERIFY-2026-11-04/seal-aggregate.json`（仅状态/计数/预算：不得有原始SHA、绝对路径、权重字节、私有标签或逐项源映射；如按文件出结果，仅固定相对方法seed）
4. `docs/codex-artifacts/VLM-063-LOCAL-SEAL-VERIFY-2026-11-04/execution-receipt.md`（start/stop、测试、两封存链、SHA覆盖、内存/IO范围与限制）
5. `docs/codex-results.md`**仅一条**完整本父记录（Codex真实执行结果）。
本README、旧062/063/068及论文、其它任务、AGENTS和规划目录均不改。父运行后只可一次普通安全push main，严禁force push、reset、私有文件入库。暂存前检验`git diff --cached --name-only`恰在上述白名单内。

输出状态只可以是`SHA_MATCH_12_HEADS_2_VIEWS_LOCAL_SEAL_CHAIN_UNVERIFIED_EXTERNALLY`、`BLOCKED_SHA_MISMATCH`、`BLOCKED_MISSING_ENTRY`、`BLOCKED_REGISTERED_ROOT_UNKNOWN`、`BLOCKED_LIMIT_OR_SAFETY`或`BLOCKED_TOOLING`。如某个内容 SHA 不匹配，**停止继续做模型工作**，不就地修复文件、不重封、不重训。两份封存一致仍不代表真实独立外部基准可运行。

推送后STOP，**不自动恢复063/083或建立086、不自动触发后续TimeBlind评价或任何GPU/媒体/训练**。负责人在收到脱敏结果后决定是否存在值得新授权的独立验证实验。  

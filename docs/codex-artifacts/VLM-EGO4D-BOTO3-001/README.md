# VLM-EGO4D-BOTO3-001｜利用已有 boto3 完成官方 full_scale 对象映射与硬预算的离线可执行门

**2026-10-13｜唯一一次性 READY 父任务（用户回复「好的」，同意优先走已安装 boto3 路线）**。原媒体父任务`VLM-EGO4D-MEDIA-001`已`ACCEPTED_SAFE_STOP`、原工具及一次独立修复`VLM-EGO4D-TOOLS-001`已`ACCEPTED_PARTIAL_BOTO3 / EGO4D_CLI_SOURCE_BUILD_HOLD`，不可重跑。**用户此次只批准有限离线工程代码与官方公开源码核对；不批准 AWS 凭据/profile访问、任何 S3 API 调用、读取真实 HourVideo/Ego4D 数据或下载视频。** 不要把此前未消费的2段/8GiB预算当成现授权下载。

目标不是又写一轮文档：**交付独立可执行的、CPU/标准库、纯虚构 manifest 的官方映射验证器 + 模拟网络GET预算/崩溃恢复门 + 真正运行的 unittest**。用于未来（新用户授权后）由受控 boto3 接入的**设计基础**，不在此轮完成真实S3实现。

## 一、启动门与禁止事项

1. 只在**独立公有Git checkout**安全检查 `git status --short`、`git fetch origin main`、可fast-forward才同步。阅读`AGENTS.md`、`docs/next-steps.md`、`docs/codex-results.md`、此合同、[前轮工具收据](../VLM-EGO4D-TOOLS-001/isolated-tool-readiness-receipt.md)、[上轮媒体安全停止收据](../VLM-EGO4D-MEDIA-001/limited-media-receipt.md)以及Ego4D官方公共开源文件。**仅本ID恰好唯一READY且结果尚无本ID任意回报才开始**；已有本ID结果、Git不洁/不同步/其它READY则立即STOP。由用户在**原同一个Codex长对话**主动触发执行，不能后台自动启动。
2. **允许网络仅供读取官方公开GitHub源码和本仓库正常Git交接**；无新PyPI包安装/更新/构建或外部镜像。不访问`pypi.org`获取新发行物。**禁止**任何私有 AWS CLI/SDK认证/profile枚举、AWS credentials原文/环境变量或密钥，禁止调用任何 S3`HeadObject`/`GetObject`/`ListObjects`/`STS`或Ego4D真实manifest API；禁止读取已经下载的真实`dev_v1.0_annotations.json`或视频/UID/QAs/答案/canary，禁止任何真实媒体/metadata/标注下载。也禁止模型/视频解码/ffprobe/GPU/训练、原Windows研究工作区/Conda`pytorch`/旧锁或ledger任何改动。**本轮SDK不用于真实连接**；至多对原已存在的专用venv做一个离线、无凭据的`importlib.metadata.version('boto3')`只读核验，可跳过（无需改环境、不创建Session/client）。
3. 官方源码可用**准确的固定commit `facebookresearch/Ego4d@4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb`**为公开证据锚：
   - [`ego4d/cli/manifest.py`](https://github.com/facebookresearch/Ego4d/blob/4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb/ego4d/cli/manifest.py)：`public/{version}/{dataset}/manifest.csv`，`full_scale`清单中可能存在`video_uid`、`file_uid`、`canonical_s3_location`、`s3_path`，`file_uid`与video UID不等价；
   - [`ego4d/cli/config.py`](https://github.com/facebookresearch/Ego4d/blob/4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb/ego4d/cli/config.py)：`VERSION_DEFAULT='v2_1'`，默认`full_scale`；不能默认HourVideo开发`v1.0`标注必与Ego4D`v1`或`v2_1`视频同版；
   - [`ego4d/cli/download.py`](https://github.com/facebookresearch/Ego4d/blob/4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb/ego4d/cli/download.py)：使用video UID过滤，但普通CLI批量下载/自动重试不会自动实现本研究8GiB GET硬预算。
   只读校验这些源码实际字段和行为；有差异则报告证据差异并安全停止相应解析规则，不静默回退到clip/540ss/镜像。
4. **工程资源**：在独立公有checkout仅运行新纯stdlib Python文件/新测试，最多20分钟CPU前台，不安装、不触摸GPU、不新建私有实验资产。测试产生的文件仅`tempfile`拥有的极小虚构manifest/ledger，退出仅清理本测试自己的临时根；不能创建真实网络对象或持久私有下载器。模拟`8GiB`与`4GiB`仅用整数/微型字节块，不实际分配GiB内存/磁盘。

## 二、必须交付的可执行工程（限定新增两个Python文件）

**新增** `prototypes/ego4d_boto3_offline_gate.py` （标准库、明确`SYNTHETIC_ONLY`、可CLI `--synthetic --self-test`以及`--synthetic`dry-run），**新增** `prototypes/test_ego4d_boto3_offline_gate.py`（`unittest`），不能仅给伪代码、计划或只做`--help`。默认拒绝其它真实参数（`--real`、`--profile`、`--manifest`、`--video`、`--s3`、`--download`等返回退出码非0）。源码文件不`import boto3`/创建Session/client或网络连接；未来接入点只通过**显式未集成接口**`LIVE_ACCESS_NOT_AUTHORIZED`拒绝。

**A. 离线对象身份 + 版本门：**
- 使用**完全虚构、内存生成**的 HourVideo风格`SYNTH_` UID集合和 Ego4D风格`manifest.csv`行，验证`video_uid`与`canonical_s3_location`/`s3_path`字段形态；默认只接收测试显式声称为官方`full_scale`的枚举版本，`file_uid`不能冒充`video_uid`、`clips`/`video_540ss`不能当`full_scale`、同一UID多条冲突来源必须拒绝、缺字段/URI不是合法S3/不可信镜像或路径不符要停止。保守解析每行，**绝不使用manifest中任意URL发请求**，拒绝`http(s)://`、bucket与key空、路径越界、路径分隔异常和不属于模拟授权官方来源身份的对象。测试可内存生成虚构`s3://SYNTH_.../`但无真实云连接；实际未来对象源必须经过正式manifest真实性与存储桶白名单独立授权，不能仅靠字符串看起来像S3。
- **重点**：任何UID join的本地模拟PASS只说明解析器机械性，**不能证明真实HourVideo`dev_v1.0`标注与Ego4D`v1`/`v2_1`同版、时间轴一致、视频权利/真正存在**。必须有独立`RELEASE_BRIDGE_UNKNOWN`默认安全停止；**不得把`v1.0`自动变为`v1`**。允许测试传入明显虚构的`SYNTH_BRIDGE_CONFIRMED`布尔模拟成功分支，但实际输出始终`REAL_BRIDGE_NOT_VERIFIED`。
- 不打印/保存任何真实UID、bucket/key或受限QA，测试ID统一`SYNTH_`。

**B. 完整离线模拟网络预算与账本：**
- 统一以字节整数固定：一次最多2个不同视频，单个官方对象声明长度≤`4*1024**3`，本父轮所有**未来研究数据 GET正文**含必要manifest/错误正文/重试/partial累计≤`8*1024**3`，其中元数据模拟子预算≤`32*1024**2`。**不要把 HEAD=0正文等于授权或不计请求；SDK`download_file`/TransferManager可能启动多线程/分段/自动重试，下一轮真实场景需关这些隐式行为。**
- 把预算实现为**写前保守预扣所有计划GET Content-Length上界**（对象未知长度/压缩传输长度可能变化/无上界即 STOP）、每个`STARTED`通过原子`fsync+os.replace`保存在测试自己tempfile ledger里，失败或中断不退款、不以新run ID重置/免费重试；幂等禁止相同对象或失败后自动第二次GET；若模拟失败后另对象须在剩余额度内且遵循冻结≤2对象；不同进程非阻塞互斥/并发冲突时fail-closed；磁盘文件路径只能在拥有的测试目录里，若锁或账本校验不通过STOP。
- 模拟`HEAD`的`ContentLength`和`ETag`/version ID一致性；校验初始声明、`GET`响应真实流入的每个**虚构微小块**及最终字节数（可以用整数代替分配大字节块），模拟响应超长/short read、ETag改变、206/Range意外、重定向、重试、异常、crash-after-start、重复启动，全部保持字节预扣与冻结状态。禁止把ETag擅自当官方SHA/MD5。
- 模拟成本/传输收据区分`reserved`上限和`actually_read`字节、错误/未终态/未开始；**不能把本地缓存文件大小当所有网络GET实际用量**，真实SDK未来如何统计HTTP响应正文、失败正文和未读正文必须在后续获批真实小请求前单独明确证明。切忌把“模拟账本通过”说成线上8GiB真硬限已认证。
- 禁止任何实际S3调用、凭据读取、SDK使用和对真实UID的HTTP请求。**工程函数必须能被纯std-lib测试独立运行**；若确实无法在不引入真实网络的情况下安全验证某项，保留`REAL_TRANSFER_ENFORCEMENT_NOT_VERIFIED`显式停止，不伪造。

**C. 真正执行的测试：**
- 必跑`python -B -m unittest prototypes/test_ego4d_boto3_offline_gate.py -v`与`python -B prototypes/ego4d_boto3_offline_gate.py --synthetic --self-test`，最好再跑CLI synthetic默认完整演练；至少**18个独立测试**，涵盖官方manifest字段/UID身份、file_uid冲突、非法release/version、官方源信任/相同UID冲突、非S3拒绝、无真实桥接拒绝、≤2不同视频/4GiB/8GiB/32MiB元数据预算、未知长度拒绝、预扣不可退、STARTED崩溃不重跑、ledger重启一致性/篡改或配置变更拒绝、同时进程锁冲突、假流块超限或长度不足、错误/重试/Range/ETag变更 fail-close，以及所有实时标志拒绝；失败不能当PASS，也不能隐藏旧测试。
- CLI必须默认只输出`SYNTHETIC_ONLY`、tests总数/通过情况、hard limits及`LIVE_ACCESS_NOT_AUTHORIZED / REAL_BRIDGE_NOT_VERIFIED`，**真实AWS请求=0、视频=0、GPU=0**；模拟成功不等于科研数据。
- **目标可执行演练**：从合成release manifest中给定2个虚构UID，模拟精确JOIN、HEAD对象长度、以STARTED预扣+小模拟chunk展示完成/安全停止和重启拒绝；不能只提交独立单元函数而没有end-to-end synthetic dry-run。

## 三、路径与退出

**公有Git只允许恰好以下四处，至少两个Python必须是真正新增可执行文件：**
1. `prototypes/ego4d_boto3_offline_gate.py`（新代码）
2. `prototypes/test_ego4d_boto3_offline_gate.py`（新至少18项单测）
3. `docs/codex-artifacts/VLM-EGO4D-BOTO3-001/offline-source-and-budget-receipt.md`（新简短匿名执行收据：两个命令真实退出码/测试数/失败数、测试版本与安全失败分支，官方源码证据/明确的未证实项，不写任何现实UID、私有path、媒体/题/答案/密钥）
4. `docs/codex-results.md`末尾只追加**一条**`### VLM-EGO4D-BOTO3-001`，链接源代码/测试/收据、真正执行次数及0AWS/S3/媒体/GPU。

严禁修改`docs/next-steps.md`、`docs/research-overview.md`、旧工具、旧Codex收据和历史程序/账本，禁止新依赖、AWS认证、云付费、私有文件扫描、外部联系或后台任务。预提交用`git diff --cached --name-only`核恰好四路径并检查无可回溯真实数据、没有高危网络调用；一次正常push main后**STOP**。若做不出离线可执行安全代码，就回报`ENGINEERING_BLOCKED`，不能用另一份静态规划替代代码，也不能开第二批。ChatGPT负责验收和后续真实AWS请求/下载授权。

**固定科学边界**：HourVideo开发元数据50视频/1182QA已验收**只属标注层**；真实同版媒体验证/物理长视频获取/S3凭据与限流仍`UNKNOWN/NOT_RUN`，`NOVELTY=RETAIN0`、Charades`FINAL_MEDIA_STOP`保持。Ego4D官方获批截止**2026-10-26**，本轮不得为了赶截止日期跳过门或直接下载。

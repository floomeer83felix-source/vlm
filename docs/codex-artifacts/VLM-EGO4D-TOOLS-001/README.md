# VLM-EGO4D-TOOLS-001｜Ego4D 官方工具就绪：先查现有环境，缺少才隔离安装，零媒体下载

**2026-10-12｜唯一受限 READY 父任务（用户明确回复「好的」，批准“检查并在必要时安装这些官方访问工具”）**。目的仅是解决[上一轮 SAFE_TOOL_MISSING](../VLM-EGO4D-MEDIA-001/limited-media-receipt.md)，交付能在同一 Windows 机器上复用的**官方 Ego4D CLI / AWS Python SDK 工具**及可核查的离线冒烟测试；**不是再执行旧下载任务**。由用户在**原同一个 Codex 长会话主动触发**；完成一次交付即停止。

## 一、唯一READY与访问界线

1. 首先在**独立公有Git文档checkout**执行安全`git status --short`、`git fetch origin main`、无冲突且工作区干净才fast-forward；重读`AGENTS.md`、`docs/next-steps.md`、`docs/research-overview.md`、`docs/codex-results.md`、本README、上轮[失败收据](../VLM-EGO4D-MEDIA-001/limited-media-receipt.md)、官方[Ego4D项目安装说明](https://github.com/facebookresearch/Ego4d/blob/main/README.md)、[官方CLI说明](https://github.com/facebookresearch/Ego4d/blob/main/ego4d/cli/README.md)、[AWS Boto3安装指南](https://docs.aws.amazon.com/boto3/latest/guide/quickstart.html)。仅当**唯一READY=VLM-EGO4D-TOOLS-001且`codex-results.md`没有本ID任何回报**才进入本机操作，否则STOP。旧`VLM-EGO4D-MEDIA-001`/REAL-PILOT/Charades已结案，**严禁重跑/复活**。
2. 用户的Ego4D访问许可**有效至2026-10-26**（用户本人提供审批通知）；本轮安装成功不证明访问凭据已就绪、UID对应/文件大小/真实许可用途门已过。**绝对禁止Ego4D/S3/HourVideo的HEAD、GET、LIST、API认证请求、数据manifest/字幕/视频/标注/权重下载、网页账号登录、任何真实QA/UID/原JSON读取；GPU/Qwen/SigLIP/ffprobe/媒体像素解码/训练=0。** 仅允许审阅公开官方工具文档和为包安装访问PyPI包索引/发行归档，原Git连接只作授权交接。
3. **严禁接触任何AWS密钥/Session Token、凭据文件原文、AWS_PROFILE、私人邮件或用户签署许可文件**；不枚举AWS profile、不调用`aws configure`、`sts get-caller-identity`、S3 client认证，不打印/导出私有路径、环境变量、用户名或账户信息。安装子进程尽量不继承AWS相关秘密环境变量；不改变AWS配置、系统PATH、证书校验/代理安全策略。若认证配置问题留待未来另批次且请用户**仅在其本机私下完成**，不向Codex或GitHub提供钥匙。
4. 禁止修改旧私有VLM原研究目录、`pytorch`环境、Conda/base/Python/Torch/CUDA/NVIDIA驱动、旧ledger/lock/`research_state.json`、原视频/HourVideo文件、Charades资产；不得另装GPU框架、AWS CLI v2系统级MSI、升级系统/开发工具、重置账户或杀进程。**本任务可创建的持久私有环境仅一个**，显式隔离、不写公有repo，不转存到GitHub。禁止新后台守护/调度与自动续作。

## 二、按顺序执行有限安全步骤

### A. 先做明确的只读工具发现

- 在当前shell只检查`aws`、`ego4d`可执行是否可发现（只公开YES/NO/版本）；用当前解释器`importlib.util.find_spec`与`importlib.metadata.version`检测`boto3`、`ego4d`，**不要导入torch，也不要实例化AWS Session/client**。
- 仅当本机已存在可正常调用的Conda，额外**只读**检查**唯一既知命名**环境`pytorch`中的这两个包（`conda run -n pytorch python -B -c ...`只查模块/发行包，不安装、不切换/升级、不激活其GPU）。若shell或已知环境已具备可用的官方访问工具组合，记录`EXISTING_TOOL_READY`并**停止安装**，只交匿名收据，不能因此启动AWS认证/GET。
- 不检查其它Conda环境，不递归搜索`Program Files`/硬盘，不打印exe绝对路径、全部pip list、AWS配置或全机安装日志。缺失是这些**精确环境**下的事实，不能概括为全机绝对缺失。

### B. 确实缺少时可创建**一个新的专用venv**

- 只可选择**已存在**且安全的Python **>=3.10**解释器创建`venv`，验证`include-system-site-packages=false`，**不绑定或写入原`pytorch` Conda环境**；若无法隔离、不存在支持版本、原盘余量不足则`ISOLATION_UNAVAILABLE` STOP。路径必须是**当前Windows登录用户下新且不存在的私人LocalAppData子目录**，例如专用`vlm-ego4d-tools-001`，绝不能在公有Git、Downloads、原实验工作树、已有环境或AWS凭据目录；不得覆盖已有目录/删除别人文件。
- 最多一个venv，缓存/下载暂存仅在此轮拥有的私人目录；可读版本/发行包元数据，不记录用户全路径。安装/测试过程不得连接任何AWS或Ego4D数据服务。使用该venv的**明确Python绝对可执行句柄**运行pip，不全局`pip`，不用`--user`或管理员权限；`pip --isolated`，仅官方`https://pypi.org/simple`及`files.pythonhosted.org`归档，强制TLS校验，`--no-input --disable-pip-version-check --no-cache-dir --retries 0`且合理超时、禁止VCS/git依赖、自定义索引/镜像、任意脚本下载执行及无界重试。不能安全使用官方PyPI就`PYPI_SOURCE_OR_TLS_STOP`。
- **资源上限**：本轮新获取的发行包/依赖归档**落地文件体积总和≤128MiB**，新增专用venv+临时文件总体**≤512MiB**，安装/测试CPU前台运行**总计≤20分钟**；达到边界立刻停，不擅自加包/扩额。注意pip网页请求/失败流量无法用归档大小精确推断：报告“落地包体积”，**不要冒称网络全GET字节受128MiB硬限制**。禁下载视频/模型/大型PyTorch依赖；若依赖图涉及`torch`、`tensorflow`、`opencv`、`av`、`pycocotools`或不相关机器学习软件，STOP而非安装。
- **第一优先**：在venv中从官方PyPI安装`boto3`及其标准必需依赖，采用明确锁定到本次记录的包版本、**优先仅可用的wheel**（`--only-binary=:all:`）、禁止源码编译/版本任意浮动；先读依赖元数据并约束包集合，再离线wheelhouse安装。基础可接受依赖只限`boto3/botocore/jmespath/s3transfer/python-dateutil/six/urllib3`及确实必须的`setuptools/wheel`；额外依赖须先停止提请审核。允许一次明确的下载安装尝试，不自动退回不可信镜像/HTTP/TLS禁验。实际版本与非敏感安装成功指标可公开。
- **第二优先，仅为Ego4D CLI所必需**：官方PyPI `ego4d==1.7.3` 当前发布为**只有source distribution**，其官方PyPI发布归档SHA256固定为`7689a8ff10b195d02697480c8ad0e6a863758399c6b185dcb9634f5171ee08c4`，在[PyPI发行记录](https://pypi.org/project/ego4d/1.7.3/)可核；绝不把它假称wheel。只有**先完整核实其官方发行来源及精确SHA、离线检查`setup.py`/build backend无附带网络/危险写操作、依赖限在官方项目`setup.py`的`boto3/tqdm/regex/dataclasses_json/iopath`及各自必需且能获可信wheel的轻量依赖**，且第一个SDK已就绪、总资源额度仍足够，才允许在**同一个独立venv**里用本机已验证的`setuptools`对这一个pin住的本地源码归档做**一次离线受限打包安装**（禁止自动构建隔离环境联网与其余sdist、未知setup动作）。只要不能证明上述源/依赖/打包安全，**立即标记`EGO4D_CLI_SOURCE_BUILD_HOLD`，保留已可用的boto3，不要硬装**。不以`pip install -r requirements.txt`全项目路径引入Tor​ch/CUDA；无系统AWS CLI升级/MSI。
- 如已现存`ego4d`可运行或其相同功能已验证，原则上不需要重复安装。安装Python包成功不会自动申请 AWS 服务调用或证书配置。

### C. 完成后仅**离线**验证

- 使用隔离Python运行`importlib.metadata.version('boto3')`、`import boto3, botocore`（关EC2 IMDS/远端查找，**只导入不建AWS Session/client**）；可通过静态检查提供`boto3.client('s3')`的**API签名可用性证明，但不能实际构造client或发网络请求**。
- 若Ego4D已安全安装，先静态确认CLI help不会隐式下载/认证，再执行**仅`--help`**或离线模拟解析标志，确认`full_scale`、`--video_uids`和`--no-metadata`参数在该版本实际存在；任何运行时副作用迹象，STOP且只保留静态证据。绝不可执行真实`ego4d --datasets ...`，即使带UID，也不得登录或验证私有AWS profile。
- 给出脱敏实测：现有工具是否找到、隔离venv是否成功、`boto3`是否可离线导入、`ego4d`是否可离线查看帮助、安装使用的发行源/包名/版本/官方SHA比对PASS/HOLD、发行包落地体积/新环境逻辑大小及CPU前台耗时的粗数量、无敏感路径/命令实际文本、`S3_GET/HEAD/LIST=0`、模型/GPU=0，以及未通过的门。没有下载媒体或验证AWS权限，不得写`MEDIA_READY`或`DOWNLOAD_GO`。

## 三、交付与停止

**公共Git改动仅限：**
1. 新建`docs/codex-artifacts/VLM-EGO4D-TOOLS-001/isolated-tool-readiness-receipt.md`：简洁匿名实际工具检查与安装/不安装证据，状态为`TOOLS_READY_OFFLINE`、`PARTIAL_BOTO3_READY`或真实阻塞原因（例如`ISOLATION_UNAVAILABLE`、`PYPI_SOURCE_OR_TLS_STOP`、`EGO4D_CLI_SOURCE_BUILD_HOLD`）；只能描述可复核的执行行为/版本/计数、不暴露凭据、私有路径、用户名、全盘设备身份、AWS profile、UID/QA/视频/缓存/程序日志或安装器原始stderr含token。
2. `docs/codex-results.md`**末尾只追加一条**`### VLM-EGO4D-TOOLS-001`，链接收据、实际状态/包数量/测试及**数据请求零**。不能改旧回报。

**严禁**修改`docs/next-steps.md`、`docs/research-overview.md`、`AGENTS.md`、本README、任何已有代码/实验文件；安装资产只能在本次私有venv，不得上传PyPI归档或源码、pip缓存/完整freeze、SSH密钥、视频。前次`VLM-EGO4D-MEDIA-001`结案不可重跑，即使新工具已PASS，也**不能把剩余2视频/8GiB权限自动转移**；媒体真实GET/UID join/签名URL/credential验证及GPU必须有用户**之后新一轮**明示批准。检查`git diff --cached --name-only`恰好上述两处与脱敏内容，正常向main**只push一次**后STOP，保留原Codex会话等待ChatGPT验收。Codex可交付安全负结果，不能在失败后继续其它安装源/第二环境/新任务。

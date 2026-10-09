# VLM-BATCH-014｜独立CPU ffprobe供应链校验、隔离部署与联网安全审查（10项）

**2026-10-09；当前父任务必须是`docs/next-steps.md`中唯一READY，且原Codex聊天收到用户明确“执行BATCH-014”。**
用户本轮**额外明确批准**：为已完成并阻塞的Charades V1试点准备可信CPU `ffprobe`，仅在`%LOCALAPPDATA%\VLM-Research-Isolated\CPU-Tools\ffprobe\`下**下载、校验、按白名单提取并执行`-version`健康检查**。不批准Charades视频/13GB大包、Range、联网媒体测试、packet PTS实测、画面解码/观看、GPU/模型、Conda/PATH/系统安装器或原RTX3090工作区更改。**013及013-FIX均历史已结束，不得重跑或改写**。本任务是工具部署安全门；即使工具READY，也**不**自动放行视频获取，新媒体父任务将另行审查代理安全与Python代码。

## 固定可信来源、版本与校验锚点（无“latest”漂移）

- [FFmpeg官方Windows预编译推荐](https://ffmpeg.org/download.html#build-windows)：FFmpeg项目**仅直接提供源代码**，在Windows预编译二进制上推荐Gyan.dev与BtbN。Gyan构建是**第三方打包的FFmpeg**，不可称FFmpeg项目直接发布或签名的Windows二进制。
- [Gyan.dev构建说明](https://www.gyan.dev/ffmpeg/builds/)发布`ffmpeg`、`ffprobe`、`ffplay`，静态x64 release essentials、GPLv3；当期9.0.2（2026-09），其release essentials ZIP在官网页面列为**约109 MB（十进制）**。不使用7z（禁止为7z安装新程序）、winget/choco/scoop/全局安装和其它镜像。
- **冻结真正包对象URL**：`https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-9.0.2-essentials_build.zip`；
  **发布方固定SHA256（来自同站`.sha256`，ChatGPT查看2026-10-09 Gyan官网相应链接）**：
  `60f467265b1e312373dbcd92200c2618a74850f98d3d078e94296bb3fa2047ba`；
  对应checksum URL：`https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-9.0.2-essentials_build.zip.sha256`。
  先从[发布方主页](https://www.gyan.dev/ffmpeg/builds/)核对`ffmpeg-release-essentials.zip`和`.sha256`当前重定向确实锁定**同一个9.0.2对象**，从固定checksum位置读取不超过4KiB文本并与任务书固定SHA逐字一致；若SHA、版本、URL、许可、大小改变或来源不确定，**STOP、不得把动态latest替换为别的包**。SHA来自同一构建者站点，不是独立第三方数字签名；不能宣称已证发布者身份高保证/无恶意软件，仅为发布方校验一致性。
- 包体仅允许HTTPS`www.gyan.dev`或严格一致的由官网显式确认的同站`packages`路径，**不允许跳到镜像/CDN/未列明域名、重定向、代理、禁TLS证书校验**。若服务器要求代理/重定向且不能确认符合这个要求，`BLOCKED_SOURCE`，先请ChatGPT审查，不绕过。
- **安装/download硬限**：包括页面/校验文本/ZIP与失败已读正文等本批累计工具HTTP响应正文**≤150MiB（157,286,400字节）**，单次ZIP正文流式≤150MiB；本批工具包+临时part+最终可执行文件+审计和许可留档**任意时点占用≤512MiB（536,870,912字节）**；本地独立卷空闲≥1GiB。最多**1次成功完整工具ZIP下载，失败额外尝试最多1次**且两次全部字节计入全局持久化ledger，不可重复下载“校验直到成功”。如果正式包大小/解压需超预算，STOP而不是增额。此次150MiB是**工具供应链流量专用**，绝不可挪为新增媒体流量/扩展Charades此前的64MiB媒体预算。
- 机器需Windows x86_64、Windows10+兼容，固定CPU工具根`%LOCALAPPDATA%\VLM-Research-Isolated\CPU-Tools\ffprobe\`，不写其它位置，包括OneDrive/Dropbox同步、公共Git checkout、原研究工作区、原Conda/RTX3090程序及其子父树。无reparse/junction/symlink/物理重合、无用户旧文件覆盖；任何信息UNKNOWN则STOP而不是修改原环境/切目录。

## 严格10项执行

**1. 独立文档仓库/用户权限重核**：安全只对公共Git docs checkout fast-forward main，重读`AGENTS.md`、`docs/next-steps.md`、`docs/codex-results.md`、本README、[原BATCH013阻塞报告](../VLM-BATCH-013/remote-range-and-privacy-receipt.md)与[独立FIX回报](../../codex-results.md)。仅当014唯一READY、尚无`### VLM-BATCH-014 ...`结果、独立checkout干净/无冲突时继续。若用户Windows不是x64或原ffprobe已经有明确独立安装资产，STOP，不能覆盖。
**2. Windows目标树和权限前置**：执行者从受信Windows上下文取得原科研工作区绝对路径用于只读重合排除（此绝对值**永不输出/上Git**），检查LOCALAPPDATA实际规范路径/已存在祖先的reparse和cloud roots、剩余≥1GiB和新目录可创建性；不触碰旧环境，失败`BLOCKED_STORAGE`、不联网下载工具。可只在新工具根做最小新文件创建测试，禁止改系统注册表/全局PATH。
**3. 来源/许可/发布方SHA证据**：在正式包字节下载前阅读FFmpeg官方Windows构建引用、Gyan官方release essentials固定9.0.2链接/文案、GPLv3使用与分发说明。允许将官网清楚标识的GPLv3 license/NOTICE文档保留在私有tool root，不向GitHub推二进制或整份第三方许可文本。检查固定`.sha256`与上面SHA一致；**该checksum只是同站供应链校验值，不是独立签名**。
**4. 纯合成安全逻辑先测**：使用现有Python3.9+标准库，先创建只处理虚构HTTP/ZIP流的独立安装工具及synthetic unittest，覆盖no-proxy、TLS/源域/重定向停止、HTTP大小缺失/欺骗、累计ledger写前提交/跨失败请求与限额、ZIP畸形/文件名转义/大小写碰撞/符号链接/ZIP64/加密/zipbomb/CRC、只允许唯一`ffprobe.exe`、已有目标不覆盖、SHA错拒绝、`-version`异常/超时、权限泄露。**至少12项合成用例全部PASS才允许真网络传输**，未通过STOP。
**5. 凭唯一固定发布包进行工具GET**：显式在`urllib.request` opener 设`ProxyHandler({})`+拒绝跳转，不继承环境或系统代理，不允许把HTTP降级/关闭证书验证；checksum/页面/包正文总量由单个持久账本记录，先HEAD读Size/Content-Type与对象最终host（若HEAD缺Size，改严格流式上限，但不冒险读取无限正文）。只有预检一致才进行1次有界GET，流式64KiB写入`incoming/.part`，每块先核全局字节预算，再写；失败最多独立重试1次（必须额外计入）。每次请求完成后核zip签名与固定SHA，再原子改名。无偷偷跳转或到GitHub/镜像请求。
**6. ZIP/白名单安全**：只用`zipfile`检中央目录安全路径、无特殊文件/symlink/绝对/..、无重复/casefold冲突、无加密、无超限/多级嵌套、成员数≤200、整体展开声明≤512MiB、只允许唯一正常`*/bin/ffprobe.exe`及可确实关联的LICENSE/NOTICE/README（不能执行任意源码/其他EXE/DLL）。验证ZIP所有成员CRC，若审计解压可能耗尽体积限制，STOP；静态build的ffprobe.exe单独运行版本命令，不把其它二进制释放到可执行路径。**若ffprobe.exe依赖额外打包DLL，不能在本批扩大白名单；标BLOCKED依赖并停止**。白名单逐成员提取采用“绝不覆写”原子写，只创建新根，不调用extractall/安装脚本。
**7. 本机ffprobe -version非媒体健康检查**：使用完整私人路径从唯一独立`bin/ffprobe.exe`执行一次`-version`，禁网络选项、0视频输入、timeout≤10s；核stdout包含合理`ffprobe version`、与官方9.0.2 release一致，返回0，记录版本与文件SHA、本次CPU/可执行文件签名状态（若系统工具可只读提供）；不把无签名误报“通过Authenticode”，不上传私人绝对路径。**不运行`-show_packets`、不访问任何Charades ZIP/CSV/MP4或原GPU目录**。
**8. 审查此前013-FIX网络客户端代理问题**：只对[现有Python媒体协调器](../../../prototypes/charades_range_media_clock_pilot.py)做**静态只读**风险说明：`urllib.request.build_opener(NoRedirect())`可能继承系统ProxyHandler。给下一独立Codex批的精确修复建议与合成反例（显式`ProxyHandler({})`、禁重定向、可审计直连），**本批不得修改013/FIX旧源码/测试，也不得媒体HTTP GET**。不因工具安装成功就解除原013 completed-parent guard。
**9. 收据/隐私/资源审查**：本地保留唯一ZIP SHA、来源/版本、返回字节/重试/文件占用/许可证与私有安装manifest/工具hash；公有报告只包含非身份性架构、发布者固定checksum验证状态、取包大小和执行-version结果、预算以及无原科研目录变化的“执行者收据”。不上传整个ZIP、ffprobe.exe、文档全文或Windows用户名、private path、系统软件清单、个人目录/运行日志。允许Git公开固定供应商包SHA，绝不上传私有视频或CSV。
**10. 交付三门决定**：`CPU_TOOL=AVAILABLE_VERIFIED_WITHIN_PUBLISHER_HASH_SCOPE / BLOCKED / UNKNOWN`，`MEDIA_NETWORK_CLIENT_PROXY=HOLD`（未经修复/复测不能GO），`V1_MEDIA_ACCESS=NOT_RUN`，`B/C_EVENT_TRUTH=HOLD`，创新retain0、GPU仍BLOCKED。测试PASS、包SHA和版本PASS也不自动执行旧013、启动视频下载或创造下一READY。供应链不满足就STOP并明示原因、0工具运行或经批准范围内的失败字节。
  
## 只允许5处新的公共GitHub交付

1. `docs/codex-artifacts/VLM-BATCH-014/tool-source-integrity-and-isolation.md`：FFmpeg→Gyan公开源链、版本/固定checksum/可核响应字节、GPLv3、隔离存储和验证收据/阻塞原因。
2. `docs/codex-artifacts/VLM-BATCH-014/ffprobe-readiness-and-proxy-hold.md`：是否真实部署且仅执行`-version`、CPU工具入口状态及旧媒体网络客户端代理漏洞的源码级审查，要求下一父任务独立安全测试；无媒体推理。
3. `prototypes/isolated_ffprobe_installer.py`：**独立**标准库固定来源、指定隔离目标、无代理、带SHA/大小/ZIP白名单预算和只执行`-version`的保守工具安装器；代码本身不接受任意URL/文件目标，默认仅预检，真正安装必须显式`--install`和014唯一READY/无父结果前置。
4. `prototypes/test_isolated_ffprobe_installer.py`：合成HTTP/ZIP/供应商checksum与本地路径反例，不访问真实网络，至少12项unittest。
5. `docs/codex-results.md`末尾**仅追加一条**`### VLM-BATCH-014 ...`，记录10项DONE/BLOCKED/UNKNOWN、合成test收据/是否真实部署/ZIP bytes/SHA/ffprobe版本、视频GET次数**0**、代理门HOLD、无GPU/原研究资产改动。

执行者只能正常`git add`上述5处、检查脱敏差异后单次commit/push，不能force push、改`docs/next-steps.md`、`docs/research-overview.md`、013旧代码、原ZIP/CSV、conda/PATH/锁、PR/Issue或非授权系统路径。任何权限/安装风险→不安装且仅提交脱敏BLOCKED报告和必要合成源码；提交后立刻停留原Codex聊天，等ChatGPT独立验收。**本README并不授权消费现有64MiB媒体预算。**

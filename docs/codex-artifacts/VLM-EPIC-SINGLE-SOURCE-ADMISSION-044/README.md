# 044：单个EPIC原片的真实获取与CPU时钟核验（待授权）

2026-10-24（北京时间）。**BLOCKED_PENDING_EXPLICIT_MEDIA_CPU_AUTHORIZATION / NOT_READY / NOT_RUN。**
父任务：VLM-EPIC-SINGLE-SOURCE-ADMISSION-044。先读[043负责人验收](../../research-decisions/post-043-fetch-repair-disposition-2026-10-24.md)。
本包将真实传输适配、必要预检、一次媒体获取和成功后的时钟扫描合并；不再分派纯假传输任务。
043已关闭；其PASS不是下载许可。用户此前的042许可已消费，本文件没有新HEAD/GET、解码或GPU许可。
负责人只有在用户明确批准本文件的新范围后，才将其及看板改为唯一READY。

## 1. 唯一对象与目的

[manifest.json](./manifest.json)原始UTF-8/LF SHA256：
`0f21ca3a765a5dd5ed264fca5147676d762b32f0dc4526db87b26153778b75c4`。
仅原16候选中的C02（rank2），不是新8源队列；REGISTERED_UNTESTED仅指素材未测，不代表执行授权。

| 项目 | 固定值 |
|---|---|
| video_id | P31_10 |
| 官方原MP4 | https://data.bris.ac.uk/datasets/3h91syskeag572hl6tvuovwv4d/videos/test/P31/P31_10.MP4 |
| 出版者MD5 | d400c28d06a4c4302312549a34008309 |
| 发布时长/分区 | 540.08955秒；55代原片、EPIC100 validation |
| 当前真实大小/时钟 | UNKNOWN / NOT_READ |

本次只判断此真实传输路径能否取得完整同版原片并给出实际显示时钟；不做模型问答，不评IoU。
C01维持042失败，旧11MiB及该GET≤4GiB责任不动；C03–C16保持NOT_RUN，不补源、不变6+2门或原16候选分母。
本包媒体上限是**新许可上限**，不使用旧预算，也不重试/续传C01。用单对象固定责任避开未验证的多对象分配器。

## 2. 新范围与硬上限（尚未授予）

| 项目 | 拟授权上限 |
|---|---|
| 应用HTTP | 上述唯一URL，≤1 HEAD及其通过后的≤1 GET；合计≤2次发送 |
| 媒体正文/磁盘 | 新GET累计≤4GiB（4294967296B），完整+partial合计≤4GiB；仅一个副本 |
| 获取包络 | 从传输准备之前一个monotonic起点；工作截止840秒，kill目标839.9秒，active0截止870秒，受控收尾截止900秒 |
| CPU准备/预检/验钟 | 累计受监督wall≤1200秒；完整原片扫描一次≤900秒；线程≤4 |
| 进程与父包 | 单worker；自有工作组RAM≤4GiB；父从首次本地执行起≤5400秒，包含实现、预检和报告 |
| 其他输出 | 新根媒体外≤64MiB/2048文件；公开交付≤16MiB；起步空闲≥4GiB+64MiB+2GiB |
| 禁止项 | 自动重试/跳转/Range/续传/镜像/批量获取、安装/环境更改、音频/图像输出、标注/问题/评分端点、processor/模型/GPU均0 |

900秒为总包络，工作与清理余量分列；不能在读阻塞时等worker finally再开始计时，任何超限如实失败，不改阈值凑PASS。
连接timeout≤15秒、单次read timeout≤30秒，并受剩余工作时长限制；不能代替独立监督。
未知网络/TLS缓冲不称精确线速统计：完整GET责任须在发送前预留；中断保留全额已登记责任，缺可信元数据时以4GiB上限保守记，不归零或复用。
服务返回新条款、登录门、鉴权/HTML、重定向、异常长度/编码即止，不接受新条款或换入口。只限既定非商业研究用途。

## 3. 前置与限定只读输入

按AGENTS安全同步独立文档checkout；重读AGENTS/看板/总览/results/本README并核唯一READY及无本父既报结果。
只读本manifest、043两新模块/回执/CSV、042公开代码及原片准入设计，040只准复用Job/Process平台；
不得运行040/042/043历史任务或tests、读取旧私有根/partial/日志/QA/帧或扫描磁盘找视频。
044本地新根固定为独立文档checkout同级新目录`vlm-private-044`，存在即STOP。
父链/新根非symlink/reparse、磁盘余量、既有CPU PyAV接口和Job监督均在媒体HTTP前检查；不安装工具/找旧未完工具包。

固定公开代码版本（核Git LF字节，允许无内容差异的checkout换行）：
- 043核心blob06a027564191f93c22767785aa2e7b755e6a20ed；验证器blob9aec0e1c19692b5ec7c4723aeb440446a6cf9eb0。
- 042核心blob62bc3ff492f07bcd4b872e17347311503f19f6c4，仅其mp4_clock/qualify/scan思想与可审查函数可复用为库能力，不能启动其旧fetch/supervise/suite。
- 040平台blob3e56faf30afea1bed850c085bceb2afcc4fb257c。旧文件不编辑。

## 4. 一包连续执行，按门自动停止

### A. 新真实传输适配与一次预检

新增`prototypes/single_source_admission_044.py`和其新tests，显式实现真实HTTPS传输及单对象生命周期。
043强制FakeTransport且额度很小，不能通过运行时替换类型/常量或取消guard伪装已验证生产路径；
新模块的实质差异、固定4GiB上限、已登记C02身份和源码SHA要封存。
可沿用043已审监督/写前状态原则，不改旧模块，不建新框架。
先用进程内网络拒绝守卫和注入connection/stream，在新代码的实际适配路径核六组关键风险：
1. exact URL/方法白名单、TLS证书/hostname校验及无retry/redirect/Range；
2. HEAD原始元数据与校验后长度/ETag持久化后才允许GET，持久化失败GET0；
3. GET长度/ETag/状态/编码异常或重复关键头拒绝body read；
4. 相同新核心的阻塞read受独立监督回收（短测沿用8/12/15秒，不跑旧矩阵）；
5. 完整小payload的双摘要、完整性/原子改名；摘要失败不准入；
6. 中断后独立回放保留长度/预留/未知缓冲，不重发、不自动下一个对象。
这是一次必要的新集成预检，不再重复043全部12矩阵或增加压力测试。最多一次有定位依据的实现修复回归，所有失败和耗时保留。
隔离守卫所在预检进程退出后，才可创建另外的本轮真实网络worker；不能尝试移除进程内审计钩子。
预检、CPU接口或资源监督任一失败：真实HEAD/GET0，独立可安全部分只作报告，结束父任务。
全部封存后才进入B，不需要每子步骤再问用户。

### B. 唯一真实HEAD及有条件GET

- 发送前持久化attempt claim和HEAD意图；TLS验证启用，只用给定hostname/path/443，禁隐式代理回退。
- HEAD必须200，有唯一可靠正Content-Length≤4GiB，identity编码且无transfer-encoding/条款异常。
  原始状态/头、长度、ETag（缺失亦显式）须持久化并可由监督者独立重建后，才登记GET完整责任和发送意图。
- 有strong ETag时GET使用If-Match；若无strong ETag，明确记录条件身份保证缺失，仍须核GET声明长度与已提供ETag一致，最终以出版者MD5验证原字节。
  不把weak或缺ETag写成原子版本绑定已证明，不为补ETag发第二次HEAD。
- GET须200且元数据一致，原始头先持久化，再流式读取；每块≤1MiB，累计请求/责任/读返回/落盘进展分开记。
  日志有事前事件/行长上限（≤20000事件、≤2048B/行），不得沿用043的256事件小测试上限。
- 流式算MD5及SHA256；完整长度、出版者MD5和摘要收据齐全后只原子改名，不复制原片。
  不匹配/短读/超时/监督或记账失败均不重传。监督的关键等待独立于worker磁盘/HTTP/报表I/O。
- active0后再回放日志与责任，真实状态/字节/期限全部保留。无法确认自有组退出就停止后续；禁止按不确定PID杀其他任务。
- HEAD不准入或GET失败，则C只记NOT_RUN并进入D。保持原候选和失败，不改文件/时长阈值救场。

### C. 成功原片的一次CPU显示时钟扫描

仅B完整验证通过才读取本轮新媒体。用既有PyAV CPU、单视频track、禁hwaccel/音频/像素输出。
记录实际解码显示顺序的整数PTS/duration/time_base、frame count、平均帧率有理数、原点和video edit-list；
不以DTS/packet到达序/best-effort或发布fps代替。逐帧数据只留本轮本地、流式记录。
原点/编辑、缺或逆序PTS、缺显示时长、间隙/重叠、边界不明都记CLOCK_UNKNOWN，不拟合/补时长。
可复用042已公开的相关函数为只读库，但新调用入口、文件归属及900秒监督须属于044，不能运行旧任务启动代码。
用原设计48个索引采样点的精确有理数ties-to-even舍入，计算d=max|i/actual_avg_fps−p_i|。
高偏移须真实非均匀PTS且d≥0.25秒；CFR须完整显示间隔在单tick量化内一致、显示边界相容且d≤0.02秒。
单源结果只报其类别/UNKNOWN，不按一个源报6+2准入、自然发生率或新发现。
不读动作标注、nongold问题、评分端点，不做processor/模型，标注同钟与题目身份继续HOLD。

### D. 一次统一回执并停止

明确区分PRECHECK_FAILED / FETCH_FAILED_OR_TIMEOUT / VERIFIED_MEDIA_CLOCK_UNKNOWN / SINGLE_SOURCE_CLOCK_MEASURED。
报告源码/配置、全部本轮HTTP意图与实际发送、完整元数据、MD5/SHA/字节精确性、保守责任、每阶段wall/真实kill/active0/finish、
Job CPU/内存、根内存储及新适配尚未覆盖的真实环境限制。共享计量只记一次，快照不叫卷级硬配额证明。
原16项分母与C01关闭保留；只更新C02，其余没有请求。失败不当科学阴性。
若真实获取再次超时/记账失败，判CURRENT_OFFICIAL_FETCH_ROUTE_STOP：暂停该直接获取入口，不自动加时、换候选试同一路径或发续传修复包。
下一选择应是用户确切已有合法文件或重新选择来源；不在本包访问它们。
即使成功，一个源也不自动放行其余媒体、64格实验、模型/GPU或投稿。

## 5. 执行者GitHub交付allowlist

仅新增：
- `prototypes/single_source_admission_044.py`
- `prototypes/test_single_source_admission_044.py`
- 本目录`single-source-admission-receipt.md`
- 本目录`single-source-summary.csv`（原C02一行，阶段失败/未知保留）
并仅在`docs/codex-results.md`末尾追加一条044父结果。

本README/manifest由负责人冻结，不改看板/总览/旧代码/旧收据，不上传视频、逐帧原表、标签或私人路径。
核stage严格上述五处，安全push main一次后STOP；已报completed/partial/blocked即消费，不自动045或迁移余量。

## 6. 授权与启动状态

当前仅负责人已准备此完整合同，**没有READY任务、没有新下载许可**。
需用户明确同意“044：唯一C02原视频，新媒体累计≤4GiB；下载总包络≤900秒，CPU准备/验钟≤1200秒；标签/模型/GPU0”后，
负责人同步授权记录、README与看板为唯一READY，再交本地Codex一次启动指令。
批准此范围只作用于本包，不追认旧失败下载，不接受任何新站点条款，不授权后台任务。

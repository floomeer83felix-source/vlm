# VLM-BATCH-018｜Charades 最后一次有界双视频 V1 媒体时钟试点（先双环境合成，至多一次 execute）

**2026-10-10｜唯一 READY 父任务须为 VLM-BATCH-018；用户刚明确回复“同意”再开一个全新一次性试点。** 这是**本路线最后一次**已授权的实际媒体时钟尝试；既有013至017均已结案，绝不改其历史、重新运行017或清除任何日志。Codex只在**原持续聊天**收到用户明确“执行唯一READY VLM-BATCH-018”后工作。ChatGPT目前只读GitHub，未登录用户Windows、未发Charades媒体HTTP；真实官方S3是否支持206、两个成员是否可在预算内取得、原CSV与视频PTS是否同钟，均UNKNOWN。

## 不可突破的边界

- **现有用户限定授权，不追加金额**：最多**2个**官方Charades 480p训练视频（先固定1个`0≤start<length<end, end-length∈(1,5]`越界案例+1个整行严格合法、尽量同等时长异subject对照）；研究用HTTP GET**所有实际正文与保守预扣总额≤64MiB＝67,108,864B**（含官方项目页/许可/ZIP尾部、ZIP64/中央目录、local header、两压缩成员、错误响应的已读字节）；GET次数**≤12**；全部本轮私有媒体+临时+审计占用**≤128MiB＝134,217,728B**；最多1个真实媒体HEAD，不扩权至其他URL。选择必先于看到远端成员大小，不能为了凑预算更换真实视频ID。
- **来源唯一**：只允许官网精确`https://prior.allenai.org/projects/charades`和许可`https://prior.allenai.org/projects/data/charades/license.txt`文本，以及指向的官方S3整档对象`https://ai2-public-datasets.s3-us-west-2.amazonaws.com/charades/Charades_v1_480.zip`的**安全按需Range**；这些地址并**不**授权下载整个约13GB媒体包。严禁镜像/代理/静默重定向/Range返回200全包时读正文、STA、原版55GB、新数据集下载、音视频观看/像素解码/截图、视觉事件人工重标、Qwen或其它模型/GPU/训练、Conda/PATH/原RTX3090科研工作区/私有锁及既有工具或元数据改动。
- **固定隔离**：只读`%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-Metadata\incoming\Charades.zip`、`extracted\Charades_v1_train.csv`与`extracted\Charades_v1_classes.txt`；内置固定SHA必须匹配。既有独立CPU工具在`%LOCALAPPDATA%\VLM-Research-Isolated\CPU-Tools\ffprobe\bin\ffprobe.exe`（BATCH015执行者报告9.0.2、发布方整ZIP SHA验证）；本批只核只读内容/私有部署收据，不再下载/重装。媒体**只**落至`%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-MediaPilot\`，之前017报告未创建；如今若发现任何未知文件/目录/账本/残留，STOP，不能覆盖、删除或换目录绕过。彻查Windows祖先reparse/junction/cloud sync与原科研树父子重合、磁盘空间≥512MiB，否则STOP。
- **预先冻结科学分门**：旧012`OFFICIAL_FRAME_LABEL=A_VERIFIED_WITHIN_012_SCOPE`；`B_TIME_RANGE_QUALITY=HOLD`；`C_P1/P2_EVENT_TRUTH=HOLD`；Charades不是天然长视频验证库，长域独立确认FAIL，创新`RETAIN0`，GPU BLOCKED。V1若成功仅证明这最多2例的媒体容器/video **packet** PTS与CSV`length`相对钟/末端关系，既不验证视觉动作实例也不能外推全部19,625条strict不通过记录。

## 冻结的10项顺序检查与不可重试入口

**1. Git/旧批与父任务唯一性（零媒体副作用）**：Codex在独立公有docs checkout安全fast-forward main，重读`AGENTS.md`、`docs/next-steps.md`、`docs/codex-results.md`、本README、[017阻塞收据](../VLM-BATCH-017/media-v1-access-and-budget-receipt.md)及[两臂科学报告](../VLM-BATCH-017/two-case-clock-and-science-decision.md)、016安全源码、015工具收据。检查**唯一 READY=018**、结果没有任何`### VLM-BATCH-018`，历史013–017全已结案；checkout脏/冲突/此前结果重复立即STOP。**严格程序父门须在ffprobe调用、创建真实媒体目录、真实SHA读取及所有外网请求之前通过**。不得重新使用旧`--parent-task VLM-BATCH-017`。

**2. 尽量不改科学程序的017→018授权迁移**：只允许修改`prototypes/charades_range_media_clock_pilot.py`与对应纯合成test；把`PARENT`严格改为`VLM-BATCH-018`；依原`authorize_parent`的**同一规范文本字节和SHA256算法**重算**本README完整合同**的`CONTRACT_SHA`，增加`VLM-BATCH-017`公开回报段落的`HISTORY_SHA`并继续冻结013–016历史报文SHA；所有结果条目核“已结案”且不允许任何未来历史回报漂移。不得靠mock替真实授权、只关键词匹配或硬编码虚假的通过值。只能解决必要的任务迁移/执行上下文mock隔离，不放宽`NET_LIMIT`/`GET_LIMIT`/`DISK_LIMIT`/fixed S3 URL/ZIP/CRC/类表/双臂抽选/容器时钟计算/源SHA。用户许可同017，只是新父任务ID，**不是新增媒体预算**。

**3. 先双环境完整合成（真实执行入口前的独立离线外部门）**：在**完全隔离的虚构临时路径与mock**下执行旧56个`unittest`方法，并针对014–017的原Windows PATH/reparse/Conda祖先检查、`VLM_ORIGINAL_WORKSPACE`污染、早期父门副作用0等**至少增加2个**反例。必须**先**在普通文档checkout CPU测试环境跑全集，再在**与后续唯一真实执行相同的相关环境变量上下文**下（不得把真实原科研路径暴露给mock）、用合成`LOCALAPPDATA`和工作区变量运行全集，最后在子进程中证明**内置`unittest.defaultTestLoader.loadTestsFromName`实际调用**在两种上下文都是同一测试数、全PASS、0ERROR/FAIL/SKIP。测试中真HTTP/工具/原本地CSV/媒体等访问均必须mock隔绝；如任何路径mock可能触及真实祖先`stat`，先修合成fixture，仅限测试代码，不能调整生产`check_ancestors`放行。若任何1项不通过，本批**只产出BLOCKED_SYNTHETIC_GATE**收据、**不得调用任何真实`--execute`**，也不“先发网络试试”。

**4. 唯一一次真实执行门（仅在3完全PASS后）**：**最多且恰好只尝试1次** `--execute --parent-task VLM-BATCH-018`，禁止自动重试/失败后再执行/改动生产逻辑就地续跑；程序内置合成门仍必须PASS，若不同环境造成失败也立即STOP。真实门先`authorize_parent`、再二次双上下文合成状态/合同一致性，随后才`fixed_preflight`（元数据SHA/路径身份/独立隔离/磁盘）、已部署工具私有回报SHA与路径、最多1次CPU`-version`；以上任何1项失败不触发HTTP，并在脱敏报告记录具体阶段，不能掩盖误报PASS。既有013/014/015/016/017父任务禁止重跑。

**5. 冻结原CSV私有双臂**：真实固定SHA train的`id,subject,actions,length`只读，先按旧确定性公式选择1越界+1整行合法近长对照且不同ID、优先异subject；在新私有MediaPilot内存/独占审计映射中冻结，不将任意真实ID、class、动作精确边界、subject、视频hash或绝对用户路径打印/提交。若合法样本无法取得或目录已有文件→STOP，不降阈值、不替换样本。
  
**6. 官网/官方S3安全访问**：此前服务器并未真实验证。用016唯一`build_media_opener`显式`ProxyHandler({})`、HTTPS证书校验及NoRedirect、固定官方URL/GET方法白名单；官网项目页与许可正文均计入原64MiB并在每次`response.read`之前用017`Ledger.reserve`先原子fsync持久保守扣除（实际bytes与charged分别记）；最多1个官方S3 HEAD须响应固定URL、身份、正长度、**强ETag**。所有ZIP尾部EOCD/ZIP64/中央目录、local header和压缩媒体仅精确`206 Content-Range`并固定If-Range/ETag/identity；如果200整包、301/302、弱ETag、源转移、ZIP目录难解析、成员缺失、总预算/GET12不足，**不读不必要正文立即STOP**，不换镜像/视频/官方源。
  
**7. 只按需两MP4文件**：必须先从官方ZIP中央目录安全定位2个预先选定成员，估算所有索引+成员下载正文与展开后本地预算，若不满足≤64MiB网络与≤128MiB盘，STOP不读取压缩成员。仅支持源代码既有ZIP安全结构/CRC与白名单、不得为了完成结果解除ZIP64/路径/重复/descriptor等安全拒绝；取得1段另一段失败也STOP，保留本批私有资产/ledger，不再重试。
  
**8. V1容器/packet PTS只读**：只允许此前隔离CPU`ffprobe.exe`读取至多2个已授权本地MP4，`-protocol_whitelist file`，`-select_streams v:0 -show_packets`限定，记录容器`duration/start_time`、stream`time_base`/rate/start、first/last video packet PTS/DTS/duration，与CSV`length`和选定越界end的关系；packet PTS不是精确已解码帧时间或事件真值，B帧/VFR/起点不可信时归`CLOCK_UNKNOWN`，不能使用视觉/音频帧、截图/模型或手工逐帧动作标注。只发布`CASE_OVERFLOW`和`CASE_CONTROL`的粗类别钟结果，不提供两视频私人ID、精确时长/PTS/end/class/subject。
  
**9. 双层资源/匿名审计与单次退出**：014/015工具GET预算、工具ZIP/私有账本不属本批研究HTTP且不得修改；MediaPilot研究GET新增正文与charged保守预扣分别汇总，两者均不得超64MiB，GET≤12，实际存储与1MiB审计余量≤128MiB，不能删除ledger后重来。若因媒体预检、连通性/206、ZIP结构、数量或预算失败，只给真实阶段`BLOCKED_<REASON>`和≤授权额的聚合事实，保留已写私有文件不移动到科研/Git目录；不公布ZIP成员名/视频ID/帧/音频/原CSV行/私有哈希/绝对路径/细PTS/请求令牌。
  
**10. 三层科学结论与止损**：分别判`SOURCE_SHA_AND_ISOLATION=PASS/NOT_RUN/BLOCKED`、`FFPROBE_VERSION=PASS/NOT_RUN/BLOCKED`、`MEDIA_ZIP_RANGE206=VERIFIED_FOR_SELECTED_MEMBERS/NOT_VERIFIED/BLOCKED`、`V1_CASE_OVERFLOW=.../UNKNOWN`、`V1_CASE_CONTROL=.../UNKNOWN`、`V1_CLOCK=CASE_LIMITED_.../UNKNOWN`；B/C时间/实例真值维持HOLD，Charades不可能因这2例升级为长视频验证，创新retain0/GPU BLOCKED。**失败或成功都一次STOP，绝不自动安排019或V2/GPU**；如果本最后机会仍未取得合法可靠的媒体钟，优先止损Charades视频获取路线，将其仅作短视频工程对照并重新评估真正长视频合法数据，而非默认再开019。

## GitHub仅5处白名单交付（匿名、可追溯）

1. `docs/codex-artifacts/VLM-BATCH-018/preflight-and-http-resource-receipt.md`：双环境完整套件各自用例数/执行上下文类别、真实父门、源SHA/工具/MediaPilot身份核验状态、官网/206/ZIP资源和预算实际/charged、一次真实机会/停止条件。
2. `docs/codex-artifacts/VLM-BATCH-018/two-case-pts-and-research-decision.md`：两臂仅类别化媒体PTS/CSV对照或NOT_RUN、样本级科学限制、停止/下一许可决定，不泄露私有媒体身份或精确PTS。
3. `prototypes/charades_range_media_clock_pilot.py`：**仅**最小018父任务与历史/合同哈希迁移、如必要的双上下文前置合成守卫，不改旧安全核心与时钟算法。
4. `prototypes/test_charades_range_media_clock_pilot.py`：原56项全部保留，必要的018父任务/mock环境防回归新增至少2项，**最终≥58项全PASS、0SKIP/FAIL/ERROR**（一份真实执行上下文集成门也需独立成功）。
5. `docs/codex-results.md`末尾只追加**1条`### VLM-BATCH-018 ...`**，按1—10报告完成/阻塞、真实GET/实际与预留正文、文件数、本机只读工具/PTS调用和A/B/C结论；只能提交脱敏数字与可复查的测试方法，禁止原媒体/ZIP/ffprobe EXE或旧账本。

Git只stage以上5处，`git diff --cached --name-only`核对后一个普通commit/push main（无force/PR/Issue/外部联系），不得改`docs/next-steps.md`/`docs/research-overview.md`、已结案013–017报告/README、原CSV/ZIP/原RTX3090 workspace/Conda/GPU/系统代理或私有工具树。若任何隐私/计量/目录身份不能证明，STOP并报告UNKNOWN，不进行未授权写入。本任务须在原Codex聊天**由用户显式触发一次**；本README与READY并不代表ChatGPT已经运行测试或下载任何视频。

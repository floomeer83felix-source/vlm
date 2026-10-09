# VLM-BATCH-013｜用户批准的 Charades 官方两视频 V1 时钟试点（10项，条件式）

**授权时间：2026-10-09｜执行入口以 `docs/next-steps.md` 中唯一 READY 父任务为准。**
用户已在方案A基础上**明确批准**一个有硬边界的媒体访问试点：**最多2个**来自 Charades 官网 480p ZIP 的视频成员；**全部远端HTTP响应正文累计≤64 MiB（67,108,864字节，包含central-directory/ZIP头/Range及任何错误响应已读的字节）**；**本地实际存储的媒体文件与所有本轮临时媒体字节累计≤128 MiB**；仅现有CPU能力读取**MP4容器、视频包时间戳与时间基准**，同本地已授权CSV的`length`、越界`end`进行数值核验。**不批准13GB整包、视频画面/音频内容人工观看或抽帧、视觉动作标注、Qwen/GPU/其他模型、原RTX3090科研目录/conda修改。** 这不是整库时间标准修复或任何P1/P2真值许可。

**用户须在原同一个Codex聊天显式指令“执行VLM-BATCH-013”才开始。** 从独立**公开文档Git checkout**安全fast-forward main，读`AGENTS.md`、`docs/next-steps.md`、`docs/codex-results.md`、本README、[Route A方案及许可](../../charades-media-boundary-pilot-proposal-2026-10-09.md)、[原元数据隔离协议](../../charades-metadata-safety-protocol-2026-10-09.md)、[BATCH012三层结果](../VLM-BATCH-012/three-tier-aggregate-and-go-no-go.md)。如果已有任何`### VLM-BATCH-013 ...`结果、多READY、文档checkout脏或无法安全fast-forward，**停止且不得传输视频**；不得重复旧批。

## 已冻结路径、预算及来源

- **原数据只读**：`%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-Metadata\incoming\Charades.zip` 与`extracted\Charades_v1_train.csv`、`extracted\Charades_v1_classes.txt`（必要时只读Test CSV做版本确认；不选择测试视频），ZIP SHA256`c616913ef79c2ddde06d9c562eae57bb8901d459d7568a0d27bf09cbf33ae866`、train SHA`59273c6dc2139ec7eb95b980fd26bc8529774b1ede0602f6ca90b546ed12f0fc`、类表SHA`7b95127e60300d6a69849d161869eb3e9657fa320fc9e92b6f2c9403b49c1887`必须吻合；否则`BLOCKED_SOURCE`，不恢复/修改/重新下载。
- **唯一新媒体落点**：`%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-MediaPilot\`，可使用`incoming/`存本轮`.part`、`media/`保管最多2个原MP4、`local-audit/`存本地选择映射/sha/PTS等敏感审计信息。新目录不得与元数据目录、公共Git checkout、原RTX3090实验目录、云同步根或这些目录的父子树重叠；所有祖先和目标必须验证物理身份、无symlink/junction/reparse、足够磁盘空间≥512MiB和权限；如未知、已存在陌生文件/路径或存在冲突，立即STOP。不得换目录绕过检查，不删除已有用户文件、不修改旧工作区。
- **唯一远端可获视频字节的候选**：[AllenAI Charades官网](https://prior.allenai.org/projects/charades)所列`Data (scaled to 480p, 13 GB)`对应的HTTPS S3整包`https://ai2-public-datasets.s3-us-west-2.amazonaws.com/charades/Charades_v1_480.zip`。**官网URL是整个档案，并非独立MP4下载许可或可行性的证明。** 执行前必须确认官网对应锚点仍为此对象，域名、协议和跳转目标严格一致；任何第三方镜像、视频服务、Google Drive、其他版本55GB/76GB/13GB全包直下都禁止。
- **双预算硬限**：累计任意GET响应正文≤67,108,864B；本轮所有媒体/临时下载文件磁盘占用≤134,217,728B；只允许总视频成员数≤2、任一视频目标和总量提前已知且不会溢出预算时才继续。所有请求计入**单个全局持久化本地ledger**，包括失败/已读错误正文、中央目录与元信息字节；无法可靠计数或ledger不可安全写入就STOP。远程每次请求须先判断状态/Content-Range/Content-Length，任何上限将被超过时不要读取正文。每次实际读取再做硬限，即使Content-Length错误也不能超限；网络重试计入预算、异常不通过更换对象/域名消解。

## 十项顺序任务（分层的可失败决策）

**1. 授权、源与存储预检**：对照用户最新的2段/64MiB/128MiB/CPU限定；安全核路径，原metadata SHA、既有媒体试点目录是否为空、磁盘≥512MiB；检查预存的`ffprobe`可执行文件是否已安装且非原科研conda/新增安装，仅记CPU/版本与可用性，不调用媒体。缺工具或路径不明则`BLOCKED`且不得网络尝试；**不要自行安装ffmpeg/7zip/pip/conda**。

**2. 冻结私有、可复现的2个候选**：从固定train CSV仅在本机以标准库读`id,subject,actions,length`及类表；越界臂：`0<=start<length<end`且`end-length∈(1,5]`、合法类别与数字；严格对照臂：整行所有动作`0<=start<end<=length`，近似匹配duration且优先不同subject。用固定公开算法（例如分类后以`SHA256('VLM-BATCH-013|' + video_id)`的十六进制顺序选择第一候选，明文ID不输出）确定，**必须在远端成员清单或时钟结果出现之前冻结，不得挑解释最容易的片段；不能满足最多两名及唯一映射则STOP。** ID与subject及匹配表只存在新媒体隔离目录的本地审计文件，不能将任何原ID/动作标签/video/subject/哈希ID传输到公共GitHub、对外API或模型。

**3. 官方源与最小Range先验**：仅做必要HEAD、确认总文件size和`Accept-Ranges`等；若HEAD不支持，不能仅凭标头声称支持206。先用**单个有界**HTTP Range GET取ZIP末端最多128KiB以探测EOCD/ZIP64，并验证`206 Partial Content`、`Content-Range`的总长/起止与实际正文一致、`Content-Encoding: identity`、域/ETag一致；**200 OK = 服务器试图回整包，读正文前立即STOP**。禁止未经授权的“下载一个视频试试”、匿名代理/镜像和全包重定向。最多12次HTTP Range GET（含所有探测/ZIP成员读取），实际次数与正文ledger必须可追溯；若无法实现无静默重定向且严格计数的请求器则STOP。

**4. ZIP索引安全核验**：从有界尾部读取End-of-Central-Directory、若必要ZIP64定位器/记录，只准**单档、非分卷、非加密且已被测试覆盖的ZIP结构**。要用Range获取必要的central directory，其成员名/offset/size/CRC、ZIP64 extra字段及本地文件头必须一致；验证ZIP成员数、声明size、路径遍历、大小写冲突、symlink、非普通文件、压缩法白名单、重叠偏移、CRC和不变的remote size/ETag。ZIP64、压缩数据描述符或任何结构无法被**可靠**安全解析时STOP，不因13GB来源而推测偏移；不下载整ZIP用于`zipfile`解析。只允许被选择的**准确2个**候选匹配唯一MP4成员，成员路径只留本地。若其中1个缺失、重名、大小不满足预算，**立即STOP**，不事后更换视频。

**5. 按需取两成员而非整个压缩包**：只在4全部PASS且总Compressed member bytes+必要头/Range开销不会超过剩余网络预算、Expanded MP4和临时文件不会超出128MiB本地限额后发出各成员数据Range，严格逐块GET计数与status206/range/ETag比对。只使用已有stdlib的有界`zlib`或`ZIP_STORED`安全处理明确支持的压缩格式，单文件CRC/大小核对后在新隔离目录内完成原子落盘、计算SHA。不解码视频像素/音频，不读取/保留另外的ZIP成员；路径泄漏/完整性/超预算立即STOP，无自动镜像/整包回退。发生部分失败时仅保留本试点创建的`.part`作用户后续决策，不能覆盖或删除已有资产，不做隐藏重试。

**6. CPU容器/PTS原始事实（V1，不看画面）**：仅调用既有`ffprobe`，禁网络选项/网络输入路径和外部依赖下载；只打开新隔离`media/*.mp4`，输出**容器/流元数据与视频packet时间信息**（`format.duration`/`start_time`、video`time_base`/`avg_frame_rate`/`r_frame_rate`/`start_time`、first/last packet PTS/DTS/duration）。只允许Packet demux或metadata，不执行全视频视觉帧解码、`-show_frames`、截图、图片输出、ffmpeg转码、人工观看、OCR、模型推理。没packet PTS或不可信末包时`PTS_UNKNOWN`，不能用`frame_index/FPS`伪造PTS。**末视频包PTS不必等于最后一个可显示帧时刻**，若涉及B帧/DTS重排或VFR须明确说明限制。

**7. 对照CSV的时间与版本语义**：仅本地私密表对比每个样本的CSV `length`与媒体duration/stream start/timebase、首末video-packet PTS（尽可能合理归一到同一媒体时间基；无充分原点信息则UNKNOWN），以及selected越界动作的`end`与媒体可表示末端的相对位置。公开**只允许类别化结论**如`CASE_OVERFLOW: LENGTH_APPROX_MATCH / LENGTH_DIFFERS / CLOCK_UNKNOWN`与`CASE_CONTROL`分类，禁止两视频的精确duration/PTS、视频ID/subject、动作类别/精确end或可链接组合。预先规定比较容差/时间刻度推导：容差来自视频流单帧名义时间或容器timebase与报告精度，并以本地公式记录；不可事后选择一个阈值让匹配成立。媒体`format duration`、video`stream duration`和packet末尾是不同对象，不能偷换。

**8. 科学解释与样本外推上限**：即使两样本时钟`MATCH`也只是在这2段中的media clock/CSV length数值匹配，**不**代表动作真实发生在end后、真实时序排序已验证，**不**能外推19,625条旧strict拒绝或347 P1组/97,723 P2 pairs；A官方frame label仍限域VERIFIED，B区间语义HOLD、C实例真值HOLD。若视频取不到，报告`ACCESS_BLOCKED`而非猜时间；如PTS不可信，报告`HOLD_TIMEBASE`。不生成negative/first/second问题或模型输入manifest。

**9. 网络、磁盘、隐私和合成测试的独立验收**：在任何视频Range GET之前，必须运行**纯合成**标准库单测覆盖：206 good/200 stop、Range错位/重定向/编码、累计硬预算跨请求与失败、ZIP64/EOCD/多盘/目录和本地头、ZIP traversal/symlink/重复ID、STORED/DEFLATE/CRC及zipbomb、只有2个精确成员、保护原目录、不发布ID/源文件路径/私有音视频、ffprobe脱敏。**未证明安全实现或合成测试失败，不能请求远程正文**。随后才允许1次限定试点，不能使用真实试点结果临时修改成员筛选或时钟容差再重试。新文件写入仅限用户授权的隔离目录；公共源码和报告不含服务账户/私有映射/视频字节。

**10. 三门裁决、停止及下一许可需求**：`A_OFFICIAL_FRAME_POLICY`沿012限域VERIFIED；`V1_MEDIA_ACCESS = CONFIRMED_SMALL_RANGE / BLOCKED / UNKNOWN`; `V1_CLOCK=CASE_LIMITED_MATCH / CASE_LIMITED_MISMATCH / UNKNOWN`; `B_TIME_BOUNDARY_QUALITY`与`C_EVENT_TRUTH`最多报告病例级线索，**不能凭V1全面PASS**；`LONGVIDEO=FAIL_AS_SOLE_DATASET`、`NOVELTY=RETAIN0`、`GPU=BLOCKED`。若2视频无法在64MiB/安全规则下获得，则`NO_GO_THIS_ACCESS_PATH`并STOP；不可默认请求整包/换源、自动BATCH014或私自扩大授权。需要画面与动作边界的V2，**另行明确向用户申请**。

## 允许的唯一5处GitHub交付

1. `docs/codex-artifacts/VLM-BATCH-013/remote-range-and-privacy-receipt.md`：匿名许可、隔离、Range/ZIP结构及资源计数、视频数、是否GET/ffprobe执行、失败原因；**不含URL查询令牌、视频ID、媒体精确fingerprint/文件名、真实子目录或极细分量**。
2. `docs/codex-artifacts/VLM-BATCH-013/clock-case-control-and-science-decision.md`：仅上文类别化CASE_OVERFLOW/CASE_CONTROL时钟结果、时间坐标合同、证据限制、科学决策；不要发表两视频的精确长度/动作边界。
3. `prototypes/charades_range_media_clock_pilot.py`：标准库的受限官方HTTPS Range只获取两指定成员和固定隔离来源的CPU ffprobe协调器；不接受自定义源URL/目录、不能抓第三方或下载整档案，不需要安装包；不上传任何本地敏感映射。
4. `prototypes/test_charades_range_media_clock_pilot.py`：仅虚构ZIP/HTTP响应/时间戳的unittest，至少12个反例；不得连接实际服务器或使用真实视频。
5. `docs/codex-results.md`末尾仅追加一条`### VLM-BATCH-013 ...`父报告，任务1—10状态/官方联网次数和响应正文字节总量、最高本地占用、最终保存视频数量、单测收据、不可行停止原因、V1/A/B/C分层判定与0GPU/0原科研目录改动。

仅stage这5处，仔细审查所有文件/日志/traceback，确保没有真实视频/帧、CSV行、subject/video ID、精确私有PTS/时长、用户名绝对路径、外网非官方服务或底层私有ZIP成员映射；`git diff --cached --name-only`确认。若无法在不写入数据或隐私的情况下完成报告，STOP/仅交匿名BLOCKED收据。单次普通commit/push，禁止force-push/PR/Issue/外部联系；推送后立刻停止，保留原Codex聊天。

**重复强调**：此前没有媒体下载是历史；本轮用户新授权**仅**已定义的≤2官方480p MP4、总GET≤64MiB/本地媒体≤128MiB、CPU容器/Packet-PTS读取，**没有**13GB zip全包、模型/GPU、可视动作边界判断、STA或更换数据集、旧RTX3090原代码/conda/torch/CUDA/锁/账本编辑、上传数据的权限。

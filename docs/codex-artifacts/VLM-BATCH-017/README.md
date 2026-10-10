# VLM-BATCH-017｜Charades 2段官方480p视频的有界V1媒体时钟试点（先补齐安全门，再至多一次真实执行）

**2026-10-10。只在`docs/next-steps.md`中唯一`VLM-BATCH-017=READY`且用户在**原持续Codex聊天**明确指令时执行。** 旧父任务013、013-FIX、014、015、016均已提交且结案，绝不重新运行或补写旧结果。这是**全新父任务**。用户先前已明确独立批准有条件的真实V1试点：**仅最多2段Charades官方480p视频，全部媒体研究GET正文（包括官网项目页及许可文本、ZIP索引、HEAD后Range、失败已读与保守预留）累计≤64MiB=67,108,864 B，本轮全部本地媒体/临时/敏感审计总占用≤128MiB=134,217,728 B，仅既有CPU ffprobe容器与video packet PTS**。无需额外申请工具安装；BATCH015报告现有CPU ffprobe 9.0.2已在指定隔离目录安装并经发布方ZIP SHA/CRC/version健康检查，**本任务仍须核本机固定路径和版本，但无任何工具/Gyan下载**。

**严禁**13GB整包下载或55GB原版、任意非官方镜像/代理、其它数据/STA/帧或音频观看/解码/截图/视觉人工标注、模型/GPU/Conda/PATH/原RTX3090工作区/锁/manifest/老数据/老任务脚本外的更改。BATCH016已完成的`ProxyHandler({})`、严格TLS/NoRedirect与URL白名单保留；`CODE_LEVEL_VERIFIED`不等于真实服务器`206`已知。**只允许一个条件式媒体机会，不能为取得两视频反复变更规则或扩大许可。**

## 科学与工程的现有硬证据

- [BATCH012](../VLM-BATCH-012/three-tier-aggregate-and-go-no-go.md)：仅官方frame label 25点采样口径限域`VERIFIED`。CSV `0≤start<end≤length`属于额外区间质量规则，旧19,625不通过不是19,625已证坏标注；B原边界质量、C P1/P2物理/语义实例真值仍HOLD，创新retain0，Charades约30秒不能单独支持自然长视频论文。
- [BATCH013](../VLM-BATCH-013/README.md)已安全停止于缺既有ffprobe时（0视频）；[BATCH015](../VLM-BATCH-015/resume-integrity-install-and-science-decision.md)合法隔离取得工具；[BATCH016](../VLM-BATCH-016/media-http-proxy-threat-and-fix.md)以40项纯合成PASS（执行者报告）修复媒体HTTP默认系统代理继承，但仍保留媒体下载账本**响应`read`后才`add`**、默认`run_pilot`先跑`ffprobe -version`才检查新父授权、以及`authorize_parent`仅关键字式许可证合同检查的风险；这些必须**在任何真实研究HTTP之前**离线补强。
- 原唯一官方媒体候选：从[AllenAI官网项目页](https://prior.allenai.org/projects/charades)严格锚点对应`https://ai2-public-datasets.s3-us-west-2.amazonaws.com/charades/Charades_v1_480.zip`（官方480p约13GB整ZIP，**不是**允许整档传输）；[官方license](https://prior.allenai.org/projects/data/charades/license.txt)。实际源HEAD的强ETag、Content-Length、206/ZIP64/member可取性**此前未被证实**；Gyan工具包Range成功**不等于Charades媒体源支持206**。
- 元数据只读固定Windows路径：`%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-Metadata\incoming\Charades.zip`及`extracted\Charades_v1_train.csv`、`Charades_v1_classes.txt`；既有SHA由`SOURCE_SHA`在媒体协调器固定并在本轮运行前核；只能选**train**，不能下载/test/STA。新媒体只能在`%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-MediaPilot\`，与metadata/CPU工具/原科研工作区/Git checkout/云同步根物理隔离，无reparse/junction/symlink，必须**新且空目录**，未知STOP。

## 10项、明确的顺序与失败退出点

**1. 安全Git/任务许可门**：在独立公共文档checkout安全fast-forward main，重读`AGENTS.md`、任务板、codex-results、本017 README、013原许可、015工具收据与016禁代理源码。必须**唯一READY=VLM-BATCH-017、结果里无`### VLM-BATCH-017`，历史013/014/015/016已结案**；checkout脏、源冲突、重复parent、任何权限不明→STOP。**在进入任何ffprobe调用、创建目录或联网前先执行并通过任务门**。原`run_pilot(execute=False)`默认只是预检，不构成执行许可；此次只有显式新`--parent-task VLM-BATCH-017 --execute`并通过许可才可真正运行。
**2. 先修两处失败安全逻辑，不放宽媒体规则**：仅编辑现有`prototypes/charades_range_media_clock_pilot.py`与现有合成测试。把原`Ledger`改为每个最多64KiB网络`read(n)`前**先原子保存并fsync不可撤销的保守已计费reserve(n)**，真实read后再登记actual receipt、遇短读/异常只保留已预留账额，不重置，记录实际与保守计费为不同字段；所有官网页面/许可文本GET以及S3 Range共用单一额度≤64MiB，任何前置创建失败/ledger写失败就在请求或读取正文前STOP；总GET≤12，任何自动GET重试0。故障后存在残留`.next`/私有账本即拒绝整个017重复执行，不能删除后重启。确保错误200整包/416/重定向在正文**0读入**即STOP。修正入口顺序为**先父任务与授予作用域核验**，再允许`ffprobe -version`、目录操作；严格读取**只属于017的冻结README及014/015/016结果状态和具体数值**，不得靠旧“64/128/ffprobe”三个关键词证明用户授权，不能接受非017任意`--parent-task`。保留现有安全`ProxyHandler({})`、默认TLS、NoRedirect与固定官方HTTPS请求路径。
**3. 合成测试前置（真实GET、ffprobe、原Windows资产都不允许）**：旧40个合成测试方法**全部保留**，新增至少12项覆盖：无父任务/完成旧父/旧README关键词伪冒时版本调用0；旧013不能重跑；授权门/时钟工具路径检测早于来源网络；网络GET read前预扣+持久fsync；crash/超时短读/错误响应的预扣不回收及跨两个请求持续累积；64MiB总预算含文档文本与ZIP数据；text encoding/Range无200正文读取；系统代理污染仍零代理发现；ZIP尾端/ZIP64不支持即STOP；13GB直接GET拒绝；两媒体成员精确身份/存储预算及原CPU包/旧元数据不碰；源锚/强ETag/源总长变化拒绝；媒体身份/精确PTS不写Git；测试套件**≥52项全PASS、0FAIL/ERROR/SKIP**且完整纯合成。除合成构造必要文件外不触碰用户真实媒体/ZIP/Windows工作区；若新修测试不过就STOP，不能使用现场媒体响应改策略后重试。
**4. 本机执行门和媒体隔离预检**：测试PASS之后才允许`--execute --parent-task VLM-BATCH-017`进入实地门；确认固定元数据ZIP/train/classes完整SHA与源隔离路径身份、原科研根排除、Win云同步/祖先无reparse、同盘空闲≥512MiB、新媒体根不存在且不在任何旧受限树内、CPU ffprobe位于015私有bin，`-version`只运行一次并退出0。若缺环境变量/原工作区无法确定/发现其它`ffprobe`优先于已验收独立工具，则STOP，不换到Conda/全局或安装工具。**没有通过这些前置就0官方HTTP。**
**5. 冻结两个本地私有视频候选**：从已固定SHA train CSV基于预先冻结算法只读选：一例`0≤start<length<end, end-length∈(1,5]`（数值合法越界）、一例整行严格合法、尽量匹配长度/异subject，且文件ID唯一。先确定选择与本地隐私记录，才请求官方媒体目录；不能看实际服务器有哪些文件后改选“容易下载”的两个，更不得泄露原视频/subject ID、实例class、候选hash ID、精确end或本地路径到GitHub。
**6. 仅必要的官方GET/HEAD与ZIP索引**：用单个禁代理TLS客户端，项目页/官方许可精确地址GET要计入整个**64MiB媒体研究GET**（不是另批），最多1 ZIP HEAD，确认唯一官方480p归档链接、许可文本完整性、远端`Content-Length`与**强引号ETag**，身份不明STOP。随后只按需用`206 Content-Range`、`If-Range`进行ZIP尾部EOCD/ZIP64/单盘中央目录/唯一两成员local header+body Range。拒绝HTTP200整ZIP、301/302、域/大小/ETag漂移、ZIP64不支持、数据描述符/成员不唯一、CRC/文件展开预算或网络GET次数超过12。**先验计算完整两个压缩成员+索引+已用GET后剩余余额**，不够就STOP并不碰媒体成员。**若服务器无法在64MiB内返回确定目标成员，不能换镜像或下载13GB。**
**7. 最多两视频受控落盘**：仅取固定目标成员最多2个、总媒体私有目录/临时/账本≤128MiB；只读ZIP/成员CRC和大小通过，再在独立新`media/`保存MP4；不得新增解码工具、远程模型、ffmpeg转码、截图、外传媒体/子ID/音频。若只取得1段或出现任何损坏/中断，按BLOCKED保留已有私有资产及账本，**不自动重试、也不对外展示例子**。
**8. V1仅容器与video packet-PTS对照**：用现有CPU ffprobe`-protocol_whitelist file`、`-show_packets`且仅v:0，读取两MP4的容器duration/start、视频stream time_base/fps/start、video packet PTS/DTS/duration，不调用`-show_frames`、像素解码/观看或人工动作核对。和CSV`length`及一个预冻结异常`end`做本地时间尺度对照；packet/封装时长不等于物理动作结束时刻，B帧/VFR/时间原点未知时`CLOCK_UNKNOWN`，不得现场改容差/训练模型/生成first-second问题。仅本地私有目录保存精确PTS/视频身份，公共文档只能出两臂大类标签。
**9. 审计与资源、脱敏红队**：旧014/015工具ZIP与账本只读且绝不计入本媒体64MiB预算；此次私有新账本记录GET请求和实际/预留计费全链条、响应状态、磁盘峰值、视频数和失败原因，任何中断都不可重置；公网Git只准发布宏观总正文/保守已计/尝试次数/视频数、CASE_OVERFLOW和CASE_CONTROL粗类别，不发个体精确长度/PTS/视频ID/hash/subject/class/原CSV行、视频/音频/帧、整个官方脚本、系统代理/本机路径。没有第二次运行自动恢复权。
**10. 科学分门和STOP**：分别给`MEDIA_RANGE_206=VERIFIED_FOR_CASES/UNKNOWN/BLOCKED`、`V1_CLOCK=CASE_LIMITED_MATCH/DIFFERS/UNKNOWN`、`B_TIME_RANGE_QUALITY`与`C_P1/P2_EVENT_TRUTH`继续HOLD，`OFFICIAL_FRAME_LABEL=A_VERIFIED_WITHIN_012_SCOPE`、`NOVELTY=RETAIN0`、`LONGVIDEO=FAIL_AS_SOLE_DATASET`、`GPU=BLOCKED`。即使2例成功，不能推广全9,848视频或原19,625 strict拒绝动作；不能凭CPU packet PTS确认事件边界语义。成功/阻塞都只产生一次新的017结果并STOP，不自动开018/视觉V2许可。

## 仅准5处公开GitHub交付（含前置安全代码修复及真实试点收据）

1. `docs/codex-artifacts/VLM-BATCH-017/media-v1-access-and-budget-receipt.md`：唯官方固定对象HEAD/GET/206及索引/ZIP64/CRC/限额收据、原Windows隔离路径身份是否通过、预留/实际计费/停止原因，只给聚合脱敏指标。
2. `docs/codex-artifacts/VLM-BATCH-017/two-case-clock-and-science-decision.md`：CASE_OVERFLOW/CASE_CONTROL媒体时钟粗类别或`NOT_RUN`，A/B/C门与样本局限，不提供具体两段识别符/精确PTS/动作数据。
3. `prototypes/charades_range_media_clock_pilot.py`：仅在现有协调器修安全父门/ledger预扣、保持先前BATCH016固定源无代理，禁止任何媒体/数据规则扩权。
4. `prototypes/test_charades_range_media_clock_pilot.py`：旧40个方法保留+≥12项纯虚构回归，最终≥52 PASS先于真GET。
5. `docs/codex-results.md`**尾部追加恰好一条**`### VLM-BATCH-017 ...`，分10项状态+CPU suite/请求/实际+保守计费、最高本地占用、保存媒体数、一次`ffprobe-version`及0GPU/0原实验改动。

仅stage五处且diff彻查内容脱敏后单次普通commit/push main；不能force push/PR、修改`docs/next-steps.md`和`docs/research-overview.md`、013～016历史文件/结果、元数据/工具ZIP、原Windows RTX3090环境或云同步。若任一安全门无法满足就上传合法匿名`BLOCKED`收据、保留私有账本/已产生资产，不准后台继续或删旧数据；执行者在原Codex聊天一次回报后等ChatGPT科学审查。

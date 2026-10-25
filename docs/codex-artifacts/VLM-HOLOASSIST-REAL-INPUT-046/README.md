# 046：一个HoloAssist分发副本的获取、真实CPU时钟与B0/P/N输入（已授权执行合同）

2026-10-25（北京时间）。**READY / USER_APPROVED_MEDIA_AND_CPU_INPUT / NOT_YET_EXECUTED。**
父任务：VLM-HOLOASSIST-REAL-INPUT-046。用户对已冻结完整提案明确回复“批准”，新媒体获取和限定CPU解码/输入范围已获授权。
最新任务板将本父设为唯一READY；本地Codex安全同步main，确认本父无既报结果后，一次连续完成本合同允许的A→B→C→D。
各阶段按门自动继续或停止，不需要再次确认本范围；授权记录和启动消息见第6节。
本包绑定一个确切新资产；不恢复042–045、不扩纯受控夹具，不修改已安装环境。

## 1. 对象、目的及已知边界

[manifest.json](./manifest.json)原始UTF-8/LF SHA256：
`d79a7eeb7ec57e95c4c1c60418db12b794f14736891ed3046fd58712fed63ef9`。
资产状态REGISTERED_UNTESTED仅指未测；授权以本README和最新任务板为准。

| 项目 | 固定内容 |
|---|---|
| 唯一候选H01 | HoloAssist / R015-7July-Switch |
| 分发者及版本 | lmms-lab/EgoIT-99K，dabc7958c501ce7cb7a0e6082e41ffdee547a1b7 |
| 路径 | HoloAssist/video/R015-7July-Switch.mp4 |
| 已公开LFS大小 | 114523050B，约109.22MiB |
| 已公开LFS SHA256 | 8ee70b404c996a1c823b65744debc9763564ac6bb5e57835f15be8c07d3bac98 |
| 实际时长、逐帧PTS、是否高漂移 | UNKNOWN，完整获取后一次核查 |
| 与HoloAssist原发布字节/时钟相同 | UNKNOWN，不能仅凭文件名或该LFS摘要认证 |
| 标注时钟、已有可识别区间问题 | UNKNOWN，本包不读取标签或QA |

确切URL见manifest，必须用完整commit而非main。出处、许可及111秒小样例的否决见
[负责人来源说明](../../research-decisions/holoassist-single-copy-entry-proposal-2026-10-25.md)。
此为首次可见目录项的固定可得性候选，不是随机自然视频样本；未按漂移或模型成绩选源。
上游明确声明CDLA-Permissive-2.0；分发副本尚无已核同版证明。本包只取得并诊断该公开分发副本，
**不以其替换已冻结EPIC16候选或宣称原片、标签桥接、6+2、64格或论文资格已通过**。

目标是顺序关闭：完整分发文件可得性 → 实际视频显示时钟 → 若满足180–900秒且自然高漂移，
在此确切资产上实现实际F/T的PTS适配和已有均匀时间采样N，构建三个真实CPU输入。
只做“Describe the video.”输入，不生成答案；任务效果继续UNKNOWN。

## 2. 已授权上限

| 资源 | 上限 |
|---|---|
| HTTP | 固定resolve URL一次HEAD；一次GET链，最多2次302/307跳转；总发送≤4（HEAD1+GET3） |
| 新媒体正文及磁盘 | 累计≤128MiB=134217728B；预期正文114523050B；partial/完整仅同一个副本，原子改名 |
| 获取独立包络 | 工作840秒、kill目标839.9秒、active0≤870秒、受控收尾≤900秒；所有跳转共用同一起点 |
| CPU | 准备/预检/解码/processor累计受监督wall≤1800秒；全帧验钟≤600秒，取帧解码≤600秒，processor worker≤300秒 |
| 进程/内存 | 单阶段单worker，自有Job RAM≤4GiB、线程≤4；父从首次本地执行起≤5400秒 |
| 媒体CPU读取 | 最多2次完整顺序解码；Python可计量read返回累计≤512MiB，含容器元数据；不冒称OS物理I/O |
| processor | 一次配置加载；实际调用总≤5（必要探针≤2+正式B0/P/N各一次）；正式不重跑 |
| 输出 | 新根媒体外≤64MiB/1024文件，公开附件≤16MiB；首输出前空闲≥128MiB+64MiB+2GiB |

禁止重试、断点/Range、SDK自动下载/Xet分块客户端、并发、其它媒体、其它站点回退、安装、改环境、
音频解码、像素/音频导出、标签/问题/评分读取、权重加载、AutoModel、forward/generate、CUDA/GPU及训练。
达到任一上限、所有权/元数据不明即停止，保留失败和剩余NOT_RUN；不移用旧额度。

## 3. 前置、只读范围及实现封存

按AGENTS安全同步独立文档checkout，核本父唯一READY且results无既报；否则STOP。
新私有根固定为文档checkout同级`vlm-private-046`，存在即STOP，不扫描其它目录寻找替代位置。
核父链/新根无reparse/symlink、空间、现有pytorch环境与Job监督；不读旧私有根、partial、日志、runtime、
旧帧/QA/gold/预测/账本或运行旧任务/tests。

允许只读本提案/manifest、关联设计、下列公共源码和相应公开回执：
- 040 Job/Process平台blob3e56faf30afea1bed850c085bceb2afcc4fb257c，仅平台类作库，不运行040工作。
- 042核心blob62bc3ff492f07bcd4b872e17347311503f19f6c4，仅容器元数据/有理数时钟逻辑参考。
- 044核心blobc8267b25e6b2ad3d4be94d5348c1aafd09a3f10e，仅TLS/写前账本/独立监督参考。
- 045核心blob680aa191f801d8429adfda0a11620919ac7e1ad8，仅请求隔离/原生CPU边界逻辑参考。
旧源码不编辑、不改运行时常量/guard绕过硬编码URL或F96/T96；新增本轮实现，参数绑定本轮核验的真实H01。

现有PyAV15.1.0 CPU API/二进制仅精确文件核验，不安装替代解码器。
processor/tokenizer只限当前本地Codex聊天已明确的045同一既有精确目录；不得读取045私有runtime找回它、
猜父目录或递归搜盘。入口遗失则输入部分NOT_RUN，不阻塞可独立完成的获取/验钟。
限定配置/tokenizer与CPU Torch2.5.1、Transformers4.57.6、NumPy1.26.4及既有Pillow；不读权重正文。
明确API源码核验≤8个精确依赖文件/累计8MiB，不查无关安装目录。
目标原生processor Git blob17bdd975eef337371aa763824edc7e6ec1987dbf，SHA256
efd8d64aaf608aad1ffb3e6d503d6a99e5227d007df95c1d9fa905d998cda4a9。

新增`prototypes/holoassist_real_input_046.py`及对应tests，整个包只做一次必要集成预检：
精确对象/摘要、HEAD写前责任、受限跳转、TLS/身份/长度/编码异常、短读/错误摘要拒绝、
短8/12/15秒阻塞read监督、CPU严格时钟/N区间归属、动态F/T绑定与请求隔离。
用注入transport和小型数学fixture，网络拒绝；不跑043完整矩阵，不创建额外研究变体。
suite≤60秒，最多一次有定位证据的代码修复与≤60秒回归；保留全部失败。正式媒体或processor失败不重跑。
guard所在预检worker退出后另建真实网络worker，不能卸载审计hook。

## 4. 同包连续执行

### A. 一次受限获取

发送前持久化独占claim、HEAD意图；所有HTTP使用验证证书/hostname的HTTPS/443，无代理回退、
Cookie/账号凭据/Authorization或用户登录。初始host/path严格匹配manifest。

HEAD只向固定resolve URL发一次，不跟跳转。允许：
- 200，唯一Content-Length恰114523050B；若有linked摘要/大小必须一致；
- 302/307，唯一X-Linked-Size恰114523050B、X-Linked-ETag去引号后恰已登记LFS SHA256。
其它/缺失/重复关键头、HTML、登录/条款、编码异常即STOP，GET0。
HEAD原始状态/头和校验结果持久化后，预留完整114523050B责任，才登记GET意图。

GET从同一固定URL开始，最多2次302/307、共≤3次发送；每跳发送前持久化意图/剩余计数。
只跟响应提供的HTTPS绝对Location，host必须在manifest精确白名单，无userinfo/fragment/非443端口；
不接受301/303、越界host、登录/鉴权路径、重复Location、循环或手工改写链接。
HEAD的Location不直接当GET入口；不同host的ETag不互相冒充版本锁。
签名query只留本轮私有头收据，不复制到公开附件/命令日志；公开只给host、状态、跳数和URL摘要。
跳转response不读正文，及时关闭。未知重定向即失败，不增白名单救场。

最终GET须200、identity、无transfer-encoding，唯一Content-Length恰114523050B；
若返回linked元数据也必须匹配；最终ETag与HEAD所指对象是否可比较分别记录。
原始头先持久化再流式读，每块≤1MiB，持续计量read-return/写盘/责任，完整后必须精确长度及SHA256均匹配才原子改名。
固定commit+最终摘要为本分发版本完整性依据，不能把Xet hash或不同host ETag当LFS SHA256。
断连、短读、摘要错误、磁盘/日志失败或超时均不重发；中断未知缓冲不报0，保留全额责任。

连接timeout≤15秒、read≤30秒且不超过剩余工作时长。独立监督关键等待不依赖worker HTTP/磁盘/报表/finally。
每个原始header文件≤64KiB；账本≤20000事件、≤2048B/事件，事件只放摘要而非长签名URL。
active0后独立回放发送/元数据/字节及责任；不能确认自有组退出则停止，不清理其它任务。
失败则B/C均NOT_RUN，仍交完整回执；此路线失败不再自动产生下载修复或换源任务。

### B. 唯一文件的一次CPU显示时钟扫描

仅A完整校验通过后，用PyAV纯CPU、禁hwaccel、仅video=0，最多一次全帧解码；
计量文件read返回/seek，不读音频，不输出像素。视频track必须唯一。
流式记实际解码输出顺序的整数PTS/duration/time_base、F、源average_rate有理数、容器/视频track时钟、
原点和edit-list；不以DTS、发布fps、packet到达顺序或best-effort代替。

只有无编辑或经元数据证明的单个0起点/单位速率恒等编辑，且首帧/视频stream起点0、时间基一致、
全帧PTS严格增、duration正且逐帧连续、末帧显示结束与stream及视频mdhd边界在1tick内一致，
才认证该**分发副本的视频显示时钟**。不能拟合/补时刻；不满足记CLOCK_UNKNOWN。
container/movie总时长与视频时长差单列，不因音频更长就改视频时间轴；不据此认证标注播放器时钟。

T固定为末帧显示结束减0原点；必须180≤T≤900、F≥48，否则DURATION_OR_FRAME_GATE_FAILED并结束，
不裁剪、拼接、改速、换文件或放宽阈值。实际元数据未知，下载成功不保证此门成立。
按round(j*(F-1)/47)、Fraction精确ties-to-even取48个源index，算d=max|index/actual_average_fps−PTS|。
HIGH_OFFSET要求真实非均匀PTS（间隔跨度>1tick）且d≥1/4秒；
CFR要求完整间隔在1tick量化内一致且d≤1/50秒；其余OTHER/UNKNOWN。
只报单副本类别，不估计自然发生率。
若非HIGH_OFFSET，报告此实测并将C记NOT_RUN，避免额外无效输入比较。

### C. 条件满足后的真实B0/P/N输入

只有B认证HIGH_OFFSET、时长/资源门通过且已有配置入口明确才执行。
使用该文件第二次也是最后一次顺序video解码，核与首遍PTS/index一致；仅保留B0与N最多96个不同索引的
192×288 RGB（流式转色及既有Pillow bilinear等比letterbox、补0），不保存原图或视频，不seek反复解码。
N目标u_j=j*T/48，用Fraction在全帧左闭右开显示区间找覆盖帧；gap/overlap/无覆盖则NOT_RUN，不插值/补帧。
实际解码/转色/letterbox/共享准备分别实付一次，不把共享解码为三臂重复计费。

只允许三个正式槽，均48帧、同prompt与同base配置：
- B0：原生processor，实际源F/T/average_fps、上述48个真实源indices，保留native timestamps；
- P：与B0同一RGB/indices/fps，只以本次资产真实source index→PTS不可变映射返回24个patch首尾均值；
  新单请求实例继承native __call__，原生formatter/tokenizer，不修最终tokens或全局/安装库；
- N：u_j覆盖的源RGB，metadata的表示时钟为48/T，frames_indices=0..47、total_num_frames=48、duration=T；
  不是声称源fps为48/T；允许重复源帧，计其数量及与B0不同的indices。
processor的width/height记实际letterbox payload 288×192，原片宽高另列；
按已核API记录实际源F/表示帧数和采样关系，不复用045的96常量。

共同system“You are a helpful assistant.”；user video+“Describe the video.”；
native apply_chat_template(tokenize=False,add_generation_prompt=True)，
do_sample_frames=False、do_resize=False、return_tensors="pt"。
仅最终视觉浮点tensor转CPU BF16；整数input_ids/attention/grid不变，不初始化CUDA。
同base身份封存前后、各槽真实回调参数/次数、未量化有理数时刻、实际native一位小数时码及其误差、
返回的全部kwargs/shape/dtype/设备/字节hash与完整签名。
完整签名仅含实际输入/共同base身份，asset/臂/code身份另存，不能制造假DIFF。

B0/P直接torch.equal视觉和grid且grid=[[24,12,18]]、1296视觉tokens；
仅允许native时码文本区域改变，token roundtrip/去时码后的其余文本相同。
P若量化后与B0完整输入相同，报INPUT_EQUIVALENT_AFTER_NATIVE_QUANTIZATION，不当模型不敏感。
N同grid/视觉tokens，不强求RGB/视觉相同；报告源帧重复/位移和全部输入等价类。
正式每槽一次，失败保留并余槽NOT_RUN，不换prompt、阈值或增加探针补救。
这些是实际输入证据，没有模型输出/IoU/准确率/显存性能结论。

### D. 统一回执并停止

一份报告按阶段区分PRECHECK_FAILED / FETCH_FAILED / VERIFIED_COPY_CLOCK_UNKNOWN /
COPY_CLOCK_MEASURED / CPU_INPUT_BOUNDARY_MEASURED或PARTIAL。
保留H01一行媒体/时钟表，B0/P/N固定三行输入表（未运行也在表内），不缩分母。
报告所有HTTP实际发送/跳转、摘要/完整性/责任与字节精确性、每阶段wall、kill/active0/finish、
Job CPU/峰RAM、processor全部调用、两遍解码读入和新根配额；驻留快照不叫卷级硬配额证明。
公开只放脱敏聚合、48点时钟/索引和tensor摘要，不放媒体、视觉tensor/像素、全帧PTS表、
原始signed头/URL、绝对私有路径、标签/QA或旧材料。

即使成功也仅通过此分发副本/输入门；原始同版身份、标注桥接、可识别已有题目、独立源、
6+2/64格、实际N成本收益及模型效果仍待明确新依据。NOVELTY=RETAIN0。
一次统一安全push后STOP，无自动047、其它媒体/下载修复/受控变体/GPU。

## 5. 执行者上传allowlist

只新增以下五处，并末尾追加一条父结果（合计六个变更路径）：
- `prototypes/holoassist_real_input_046.py`
- `prototypes/test_holoassist_real_input_046.py`
- 本目录`real-input-receipt.md`
- 本目录`source-clock-summary.csv`（H01固定一行）
- 本目录`input-boundaries.csv`（B0/P/N固定三行）
- `docs/codex-results.md`（仅一条append）

README/manifest/负责人规划、旧代码/旧报告均不改。核stage仅此六处，普通push main一次；冲突安全停止。
completed/partial/blocked任一回报均消费父任务，不继承未用预算。
本包已获批准并设为唯一READY；用户在当前本地Codex聊天发一次第6节启动消息即可，GitHub更新不会自动唤醒Codex。

## 6. 用户授权记录与启动消息

2026-10-25（北京时间），用户对[完整冻结提案](https://github.com/floomeer83felix-source/vlm/tree/1ea814cd5e4bcd520516295d67a63a5c26ff6ac4/docs/codex-artifacts/VLM-HOLOASSIST-REAL-INPUT-046)
明确回复原话“批准”。该答复确认上述H01固定分发版本的新媒体与CPU解码/输入范围；不要求额外口令，不对子阶段重复询问。
授权包含一次必要集成预检、HEAD一次/有条件GET链最多三次发送、完整性通过后的CPU验钟，
以及全部条件满足后的B0/P/N实际输入核验。资源、科学门槛、文件allowlist与停止条件均沿用冻结提案。

manifest字节未改，SHA256仍为d79a7eeb7ec57e95c4c1c60418db12b794f14736891ed3046fd58712fed63ef9；
候选仍仅H01/R015，114523050B及既定LFS SHA256、完整commit/URL、主机白名单均未改变。
新媒体≤128MiB、获取840/870/900秒、CPU累计≤1800秒、父≤5400秒、RAM4GiB/线程4、
最多两遍解码/processor≤5次/正式三槽和输出配额全部不变。
REGISTERED_UNTESTED是素材未测状态，不代表缺少执行授权；来源说明中原待批准文字保留提案历史，以本节及最新任务板为准。

本次授权不继承042–045额度，不恢复044直接获取入口，不授权其它媒体、标签/QA/旧私有材料、
权重/模型推理/GPU、安装/环境改变或后台连续工作。入口/时钟/时长等门失败则依合同保留UNKNOWN/NOT_RUN并结束。
负责人本轮只登记授权并更新规划，未访问本地Windows、获取媒体正文、运行decoder/processor或追加执行结果。
本地Codex需用户在当前活跃聊天发送一次消息启动；复制下段即可：

> 安全同步GitHub文档仓库main，重读AGENTS.md、docs/next-steps.md、docs/research-overview.md、docs/codex-results.md及docs/codex-artifacts/VLM-HOLOASSIST-REAL-INPUT-046/README.md，确认唯一尚未交付的READY父任务VLM-HOLOASSIST-REAL-INPUT-046。046已批准：按冻结manifest和合同连续完成必要预检、唯一H01一次获取、成功后的CPU验钟，满足时长/高漂移等门后继续真实B0/P/N输入核验；统一脱敏推送后停止。新媒体≤128MiB、获取≤900秒、CPU累计≤1800秒，模型/GPU/标签0；不重跑旧任务、不重试/续传/换源或继承旧额度。

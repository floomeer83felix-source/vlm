# 042已归档，禁止启动或重跑

2026-10-24：042已关闭，当前0 READY。完整媒体0/16、时钟认证0/16；首下载913.25秒超时，已落盘11534336B（11MiB）。接受失败回执，不认证资源合同全部通过：900秒截止超出，HEAD长度/ETag未持久化，实际接收正文精确值UNKNOWN、该GET保守上界4GiB。禁止042重跑/自动续传；标签/模型/GPU0，科研效应UNKNOWN。

以下合同保留历史，旧READY和启动语句均失效。

# 042：EPIC原视频与自然时钟资格核验（已授权执行合同）

2026-10-24（北京时间）。**READY / USER_APPROVED_BOUNDED_MEDIA_CPU / NOT_RUN。**
任务ID：VLM-NATURAL-CLOCK-ADMISSION-042。本文件及最新看板将本包设为唯一READY；本地Codex须安全同步main并确认该父任务尚无既报结果后，才执行一次整包。
“准备就绪/READY”是授权状态，不是媒体已下载、时钟已通过或实验已完成。

### 用户授权记录

用户在本对话收到[已冻结的完整范围](https://github.com/floomeer83felix-source/vlm/tree/b328f291d8e472e60495f54ec5a66d20a3708b45/docs/codex-artifacts/VLM-NATURAL-CLOCK-ADMISSION-042)和明确提问后，原话回复“好的”（2026-10-24，北京时间）。
提问明确为：固定16个视频，实际下载累计最多32GiB，CPU核验最多2小时，不读取标注、不运行GPU，并询问是否批准。
本次“好的”是对上述具体行动的肯定答复，负责人据此授权本文件既定范围；不要求用户重复输入指定批准口令。
这不把此前笼统“继续”追认为下载许可，也不扩大到其他数据、模型、GPU、旧任务或后台续跑。
每项单4GiB、请求次数、工具/监督前置、新根和其余硬上限均沿用该冻结合同，无新增额度。
本包允许本地Codex在已授权边界内连续完成独立步骤，统一交付一次；无需逐文件再次确认。

## 1. 要取得的证据

一次核清固定16个原视频的可获取性、实际字节身份、原始显示时钟和48点索引/fps偏移。
这是后续8源可行性设计的数据准入，非新算法、非模型效果实验；即使发现VFR，也不构成新贡献。
完成全部独立安全步骤并统一报告，不为每个文件再问一次；失败、超额与UNKNOWN留在固定16项名单，不补候选。

本包**不读取动作标注CSV、问题正文、评分端点、旧QA/预测、模型/processor资产**；
不创建64格模型输入，不做P适配或generate，不读取私人实验盘。标签桥接与提问语义未通过，不能报告完整数据资格PASS。

## 2. 冻结候选与依据

同目录[manifest.json](./manifest.json)是唯一媒体allowlist，UTF-8/LF文件SHA256：
`24d2177a27a376da48bd6a3c9e7dfa12bf2396066d690056d3e743847d4b760c`。
其中actual_bytes/actual_sha256为空，PTS=NOT_READ、bridge=UNKNOWN、admission=AUTHORIZED_NOT_RUN；均不是实测资产。
相较待授权版manifest，仅16项admission_status改为AUTHORIZED_NOT_RUN；URL、校验值、候选/顺序、科学与资源范围完全不变。

候选仅用三份公开nongold元数据生成：
- EPIC100 annotations提交ea8b40457a400c3fffa1c7f406ef3dc169cc2522的video_info，blob be226d778c0c80dd68cddc041fac9f6761949cd2。
- 官方下载器提交4f11fb2b579833f360c3c7bb917bf1e24a9787b5的epic_100_splits.csv，blob10563a493bb97f4d173876bf8fb9e04c83faf1fb；
  以及md5.csv，blob5bfdf8891aa1b52e28a19bc26500504bbb332dd5。
- 从700行取180≤duration≤900、ID匹配P[0-9]{2}_[0-9]{2}、ar_val=TRUE的66行/25位参与者。
  选择55代原片是因为已核自然降帧率说明针对该采集代；validation仅固定可用发布分区，不声称未见训练或独立测试。
- 对每个ID计算SHA256(UTF-8字符串“19\n”+video_id+“\n”)，按完整hex升序、ID破同序；
  依序每位参与者最多一项，取前16。这个入围政策在读取真实PTS、动作行或模型结果之前固定。
- 每项须在官方MD5表唯一匹配原MP4；URL直接使用校验表的发布相对路径，不能把EPIC100 validation误拼成55的媒体目录。
  不依据VFR实测、gold位置、被采到的事件或模型成绩挑原片。
- 16个公共participant ID互异只能减少同人相关，不能独立证明全部物理采集身份；后续仍须核原录制/派生关系。
  总发布时长6359.065214秒（约106分钟），单项190.3902–615.4148秒。不是媒体大小或解码耗时测量。

| 顺序 | 视频ID | 发布时长/秒 | 发布MD5 |
|---|---|---|---|
| 1 | P25_06 | 207.290417 | 3643f10b0975bb642cbdf112c8acdab1 |
| 2 | P31_10 | 540.08955 | d400c28d06a4c4302312549a34008309 |
| 3 | P32_10 | 406.072333 | 1a07ca3a8ef378d5c25d68c114916619 |
| 4 | P04_29 | 425.408317 | 4960841734afd0d5ff5102c517e33c2e |
| 5 | P18_02 | 190.3902 | 07c8c7210ccecf1d1c48f1f45c8c7579 |
| 6 | P08_15 | 563.31275 | c9e95bca19031b884aea4be71359b853 |
| 7 | P14_08 | 398.030967 | bafb132ecf5e5d5a9f2243edd9deb4fb |
| 8 | P27_05 | 615.4148 | a9974532d6faca332ab44975a49cb740 |
| 9 | P19_06 | 233.58335 | 6642431a2d5b7356256b4818effd0869 |
| 10 | P30_07 | 305.438467 | 4abef13f1df08280d76ef42e1df17406 |
| 11 | P05_09 | 421.104017 | 7431b8c8c1dd8b36526427d872f3498e |
| 12 | P17_02 | 545.774396 | bdea7eee70cb05e4d354e8ccc2a8a7d1 |
| 13 | P20_05 | 467.150017 | fc34ce1e4ebf0ad91411f941ba7ad250 |
| 14 | P28_16 | 313.379733 | fb35090ea6a65b41305826c3426ccf81 |
| 15 | P21_02 | 490.606783 | e435fe82162d4ac5ffe5f152feefdfcf |
| 16 | P07_12 | 236.019117 | 0079bed6614f78c2cf71eb360867a0ce |

MD5只核与出版者清单一致，不能作安全哈希/许可/时钟证明；成功后另算实际SHA256。
来源许可及资源声明沿用[入口核查](../../research-proposals/natural-clock-source-entry-screen-2026-10-24.md)，不混用注释、代码和媒体许可证。
本包仅用于非商业研究；发布服务有新条款/登录门/权利限制即停，不替用户接受条款或换镜像。

## 3. 已授权资源（均为硬上限，不要求耗完）

| 项目 | 上限与口径 |
|---|---|
| 远程对象 | manifest内16个完整原MP4；只允许data.bris.ac.uk的逐项HTTPS URL |
| HTTP | 每项≤1 HEAD、≤1 GET，总≤32实际发送；TLS校验开启，禁自动重试/重定向/Range/续传/批量下载器 |
| 媒体响应正文 | 全轮累计≤32GiB（34359738368B），单项≤4GiB（4294967296B）；失败及未写盘字节也计入 |
| 本地媒体 | 新根内完整+partial合计≤32GiB；GET只写同一临时文件，校验后原子改名，禁止复制倍增 |
| CPU | 单worker、≤4线程、受监督CPU阶段wall合计≤7200秒，单视频完整时钟扫描≤900秒，工作进程树RAM≤4GiB |
| 下载/父wall | 下载累计≤7200秒，整包≤14400秒；超时不重试，不后台挂起续跑 |
| 临时输出 | 媒体外≤256MiB/2048文件；公开脱敏交付≤16MiB；不保存RGB帧、音频或可视化画面 |
| GPU/模型 | GPU、Torch/CUDA模型、processor、forward/generate/训练均0；不安装依赖、不建环境 |

实际大小未知，32GiB是允许耗用的上限，不是估计账单。依冻结顺序处理；HEAD缺可靠Content-Length、
大于单项上限或剩余额度不足的条目标记NOT_FETCHED，不发GET、不换成小片。成功媒体不足时不补第17项。
连接、读和总wall均须在执行前固定；建议连接15秒、单次read60秒、每GET绝对900秒，均服从全轮预算。
响应压缩禁用并核Content-Encoding；GET声明长度/ETag（如提供）须与HEAD一致，短读、状态异常、MD5不符即该项失败，不重传。
全轮鉴权/条款异常或计量、监督/输出边界失效立即停止其余网络；普通独立单项404/超额可记状态后继续名单其余项。

## 4. 执行顺序与停止条件

A. 安全同步独立文档checkout，重读AGENTS/看板/results；确认唯一READY且042无既报结果。
校验manifest内容和上述SHA；本地新根固定为该文档checkout的同级新目录`vlm-private-042`，存在即STOP，不复用旧根。
父目录及新根须为正常非reparse/symlink对象，可用空间须≥媒体最大预算32GiB+输出256MiB+余量2GiB。
完整路径仅留本地。不能扫描实验盘、用户home或旧媒体目录来“找已有文件”。

B. **任何媒体HTTP之前**先核本机既有工具及监督能力：限PATH的ffprobe/ffmpeg定位及既有pytorch环境的
av/torchcodec分发包版本元数据，不导入Torch、不递归找工具。只选可明确禁硬件解码的既有CPU接口；
版本/二进制SHA与选定命令/API写入收据。不能安装或沿用旧任务未完下载。
若没有能返回真实解码帧PTS/显示时长的接口、或不能有效约束进程树RAM/threads/wall/新根配额，STOP，媒体HEAD/GET=0。
不得用容器packet序、DTS、best-effort估计时间或单看avg_fps代替显示帧时钟。

C. 顺序获取固定对象，边流式记全轮/单项收到字节并执行上限；每项最多一次。
流式更新MD5/SHA256可避免额外通读；成功须长度及MD5一致。重命名不重新下载、不重编码。
本地媒体只在本包新根，绝不上Git。授权不要求耗完额度；任何已完成/partial对象不得因预算复位重新取。

D. 对成功对象各执行一次完整CPU显示帧时钟扫描，只读指定视频track，禁音频/图像输出。
记录整数PTS、time_base、逐帧显示duration、显示顺序、frame count、流avg_frame_rate、原点/edit-list语义；
边扫描边聚合/本地流式写表，禁止把全帧RGB或全部解码对象驻留内存。
若接口只给推算时刻、显示duration缺失或编辑列表/时钟原点不清，该项CLOCK_UNKNOWN；
不能减去任意首帧值、拟合偏移、补缺失duration或凭packet统计冒充全帧认证。
扫描/完整性失败留失败状态且不重扫；允许继续其余独立候选。
有B帧时必须使用解码器显示顺序/真实frame PTS，不能按packet到达序关联。

E. 以已认证同一媒体原点计算48点。
索引是精确有理数j*(F-1)/47（j=0..47）的round-to-nearest、ties-to-even整数。
用实际源avg_frame_rate的有理数（不是发布表的十进制字符串）计算i/fps；
PTS用整数*time_base减去已证统一原点，计算d=max|i/fps-p|。
高偏移层需要真实非均匀显示时序且d≥0.25秒；CFR需完整相邻显示间隔在源time_base允许的单tick量化内一致、
持续时间/边界相容且d≤0.02秒，不能仅凭d小即CFR。
边界量化超出/覆盖重叠、间隙、缺PTS/显示duration、未知edit-list均UNKNOWN，不悄悄放宽准入。
按固定selection_sha256顺序各层取前6/2，绝不按漂移最大值取赢家；未够6+2如实SOURCE_CLOCK_INSUFFICIENT，停止该候选当前准入。

F. 统一报告每个候选状态、实际字节/SHA/校验、是否完整时钟认证、F/time_base/源fps/d/量化、
总请求与收取正文（含失败）、共享wall/峰RAM/新根峰值。上传固定16项分母的汇总，不上传逐帧表、媒体、原标注或私人路径。
即使6+2成立，也只报SOURCE_CLOCK_FEASIBLE / LABEL_AND_INPUT_GATES_HOLD；
没有nongold问题队列、既有标签时钟桥接及实际processor输入门，不得报64格READY或真实任务收益。

## 5. 评测定义的已知缺口

[EPIC100原论文](https://link.springer.com/article/10.1007/s11263-021-01531-2)的Temporal Annotator节明确处理同一动作反复发生，
原标注者还获得粗时刻来区分实例。通用“Locate the event”只给动作文本时，不能假定已指定一个唯一隐藏实例。
所以后续若使用EPIC，必须在任何模型结果前解决重复描述的有效答案集合/题目可识别性；
不能把narration_timestamp、gold附近crop或事件编号悄悄加入提示，也不能看预测后才决定哪个区间算对。
本包不读动作CSV、不挑题、不计IoU；这项缺口保持HOLD，不能用真实VFR计数代替解决它。

标注schema里的“秒”、start_frame/fps数值近似、同一video_id，以及出版者MD5均不单独证明标注播放器与原MP4同钟。
EPIC55的帧索引说明针对其规定抽帧方法；不得据此直接映射原始解码帧。
后续时钟桥接仍需固定版本、原点/编辑规则或可核映射；缺失时不臆定恒等桥接。

## 6. 本地Codex准许交付与结束

当前尚未执行；确认唯一READY、该父任务无既报结果并满足前置后，准许以下同一包变更：
- 可新增prototypes/epic_clock_admission_042.py及prototypes/test_epic_clock_admission_042.py；
  tests只覆盖有实际风险的硬预算/一次发送/非重试、帧时钟算术、B帧显示顺序和不确定条件拒绝，不重开toy科研任务。
- 新增本目录clock-admission-receipt.md、candidate-clock-summary.csv；只追加docs/codex-results.md末尾一条042父结果。
- README/manifest由负责人冻结，Codex不得自行扩大；不改规划总览、旧代码/历史收据/旧实验根。
- 确认公开diff仅上述路径、剔除完整私人路径/媒体/逐帧原表/标签后安全push main，STOP一次执行轮；
  不启动P适配、模型、扩样、第二下载或后台监控。
- 一旦产生completed/partial/blocked父回报，042即已消费，不能把未用额度迁移重跑。

授权记录已见页首；不需再次批准同一范围。本合同不会唤醒另一聊天中的本地Codex；用户在当前本地Codex聊天发送一次启动指令即可：
“安全同步文档仓库main，重读AGENTS.md、docs/next-steps.md、docs/codex-results.md及042 README，执行唯一尚未交付的READY父任务VLM-NATURAL-CLOCK-ADMISSION-042。
已批准清单内16个原视频累计最多32GiB、单项最多4GiB和既有CPU工具核时钟最多2小时；严格按README连续完成允许的独立步骤，统一脱敏推送后停止，标签和GPU均0。”

## 7. 负责人本轮完成与边界

负责人已从公开nongold清单独立生成/验证16项：ID/URL/参与者唯一、均55代validation、时长合格、每项唯一MD5匹配；
未向这些MP4发HEAD/GET，未读视频或动作CSV，未测试本机工具、PTS/时钟桥接、processor或GPU。
本包已依据本次肯定答复转唯一READY，等待本地Codex启动；本轮负责人仅更新授权与交接文档，未代替执行、未下载媒体，也未写执行结果。
040/041关闭、NOVELTY=RETAIN0、NATURAL_VIDEO_EFFECT_UNKNOWN和既有媒体/训练停止结论不变。

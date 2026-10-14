# VLM-PD-LONGVIDEO-007｜以实际返回的官方转码键执行一轮长视频A/B

**2026-10-14｜READY / USER_REQUESTED_CONTINUE_EXPERIMENT（唯一READY，限本父任务）**。用户要求加快实验，且不希望同一已准范围逐步骤审批。本轮优先纠正006已实证的**预设360p键未形成唯一匹配**，不再假设官方页面展示的“360P 已完成”必然等于`videoinfo.derivatives`提供对应播放键。用户在原Codex长期聊天一次发送启动指令；GitHub更新不会自动启动本机GPU。

## 已验收的历史与新版来源策略

- [d5a7677](https://github.com/floomeer83felix-source/vlm/commit/d5a767740a671829ec2021071c1dd6104f89846d)：006离线结构校验PASS，Commons官方API HTTP200，meta完整3,155B，文件JSON/schema/身份及美国公有领域结构化字段全部PASS；**`DERIVATIVE_EXACT_KEY_COUNT`** 指旧代码预设`360p.vp9.webm`在当前`videoinfo.derivatives`中匹配数≠1，未记录实际0或≥2；**视频GET0、GPU两个臂各0更新**。原006已结案、GET1次不得退款、重开/续传，不把旧结果冒称任意转码均不可用。
- Wikimedia官方[TimedMediaHandler配置](https://github.com/wikimedia/mediawiki-extensions-TimedMediaHandler/blob/master/extension.json)的通用配置列出`240p.vp9.webm`启用、`360p.vp9.webm`默认禁用，这**不能证明当前Commons站点实际配置或此文件的实际衍生列表**；[官方《One Week》(1920)页面](https://commons.wikimedia.org/wiki/File:One_Week_(1920).webm)显示美国公有领域与24m26s影片、VP9多尺寸完成，但网页不等于API响应。**不猜测源文件下载路径**，所有影片媒体URL仍必须来自本次**唯一真实API`videoinfo`返回**。
- 新执行源固定`File:One Week (1920).webm`，**只允许**按顺序`360p.vp9.webm`、`240p.vp9.webm`两个精确白名单键。若首选当前API未返回、但第二项**恰有一个**且URI验证为`https://upload.wikimedia.org/wikipedia/commons/transcoded/.../...240p.vp9.webm`，则安全取240p低码率版本；任一键多次重复、实际地址来自非官方域/不在transcoded路径、无受支持项，一律`HOLD`并0媒体GET；**不能选择480p、原版132MB、站外镜像或动态任意首项**。240p降低分辨率但不改变影片实际时间跨度，实验意义仍受质量限制；必须实测PTS跨度≥1200秒。
- 许可：结构化美国PD声明须真实当轮PASS，仍不推断全球法律状态。若研究运行地点或具体使用所需许可不合适、版权冲突或使用条款不清楚，就`SOURCE_LICENSE_HOLD`且0媒体GET，不用来源页面的PD图标强行覆盖实际API。

## 已写好真正可运行的有限脚本——先离线、再一轮网络和GPU

1. ChatGPT已提供[**`fetch_official_variant.py`**](./fetch_official_variant.py)——直接来自006验证过的单源受控下载器，仅将单固定360p键更正为**预先列明的两个精确键/确定优先级**，并补充两者均可返回、只有240p返回、重复键、恶意URI、缺键、错误页、license失败的**网络前离线`--selftest`**。不需要公开JSON或泄露完整媒体URL来诊断。Codex只复制GitHub本任务代码到本人**全新私有任务目录**，UTF-8 AST检查、`python fetch_official_variant.py --selftest`必须PASS。否则本轮网络请求0、不尝试改官方素材。有限、报告类别的逻辑缺陷只能在任务私有副本做保守修复，不修改旧005/006源码或其账本、不放宽源/许可。
2. 每个GET前独立`STARTED/fsync`，本父任务总计**最多2个真实HTTPS请求**：官方 Commons `videoinfo`元数据GET≤1（应用正文**<512KiB**，本版代码不会多读1字节），源/许可/唯一白名单衍生键与完整官方HTTPS地址PASS后，来自其返回唯一src的**视频GET≤1且ContentLength和应用正文≤96MiB**。TLS核验、禁代理/自动重定向/Range/隐藏重试/二次请求/备用镜像；一次失败的GET/预算不退款、不继承006。小网络下载最长≤10min；只保存视频到新父任务私有目录，完整WebM且EBML/大小/私有SHA核验后才原子完成。**≤96MiB指媒体HTTP应用正文；并非所有TLS/wire/物理流量上限的虚假保证**。
3. 仅当完整视频、使用许可和真实PTS≥1,200秒、采集至少350帧数据全PASS，复制已有[**`long_temporal_ab.py`**](../VLM-PD-LONGVIDEO-005/long_temporal_ab.py)到新父任务私有目录AST验证、按固定`python long_temporal_ab.py --video <PRIVATE_TASK_DIR>/one-week-360p.webm --steps-per-arm 100 --gpu-minutes 12`执行。现成PyAV/OpenCV/NumPy/Torch，不安装/下载权重。CPU解码/抽帧≤10分钟，GPU两臂累计≤12分钟，前台总≤25分钟，独立单调计时、外层既存限时器不得犯历史UTC转换错误。
4. 预冻结真实长时公平A/B：同影片前70%作train、后30%晚段验证（隔离9秒buffer），**uniform128** vs 运动变化优先128，完全相同验证70真实帧/固定160时序pair、相同初始化/优化器/种子/各≤100真`backward+optimizer.step`，上限200实际步骤。torch新增allocated峰值≤512MiB，两次GPU快照分别free≥8GiB/util≤30%、已知互斥和明确冲突保护PASS才能运行；Windows C+G本身不禁用、不能杀他人进程/解锁。若媒体/PTS/许可/CPU监督/GPU任何条件失败，停止、真实训练步0，不以旧MDN短片、合成帧、HourVideo开发问答或Charades替代。
5. 本阶段始终只是**单部1920年电影的真实长跨度低维帧顺序分类实验**，不是Ego4D/HourVideo第一视角VLM QA，没有Qwen3-VL主干权重前向、SigLIP查询相关选择或模型微调；同片后段准确率不能证明跨影片泛化、准确率优势或论文创新。声明`NOVELTY=RETAIN0`、Charades`FINAL_MEDIA_STOP`、HourVideo dev↔Ego4D v2_1发布与PTS桥接UNKNOWN不变。

## 一次匿名回报与停止

仅可创建`docs/codex-artifacts/VLM-PD-LONGVIDEO-007/available-variant-long-ab-receipt.md`和`docs/codex-results.md`末尾恰好一条`### VLM-PD-LONGVIDEO-007`。匿名报告新离线fixtures是否PASS、API返回两个白名单键的**各0/1/重复的计数类别**（禁止原JSON/原src、用户私有目录）、被选确切白名单名称或稳健reason_code、两次GET的实际尝试/字节、完整容器/帧PTS跨度、两臂各真optimizer更新/首末loss/同clip后段指标、时间/显存及所有安全STOP。视频/解码帧/特征/私有账本/密钥/源UID/私人补丁与全部日志不进公共仓库。旧005/006 STARTED预算与部分文件不变，无额外官方站点HTTP诊断，0 AWS/Ego4D/HourVideo媒体/Charades/权重下载，最终一次正常main push后STOP、不自动开启任何QUEUED GPU或数据任务。

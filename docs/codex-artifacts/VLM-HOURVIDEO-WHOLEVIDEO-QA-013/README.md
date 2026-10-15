# VLM-HOURVIDEO-WHOLEVIDEO-QA-013｜官方同UID视频、真实43题，时间零点假设条件下的完整视频Qwen×SigLIP配对A/B

**2026-10-15｜唯一READY / USER_TRIGGERED_EXPLORATORY_MATCHED_QA（新GPU模型预算尚未授权，GitHub READY不自动运行）**。用户要求加快真实有答案VLM研究；本父任务依据[012实证](../VLM-HOURVIDEO-MATCHED-QA-012/matched-hourvideo-pilot-receipt.md)修订过严的时钟证明门，**只对整个视频的无时间戳提示的多选题做固定PTS全片采样**，并严格用`CLOCK_ZERO_ASSUMED_NOT_CERTIFIED`表达同发布零点未独立证实的科学限定，**不得写成`RELEASE_PTS_BRIDGE_PASS`或正式HourVideo榜单结果**。与先前013以外任何旧任务无额度继承，**本任务须用户在原同一Codex聊天明确一次授权至多86次本地Qwen生成／GPU累计≤30分钟后才可以开始**。

## 证据基础与改动动机

- [f405b99](https://github.com/floomeer83felix-source/vlm/commit/f405b99b536d0ffb59c2ea1329ced16683acaf26)已经充分证实：由用户从官方HourVideo发布源手工获取、已有确切私有入口的demo MP4 **889.396MiB**，文件与已准私人HourVideo dev带gold标注 **video_uid完整相同**，**43条同UID五选项有效gold标签**。ffprobe视频流长**3598.033333s**、标注metadata长**3598.030000s**，仅差0.003333秒；已单次完整PyAV解码到EOF实测**107,941帧**，首/末PTS**0.021029/3598.021029s**、严格递增、整个跨度3598s。012保守地因没有**独立同版裁剪/零点映射原始证书**而安全HOLD，Qwen0、SigLIP0、GPU0。**不能把该HOLD描述为源不匹配、视频不可用、视频不完整或没有金标**。
- [HourVideo官方HF数据集README](https://huggingface.co/datasets/HourVideo/HourVideo/blob/main/README.md)明确将该`demo_video`内MP4用作**官方Quick Start样本**，官方`samples_v1.0.json`有gold，而`dev_v1.0.json`没有gold；官方[NeurIPS代码仓](https://github.com/keshik6/HourVideo)提供基于官方demo的评测教程。此前用户已获准的本机私有标注`dev_v1.0_annotations.json`经012实测此同UID43个真gold，这些证据足以将它纳入**对原假设持保留的、同视频全局多选问答技术探索**。
- **本协议是独立研究设计更改，不是事后宣布零点已获证明。** 整片全局问题的uniform12与SigLIP12都直接在**同一现有完整媒体PTS范围**取帧，SigLIP只看问题文字；不读取、映射或依赖QA的`relevant_timestamps`、时间标签、剪辑起点来决定选帧。因此未知的`annotation t=0→media PTS=0`偏移不参与任何取帧计算；潜在**视频内容/发布版本的不可观察不一致仍是主要解释性局限**。预先固定名义假设`MEDIA_PTS_DIRECT_WHOLE_VIDEO`，在所有匿名指标上标`CLOCK_ZERO_ASSUMED_NOT_CERTIFIED`，结果称`MATCHED_UID_WHOLE_VIDEO_QA_PROVISIONAL`，不能当官方完整基准、精确时刻定位验证、版本对齐已经过独立证明或SOTA增益。
- **不要求用户重新下载视频、注释、模型，不能恢复旧Ego4D残片/AWS账本；不能重跑012已经通过的107,941帧全量完整解码。** 上游011真实Qwen3-VL-4B-Instruct＋SigLIP双塔在RTX3090已完成4/4 Qwen生成38.906秒，模型配置由用户授权于`D:\models\Qwen3-VL-4B-Instruct`与`D:\models\siglip-base-patch16-224`，仅需最小CPU确认现有目录未变；此前技术运行并不算本次科学推理。

## 用户批准后，前台一次性执行而不是分43次申请

### A｜0模型GPU的合法性/内容门（约≤5分钟）

1. 安全同步**独立公共文档Git checkout**的main及AGENTS，确认013唯一READY且Codex results无同父任务；绝不对Windows真正实验树做git操作。确认原Codex同一聊天消息明确允许：已经合法授权的该demo**已知精确私人MP4入口**、已授权的私有同UID有gold标注**已知单一入口**、先前已指定的两个本地模型根、和**本轮新预算最多86次Qwen本地generate/GPU≤30分钟、0研究媒体/模型网络**。若授权或明确入口缺失则不启动013，不再提交一份旧012重复HOLD报告。
2. CPU只读必要的确切非symlink普通视频/标注/model roots/processor及最低限度ffprobe头信息，不遍历用户下载、科研资料或私人其它目录，不重解码十万帧。验证视频文件未换物、标注UID与该官方demo完全一致、且**43个五选项+金标可按原012相同规则复核**；如果少于2个可独立支持的视频问题则HOLD。限制帧输入仍是**从现成同一完整PTS时轴解码得到的48个真实帧、覆盖≥1200s**，不调用QA相关`relevant_timestamps`或使用gold定义帧窗口。
3. 为维护**附图题公平性与官方发布契合**，在看gold之前用预定义的**仅问题/任务schema规则**排除确实需要额外官方navigation/spatial images、caption外部资源或不能由视频和文字回答的条目；只读检查它们在question/mcq metadata里是否存在显式外部图片引用及任务字段。**不要擅自把文本中普通词“image”当成外部图题**；不确定则标`AUX_ASSET_UNVERIFIED`并从预冻结可评集合排除、匿名只上报数量。保留所有纯文字五选项且无需外部asset的题，最多43；固定按官方原始稳定顺序进入全量配对，不根据gold内容/是否容易/单模型响应挑题。**计分分母在GPU前冻结、同时记预排eligible N、被排除非文本依赖数，N需≥2。** 任何私人gold只由隔离评分器在所有输出完成后读取；前置schema checker仅验证gold字段存在与编码合法，不读取实际答案内容进入选帧/模型程序。
4. CPU先离线合成fixtures验证已存在的多选label编码与解析器逻辑、私有gold隔离、同样N的A/B队列、计数/错误归集，无实际模型/网络。凡需重装transformers、下载模型、替换量化策略，STOP而不是绕过。

### B｜真正的RTX3090对照：所有可评问题每题两臂，≤86次generate

1. 在全视频PTS有限递增时轴，确定性**均匀48个真实候选帧**，视频输入帧仅来自已授权本地demo且frame PTS与source相同。对每一预冻结有资格的MCQ：A从同48中uniform12；B用真实SigLIP text prompt（**只能用问题本身，不含正确答案、图片外部字段及选项中的潜在答案偏置**）与共享48图像embedding按归一化余弦排序top12、恢复PTS顺序。A/B都12帧；Qwen输入两臂完全同一question和**官方原五选项**、同模型权重/processor/视觉像素预算、max input size与metadata、采样/decoding设置（`do_sample=False`）、同一答题系统指令`Choose exactly one answer from A, B, C, D, E. Output only the single letter.`。
2. Qwen3-VL-4B-Instruct BF16与SigLIP图文双塔权重仅从已授权本地根`local_files_only=True`、`HF_HUB_OFFLINE=1`加载；`eval()+torch.inference_mode()`，**不训练Qwen/LoRA/head**，不使用远程模型API。每条generate`max_new_tokens≤64`、前0 warmup、请求前私有`fsync`预扣本轮尝试数；`N≤43`则最多**2N≤86 Qwen实际generate attempts**，每题严格配对A/B（按题序AB/BA交错以抵御系统效应），计入失败/未生成/长度截断。只接受`strip()`之后**单字母A–E（可选尾句号）**为valid，否则INVALID；**不要从长自由答复里搜索任意A–E并择有利输出**。每次生成记录natural EOS vs cap、推理时间、枚举有效性。任何GPU超时/OOM/失配必须安全停止，已冻结题分母内未完成的一律not-run，**不得根据错误/正确率重新运行、替换prompt或换题**。
3. 先两次≥2秒nvidia-smi空闲门均free≥8GiB/util≤30%、自有互斥及明确冲突检查PASS，不清他人锁/进程。RTX3090所有模型load、视频text/image编码、generate GPU累计≤30分钟，**新增框架allocated峰≤20GiB**，整个本轮前台墙钟≤50分钟，其中CPU只读抽帧≤10min。使用独立只监督自己子进程`time.monotonic`硬截止与阶段计数，不放大因UTC时区转换产生的历史误差。没有安全上限执行器就GPU0，不使用云GPU、改变conda/driver或重复生成。
4. 正常完成或预算提前停止后才使用**隔离私有计分器**读gold，与已经冻结的全部eligible题映射配对；在固定每臂N分母中，正确/错误/INVALID/NOT_RUN都清楚记录，报告A/B correct/N、A_only、B_only、both_right、both_wrong、invalid和McNemar**描述性**配对差值及简单不确定性（N≤43，不足以确认创新/统计优势）。**条件性质必须写在每一个涉及准确率的报告语句旁**：视频零点/版次没有独立桥证，只能报告`provisional within same-user-matched demo, assumed whole-video clock`；正式HourVideo DEV leaderboard accuracy = **NOT_ESTABLISHED**。绝不能把任何题目、选项、真实gold、真实UID、完整生成文本或其hash发到public GitHub。

## 安全输出、不可变科研限制与停止

- 任务只允许新增`docs/codex-artifacts/VLM-HOURVIDEO-WHOLEVIDEO-QA-013/whole-video-provisional-qa-receipt.md`与在`docs/codex-results.md`尾部一条`### VLM-HOURVIDEO-WHOLEVIDEO-QA-013`；父级仅一次正常push main后STOP，不修改旧012/011结果或其他旧账本。报告最多43 eligible/筛除数、实际paired attempted/completed、Qwen生成实际调用和失败、选帧时间覆盖/交集聚合、真实GPU wall/allocated、每臂fixed denominator正确/错误/invalid/未运行/配对四格、零点证据等级和用户授权分类。
- **不下载任何研究视频/模型或Ego4D、无AWS/HTTP/云GPU、无安装、无私人目录扫描/音频转写/标注修改/原模型全文上传**；QAs及benchmark canary串不得进入训练数据或公共日志。**HourVideo dev永不用于训练，答案只在最后隔离评价**。若存在不确定答案协议、身份突变、许可不符或现成模型无法安全离线装载，立即HOLD/0新GPU。
- 科学结论最多是“同一用户获准HourVideo官方demo与同UID带gold标注，在**未获独立零时刻映射**的名义全片时间假设下开展的探索性配对多选QA”；不是官方发布版PTS对齐已证、HourVideo完整榜单、多视频泛化、采样创新或Qwen微调。保留`CLOCK_ZERO_ASSUMED_NOT_CERTIFIED`、`NOVELTY=RETAIN0`和Charades`FINAL_MEDIA_STOP`。

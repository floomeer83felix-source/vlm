# VLM-BATCH-019：时间基、来源与真值合同

2026-10-10。只读官方schema和网页源码，不读取任何标注行/私有媒体、执行loader或运行ffprobe。下列公式是坐标合同的纸面推导；“字段/代码已核”不等于MEDIA_CLOCK_PASS，条件缺失时返回UNKNOWN。

## Ego4D：先区分三个命名空间

[官方schema](https://ego4d-data.org/docs/data/annotations-schemas/)分别给出metadata的`video_metadata`（stream起点/时长、PTS及`video_base_numerator/denominator`）、component的`canonical_video_start_sec/end_sec`与各自timebase，以及NLQ clip/header/query中的`video_start_sec/end_sec`、`clip_start_sec/end_sec`。同名字段必须带所属对象：metadata stream起点不是NLQ clip在parent中的起点，query起止也不是clip总边界。

若呈现PTS为p、同一stream起点p0、timebase为n/d，则相对视频stream时间为 `(p-p0)*n/d`；若q处于某canonical clip、同一锚点在video/clip坐标分别为av/ac，且只做连续裁剪、无变速，则 `t_video(q)=q+(av-ac)`。component k候选映射为 `t_canonical = canonical_video_start_sec[k] + (p-p0[k])*n[k]/d[k]`，但仅在其trim/重编码/拼接映射确实同版成立时适用；不是仅凭字段值就证明准确。

[Videos文档](https://ego4d-data.org/docs/data/videos/)明确canonical标准化/拼接、30fps、clip半开裁剪范围；源component可以有不同timebase和stream/container终点。CFR的文档承诺不替代文件级PTS、裁剪起点、边界舍入与版本关联核验。packet解码次序不能直接冒充呈现帧序列；也不把B帧一概解释为时间不可读。本轮不重新解释或重跑Charades018的冻结UNKNOWN。

[Episodic Memory任务页](https://ego4d-data.org/docs/benchmarks/episodic-memory/)将NLQ定义为答案可见窗口、VQ为对象最后出现轨迹、MQ为活动区间；这些支持各自标签语义，不能将NLQ interval理解为穷尽的同类重复事件实例表。官方[版本更新页](https://ego4d-data.org/docs/updates/)说明NLQ增加覆盖并修过零长度窗口；因此版本/date和媒体对象关系需绑定，旧v1/新v2不可无说明混用。当前小时级评测GT密度、漏标率与重复实例身份完备性UNKNOWN。

## HourVideo：长域真实，但与Ego4D映射未闭合

[官方README](https://github.com/keshik6/HourVideo)确认Ego4D来源和多选评估、禁止训练。仅源标签“来自Ego4D”不保证相同canonical版本、完整视频还是裁剪/降采样派生文件，也不提供可公开审计的PTS—QA interval逐项对应。

本次读到[hv_utils.py网页](https://github.com/keshik6/HourVideo/blob/main/hourvideo/hv_utils.py)的load_video按平均fps选择索引，downsample_video经固定输出fps重写，trim_video把秒转换为索引。不能由README的1分钟caption段推导逐帧PTS或动作边界GT。若无重采样/裁剪，可候选写作 `t_Ego4D=a*t_HourVideo+b`；a、b、源版本、视频/问题窗口GT没有独立证据时不得默认(1,0)。没有打开HF标注或生成描述文件，QA正确选项不当物理时间真值。

## LongVideoBench：源码明确减偏移，不应将字段混作PTS

[官方loader](https://github.com/longvideobench/LongVideoBench/blob/main/longvideobench/longvideobench_dataset.py)的load_video取平均fps f，以 `int(duration*f)`限制有效帧索引，输出时间 `i/f`；这属于名义帧序号坐标，不是读取实际呈现PTS。insert_subtitles_into_frames把字幕起止减`starting_timestamp_for_subtitles`，以中点交错，短于1秒的支持窗还会扩展。不能反向把该插入窗当原始精确视觉证据区间。

条件式合同：`t_local_subtitle = t_source_subtitle - starting_timestamp_for_subtitles`；字幕s/m/秒字符串先解析为秒。唯有源偏移、裁剪文件原点、同版媒体与字幕都成立时才可和 `i/f`比较。要转呈现时间另需 `t_PTS=(p-p0)*timebase` 和实际media映射，duration字段不能等同容器总时长。

[v1论文§3.3](https://arxiv.org/html/2407.15754v1)要求annotator标记引用时刻的frame index，因此不能写“完全没有时间证据标注”；但其发布JSON是否保留全部引用索引及其版本、是否有多实例身份/完整区间GT，本轮UNKNOWN。loader公开读取QA选项/帧/字幕不证明上述字段公开且可作科学真值；未访问QA行或HF实体。

## Video-MME：字幕取用规则已核，物理时钟仍未证

[官方评测README](https://github.com/MME-Benchmarks/Video-MME#-evaluation-pipeline)要求有字幕设置仅用采样帧对应字幕；长组都有字幕，不代表时钟已逐文件核准。官方链接的[video-slicer脚本网页](https://github.com/look4u-ok/video-slicer/blob/main/slice_and_extract.py)是外部工具，不能假称官方作者源码：按OpenCV帧数/fps取索引，图像命名按整数秒，pysubs2以同fps将帧索引换为字幕时间，再判断严格位于字幕起止内。

因此可读代码仅支持“假定帧序号/fps与SRT时间原点相同”的工程逻辑；没有文件级PTS、版本SHA、剪辑替换后的字幕偏移证明。QA标注不是事件身份证据。所读官方正文有移除侵权内容的机制，没有足以认证替换文件仍同版的规则，MEDIA_REPLACEMENT_MAPPING_UNKNOWN；不猜替换数量。

## 其它两候选与禁止升级

[MLVU](https://github.com/JUNJIE99/MLVU#hosting-and-maintenance)明确可能将被移除视频换为稀疏帧或元信息；QA稳定不保证连续时间轴稳定。[LVBench](https://github.com/zai-org/LVBench#download)凭平台身份取源视频，也不是内容hash/裁剪/字幕原点合同。二者当前TIMEBASE与事件实例GT均UNKNOWN。

| 使用目的 | 静态可支持的对象 | 尚缺的独立证明 |
|---|---|---|
| QA准确率 | 合规前提下的benchmark选项/评分规则 | 同版媒体、许可链、泄漏隔离与真长域分组 |
| 时间定位 | Ego4D NLQ窗口；LongVideoBench创建阶段引用frame index | 发布/版本/呈现PTS及标注对应，不自动是所有重复实例GT |
| 重复实体或事件排序 | 任务可能涉及关联；Ego4D其它EM任务有特定轨迹/区间 | 对象身份与事件实例分别可识别，跨分钟覆盖、歧义与缺失真值 |

本轮所有MEDIA_CLOCK与EVENT_TRUTH实证门仍UNKNOWN/HOLD。坐标可转换不是新算法，软件字段不是独立视觉真值，QA标准答案不能进入选择政策或替代物理边界。

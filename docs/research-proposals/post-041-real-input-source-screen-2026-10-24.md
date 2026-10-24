# 041后真实输入链路筛查：现有覆盖与PTS边界

2026-10-24（北京时间）。**PUBLIC_SOURCE_SCREEN_COMPLETE / NO_NEW_TASK / NOVELTY=RETAIN0。**
本轮是研究负责人公开论文与源码筛查，不是042实验；041已关闭，当前0 READY。

## 筛查裁决

| 候选 | 本轮核到的先例或源码 | 当前裁决 |
|---|---|---|
| 统一评测配方、解释后端/输入形式差异 | Meta-Video已研究采样、解码、输入形式、后端和报告规范，并修正特定视频转独立图片的路径 | 宽泛标准化主张有直接近邻，不据此立项 |
| 保留原生视频时间信号 | ExtremeWhenBench项目已发布相关适配路径并报告其影响 | 转发metadata或改用video URL不能直接算我们的新机制 |
| 可变帧率下保持真实显示时刻 | Qwen/HF路径使用帧索引与平均fps重建时刻；VeOmni已明确说明VFR精确时刻需要保留PTS | 限制确有源码依据，但认识本身已有明确先例；真实任务影响未核 |

已核Meta-Video的后端、输入形式、评测卡讨论及附录A.3；它在所研究实现上区分视频与图片路径，并提供评测卡与参考配置。本轮不复用其分数为项目结果，也不把其对特定包装器的观察泛化为所有vLLM版本。来源：[arXiv:2610.18535v1](https://arxiv.org/html/2610.18535v1)。

ExtremeWhenBench此处仅核项目README对原生视频路径和时间信号的说明，没有执行其基准、补丁或读取数据集。来源：[项目README](https://github.com/naver-ai/ExtremeWhenbench/blob/main/README.md)，Git blob `ab994bae53ce8ecca055ac584e12d0cde2bde5a2`。相关效果为作者报告，不是本项目复算或性能证据。

## 精确源码边界

1. [Qwen qwen-vl-utils](https://github.com/QwenLM/Qwen3-VL/blob/96588727e44c78b25ba03ea03b8e12f7e64fd0da/qwen-vl-utils/src/qwen_vl_utils/vision_process.py#L338-L377)，`_read_video_torchcodec`：从decoder取得average_fps/num_frames，按索引取帧后只取.data，并向后传fps、frames_indices和帧数。该路径未向processor传递逐帧PTS。读取时固定commit `96588727e44c78b25ba03ea03b8e12f7e64fd0da`，文件blob `0bb3c5ae1e47349e474b5e24b6d9c29d7f44e1be`。
2. [Transformers v4.57.6 Qwen3 processor](https://github.com/huggingface/transformers/blob/v4.57.6/src/transformers/models/qwen3_vl/processing_qwen3_vl.py)，`_calculate_timestamps`：先以index/fps取得时间，再平均每个temporal patch的首尾时刻。公开文件UTF-8为17,149B、SHA256 `efd8d64aaf608aad1ffb3e6d503d6a99e5227d007df95c1d9fa905d998cda4a9`，与041安装源码收据一致。这是公开字节与既有收据的匹配，不是本轮重新读取私人安装目录。
3. 当前HF [processor](https://github.com/huggingface/transformers/blob/50e35cc0ca18ec19b80653690de553e6decf74f5/src/transformers/models/qwen3_vl/processing_qwen3_vl.py#L178-L189)与[VideoMetadata](https://github.com/huggingface/transformers/blob/50e35cc0ca18ec19b80653690de553e6decf74f5/src/transformers/video_utils.py#L79-L113)仍可见该计算形式。固定commit `50e35cc0ca18ec19b80653690de553e6decf74f5`；两个文件blob依次为 `bbb187a4c9f60e8e9f27a6706004b5b0d6ebe7f6`、`71baf0ce5e5ac24721d159acd7148ae96bae5fe1`。不据此声称全部HF解码器或其他模型均有同样路径。
4. [VeOmni官方说明](https://github.com/ByteDance-Seed/VeOmni/blob/eba362dd4ca43b6cba53dc69c1d378cf3eda57b6/docs/usage/multimodal_data_processing.md)的Video Timing Metadata节已说明平均fps与VFR精确PTS的差别。固定commit `eba362dd4ca43b6cba53dc69c1d378cf3eda57b6`，文件blob `8b28e743d117f4d587af115fe6a27491140c84c2`。这直接否定“首次认识到这一限制”的主张。

可推断的范围：仅有索引和一个平均fps时，通常不能恢复任意不均匀显示时间轴。这是从上述表示推得的信息缺失，不是自然视频错误发生率、Qwen能力失败或新算法结论。041证明的缓存身份一致性，也不能认证metadata本身与媒体时钟相符。

## 数值示意，非媒体或模型实验

设12帧、时长12秒、声明平均fps=1，帧索引0..11。
若逐帧显示时刻为
`[0, 0.1, 0.2, 0.3, 0.4, 0.5, 6, 7, 8, 9, 10, 11]`，
最后一帧显示至12秒，则两帧patch按索引重建的中点为
`[0.5, 2.5, 4.5, 6.5, 8.5, 10.5]`，
逐帧PTS首尾平均则为
`[0.05, 0.25, 0.45, 6.5, 8.5, 10.5]`；
最大中点差为4.05秒。

这只是对公式的可检验数值说明，无文件封装、解码、真实processor、forward或generate；没有创建实验run或结果父记录。它不说明真实容器、任务或模型答案会出现该幅度误差，也不把patch中点定义为事件gold。

## 未满足的立项条件

- 尚未确认一个有明确使用许可、可复查逐帧时钟、具有实际相关任务的自然来源会受到这一表示限制影响；不能继承旧媒体/annotation许可或擅读旧数据确认。
- 尚未排除现有保留PTS的解码/适配方案或时间轴规范化足以解决目标工作流。CFR重采样可能改变重复帧、像素和成本，后续若比较须完整计入；本轮未实现或测试。
- 尚无任务级收益、相同资源下的强比较或超出现有修复的技术增量。不能只靠公式反例、增加字段或新测试集宣称核心期刊贡献。
- 《Frames Don’t Add Up》的原OpenReview入口本轮仍返回验证页，未获得全文；不以搜索片段排除其覆盖范围，也不将Meta-Video误认作同一论文。

因此本轮只保留公开源码边界与先例记录，**不下达042，不恢复041或图形时钟变体，不启动新媒体/QA/GPU/训练/安装，也不发Issue、PR或投稿**。接下来只有在真实用途、已有方案剩余缺口与可测收益同时明确时才形成正式实验合同；此句不是新的执行授权。

041与040原裁决、144格选帧候选/路径交接PARKED、NOVELTY=RETAIN0、NATURAL_VIDEO_EFFECT_UNKNOWN、原C/D及038–039停止、TRAIN-GPU HOLD、CLOCK_ZERO_ASSUMED_NOT_CERTIFIED、Charades FINAL_MEDIA_STOP均保持。

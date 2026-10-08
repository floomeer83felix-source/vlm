# VLM-BATCH-004 A：VES-Bench许可与无答案字段请求草案

日期：2026-10-08。**仅供用户审阅，未发送邮件、Issue或私信；官方联系地址在已批准材料中未确认，收件地址UNKNOWN，不猜邮箱。**

已见事实来自[VLM-002](../VLM-002/dataset-metadata-review.md)：[TRACE仓库](https://github.com/buaa-colalab/TRACE/tree/1b60646dd37657e01b66060bc637742e5d4b5db7)说明联合必要证据集；[VES-Bench revision](https://huggingface.co/datasets/buaaplay/VES-Bench/tree/b1cdbb370ad866090e6fec82ccb9e699b10edbc7)目录可见。实际问答区间字典、注释／视频许可及同版时间桥接仍未确认；本轮没有重新访问数据站点。

## 中文邮件草案

**主题：VES-Bench本地非商业研究许可与无答案元数据确认**

TRACE／VES-Bench作者您好：

我们计划开展一项冻结VLM、固定12源帧的离线配对诊断，研究在相同参考支持下区间外背景组成的影响。目前仅做技术合同准备，尚未为该诊断下载视频或运行问答；项目此前的其他实验不作为这项诊断的验证。希望确认以下四项：

1. 问答注释与底层视频的许可是否分别允许本地非商业研究，以及发表脱敏聚合指标／方法描述？若需申请，请说明资格、流程与披露限制；网页公开本身不被我们视为许可。
2. 是否有**不含答案**的schema／字段字典，说明视频ID、正式问答split、联合必要参考区间的时间单位、闭开端点、区间数与必要性验证依据，以及注释所对应的媒体revision和裁剪／转码起点？
3. 是否有可核验的视频SHA或版本manifest、逐视频frame PTS／timebase说明、clip到上游parent视频的映射元数据？我们只请求定义与版本资料，不请求整套视频或带答案记录。
4. 在许可、源组关系或上述桥接无法确认时，我们将保持实验HOLD，不把文件名、FPS估计或覆盖区间解释为独立来源／充分视觉证据。

感谢您提供最小可公开的说明或正式申请入口。此消息须由用户确认联系方式和内容后自行决定是否发送。

## English draft

**Subject: VES-Bench permissions and answer-free metadata for local non-commercial research**

Dear TRACE / VES-Bench authors,

We are preparing an offline paired diagnostic with a frozen VLM and 12 source frames, comparing background composition while retaining the same reference support. No videos have been downloaded for this proposed diagnostic and it has not been run; earlier project experiments do not validate it. Could you clarify:

1. The separate annotation and underlying-video permissions for local non-commercial research and publication of sanitized aggregate metrics/method descriptions, including any application requirements or disclosure restrictions.
2. An **answer-free schema/data dictionary** covering video IDs, official QA splits, jointly necessary evidence intervals (units, endpoint semantics, counts and necessity-validation criteria), media revisions, and crop/transcode origins.
3. Available video hashes or version manifests, frame PTS/time-base specifications, and clip-to-parent mappings. We request metadata definitions and version information, not full videos or answer-bearing examples.
4. We will keep the experiment on HOLD while permissions, source grouping or coordinate mappings remain unverified; public access, filenames and nominal FPS are not treated as such verification.

Thank you for pointing us to the minimum public documentation or formal application route. The user will decide whether to send this draft after reviewing the contact channel and content.

## 状态

请求待确认／未发送；没有新联系事实、许可承诺、无答案样本或G1放行。实际发送邮件／Issue须用户另行授权；回复如包含完整标注或答案，也不得直接流入采样器。

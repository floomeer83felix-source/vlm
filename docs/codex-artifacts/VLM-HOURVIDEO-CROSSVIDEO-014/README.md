# VLM-HOURVIDEO-CROSSVIDEO-014｜多独立视频的冻结选帧方案复现，不用同一37题反复挑结果

**2026-10-15｜READY / AWAIT_USER_ADDITIONAL_MATCHED_VIDEOS（唯一READY、未具备执行数据与新的GPU授权）**。用户希望尽快推进有科研意义的VLM研究；前一[013](../VLM-HOURVIDEO-WHOLEVIDEO-QA-013/whole-video-provisional-qa-receipt.md)已得到同一官方demo上37个配对有金标题的**假设限定**结果，**不能因观察到B占优就重跑该视频来选最佳prompt/帧数/窗口/seed**。本父任务被冻结为最多3段**新且互相独立**合法官方视频的*验证/复现*，不是已获得第二段视频的声明。**收到用户在原Codex长期聊天明确提供新匹配媒体的精确本地入口及新最多258次Qwen本机generate、GPU合计≤30min授权之后才可执行；没有数据则不开始/不提交另一份空HOLD报告。**

## 固定上游结果和解释限制

- 013实际执行[bf5e36a](https://github.com/floomeer83felix-source/vlm/commit/bf5e36ad216c33e6cb04d2493c9e5fce050f7713)：43个同视频金标五选项中**预冻结排除6个辅助图像题**，剩37条纯视频/文本，uniform12 vs SigLIP问题文字top12；Qwen真实74/74成功、all natural EOS、GPU阶段31.906s、allocator峰8848.589MiB，0新模型或媒体下载、0训练步。**探索性、假设限定**：uniform **6/37=16.22%** vs SigLIP **12/37=32.43%**，同题配对both4/Aonly2/Bonly8/neither23；B-A **+6/37=+16.22pp**，描述性双侧exact McNemar **p=0.109375**，**未建立统计显著优越性**。目前只有**1条视频**，37条题不构成37条独立视频；来源同UID但发布时间零点桥仍`CLOCK_ZERO_ASSUMED_NOT_CERTIFIED`，不能称正式HourVideo leaderboard准确率/模型训练/算法优越。
- **013所有37条题及原demo视频视为development/已观察集合**：014不可用它们训练、调参、重新评价来选择配置，不能事后调prompt阈值/覆盖比例或根据013成绩挑适合的后续媒体。无法保证全HourVideo数据集完全未接触，但必须实施物理视频/UID相互分离和预冻结实验规则。

## 用户新提供数据以后，一轮最多3段新媒体的受限研究

1. **只读资格**。只沿用户下一条Codex消息给出的**最多3个明确绝对路径**读取已合法获得、完整、非reparse的HourVideo/Ego4D候选视频；另仅可读取在先前明确授权的私有dev_v1.0_annotations或官方samples_v1.0 gold入口及其**既有精确授权的**发布/时轴映射证据。绝不扫描Downloads/用户私人目录/整块SSD、访问旧受限part/Charades文件、从AWS/HTTP/HF/镜像下载、打开其它媒体。各源必须独立video_uid和不同原采集源，**不得复用013的官方demo UID或其任何相同实物转码/片段**。非法源/未获授权、无匹配带gold五选项/长度过短/视频不能解码等直接HOLD，不拿1920电影代替。
2. **视频与标签相容性**。本轮固定继续只做*整视频可见内容*相关文本五选项MCQ，不用任何`relevant_timestamps`字段、答案、原视频时间零点映射进行采样或挑帧。至少有用户授权的source/UID一致性、可复核合法来源、≥1,200秒真实PTS且整个视频实际覆盖准许全片问题的必要证据；如来自不同Ego4D release、可能剪裁同长度/PTS零点未知，则标`CLOCK_ZERO_ASSUMED_NOT_CERTIFIED`并且结果**只能作为假设限定探索性复现**，不能归纳正式HourVideo评测或合并已认证时钟的样本；若内容/源身份同源无法支持则`MEDIA_CONTENT_MAPPING_HOLD`，0 GPU。仍优先真正同源官方发布包/带不可变映射凭证的完整视频。
3. **严格锁死方法**。直接复用013冻结的两臂模型资产（本地Qwen3-VL-4B-Instruct BF16、SigLIP base双塔 F32、相同processor、`do_sample=False`、max_new_tokens64、同输出解析规则和同MCQ A–E单字母指令），每个媒体从其自身PTS均匀48真实候选帧、A uniform12、B question-only SigLIP cosine top12、恢复PTS，全部在同一Qwen上paired固定交错顺序；不动13的input pixel/grid/text规则、不加时间覆盖约束/权重混合/视频知识提示、不引入其他模型。先用与013相同的非gold schema规则排除外部辅助视觉资产题；题目按原索引稳定顺序，**每新视频最多43条**，若视频本身题目数量不同照实际N预冻结，且**所有合格题纳入配对、n不随是否答对而变**。答题金标须独立评分器在全部生成完后使用；SigLIP query只能问题原文，不能把选项或gold偷偷拼接。
4. **防过拟合统计**。先按每视频分别给出正确/N、A_only/B_only/neither/both与invalid/notrun、帧覆盖和计算成本；再在**有至少2段新相互独立视频真实完成、每段至少10道合格题**时，才给跨视频汇总的*描述性*macro accuracy、宏平均配对差与视频级变化方向；不可把题视作独立采集对象来假报可靠显著。若总共只有1条新视频完成，则明确`SINGLE_ADDITIONAL_VIDEO_EXPLORATORY_REPLICATION`，不宣称跨视频验证完成；如果≥3新视频且合理适用，报告不做选择性的每视频全部结果与不确定性，仍不能仅靠3视频声称论文创新/正式总榜。不得为了符合观察到的差异多跑几次或补“更有利的视频”。
5. **硬资源**：下一条用户消息须清楚授予**最多3新视频、总Qwen实际generate attempts≤258（3×43×2）、本轮RTX3090 GPU所有加载/检索/生成合计≤30分钟、框架新增allocated≤20GiB、父任务单调墙钟≤60分钟**；CPU每片有限定PTS抽样，避免重解码所有旧数据。GPU前两个≥2秒间隔资源快照free≥8GiB/util≤30%和任务自有互斥无冲突，按之前安全门只监护自有子进程。任何OOM/超时/加载问题一次STOP、**不重试已生成题目、不得擅自降帧或缩小模型**，未完成题进入预冻结分母，其他尚未开始的视频也记录NOT_RUN。仅已获准本地模型与标注文件，零视频/权重/云网络请求，零依赖安装或系统修改。

## 科研结果与公开交付边界

- 与013实验必须严格分开：013统计的37道题是已看过的开发数据，014只在新UID与新物理采集源上进行预冻结复现；对有独立时间轴/版本证据的视频可以更强描述，其余仍加`CLOCK_ZERO_ASSUMED_NOT_CERTIFIED`，任何未证实的零点/发布差异不能被填造为PASS。Qwen/SigLIP推理属于模型评测而非训练，无Qwen/LoRA梯度；不能声称在整个HourVideo dev或独立测试集上达到新的准确率、SOTA或显著创新。Charades`FINAL_MEDIA_STOP`、`NOVELTY=RETAIN0`持续。
- 如果用户提供媒体且本父任务实际执行，仅许新增`docs/codex-artifacts/VLM-HOURVIDEO-CROSSVIDEO-014/crossvideo-heldout-receipt.md`以及在`docs/codex-results.md`尾追加恰一条`### VLM-HOURVIDEO-CROSSVIDEO-014`，单次正常main push后STOP；匿名报告全数目/权限/证据等级、每视频以`video-1/2/3`**匿名类别**汇总成绩（不能输出私有UID、媒体路径、文件名、题目、金标、预测、哈希）、配对统计、invalid/notrun、采样覆盖、Qwen次数、GPU耗时/峰值VRAM及局限。旧012/013视频与私有题库/账本不更改，不重复历史训练或Qwen推理。**没有新的合法具体媒体入口及新GPU授权前，本014保持AWAIT，不运行、不交空报告。**

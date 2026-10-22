# 时间码与视觉身份绑定：最小可识别诊断设计 — 2026-10-22

ChatGPT研究负责人。承接[037正式处置](../research-decisions/post-037-scientific-disposition-2026-10-22.md)。
**新候选问题：CONDITIONAL_MEASUREMENT_PILOT_ONLY；NOVELTY=RETAIN0；尚未执行。**
不是恢复C/D选帧主线，不保证形成论文新机制；下列推导和预期标签不是模型实测结果。
本新设计完成后，以最新board/038合同替换037结案时“重设计期间0 READY”的历史状态；
037对原C/D的停投裁决与旧run关闭状态不变。

## 1. 为什么保留这个问题，而不再实现一个选帧器

问题：**固定所见像素、帧顺序和帧数，只改变合法、实际进入模型输入的时间码时，
Qwen能否把视觉标记与其时间码绑定，正确求间隔；能否同时满足“局部时间变化应响应”和“整体平移应不变”？**

研究对象由选帧策略改为已呈现证据中的视觉身份—时间码结合。
首轮用完全自有、程序化真值的短合成序列，省去真实事件实例、媒体时钟桥接及缺失原标注的歧义。
这不会证明自然长视频或复杂事件推理；若这个受限测量本身无信息，就停止，不扩成新benchmark工程。

科学负责人已定向读原始材料，筛去：
- “长视频主要是搜索瓶颈”：ExtremeWhenBench已直接研究search/localize分解；
- “定位所有满足条件的重复事件”：Conditional Multi-Event Grounding已有近邻；
- “任意反转后不改答案说明时间盲”：037已经指出标签语义错误，且既有工作广泛覆盖反转/一致性。
  上述阅读不构成对全部方法的穷尽等价证明。

保留的窄差异是**同像素/同索引位置＋相同全局时长的非均匀局部时钟改变，
与整体平移负控制、逐条件文字算术对照配对**。
在已读方法段中尚未确认完全相同的因子设计，但这只是定向检索的UNKNOWN，
不是“首次”或新颖性PASS。若有直接同设计先例，本轮应标DIRECT_DUPLICATE，不制造新名词。

## 2. 原始近邻与本设计的边界

| 原始出处与实读重点 | 已有内容 | 本轮可说的区别/不能说的结论 |
|---|---|---|
| [Jung等，CVPR2025版本方法§3.2](https://arxiv.org/html/2411.12951v1) | 将视频片段搬到新时间位置，做shift/rephrase与ground/verify一致性测试 | 一般时序一致性不是创新；本轮固定呈现RGB与索引位置，操纵合法时间映射，不能声称首次时序扰动 |
| [SVLTA，CVPR2025，§3–4](https://arxiv.org/html/2504.05925v1) | 仿真活动、程序化时刻真值、持续时间/排列和分布偏移，评估时间定位 | 合成真值/时间对齐不是创新；本轮诊断时间码条件与视觉身份配对，不复现其活动benchmark，不声称已排除它的全部变体 |
| [SpookyBench v2，§3及§4.3](https://arxiv.org/html/2505.24867v2) | 隐藏单帧空间信号，测试仅由动态编码的信息及FPS影响 | 本轮故意让单帧颜色非常容易，测试另一种信息结合；不能据此宣称研究纯运动知觉 |
| [VCBench，§3](https://arxiv.org/html/2411.09105v1) | 程序生成可控符号视频、颜色/形状/动作和认知任务 | 程序化符号视频不是新贡献；本轮只有小型配对探针，不作为新大型基准发布 |
| [ExtremeWhenBench v1，§3–4](https://arxiv.org/html/2606.12300v1) | 小时级query检索与局部定位分解 | 已覆盖搜索瓶颈；本轮不给检索增加预算，不用短序列成绩替代小时级证据 |
| [Conditional Multi-Event Grounding v1](https://arxiv.org/html/2606.15320v1) | 条件组合下多事件定位/计数 | 已有重复事件相关研究；本轮只用唯一简单标记，不能声称解决真实重复实例 |

以上比较为研究负责人推断，未在本机运行近邻；预印本状态不推定同行评审。
本轮不做邻居排行榜，不把无新数据下载当新颖性证据，不增加广综述任务。

## 3. 为什么必须先核processor，而不是直接GPU

已核Hugging Face官方源码，读取日期2026-10-22，upstream commit
`360d22e2d1183af882ad437bfc74ce3337065f5d`：
[processing_qwen3_vl.py](https://github.com/huggingface/transformers/blob/360d22e2d1183af882ad437bfc74ce3337065f5d/src/transformers/models/qwen3_vl/processing_qwen3_vl.py)
与[video_processing_qwen3_vl.py](https://github.com/huggingface/transformers/blob/360d22e2d1183af882ad437bfc74ce3337065f5d/src/transformers/models/qwen3_vl/video_processing_qwen3_vl.py)。
观察到通过frames_indices/fps计算时间码、相邻temporal patch首尾时刻取均值，
并将时间码作为文本插入视频块；缺fps会fallback，因此本轮必须显式给fps。
这只是upstream实现证据，**不证明用户已安装版本相同**。

本机先只加载CPU processor/tokenizer：
- 核安装版本和至多3个确切模块源码；不安装/升级/换环境。
- 显式传预采样12帧、禁二次采样、保留指定indices/fps；不手改input_ids/拼接伪时间码绕过原processor。
- 实际解码输入验证六个时间码，核RGB/视觉tensor在同一world的G0/G1/G2完全相同；
  question文本相同，时间文本按设计变化，grid=[6,12,18]、324 visual tokens，
  允许时间数字使总文本token数变化。不能用旧036回执填本轮数据。
- 若本机接口不支持、丢弃/重置indices、时间码未暴露或视觉tensor意外变化，记
  INPUT_NOT_IDENTIFIED/HOLD，模型权重/GPU/generate0；不能把它记为模型时间能力失败。

## 4. 完整冻结刺激、时间码与48槽

### 4.1 自有画面及虚拟源时钟

12 RGB帧、uint8、192×288；按相邻两帧成六块k=0..5，每块两帧像素完全相同。
背景RGB=(16,16,16)，中央正方形x∈[96,192)、y∈[48,144)：
默认RGB=(96,96,96)，红标记=(240,32,32)，蓝标记=(32,64,240)。
无文字、数字、闪烁噪声或隐藏时间水印。四组标记块位置及两个颜色分配组成8个world：

```text
p=0:(1,3), p=1:(1,4), p=2:(2,3), p=3:(2,4)
c=0: earlier block red, later blue
c=1: earlier block blue, later red
world index w=2*p+c
```

每种颜色仅出现在其一块的两个帧中，消除重复实例/端点选择歧义。
不读取现有视频/frames/真实QA，不借用SpookyBench/VCBench/SVLTA的资产。
这是程序定义的虚拟源：fps=1，各未采样源帧均为灰色；
采样indices和源时长如下，未生成/保存MP4，也不做视频解码。
三个条件对应不同但合法的虚拟时间线，不能称“对同一真实视频伪造metadata”。

| 条件 | 六组原始frame indices（每组2帧） | 预期六个显示时间码，秒 | total frames / duration |
|---|---|---|---|
| G0 均匀 | (0,1),(4,5),(8,9),(12,13),(16,17),(20,21) | .5,4.5,8.5,12.5,16.5,20.5 | 22 / 22s |
| G1 局部非均匀 | (0,1),(2,3),(6,7),(14,15),(18,19),(20,21) | .5,2.5,6.5,14.5,18.5,20.5 | 22 / 22s |
| G2 整体平移 | G0每个index＋60 | 60.5,64.5,68.5,72.5,76.5,80.5 | 82 / 82s |

G0/G1固定总源时长、端点、像素和所见顺序，仅改变内部合法采样时刻，
可反驳“只按帧序号/总时长算间隔”的解释。G2的间隔真值保持不变；
它是时间原点负控制，源前缀/总时长不同，不能称所有metadata都固定。
问题只问所提供标记组的显示时间码差，不依赖未观测真实片段的事件存在。
两帧块均值均为.5结尾，避免0.1s格式化导致标签不可区分。

### 4.2 两条输入通道与唯一模板

系统提示均为：`You are a helpful assistant.`，不使用旧科学任务的选项字母系统提示。

V视频条件固定英文问题：
```text
Using the timestamps attached to the red square and the blue square in the provided video, what is their absolute time difference in seconds? Output only a non-negative integer.
```

O文字算术对照，对**每个world及每个G**各一槽，无图/无video tokens：
```text
The red square has timestamp {red:.1f} seconds. The blue square has timestamp {blue:.1f} seconds. What is their absolute time difference in seconds? Output only a non-negative integer.
```

O明确给出操作数，是component control，不是与V信息/成本相同的竞争算法。
即使O对V错，也只能指向视觉定位/时间码读取或结合链的行为缺口，不能单凭此断定某神经模块原因。
不额外加CoT/多选项/追问/重答，不按输出改prompt。

| p及位置 | G0/G2准确整数 | G1准确整数 |
|---|---:|---:|
| 0:(1,3) | 8 | 12 |
| 1:(1,4) | 12 | 16 |
| 2:(2,3) | 4 | 8 |
| 3:(2,4) | 8 | 12 |

色彩互换不改绝对间隔。真值由源indices/fps及双帧均值解析得出，
独立CPU评分再从冻结spec推导核对，不使用模型判分或新人工标签。
这测的是显示时间码结合/间隔计算，不把它改称复杂自然事件或未知先后理解。

8 world ×3 clocks ×2 channels = **48个全新槽**（24 V、24 O）。
每world基础顺序[V0,V1,V2,O0,O1,O2]左旋w mod6，按w=0..7串行；
唯一slot id=6*w+执行序号。先冻结完整manifest/spec/hash/输出解析，再任何模型加载。
不按第一槽成绩删源、改样本或选择后续条件。

## 5. 主要观测、失败解释与停止条件

- **输入识别**：V同world三clock的RGB/视觉tensor完全同，
  原生显示六时间码符合表，完整输入差异只来源于时钟文本及其派生长度/attention信息；
  O每clock操作数相应一致。缺一不做模型效果归因。
- **主要描述量**：V0/V1联合正确及预测间隔变化是否等于预定+4，
  V0/V2联合正确及平移不变性。两者都报告“联合正确”和仅“关系一致”，
  错两次但同差/同答不能算能力通过。
- **匹配分解**：逐world/clock列V/O正确性、INVALID/FAILED/NOT_RUN；
  算术控制失败时对应V失败的细分归因UNKNOWN，不剔除该world或补一个更容易的题。
- 输出strip后必须完整匹配`[0-9]{1,3}`，再转整数；
  其他文本/单位/理由为INVALID；截断/EOS/原token数保留，不后处理成成功。
- 全48终态与真实模型PID/Job退出后才运行一次CPU scorer。
  固定每condition planned=8和全部48状态；不把NOT_RUN写成已观测答错。
  未全完成时主配对项给已知/未知数量和原因，不以完成子集替换计划分母。
- 只有4种基础位置组、颜色互换为依赖重复；没有8个独立自然来源，
  没有统计功效/显著性、跨模型/自然长视频泛化或模型训练域独立性证明。
  所有数字仅描述这一个冻结构造。

预先固定本轮结束后的解释：
1. 输入门失败：停止当前表示实现，HOLD_INPUT；不称模型失败、不自动补接口/加图像提示绕过。
2. V/O都顺利且全对：本探针未见目标行为缺陷，停止以此缺陷为前提的扩大投入。
3. O正确而V在clock响应/平移上失败：记录候选行为现象，最多DEVELOPMENT_PROBE_OBSERVED；
   先复核输入/定位/格式与最近邻，不自动训练、扩样或认定新机制。
4. O也失败或输出格式普遍无效：算术/指令混杂未分离，归因UNKNOWN，停止调prompt救结果。
5. GPU/资源/进程失败：保留实施状态，不作科学阴性，不继承旧预算补run。

一次pilot的阴性或阳性都不证明全部时间绑定方法有效/无效。
任何后续确认必须在查看独立结果前冻结新刺激/来源/模型/停止规则，
不得把用于选择方向的本轮结果再当独立确认。NOVELTY始终RETAIN0，直到有额外创新证据。

## 6. 预算与新权限

执行合同为[VLM-CLOCK-BINDING-PROBE-038](../codex-artifacts/VLM-CLOCK-BINDING-PROBE-038/README.md)。
公开READY仅实现许可；用户在当前本地Codex发送完整第6节消息，才激活本轮新合成/本机模型范围：
新48generate、单worker/GPU600s、CPU480s/父1800s；
原真实标注/frames/QA/gold、下载、解码、训练与安装均0。
短合成pilot不自动升级原C/D/HourVideo/Charades或新论文路线。

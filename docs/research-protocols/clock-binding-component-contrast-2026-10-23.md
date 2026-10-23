# 039：时间码读出、间隔组合与输入呈现的分量对照

2026-10-23（北京时间）。研究负责人在038结果已公开后冻结的**探索性判别设计**。
执行合同：[VLM-CLOCK-COMPONENTS-039](../codex-artifacts/VLM-CLOCK-COMPONENTS-039/README.md)。
**未执行；不是确认性复现、论文新算法或训练方案。NOVELTY=RETAIN0。**

## 1. 为什么值得这一轮

[038公开结果](../codex-artifacts/VLM-CLOCK-BINDING-PROBE-038/scientific-results.md)
实际48次生成：视频间隔3/24、匹配文字算术22/24；视频时钟局部响应与平移关系均0/8。
实际CPU与最终BF16输入绑定支持“时钟干预进入输入”，不支持唯一神经归因。
目前仍混合了颜色位置识别、时间码读出、角色结合、计算/输出和输入呈现。
只重复更多间隔题不能有效拆开这些解释。

本轮问：同一新world/clock中，直接读出两个角色的时刻、直接回答间隔、
把相同时刻印在空间拼图上，以及显式文字算术，会出现怎样的配对差异？
五任务独立生成；不把读出回复作为另一任务输入，不提出read-then-regenerate算法。

## 2. 先例与贡献边界

- [Jung等，On the Consistency of Video Large Language Models in Temporal Comprehension，
  2024，§3.2](https://arxiv.org/html/2411.12951v1)：已经研究时移、改写及grounding/verification任务一致性。
  跨任务回答矛盾与时移探针不是这里的新概念。
- [Wu等，Number it: Temporal Grounding Videos like Flipping Manga，
  CVPR2025](https://openaccess.thecvf.com/content/CVPR2025/html/Wu_Number_it_Temporal_Grounding_Videos_like_Flipping_Manga_CVPR_2025_paper.html)：
  NumPro已经用画面数值标识辅助时序定位。这里带时间码拼图只是已知思路的呈现对照，
  不能把它包装为新方法，也没有复现其完整评测/训练或排除其变体。
- [Du等，MLLMs Know When Before Speaking，2026-05-21预印本，
  摘要及§3–4](https://arxiv.org/html/2605.21954v1)：作者报告attention/prefill与生成的时序定位差异，
  并提出attention引导再推理。本轮只有行为读出/计算对照，
  没有attention knockout、内部状态读出或因果定位；即使读出正确而间隔错误，也不能宣称发现相同内部机制。

这是一轮针对038剩余歧义的低成本分量判别，不是新颖性通过。
无自然视频、独立来源/跨模型验证，也没有认定“在所有先例中首次使用这组因子”。

## 3. 冻结刺激与时钟

保留038自有图形规范：12帧uint8 RGB，单帧H192×W288，六个temporal块，
块k包含完全相同的帧2k、2k+1。背景(16,16,16)；
中央方块x∈[96,192)、y∈[48,144)，默认灰(96,96,96)，
红(240,32,32)，蓝(32,64,240)。不读取真实媒体/原QA或标注。

用038**未测试过的四种位置组合**，索引从0开始：

| 基础组p | 两个有色temporal块(i,j) | G0间隔 | G1间隔 | G2间隔 | G1−G0 |
|---|---|---:|---:|---:|---:|
| 0 | (0,2) | 8 | 6 | 8 | −2 |
| 1 | (0,4) | 16 | 18 | 16 | +2 |
| 2 | (1,5) | 16 | 18 | 16 | +2 |
| 3 | (3,5) | 8 | 6 | 8 | −2 |

w=2p+c，c=0时红在i/蓝在j，c=1时蓝在i/红在j。
8 world只有4基础组及颜色互换依赖重复，不能说8个独立来源。
这些组事前按未用组合/覆盖端点/正负时钟响应选定，未按038哪些个例有利挑选。
仍复用模型、图形、时钟与部分模板，故是开发判别集，不是外部holdout或独立确认。

fps=1，raw frame indices：
- G0=[0,1,4,5,8,9,12,13,16,17,20,21]，total_num_frames=22，duration=22。
- G1=[0,1,2,3,6,7,14,15,18,19,20,21]，total_num_frames=22，duration=22。
- G2=[60,61,64,65,68,69,72,73,76,77,80,81]，total_num_frames=82，duration=82。

原生video显式传入这些VideoMetadata字段、fps=1、do_sample_frames=False、do_resize=False；
不使用缺fps fallback，不重采样或手工拼timecode/token。
每块时刻t_k为该双帧index均值/fps：
G0=[0.5,4.5,8.5,12.5,16.5,20.5]；
G1=[0.5,2.5,6.5,14.5,18.5,20.5]；G2=G0+60。
未采样时刻定义为灰色背景的自有虚拟源，不伪造真实视频metadata。
真值R=t_red、B=t_blue；间隔Y=|R−B|。角色交换只交换R/B，不改变Y。
程序真值直接由这些常量推导，无新人工标签。

## 4. 五个任务、120个固定槽

系统提示固定为 `You are a helpful assistant.`。
下列英文问题空格连接为单行；OG只做指定数值格式化。
不给模型world/clock/task ID、真值表或前槽回复。

| 任务 | 输入 | 要求 | 槽数 |
|---|---|---|---:|
| NG | 原生12帧video＋processor原生timecodes | 直接绝对间隔 | 24 |
| NR | 同NG的原生video | 红、蓝时刻的有序读出 | 24 |
| SG | 一张六面板带时间码拼图image | 直接绝对间隔 | 24 |
| SR | 同SG的image | 红、蓝时刻的有序读出 | 24 |
| OG | 显式给红/蓝时刻的纯文字 | 直接绝对间隔 | 24 |

NG（与038视频问题完全相同）：
```text
Using the timestamps attached to the red square and the blue square in the provided video, what is their absolute time difference in seconds? Output only a non-negative integer.
```
NR：
```text
Read the timestamp attached to the red square and the timestamp attached to the blue square in the provided video. Output only the red timestamp first and the blue timestamp second, each in seconds with one decimal place, separated by a comma and no spaces.
```
SG：
```text
The image contains six panels, each with a square and a printed timestamp in seconds. What is the absolute time difference between the printed timestamp for the red square and the printed timestamp for the blue square? Output only a non-negative integer.
```
SR：
```text
The image contains six panels, each with a square and a printed timestamp in seconds. Read the printed timestamp for the red square and the printed timestamp for the blue square. Output only the red timestamp first and the blue timestamp second, each in seconds with one decimal place, separated by a comma and no spaces.
```
OG（与038文字模板相同，R/B各一位小数）：
```text
The red square has timestamp {red:.1f} seconds. The blue square has timestamp {blue:.1f} seconds. What is their absolute time difference in seconds? Output only a non-negative integer.
```

每world固定基础序列：
[NG0,NG1,NG2,NR0,NR1,NR2,SG0,SG1,SG2,SR0,SR1,SR2,OG0,OG1,OG2]。
world按0…7执行；world内向左轮转(7w)%15，slot=15w+轮转后的执行序号。
共8×3×5=120唯一槽。每槽fresh messages/无跨槽KV或聊天历史；batch1，
同一Qwen3-VL-4B BF16/SDPA/eval/inference_mode，seed19，greedy，
max_new_tokens=16，完整输入≤2048 tokens。不warmup/额外forward、重启或重复已STARTED槽。

## 5. 拼图的像素规范及控制含义

取每temporal块的第一帧，即原帧0、2、4、6、8、10；
不重新检索/选帧。按k从0到5排列成两行三列，面板不加间隙/边框：
全图H384×W864 RGB，面板k原点(row=floor(k/3)×192,col=(k%3)×288)。
复制该192×288原帧，在局部(x=16,y=8)绘制该块t_k的一位小数字符串，
无单位/额外编号或标签。字体为附录固定5×7位图，整数scale=4，
字符起点advance=24；1位画(240,240,240)，0位保留原像素。
文字28像素高，最高y<36，不覆盖y≥48的方块。不得按回答改字号、版式或色彩。

预期原生video grid=[6,12,18]、324个video tokens；
image grid=[1,24,54]、324个image tokens。do_resize=False，
image由原生image processor编码，不伪装成video。
原生image processor如需在其内部复制temporal patch，记录实际行为，不手造token。
**这些是必须实测的输入门，不是已观测值；不能达到即HOLD_INPUT/GPU0。**

两种呈现匹配的是视觉token数及源图形/数值，不是相同tensor、文本长度、信息编码或FLOPs。
拼图同时改变空间布局、位置编码及数值所在通道；更好表现只支持呈现敏感的行为，
不能唯一证明原生视频的某个内部模块失效，更不能把SG当公平新算法收益。

## 6. CPU暴露与输入绑定门

逐槽构造并释放实际输入，CPU不载模型权重/不初始化CUDA：
- 所有NG/NR：六个实际decoded native timecodes精确匹配；grid/token数满足上表。
  每world三clock及NG/NR的原始RGB和最终BF16视觉tensor均相同。
  对同一个任务，去除六个原生timecode字符串后的文本完全相同；
  不要求NG与NR问题文本相同。
- SG/SR同world/clock的完整image及视觉tensor相同。
  跨clock只有固定字形绘制区域允许变化，方块/面板复制和其他像素不变；
  实际image grid/token数正确，text中没有R/B的数值操作数或隐含答案。
- OG无视觉tensor/视觉token，R/B数值与本轮world/clock匹配。
- 绑定覆盖全部tensor的key/shape/dtype/内容；visual分区同时识别
  pixel_values、image_grid_thw、pixel_values_videos、video_grid_thw。
  不可沿用“video keys之外都算text”的旧分区。
  CPU按最终BF16转换生成签名，模型worker重建后匹配，且实际CUDA输入dtype/内容再绑定后才STARTED。
  code/spec/queue/model config和逐槽输入receipt同属一个冻结run。

只允许一次有确切安装源码依据的API兼容修复、用剩余suite/CPU预检验证；
不改位置/clock/prompt/font/任务/分母绕过输入门。门前生成数始终0。
原生video可读文字是processor提供的原生时间码；image的数值只来自规定像素；
不得把目标时刻另填进NG/NR/SG/SR问题。

## 7. 冻结解析与统计

先strip整段回答；NG/SG/OG须全匹配ASCII `[0-9]{1,3}`。
NR/SR须全匹配ASCII `([0-9]{1,3}\.[0-9]),([0-9]{1,3}\.[0-9])`；
不准内部空格、单位、解释、额外数字或修复格式。分数采用十分之一秒整数/精确数，
不通过近似四舍五入制造正确。非.5数字仍可合法解析但按数值判错，不伪装成格式无效。

全120 planned保留；RETURNED为合法解析，坏格式单记INVALID，异常FAILED，
未调用NOT_RUN。所有状态分任务/clock报告，未知不装作观测错误。
主要表每task/clock分母固定8，共15格，不筛OG正确/颜色容易的子集作主要成绩。

必须完整公开120个自有合成小结果（world/clock/task、状态、规范解析值、EOS/截断），
无需公开私人trace/完整自然QA。统计至少：
1. NG/SG/OG精确间隔正确数；NG与OG、SG与OG、NG与SG的both/仅左/仅右/neither/unknown。
2. NR/SR的红正确、蓝正确、两角色同时正确；双值正好角色交换；
   两预测都属于六个真实时刻但关联错误；存在off-grid数值。诊断可重叠，注明分母。
   CPU从读出对导出的绝对差正确数单独列；角色全错而差值对不能称绑定正确。
3. 对每一world/clock事前列出
   C=(NR两角色正确且NG错误且OG正确)，
   P=(SR两角色正确且SG正确且NR两角色未全对且NG错误且OG正确)。
   格式错误是观测失败；任一关键任务未执行/FAILED则该比较UNKNOWN。
   报全24格及4基础组两种颜色分别的分布，不用事后有利子集替代全表。
   C最多为跨任务组合/读出行为差异；P最多为呈现敏感行为。
   不据此认定“模型隐含知道时间”或宣称唯一因果机制。
4. NG/SG/OG分别报告G0→G1的有符号差值[-2,+2,+2,-2]（按p）
   及G0→G2间隔不变：端点两槽同时正确与仅关系满足分开。
   NR/SR还报告G0→G2两字段分别+60，以及角色同时正确与仅变换满足。
   无合法数值时不能计算关系，列未知，不把错误一致当正确。
5. 按4基础组及颜色交换报告，不作独立样本显著性/p值或自然长视频推广。
   与038只作描述，不合并为独立样本或拿新几何的准确率变化当干预因果效应。

## 8. 事前解释与停止

- 输入未识别：HOLD_INPUT，不能把未运行算模型时间能力负结果。
- OG错误：该格仍混合算术/指令问题，不以只报OG正确格消除混杂。
- NR正确而NG错误且OG正确：支持C行为，任务提示不同，不能推断NG内部曾读对。
- SR与SG都正确、原生对应失败且OG正确：支持P行为，空间布局/OCR/通道等仍混合；
  SR失败意味着拼图正对照未在该格验证，不能断言原生接口独有缺陷。
- 五任务都成功或C/P不出现，也必须结案；不再靠换font/prompt/clock持续找失败。
- 单一依赖图形家族只能成为LOCAL_DIAGNOSTIC_ONLY。出现C/P也只保留待解释现象，
  尚无算法/机制创新通过。本轮不设置按有利数值自动扩样/再训练的门。

039只安排这一轮分量判别；交付即STOP。研究负责人再判断这些行为是否值得另立独立问题；
若仍不能排除普通读数/指令/呈现解释，则停止合成变体投入。
自然长视频效应UNKNOWN、旧C/D核心NO_GO、TRAIN-GPU HOLD、
原真实媒体CLOCK_ZERO_ASSUMED_NOT_CERTIFIED、Charades FINAL_MEDIA_STOP保持。

## 附录：固定位图字体

每项七行以/分隔，从上到下、从左到右；scale/位置规则见第5节。
```text
0 01110/10001/10011/10101/11001/10001/01110
1 00100/01100/00100/00100/00100/00100/01110
2 01110/10001/00001/00010/00100/01000/11111
3 11110/00001/00001/01110/00001/00001/11110
4 00010/00110/01010/10010/11111/00010/00010
5 11111/10000/10000/11110/00001/00001/11110
6 01110/10000/10000/11110/10001/10001/01110
7 11111/00001/00010/00100/01000/01000/01000
8 01110/10001/10001/01110/10001/10001/01110
9 01110/10001/10001/01111/00001/00001/01110
. 00000/00000/00000/00000/00000/00100/00100
```

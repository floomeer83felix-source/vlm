# 045负责人验收：原生PTS链路的限定CPU原型通过

2026-10-25（北京时间）。执行提交[8f648e8](https://github.com/floomeer83felix-source/vlm/commit/8f648e875e8339fe2fb3c1c78dea9ef2df64bc30)。
**ACCEPTED_CPU_NATIVE_PTS_BOUNDARY_PROTOTYPE / NATURAL_MEDIA_AND_TASK_EFFECT_UNKNOWN / 045_CLOSED。**
依据：[CPU边界回执](../codex-artifacts/VLM-NATIVE-PTS-ADAPTER-045/processor-boundary-receipt.md)、
[完整9槽CSV](../codex-artifacts/VLM-NATIVE-PTS-ADAPTER-045/input-boundaries.csv)。

## 1. 独立审查与复算

- GitHub比较恰好五个允许路径，results仅追加10行；合同、旧代码/证据及规划未由执行者改动。
  逐读新核心244行、验证器99行；代码SHA256分别独立计算匹配封存：
  605b6299ce397a90d51509a0debf2a113dd5269890ff47f5e0813ece8fef7f94、
  e65909a05c38c0d48bb88e25f715a219cccd56ea4ad1aa0de4cc083fee109efd。
- 新类调用继承的原生__call__，只在_calculate_timestamps计算处使用不可变source index→Fraction PTS。
  原indices/fps/merge在实际回调核对；没有修改安装库、base方法、tokenizer或最终input_ids/attention。
  串行A→B→新显式A及适配后native关系通过；不声明并发安全。
- 使用标准库csv/json/Fraction/struct独立复算9行，无Torch/模型或原测试重跑。
  索引由独立divmod舍入生成；24个未量化均值与实际原生时码逐行一致，fps=1、merge=2、每槽实际回调1次，
  状态9 PASS、FAIL/UNKNOWN/NOT_RUN均0。
- 以公开input_ids、attention与grid值重建int64连续字节SHA；逐行核形状/CPU dtype/device、attention全1、grid[[24,12,18]]及1296视觉tokens。
  全部四个实际返回kwargs纳入完整签名，共同base配置身份前后不变；完整hash和视觉子集hash独立重算一致。
  BF16视觉直接torch.equal由执行者实测；公开视觉shape/dtype/hash一致已核，负责人未独立重算原始视觉tensor。
- 按公开ID序列的24个视觉块及前置时码区域分段，其他token序列一致；tokenizer decode/encode roundtrip为执行者实测，
  未由负责人重新加载私有tokenizer。文本token长度分别1532、1530、1533，不能用同1296视觉tokens推定相同总计算。

## 2. 已成立的输入关系

| 关系 | 独立核查 |
|---|---|
| Q02=P/CFR vs Q01=native/CFR | 完整输入相同 |
| Q03=native/A、Q06=适配后的native/A、Q08=native/Q vs Q01 | 完整输入相同 |
| Q04=P/A vs Q03，Q05=P/B vs Q04 | 视觉相同，仅预期原生时码区域的文本输入不同 |
| Q07=新显式P/A vs Q04 | 完整输入相同，未继承B |
| Q09=P/Q vs Q08 | 未量化差为首patch 1/200秒、其余23个各1/100秒；原生量化差全0，完整输入相同 |

9个实际预处理槽只有3个完整输入等价类：
[Q01,Q02,Q03,Q06,Q08,Q09]、[Q04,Q07]、[Q05]。
这是受控输入关系，不是9个或3个模型/视频观测；模型调用0，量化相同也不是模型不敏感。

## 3. 资源、异常与验收边界

初次纯计算43项通过后，库bootstrap的可选PyAV导入因guard抛PermissionError而失败，
未加载processor资产或执行processor。根据确切源码改为ImportError仍保持解码器不可用；
唯一修复轮纯计算44项通过。初始失败与资源保留，不是将两轮加为87个独立研究结果。
当前单worker加载资产一次，1探针+9正式=10/12实际调用，正式无重跑。
四阶段outer wall独立相加为110.0447841秒≤600；当前worker80.3304963秒≤300。
峰Job1388044288B、父1425.507秒、29文件/952918B及actual active0由执行者报告，与公开可核部分相容。
初始失败worker未到CUDA初始化断言，不补签其动态断言通过；当前worker实测未初始化，源码未见模型/设备调用。

已安装目标源码与固定Transformers4.57.6一致；明确API源码检查3文件/102520B在范围内。
目录驻留快照不是卷级配额或累计写入峰值证明；负责人未访问Windows、原始Job日志、现有资产或旧私有根。
本轮应用网络、媒体/解码、标签、权重、模型加载/forward/generate、GPU与安装均未运行。

**045按声明的原型范围验收通过。** 代码硬限定96个源index、96秒metadata、48输入帧与merge2，
不宜直接当180–900秒任意自然原片的生产适配；未来需结合明确真实资产验证/参数化F、T、索引与PTS映射，不能只改常量宣称通用资格。
本次关闭了“原生回调能否承载PTS并保持视觉输入”的窄实现疑问，不关闭自然数据/任务输入门。

## 4. 后续裁决

045已消费不可重跑；当前0 READY，不自动046、不继续纯受控时钟变体或为填表重跑。
044当前直接获取路线仍暂停，042–044旧partial及预算责任不变；不续传、加时或换候选再下载。
下一实质输入仍是确切已有完整合法原片及来源/版本依据，或不同可得实物来源；
私人路径留本地，不搜索旧盘/私有日志来填输入。
仍缺实际显示时钟/原点/编辑、源独立性、标签同钟、重复动作题目身份、强N基线及真实任务效果，
故64格/GPU仍HOLD。NOVELTY=RETAIN0，既有科学/训练/媒体停止结论保持。

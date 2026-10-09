# VLM-BATCH-012：固定ZIP官方评测器与三层合同

2026-10-09，main72eee14。本轮修复的是**两种判定口径混用**，不是编辑Charades标注。官方标签采样规则已由同ZIP源码确定并构造标准库模拟；端点质量与事件真值独立HOLD。未执行MATLAB、下载、提取脚本或运行任何模型。

## 1. 权限、入口与字节来源

重新读取唯一READY任务、AGENTS、结果、安全协议及010/011记录。固定根仍为`%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-Metadata\`，原源树只读。调用已审check_ancestors核逻辑／规范路径身份、双祖先链无reparse／稳定性，并核LOCALAPPDATA包含。ZIP、两CSV及类表分别与任务固定SHA一致，未重下／解压／更新manifest。

| 对象 | 实测固定SHA256 |
|---|---|
| ZIP | `c616913ef79c2ddde06d9c562eae57bb8901d459d7568a0d27bf09cbf33ae866` |
| Train | `59273c6dc2139ec7eb95b980fd26bc8529774b1ede0602f6ca90b546ed12f0fc` |
| Test | `8b8b207b55fb95b949018027f69d83bd46cd844d15834f8f592ee8e7446173eb` |
| 类表 | `7b95127e60300d6a69849d161869eb3e9657fa320fc9e92b6f2c9403b49c1887` |

只读检查完整central directory的路径／名字／类型／大小／碰撞／加密等安全属性，再选择**唯一严格basename**为Charades_v1_localize.m的成员。目标4,649B、155行、UTF-8可解码、SHA256 **`83eb3a2f30c87cc45db76235886f8d5331edb943acfdee8bab5656c5d51e0096`**；以z.open有界读取并通过目标CRC。全ZIP完整性沿010固定SHA及其CRC收据，本轮不重新打开其余脚本内容；没有写出.m或发布完整源码／成员清单。

## 2. 官方实现的可核依据（只给极短表达式）

行号属于上述固定成员字节，不是网上另一修订。以下是源码释义与极短表达式，不复制完整函数。

| 代码锚点 | 已确认语义 |
|---|---|
| L1、L76、L100 | 主函数、AP辅助函数THUMOSeventclspr、CSV定位标签加载函数均在同文件；标签构造不需外部标签生成脚本 |
| L22／L24 | 25时间点、157类别 |
| L105—114 | 从真实header建立字段位置，以带引号CSV格式读取；不是固定第10列、不是以文件行推定事件 |
| L120／L123—133 | 本地uncell辅助、读取id/actions/length，length转double，按分号解析数值class/start/end；空actions保持无动作 |
| L135—138 | MATLAB j=1…25，时间为**`(j-1)/25*L`**；Python零基j=0…24需保持先除后乘 |
| L139—143 | 对所有动作逐一检查**`s<=t<=e`**，两端均inclusive，没有预先end≤L过滤，也没有要求s<e的质量门 |
| L146—148／L54—58 | 采样位置标号1…25；收集命中class，最终该cell赋1，因此同类重复／重叠按布尔OR而非累加 |
| L30—35／L59—66 | 预测分数另读submission，0基帧号有调整，缺预测与AP计算另有代码路径；本轮不模拟分数／AP，也无模型预测 |

源码**没有**将视频外end自动裁剪或缩放，而是在域内25点上判断原区间是否覆盖。无命中不等于现实动作不存在；s=e也可能在一个采样点命中，但并不满足旧正时长质量要求。原脚本未给非finite、畸形输入、错误类别、非正length的完整研究级质量保障，不能称它认证了这些记录。

## 3. 精度、模拟范围与不变式

[新标准库程序](../../../prototypes/charades_official_time_alignment.py)将官方已确认有限数值路径翻译为binary64：CSV数值转Python float，t=(j/25.0)·float(L)，原s/e直接比较，保持源码运算顺序。旧质量规则则保留Decimal字段判定，不覆盖原标注、改单位／端点或统一舍入。

将先除后乘改写为j·L/25，二进制浮点下可能不同；合成L=0.1的端点用例对此有反例。因此README的代数等价写法不能替代源码操作顺序。对每行生成的class/point布尔集合仅临时用于宏观cell计数，**不导出矩阵、frame ID或原始记录**。

实际模拟范围：固定文件、已知157类、有限可解析端点、正length。遇畸形、非finite、未知class或不支持的length立即UNKNOWN／STOP，**不是声称官方会拒绝它们**。合成零length可按原算式产生重复0点，但真实分析入口不将其当物理视频；未执行MATLAB，跨语言文本解析／编译器/JIT的全域逐bit一致及端到端mAP重现仍未验证。

全部token保持全分母；strict只决定另一套对照标签，不删除CSV行。strict标签集合应是官方标签集合子集，程序实际核此不变式；原strict P1/P2冻结值也必须匹配，否则STOP。

## 4. 三层状态不相互提升

| 层 | 规则与当前状态 |
|---|---|
| A OFFICIAL_LABEL_SAMPLING_COMPATIBILITY | **VERIFIED_WITHIN_STATED_SCOPE**：同ZIP源码到有限、正规输入的25点布尔标签构造合同；不是MATLAB实跑或mAP／媒体帧认证 |
| B TIME_RANGE_QUALITY | **HOLD／记录质量分层已测**：within、crosses_end、starts_outside、invalid；可命中网格不免除越界／顺序风险 |
| C P1/P2_EVENT_TRUTH | **HOLD**：完整实例、主体／语义、真实媒体PTS／原点与自然独立来源仍未建立，不能生成ordinal或模型真值 |

短域工程对比今后应明确采用**官方采样谓词**构造标签，不能用自加end≤L门并称官方frame-mAP口径。若进行精确实例研究，则另需B/C证据；本批不恢复任何真实模型评测。AGQA错误区间及Perfect Times先例只作为任务书提示，本轮未下载补充PDF／读取其方法，不升格为新独立论文证据。

## 5. 合成先行与资源

[19项合成测试](../../../prototypes/test_charades_official_time_alignment.py)在真实CSV分析前1次通过：0 FAIL/ERROR/SKIP，suite0.007秒，不含启动；覆盖25点索引／last sample、越界命中、域内短段miss、start≥L、等号、零／极短length、同类OR／不同类并发、重复ID／记录、浮点操作顺序、坏／非finite、脚本唯一性／限额／危险名字、输出及多表／小余项保护。

随后真实只读聚合1次成功，源码规则未按真实结果调整。0执行.m、0新数据／HTTP／媒体／STA／特征／模型／GPU／QA／真实解码，0原隔离树／环境／历史源码／manifest写入。只提交两个报告、两个新通用文件与一条结果，见[三层统计](./three-tier-aggregate-and-go-no-go.md)。

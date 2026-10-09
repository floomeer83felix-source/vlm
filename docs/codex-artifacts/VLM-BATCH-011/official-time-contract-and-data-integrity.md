# VLM-BATCH-011：官方时间合同与固定数据完整性

2026-10-09，main5496956。只读新父任务，未重做009/FIX/010、未下载或写入原隔离树。**字节与独立计数核验PASS；时间语义合同仍HOLD_TIME_CONTRACT。** 本文只区分文档、数值观察和未证实事实，不能据此修正标注或启动模型。

## 1. 授权、路径与字节锚点

重新读取AGENTS、唯一READY任务、结果和指定010报告，确认无011既有回报。固定根仍为`%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-Metadata\`。新程序不接受目录／URL参数；入口只打开指定ZIP、两个CSV和类表，没有下载／解压／数据写入能力。调用既有check_ancestors仅作目录／文件身份安全核验，不复用旧范围、解析或资格函数。

目录身份／双链无reparse／规范稳定及LOCALAPPDATA包含检查PASS，与文档仓库不重合。不存在需要换位置、恢复数据或改环境的条件。

| 固定对象 | 实测SHA256及结论 |
|---|---|
| 原ZIP | `c616913ef79c2ddde06d9c562eae57bb8901d459d7568a0d27bf09cbf33ae866`，与任务书一致 |
| Train CSV | `59273c6dc2139ec7eb95b980fd26bc8529774b1ede0602f6ca90b546ed12f0fc`，一致 |
| Test CSV | `8b8b207b55fb95b949018027f69d83bd46cd844d15834f8f592ee8e7446173eb`，一致 |
| 类表 | `7b95127e60300d6a69849d161869eb3e9657fa320fc9e92b6f2c9403b49c1887`；与SHA固定ZIP中的唯一同名类表字节一致，157类 |

没有再次获取包、提取原文件、覆盖manifest或保存中间统计。文件指纹证明本轮读的是010那份字节，不证明媒体时钟／实例／官方文档假设正确。official_sha256仍未建立，不将本机SHA当独立官方供应链证书。

## 2. 冻结的官方时间文本：分级而不猜单位

使用此前取得的[官方README](https://prior.allenai.org/projects/data/charades/README.txt)公开文本缓存；其SHA256为`a75c27daa0aeacdbaac6b99e022f8257a8c38e1c03848470a9088933c7fc12a0`，本轮核其与010已固定官方README指纹一致。**没有新HTTP请求；不宣称重新访问了今天的官网。** [官方许可](https://prior.allenai.org/projects/data/charades/license.txt)沿010已核正文和用户非商业用途，权限不扩大。

| 命题／原文锚点 | 证据级别 | 可以／不能推出 |
|---|---|---|
| actions段写“class start end” | DOCUMENTED | 分号多三元组的文本格式；未直接给完整端点闭半开、误差或实例切分保证 |
| length段写“The length of the video in seconds” | DOCUMENTED | length列声明单位秒；不证明这个字节版本与所有action端点或某媒体版本同一原点 |
| changelog 2017-02-27 | DOCUMENTED | 当时新增length及localization支持；不提供当前包所有修改、媒体时长取得流程或区间回标桥接 |
| localization段25点 | DOCUMENTED | 官方帧级mAP在0、length/25、…、24·length/25处取点；不是所有事件区间det-mAP或当前异常修正规则 |
| action端点以秒、同媒体／同原点与length比较 | INFERRED | 从字段与定位背景形成待核前提；现公开说明没有完整证明所有条件，不能由读数字自动认证 |
| 所有端点必须不超过本length、超出仅属舍入／VFR／单位错 | UNKNOWN | 原README没有授权自动钳位、缩放、换FPS或重建长度，本轮也无媒体验证 |

以上短引文合计未超25英文词；其余为释义。没有复制官方数值例子或真实样本。本轮不是寻访作者、修改license、查新资料或媒体时钟实验。

## 3. 独立解析器和010交叉核验

新增[只读诊断器](../../../prototypes/charades_time_contract_diagnostic.py)，用csv.DictReader、独立Decimal转换、主因优先级、差额桶和集合／区间算术；不调用旧finite_number、summarize_split或retract等范围／资格判定。Python3.9.21，UTF-8-SIG读取成功。真实header11列两split一致：`id, subject, scene, quality, relevance, verified, script, objects, descriptions, actions, length`。只将必要id/actions/length投影用于本机聚合，不使用或返回subject值、脚本／描述、原始行。

| 全分母与原合同 | Train | Test | 总计 |
|---|---:|---:|---:|
| CSV行 | 7,985 | 1,863 | 9,848 |
| 原始动作token | 49,809 | 16,691 | 66,500 |
| 合同通过token | 35,211 | 11,664 | 46,875 |
| 不通过token | 14,598 | 5,027 | 19,625 |
| 含不通过token的行 | 5,896 | 1,537 | 7,433 |

全部参考键与010逐项相符，包括P1三种gap阈值／混合歧义、P2pair／strong／视频分母；任一不符入口会STOP。新解析没有发现先前分母算错；**两个实现复现同数字不证明它们共同使用的时间合同成立**。

## 4. 唯一主因与可重叠flag

主因优先级冻结为parse→length非法→时间非finite/不可解析→class不在类表→负起点→start≥end→end>length→OK。每token只选一个主因，原始互斥计数和严格等于66,500；valid+invalid也等于此分母。flag独立检查可多重触发，其和不是66,500的互斥全分母，本轮也不按flag之和报不同坏token。

| 互斥主因／非互斥flag | Train | Test | 总计 |
|---|---:|---:|---:|
| parse、非法length、非finite时间、未知class、负起点（分别） | 各0 | 各0 | 各0 |
| start≥end | WITHHELD_LT10 | 0 | WITHHELD_LT10 |
| end>length | WITHHELD_LINKED_OR_COMPLEMENTARY | 同左 | 同左 |
| OK（仅主因） | 35,211 | 11,664 | 46,875 |

当前主因表与flag表在上述披露级别取值相同，但语义仍不同。不能由表内小格抑制后看不到sum就称不守恒；sum检查在抑制前完成。end>length的宏观计数也补充隐藏，以防从已知不通过分母反推小主因，不能以隐藏值认作0。

## 测试、执行与证据边界

新增[纯合成测试](../../../prototypes/test_charades_time_contract_diagnostic.py)：首次14方法PASS、0 FAIL/ERROR/SKIP，suite0.003秒后，才进行1次真实只读计算。公开前发现“总候选−异常行关联候选”可能还原小余项，随后**只以合成用例**强化关联／补充抑制，新15方法PASS，0 FAIL/ERROR/SKIP，suite0.003秒；没有再读真实CSV，没有修改数值、范围、桶或P1/P2规则。最终源码的算术与实跑版本相同，新增披露守卫只经过合成验证，不伪称已重新实跑最终版本。

真实执行只给宏观数字、header和文件级SHA，没有回传实际行或ID；旧审计器／旧test未改，原隔离树无文件写入。下一报告描述新分布与资格可信性。**结论HOLD_TIME_CONTRACT**：有数值矛盾且公式可复现，仍缺同版媒体／标注时间语义桥接，不能制造规则PASS。

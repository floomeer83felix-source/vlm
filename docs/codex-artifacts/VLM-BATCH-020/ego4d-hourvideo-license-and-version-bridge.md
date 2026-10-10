# VLM-BATCH-020：Ego4D—HourVideo许可与同版时间桥接

公开静态核查：2026-10-10；公有文档基线main `7c70287ed0ee372c8fada74a9bdea323ae704698`。本轮仅网页文字，未取得数据实体、接受协议或核验媒体文件。`VERIFIED_TEXT`只认证所见公开文字；`UNKNOWN`不是非法判定，也不是使用许可。第三方GitHub页面为当日main快照，未显示可核完整提交SHA，不虚构版本pin。

## 1. 两层权利链

| 对象/用途 | Ego4D | HourVideo及其Ego4D上游 | 本项目状态 |
|---|---|---|---|
| 软件 | [LICENSE正文](https://github.com/facebookresearch/Ego4d/blob/main/LICENSE)是MIT，授予对象为软件及配套文档 | [LICENSE正文](https://github.com/keshik6/HourVideo/blob/main/LICENSE)是Apache-2.0 | VERIFIED_TEXT，仅软件层；不外推媒体/标注 |
| 原媒体与Ego4D标注 | [Start Here / License Agreement](https://ego4d-data.org/docs/start-here/)要求取得数据或任何标注前接受正式协议 | [README Abstract](https://github.com/keshik6/HourVideo#abstract)明确以Ego4D为来源；下游公开入口不能豁免上游条件 | RESTRICTED；完整授予范围UNKNOWN |
| 完整协议 | [官方协议入口](https://ego4d.dev/)本轮返回403 Forbidden；未登录或签署 | 未在所读README/LICENSE中取得独立的完整标注/源媒体使用合同 | SOURCE_UNAVAILABLE / UNKNOWN；不是协议不存在 |
| 训练 | Ego4D正式训练用途、机构范围及衍生监督条件未读到，UNKNOWN | [Benchmark Data Usage Restrictions](https://github.com/keshik6/HourVideo#benchmark-data-usage-restrictions)明确benchmark不得进入训练语料，开发标注也受防污染限制 | HourVideo禁训为VERIFIED_TEXT；不能以开发集训练控制器/校准器绕过禁训；校准是否获准须另核用途 |
| 评估 | Benchmark文档介绍评估，但未替本项目完成协议与许可 | README推荐开发集作评估，不能据此推断本项目已获得上游权利 | 评估意图公开；执行权利HOLD |
| 标注/媒体再分发 | 正式条款未读到 | Apache代码许可不能覆盖原视频或QA；完整再分发授予未核 | UNKNOWN；本轮不上传实体 |
| 派生时钟、研究真值构造 | 生成新时间标签与公开其版本/时间映射的许可须分别查验 | 禁训之外，制作与公开新证据窗口/时钟标签的权限没有可核完整文字 | DERIVED_LABEL_CREATION=UNKNOWN；DERIVED_LABEL_PUBLICATION=UNKNOWN |
| 商业、地域、跨境、期限 | 完整协议不可得，不补写“仅研究”等未见条款 | 源协议与下游条件均需符合；未见完整地域/商业条款 | UNKNOWN；代码可商业使用不等于数据可商业使用 |
| 隐私伦理 | [Privacy and Ethics](https://ego4d-data.org/docs/privacy/)介绍各站点同意与PII处理，部分参与者同意未模糊；并非所有人均匿名 | 继承源素材隐私风险，未核项目特定衍生发布伦理条件 | VERIFIED_TEXT（政策概要），具体使用/再识别/机构义务UNKNOWN |

上游正式数据条件与下游benchmark限制是累加审核项。用户本轮只授权文本审查，没有签约、凭据、数据获取或新标注许可。报告不复制防污染字符串、邮箱、样本身份或许可长正文。

## 2. 仅纸面依赖图

```text
Ego4D release + canonical video identity/version
  ← source components +各自stream原点/timebase + trim/concat记录
  → canonical clip identity +裁剪端点/版本
  → HourVideo source选择 +派生文件版本/hash +实际转换记录 [缺口]
  → HourVideo容器/呈现PTS与输入采样时钟 [未实测]
  → QA证据窗口 / caption或字幕时钟 / evaluator坐标 [合同未闭合]
```

箭头表示需要证明的依赖，不表示所有HourVideo文件经过clip环节或下列工具。canonical video直接选入HourVideo也是待核路径。软件网页包含函数不证明发布流程执行了它。

## 3. 字段、单位和成立条件

以下是[官方Annotation Schemas](https://ego4d-data.org/docs/data/annotations-schemas/)中metadata及NLQ两个节的字段名，只有类型，没有任何真实值。

| 命名空间 | 字段与坐标 | 能支持什么 / 尚缺什么 |
|---|---|---|
| metadata `videos[].video_metadata` | `video_start_pts`为整数tick；`video_base_numerator/denominator`定义秒/tick；`video_start_sec`是stream相对容器的起点 | 可写stream-relative换算，不证明HourVideo沿同原点 |
| metadata `videos[].video_components[]` | `component_idx`；`canonical_video_start_sec/end_sec`（秒）及frame端点；每component自有`video_metadata` | 组件位置与组件自身PTS需合并；不能用全video的timebase换组件tick |
| metadata `clips[]` | `video_start_sec/end_sec`是parent中的clip边界；`clip_metadata`给clip自身stream/timebase | 同名`video_start_sec`不同于上一行stream原点 |
| NLQ `videos[].clips[]` | `video_start_sec/end_sec`与`clip_start_sec/end_sec`、相应frame字段、`source_clip_uid` | clip锚点不是query真值边界 |
| NLQ `clips[].annotations[].language_queries[]` | query自己的clip/video起止秒与video frame边界；顶层`version/date/manifest` | 两坐标存在不保证跨release可混用，也不保证小时QA证据穷尽 |

**条件公式（本报告推导，非文件实测）**：令同一stream呈现PTS为p、其起点p0、秒/tick为n/d，则相对stream时间 `t=(p-p0)n/d`。只有连续裁剪且无变速、对应锚点在canonical/clip分别为av/ac，才有 `t_video=t_clip+(av-ac)`。组件k映到canonical的候选式 `t_v=c_k+(p-p0k)n_k/d_k` 还需同版trim、速率及拼接连续性成立；帧重复/删除、缺口或变速须用实际分段/帧对应映射。转为容器绝对时间另需明确stream offset，不混用DTS、packet序号与呈现时间。

[Videos / Canonical Videos & Clips](https://ego4d-data.org/docs/data/videos/)说明组件trim、标准化30FPS、拼接及clip半开frame范围。标准化文档不等于目标文件PTS/标注一致性证书。若源CFR的FPS为f、每k帧重写为f'，第j个保留帧的源名义时间为jk/f，输出名义时间为j/f'，二者仅当 `kf'=f` 且原点一致时相等。这是纸面关系，不是任何实际素材的测量。

[HourVideo hv_utils.py](https://github.com/keshik6/HourVideo/blob/main/hourvideo/hv_utils.py)的`load_video`用平均fps和整数步长采样；`downsample_video`用整数skip及指定输出fps重写；`trim_video`从开头保留到由秒×平均fps取整的frame端点。这些只能支持“名义索引重写需要映射审核”，不能认定发布版已漂移或全部调用这些函数。源码形参`video_uid`亦不证明其与Ego4D canonical UID构成同版、唯一、稳定join。

## 4. 版本、标签与长期域缺口

[Ego4D Updates / v2.0及v2.1](https://ego4d-data.org/docs/updates/)公开说明NLQ零长度区间修订及一些原本应合并的视频在后续分组。故同一个库名不是同一个时间合同。HourVideo README记载v1.0及开发标注发布时间，但所读公开页面未认证源Ego4D release、派生文件hash、裁剪/重采样操作日志、QA证据坐标原点和caption对应版本的闭环。`MAPPING_NOT_PUBLICLY_CERTIFIED`只针对本轮允许阅读的页面；没有进入HF数据卡/QA实体，也不声称所有受控发布资料均无相关字段。

必须另有：稳定源对象及release、派生对象digest、可核转换与时间锚、帧/PTS对应和舍入政策、QA与证据标签版本、评估器坐标及标注不确定性定义。hash只认证字节身份，不自行证明转换语义或标注真值。无这些证据不能设映射为恒等，也不能自行猜offset分布。

[Episodic Memory / NLQ](https://ego4d-data.org/docs/benchmarks/episodic-memory/)描述答案可见窗口，不是穷尽所有重复事件的身份表；Videos页给NLQ clip平均10/最长20分钟。HourVideo作者声明20–120分钟输入不替它提供同版小时定位GT。二者共享Ego4D来源，不构成独立外测；仅按不同文件名分组也不能证明源独立。

## 5. 静态结案

LEGAL_PROVENANCE=HOLD；SAME_VERSION_TIMEBASE=UNKNOWN；MAPPING_NOT_PUBLICLY_CERTIFIED；派生真值构造/公开权限UNKNOWN。没有可核新增授权或桥接闭环，不进入媒体核查、QA实体验证、签约或下载。未知可以被未来公开证据修订，本轮不通过其它资产或联系渠道填补。联合科学裁决见[止损报告](h1-legal-novelty-stop-decision.md)。

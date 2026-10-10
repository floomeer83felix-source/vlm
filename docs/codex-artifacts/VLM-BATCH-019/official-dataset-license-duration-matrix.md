# VLM-BATCH-019：官方许可链与真实输入时长

静态阅读日：2026-10-10（北京时间）；文档基线main `3d784c2`。这是一轮有界公开资料筛选，不是数据使用法律批准、媒体实测或完整系统综述。网页main无可核提交SHA时只记录阅读快照；论文明确注明版本。未打开数据实体/QA文件、下载PDF、签协议、登录或运行代码。仅采用官方项目/仓库/论文网页；搜索结果用来定位原始来源。

`VERIFIED_OFFICIAL_TEXT`只表示相应文字已核；`RESTRICTED`表示有明确使用/访问条件；`UNKNOWN`表示证据未读到或不足。代码、标注与原视频权利分别判断，不能合并成一个LICENSE_PASS。

## 六候选许可链

| 候选 | 软件/论文与标注层 | 原媒体、训练/商用与再分发 | 访问/伦理层及本轮门 |
|---|---|---|---|
| Ego4D NLQ | 软件[MIT正文](https://github.com/facebookresearch/Ego4d/blob/main/LICENSE)已核；标注与数据均须先接受[数据协议入口](https://ego4d-data.org/docs/start-here/) | 不能用软件MIT推导视频许可；完整协议在ego4d.dev本次无法读取，具体训练、商用/再分发范围UNKNOWN | RESTRICTED：审批后凭据访问，本轮未签约。具体地域/跨境条款UNKNOWN；[官方伦理页](https://ego4d-data.org/docs/privacy/)说明同意/PII处理仍需遵守。当前不准取数据 |
| HourVideo | [软件Apache-2.0](https://github.com/keshik6/HourVideo/blob/main/LICENSE)已核；[README使用限制](https://github.com/keshik6/HourVideo#benchmark-data-usage-restrictions)明确benchmark不得进入训练语料 | 软件许可不覆盖Ego4D原媒体。标注含防污染机制；不得训练/删除该机制。完整标注再分发与源媒体许可链仍待证 | RESTRICTED：Ego4D源协议和独立benchmark条件均须满足；开发集不是训练集。未打开HF实体/标注 |
| LongVideoBench | [README License](https://github.com/longvideobench/LongVideoBench#license)声明数据CC-BY-NC-SA-4.0；独立软件授权未核，CODE_LICENSE_UNKNOWN | 非商用条件明确；[论文HTML](https://arxiv.org/html/2407.15754v1)为网页来源。项目数据许可不能替第三方逐视频权利链，LEGAL_MEDIA UNKNOWN | 数据源/HF入口并非本轮下载许可；数据无train集，验证/测试用于评估设置而非当然许可训练。地理/伦理细则未逐项核准 |
| Video-MME | [官方Dataset段](https://github.com/MME-Benchmarks/Video-MME#-dataset)只准学术、禁商用；独立软件许可未核 | 原视频归原权利人；没有事先批准不得发布、复制、分发或修改等。不能把公开链接解释成研究衍生素材全权许可 | RESTRICTED；需要澄清具体本地使用/派生真值的批准链，当前BLOCKED_DATA_LICENSE。未取HF数据/字幕 |
| MLVU | [README License](https://github.com/JUNJIE99/MLVU#license)声明数据CC-BY-NC-SA-4.0和研究用途；CODE_LICENSE_UNKNOWN | 项目明确不拥有原视频版权，存在缩放/裁剪及移除请求后的帧/元信息替代；非商用明确，训练及再标注的完整媒体权利链UNKNOWN | 原条款须认可；本轮不继承旧本地MLVU资产。实际访问状态及逐资产权限未核，BLOCKED_DATA_LICENSE |
| LVBench | [README License](https://github.com/zai-org/LVBench#license)声明CC-BY-NC-SA-4.0、学术/非商用；CODE_LICENSE_UNKNOWN | 项目明确不拥有原视频版权；YouTube来源与video2dataset说明不是版权授予或同版保证，训练/衍生实例真值权限UNKNOWN | 不执行抓取/安装。逐视频权利和可重现版本未闭合，BLOCKED_DATA_LICENSE |

所有候选目前都没有“标注可取+源媒体可合法使用+可派生本研究真值”的完整许可PASS。UNKNOWN不表示不合法，也不表示可以先拿来试；本轮只停在公开文字核查。除了明确HourVideo禁止训练，不把其它候选条款的UNKNOWN擅自升级为法律层面一律禁训；但本项目当前仍无任何数据训练许可，benchmark评估数据不能混入模型或控制器训练。

论文文本公开可读与论文再分发许可也是不同层。本轮未逐一核论文全文再利用许可，PAPER_REUSE_LICENSE_UNKNOWN；没有将arXiv网页、软件MIT/Apache或数据集CC声明互相替代，也不复制论文/许可长正文。

## 视频长度与评测单位

| 候选与官方证据 | 已核输入/数据范围 | 20/30/60分钟与更久：哪些能证、哪些不能 |
|---|---|---|
| Ego4D NLQ：[官方Videos/EM clips](https://ego4d-data.org/docs/data/videos/) | NLQ canonical clip平均10分钟、最长20分钟；长canonical video与标注clip是不同对象 | 不能将NLQ常规评测直接当30/60分钟输入。母库/HourVideo有长视频，不证明小时输入上的NLQ标签覆盖；各阈值分组数量UNKNOWN |
| HourVideo：[官方README摘要](https://github.com/keshik6/HourVideo) | 500个Ego4D来源视频，20–120分钟，12,976题 | 20–120分钟范围已证；≥30、≥60分钟及>60分钟具体数量UNKNOWN，不把500全记成≥60分钟 |
| LongVideoBench：[v1 HTML Table 3](https://arxiv.org/html/2407.15754v1) | 3,763视频、6,678题；四档(8,15]秒、(15,60]秒、(180,600]秒、(900,3600]秒；最后一档966视频 | 15–60分钟档不等于全部≥20/30分钟；≥20/30/恰60分钟数量UNKNOWN；没有>60分钟档证据。966是视频数，不是题数/独立来源数 |
| Video-MME：[官方Introduction](https://github.com/MME-Benchmarks/Video-MME#introduction) | 900视频/2,700题，短<2分钟、中4–15分钟、长30–60分钟 | 30–60分钟组存在已证；所读README没有可核该组数目，不能由900/3擅自填300；20–30/>60分钟不在所述档，端点数量UNKNOWN |
| MLVU：[官方Introduction](https://github.com/JUNJIE99/MLVU#introduction) | 明确3分钟至2小时，九任务 | 修正种子：范围本身已证。≥20/30/60分钟各比例、当前每题实际输入截断/替代资产分布仍UNKNOWN |
| LVBench：[论文v2 §3.1/Table 1](https://arxiv.org/html/2406.08035v2) | v2说明103视频、1,549题、入选至少30分钟、均值4,101秒；[当前arXiv](https://arxiv.org/abs/2406.08035)已是v3（2025-08-09） | 历史v2足以证长域，不能充当2026当前实体逐条审计。≥60数量UNKNOWN；所读正文/主页未确证种子“最长2小时”，MAX_DURATION_UNKNOWN，不反向断言无两小时视频 |

LongVideoBench Table3网页可读六个布局格为546/338/551/374/986/966，纸面相加3,761，而摘要宣称3,763：STATIC_TABLE_TOTAL_CONFLICT，不能在没有原始版面/实体核验时认定哪格错或两条媒体缺失，未校改官方数字。最长档966仅按该表报告，当前实体数量UNKNOWN。不以长度平均值推断尾部概率。以上均为公开作者声明，尚无同版文件实测。采样16/32帧不将视频压成16/32秒；反之“全库几千小时”也不使每道QA成为一小时任务。

[EgoSchema官网](https://egoschema.github.io/index.html)与[论文摘要](https://arxiv.org/abs/2308.09126)均指3分钟输入；只列短域辅助，不列核心长域候选。HourVideo来自Ego4D，二者不能构成独立外部来源验证；EgoSchema也有该重叠。网络来源候选之间的频道/影片重复UNKNOWN，没有下载媒体核指纹，不假定独立。

## 可用性与版本收据

六候选官方入口均读到。Ego4D完整协议前端ego4d.dev不可得，保留SOURCE_UNAVAILABLE及条款UNKNOWN；未尝试登录。LongVideoBench所读HTML为真实v1，尝试v2地址不可得，不编造v2论文；LVBench数量明标v2，最新v3实体统计未取。第三方GitHub main网页未显示完整提交pin，不伪造SHA。不开数据实体、不签约、不申请凭据、不重跑旧资产，历史Charades最终媒体STOP/A限域/B-C HOLD保持。

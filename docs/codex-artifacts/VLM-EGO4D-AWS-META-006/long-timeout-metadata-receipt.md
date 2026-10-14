# META-006：完整官方清单与50个UID命中；canonical来源校验HOLD

2026-10-14（北京时间）。**SAFE_METADATA_STOP / CANONICAL_SOURCE_HOLD**。唯一官方清单的条件GET完整成功；真实本地UID精确交集50。随后canonical来源安全门拒绝继续，媒体桶探测与媒体对象HEAD均NOT_RUN。不是MEDIA_READY，也没有合法可下载视频已经通过本轮全部检查的结论。

## 启动与本地门

独立公有文档checkout原工作树干净，安全fetch/fast-forward到main `ea84adf`。读取最新AGENTS、任务板、结果、META-006合同、META-005合同及实测收据、研究总览和2026-10-14 GPU路线。任务板旧段仍有META-006待授权的历史文字，但最新2026-10-14记录、当前表行与本合同一致为唯一READY；本ID无既有结果。排队任务没有执行。

只读定位用户此前指定目录内的精确基础文件名。正规文件及目录祖先无链接/reparse；文件1,854,695B、≤16MiB，JSON/dev结构PASS，顶层视频UID及有限正时长50记录，读取前后SHA在RAM比对一致。未扫描旧目录或编号副本、修改或复制原JSON。整体JSON解析技术上读入QA字节，仅额外取得开发题数组长度作为≥2题资格门；未读取答案值用于匹配、候选排序或输出，也未重做QA内容审计。

复用既有独立SDK环境与ego4d静态共享凭据提供器，仅SDK内部加载签名；无手工凭据查看、profile枚举、环境账户/default、SSO/IMDS/STS/刷新、配置或依赖改动。新父任务独立私有执行器与匿名计数，不执行META-005，也不修改旧账本。

## 实际请求与清单

| 阶段 | 实际HTTP尝试 | 实际结果 |
|---|---:|---|
| A manifest桶HeadBucket | 1 | 301；可信TLS响应区域头通过SDK本地商业区列表检查，区域发现PASS；不跟Location，不视为认证成功 |
| B regional manifest HeadObject | 1 | 200；声明4,653,141B，≤8MiB，ETag条件身份锁可用 |
| C 同对象条件GetObject | 1 | 200；长度/ETag、如有VersionId、非压缩条件检查通过，完整应用读4,653,141B；无超时、无partial解析 |
| D 媒体贡献桶HeadBucket | 0 | NOT_RUN；canonical来源校验阻塞 |
| E canonical媒体HeadObject | 0 | NOT_RUN；未得到任何媒体对象大小 |

总S3 HTTP尝试 **3/7**；HeadBucket1、HeadObject1、GetObject1。manifest HEAD成功1、完整GET成功1；本轮未出现流读取超时。实际执行约40.256秒，低于20分钟。

发送前按HTTPS/精确host、method、bucket-key、阶段次数/总7次及许可截止检查，逐attempt fsync持久匿名计数。串行、连接池1、connect_timeout=5、read_timeout=90、total_max_attempts=1、显式禁代理继承、TLS验证保留。阶段A捕获区域响应后先于SDK自动跳转停止该调用，按核定区域建立client；不猜区域/来源。保守1100秒操作门及1180秒独立进程监督限时已设置，本轮未触发。隐藏补发拦截计数0，没有重试、Range、LIST或STS。

应用正文大小是成功返回脚本的流read总量，等于声明清单长度；**不等于SDK缓冲、TLS开销或网卡wire总量**，未独立测量线上总字节。

## UID与来源门：事实及限制

完整CSV解码/表头检查通过，对50个授权本地顶层video_uid进行严格等值匹配，**唯一UID交集计数50**。不按file_uid拼猜媒体key，不切换发行版本，不用答案挑选候选。UID命中仅为UID_PRESENT_IN_V2_1，不证明同发布媒体、剪辑起点或PTS一致。

后续逐匹配行的canonical来源门触发 **CANONICAL_SOURCE_HOLD**。该门组合检查URI方案、官方贡献桶白名单、非空安全key、查询/fragment及异常路径字符。该匿名错误没有记录究竟哪一子条件失败，也没有记录问题行序号或身份；所以根因子项 **UNKNOWN**，不能断言官方数据非法、访问被拒或真实视频不存在。发生阻塞后立即结束，不检查另一个版本、重选视频、修改/放宽规则或再次运行。

| 门 | 本轮结论 |
|---|---|
| 固定官方manifest权限 | AUTH_OK：仅实际HEAD200、GET200及完整清单读取证据 |
| 完整清单与本地UID等值匹配 | PASS；50个唯一UID命中 |
| 全部canonical来源资格/安全候选数量 | HOLD / UNKNOWN；中途检查停止，不填0候选 |
| 0–2媒体HEAD成功/对象大小 | NOT_RUN / UNKNOWN |
| 单段≤4GiB、合计≤8GiB | NOT_RUN / UNKNOWN；没有视频大小证据 |
| 贡献桶对象权限 | NOT_TESTED，不从manifest权限外推 |
| 发布版本与时钟桥接 | RELEASE_AND_CLOCK_BRIDGE_UNKNOWN |
| 后续视频GET | MEDIA_GET_NOT_AUTHORIZED |

本轮首要交接是审查组合canonical来源安全门与官方实际清单字段之间的差异，必要时由ChatGPT冻结新的有界只读诊断任务；本轮未开展诊断、源码修改或新请求。公开报告没有原清单行、UID/身份映射、对象位置、实际区域、ETag/响应头、凭据或私有路径；不存在从本轮证据自动放行下载的对象。

## 执行边界与停止

媒体GET/Range/正文0；GPU、模型、ffprobe、视频解码、训练0；工具安装、合成测试、无关调研、原科研环境与旧实验/锁/账本修改0。CSV只在私有RAM，未保存partial或完整清单到磁盘，私有脚本和匿名计数不上传。

仅交本收据和codex-results末尾一条结果，不改任务书/路线/总览或公共代码。正常main一次push后停止并保留聊天，等待ChatGPT审查；不执行任何排队媒体、A/B或训练任务。NOVELTY=RETAIN0、Charades FINAL_MEDIA_STOP保持。
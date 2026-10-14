# META-007：45个安全来源候选，两个媒体HEAD成功；一段满足后续大小门

2026-10-14（北京时间）。**META_PREFLIGHT_EVIDENCE / MEDIA_GET_NOT_AUTHORIZED**。官方完整清单与50个本地UID等值匹配通过；45个固定白名单来源合法候选，5个来源未在固定官方桶表内而隔离。两个预先排序候选HEAD200，其中1个≤3.5GiB，另1个>4GiB，两段合计>8GiB。没有媒体GET、帧读取、GPU或模型执行；未认证HourVideo发布/时钟桥接。

## 启动和阶段0：0 AWS的静态诊断

独立docs工作树干净，安全同步main `026aa28`。读取AGENTS、最新任务板/结果/总览与META-007合同，确认当前唯一READY且无本ID回报；历史待授权文字以最新2026-10-14批准记录及当前表行为准。只读检查META-006私有校验器，没有执行或改写006、旧账本和公共代码。

对照固定Ego4D提交 `4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb` 的公开源码：[manifest.py](https://github.com/facebookresearch/Ego4d/blob/4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb/ego4d/cli/manifest.py)、[universities.py](https://github.com/facebookresearch/Ego4d/blob/4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb/ego4d/cli/universities.py)、[s3path.py](https://github.com/facebookresearch/Ego4d/blob/4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb/ego4d/cli/s3path.py)、[config.py](https://github.com/facebookresearch/Ego4d/blob/4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb/ego4d/cli/config.py)。仅公开源码文档访问，不执行官方批量下载器。

| 匿名静态类别 | 真实诊断 |
|---|---|
| GUARD_DIFF_SYNTH_PREFIX | 006校验器没有固定合成媒体key前缀/UID文件名限制；合成测试器有虚构路径合同，但006未调用它。不能归因合成前缀 |
| GUARD_DIFF_BUCKET_TABLE | 006白名单与固定官方表精确一致；缺失0、额外0，没有扩充白名单 |
| GUARD_DIFF_FIELD_SELECTION | 官方取第一个存在的canonical字段，再取替代字段；006收集非空字段并要求相同。本轮采用官方字段优先顺序，但空值拒绝、双字段冲突仍隔离，不任意挑一个 |
| GUARD_DIFF_URI_KEY | 006要求S3 URI、官方桶、非空安全key、无query/fragment/异常路径字符；官方基础解析器本身不认证这些安全条件。本轮保留安全门，不因为官方CSV来源而放行任意地址 |
| GUARD_DIFF_TYPE_UID | 精确video_uid join，不按file_uid拼key；非空file_uid/非视频类型保守隔离。本轮相关拒绝计数0 |
| GUARD_DIFF_STOP_SCOPE | 006在首个不安全来源停止整个候选扫描；本合同允许封顶逐UID匿名分类并只对其余安全候选继续。此分类策略在新请求前固定，不重跑006 |

阶段0没有006原始清单缓存或失败身份，所以当时的精确停止行/子原因仍 **CAUSE_UNKNOWN_HISTORICAL_006**。不能以静态差异冒称已证旧根因。

## 本轮执行和本地门

只读同一已授权目录顶层精确JSON，正规无链接/reparse、1,854,695B/≤16MiB、dev schema PASS、50个顶层UID与有限正时长，读取前后SHA RAM一致。QA只取数组长度作为≥2题过滤；整体JSON解析含QA字节，不以答案、题目或选项排序、映射或输出。未扫描其它目录、复制或改动原JSON。

复用已有独立SDK环境和ego4d静态共享提供器，SDK内部签名；不手工读/输出凭据、不枚举profile，不使用环境/default账户、STS/SSO/IMDS或刷新。私人新执行器先发生一次字符串转义SyntaxError，在Python解析阶段退出1，无SDK加载、网络请求或持久计数；离线修正两处反斜线字面量并通过AST语法检查。随后只有一次真正运行到本地/AWS流程的执行；没有真实请求重试、计数重置、合成测试或环境修改。该初始工程错误如实保留，未声称首次代码启动通过。

## A–E真实请求

| 阶段 | HTTP尝试 | 真实结果 |
|---|---:|---|
| A manifest桶HeadBucket | 1 | 301，可信AWS TLS区域头通过商业区域表检查；区域发现PASS，不跟Location |
| B regional manifest HeadObject | 1 | 200，4,653,141B、ETag可绑定 |
| C 同对象条件GetObject | 1 | 200，完整应用读取4,653,141B，长度/身份/非压缩一致，无超时 |
| D 两个不同安全候选贡献桶HeadBucket | 2 | 301、301；可信区域头均通过，随后只在核定区域发对象HEAD |
| E 两个不同canonical视频HeadObject | 2 | 200、200；ContentLength已知且正，身份绑定字段均可用 |

总 **7/7 S3 HTTP尝试**：HeadBucket3、HeadObject3、GetObject1。没有隐藏补发或重试、LIST/STS/媒体GET/Range。实际前台AWS流程约36.496秒，≤20分钟。

发送前审计HTTPS/精确host/method/bucket-key、阶段次数及总额度/许可窗口；每次wire发送前fsync匿名计数。串行连接池1，total_max_attempts=1，connect_timeout=5/read_timeout=90，显式禁代理继承/TLS验证保持。A/D仅从可信响应头验证区域，先于SDK自动跳转终止探测调用；不采纳Location。1100秒操作门和1180秒程序监督保留，本轮未触发。应用清单read字节不是SDK缓冲、TLS或网卡wire总量，后者未精确计量。

## 完整CSV、互斥来源分类与冻结选样

完整CSV/表头/行结构通过。精确video_uid唯一交集 **50**；无任意其它发行或元数据请求。每个匹配UID按固定顺序分类一次；重复UID及跨UID同对象优先隔离，不挑其中一条。所有类别分母合计50：

| 互斥匿名类别 | UID数 |
|---|---:|
| AMBIGUOUS_UID_OR_OBJECT | 0 |
| NOT_VIDEO_TYPE | 0 |
| FIELD_MISSING_OR_EMPTY | 0 |
| FIELD_CONFLICT | 0 |
| S3_URI_INVALID | 0 |
| BUCKET_NOT_IN_PINNED_OFFICIAL_LIST | 5 |
| KEY_UNSAFE | 0 |
| VALID_CANDIDATE | 45 |

同一轮RAM内分解006组合来源谓词：**OFFICIAL_BUCKET失败5**，其余组合谓词未出现失败。这是本轮真实行级证据 **CAUSE_CONFIRMED_CURRENT_READ**；意味着5个匹配来源不符合本合同的固定官方表，不能断言这些桶非法或全部数据不可用。未持久化旧清单身份，仍不能证明它们就是006确切首个失败行。没有公开真实桶名称/UID/对象地址，也未查询、HEAD或GET这5个不合规来源。

45个安全来源候选均满足声明时长≥20分钟及开发QA数组长度≥2。请求前固定优先≥30分钟，再按UID SHA256稳定排序，私有hash不输出；选最多2个不同UID/对象。不使用答案或按远端大小重选有利视频，两个HEAD后未替换超大对象。

## 实际媒体大小门与后续边界

| 门 | 真实结果 |
|---|---|
| 媒体HEAD200数/已知大小数 | 2 / 2 |
| 身份绑定字段可用数 | 2 |
| 单段≤3.5GiB（后续单视频候选门） | 1通过、1不通过 |
| 单段≤4GiB | 1通过、1不通过 |
| 两个对象ContentLength合计 | 12,897,682,214B；≤8GiB不通过 |
| manifest权限 | AUTH_OK仅实际HEAD/GET响应证据 |
| 所选媒体对象metadata权限 | 两个实际HEAD200支持，不推广到全部贡献桶/下载权限 |
| 发布/剪辑/PTS同钟 | RELEASE_AND_CLOCK_BRIDGE_UNKNOWN |
| 视频GET、解码、模型/GPU | NOT_RUN；未授权 |

**至少一段canonical对象的HEAD大小满足≤3.5GiB**，是后续单视频许可申请的元数据输入；不是本轮已下载、发布桥接通过或GPU可运行。两段组合不满足8GiB，不能批准双视频获取或扩大预算；当前合同只检查大小，不获取正文。

## 停止与交付

媒体GET/Range/视频正文、ffprobe/像素与音频解码、GPU/Qwen/SigLIP/训练均0。依赖安装、旧科研环境、Conda/PATH/AWS配置、历史ledger/锁和旧批次修改0。CSV/真实映射只在本次RAM，未写缓存；新私人脚本和匿名计数不上传。正式metadata结果并不保证下一任务能无请求重建对象映射，需要其合同独立规定来源身份与预算。

公有仅本匿名收据与codex-results尾部一次回报；不修改任务书、总览、路线或公共代码，不上传原JSON/CSV/QA/UID、桶/区域/对象、ETag、私有路径、凭据或日志。正常main push后停止，等待ChatGPT验收和用户另批单视频GET，不自动MEDIA/AB/训练。NOVELTY=RETAIN0、Charades FINAL_MEDIA_STOP持续。
# VLM-EGO4D-AWS-META-004：文件门通过，首次S3 HEAD因301安全停止

2026-10-13（北京时间）。结果 **SAFE_METADATA_STOP / HTTP_STATUS_301**。本轮真正发出1次限定manifest HEAD，官方S3 HTTPS端点返回301；按合同禁止隐式重定向、区域发现及补发请求，在响应解析/重试前关闭并停止。尚未取得清单或媒体对象大小，远端AUTH **NOT_TESTED**，不能将301当作签名权限PASS或403拒绝。

## 入口与本地实测

公有文档checkout原工作树干净，安全同步main `24631f6`，确认唯一META-004 READY且无旧回报，重读AGENTS、看板/结果/总览、本合同及指定历史收据、原AWS技术合同。旧META及工具/媒体批次不重跑。

只使用用户本轮指定目录顶层的精确基础文件名；文件直接存在，不需要编号副本枚举，不查询旧Downloads、其它目录或浏览器记录。目录及祖先、源文件无链接/reparse，正规文件存在PASS。

| 本机门 | 实测 |
|---|---|
| 源文件正规存在 | PASS |
| 实际体量 | 1,854,695字节，0<size≤16MiB PASS |
| 完整JSON可解析 | PASS，顶层对象 |
| dev结构 | video_metadata对象、benchmark_dataset列表、非空顶层UID及正有限duration字段PASS |
| 顶层视频元数据数 | 50 |
| 重复JSON键检查 | 无重复键异常 |
| 读取前后字节身份 | SHA内存比对PASS；原文件未改/移/复制，digest不披露 |
| 专用profile/静态凭据提供器 | PRESENT / 可加载，仅SDK内部签名 |

没有重跑1182题资格审计或答案评分，本轮不报重新验证了全部QA。JSON完整解析确实在内存读取包含QA的字节，但只抽取UID与声明时长用于候选映射，问答/选项/答案/canary不用于排序、输出或日志；这些与真实UID仅在私有RAM，不进入公有报告。独立发布版本与同钟仍未知。

## 唯一一次真实S3尝试

使用原已装boto3的唯一隔离venv、专用ego4d静态共享文件提供器；排除其它环境凭据与自动刷新链，不调用default/STS/SSO/IMDS/credential_process。一个串行S3 client，total_max_attempts=1、connect_timeout=5、read_timeout=12、连接池1，TLS证书验证保持、进程代理继承禁用，原系统配置不改。

本次manifest请求使用明确固定的S3全球HTTPS端点、us-east-1签名区域及path式寻址。发送前钩子限定HTTPS host、HEAD方法、唯一官方manifest桶/key及本阶段只能发送一次，预先fsync保存无秘密聚合计数。唯一允许研究GET仅manifest，媒体GET/Range无执行路径。

首次manifest HEAD已发送，收到HTTP301。传输层包装器在SDK解析或自动区域补救之前关闭响应并抛安全停止；没有跟随Location、换区域、另发HEAD或消费其余3次额度。**本轮未记录301目标或服务区域提示，不猜实际正确区域**；后续若调整请求端点，必须由独立合同明确授权及限定，而不是本任务自动补救。301也不能证明profile不正确或已失效。

## 请求与元数据收据

| 合同项目 | 本轮实际 |
|---|---|
| 正式批准至2026-10-26 | USER_CONFIRMED；当前在允许窗口 |
| 本机profile | 静态加载PASS |
| 远端身份/权限 | NOT_TESTED，非AUTH_OK、非已证AUTH_DENIED |
| S3 HTTP发送尝试 | 1 / 4，发送前计数，未证明服务端认证成功 |
| manifest HEAD | 尝试1、成功0、非成功响应1（301） |
| manifest GET | 尝试0、成功0、失败0 |
| 媒体HEAD | 尝试0、成功0、失败0 |
| 隐藏重试/区域补发/跳转发起 | 0；301响应即停止 |
| LIST / STS / 其它数据API | 全部0 |
| manifest声明长度、ETag/VersionId绑定 | NOT_RUN / UNKNOWN；无成功HEAD结果 |
| manifest实际应用GET正文 | 0字节 / 8,388,608字节 |
| v2_1精确UID命中数 | NOT_RUN / UNKNOWN，不填成0匹配 |
| 无歧义可HEAD候选数 | NOT_RUN / UNKNOWN |
| 媒体大小已知/≤4GiB数、合计≤8GiB | NOT_RUN / UNKNOWN |
| 媒体GET / Range / 视频正文 | 全部0 |
| GPU / 真实模型 / ffprobe / 解码 | 全部0 |
| 现场执行耗时 | 约2.230秒 |

本轮取得真实网络响应类别，证实此次HTTPS请求可到达S3并被重定向，但没有官方CSV、UID_PRESENT_IN_V2_1或媒体大小证据。没有读取响应研究正文；应用GET字节0不等于HEAD/TLS/文档交接总wire流量0，不能称真实大文件流控已认证。

## 隐私与结束

0AWS密钥手工读取/打印/复制、profile枚举、登录/刷新/AWS配置修改；0真实媒体或额外标注/模型下载，0安装/合成测试/额外文献与工程规划/原研究树/旧ledger锁/Charades改动，GPU/模型/训练0。私有新脚本及无秘密计数不上传；公有报告不含用户目录、实际文件编号、真实UID、对象URL、ETag/VersionId、原JSON/CSV/QA、密钥或底层异常原文。

仅公有本收据及结果末尾唯一父回报，普通main push一次后停止。输入与profile缺口已解决，当前阻塞是合同不允许跟随的首次301，不要求用户再次发送/更改密钥。RELEASE_AND_CLOCK_BRIDGE_UNKNOWN、MEDIA_GET_NOT_AUTHORIZED、NOVELTY=RETAIN0、Charades FINAL_MEDIA_STOP保持；后续端点核定/媒体下载/GPU需新的明确授权，旧2段/8GiB额度不自动转移。

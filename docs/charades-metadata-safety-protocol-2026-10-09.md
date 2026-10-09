# Charades 原始标注包最小下载与隔离核验：安全执行协议

**记录：2026-10-09｜状态：USER_EXPLICITLY_APPROVED_METADATA_ONLY / NOT_YET_DOWNLOADED / NO_GPU。** 用户明确确认研究用途符合[Charades官方非商业使用许可](https://prior.allenai.org/projects/data/charades/license.txt)，并授权只获取[AllenAI Charades官网](https://prior.allenai.org/projects/charades)所列 **Annotations & Evaluation Code (~3 MB)**，作CSV/时间区间/来源资格统计。未经用户新批准，**不**下载视频、STA、Ego版、媒体帧、特征或任何模型权重，不用GPU、不运行真实视频解码，不修改原Windows研究环境。授权仅适用于本次有限操作，不是无限数据获取批准或数据再分发许可。

## 1. 固定独立存储位置（Windows）

建议、默认且唯一允许的数据落点（由Windows本地环境变量解析）：

`%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-Metadata\`

本次**先于执行固定此路径**，不猜用户账户名，也不向GitHub输出绝对路径。Codex只可在这棵树中创建：

- `incoming/Charades.zip`：唯一原始官方注释+评测压缩包（若响应提供的文件名不同，保留原文件名于manifest并在incoming/只放一个）；先下载临时`.part`，完整校验后同目录原子重命名。
- `extracted/`：只存已核安全的 `Charades_v1_train.csv`、`Charades_v1_test.csv`、`Charades_v1_classes.txt`、`Charades_v1_objectclasses.txt`、`Charades_v1_verbclasses.txt`、`Charades_v1_mapping.txt` 以及ZIP内自带的 `README.txt`/`license.txt`（缺失就只记录官方公共URL；不执行任何随包代码）。实际子目录名以ZIP白名单查找后的安全路径为准。
- `local-audit/`：仅供本机的`source-manifest.json`（官方URL，不含访问token/身份、HTTP status、获取时间、字节大小、SHA256、ZIP文件清单/版本信息、许可URL）；本地可能含受限来源关系，仅留本地，不推送GitHub。

**不允许**将下载包、解压文件或真实行暂存于公共Git checkout、`docs/codex-artifacts/`、原GPU研究工作区、OneDrive同步目录或任意其他路径。不修改已有工作区gitignore来掩盖不合规下载。下载前只读核对以`GetFullPath`/realpath及Windows reparse-point检查确认解析的目标不在这些目录或其父/子目录内，检查磁盘空间≥150MiB和写权限（只对新隔离目录做最小创建测试）；不确认隔离或命中已有非本任务内容**立刻BLOCKED并STOP**。不删除、清理、覆盖已有用户文件；如同名已存在，先核manifest/hash，绝不覆盖。

## 2. 官方来源与单包硬配额

**唯一官方下载入口**：[AllenAI Charades](https://prior.allenai.org/projects/charades)页面文本为`Annotations & Evaluation Code (3 MB)`的**官方S3链接**。由执行者重新从官方页面的该锚点解析最终HTTPS URL，明确对比域名`ai2-public-datasets.s3-us-west-2.amazonaws.com`及服务器重定向目标；**不是**`Data (scaled to 480p, 13 GB)`、`Data (original size)`、`RGB frames`、`Caption evaluation code (70 MB)`或`Charades-STA` Google Drive。

- 下载前以不获取正文的HEAD（若服务支持）查`Content-Length`/类型/重定向。实际单包大小硬上限 **8 MiB**（允许官网3MB估值和HTTP误差，但超过立即拒绝；若服务器无法HEAD仍可流式限量GET）；zip容器须有ZIP签名且可以通过`zipfile`完整性检查。**只允许1次成功内容下载，网络失败最多额外1次独立重试；不要爬镜像或替换为别的数据**。
- HTTP不是200、目标不是经官方锚点明确的安全HTTPS链接、链接变化到非官方域、响应为HTML错误页、超大、hash不一致、截断或空间不够，**STOP**并写脱敏失败报告，不能从第三方镜像补齐。
- 计算压缩包SHA256与字节数，本地manifest记录日期、原始官方URL、ETag/Last-Modified（如有）。SHA是文件指纹，不是媒体PTS/身份或学术split认证。官方可能不提供可比对校验值；没有官方hash时明确`official_sha256=UNKNOWN`，不称供应链验证通过。
- 仅在原隔离目录保存元数据。不向公共Git仓库提交或使用Github Actions缓存传输数据。

## 3. ZIP安全与许可保留

只用已有Python标准库`zipfile`／`csv`／`hashlib`，**绝不执行包中.m/.py/.sh/.exe/评测代码，不运行pickle/matlab，不安装依赖**。

解压前检查完整central directory：每项相对路径、盘符/冒号、`../`、绝对路径、Windows特殊设备名、重名/大小写碰撞、加密位、symlink/特殊类型、嵌套ZIP、单项和总解压上限。建议成员≤200、总声明解压≤64MiB、单CSV≤16MiB、整体层级≤4；zip包可能包含其它脚本和测试submission文件，**只提取显式白名单的6类CSV/TXT字段文件和README/license**；未知成员不执行、不解压，若发现路径逃逸/畸形成员就整个STOP。使用规范化逐成员新文件写入并避免覆盖，不能直接`extractall`。
- 官方[README](https://prior.allenai.org/projects/data/charades/README.txt)说明压缩包含 `Charades_v1_train.csv`、`Charades_v1_test.csv`及类/对象/动作映射文件等；[独立license文本](https://prior.allenai.org/projects/data/charades/license.txt)需保留其来源链接，不因压缩包中缺LICENSE就推论不存在许可。
- 若表中包含`script`、`descriptions`、`subject`、`id`，只能在本机计算资格，严禁打印/上传CSV行、原始脚本、文本、subject/video ID映射、模型答案、精确小组记录。不存能够逆推出原始行的公开摘要。

## 4. 标注资格和指标：仅聚合，不做模型实验

逐文件读取`csv.DictReader`（标准库，使用真实header而非MATLAB示例中的固定列序），仅处理`id,subject,actions,length`和必要class/split字段；其它自由描述列不打印、不转储。原始内容不得传入外部API。每一行最多接受有限动作项，非法或缺值分类计数，保留全分母；**不自动校正、删除困难源后伪装全集**。

- **前置完整性**：实际header/encoding、train/test行数、空ID/重复ID、缺subject/跨split subject重合`计数`、类别定义范围、起止有穷非负数且`0 ≤ start < end ≤ length`的候选区间、重复区间、超界/异常/可能坐标精度，不从这些字段宣称真实媒体PTS正确。根据原README`actions`是`class start end`多段分隔，但真实端点/精度尚需确认；如不明确，以`UNKNOWN`继续保守计数。
- **P1同类重复候选**：每个`(video, action class)`分组，报告含≥2条不同、**严格不重叠且间隔>0秒**区间的组数、涉及视频数、重复/相接/同类重叠歧义数与实际分母。敏感性另报固定间隔>0.5s和>1.0s的`组级合格数`，不利用模型输出调阈值。两条记录不证明独立物理事件/完整同类实例序列，也**不**授权自动生成“第一次/第二次”问题。
- **P2异类重叠候选**：同视频、不同class、区间严格交集>0，组级/视频级数；另给交集/min(duration)≥0.5的事前敏感性数及接触边界、非法、完全包含的计数。**异类并发不等于目标自然语言关系、语义因果或可观察性已验证**。
- 数据覆盖：按train/test统计视频数/标注数、视频时长汇总的粗统计、涉及不同subject数与跨split重叠subject**数量**（只供保守来源组提醒，不能以video ID算独立participant N）。不用参与者细粒度映射公开披露；小群统计低于10的组或涉及身份的小单元一律抑制，必要时整体`WITHHELD`。
- **唯一允许公开的科研产物**：上述非识别性整数与粗分层、可安全披露的CSV header字段名、文档版本名和ZIP SHA、统计规则、失败/歧义分母与UNKNOWN列表；不上传每video/class/subject的分布、真实行、文字描述、示例ID、文件路径或图片。若计数本身可能被链接为敏感小单元，应仅报告区间或`WITHHELD`。
- **绝不**构建模型输入manifest、自动回答问题、调用Qwen3-VL/SigLIP、生成可用于重识别的来源join或向公有GitHub上传中间CSV。

## 5. 验收门槛与停止规则

任务可判断的只有`DATA_READY_FOR_FURTHER_REVIEW`（原Charades实际字段与保守资格数量得到证据）／`STOP_OR_UNKNOWN`，不允许`G1 PASS`、`NEW_MECHANISM PASS`、`LONGVIDEO PASS`、`GPU GO`。若P1/P2样本合格候选为0或歧义严重，则停止对应假设；非0也不证明物理实例独立/模型发生错误。Charades短片不是自然长时域数据，STA许可与实际媒体PTS仍HOLD。

**禁止范围再列**：0视频/媒体/帧（任何480p/55GB/76GB等）、0Charades-STA/Charades-Ego/Ego4D数据、0GPU/模型QA/训练/评分/推理、0真实视频解码、0原Windows研究代码/conda/CUDA/进程/锁/账本变更、0历史模型重跑、0对外联系、0修改PR。未授权把个人身份信息或标注文本上传云端。发生权限/许可/文件不符立即停止；不要扩大样本或上网找替代。

**执行控制**：仅在最新主分支明确标记`VLM-BATCH-009=READY`且本任务无已有结果时，由用户**在原Codex聊天**发一次执行指令，Codex完成受限下载＋统计再提交**仅脱敏报告和Codex追加结果**后停机。GitHub文档更新不等于Codex已经执行或数据已经下载。

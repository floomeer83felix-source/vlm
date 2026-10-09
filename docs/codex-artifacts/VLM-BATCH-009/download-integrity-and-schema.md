# VLM-BATCH-009：下载前置与schema阻塞报告（任务1—6）

2026-10-09；文档基线main71a24ab。**整轮BLOCKED_STORAGE_REALPATH_MISMATCH／NO_DOWNLOAD**。用户已授权单个官方标注评测包，但硬路径复核失败；没有数据GET、ZIP、CSV或真实统计。检查失败不等于已经证明目录有恶意链接，也不能当安全通过。未改变落点、放宽规则、改找镜像或继续统计。

## 1. 授权与当前官方条款

重新读取最新AGENTS、唯一READY任务及[固定协议](../../charades-metadata-safety-protocol-2026-10-09.md)，结果文件无本批先前回报。用户已确认其用途符合非商业研究范围，并仅批准官网约3MB的Annotations & Evaluation Code；不授予视频、STA、特征、模型、GPU、原实验目录或分发权限。

本轮重新读取[官方项目](https://prior.allenai.org/projects/charades)、[许可](https://prior.allenai.org/projects/data/charades/license.txt)与[README](https://prior.allenai.org/projects/data/charades/README.txt)。许可正文与BATCH-008读取文本逐字节相同，条款一致性PASS；保留其非商业、禁止第三方分发／公开改造数据及必要学术示例限制，不全文复制。实际下载未发生，不能将许可确认写成数据已获证。

## 2. 固定存储根：前后两层检查必须同时通过

唯一目标仍为`%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-Metadata\`，未向公开仓库披露实际账户路径。已知原研究目录与文档checkout仅用于路径交叉判断，没有扫描研究资产。

| 前置 | 实际检查／结果 |
|---|---|
| 变量／GetFullPath隔离 | PowerShell阶段与已知原研究、文档Git及云同步根的父子重合检查PASS |
| 云同步 | 环境、OneDrive账户及Windows登记同步根共4个候选根参与检查，未命中；只证明所查已知根不重合 |
| 已存在祖先 | 目录类型及ReparsePoint属性检查PASS，未检出重解析点；不凭此替代realpath一致性 |
| 旧内容／覆盖 | 任务根不存在时新建，未覆盖既有用户内容；只作新目录最小写测试，测试文件已移除 |
| 空间 | 创建前可用空间≥150MiB，PASS；不公布用户盘符／账户细节 |
| 下载前Python复核 | `check_ancestors`检查absolute与resolve一致性失败：`STORAGE_REALPATH_MISMATCH` |
| 最终storage_preflight | **BLOCKED**，早期PowerShell PASS不能覆盖后续失败 |

Python复核在打开数据请求之前失败。没有继续展开真实绝对路径、推断为何不一致、修改比较规则或改存储位置。受控目录只含此前准备的空incoming/extracted及local-audit元数据manifest；没有`.part`或数据包。本轮保留状态，不清理／覆盖用户文件。路径差异是否仅命名规范化、或存在其他原因仍UNKNOWN，不能猜成无害并继续。

## 3. 官方单包预检与实际传输计数

从当前项目页文本完全匹配的唯一锚点解析出：

[官方Charades.zip](https://ai2-public-datasets.s3-us-west-2.amazonaws.com/charades/Charades.zip)

该链接HTTPS且host精确匹配协议，未打开网站其他数据入口。无正文HEAD结果：HTTP200、application/zip、Content-Length **3,519,822字节**，低于8MiB硬限；ETag为`8f64f8d7d4cdf0e207e53f8e1fe1703b`，Last-Modified为2021-02-04 00:34:04 GMT，最终URL未改域。ETag只是服务器对象标识，**不是官方SHA256认证**。

| 项目 | 实际值 |
|---|---|
| 数据GET发起次数／成功次数／重试次数 | **0／0／0** |
| 实际数据正文接收及落盘 | **0字节** |
| archive SHA256／实际大小／官方SHA256 | UNKNOWN／NOT_ACQUIRED／UNKNOWN |
| `.part`／原子重命名 | 未发生 |
| 预检大小与完整ZIP校验 | HEAD大小通过；ZIP签名／CRC／中央目录均未实际检查 |

公开文本3次读取＋官方数据HEAD1次；无数据正文请求。早期本地manifest保存的是官网／许可／README和HEAD元数据，不能作为下载成功、archive integrity或CSV资格收据。

## 4—6. ZIP、白名单和真实CSV：未执行

新[通用标准库工具](../../../prototypes/charades_metadata_audit.py)只含安全ZIP成员／白名单、字段读取及聚合逻辑，无网络、媒体或模型。设计拒绝原始危险路径、Windows特殊名字／字符、重名／大小写及文件父路径碰撞、加密／特殊文件、嵌套压缩、成员数及尺寸越界；白名单最多6类表/CSV加README/license，不执行包内任何代码。**这些是实现及合成测试覆盖，不是该官方包安全PASS。**

真实header、encoding、版本、类数、train/test行数、空／重复ID、缺subject、空actions、坏时间／超界／重复区间全部UNKNOWN；不能把未读数据写成0错误。没有创建模型输入manifest、生成问题、读取描述或访问实际来源映射。

### 合成CPU测试收据

Python3.9.21，既有环境，运行指定命令2次，仅新[合成测试](../../../prototypes/test_charades_metadata_audit.py)：首次13方法中12通过、1个反斜杠路径子断言失败，suite0.002秒；原因是Windows ZipInfo构造器已规范化成员名，原实现只看规范化后的值。修复为同时检查原始成员名、补NUL／特殊字符及文件父路径冲突，**保留原失败断言**；第二次13 PASS、0 FAIL/ERROR/SKIP，suite0.002秒，不含启动。该修复发生在任何数据获取之前。

覆盖P1间隔阈值／相接／重复／混合歧义、P2重叠／包含／接触、非法时间与完整分母、重复ID的全部行资格阻塞、跨split subject聚合、空分母、描述不进入输出、小正计数抑制及ZIP边界。未实际运行CSV审计CLI；只在下载前调用路径复核，而该复核失败。

结论：任务1及部分2/3文档／预检完成；**任务2最终BLOCKED、任务3NO_DOWNLOAD、任务4—6真实执行UNKNOWN／未开始**。0视频/STA/Ego/模型/特征获取，0GPU/QA/真实评分/解码/原研究资产修改/外部联系。失败按协议停止，不转为别的下载任务。

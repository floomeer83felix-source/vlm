# VLM-BATCH-010：官方单包获取、完整性与真实schema

2026-10-09；基线main abe39e1。新父任务仅续接未消耗的单包授权，009／009-FIX历史不改、不重跑。**获取与结构解析完成；数值区间质量HOLD**。仅做标准库CPU元数据统计，无视频、STA、模型、GPU或原研究资产修改。

## 1—2. 权限、固定路径与既有状态

重新读取唯一READY任务、安全协议、AGENTS、结果及指定009历史。任务开始无本批回报，文档checkout干净并安全fast-forward。固定数据根仍为`%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-Metadata\`；不披露实际账户路径、不换落点。

修复版check_ancestors复核samefile／非零目录inode、device一致、规范名称稳定、逻辑和规范两条祖先链无reparse，通过。逻辑／规范落点均与已知原研究、文档Git及4个登记／环境云根无父子重合，规范落点位于LOCALAPPDATA内。空间≥150MiB；仅用本任务新空探针确认可写并移除探针。incoming/extracted为空，仅旧任务来源HEAD manifest存在；核其task与successful_data_gets=0，不覆盖旧manifest。

[当前官方许可](https://prior.allenai.org/projects/data/charades/license.txt)与旧许可SHA一致，包内license也与官网逐字节一致。用户已确认非商业用途；仍禁止第三方分发、公开改造数据，本轮不发布原标注或文本。README/许可保留在隔离目录；新010 manifest和完成收据仅本机，不上传。

## 3—4. 唯一官方来源和实际流量

从[官网项目页](https://prior.allenai.org/projects/charades)唯一Annotations & Evaluation Code (3 MB)锚点重新解析，目标固定为[官方S3 Charades.zip](https://ai2-public-datasets.s3-us-west-2.amazonaws.com/charades/Charades.zip)。HTTPS且host精确匹配；重定向拦截未遇陌生域，不访问其他资源。

| 收据 | 实际值 |
|---|---|
| 本轮HEAD | 200，application/zip，Content-Length 3,519,822B |
| HEAD/GET对象标识 | ETag `8f64f8d7d4cdf0e207e53f8e1fe1703b`一致；Last-Modified 2021-02-04 00:34:04 GMT |
| 数据GET尝试／成功／额外重试 | **1／1／0**；授权的一次成功下载已使用 |
| 实际包字节数 | **3,519,822**，低于8MiB硬限 |
| 实际SHA256 | `c616913ef79c2ddde06d9c562eae57bb8901d459d7568a0d27bf09cbf33ae866` |
| official_sha256 | **UNKNOWN**，未见独立官方校验值，ETag不充SHA认证 |
| 本地落盘 | 64KiB块流式写incoming/.part，长度与ZIP magic核验后原位置原子改名；无旧包覆盖 |

官网／license／README另3个公开文本响应，共76,881B；没有其他数据GET。HTTP头与工具通信未计入该正文字节数，不把它当全网络流量。下载执行为短期标准库urllib操作，无新公共网络runner、依赖安装或环境变更。

## 5. 实际ZIP安全与白名单

中央目录**14成员**，声明解压总量**9,591,127B**；成员／总量／单文件／层级在协议上限内，路径、原始名字、Windows特殊字符／设备名、大小写／父路径碰撞、加密／特殊类型及嵌套压缩检查通过。CRC完整性PASS。仅提取8个白名单basename：train/test CSV、class/objectclass/verbclass/mapping TXT、README、license；其余6成员不解压、不执行，不公开完整成员清单。

白名单新文件以exclusive模式逐个写入，未用extractall、未执行任何.m/.py/.sh/评测程序。全部数据及含本地成员清单的manifest留在协议隔离树。计算SHA只是固定此包字节／版本，**不证明实际媒体PTS、事件身份或来源独立**。

## 6. 真实CSV、完整分母与重要质量冲突

两CSV用UTF-8-SIG解码器成功读取、csv.DictReader按真实header解析；是否带BOM没有另作判定。实际header两split一致：`id, subject, scene, quality, relevance, verified, script, objects, descriptions, actions, length`。共11列，比网页的简化字段列表多objects；没有按MATLAB示例数字列索引取值。只以id/subject/actions/length及类表计算，未使用或输出脚本／描述内容。

| 结构／全分母 | Train | Test |
|---|---:|---:|
| CSV行／唯一video ID | 7,985／7,985 | 1,863／1,863 |
| 原始动作token | 49,809 | 16,691 |
| 通过既定数值规则的token／distinct有效区间 | 35,211／35,211 | 11,664／11,664 |
| 未通过规则的token | **14,598** | **5,027** |
| 含无效动作的行 | **5,896** | **1,537** |
| 空actions行 | 174 | 49 |
| 空ID／空subject／duplicate ID额外行 | 0／0／0 | 0／0／0 |
| 不规则行形／缺必需值／非法length | 0／0／0 | 0／0／0 |
| 无法拆三元组／未知class／非finite或不可解析时间／负起点 | 0／0／0／0 | 0／0／0／0 |
| 有效区间中的确切重复 | 0 | 0 |

类表157类。上表0来自完整循环的实际检查，缺省Counter项按其受测条件解释为0；未测语义／媒体项目不填0。无效token不从原动作分母删除，P1/P2仅使用规则通过的distinct区间，不意味着整行或完整同类序列通过。

主要冲突为`end>length`，Train约14.6k、Test约5.0k；以粗量披露，避免反推已抑制的小异常类别。`start≥end`存在正小计数，**WITHHELD_LT10**。原始66,500 token中19,625未通过，即约29.5%；9,848行中7,433含无效动作，即约75.5%。这表示当前**数值合同冲突**，不能直接断言原数据损坏、某字段单位错误或parser正确解释了全部语义。

未缩放、平移、钳位、删除异常或调整源码；发现后停止后续数据诊断，仅整理既有聚合收据。时间单位／length来源／区间覆盖及真实媒体对齐原因仍UNKNOWN。结构解析PASS与数值质量HOLD分开，不能给全集资格PASS。

固定字节：train CSV SHA256 `59273c6dc2139ec7eb95b980fd26bc8529774b1ede0602f6ca90b546ed12f0fc`，3,622,045B；test CSV `8b8b207b55fb95b949018027f69d83bd46cd844d15834f8f592ee8e7446173eb`，1,173,833B。这里只给文件级版本指纹，不给任何逐视频／人物hash或行内容。

### 本轮测试与停止

既有Python3.9.21，源码未修改；指定标准库合成suite本轮1次，**21 PASS／0 FAIL/ERROR/SKIP，0.034秒**，不含启动。真实审计器本轮1次成功返回并在隔离树生成聚合摘要；CRC及结构成功不证明物理事件／视觉性能。0视频／STA／模型／特征／GPU／QA／真实解码／原研究环境改动／外部联系。后续科学判断见[资格报告](./qualification-and-decision.md)，本轮只上传两个报告和一条结果。

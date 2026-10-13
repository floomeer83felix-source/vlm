# VLM-EGO4D-BOTO3-001：离线映射与预算程序实测收据

2026-10-13。**SYNTHETIC_MAPPING_AND_BUDGET_READY**：新增两个可执行stdlib文件，最终32项unittest与CLI self-test、完整synthetic演练均退出0。不是AWS_ACCESS、MEDIA_READY或真实网络硬限证明；NOVELTY=RETAIN0。

公有docs checkout安全同步main `d776403`，唯一READY/无既有父回报，重读AGENTS、任务板/结果/总览、合同及工具和媒体收据。没有访问专用venv或旧研究树，也未重跑旧父任务。

## 固定官方源码与实际差异

阅读Ego4D固定commit `4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb`的三文件，未执行官方代码或连接其数据服务：

- [manifest.py](https://github.com/facebookresearch/Ego4d/blob/4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb/ego4d/cli/manifest.py)：`VideoMetadata`区分file_uid/video_uid，支持canonical_s3_location/s3_path；`_manifest_object`按public/version/dataset组织清单。file_uid存在时官方对象uid优先取它，新合成门保守拒绝file_uid冒充视频匹配。
- [config.py](https://github.com/facebookresearch/Ego4d/blob/4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb/ego4d/cli/config.py)：VERSION_DEFAULT=v2_1、DATASET_PRIMARY=full_scale；**实际argparse datasets默认annotations**，不能将PRIMARY常量称作CLI默认选择。其validate_config还会创建Session，故本轮不导入/调用。
- [download.py](https://github.com/facebookresearch/Ego4d/blob/4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb/ego4d/cli/download.py)：GitHub blob首次不可得，改读同官方仓库同固定commit的[原始源码](https://raw.githubusercontent.com/facebookresearch/Ego4d/4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb/ego4d/cli/download.py)。UID过滤依赖VideoMetadata.uid；存在并发及SDK重试配置、download_file，不能用作本工程累计硬限。

**不采用不符的默认假设**：新门要求显式full_scale，release枚举为v1/v2/v2_1，不把HourVideo v1.0转成v1。来源默认RELEASE_BRIDGE_UNKNOWN；仅纯虚构成功分支接受显式SYNTH_BRIDGE_CONFIRMED，公开结果仍REAL_BRIDGE_NOT_VERIFIED。

## 程序与真实执行

[主程序](../../../prototypes/ego4d_boto3_offline_gate.py)和[测试](../../../prototypes/test_ego4d_boto3_offline_gate.py)均新建，没有修改任何旧程序。可在公有checkout复现：

```powershell
python -B -m unittest prototypes/test_ego4d_boto3_offline_gate.py -v
python -B prototypes/ego4d_boto3_offline_gate.py --synthetic --self-test
python -B prototypes/ego4d_boto3_offline_gate.py --synthetic
```

| 实际执行 | 结果 |
|---|---|
| 初版unittest | 30/30 PASS，退出0，1.871秒 |
| 初版CLI self-test | 30测试、29通过/1 ERROR，退出1，1.744秒；未运行随后的dry-run |
| 修正后unittest | 32/32 PASS，0失败/错误/跳过，退出0，2.215秒 |
| 修正后CLI self-test | 32/32 PASS，0失败/错误/跳过，退出0，1.904秒 |
| 完整CLI演练 | 退出0；两虚构对象完成，重启拒绝重复GET；预扣与接受的模拟字节均18，真实请求/视频/GPU全0 |

指定unittest执行2次、CLI self-test2次、测试文件直接执行1次、完整CLI演练1次，5次suite共156次方法执行。初版错误保留：Windows替换既有ledger目标出现PermissionError，残留pending导致第二次写入拒绝。修正为**不覆盖已存在文件的连续原子快照**：每代先fsync，再os.replace到未存在的新文件；读取时检查连续序号、各代checksum及前驱摘要链。新增历史损坏和写入失败不重试测试；不删除pending继续执行、不使用睡眠/写入重试掩盖问题。测试累计框架wallclock9.617秒，均为CPU工程测试，不是GPU或下载速度。

补充执行测试文件直接入口（python -B prototypes/test_ego4d_boto3_offline_gate.py -q）：32/32 PASS，退出0，1.883秒，确认第二份Python亦可直接运行。

## 机械映射、计费与恢复门

仅内存生成SYNTH UID/CSV；严格识别video_uid与两个来源字段，重复header/UID、file_uid、缺字段、冲突来源、非S3/不可信bucket、空或错误key、穿越/分隔异常等拒绝。虚构桶名和public/version/full_scale/UID路径是**测试策略**，不是声称真实所有官方对象遵循这个媒体key布局；不会凭字符串对真实来源授权，也不使用URI联网。

Request描述符是冻结的**模拟HEAD结果**（长度、ETag、version ID），不是一次AWS HEAD调用。未知长度或单视频>4,294,967,296B拒绝；最多2个不同视频；所有计划GET上界合计≤8,589,934,592B，含metadata≤33,554,432B。全计划先验检查保证每个对象有上界、总预算可容纳，STARTED在接受响应前持久预扣；错误/未终态/中断不退款、对象不自动重试，新run ID或配置变更不能重置已有账本。

完整流模拟分别统计reserved和actually_read；提供整数块，不实际分配GiB。8GiB边界测试只处理两个4GiB整数，单快照远小于5KB。status/encoding/content length/ETag/version改变、非预期206或重定向/重试拒绝；错误正文受上界约束并计入模拟实际读取，短读/异常保留partial与失败状态。中断后仍STARTED，另一冻结对象可依余量继续，原对象不能重复。跨进程非阻塞OS锁冲突拒绝，不删除他人锁。

程序限定自己tempfile目录的合成账本，CLI拒绝real/profile/manifest/video/s3/download等实时flags，live接口始终LIVE_ACCESS_NOT_AUTHORIZED。临时根退出仅清理自己文件；源码指纹及冻结计划随快照绑定，原始期次/旧账本不读取。32项测试涵盖合同至少18项要求、错误正文、恢复等价、账本链与写入故障；未安装/导入boto3，没有凭据或SDK实例。

## 必须保留的未知

整数块表示**拟接受的读量**，超过已知上界的拟读块在接受前拒绝；这不证明真实HTTP已收到超长buffer后仍能让网络实际字节不超限。线上失败正文、SDK隐式重试/连接中断、压缩/Range语义、代理、服务源身份与跨恢复流量统计均REAL_TRANSFER_ENFORCEMENT_NOT_VERIFIED。ETag仅用于身份相等性比较，不当MD5或发布checksum。

原子快照通过正常中断/损坏模拟，不认证机器停电耐久性、恶意删除整条快照尾链或备份回滚、共享文件系统锁。程序也不是接受任意真实官方CSV的生产下载器：实际manifest真实性、桶授权白名单、release桥接、媒体大小/时钟、许可/身份与AWS权限仍未取得；旧开发集数量PASS不改变这些门。

## 交付与停止

本轮0 AWS认证/Session/client/S3 HEAD/GET/LIST、0真实HourVideo JSON/UID/QA/视频/数据manifest访问下载、0PyPI/依赖安装或venv修改、0GPU/模型/解码/ffprobe、0原科研环境/旧资产/锁/ledger改动。网络仅官方公开源码阅读与授权Git交接；不发真实对象请求。源码/收据只含虚构值，不上传原日志、manifest实值、私有路径、身份或凭据。

严格四处新增/追加，正常main push一次后停止，等待ChatGPT验收。真实bridge/transfer仍未认证，Ego4D批准用户确认至2026-10-26不加速跳门，不转移旧2视频/8GiB下载授权，不自动开始下一轮媒体或GPU任务；Charades FINAL_MEDIA_STOP保持。

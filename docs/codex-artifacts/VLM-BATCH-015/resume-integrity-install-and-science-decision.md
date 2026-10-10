# VLM-BATCH-015：续传完整性、最小工具部署与科学裁决

2026-10-10。最终工具门通过：`CPU_TOOL=AVAILABLE_PUBLISHER_HASH_VERIFIED`，仅在发布方固定SHA范围内验证；媒体与科研真值门保持HOLD。

## 真实完整性与最小部署

原part/旧账本与固定预期相符，27项最终合成测试PASS，两次HEAD及1字节探测实际206资格通过；唯一后缀GET完成。没有新整包下载、自动重试或换源，未修改014公共历史或旧ledger。原part仅增加获准后缀，原前缀私有SHA复核不变。

拼合长度实测114,768,076 B，完整SHA-256与冻结发布方`60f467265b1e312373dbcd92200c2618a74850f98d3d078e94296bb3fa2047ba`完全一致，并在部署后再次只读核验。故现存旧前缀和新后缀共同组成该冻结发布包。014首次ETag并未追溯恢复，1字节探测单独也不证明整个前缀；完整SHA提供本次拼合文件的最终桥接证据。发布方同站SHA不是独立数字签名或无恶意软件保证。

仅复用只读014安全助手safe_tool_members、zipfile全成员CRC、原白名单及独占提取逻辑。实际ZIP路径/单一ffprobe/许可证/无禁止DLL及展开预算检查PASS，全成员`testzip()` CRC PASS，白名单实际提取3个文件：唯一bin/ffprobe.exe、LICENSE、README.txt。其他exe未提取或执行；旧part和两代ledger保留，没有extractall或系统安装。

实际仅一次完整私人路径`ffprobe.exe -version`，timeout=10秒，返回0，输出首行为`ffprobe version 9.0.2-essentials_build-www.gyan.dev Copyright (c) 2007-2026 the FFmpeg developers`。exe SHA在本机记录并随后只读重核一致，不在公共报告中输出。`Authenticode=UNKNOWN_NOT_CHECKED`，不能写数字签名通过；版本健康检查只证明本机无媒体启动可行。

本轮新增工具正文101,660,877 B，两轮累计114,847,784 B；新GET2/HEAD2、重试0。最终逻辑文件字节220,068,317 B；最大观测文件名逻辑和325,212,443 B（硬链接名重复保守计数），含瞬时账本额外1MiB预留上界326,261,019 B＜512MiB。精确物理分配峰值未测。[双账本与网络资源细表](local-part-ledger-and-remote-identity.md)解释计量范围及旧账本只读证据。

## 科研与媒体边界

工具成功与否均不放行旧013/FIX或后续媒体任务。旧媒体客户端默认ProxyHandler风险没有在本批修改或复测，`MEDIA_NETWORK_CLIENT_PROXY=PROXY_HOLD`；`V1_MEDIA_ACCESS=NOT_RUN`，0 Charades媒体/Range/packet PTS/视觉解码/动作人工核验。A官方评测兼容性的既有限域结论不扩大，B时间质量/C事件真值HOLD、创新RETAIN 0、Charades单独自然长域缺口不变、GPU BLOCKED。

| 步骤 | 最终状态 |
|---|---|
| 1 任务/历史/独立checkout | DONE：main安全同步，014已结束、015启动时唯一READY且无结果 |
| 2 原part/旧ledger/路径 | DONE：大小、签名、事件、预算、身份/no reparse/已知云根排除与空间吻合 |
| 3 合成前置 | DONE：首26 PASS；加失败探测门后最终27 PASS，0 FAIL/ERROR/SKIP；均先于网络 |
| 4 同源HEAD | DONE：2次同固定对象、114,768,076 B、相同强ETag；不公开ETag |
| 5 探测/后缀206 | DONE：1字节匹配+唯一101,660,876 B后缀，If-Range、精确范围/长度/identity/ETag通过，无重试 |
| 6 全包最终SHA | DONE：与冻结发布方SHA完全一致，最终只读复核PASS |
| 7 ZIP/CRC/白名单 | DONE：全CRC PASS，仅3白名单新文件，旧part与旧ledger保留 |
| 8 版本健康检查 | DONE：实际一次、返回0、9.0.2、0媒体输入，签名仍UNKNOWN |
| 9 双账本/隐私/资源 | DONE：旧ledger和原前缀不变、实际/预留相等、预算内；精确物理峰值未测，仅公开逻辑和保守上界 |
| 10 独立裁决 | DONE：工具可用/工具206通过；媒体PROXY_HOLD和NOT_RUN、B/C HOLD、RETAIN 0、GPU BLOCKED |

下一步仅由ChatGPT审查和安排新父任务；需要先独立修复/测试媒体客户端代理继承，再决定有限媒体试点是否可以执行。本批不创建下一READY、不自动执行013/FIX、媒体获取或任何研究实验。正常push后停止，保留原聊天。

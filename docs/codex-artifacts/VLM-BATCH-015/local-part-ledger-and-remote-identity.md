# VLM-BATCH-015：原部分文件、双账本与远端身份

2026-10-10。最终收据：`TOOL_RANGE_SUPPORT=VERIFIED_206`，`CPU_TOOL=AVAILABLE_PUBLISHER_HASH_VERIFIED`。基线main `67590a0`，独立docs checkout安全fast-forward，启动时唯一READY=015、014已有结果、015无结果。原研究目录、014公共文件与旧私有账本不改；仅按授权追加旧part后缀。

## 恢复前只读核验

固定工具根为`%LOCALAPPDATA%\VLM-Research-Isolated\CPU-Tools\ffprobe`。本机Windows x64/Windows10+、双路径祖先身份/no reparse、已知云根与原研究环境/docs/metadata/media兄弟树排除、同盘≥1GiB空闲均通过；没有修改PATH或Conda。实际私人路径、代理设置不公开。

原part确为普通单链接文件13,107,200 B，开头PK ZIP签名通过；原账本574 B，body=13,186,907 B、GET4/HEAD3、完整ZIP0、版本调用0、BLOCKED timeout。三个TEXT COMPLETE事件27,484/52,159/64 B与末尾PACKAGE STOPPED 13,107,200 B相加一致。根内只有这两文件，无旧续传账本、额外工具或已安装exe。原part及旧账本SHA在本机计算并留作私有基线，不公开部分指纹。

原工具硬限157,286,400 B，剩余144,099,493 B。本批独占创建新续传ledger，继承旧实际正文、GET/HEAD和原事件，旧ledger始终只读。原part只能ab追加，不删、不覆盖或复制成新整包。

## 合成先于网络

首轮26方法全部PASS，suite1.447秒；再增加“失败探测不能解锁后缀”防御和回归，最终一次27方法全部PASS，0 FAIL/ERROR/SKIP，suite1.400秒。所有HTTP/ZIP/路径与进程均虚构或mock，无真实网络/媒体。测试覆盖代理污染禁用/TLS/拒绝跳转、固定源、弱ETag/200/416/错范围/长度/编码、If-Range、旧前缀变更、账本继承与旧文件不改、独占创建、读前持久保守预留/预算/短读/次数、固定SHA否决、ZIP64/CRC/许可证/危险路径/DLL/已有exe/版本异常和隐私。

测试完成后默认`--preflight`实际PASS，0HTTP/0本地写入，再仅一次运行`--resume`。没有重跑014安装器或测试，也没有在真实错误后改代码重试。

## 本会话远端资格

仅[冻结Gyan9.0.2对象](https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-9.0.2-essentials_build.zip)，显式ProxyHandler({})、默认TLS和NoRedirect，无网页/checksum GET。两次HEAD返回资格通过，同Content-Length=114,768,076 B、ZIP类型、相同带引号非弱ETag，ETag仅保留私有账本。1字节探测固定offset 13,107,199，与原part边界逐字匹配，实际206、精确Content-Range/Length/identity和同强ETag通过。

随后仅一次请求后缀`bytes=13107200-114768075`，带If-Range，预期101,660,876 B；响应必须实际206且对象身份相同才读正文。没有重新GET整包、第三个GET、代理、镜像、latest或自动重试。强ETag只能约束当前HEAD/206会话，边界1字节不能认证整个旧前缀；只有最终拼合SHA匹配发布方冻结值才能补足014缺失ETag证据。

## 最终双账本和资源收据

新GET最多2、HEAD最多2；每chunk≤64KiB，在read前原子写入并fsync保守预留。actual body和charged upper bound分开；预留从不减，读取异常仍保守占额。旧13,186,907 B计费不重置；本批HEAD正文0，探测1 B另计，失败读入也计费。传输不完整不得认证工具已就绪。

| 项目 | 真实结果 |
|---|---|
| 014原正文 / 本轮新增正文 | 13,186,907 B / 101,660,877 B |
| 探测 / 唯一后缀 | 1 B / 101,660,876 B，均COMPLETE |
| 两轮累计实际 / 保守计费上界 | 114,847,784 B / 114,847,784 B；本次无未决预留差额 |
| 剩余总预算 | 42,438,616 B；没有新增额度 |
| 本轮HEAD / GET / 重试 | 2 / 2 / 0；没有网页或checksum GET |
| 继承后总HEAD / GET | 5 / 6；含014原3 HEAD/4 GET |
| 完整part文件长度 | 114,768,076 B，与两次HEAD一致 |
| 本轮前后原前缀 / 旧ledger | 私有SHA复核均不变；旧ledger仍574 B |
| 新ledger | 独占创建、1,823 B；两事件read=reserved=expected，均COMPLETE；原事件和总计复核相符 |
| 最终本地逻辑文件字节 / 文件数 | 220,068,317 B / 6 |
| 最大观测文件名逻辑字节和 | 325,212,443 B；提取原子发布时两个硬链接名保守重复计数，不能称实际物理磁盘分配峰值 |
| 瞬时账本临时文件保守上界 | 上述观测值加1MiB预留，≤326,261,019 B，低于536,870,912 B硬限；精确物理分配峰值未测 |

全部现存文件仅完整原part、旧ledger、新ledger、bin/ffprobe.exe、licenses/LICENSE和licenses/README.txt；最终无原子ledger `.next`残留。完整ZIP仍用原part文件名保留，没有删除、复制或替换原part。旧13,107,200 B前缀在本轮前后私有SHA一致，旧ledger整体SHA一致；完成后的全包SHA再次只读核验等于冻结发布方值。exe私有SHA也与安装阶段记录一致，没有再执行版本命令。

传输全部成功才消除本轮预留与实际差额；若读超时，代码会保留读前预留作为保守计费，而非宣称所有未返回的字节为0。本轮未触发该失败路径。网络资源依合同计应用层读取/预留的工具HTTP正文，不当作网卡/TLS总流量计量。

0 Charades GET/Range、0视频/PTS/GPU/模型；私有ETag、部分指纹、exe hash、本地ledger、ZIP和exe不上传。没有改旧014代码/报告或原科研环境。本次续传资格只证明固定工具对象，不证明Charades服务Range能力。

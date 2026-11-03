# 080 执行回执

2026-11-03 Asia/Shanghai。**PARTIAL_JOURNAL_AND_FIVE_MEDIA_PASS / TRUNCATED_RANGE_RESPONSE / INCOMPLETE_NO_SCIENTIFIC_GATE**。

独立文档 checkout 初始干净，一次fetch并安全快进48dd29c→678a00b3e4a22be2e7559463fec7006baef78a05。重读AGENTS、当前看板/results/总览、080合同/扣账和079验收，核唯一未交付READY及用户明确启动；同范围未重复申请批准。新080根原不存在，首次同步前持久父时钟；起始free 342,143,442,944B≥12GiB。旧078/079/076只读，无扫盘/reset/rebase/clean，未改旧失败和锁。

完整实际worker/supervisor/journal/network恢复、输入、训练、评分及独立oracle在正式payload前封存。Pipeline LF SHA256 **`074498ef740ded1c869e845d686edbdf31e18957c201a48458a62dd0b58c555c`**；只读 progress组件 **`0b12bfed5a2f74f4856ca841967d648fbd29fd3337e96d0a37ba7b0cf1d44140`**，identity组件 **`89567c6d5d31166be0e319cf4837292c828d2c593c8d4d6d843fd154df7edf6c`**。版本v1，后置代码修改0、非科学修复1（仅报告显式UTF8读取，原render v1保留，科学pipeline不变）；六科学函数AST精确等价078。建根host脚本一处数字开头keyword语法错在脚本执行前修正，随后空路径启动未触及Job/HTTP；无正式输入重试。该记录保留在私有prepayload note，不追称原host命令成功。

## 本轮实际阶段

- Windows通信fixture：218检查、201次append及1个拆半行记录，通过共享句柄/校验链/deadline/损坏拒绝/模拟replace不被调用/fsync失败后禁写。耗1.156s，模型/媒体/网络0。
- reuse080：0.844s，复用闭合metadata/真实media-plan/GT/关系/缓存注册和36帧fixture，历史22987/3556与成功head/processor fixture没有重跑。当前SHA与旧闭合seal关系注册，不把新hash冒称历史证书；缓存12stat/小源码连续，新全权重hash0。
- first_media_reuse：0.312s，一次只读15770653B，size/CRC/SHA通过，写080首成员新seal并引用旧只读文件；新HTTP/BZIP2均0。
- network：244.000s/1788.45，15新请求、14CLOSED/1FAILED，新应用body95375536B、新Range预留98494094B。4新媒体完成后立即flush/fsync/CRC/SHA/member seal再发下一源；加首个复用，共5seals/78060287B。第15请求正文实际32956271B/声明36074829B，EOF短少3118558B，ValueError TRUNCATED_RANGE。exit1、nokill、supervisor stop=None、最终active0；最后151条完整journal终态FAILED、writer未坏。没有吞错误转IDLE，也未发生活跃状态文件rename/replace/truncate/delete。
- independent：0.359s/599.52，预封bookkeeping55检查PASS；停止核验6个finalactive0记录含4当轮Job+2复制历史079Job。不是6个新执行，也不是完整科学输出复核；后者NOT_RUN。全部当前5Job最终active0。

完整31成员获取未完成，不能执行32源解码或以5源代替训练。合同唯一允许重取的是079中断成员的一次恢复，已按本轮第1新成员完成；本轮新失败不能再GET/续传。78个请求余量只够26未请求成员，不能使失败成员额外重取变合法。唯一一次非科学修复用于报告显式UTF8加载，原失败render代码保留，下载与科学pipeline未改；它不能用于HTTP重取；不越界增加HTTP，不请求同范围重复批准，不伪造科研阴性。

## 累计、计量与覆盖

本轮准入准备 2.312s/538.83（前轮合计61.156s）；网络244s+旧11.547s，未耗解码/GPU/真实训练。训练仍原4500更新/1796.25s未执行，旧synthetic3.750s保留；新review0.359s加旧0.468s。079旧Range保守占用36263866B，不用应用34690881B当wire；新预留98494094B，累计134757960B/805306368B，新应用95375536B另列。无redirect、整包、额外retry/resume/源替换。

当前显式settled读取 **{'old': 787791, 'prepared': 235446, 'media': 15770653}**，未结算reserve 0。新上限old7292402B/prepared12881386093B/media4GiB/hash0；首视频CRC/SHA读取15770653B计media。读前stat/limit/fsyncreserve、读后settle；强杀未结算不清零。078未知old32MiB/prepared12GiB/hash12GiB仍保留上界，079settled1096206B/3515795B另列，不冒称实际0。HTTP Range长度为读前持久上界，应用计数与UNKNOWN的wire/socket预取分开。

当前进程basename汇总 {'python.exe': 5, 'conhost.exe': 5}；Accounting总10、采样PID记录10，快进程遗漏0，不称完整树认证。Accounting.active峰2/8，native线程峰6/256；limit readback active8/16GiB/kill-on-close均PASS，一个科学worker。codec/Torch科学阶段NOT_RUN，既有Torch/BLAS4/interop1约束不扩大。20ms进程/线程和周期三根quota不是连续硬OS认证；host/Git/控制/报告/代码seal自检、框架native/物理IO不全量计量，完整resource certification=false。

078父1062.250s，079父1267.284s；080报告1490.305s/12000，三父合计3819.839s/14400，用户等待未计。旧两根127文件/18,941,802B；新根报告91文件/63,409,049B，三根低于4096/8GiB，checkpoint0/64MiB。最终私有闭合保存推送/最终wall/quota/active0。

精确九处：公开实际080pipeline、七报告/表及results唯一append；metadata/identity/progress组件、负责人README/看板/决策/总览与历史只读。无raw QA/GT/源ID/时间戳/member映射/媒体/RGB/特征/state/weights/私人路径/凭据进Git。保留Google DeepMind Perception Test归属、固定revision3938d2f1ba3a6b502025741cea4cd73c7b3bdfaf、数据CC-BY-4.0/软件Apache-2.0及derived采样拼接说明。无环境变更、论文、旧QA训练、后台或自动081；一次普通main推送后STOP。

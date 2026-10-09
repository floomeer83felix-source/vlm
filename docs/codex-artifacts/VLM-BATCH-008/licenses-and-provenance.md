# VLM-BATCH-008：许可与出处（任务1—2）

2026-10-09；执行基线main eb2c53f。只读官方网页、许可及作者仓库展示页，不获取标注、视频、特征或Drive内容。ALLOWED只表示条款允许的用途类别，不表示本项目已完成全部使用前提或获准下载。

## 1. Charades原许可：目标用途的有条件准入

实读[官方许可](https://prior.allenai.org/projects/data/charades/license.txt)，题名为“License for Non-Commercial Use”，正文2016版权声明；[官方项目](https://prior.allenai.org/projects/charades)指向该许可和公开下载入口。本轮逐条阅读、以下为释义，不复制整份许可。

| 使用／义务 | 判定 | 条款依据与项目边界 |
|---|---|---|
| 学术、非营利或政府资助研究 | ALLOWED，受条款限制 | 原文明确这些研究者的一般使用；本项目可考虑非商业本地研究，但具体主体／资助／商业关系未核，实际用途匹配UNKNOWN |
| 模型评测 | ALLOWED，受条款限制 | 原文另外容许其他场合的评估用途；此句不能被扩张为商业衍生训练／产品部署权。本轮不运行模型 |
| 必要的学术短片段／静帧示例 | ALLOWED，仅限定情形 | 仅学术发表中为展示示例、实验结果或观察所必要的短片段／静帧，并要求尊重被摄者。本轮不发布图像；没有数值长度上限可凭空填入 |
| 公开改造后的数据 | PROHIBITED（本许可不授予） | 不能以重编码、裁剪、拼接、加标注、换格式消除此限制；代码或统计报告也不得夹带可恢复数据 |
| 将数据以任何形式分发给第三方 | PROHIBITED（本许可不授予） | 公共GitHub不是数据分发渠道；公开视频链接不等于再分发授权 |
| 营利企业中的软件／衍生用途 | PROHIBITED，除非另获适用授权 | 许可未授予该权利；网站列商业咨询途径，本轮不联系、不申请、不假定例外已获批 |
| 许可携带 | ALLOWED用途的义务 | 软件定义包含源码、文档、可执行文件、模型及数据；获准再分发软件时须随附许可。该一般义务不覆盖／取消专门的数据禁止分发条款 |
| 署名／引用 | 应按README引用原工作 | [官方README](https://prior.allenai.org/projects/data/charades/README.txt)请求引用Hollywood in Homes，要求携带license。许可正文并未提供完整通用署名格式；不虚构CC条款 |
| 责任／保证 | 使用者承担责任；无保证 | 许可否认担保，使用即接受其所列责任。网页可访问不证明隐私、机构条件或所有衍生用途已核准 |
| 汇总指标／论文文字 | 非商业评测结果可考虑；特殊披露UNKNOWN | 仅发布不含样本、个人身份或可恢复标注的汇总；完整数据衍生物／公开模型权重的适用范围需另审，不能据一般评测条款自动放行 |

目标限定为非商业本地评测、脱敏聚合结果和论文引用，**许可初筛可条件通过**；实际数据取得、主体匹配、披露及本轮以外操作仍HOLD。这里不是替用户接受协议或保证法律争议不存在。公开页面给3MB注释评测包和13GB480p媒体，是官方体量声明，不是已测包大小或下载授权。

### Charades-Ego候补的许可差异

实读[Charades-Ego项目](https://prior.allenai.org/projects/charades-ego)及[独立许可URL](https://prior.allenai.org/projects/data/charades-ego/license.txt)。本轮收到的许可正文与原Charades逐字符相同，**未见条款放宽**；不能因第一／第三视角配对而认为可再分发。项目称7,860视频、68,536时间标注，是另一资源声明，不能当独立人物／事件数量或天然跨来源确认。未打开其README、媒体、2MB包或任何配对身份。

## 2. Charades-STA：可见性、代码和注释权利分开

实读[TALL作者仓库](https://github.com/jiyanggao/TALL)的master展示页；嵌入页面的当前提交提示为3df6794af1482f5b3d48022bc05e5a4ecfae0e5d。该提示仅记录仓库页面revision，**不固定外部Drive文件的字节、修订或许可**。未打开train／test外链。

| 层面 | 直接证据 | 判定 |
|---|---|---|
| 出处／公开入口 | ICCV2017 TALL作者仓库提供train/test句子时间注释链接，称建立在Charades上 | PUBLICLY_VISIBLE；不是下载或使用权证明 |
| schema | README给video name、start、end、分隔符及sentence的行格式 | 格式DIRECTLY_SEEN；实际文件单位、行数、ID覆盖、边界均未验 |
| 清理声明 | README称相较ICCV版本做过anno cleaning，另列更新的Recall结果 | 声明DIRECTLY_SEEN；清理规则、版本标签、Drive哈希、变更清单UNKNOWN |
| 代码许可 | 读取的根目录展示及README未见明确LICENSE／许可证说明 | UNKNOWN；没有全仓扫描，不能断言所有文件都无许可，更不能推断MIT/Apache |
| STA句子／衍生注释使用和公开权利 | 页面未给独立数据许可，原视频受Charades限制 | UNKNOWN／HOLD；代码开放、作者下载链接和论文发表均不足以授权衍生文本无限制使用或再发布 |
| 上游媒体和文本链 | 原Charades有script/descriptions；TALL[正式摘要](https://openaccess.thecvf.com/content_iccv_2017/html/Gao_TALL_Temporal_Activity_ICCV_2017_paper.html)称添加sentence temporal annotations | 摘要不提供句子取得／清理细节或独立许可，不能把动作标签文字当STA句子权利 |

结论：**原Charades非商业用途可进入下一次最小官方注释计数授权讨论；STA独立权利、清理revision及时间join保持UNKNOWN／HOLD。** 本轮不联系作者，也不读取仓库中样本结果、pkl、模型特征或注释包。权利不明不能由镜像或自行造句绕过。

资源：本报告所涉6个官方项目／许可／README页面加已核TALL论文页面，均在整包12页上限内；未重复访问。数据／媒体／特征／模型下载、GPU、真实解码、原工作区修改及外部联系均0。

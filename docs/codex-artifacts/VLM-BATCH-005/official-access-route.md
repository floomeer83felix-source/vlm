# VLM-BATCH-005 A：TRACE/VES-Bench官方访问渠道

检查：2026-10-09，北京时间；任务基线main 30d142b。仅6项小型官方页面／版本接口，全部HTTP200，实际响应体合计50299 bytes，低于1MiB；最大21795 bytes。没有读取Parquet、视频、题目答案或完整标注，也没有邮件、Issue或表单发送。

## 可验证入口与边界

| 入口 | 实读证据 | 不能推断的事项 |
|---|---|---|
| [作者项目页](https://buaa-colalab.github.io/TRACE/) | 明确链接官方TRACE仓库和HF数据页 | 没有发现mailto入口；不能推断作者没有其他公开邮箱 |
| [TRACE仓库](https://github.com/buaa-colalab/TRACE) | 官方项目链接来源；仓库API为公开、未archived／disabled，has_issues=true | [Issues](https://github.com/buaa-colalab/TRACE/issues)是技术上启用的公开提问入口，不是已确认的专用数据申请通道或答复承诺；本轮没有打开或发布Issue |
| [HF数据入口](https://huggingface.co/datasets/buaaplay/VES-Bench) | 官方README指向该数据；公开、gated=false、disabled=false | 可访问不是媒体／注释研究许可，也不证明完整数据有可用字典 |
| 固定README | 提供全数据下载命令及Parquet／videos目录说明 | 该命令涉及数据本体，本轮未执行；没有专用申请流程或无答案投影说明 |

官方联系邮箱、专门申请表、正式访问资格／审批流程：**UNKNOWN**。不猜个人邮箱，不以GitHub账号名或论文作者名构造地址。用户可以另行决定是否使用启用的仓库咨询入口；实际发送仍须明确授权。

## 版本、许可和字段

- 当前仓库commit仍为 [1b60646dd37657e01b66060bc637742e5d4b5db7](https://github.com/buaa-colalab/TRACE/tree/1b60646dd37657e01b66060bc637742e5d4b5db7)，[README](https://github.com/buaa-colalab/TRACE/blob/1b60646dd37657e01b66060bc637742e5d4b5db7/README.md)和根tree实读；根仅README与assets，API license=null。本轮没有找到明确注释或媒体许可证，但不据此断言数据集无法取得许可。
- HF revision仍为 [b1cdbb370ad866090e6fec82ccb9e699b10edbc7](https://huggingface.co/datasets/buaaplay/VES-Bench/tree/b1cdbb370ad866090e6fec82ccb9e699b10edbc7)，API cardData=null、文件清单无README。没有读文件内容。
- 联合必要区间、600题、348视频和观察审计仍是作者说明，未转化为实际无答案区间schema、正式问答split或同版PTS证明。论文许可不移用为数据许可。

原[VES中英请求草案](../VLM-BATCH-004/ves-access-request.md)保持原样、不重复改写，可供用户确认渠道后审阅。应询问注释／视频分别的本地研究与披露许可、无答案支持字典、版本SHA／clip零点／PTS／parent元数据，不请求整套媒体或正答样本。

## 6项访问清单

1. https://buaa-colalab.github.io/TRACE/ — 21795 bytes
2. https://api.github.com/repos/buaa-colalab/TRACE — 6191 bytes
3. https://api.github.com/repos/buaa-colalab/TRACE/commits/main — 4739 bytes
4. https://raw.githubusercontent.com/buaa-colalab/TRACE/1b60646dd37657e01b66060bc637742e5d4b5db7/README.md — 2454 bytes
5. https://huggingface.co/api/datasets/buaaplay/VES-Bench — 14513 bytes
6. https://api.github.com/repos/buaa-colalab/TRACE/git/trees/1b60646dd37657e01b66060bc637742e5d4b5db7 — 607 bytes

全部完成，没有超限、重试、404链或新候选搜索。这里记录API与页面字节，不含协作仓库Git传输。元数据缓存只在文档checkout的Git内部临时目录，不上传原响应或视频名列表。

**结论：公开获取入口和一个可用的官方仓库咨询入口可定位；专用许可／申请与关键schema仍UNKNOWN，G1继续HOLD。** 无新增证据或作者回复时，不再重复相同官方页面盘点。本轮只定位渠道，外部联系数0。

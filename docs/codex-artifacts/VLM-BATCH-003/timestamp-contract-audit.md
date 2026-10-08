# VLM-BATCH-003 A：时间戳与媒体桥接静态审计

日期：2026-10-08，北京时间。依据main `17a88e2`。复用上轮已完成但未上传的PTS静态审计，按本任务包精简；不重复解码、测试或模型调用，不向旧VLM-PTS-001目录提交。

## 1. 已核代码与结论

| 路径／函数 | 已查静态事实 |
|---|---|
| `active_vlm/video.py::sample_video` | OpenCV读FPS和N、按索引采样、seek后读RGB；timestamp为index/FPS。seek返回成功不是实际展示帧PTS的证明；源码已注明VFR需要PTS-aware后端。 |
| `active_vlm/types.py::Frame` | 只有frame_id、浮点timestamp、image，没有PTS、timebase、stream、clip零点与媒体版本。 |
| `gap_defusion_fresh20_runner.py::prepare_one/process_inputs` | 最近四臂独立读N/FPS、调用旧采帧器，要求timestamp等于frame_id/FPS；媒体SHA和RGB摘要校验存在，但没有PTS桥接。 |
| `active_vlm/gap_defusion_policy.py::native_clip/endpoint_ledger` | 保存源索引/FPS和重复提供槽；IMAGE时间文本三位小数，双帧均值标签一位小数。标签不是区间覆盖依据。 |
| `active_vlm/reference_pts.py` | 接受整数PTS和有理time_base，拒缺失、重复索引、非正时基和非单调；按明确闭区间匹配、不钳位。只处理外部inventory，不生成PTS、不认证媒体版本。 |
| `prepare_natural32.py::decode_worker`、`active_vlm/natural_qa.py::load_frames/frame_manifest` | 历史PyAV两遍解码路径记录并核对PTS×timebase和RGB；保存媒体SHA、stream起点、exact时间，模型仍使用浮点及舍入文本。非零起点拒绝，不是通用裁剪变换；既有8帧接口未接入最近12帧runner。本轮没有运行此脚本。 |

最近run静态manifest有代码／来源／模型pins；一个已存输入的`source_clock`只含FPS、N、frames，pool帧有frame_id、timestamp、RGB摘要和几何。打包scope明确是index/FPS，不是真实PTS。本轮只提取字段名，不公开题目、答案或逐题身份。

## 2. 最小字段契约与缺口

| 字段 | 必须区分的含义 | 当前状态 |
|---|---|---|
| `frame_index` | 绑定媒体SHA与stream的实际展示枚举索引；与候选pool rank、请求seek索引、parent索引不同 | 现路径保存请求索引；PTS历史路径有展示枚举；跨后端等价未实测 |
| `nominal_fps` | 容器描述／诊断统计，不能替代VFR时钟 | 现路径用其计算时间；新契约不应如此 |
| `frame_pts`、`time_base` | integer PTS及rational分子／分母；视频展示时间=两者乘积，不用packet DTS | 纯原语及历史PyAV路径存在，最近runner缺失 |
| `clip_offset`、`clip_time_origin` | 相对clip展示零点，须有声明及映射依据，不能默认为0 | 特定历史零点拒绝规则存在，通用合同缺失 |
| `source_time` | 经过已认证偏移／速率变换的parent视频时间 | 无通用parent／clip版本变换证明 |
| `video_sha`、`media_revision`、`annotation_revision` | 字节身份与标注版本分别固定，附stream及裁剪／转码链 | 字节校验存在；同版注释到媒体桥接UNKNOWN |
| 边界／重复政策 | 原始区间单位、闭／半开语义、量化不确定度、重复PTS及重复提供规则 | 现原语只支持显式closed；新数据政策未冻结 |

PyAV包元数据15.1.0、OpenCV4.11.0.86；继承PATH未见ffmpeg／ffprobe，不能推断整机无工具或PyAV无运行库。未导入AV执行、未安装依赖。`tests/test_reference_pts.py`有不规则PTS、timebase、边界、缺失／非单调和协议SHA声明；`tests/test_natural_prepare_validation.py`有区间补集和失败分母声明。**测试未运行，声明不是真实媒体通过证明。**

## 3. 风险与最小验证设计（未实现）

- **高**：VFR、随机seek帧对应、非零clip起点及裁剪／转码漂移。新adapter须独立保存展示PTS／时基／RGB绑定、parent和clip版本哈希及明确变换；未知HOLD，不fallback index/FPS。
- **高**：用patch均值代替源帧覆盖。例如假设源帧0秒与2秒的均值为1秒，并不代表观察了[0.9,1.1]秒。覆盖要在融合前按唯一源帧真实PTS判定。
- **中高**：float／文本舍入及整秒注释量化；判定使用有理值、显示另存，容差只能来自预先审查的注释精度，不按结果调整。
- **中**：同RGB不同PTS、重复槽、packet DTS、音画起点及不同索引命名空间；分别记账，不隐式去重、平移或借音频时钟补视频支持。

最小输入：视频／注释版本与SHA、stream、逐帧PTS／timebase、clip原点／parent变换、区间语义及容差政策。输出：原PTS与exact时间、已核source_time、源帧/RGB/occurrence映射、每区间成员、patch成员与显示文本、逐条status／failure_reason。不覆盖旧字段、旧run或结论。

未来纯合成测试合同：CFR与VFR有理时钟、不同timebase、非零原点、闭／半开及量化歧义；缺PTS、重复PTS、索引乱序按固定政策失败；parent偏移／速率和版本SHA不匹配；交叠区间、重复提供及patch均值假覆盖。另行授权后才可做CFR/VFR/B-frame小型受控媒体的PTS/RGB及裁剪桥接验证。

现成失败码可复用`MissingFramePTS`、`NonpositiveTimeBase`、`NonmonotonicFramePTS`、`DuplicateFrameIndex`；建议新增`MEDIA_VERSION_MISMATCH`、`CLIP_ORIGIN_UNVERIFIED`、`ANNOTATION_TIME_DOMAIN_UNKNOWN`、`FRAME_RGB_BINDING_MISMATCH`、`INTERVAL_BOUNDARY_UNCERTAIN`。新增码仅设计，未实现。

## 4. 验收边界与追溯

静态审计**完成**，运行时真实PTS／VFR／版本桥接**UNKNOWN／HOLD**；不消除G1、来源指纹或锁未知。模型／QA／解码／测试执行／研究数据下载／原资产修改均0。仅上传摘要，不上传源码、输入正文、身份映射或日志。

代码版本：`active_vlm/video.py` SHA256 `67b6297c1d91dcb613264e90f9dd270a90e5afd384a118414d4361ea7fbdceb0`；`active_vlm/reference_pts.py` `72e48125055239fc6c6bbc323aadae171ae13cd6493e745cbb65f52fa328a905`；`prepare_natural32.py` `cd464f2ecef114b6715cf92155a4a33964e00689c080ed3d8217523d7bab9616`。这是静态版本指纹，不是新运行收据。

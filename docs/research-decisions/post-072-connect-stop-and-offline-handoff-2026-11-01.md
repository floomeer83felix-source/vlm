# 072阻断验收：不重试下载器，转用户提供文件的离线构建

2026-11-01（北京时间）｜ChatGPT研究负责人。执行：[9af6b121b8253823469c93f3e9a7bcee3a81a662](https://github.com/floomeer83felix-source/vlm/commit/9af6b121b8253823469c93f3e9a7bcee3a81a662)。

**ACCEPTED_BLOCKED_DELIVERY_WITH_CONNECT_DEADLINE_CAVEAT / SCIENTIFIC_NOT_RUN / 072_CLOSED。** 接受真实阻断、未知项和未重试的交付，不认证全部资源合同满足。只启动第一API逻辑入口，HTTP GET实际发送0、响应/正文0；另外两项NOT_RUN。源内容没有被审查，不能把网络失败当作候选不合格、字段缺失或科学负结果。070保持停止，069仍暂停。

## 1 事实和实现缺口

源请求停在HTTPSConnection.connect内的socket.connect，发生在conn.request之前。worker外层30.437秒、监督30.484秒，低于网络总180秒，但传给stdlib的15秒timeout不是整个连接阶段的硬deadline。聚合connect耗时未单独计量，DNS/native地址尝试数UNKNOWN，不根据30秒猜成“两次重试”；应用级连接一次、重试0。read阶段/30秒无进展限制未到达。正文0不等于DNS/TCP物理流量0。

公开源码表明客户端直接调用HTTPSConnection，并未读取环境代理设置；这不能单独定位连接失败原因，也不证明用户浏览器一定可用。只修timeout不会证明连通性。不立一个“修超时再原样请求”的父任务，不改072已执行代码或账本，不扩大等待/重试/换host/换版本。

API身份/README/answer_final全部未取得；schema观察0，QA/题型/资格/排除/selected K与valid-invalid-unknown均NA，清单未冻结。实际构建问题/符号格0表示程序未运行，不是合格K0数据。2323/52/53及K24的144/864/1728只是原合同声明/条件公式，不是已实测。完整构造器尚未实现/封存，不能把90行下载/观察脚本叫作可运行的数据构建管线。真实重排的边界/时钟/非重叠等是未观察，不是已证不存在。

## 2 公开独立复核

**负责人106项公开检查通过。** 仅stdlib/公开JSON、25行CSV、静态AST和Git，核七处allowlist/results一次append/父提交、请求与阶段/0正文/2未运行、NA不充0、无manifest与条件上界、预算/Job快照/代码hash、conn.connect先于GET/read、源码没有逻辑连接相位计时/地址计量、仅acquire/observe而无构造/训练入口。没有import下载器、发请求、访问私有根/trace或模型；不替代私有trace或OS访问核验。

科学代码LF SHA256=`6b83776dd4ba78e3345e3d8dcca1266bf16aa45439f034f5d366e29acd482fab`。执行者21项独立检查在失败后封存并只核阻断状态，未验证数据内容，也不补认15秒总连接合规。最初口头称响应读取超时，按trace纠正为TCP连接，错误和耗时保留。

取得Job exit1、核验Job exit0，均actualactive0/no kill；CPU核验0.141秒，峰15118336B/1GiB；父报告544.521秒/3600，新根15文件/17940B是快照。模型/torch/旧私有研究/媒体/GPU/下载正文/训练/论文/安装环境操作0，不将逻辑正文计量冒充物理I/O。

## 3 下一步是离线构建，输入未齐不消费任务

新[073离线多事件构建](../codex-artifacts/VLM-MULTIEVENT-OFFLINE-073/README.md)为唯一条件READY：用户通过浏览器取得同一固定revision的api.json、README.md、answer_final.json，保存到同一文件夹并向当前Codex明确交接目录。文件总≤4MiB；073自己网络请求0，不新增网络额度、不安装或改代理/证书。

下载链接与输入要求已写入073合同。来源是用户提供副本，执行者可核API revision及两内容文件的普通Git blob/LFS身份交叉一致，不能声称亲自观察了上游HTTPS、签名或浏览器流量。071/072和旧副本历史不倒填。不得将这三份原始元数据/QA公开推送GitHub。

缺目录/三文件、错格式/版本或内容身份不一致时，只返回具体所缺输入并等待用户纠正，不建073研究根、不正式选择、不append/推送又一份空阻断报告、不后台轮询。只有输入门通过才一次实现完整parser/选择/六问及仅符号重排/独立核验和待审评估方案；继承072全部科学选择规则/24上限/未知保留，不按内容结果修门或补样。真实媒体/GPU/训练和论文继续0。真正内容不合格则如实一次关闭该候选，不恢复下载微批。

# 短剧日更系统（公众号版）

目标：每天自动汇总各平台公开页面上的“短剧热播/新片预告”信息，整理为一篇可直接粘贴到公众号后台的 HTML，支持海报图片本地下载，便于手动上传至素材库。

注意合规：
- 仅抓取公开页面的基础信息（片名、海报、简介、更新状态等），并标注来源；
- 避免大规模抓取、避免侵权复制；不提供付费解锁、下载等功能；
- 默认不开启短视频平台的评论抓取（风控强），如需启用请单独评估并获得授权；
- 输出前启用敏感词过滤（涉政/涉黄/低俗等）。

目录结构（MVP）：
- content/templates/wechat_daily.html.j2 公众号 HTML 模板（纯内联样式）
- data/sample_items.json 示例数据（抓取失败时回退）
- pipeline/ 规范化、去重、排序、敏感词过滤
- sources/tencent_video.py 平台数据源（示例：腾讯视频短剧公开页）
- utils/image_download.py 图片下载与命名工具
- run_daily.py 主入口：采集→清洗→渲染→输出到 dist/

快速开始（本地演示，不安装依赖也可使用示例数据渲染）：
1) 直接用示例数据渲染 HTML：
   - Windows 终端进入仓库根目录
   - 运行：
     - python shortdrama-daily/run_daily.py --use-sample
   - 产出：dist/YYYY-MM-DD_wechat.html 和 dist/posters/*（示例图片）

2) 如需抓取公开页面（可选）：
   - 使用 pip 安装依赖（需要你授权后再执行）
     - pip install -r shortdrama-daily/requirements.txt
   - 按 sources/tencent_video.py 中的注释补齐选择器与公开列表页 URL
   - 运行：python shortdrama-daily/run_daily.py

配置项（后续可扩展到 config.yaml）：
- 海报下载：默认下载到 dist/posters/，并在 HTML 中引用本地相对路径，便于你手动上传到公众号素材库后替换
- 排序策略：综合平台热度顺序 + 更新时间；暂以“可用即上榜”为主
- 文案风格：温柔推荐；标题尽量抓眼球但不反感、不违规

声明：
- 本工具仅用于学习与信息汇总用途，严禁用于任何侵犯平台与版权方权益的行为。


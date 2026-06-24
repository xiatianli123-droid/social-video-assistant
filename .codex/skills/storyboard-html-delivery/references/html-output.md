# HTML 分镜输出

## 目标

把分镜脚本和设计解析整理成单文件 HTML，便于客户预览或团队交接；只有已经生成首帧图片时才嵌入图片卡片。

## 输出规则

- 生成一个 `.html` 文件时，使用单文件结构：`<!doctype html>`、内联 CSS、语义化 section。
- 不依赖外部 CDN、字体或脚本。
- 保持中文可读性，表格在移动端可横向滚动。
- 若有本地图片，使用相对路径引用；若没有图片，不展示首帧图片区域。
- 不显示 AIG image prompt。prompt 是内部生成逻辑，只有用户明确索要时才另行提供。

## 推荐结构

```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>短视频分镜</title>
  <style>
    body { margin: 0; font-family: Arial, "Microsoft YaHei", sans-serif; color: #1f2933; background: #f5f7fa; }
    main { max-width: 1180px; margin: 0 auto; padding: 32px 20px 48px; }
    h1, h2 { margin: 0 0 12px; }
    section { margin-top: 28px; }
    .summary, .analysis { background: #fff; border: 1px solid #dde3ea; border-radius: 8px; padding: 18px; }
    .table-wrap { overflow-x: auto; background: #fff; border: 1px solid #dde3ea; border-radius: 8px; }
    table { width: 100%; border-collapse: collapse; min-width: 1180px; }
    th, td { border-bottom: 1px solid #e6ebf0; padding: 12px; vertical-align: top; text-align: left; }
    th { background: #edf2f7; white-space: nowrap; }
    .frames { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; }
    .frame-card { background: #fff; border: 1px solid #dde3ea; border-radius: 8px; overflow: hidden; }
    .frame-card img { width: 100%; aspect-ratio: 16 / 9; display: block; object-fit: cover; background: #dfe7ef; }
    .frame-body { padding: 14px; }
  </style>
</head>
<body>
  <main>
    <h1>短视频分镜</h1>
    <section class="summary">项目概览</section>
    <section>
      <h2>分镜表</h2>
      <div class="table-wrap">分镜表格</div>
    </section>
    <!-- 只有生成首帧图片后才加入图片区域 -->
    <section class="analysis">设计解析</section>
  </main>
</body>
</html>
```

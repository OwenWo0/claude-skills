# 发布到 Notion：步骤与坑

## 步骤

1. **读格式规范**：`notion-fetch` 传入 id `notion://docs/enhanced-markdown-spec`。
2. **找位置**：`notion-search` 搜父页面名（如「持续学习」「Claude」），再 `notion-fetch` 确认路径。
   - 新建：`notion-create-pages`，`parent: {type: "page_id", page_id}`；正文里不要再写标题。
   - 重写：`notion-update-page` 的 `replace_content` 替换正文，再用 `update_properties` 改标题、`icon` 换图标。
3. **上传文件（每个文件两步）**：
   - 调用 `notion-create-file-upload`，传 `{filename: "01-frames.svg"}`，返回 `file_upload_id`、`upload_url` 和 `authorization` 头；
   - 用 curl 从本地发送：
     ```bash
     curl -s -X POST "<upload_url>" -H "authorization: Bearer <token>" \
       -F "file=@01-frames.svg;type=image/svg+xml"
     ```
     HTML 文件用 `type=text/html`。返回里有 `"status":"uploaded"` 才算成功。
   - 多个文件可以并行申请上传地址，再在一个 shell 命令里用小函数批量发送。
4. **在页面里引用**：
   - 图片：`![图片说明](file-upload://<file_upload_id>)`
   - 交互 HTML：`<embed src="file-upload://<file_upload_id>">标题</embed>`
5. **读回检查**：`notion-fetch` 页面。`file-upload://` 会变成 `notion-file-block://…`，说明已经挂上。

## 坑

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| 上传过的文件放不进页面 | 没放进页面的上传 1 小时后过期 | 图全部做完再集中上传，传完马上写页面 |
| 正文里 `motion.mp4` 变成 `[motion.mp](http://motion.mp)4` | Notion 把像域名的文件名自动识别成链接 | 文件名一律包在行内代码里：`` `motion.mp4` `` |
| 表格单元格里 `` `a` + `b` `` 变成 `a • b` | 「空格+加号+空格」被当成列表符号 | 改写成「`a` 配合 `b`」 |
| 正文里的 `<` `>` 被吞掉 | Notion 格式会把它们当成标签 | 正文里写成 `\<` `\>`，或者换种说法；代码块里不用转义 |
| 竖线 `\|` 破坏表格 | 特殊字符 | 写成文字，例如「绝对值」 |
| 改写时把链接写成了外链 | 页面之间要用原生引用 | 引用其他 Notion 页面用 `<mention-page url="…"/>` |
| 宽表格挤成一团 | 默认不铺满 | `<table fit-page-width="true" header-row="true">` |

## 常用块

```
<table_of_contents/>
<callout icon="💡" color="blue_bg">
	带走这句话：……
</callout>
<callout icon="🧭" color="gray_bg">
	**这份指南写给谁**：……
	**怎么读**：……
	**你会学到**：A → B → C
</callout>
- [ ] 待办练习
---
```

callout 里的子行要用 Tab 缩进；多行代码用三个反引号加语言名，内容不转义。

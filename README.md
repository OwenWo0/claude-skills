# claude-skills

我自己的 Claude Code skills。每个文件夹是一个 skill，入口是其中的 `SKILL.md`。

| Skill | 用途 |
| --- | --- |
| [illustrated-explainer](illustrated-explainer/SKILL.md) | 图解式讲解：为零基础读者写带大量 SVG 插图、引导式行文和交互小实验的教学文档，通常发布到 Notion |

## 安装

把仓库克隆下来，再把需要的 skill 链接进 Claude Code 的用户 skill 目录：

```bash
git clone git@github.com:OwenWo0/claude-skills.git ~/claude-skills
ln -s ~/claude-skills/illustrated-explainer ~/.claude/skills/illustrated-explainer
```

用链接而不是复制，以后在仓库里改 skill、`git pull` 更新，Claude Code 都会直接用上新版本。

## 新增一个 skill

1. 新建文件夹，文件夹名就是 skill 名（小写加短横线）。
2. 写 `SKILL.md`，开头的 frontmatter 要有 `name` 和 `description`：description 写清楚「做什么」和「什么时候用」，Claude 靠它判断何时调用。
3. 脚本放 `scripts/`，参考资料放 `references/`，范例和模板放 `assets/`。
4. 在上面的表格里加一行。

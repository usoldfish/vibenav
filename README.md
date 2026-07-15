# 🧭 VibeNav — Vibe Coding 工具导航

仿 Craigslist 的极简纯链接导航:AI 编程 IDE、命令行 Agent、Prompt→App 生成器、MCP 生态、提示词库、发布增长、选品调研等,为独立开发者精选,每条链接悬停可看一句话说明。

**在线访问:https://usoldfish.github.io/vibenav/**

免费基础设施(托管/数据库/支付等)见姊妹项目 [FreeDev 中文版](https://usoldfish.github.io/freefordev/)。

## 维护

- 所有数据在 [`data/links.yaml`](data/links.yaml),每行格式:`名称 | 网址 | 悬停提示`
- 提交后 GitHub Actions 自动构建部署
- 本地预览:`pip install pyyaml && python scripts/build.py`,打开 `dist/index.html`

MIT License

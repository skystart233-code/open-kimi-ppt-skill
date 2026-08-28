# PPTD Studio Skill

[简体中文](README.md) | [English](README_EN.md)

面向 AI Coding Agent 的本地优先演示文稿工具链：用可读、可版本控制的
PPTD v2 项目描述页面，经过浏览器可视化编辑和图片质检，导出仍可在
PowerPoint 或 WPS 中继续修改的 PPTX。

> [!IMPORTANT]
> PPTD Studio Skill 是独立维护的开源项目，不隶属于、不代表、也未获得任何
> 第三方产品厂商的背书。必要的历史来源与第三方软件归属集中记录在
> [PROVENANCE.md](PROVENANCE.md)、[NOTICE](NOTICE) 和许可证文件中。

## 能做什么

- 让 Agent 创建、编辑、复刻和读取 PPTD/PPTX 演示文稿。
- 默认交付完整 PPTD 项目和对应 PPTX，而不是只生成整页图片。
- 在本地浏览器中编辑 PPTD，保存回项目目录并手动导出 PPTX。
- 本地生成 PPTX，支持可编辑文字、形状、图片、图表和幻灯片淡入淡出。
- 将全部页面渲染成图片并拼接总览，供多模态模型做视觉质检。
- 使用内置的通用设计系统参考，或用户原创、自有、已获授权的模板和设计规范。

## 编辑器改动

从 2.0.0 开始，项目不再加载前身项目使用的托管网页编辑器或其静态资源。
编辑、渲染和 PPTX writer 改为内置
[Open-PPTD](https://github.com/Shingwha/open-pptd) 运行时，并固定到可审计的
上游提交。

本项目在上游基础上做了以下集成改动：

1. `pptd-studio-skill serve` 只在 `127.0.0.1` 提供内置编辑器；
2. 命令行 PPTX 导出直接调用本地 OOXML writer，不再驱动浏览器下载；
3. 图片质检使用本地无头渲染器；
4. 补齐页面背景图的预加载、保存、预览和项目打包映射；
5. 对导出的 PPTX 做 ZIP 完整性、页面数量和切换动画结构校验。

### 与旧模板的兼容性

| 内容 | 支持情况 |
| --- | --- |
| PPTD v2 清单、页面、主题和版式 | 支持 |
| 文字、形状、图片、背景图、表格和图表 | 支持 |
| 内置通用设计系统参考 | 支持；不代表任何厂商官方模板 |
| 用户提供且有权使用的 PPTX/PPTD 模板 | 支持 |
| 未识别的 PPTD 字段 | 编辑保存时保留 |
| 幻灯片级淡入淡出 | 支持 |
| 旧版页内元素动画 | 元数据保留，但当前编辑器暂不播放或导出 |

技术兼容不等于获得复制或再分发许可。需要页内动画的项目可以保留相关
PPTD 元数据，但交付时应明确当前 PPTX 只包含静态版式。

### 模板与素材权利策略

内置设计系统参考和历史示例继续保留，因为它们是 Skill 的重要功能与展示材料。
它们来自采用 MIT 许可证的前身项目，但不应被宣传成任何厂商的“官方同款”或
授权模板。示例中的产品图片、Logo、字体和其他第三方素材可能受各自权利约束；
技术可用和仓库可见不等于自动获得独立商用或再分发许可。具体规则见
[主题与模板说明](theme.md)、[示例素材说明](example/NOTICE.md) 和
[RIGHTS_POLICY.md](RIGHTS_POLICY.md)。

## 环境要求

- Node.js 18 或更高版本；
- Python 3，用于导出辅助脚本；
- Chrome 或 Edge，仅在交互编辑和图片渲染时需要；
- Pillow，用于拼接质检总览；缺失时脚本会尝试安装；
- 字体文件不是强制项：可用时嵌入，不可用时由办公软件回退字体。

## 安装

当前版本从 GitHub 安装，尚未承诺新的 npm 包已经发布。不要把文档中的包名
当作 npm 发布状态证明。

```bash
# 非交互安装到 ~/.agents/skills/pptd-studio
npx --yes https://github.com/skystart233-code/pptd-studio-skill/archive/refs/heads/main.tar.gz install -y

# 指定一个或多个 Agent skills 目录
npx --yes https://github.com/skystart233-code/pptd-studio-skill/archive/refs/heads/main.tar.gz install \
  --target ~/.codex/skills \
  --target ~/.claude/skills

# 安装到所有已检测到的 Agent 目录
npx --yes https://github.com/skystart233-code/pptd-studio-skill/archive/refs/heads/main.tar.gz install --all
```

也可以从源码运行：

```bash
git clone https://github.com/skystart233-code/pptd-studio-skill.git
cd pptd-studio-skill
node bin/pptd-studio-skill.js install -y
```

重复执行安装命令会原子更新 `pptd-studio` 目录，不会修改已经生成的文稿。

### 从 1.x 迁移

2.0.0 将 Skill 目录从 `open-kimi-ppt` 改为 `pptd-studio`。安装并验证新版本后，
可以删除旧目录，避免 Agent 同时发现两个功能重叠的 Skill。安装器不会自动
删除旧目录，以免未经确认移除用户文件。

## 快速使用

安装后直接向 Agent 描述内容、页数和风格，例如：

```text
使用 pptd-studio 制作一份 10 页的新品发布 PPT，深色科技风，图片作背景。
同时交付可编辑 PPTD 项目和 PPTX，并在导出前做视觉质检。
```

### 启动本地编辑器

```bash
npx --yes https://github.com/skystart233-code/pptd-studio-skill/archive/refs/heads/main.tar.gz serve --open
```

或在源码目录运行：

```bash
node bin/pptd-studio-skill.js serve --open
```

默认地址为 <http://127.0.0.1:55173/editor/>。在 Chrome/Edge 中选择包含
`.pptd`、`pages/` 和 `media/` 的完整项目目录；文件夹写入权限只在用户主动
授权后获得。

### 直接导出

```bash
python ~/.agents/skills/pptd-studio/scripts/export_pptx.py \
  /path/to/deck.pptd --output /path/to/deck.pptx

python ~/.agents/skills/pptd-studio/scripts/export_images.py \
  /path/to/deck.pptd --output /path/to/qa-images
```

Windows 下可把 `python` 替换为 `py`，并使用 `%USERPROFILE%` 对应的实际路径。

## PPTD 项目结构

```text
deck/
├── deck.pptd
├── pages/
│   ├── 01-cover.page
│   └── 02-content.page
└── media/
    └── hero.jpg
```

PPTD 是基于 YAML 的演示文稿 DSL。完整格式说明见
[PPTD 参考](skills/pptd-studio/reference/pptd.md)，设计系统索引见
[主题列表](theme.md)。

## 本地开发与验证

```bash
npm test
python -m unittest discover -s skills/pptd-studio/tests -p "test_*.py" -v
npm run pack:check
```

渲染器或 writer 的变更还应使用真实多页项目检查总览图和 PPTX ZIP 结构。
贡献约定见 [CONTRIBUTING.md](CONTRIBUTING.md)，安全报告方式见
[SECURITY.md](SECURITY.md)，版本变化见 [CHANGELOG.md](CHANGELOG.md)。

## 安全与隐私

- 默认本地服务只监听 `127.0.0.1`；
- PPTD 解析、编辑和 PPTX 转换在本机执行；
- 文稿主动引用远程图片或字体时，浏览器仍可能访问对应资源地址；
- 外部 PPTD、PPTX、字体和媒体文件均应按不可信输入处理；
- 项目不提供或注入任何第三方服务的登录令牌。

## 开源来源与许可证

PPTD Studio Skill 整体采用 [MIT License](LICENSE)。这是衍生项目，不会删除
原作者的版权声明，也不会把第三方代码宣称为本项目原创。

- 前身项目：[acnlie/open-kimi-ppt-skill](https://github.com/acnlie/open-kimi-ppt-skill)，
  其仓库根许可证为 MIT；本项目仅在来源记录中保留该名称；
- 内置运行时：[Shingwha/open-pptd](https://github.com/Shingwha/open-pptd)，
  固定版本及本地修改见
  [UPSTREAM.md](skills/pptd-studio/vendor/open-pptd/UPSTREAM.md)；
- ECharts、js-yaml、KaTeX、Bootstrap Icons 和 d3 等再分发组件见
  [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) 与 [LICENSES](LICENSES/)；
- 第三方名称与商标仅在说明来源、互操作性或文稿主题确有必要时使用，不表示
  合作、授权或背书；详见 [TRADEMARKS.md](TRADEMARKS.md)。

使用、修改或再分发时，请同时保留 `LICENSE`、`NOTICE`、
`THIRD_PARTY_NOTICES.md`、`PROVENANCE.md` 和 `LICENSES/`。权利人通知流程见
[RIGHTS_POLICY.md](RIGHTS_POLICY.md)。

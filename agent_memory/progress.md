# Task Progress

## Current Goal

- 目标：把 `H:\TVC` 收尾为可上传的 Git 项目，并移除不再使用的 `seedance-video` 项目 skill。
- 成功标准：本地仓库已有初始提交；`.codex/skills/seedance-video/` 从工作区和 Git 跟踪中删除；项目记录说明当前工作流只保留分镜、HTML、首帧图三个职责，并随仓库提供 `aig-image-gen` 支撑首帧实际生图；公开 GitHub 仓库已创建并完成 `main` 推送。
- 范围边界：只处理 Git 打包、Seedance skill 退场和必要项目记录；不改分镜、首帧图、HTML 交付规则。
- 停止条件：Git 状态可解释，删除结果和文档引用通过检索验证。
- 验证方式：`git status --short --branch`、`rg seedance`、目录存在性检查。

## Status

- 当前状态：公开 GitHub 仓库 `https://github.com/xiatianli123-droid/social-video-assistant.git` 已创建并推送完成；本地 `main` 跟踪 `origin/main`；`aig-image-gen` 已复制进项目，等待提交推送。
- 已完成：新增根 `.gitignore`；迁移 `.png/.jpg/.mp4/.mp3/.wav` 到 Git LFS；删除 `.codex/skills/seedance-video/`，包括未跟踪的 `.env.local` 本地密钥文件；更新 `docs/session-summaries.md` 记录该 skill 退场；创建公开 GitHub 远程仓库并推送 `main`；复制 `aig-image-gen` 的 `SKILL.md`、`agents/`、`scripts/` 到 `.codex/skills/aig-image-gen/`，并忽略其运行输出目录。
- 下一步：提交并推送 `aig-image-gen` 项目 skill；协作者 clone 前确认已安装 Git LFS，以便正常拉取图片、视频和音频资产。

## Notes

- 阶段变化：分镜和首帧图交付阶段结束；项目当前目标转为打包、交接和远程发布。
- 当前有效 skill 集合：`short-video-storyboard`、`storyboard-html-delivery`、`storyboard-first-frame-images`、`aig-image-gen`；`aig-image-gen` 随仓库提供脚本，但仍从使用者本机 Codex auth/config 读取凭据。

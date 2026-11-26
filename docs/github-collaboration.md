# vla_learn 小组协作 SOP

SZTU 大三机器人工程课程作业 · [课程仓库](https://github.com/cvv0406/vla_learn) · [下载 PDF](github-collaboration.pdf?raw=1)

下面以小林更新 `README.md` 中的 SO-101 相机说明为例。请把 `xiaolin` 换成自己的 GitHub 用户名，把 `camera-docs` 换成本次任务名。同一项任务始终使用同一个分支。

## 1. 第一次把代码拉到电脑

先安装 [Git](https://git-scm.com/downloads) 和 [Git LFS](https://git-lfs.com/)。Windows 打开 Git Bash，macOS 或 Linux 打开终端，在准备存放项目的目录执行 `git lfs install`。然后按你的情况选择下面一种方式。

**已接受课程仓库的协作者邀请，或者只想下载代码：** 课程仓库已公开，查看和克隆都可以免登录。受邀协作者用接受邀请的账号向课程仓库推送个人分支。

```bash
git clone https://github.com/cvv0406/vla_learn.git
cd vla_learn
```

**想交作业，但没有课程仓库写权限：** 登录 GitHub，在课程仓库首页点 **Fork → Create fork**，保留仓库名 `vla_learn`。从自己的 fork 首页点 **Code → HTTPS** 复制地址，在下面的命令里替换示例地址。这里 `origin` 指自己的 fork，`upstream` 指全组共用的课程仓库。

```bash
git clone https://github.com/xiaolin/vla_learn.git
cd vla_learn
git remote add upstream https://github.com/cvv0406/vla_learn.git
```

已经按第一种方式克隆、后来才创建 fork 的同学，在现有 `vla_learn` 目录运行 `git remote rename origin upstream`，再用 `git remote add origin https://github.com/xiaolin/vla_learn.git` 添加自己的 fork。用 `git remote -v` 核对地址。

## 2. 从最新的 main 创建个人分支

先运行 `git status`，确认手上的修改已经提交，再同步课程仓库。已受邀的协作者执行下面两行；使用 fork 的同学将第二行的 `origin` 换成 `upstream`。

```bash
git switch main
git pull --ff-only origin main
```

每项新作业创建一个分支。最后一行应该打印你的个人分支名。

```bash
git switch -c xiaolin/camera-docs
git branch --show-current
```

## 3. 修改、提交并上传

用编辑器打开要修改的文件，保存后检查差异。下面的 `README.md` 换成你实际改动的路径。改了代码，请先运行与该改动相关的测试。

```bash
git status --short
git diff -- README.md
git add -- README.md
git diff --cached
git commit -m "Document the SO-101 camera setup"
git push -u origin xiaolin/camera-docs
```

`git diff --cached` 会显示本次准备提交的内容，包括新添加的文件。差异占满终端时按 `q` 退出。`commit` 把改动记在本机，`push` 才上传到 GitHub。首次推送按提示登录自己的账号，以后在这个分支直接用 `git push`。

## 4. 发起合并请求，等审核后合入 main

1. 打开[课程仓库的 Pull requests](https://github.com/cvv0406/vla_learn/pulls)，点 **New pull request**。如果首页已显示 **Compare & pull request**，也可以直接点它。
2. 核对方向：**base repository** 是 `cvv0406/vla_learn`，**base** 是 `main`；**compare** 是你的任务分支。使用 fork 的同学点 **compare across forks**，把 **head repository** 选成自己的 fork。
3. 在 **Files changed** 或比较页面的差异中检查文件。填写标题和说明，写清楚“改了什么、怎样验证、结果如何”，点 **Create pull request**。把生成的 PR 链接发给负责审核的同学或仓库负责人。
4. 维护者查看 **Files changed** 和 CI（GitHub 自动运行的检查）。如需修改，在原分支修改、`git add`、`git commit`、`git push`，同一个 PR 会自动更新。CI 出现红叉时，打开失败项的 **Details** 查看原因。
5. 按小组流程，审核完成且相关检查通过后，由有写权限的维护者点 **Merge pull request → Confirm merge**。PR 显示 **Merged** 时，改动已进入课程仓库的 `main`。

**需要负责人先同意吗？** 发起 PR 随时都可以。通过 fork 交作业、只有读取权限的同学，需要负责人或有写权限的协作者代为合并。本指南发布时，`main` 没有强制审批规则，有写权限的协作者可以自行合并。按上面的小组流程，仍应先请另一位成员审核，再合并。

## 5. 下次继续作业

- **上次的 PR 已合并，要做新任务：** 回到第 2 步，更新 `main` 并创建新的任务分支，例如 `xiaolin/calibration-notes`。
- **上次的 PR 还在审核：** 切回原分支。下面示例先同步已经推送的个人分支，再把课程 `main` 的新改动合进来。使用 fork 的同学将第 3、4 行换成 `git fetch upstream` 和 `git merge upstream/main`，最后仍用 `git push` 上传到自己的 fork。

```bash
git switch xiaolin/camera-docs
git pull --ff-only
git fetch origin
git merge origin/main
git push
```

## 常见卡点

- **推送提示 403：** 用 `git remote -v` 核对推送目标。向课程仓库推送需要接受协作者邀请并使用对应账号；走 fork 流程应推向自己的 fork。
- **首次提交提示 Author identity unknown：** 在本仓库设置署名，执行 `git config user.name "Xiaolin"` 和 `git config user.email "your-address@example.com"`，把示例值替换为自己的名字和提交邮箱。
- **提示分支名已存在：** 继续已有任务用 `git switch xiaolin/camera-docs`；新任务换一个分支名。
- **合并时提示 CONFLICT：** 用 `git status` 找到冲突文件，和组员确认要保留的内容，编辑并移除冲突标记，然后运行 `git add -- 文件路径`、`git commit` 和 `git push`。

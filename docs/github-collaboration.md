# vla_learn 小组协作 SOP

SZTU 大三机器人工程课程作业 · [课程仓库](https://github.com/cvv0406/vla_learn) · [下载 PDF](github-collaboration.pdf?raw=1)

第一次用 Git 的同学，从第 0 步开始。只想下载或运行项目，做到第 3 步即可；要交作业，继续做到第 6 步。已经有项目的同学，下次打开电脑从第 7 步开始。

全程用一个小作业举例：小林要给 `README.md` 补一条说明，教组员怎样查看 SO-101 相机工具的用法。请把命令中的 `xiaolin` 换成自己的 GitHub 用户名，把 `camera-docs` 换成本次任务名。真实作业只修改自己负责的文件。

## 0. 准备账号、工具和工作目录

1. **账号。** 只看和下载公开代码可以免登录。要上传或发起合并请求，请注册或登录自己的 [GitHub 账号](https://github.com/)，记下用户名。几位同学一起交作业时，每人用自己的账号。
2. **工具。** 安装 [Git](https://git-scm.com/downloads) 和 [Git LFS](https://git-lfs.com/)。Git 记录每次修改，Git LFS 下载仓库里的大文件。要在本机运行 LeRobot，还需安装 [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install)，只做文档作业可以跳过 Python 环境。
3. **终端。** Windows 从开始菜单打开 **Git Bash**；macOS 打开 **终端（Terminal）**；Linux 从应用菜单打开 **终端**。每次复制代码框中的一行，按回车执行，等到出现下一个输入提示再继续。
4. **检查是否装好。** 运行下面三行。前两行应该显示版本号，第三行通常显示 `Git LFS initialized`。如果系统找不到命令，安装对应工具后重新打开终端。

```bash
git --version
git lfs version
git lfs install
```

在上面三种终端里可以用同一组命令准备目录：

```bash
cd ~
mkdir -p sztu-course
cd sztu-course
pwd
```

`cd` 是进入目录，`~` 表示你的用户目录，`mkdir -p` 会在需要时创建文件夹，`pwd` 显示你现在的位置，`ls` 可以列出文件。记住这个 `sztu-course` 的位置，项目会下载到它里面。

## 1. 第一次把代码拉到电脑

首次下载叫 **clone（克隆）**。人在 `sztu-course` 目录时，按下面两种情况选一条路线。已经有 `vla_learn` 文件夹的同学应进入原文件夹，今后用 **pull（拉取更新）**。

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

**确认已经下载成功。** 运行 `ls` 应该能看到 `README.md`、`pyproject.toml`、`src` 等项目文件。运行 `git remote -v`，受邀协作者应看到 `origin` 指向 `cvv0406/vla_learn`；走 fork 路线应看到 `origin` 指向自己的仓库、`upstream` 指向 `cvv0406/vla_learn`。

## 2. 认识项目并设置提交署名

在编辑器中选 **文件 → 打开文件夹**，选刚克隆的整个 `vla_learn`。根目录的 `README.md` 是仓库首页说明，`src/lerobot/` 放程序，`tests/` 放测试，`docs/` 放文档。浏览文件时，可以同时保留终端窗口执行命令。

要交作业的同学，在 `vla_learn` 的终端里设置一次提交署名。把引号中的示例换成自己的名字和 GitHub 已验证的邮箱；想隐藏个人邮箱，可到 GitHub **Settings → Emails** 复制 GitHub 提供的 `noreply` 邮箱。最后两行应打印你刚填的值。

```bash
git config user.name "Xiaolin"
git config user.email "your-address@example.com"
git config --get user.name
git config --get user.email
```

署名用来标记提交作者。稍后第一次上传时，GitHub 还会核实你登录的账号。

## 3. 配好环境，第一次运行 LeRobot

要运行或修改 Python 代码的同学做这一步。安装依赖时需要联网。第一次练习会生成本机环境报告，并打开相机工具的帮助。普通电脑就能完成，无需显卡或机械臂。

1. **打开能运行 Conda 的终端。** macOS 或 Linux 可用安装 Miniconda 后重新打开的终端。Windows 在开始菜单打开 **Anaconda Prompt (Miniconda3)**，输入 `cd /d "%USERPROFILE%\sztu-course\vla_learn"` 回到项目；若项目放在别处，用自己的实际路径。在这个窗口用 `dir`（Windows）或 `ls`（macOS、Linux）确认能看到 `pyproject.toml`。
2. **首次创建独立环境。** 逐行运行下面的命令。最后的点 `.` 代表当前项目目录，`-e` 表示以后修改本地 Python 源码时，当前环境直接使用修改后的版本。

```bash
conda create -y -n lerobot python=3.10
conda activate lerobot
conda install -y -c conda-forge ffmpeg
python -m pip install -e .
```

**确认正在用课程代码，生成环境报告并打开程序帮助。**

```bash
python --version
python -c "import lerobot; print(lerobot.__file__)"
python -m lerobot.scripts.display_sys_info
lerobot-find-cameras --help
```

第一行应显示 `Python 3.10.x`；第二行应显示你刚克隆目录下的 `src/lerobot/__init__.py`（Windows 使用反斜杠）。第三行生成当前环境的报告，包含 LeRobot、Python 和 PyTorch 版本；没有 GPU 的电脑也可以运行。最后一行会打印 `usage: lerobot-find-cameras` 以及 `--output-dir` 等参数。带上 `--help` 只查看用法，不会打开相机。能看到这些输出，就完成了本次练习的运行验证。

以后重新开终端，只要进入项目目录并运行 `conda activate lerobot` 就可以继续用。实际作业如果需要电机、相机、数据集或训练模型，请按对应作业说明配置设备和依赖。更多环境选项见[本版本安装说明](source/installation.mdx)。

## 4. 从最新的 main 创建个人分支

`main` 保存全组已合并的版本；个人分支保存你这项作业还在做的修改。创建分支后，仍在原来的文件夹里编辑。回到第 0 步使用的终端，确认自己在 `vla_learn` 目录。

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

## 5. 修改文件，保存、提交并上传

**编辑并保存。** 在编辑器左侧打开你负责的文件。比如小林在 `README.md` 中补上一句话：“在已激活的 LeRobot 环境里运行 `lerobot-find-cameras --help`，可以查看相机工具的参数。”按 **Ctrl+S**（macOS 为 **⌘S**）。如果改的是代码，请运行对应作业或测试，记下结果，后面写 PR 时会用到。

**检查你改了什么。** 回到终端运行下面两行。`git status --short` 用 `M` 标记已修改的文件，用 `??` 标记刚创建的文件。`git diff` 会显示已跟踪文件中改动的行；新文件在下一步暂存后就能看到完整内容。

```bash
git status --short
git diff -- README.md
```

**把这次作业提交到本机。** 下面的 `README.md` 换成你实际修改的路径。改了多个文件，可在 `git add --` 后逐个列出，中间用空格隔开。先看清 `git diff --cached` 里面只有本次作业，再执行 `git commit`。看到个人分支名和一串提交编号，说明本地提交成功。差异占满终端时按 `q` 返回。

```bash
git add -- README.md
git diff --cached
git commit -m "Document the SO-101 camera setup"
```

**推送到 GitHub。** 两种路线都运行下面这行；`origin` 会指向你在第 1 步核对过的仓库。首次推送带上 `-u`，以后在这个分支直接运行 `git push` 即可。

```bash
git push -u origin xiaolin/camera-docs
```

如果弹出浏览器登录，请用自己的 GitHub 账号完成授权。若终端反复要求输入密码，可安装 [GitHub CLI](https://cli.github.com/)，运行 `gh auth login --hostname github.com --git-protocol https --web`，按提示在浏览器完成登录，再运行 `gh auth setup-git --hostname github.com` 后重试推送。看到 `[new branch]` 或提交编号范围后，在 GitHub 打开你的推送目标，展开分支菜单，选自己的分支就能看到刚上传的提交。

## 6. 发起合并请求，等审核后合入 main

1. 打开[课程仓库的 Pull requests](https://github.com/cvv0406/vla_learn/pulls)，点 **New pull request**。如果首页已显示 **Compare & pull request**，也可以直接点它。
2. 核对方向：**base repository** 是 `cvv0406/vla_learn`，**base** 是 `main`；**compare** 是你的任务分支。使用 fork 的同学点 **compare across forks**，把 **head repository** 选成自己的 fork。
3. 在比较页面的差异中确认只有自己的本次改动，点 **Create pull request** 填写表单。标题可以写“补充 SO-101 相机工具的使用说明”；说明可以写“在 README 增加查看参数的方法。已运行 `lerobot-find-cameras --help`，能看到 `--output-dir` 参数。”请换成自己的真实改动和验证结果。再点 **Create pull request** 提交，把这个 PR 的页面链接发给负责审核的同学或仓库负责人。
4. 维护者查看 **Files changed** 和 CI（GitHub 自动运行的检查）。如需修改，在原分支修改、`git add`、`git commit`、`git push`，同一个 PR 会自动更新。CI 出现红叉时，打开失败项的 **Details** 查看原因。
5. 按小组流程，审核完成且相关检查通过后，由有写权限的维护者点 **Merge pull request → Confirm merge**。PR 显示 **Merged** 时，改动已进入课程仓库的 `main`。

**需要负责人先同意吗？** 发起 PR 随时都可以。通过 fork 交作业、只有读取权限的同学，需要负责人或有写权限的协作者代为合并。本指南发布时，`main` 没有强制审批规则，有写权限的协作者可以自行合并。按上面的小组流程，仍应先请另一位成员审核，再合并。

## 7. 下次开电脑，接着上次做

打开 Git Bash 或终端，运行 `cd ~/sztu-course/vla_learn`（如果放在别处，请换成实际路径），再运行 `git status` 和 `git branch --show-current` 看清自己在哪个分支。运行 Python 作业时，同样在能使用 Conda 的终端进入该目录、激活环境。

- **上次的 PR 已合并，要做新任务：** 回到第 4 步，更新 `main` 并创建新的任务分支，例如 `xiaolin/calibration-notes`。想确认合并结果，更新本地 `main` 后用编辑器打开作业文件，就能看到组员和自己的改动。
- **上次的 PR 还在审核：** 切回原分支。下面示例先同步已经推送的个人分支，再把课程 `main` 的新改动合进来。使用 fork 的同学将第 3、4 行换成 `git fetch upstream` 和 `git merge upstream/main`，最后仍用 `git push` 上传到自己的 fork。

```bash
git switch xiaolin/camera-docs
git pull --ff-only
git fetch origin
git merge origin/main
git push
```

## 常见卡点

- **终端提示 not a git repository 或找不到 pyproject.toml：** 用 `pwd`（Windows Prompt 用 `cd`）看当前位置，进入包含 `README.md`、`src` 和 `pyproject.toml` 的项目根目录再运行命令。
- **conda 或 lerobot-find-cameras 找不到：** Windows 使用安装 Miniconda 时创建的 Prompt；macOS、Linux 重开终端后检查 `conda --version`。能运行 Conda 后，先 `conda activate lerobot`，再回到项目根目录确认已成功执行 `python -m pip install -e .`。
- **git status 显示 nothing to commit：** 核对编辑器打开的文件夹和刚执行 `pwd` 看到的是同一个，检查文件是否已经保存。如果已经提交过，可以用 `git log -1 --oneline` 查看最近的提交，再推送。
- **推送提示 403：** 用 `git remote -v` 核对推送目标。向课程仓库推送需要接受协作者邀请并使用对应账号；走 fork 流程应推向自己的 fork。
- **push 提示 non-fast-forward：** 确认处在自己的任务分支，并已提交手上的改动。运行 `git fetch origin`，再运行 `git merge origin/xiaolin/camera-docs`（换成自己的分支名），处理冲突后重新 `git push`。
- **首次提交提示 Author identity unknown：** 在本仓库设置署名，执行 `git config user.name "Xiaolin"` 和 `git config user.email "your-address@example.com"`，把示例值替换为自己的名字和提交邮箱。
- **提示分支名已存在：** 继续已有任务用 `git switch xiaolin/camera-docs`；新任务换一个分支名。
- **合并时提示 CONFLICT：** 用 `git status` 找到冲突文件，和组员确认要保留的内容，编辑并移除冲突标记，然后运行 `git add -- 文件路径`、`git commit` 和 `git push`。

需要同学帮忙排错时，附上你在哪一步、刚执行的命令、完整报错和 `git status` 的输出。账户密码或令牌只在自己的登录窗口使用。

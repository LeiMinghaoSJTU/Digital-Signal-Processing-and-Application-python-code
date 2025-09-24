#### 1. 检查本地分支和提交记录
首先确认本地是否有提交，以及当前所在的分支名称：
```bash
# 查看本地提交记录（若没有任何记录，会提示 "nothing to commit"）
git log

# 查看本地所有分支（当前分支前会有 * 标记）
git branch
```

- **如果没有任何提交记录**：先创建至少一次提交（否则无内容可推送）
  ```bash
  git add .  # 添加所有文件
  git commit -m "首次提交：添加项目文件"  # 创建提交
  ```

- **如果本地分支不是 `main`**：比如本地分支是 `master`（旧版本 Git 默认分支名），或其他名称


#### 2. 推送时指定正确的分支名称
如果本地分支是 `master`，而远程仓库默认分支是 `main`（GitHub 新建仓库默认分支为 `main`），直接推送时需要明确指定分支对应关系：
```bash
# 推送本地 master 分支到远程 main 分支（并建立关联）
git push -u origin master:main
```

#### 3. （推荐）将本地分支重命名为 `main`（与远程保持一致）
如果希望本地分支名与远程 `main` 统一，可重命名本地分支：
```bash
# 若当前在 master 分支，将其重命名为 main
git branch -M main

# 再推送（此时分支名匹配，直接推送即可）
git push -u origin main
```


### 关键原理说明：
- `src refspec main does not match any` 表示：Git 在本地找不到 `main` 分支的引用（可能分支名不同，或无提交）。
- 远程仓库默认分支是 `main`，但本地可能还是旧的 `master` 分支（Git 2.28+ 版本默认分支已改为 `main`，但旧版本仍可能是 `master`）。
- 通过 `本地分支:远程分支` 的格式（如 `master:main`），可以强制指定推送的对应关系，无需修改本地分支名。

按以上步骤操作后，即可解决分支名称不匹配导致的推送失败问题。
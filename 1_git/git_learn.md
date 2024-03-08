# git learn
## 1 安装入门
### 1.1 
1.1.1 创建版本库
~~~ sh
# 创建repository
$ mkdir learngit
$ cd learngit
# pwd命令用于显示当前目录
$ pwd
/Users/michael/learngit
# git init命令把这个目录变成Git可以管理的仓库：
# ls -ah 显示隐藏目录
$ git init
Initialized empty Git repository in /Users/michael/learngit/.git/
# liwei@Lewiea MINGW64 ~/learnGit (master)
$ git add readme.txt

# liwei@Lewiea MINGW64 ~/learnGit (master)
$ git commit -m“wrote a readme file”
error: pathspec 'a' did not match any file(s) known to git
error: pathspec 'readme' did not match any file(s) known to git
error: pathspec 'file”' did not match any file(s) known to git

# liwei@Lewiea MINGW64 ~/learnGit (master)
$ git commit -m “wrote a readme file”
error: pathspec 'a' did not match any file(s) known to git
error: pathspec 'readme' did not match any file(s) known to git
error: pathspec 'file”' did not match any file(s) known to git

# liwei@Lewiea MINGW64 ~/learnGit (master)
$ git commit -m "wrote a readme file"
On branch master
nothing to commit, working tree clean

# liwei@Lewiea MINGW64 ~/learnGit (master)
$ ls
readme.txt

$ dir
readme.txt
~~~

1.1.2 提交
~~~ sh
# 要随时掌握工作区的状态，使用git status命令。

# 如果git status告诉你有文件被修改过，用git diff可以查看修改内容。
# liwei@Lewiea MINGW64 ~/learnGit (master)
$ git status
On branch master
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   readme.txt

no changes added to commit (use "git add" and/or "git commit -a")

# liwei@Lewiea MINGW64 ~/learnGit (master)
$ git diff
diff --git a/readme.txt b/readme.txt
index d8036c1..389d963 100644
--- a/readme.txt
+++ b/readme.txt
@@ -1,2 +1,2 @@
-Git is a version control system.
+Git is a distribusion version control system.
 Git is free software.
\ No newline at end of file

# liwei@Lewiea MINGW64 ~/learnGit (master)
$ git add readme.txt

# liwei@Lewiea MINGW64 ~/learnGit (master)
$ git status
On branch master
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   readme.txt


# liwei@Lewiea MINGW64 ~/learnGit (master)
$ git commit -m "add distributed"
[master 66211de] add distributed
 1 file changed, 1 insertion(+), 1 deletion(-)

# liwei@Lewiea MINGW64 ~/learnGit (master)
$ git status
On branch master
nothing to commit, working tree clean

# liwei@Lewiea MINGW64 ~/learnGit (master)
$ git log
commit e7502c09c0977a4a69416fb7b4add5d3f1b6035d (HEAD -> master)
Author: Heliwei <holewiea@gmail.com>
Date:   Fri Nov 12 14:27:09 2021 +0800

    append GPL

commit 66211de120f854d8a1d4ff49c2e430e46250b17c
Author: Heliwei <holewiea@gmail.com>
Date:   Fri Nov 12 14:14:13 2021 +0800

    add distributed

commit 47cb22b10726c7684449015d9bf91cd763ba3f56
Author: lewiea-Ho <holewiea@gmail.com>
Date:   Tue Nov 5 22:29:41 2019 +0000

    wrote a readme file

# liwei@Lewiea MINGW64 ~/learnGit (master)
$ git log --pretty=oneline
e7502c09c0977a4a69416fb7b4add5d3f1b6035d (HEAD -> master) append GPL
66211de120f854d8a1d4ff49c2e430e46250b17c add distributed
47cb22b10726c7684449015d9bf91cd763ba3f56 wrote a readme file

# 用HEAD表示当前版本，也就是最新的提交1094adb...（注意我的提交ID和你的肯定不一样），上一个版本就是HEAD^，上上一个版本就是HEAD^^，当然往上100个版本写100个^比较容易数不过来，所以写成HEAD~100。

# liwei@Lewiea MINGW64 ~/learnGit (master)
$ git reset --hard HEAD^
HEAD is now at 66211de add distributed

# liwei@Lewiea MINGW64 ~/learnGit (master)
$ cat readme.txt
Git is a distribusion version control system.
Git is free software.
# liwei@Lewiea MINGW64 ~/learnGit (master)
$ git log
commit 66211de120f854d8a1d4ff49c2e430e46250b17c (HEAD -> master)
Author: Heliwei <holewiea@gmail.com>
Date:   Fri Nov 12 14:14:13 2021 +0800

    add distributed

commit 47cb22b10726c7684449015d9bf91cd763ba3f56
Author: lewiea-Ho <holewiea@gmail.com>
Date:   Tue Nov 5 22:29:41 2019 +0000

    wrote a readme file

# 第一种 记录commit id数值
# liwei@Lewiea MINGW64 ~/learnGit (master)
$ git reset --hard e7502c
HEAD is now at e7502c0 append GPL

# liwei@Lewiea MINGW64 ~/learnGit (master)
$ cat readme.txt
Git is a distribusion version control system.
Git is free software distributed under the GPL.

# 第二种：Git提供了一个命令git reflog用来记录你的每一次命令
$ git reflog
e7502c0 (HEAD -> master) HEAD@{0}: reset: moving to e7502c
66211de HEAD@{1}: reset: moving to HEAD^
e7502c0 (HEAD -> master) HEAD@{2}: commit: append GPL
66211de HEAD@{3}: commit: add distributed
47cb22b HEAD@{4}: commit (initial): wrote a readme file

~~~
1.1.3 工作区和暂存区
工作区：.git目录
![picture 1](images/62b6cfabc537dc19b8400e148be61c85427071358e082e48953ebaa095a9cdb0.png)  

1 未添加过文件：untracked
~~~ sh
#liwei@Lewiea MINGW64 ~/learnGit (master)
$ git diff HEAD -- readme,txt

#liwei@Lewiea MINGW64 ~/learnGit (master)
$ git diff HEAD -- readme.txt
diff --git a/readme.txt b/readme.txt
index 241433e..06c1e1d 100644
--- a/readme.txt
+++ b/readme.txt
@@ -1,3 +1,3 @@
 Git is a distribusion version control system.
 Git is free software distributed under the GPL.
-Git tracks change.
\ No newline at end of file
+Git tracks change of files.
\ No newline at end of file
~~~
2 撤销修改
~~~sh
# 工作区文件回到最近一次git commit或git add时的状态。
$ git checkout -- readme.txt
# 注意与checkout 区分

# 暂存区 命令git reset HEAD <file>可以把暂存区的修改撤销掉（unstage），重新放回工作区：
$ git reset HEAD readme.txt
Unstaged changes after reset:
M	readme.txt
# git reset命令既可以回退版本，也可以把暂存区的修改回退到工作区。当我们用HEAD时，表示最新的版本。
#版本库 用
$ git reset --hard e7502c
$ git reset --hard HEAD^
~~~

3 删除文件
~~~ bash
$ rm test.txt
$ git status
On branch master
Changes not staged for commit:
  (use "git add/rm <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

	deleted:    test.txt

no changes added to commit (use "git add" and/or "git commit -a")
# 确实要从版本库中删除该文件，那就用命令git rm删掉，并且git commit：
$ git rm test.txt
rm 'test.txt'

$ git commit -m "remove test.txt"
[master d46f35e] remove test.txt
 1 file changed, 1 deletion(-)
 delete mode 100644 test.txt

# 删错了
$ git checkout -- test.txt
~~~

### 1.2 远程仓库
1.2.1 创建远程仓库
~~~ SH
$ ssh-keygen -t rsa -C "youremail@example.com"
# 可以在用户主目录里找到.ssh目录，里面有id_rsa和id_rsa.pub两个文件，这两个就是SSH Key的秘钥对，id_rsa是私钥，不能泄露出去，id_rsa.pub是公钥，可以放心地告诉任何人。

#登陆GitHub，打开“Account settings”，“SSH Keys”页面：然后，点“Add SSH Key”，填上任意Title，在Key文本框里粘贴id_rsa.pub文件的内容：

# liwei@Lewiea MINGW64 ~/learnGit (master)
$ git remote add origin git@github.com:hlewiea/learngit.git

# liwei@Lewiea MINGW64 ~/learnGit (master)
# 加上了-u参数，Git不但会把本地的master分支内容推送的远程新的master分支，还会把本地的master分支和远程的master分支关联起来，在以后的推送或者拉取时就可以简化命令。
$ git push -u origin master
$ Enumerating objects: 12, done.
Writing objects: 100% (12/12), 998 bytes | 499.00 KiB/s, done.
Total 12 (delta 2), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (2/2), done.
remote:
remote: Create a pull request for 'master' on GitHub by visiting:
remote:      https://github.com/hlewiea/learngit/pull/new/master
remote:
To github.com:hlewiea/learngit.git
 * [new branch]      master -> master
Branch 'master' set up to track remote branch 'master' from 'origin'.
bash: Enumerating: command not found

#只要本地作了提交，就可以通过命令：

$ git push origin master

# 删除远程库可以用git remote rm <name>命令。使用前，建议先用git remote -v查看远程库信息：
$ git remote -v
origin  git@github.com:michaelliao/learn-git.git (fetch)
origin  git@github.com:michaelliao/learn-git.git (push)
# 然后，根据名字删除，比如删除origin：
$ git remote rm origin
# 此处的“删除”其实是解除了本地和远程的绑定关系，并不是物理上删除了远程库。

$ git clone
# 还可以用https://github.com/michaelliao/gitskills.git这样的地址。实际上，Git支持多种协议，默认的git://使用ssh，但也可以使用https等其他协议。使用https除了速度慢以外，还有个最大的麻烦是每次推送都必须输入口令，但是在某些只开放http端口的公司内部就无法使用ssh协议而只能用https。
~~~

### 1.3 分支和标签管理
#### 1.3.1 创建与合并分支
一开始的时候，master分支是一条线，Git用master指向最新的提交，再用HEAD指向master，就能确定当前分支，以及当前分支的提交点：
![picture 2](images/5cd3089e8ce289cd2babb6ec5558b57d20ead59c575075d02dd37edae0ad0628.png)  
每次提交，master分支都会向前移动一步，这样，随着你不断提交，master分支的线也越来越长。

当我们创建新的分支，例如dev时，Git新建了一个指针叫dev，指向master相同的提交，再把HEAD指向dev，就表示当前分支在dev上：
![picture 3](images/571fafd8280fb3da2dfdf1acaab17de13990e404545d26b0b815db398b24441b.png)  
~~~ sh
$ git checkout -b dev
# Switched to a new branch 'dev'
# git checkout命令加上-b参数表示创建并切换:L
$ git branch dev
$ git checkout dev
Switched to branch 'dev'
# 后，用git branch命令查看当前分支,当前分支前面会标一个*号：
$ git branch
* dev
  master

~~~
不过，从现在开始，对工作区的修改和提交就是针对dev分支了，比如新提交一次后，dev指针往前移动一步，而master指针不变：
~~~sh
$ git add readme.txt 
$ git commit -m "branch test"
[dev b17d20e] branch test
 1 file changed, 1 insertion(+)
~~~
![picture 4](images/3a7fc2b8384b573a7d02aea9e058cf6ffbb2b1ebfd5bd7d9ed1af115e3dc53e4.png)  
假如我们在dev上的工作完成了，就可以把dev合并到master上。Git怎么合并呢？最简单的方法，就是直接把master指向dev的当前提交，就完成了合并：
~~~sh
$ git checkout master
Switched to branch 'master'
# 合并指定分支到当前分支
$ git merge dev
Updating d46f35e..b17d20e
# Fast-forward信息，Git告诉我们，这次合并是“快进模式”，也就是直接把master指向dev的当前提交，所以合并速度非常快。
# 也不是每次合并都能Fast-forward，我们后面会讲其他方式的合并。
Fast-forward
 readme.txt | 1 +
 1 file changed, 1 insertion(+)
~~~
![picture 6](images/16a6224756ce8431c7fec4637292af71b8cc516ae9158ce1f620f58cf6007d71.png)  

~~~sh
#合并完成后，就可以放心地删除dev分支了：

$ git branch -d dev
Deleted branch dev (was b17d20e).
#删除后，查看branch，就只剩下master分支了：

$ git branch
* master
~~~

最新git提供git switch
~~~ sh
# 创建并切换到新的dev分支，可以使用：
$ git switch -c dev
# 直接切换到已有的master分支，可以使用：
$ git switch master
~~~

#### 1.3.2 conflit
创建新feature分支并提交
~~~ sh
$ git switch -c feature1
修改文件
$ git add readme.txt
$ git commit -m "AND simple"
# 切换回master
$ git switch master
Switched to branch 'master'
Your branch is ahead of 'origin/master' by 1 commit.
  (use "git push" to publish your local commits)

master分支上做修改并commit
~~~
![picture 7](images/e4694efc03e86b9fb941f85983583d78263de5c71f19fedc9acf17795504820c.png)  

此时无法快速合并
~~~sh
$ git merge feature1
Auto-merging readme.txt
CONFLICT (content): Merge conflict in readme.txt
Automatic merge failed; fix conflicts and then commit the result.
~~~
也可以status查看
~~~ sh
$ git status
On branch master
Your branch is ahead of 'origin/master' by 2 commits.
  (use "git push" to publish your local commits)

You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)

	both modified:   readme.txt

no changes added to commit (use "git add" and/or "git commit -a")
~~~
Git用<<<<<<<，=======，>>>>>>>标记出不同分支的内容,修改后合并
![picture 8](images/06d34c8e3c7f916d3add7e0fbcc00e40a6583d7c730ff7fdc02325c184e86635.png)  
~~~ sh
$ git log --graph --pretty=oneline --abbrev-commit
*   cf810e4 (HEAD -> master) conflict fixed
|\  
| * 14096d0 (feature1) AND simple
* | 5dc6824 & simple
|/  
* b17d20e branch test
* d46f35e (origin/master) remove test.txt
* b84166e add test.txt
* 519219b git tracks changes
* e43a48b understand how stage works
* 1094adb append GPL
* e475afc add distributed
* eaadf4e wrote a readme file

$ git branch -d feature1
Deleted branch feature1 (was 14096d0).
~~~
#### 1.3.3 分支管理
~~~sh
# 准备合并dev分支，请注意--no-ff参数，表示禁用Fast forward：

$ git merge --no-ff -m "merge with no-ff" dev
Merge made by the 'recursive' strategy.
 readme.txt | 1 +
 1 file changed, 1 insertion(+)
~~~
![picture 9](images/8631e3a0acd6ab11c57aee843a82d1b286d57886bcf530418876b4fe81877ce7.png)  

在实际开发中，我们应该按照几个基本原则进行分支管理：

首先，master分支应该是非常稳定的，也就是仅用来发布新版本，平时不能在上面干活；

那在哪干活呢？干活都在dev分支上，也就是说，dev分支是不稳定的，到某个时候，比如1.0版本发布时，再把dev分支合并到master上，在master分支发布1.0版本；你和你的小伙伴们每个人都在dev分支上干活，每个人都有自己的分支，时不时地往dev分支上合并就可以了。

#### 1.3.4 bug分支
~~~sh
$ git stash
Saved working directory and index state WIP on dev: f52c633 add merge
# 用git status查看工作区，就是干净的（除非有没有被Git管理的文件）首先确定要在哪个分支上修复bug，假定需要在master分支上修复，就从master创建临时分支：
$ git checkout master
Switched to branch 'master'
Your branch is ahead of 'origin/master' by 6 commits.
  (use "git push" to publish your local commits)

$ git checkout -b issue-101
Switched to a new branch 'issue-101'
修复提交后切换回master并合并，最后删除issue分支
切换回dev分支
$ git switch dev
Switched to branch 'dev'

$ git status list
stash@{0}: WIP on dev: f52c633 add merge

#恢复1：git stash apply恢复，但是恢复后，stash内容并不删除，你需要用git stash drop来删除；
#恢复2：git stash pop
$ git stash apply stash@{0}
$ git stash pop
~~~

cherry-pick：复制之前4c805e2 fix bug 101这个提交所做的修改到当前分支
~~~sh
$ git branch
* dev
  master
$ git cherry-pick 4c805e2
[master 1d4b803] fix bug 101
 1 file changed, 1 insertion(+), 1 deletion(-)
~~~

#### 1.3.5 feature分支
~~~sh
$ git switch -c feature-vulcan
$ git add vulcan.py

$ git status
On branch feature-vulcan
Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

	new file:   vulcan.py

$ git commit -m "add feature vulcan"
[feature-vulcan 287773e] add feature vulcan
 1 file changed, 2 insertions(+)
 create mode 100644 vulcan.p
Switched to a new branch 'feature-vulcan'
# 切回dev，准备合并：
$ git switch dev
# 或者销毁分支
$ git branch -d feature-vulcan
error: The branch 'feature-vulcan' is not fully merged.
If you are sure you want to delete it, run 'git branch -D feature-vulcan'.
~~~

#### 1.3.6 远程分支
~~~sh
$ git remote
origin
#或者，用git remote -v显示更详细的信息：
#如果没有推送权限，就看不到push的地址。
$ git remote -v
origin  git@github.com:michaelliao/learngit.git (fetch)
origin  git@github.com:michaelliao/learngit.git (push)
~~~
推送
~~~sh
$ git push origin master
如果要推送其他分支，比如dev，就改成：
$ git push origin dev
~~~
抓取
~~~sh
# 创建远程origin的dev分支到本地，于是他用这个命令创建本地dev分支：
$ git checkout -b dev origin/dev
#现在，他就可以在dev上继续修改，然后，时不时地把dev分支push到远程：
$ git push origin dev
# 当另一个人提交和本次冲突时，提交失败
# Git已经提示我们，先用git pull把最新的提交从origin/dev抓下来，然后，在本地合并，解决冲突，再推送：
$ git pull
There is no tracking information for the current branch.
Please specify which branch you want to merge with.
See git-pull(1) for details.

    git pull <remote> <branch>

If you wish to set tracking information for this branch you can do so with:

    git branch --set-upstream-to=origin/<branch> dev
# git pull也失败了，原因是没有指定本地dev分支与远程origin/dev分支的链接，根据提示，设置dev和origin/dev的链接：
$ git branch --set-upstream-to=origin/dev dev
$ git pull
Auto-merging env.txt
CONFLICT (add/add): Merge conflict in env.txt
Automatic merge failed; fix conflicts and then commit the result.
~~~
#### 1.3.7 rebase
rebase操作可以把本地未push的分叉提交历史整理成直线；rebase的目的是使得我们在查看历史提交的变化时更容易，因为分叉的提交需要三方对比。

Git把我们本地的提交“挪动”了位置，放到了f005ed4 (origin/master) set exit=1之后，这样，整个提交历史就成了一条直线。rebase操作前后，最终的提交内容是一致的，但是，我们本地的commit修改内容已经变化了，它们的修改不再基于d1be385 init hello，而是基于f005ed4 (origin/master) set exit=1，但最后的提交7e61ed4内容是一致的。

这就是rebase操作的特点：把分叉的提交历史“整理”成一条直线，看上去更直观。缺点是本地的分叉提交已经被修改过了。

### 1.4 tag
~~~sh
$ git tag v1.0
# 命令git tag查看所有标签：
$ git tag
v1.0
#
$ git log --pretty=oneline --abbrev-commit
12a631b (HEAD -> master, tag: v1.0, origin/master) merged bug fix 101
4c805e2 fix bug 101
e1e9c68 merge with no-ff
f52c633 add merge
cf810e4 conflict fixed
5dc6824 & simple
14096d0 AND simple
b17d20e branch test
d46f35e remove test.txt
b84166e add test.txt
519219b git tracks changes
e43a48b understand how stage works
1094adb append GPL
e475afc add distributed
eaadf4e wrote a readme file
# 比方说要对add merge这次提交打标签，它对应的commit id是f52c633，敲入命令：
$ git tag v0.9 f52c633
$ git tag
v0.9
v1.0
# 标签不是按时间顺序列出，而是按字母排序的。可以用git show <tagname>查看标签信息：
$ git show v0.9
commit f52c63349bc3c1593499807e5c8e972b82c8f286 (tag: v0.9)
Author: Michael Liao <askxuefeng@gmail.com>
Date:   Fri May 18 21:56:54 2018 +0800

    add merge

diff --git a/readme.txt b/readme.txt
...
# 创建带有说明的标签，用-a指定标签名，-m指定说明文字：
$ git tag -a v0.1 -m "version 0.1 released" 1094adb
# 命令git show <tagname>可以看到说明文字：

$ git show v0.1
tag v0.1
Tagger: Michael Liao <askxuefeng@gmail.com>
Date:   Fri May 18 22:48:43 2018 +0800

version 0.1 released

commit 1094adb7b9b3807259d8cb349e7df1d4d6477073 (tag: v0.1)
Author: Michael Liao <askxuefeng@gmail.com>
Date:   Fri May 18 21:06:15 2018 +0800

    append GPL

diff --git a/readme.txt b/readme.txt
...
~~~
标签删除
~~~sh
$ git tag -d v0.1
Deleted tag 'v0.1' (was f15b0dd)
# 创建的标签都只存储在本地，不会自动推送到远程。所以，打错的标签可以在本地安全删除。

#如果要推送某个标签到远程，使用命令git push origin <tagname>：

$ git push origin v1.0
Total 0 (delta 0), reused 0 (delta 0)
To github.com:michaelliao/learngit.git
 * [new tag]         v1.0 -> v1.0
# 或者，一次性推送全部尚未推送到远程的本地标签：

$ git push origin --tags
Total 0 (delta 0), reused 0 (delta 0)
To github.com:michaelliao/learngit.git
 * [new tag]         v0.9 -> v0.9
# 如果标签已经推送到远程，要删除远程标签就麻烦一点，先从本地删除：

$ git tag -d v0.9
Deleted tag 'v0.9' (was f52c633)
# 然后，从远程删除。删除命令也是push，但是格式如下：

$ git push origin :refs/tags/v0.9
To github.com:michaelliao/learngit.git
 - [deleted]         v0.9

~~~
### 1.5 常用命令
git log
![picture 10](images/4ed41e6788d498ba6dade2aa4f9e86dbfc0e136db3d91f8f230a44fdd4211ebd.png)  

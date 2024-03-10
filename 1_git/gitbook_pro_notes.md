
# GIT

参照学习链接：<https://csdiy.wiki/%E5%BF%85%E5%AD%A6%E5%B7%A5%E5%85%B7/Git/#git_1>1

## 1. 分支 - git 数据结构

commit
blob
tree
parent

HEAD

你可以简单地使用 git log 命令查看各个分支当前所指的对象。 提供这一功能的参数是 --decorate。

git rebase --onto master server client
以上命令的意思是：“取出 client 分支，找出它从 server 分支分歧之后的补丁，
 然后把这些补丁在 master 分支上重放一遍，让 client 看起来像直接基于 master 修改一样”。这理解起来有一点复杂，不过效果非常酷。
rebase的风险，rebase后请不要再基于，rebase前的原有分支开发

## 2. 协议

git clone 借助的文件传输协议

- NFS，共享文件系统文件传输
- http： dumb（ web 服务器仅把裸版本库当作普通文件来对待，提供文件服务） -> intellect （只是运行在标准的 HTTP/S 端口上并且可以使用各种 HTTP 验证机制）
- ssh：SSH 访问是安全的 —— 所有传输数据都要经过授权和加密
- git: git守护进程，要求防火墙开放 9418 端口， 使用与 SSH 相同的数据传输机制，但是省去了加密和授权的开销，缺乏授权机制

## 3. 分布式git



## x.原理

HEAD 文件、（尚待创建的）index 文件，和 objects 目录、refs 目录。 它们都是 Git 的核心组成部分。

~~~bash
@hlewiea ➜ /workspaces/hlewiea.github.io/.git (br_240309_git) $ ls -F1
COMMIT_EDITMSG
FETCH_HEAD
HEAD # HEAD 文件指向目前被检出的分支
ORIG_HEAD
branches/
config # config 文件包含项目特有的配置选项
description # 文件仅供 GitWeb 程序使用，我们无需关心。
hooks/ # hooks 目录包含客户端或服务端的钩子脚本（hook scripts）
index # index 文件保存暂存区信息
info/ # info 目录包含一个全局性排除（global exclude）文件， 用以放置那些不希望被记录在 .gitignore 文件中的忽略模式（ignored patterns）
lfs/
logs/
objects/ # objects 目录存储所有数据内容
packed-refs
refs/ # refs 目录存储指向数据（分支、远程仓库和标签等）的提交对象的指针；
~~~

### 1 object

写入object

~~~bash
/workspaces/hlewiea.github.io/.git/objects (br_240309_git) $ ls
0a  0c  12  24  25  36  37  3e  43  49  50  52  55  5b  61  6d  72  82  86  8f  96  97  
9b  9f  a3  a4  b4  c0  c1  c2  cd  ce  d2  d4  d5  da  e0  e6  f9  fb  fe  info  pack
# 写入当前文件内容到git object
@hlewiea ➜ /workspaces/hlewiea.github.io/.git/objects (br_240309_git) $ cat ../../1_git/readme.md  | git hash-object -w --stdin
18508923b3be1dcef7752d24e9b1bcd0f0d84043
@hlewiea ➜ /workspaces/hlewiea.github.io/.git/objects (br_240309_git) $ ls 18
508923b3be1dcef7752d24e9b1bcd0f0d84043
# 读取写入时的内容，非实时同步，仅仅写入时的状态
@hlewiea ➜ /workspaces/hlewiea.github.io/.git/objects (br_240309_git) $ git cat-file -p 185089
# 当前文件内容
# 若是cat的是tree对象，则会展开显示树对象下的所有blob文件
~~~

~~~bash
# 查分支上最新的提交所指向的树对象
git cat-file -p br_240309_git^{tree}
@hlewiea ➜ /workspaces/hlewiea.github.io (br_240309_git) $ cat test.txt | git hash-object -w --stdin
a5bce3fd2565d8f458555a0c6f42d0504a848bd5
# 创建staged对象， 指定文件模式、SHA-1 与文件名
@hlewiea ➜ /workspaces/hlewiea.github.io (br_240309_git) $ git update-index --add --cacheinfo 100644 a5bce3fd2565d8f458555a0c6f42d0504a848bd5 test.txt
# 将暂存区内容写入一个树对象
@hlewiea ➜ /workspaces/hlewiea.github.io (br_240309_git) $ git write-tree
ad787346437376a1444aeea7dcaf2fec2fe049ba
@hlewiea ➜ /workspaces/hlewiea.github.io (br_240309_git) $ git cat-file -p ad787
040000 tree 37170242381020f135aa8b4b924b194bf3c1cb67    .vscode
#...
100644 blob a5bce3fd2565d8f458555a0c6f42d0504a848bd5    test.txt
#通过对该命令指定 --prefix 选项，将一个已有的树对象作为子树读入暂存区：
$ git read-tree --prefix=bak ad787346437376a1444aeea7dcaf2fec2fe049ba
# 提交(head/子节点)
echo 'first commit' | git commit-tree d8329f
fdf4fc3344e67ab068f836878b6c4951e3b15f3d
echo 'second commit' | git commit-tree 0155eb -p fdf4fc3
# sha1
 => "blob 16\u0000what is up, doc?" 
3.2.3 :004 > require 'digest/sha1'
 => true 
3.2.3 :005 > ha1 = Digest::SHA1.hexdigest(store)
 => "bd9dbf5aae1a3862dd1526723246b20206e5fc37" 
3.2.3 :006 > exit
@hlewiea ➜ /workspaces/hlewiea.github.io (br_240309_git) $ echo -n "what is up, doc?" | git hash-object --stdin
bd9dbf5aae1a3862dd1526723246b20206e5fc37
@hlewiea ➜ /workspaces/hlewiea.github.io (br_240309_git) $ 
~~~

### 2 ref

~~~bash
refs (br_240309_git) $ ls
heads  remotes  tags
refs (br_240309_git) $ cat ./heads/br_240309_git
b13b38ec7238dfc376a37f8f31507471cadf57cb
# 切节点
git update-ref refs/heads/master 1a410efbd13591db07496601ebc7a059dd55cfe9
refs (br_240309_git) $ cat ./remotes/origin/HEAD 
ref: refs/remotes/origin/main
$ cat ../HEAD 
ref: refs/heads/br_240309_git
# 设置head值
$ git symbolic-ref HEAD
$ git symbolic-ref HEAD refs/heads/test
~~~

### 3.包文件

~~~bash
# 打包所有的object
git gc
(br_240309_git) $ ll .git/objects/pack/
pack-253332f996d066396d91b9314877bb1dabf67c95.idx
pack-253332f996d066396d91b9314877bb1dabf67c95.pack
pack-253332f996d066396d91b9314877bb1dabf67c95.rev
pack-ee6eee918f6c8cfcdf4eb6f4f3654bdecf2b12f7.idx
pack-ee6eee918f6c8cfcdf4eb6f4f3654bdecf2b12f7.mtimes
pack-ee6eee918f6c8cfcdf4eb6f4f3654bdecf2b12f7.pack
pack-ee6eee918f6c8cfcdf4eb6f4f3654bdecf2b12f7.rev
$ git verify-pack -v .git/objects/pack/pack-253332f996d066396d91b9314877bb1dabf67c95.idx
b042a60ef7dff760008df33cee372b945b6e884e blob   22054 5799 510600
033b4468fa6b2a9547a70d88d1bbe8bf3f9ed0d5 blob   9 20 517988 1 033b4468fa6b2a9547a70d88d1bbe8bf3f9ed0d5 blob   9 20 517988 1 
# b042a 占用了 22K 空间，而 033b4 仅占用 9 字节。 同样有趣的地方在于，第二个版本完整保存了文件内容，而原始的版本反而是以差异方式保存的——这是因为大部分情况下需要快速访问文件的最新版本。
~~~

### 4. 引用规范


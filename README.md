# legemara

代码面条，结构混乱，性能低下，文档残缺，功能阉割，配置复杂

## env

- 基于 win10 x64

- 使用 uv 管理 python 环境
- 使用 adb 操作模拟器，需要安装 Google 的 platform-tools
  - https://developer.android.com/studio/releases/platform-tools
  - https://dl.google.com/android/repository/platform-tools-latest-windows.zip 这个可以直接下，下完把 platform-tools 丢进 PATH 里就行，轮椅教程 https://zhuanlan.zhihu.com/p/140828682

- 需要将 airtest 的 minitouch push 到 adb 并赋予执行权限，否则会有报警

## boot

- 通过 uv 安装依赖

```powershell
# 如果没有安装 uv
pip install uv
uv self update

# 同步环境
uv venv  # 创建虚拟环境
uv sync  # 同步依赖到 .venv
```

- 按照 .env.example 格式在项目根目录下创建 .env

  - 一般情况下可以通过 adb 查看到设备信息

  - ```powershell
    adb devices
    ```

  - 找到对应的模拟器，配置进 .env 中

  - 如果找不到，就进模拟器的设置中查看，只要支持 adb 都会有写端口号

  - 也可以通过修改环境变量

  - ```powershell
    # cmd 和 bash 的语法会不同
    $env:DEVICE="127.0.0.1:5555"
    ```

- 启动

  - ```powershell
    uv run python main.py
    ```

  - 也可以一键通过以下方式实现（包含快速通过端口配置模拟器 DEVICE 环境变量）

  - ```powershell
    .\start.ps1 -port 5565
    ```

## development

- 蓝叠多开后所在端口在设置 - 高级 - ADB 里可以看到
  - 主引擎一般在 5555（非多开情况下可能是 5554），多开后主引擎不一定能连上 adb，原因未知
  - 子引擎一般在 5565，多开一个往后 +10
  - 主引擎的修改不会自动同步到子引擎
  - 如果需要多开则需要在脚本启动前修改环境变量
- 图片模板基于 1600 x 900，游戏内配置启动全屏（默认就是）而不是 16：9，请最好保证模板图片的规格一致，分辨率的这些东西我没仔细研究，但只要你游戏窗口截图发现像素是 1600 x 900 那就基本上没错
  - 修改 dpi 后也会对脚本运行有影响，现在我代码里自适应的逻辑有点乱

- 部分刷取逻辑是写死在代码中的，所以要客制化最好看懂源码，实际上源码非常简单
- 用来做 erolabs 滑条验证的逻辑暂时没应用，现在用不上
- 实际上我根本没有写健全的测试

碎碎念：

- 我尝试过在 ubuntu 下装 waydroid，非常麻烦，需要支持 wayland 协议，然后需要配置网关，waydriod 支持的 android 系统非常抽象，文件交互也需要手动挂载
- airtest 框架非常轮椅，大部分情况不用自己手搓 opencv 了
- 由于无论如何都需要手动装模拟器，就不考虑写 Dockerfile 了
- 开发最好是蓝叠模拟器，有坐标显示功能，雷电找了一圈没找到

### uv

尝试了用 uv 管理环境，之前一直都是 conda，conda 的问题就是体积大速度慢

uv 是 rust 写的，用起来非常快，管理的理念也非常先进，后续其他项目我都想陆陆续续换成 uv

```powershell
# 安装
pip install uv
# 更新
uv self update

# 生成配置文件，会生成 toml 和 .python-version（不指定具体 python 版本就用你环境变量里的 python 版本，反正你可以手动改，如果要手动改 toml 里也需要改），如果没有 README 也会生成一个
uv init . --python 3.x
# 生成环境文件夹，这里也可以指定 python 版本，指定的和 .python-version 里面的不匹配就会有 warning，也可以不指定，就按 .python-version 来创建
# 这一步就会创建 venv 文件夹并链接 python 解释器，链接到 anaconda 的都有可能，反正它到处找，可能会有链接的问题
uv venv --python 3.x
# 如果有需要 add
# 之后同步
uv sync
# 如果 pycharm 导入解释器出问题，就多搞几次，如果 index 有问题就重启一下，反正很容易抽风

# 安装并添加到配置里，本质上还是靠 PyPI 来装包
uv add loguru
# 移除
uv remove loguru

# 同步依赖
uv sync  # 同步所有依赖
uv sync --dev  # 包括开发依赖
# 锁定依赖
uv lock  # toml 里只记录包的版本，这里会记录精确的依赖到 uv.lock 中

# 运行
# 会自动搜索默认环境并且激活
uv run python main.py
# 效果等同于你手动 activate 后 python main.py

# 查看已安装的包
uv pip list

# add 和 remove 会更新环境配置文件
# uv pip install 和 uv pip uninstall 不会，就这个区别
# 都会安装在 .venv/Lib/site-packages 下

# uv pip list 查看当前激活环境下所有的 pip 下的包
# 它也有激活这个概念，和 conda 一样
.venv\Scripts\activate  # linux 下加个 source
# 实现效果也一样，命令行前多了个环境，可以和 conda 叠叠乐
# 激活之后你 uv pip list 就会只看你激活的环境安装的包，否则就会看全局 pip 的
# 退出也和 conda 一样 deactivate

# uv init 和 uv venv 的区别
uv venv # 后面可以跟工作目录，不跟就在目录下创建个 .venv 来存，跟就会按你指定的名称创建一个文件夹在里面存
# 不跟，环境名称激活后就是项目名称，跟了就是环境文件夹的名称
# uv init 就是创建配置文件
# 默认 .venv 是项目默认环境，如果你激活项目下的 test 环境并且 add，那么 会有如下报警
`VIRTUAL_ENV=test` does not match the project environment path `.venv` and will be ignored; use `--active` to target the active environment instead

uv venv --python 3.11
# 实际上是寻找系统内可用的 python，并且用链接到项目中
# 找不到就会去下载，下到 ~\AppData 下

# 交付的时候就这样
uv venv  # 创建虚拟环境
uv sync  # 同步依赖到 .venv
```

## prompt

现在我在手动绑定邮箱，生成 prompt 如下，丢给 grok

```
生成随机的邮箱和密码，邮箱后缀 @legeclo.com，都是 10 位，邮箱如果有字母需要小写
同时帮我生成一个字符串，格式为 邮箱名称（不要@后面的东西）_密码
```

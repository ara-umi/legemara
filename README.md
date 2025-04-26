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

## prompt

现在我在手动绑定邮箱，生成 prompt 如下，丢给 grok

```
生成随机的邮箱和密码，邮箱后缀 @legeclo.com，都是 10 位，邮箱如果有字母需要小写
同时帮我生成一个字符串，格式为 邮箱名称（不要@后面的东西）_密码
```
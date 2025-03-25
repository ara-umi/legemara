# legemara

代码面条，结构混乱，性能低下，文档残缺，功能阉割，配置复杂

## env

- 基于 win10 x64

- 使用 conda 管理 python 环境，详见 environment.yaml
- 使用 adb 操作模拟器，需要安装 Google 的 platform-tools
  - https://developer.android.com/studio/releases/platform-tools
  - https://dl.google.com/android/repository/platform-tools-latest-windows.zip 这个可以直接下，下完把 platform-tools 丢进 PATH 里就行，轮椅教程 https://zhuanlan.zhihu.com/p/140828682

- 需要将 airtest 的 minitouch push 到 adb 并赋予执行权限，否则会有报警

## boot

- 通过 conda 安装 environment.yaml

```powershell
conda env create -f environment.yml
```

- 如果 adb 和模拟器正常启动，可以通过以下命令查看到 device 信息

```powershell
adb devices
```

- 按照 .env.example 格式在项目根目录下创建 .env
- 后续可能会写个启动脚本

## development

- 所有模板图片均基于 1600 x 900 游戏窗口（游戏内配置启动全屏而不是 16：9），如果你想二次开发，请最好保证模板图片的规格和以前的一样（代码上我提供了配置模板对应分辨率的地方，没测试过效果）
- 部分刷取逻辑是写死在代码中的，所以要客制化最好看懂源码，实际上源码非常简单
- 用来做 erolabs 滑条验证的逻辑暂时没应用，现在用不上
- 实际上我根本没有写健全的测试

碎碎念：

- 我尝试过在 ubuntu 下装 waydroid，非常麻烦，需要支持 wayland 协议，然后需要配置网关，waydriod 支持的 android 系统非常抽象，文件交互也需要手动挂载
- airtest 框架非常轮椅，大部分情况不用自己手搓 opencv 了
- 由于无论如何都需要手动装模拟器，就不考虑写 Dockerfile 了
- 开发最好是蓝叠模拟器，有坐标显示功能，雷电找了一圈没找到






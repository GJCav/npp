# 平面最近点对

![](example.png)





## 编译、运行

1. 克隆仓库

2. `cd npp`

3. 安装依赖：

   ```
   npm install
   pip install flask
   ```

4. 编译
   `npm run build`
5. 运行服务器：
   `python backend/server.py`
6. 浏览器打开`http://localhost:8089/`即进入程序。



## 开发、调试

1. 安装nginx，使用项目中`nginx.conf`配置。

2. 启动前端：`npm run dev`

3. 配置后端：`export FLASK_RUN_PORT=8089`

4. 然后可以在vscode中按F5调试后端代码。

这种配置支持热重载，开发起来比较方便。



## 项目结构

忽略那些复杂的配置文件和html代码，算法位于`backend/algorithm.py`文件，与之并列的`benchmark.py`包含一些快捷测试函数。
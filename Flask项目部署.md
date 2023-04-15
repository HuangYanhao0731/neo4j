# Flask项目部署

操作系统：Ubantu20

阿里云默认安装mysql8.0版本，python3.8

## 1.1安装nginx

更新安装源

1、sudo apt update

安装nginx

2、apt install nginx

换源安装MySQL5.7

```shell
cp /etc/apt/sources.list /etc/apt/sources.list.bak
```

编辑/etc/apt/sources.list

镜像地址

```python
deb http://mirrors.ustc.edu.cn/ubuntu/ xenial main restricted universe multiverse
deb http://mirrors.ustc.edu.cn/ubuntu/ xenial-security main restricted universe multiverse
deb http://mirrors.ustc.edu.cn/ubuntu/ xenial-updates main restricted universe multiverse
deb http://mirrors.ustc.edu.cn/ubuntu/ xenial-proposed main restricted universe multiverse
deb http://mirrors.ustc.edu.cn/ubuntu/ xenial-backports main restricted universe multiverse
deb-src http://mirrors.ustc.edu.cn/ubuntu/ xenial main restricted universe multiverse
deb-src http://mirrors.ustc.edu.cn/ubuntu/ xenial-security main restricted universe multiverse
deb-src http://mirrors.ustc.edu.cn/ubuntu/ xenial-updates main restricted universe multiverse
deb-src http://mirrors.ustc.edu.cn/ubuntu/ xenial-proposed main restricted universe multiverse
deb-src http://mirrors.ustc.edu.cn/ubuntu/ xenial-backports main restricted universe multiverse
```

更新安装源

```python
sudo apt update
```

## 1.2安装Mysql

mysql 安装

```shell
sudo apt install mysql-server mysql-client
```

安装memcache

```shell
apt install memcached
```

更新pip

```shell
pip3 install --upgrade pip
```

安装虚拟环境管理包

```shell
pip install virtualenvwrapper
```

虚拟环境配置

```shell
export WORKON_HOME=$HOME/.virtualenvs
VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh
```

执行命令

```shell
source ~/.bashrc
```

创建虚拟环境

```shell
mkvirtualenv --python=/usr/bin/python3 [项目名称]_env
```

## 1.3安装uwsgi

安装uwsgi

```shell
pip install uwsgi
```

路径：/srv/[项目名称]/uwsgi.ini

配置uwsgi

```shell
[uwsgi]
  
# 项目的路径
chdir           = /srv/[项目名称]/
# Flask的uwsgi文件
wsgi-file       = /srv/[项目名称]/app.py
# 回调的app对象
callable        = app
# Python虚拟环境的路径
home            = /root/.virtualenvs/[项目名称]_env

# 进程相关的设置
# 主进程
master          = true
# 最大数量的工作进程
processes       = 10

# http            = :5000 监听5000端口（或监听socket文件，与nginx配合）

socket          = /srv/[项目名称]/[项目名称].sock

# 设置socket的权限
chmod-socket    = 666
# 退出的时候是否清理环境
vacuum          = true
```

## 1.4nginx配置

nginx配置

```shell
upstream [项目名称]{
    server unix:///srv/[项目名称]/[项目名称].sock;
}

# 配置服务器
server {
    # 监听的端口号
    listen      80;
    # 域名
    server_name 47.117.122.52;
    charset     utf-8;

    # 最大的文件上传尺寸
    client_max_body_size 75M;

    # 静态文件访问的url
    location /static {
        # 静态文件地址
        alias /srv/[项目名称]/static; 
    }

    # 最后，发送所有非静态文件请求到uwsgi服务器
    location / {
        uwsgi_pass  [项目名称];
        # uwsgi_params文件地址
        include     /etc/nginx/uwsgi_params;
    }
}
```

测试nginx

```shell
service nginx configtest
```

重启nginx

```shell
service nginx restart
```

nginx 常用命令

```shell
启动：service nginx start
关闭：service nginx stop
重启：service nginx restart
测试配置文件：service nginx configtest
```

启动运行uwsgi

```python
uwsgi --ini uwsgi.ini
```

使用supervisor管理uwsgi进程

安装supervisor

```shell
pip install supervisor
```

配置文件：/srv/etc/[项目名称]/supervisor.conf

```shell
# upervisor的程序名字
[program:项目名称]
# supervisor执行的命令
command=uwsgi --ini uwsgi.ini
# 项目的目录
directory = /srv/[项目名称]
# 开始的时候等待多少秒
startsecs=0
# 停止的时候等待多少秒
stopwaitsecs=0
# 自动开始
autostart=true
# 程序挂了后自动重启
autorestart=true
# 输出的log文件
stdout_logfile=/var/log/[项目名称]_supervisord.log
# 输出的错误文件
stderr_logfile=/var/log/[项目名称]_supervisord.err

[supervisord]
# log的级别
loglevel=debug

[inet_http_server]
# supervisor的服务器
port = :9001
# 用户名和密码
username = admin
password = 123456

# 使用supervisorctl的配置
[supervisorctl]
# 使用supervisorctl登录的地址和端口号
serverurl = http://127.0.0.1:9001

# 登录supervisorctl的用户名和密码
username = admin
password = 123456

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface
```

启动supervisor

```shell
supervisord -c supervisor.conf
```

通过supervisor客户端查看进程

```shell
supervisorctl -c supervisor.conf # 进入到管理控制台
```

supervisor 常用明令

```shell
status # 查看状态
start program_name #启动程序
restart program_name #重新启动程序
stop program_name # 关闭程序
reload # 重新加载配置文件
quit # 退出控制台
```
































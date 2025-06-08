# 基础镜像
FROM python:3.8-alpine
# 打标签
# LABEL key=value
# 给镜像一些额外信息
LABEL description='ck15 django project'

# 创建或切换工作目录 WORKDIR dir
# 如果dir存在则切换进去，如果不存在则创建并切换
WORKDIR /app

# 拷贝文件到镜像
# COPY 宿主机目录 镜像目录
# 宿主机的目录只能是相对路径，相对Dockerfile
# 镜像目录可以是相对路径，相对WORKDIR的路径，也可以是绝对路径
COPY . .

# 安装必要的库
# 执行的shell命令
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories && \
    apk update && \
    apk upgrade && \
    apk add --no-cache tzdata mariadb-dev gcc libc-dev && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone && \
    python -m pip install -i https://pypi.douban.com/simple --upgrade pip && \
    pip install --no-cache-dir -i https://pypi.douban.com/simple -r requirements.txt && \
    chmod 777 ./entrypoint.sh

# 创建日志挂载点避免容器体积越来越大
VOLUME /app/logs/

# 挂载一下端口
EXPOSE 8000

# 启动容器后要执行的命令
# docker run 时的命令会覆盖CMD
# CMD ["bash", "entrypoint.sh"]
# CMD ["aaa"]
ENTRYPOINT ["./entrypoint.sh"]



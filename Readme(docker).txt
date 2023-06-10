1. docker启动命令：sudo docker run --name test_mini_cuda114 --gpus all -it -p 3050:3050 -p 5008:5008 mini_cuda114
(务必配置-p 3050:3050 -p 5008:5008两个宿主机到容器的端口映射)
2.进入容器后，启动前端命令：1) cd /home/open/nginx/sbin;  2)./ nginx

3.进入容器后，启动后端命令：1) cd /code/backend 2) python app.py

4.linux火狐浏览器可能有bug（输入localhost:3050)，可以用同一局域网下的windows浏览器进行访问，输入linux电脑ip:3050进行访问


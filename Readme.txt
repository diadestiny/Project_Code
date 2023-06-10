1.代码结构：
1) backend 后端文件夹
2) frontend 前端文件夹
3) mmdet 后端依赖的mmdection库，需要手动编译

2.环境说明
1) 编译mmdet文件夹需要: mmcv>=1.3.17 <=1.7.0.
mmcv依赖包下载命令见https://mmcv.readthedocs.io/en/1.x/get_started/installation.html（mmcv需要对应torch和cuda版本）

2) backend依赖包：见backend/requirements.txt
没有版本限制，torch和torchvision和cuda、python对应即可，下载链接见https://download.pytorch.org/whl/torch_stable.html

3.后端环境安装步骤
1) 安装 backend依赖包：见backend/requirements.txt (只上传了基于python38、cuda11的版本)
2）安装 Cython.whl 依赖包 (只上传了基于python38的版本)
3) 编译mmdet命令：
cd mmdet
python setup.py develop
4)后端启动命令：
cd backend
python app.py

4.前端安装步骤，参考https://www.jianshu.com/p/40594bccff9a
1) 换内网源后，sudo apt-get install nginx
2) 修改前端端口为3050：
cd /etc/nginx
cd sites-enabled
修改default文件的17、18行的listen 80 default_server;listen [::]:80 default_server;将80改成3050；
3) 将frontend/dist里面的所有文件复制到/var/www/html
cd 项目根目录
cp -r frontend/dist/* /var/www/html
4) 前端启动命令
./nginx
./nginx -s stop (前端停止命令)





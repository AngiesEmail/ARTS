* 目录:/etc/apache2
* 文件:httpd.conf
* 内容:
	* DocumentRoot "/Library/WebServer/Documents"
	* ErrorLog "/private/var/log/apache2/error_log"
	* Include /private/etc/apache2/other/*.conf
	* User _www
	* Group _www
* 修改权限
	* sudo chmod 777 httpd.conf
* 修改
	* User
	* Group
	* DocumentRoot
* 修改群组与权限
	* sudo chown -R angie:staff ARTS
* 启动服务
	* sudo apachectl start/restart
* 启动服务前提
	* 在配置目录 DocumentRoot 下，有一个index.html文件
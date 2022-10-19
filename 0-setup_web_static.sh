#!/usr/bin/env bash
# a Bash script that sets up web servers for the deployment of web_static
sudo apt-get -y update
sudo apt-get -y install nginx
sudo ufw allow 'Nginx HTTP'
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
echo "<html>
  <head>
  </head>
  <body>
    Test the release
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -hR ubuntu:ubuntu /data
sudo sed -i "/listen 80 default_server;/a\\\tlocation /hbnb_static {\n\t\t alias /data/web_static/current/;\n\t}" /etc/nginx/sites-available/default
sudo service nginx restart
exit 0

#!/usr/bin/env bash
# Puppet:
package { 'nginx':
  ensure   => 'present',
  provider => 'apt'
} ->

file { '/data':
  ensure  => 'directory'
} ->

file { '/data/web_static':
  ensure => 'directory'
} ->

file { '/data/web_static/releases':
  ensure => 'directory'
} ->

file { '/data/web_static/releases/test':
  ensure => 'directory'
} ->

file { '/data/web_static/shared':
  ensure => 'directory'
} ->

file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "Test release\n"
} ->

exec {'hbnh_static location':
  provider => shell,
  command  => 'sudo sed -i "/listen 80 default_server;/a\\\tlocation /hbnb_static/ {\n\t\t alias /data/web_static/current/;\n\t}" /etc/nginx/sites-available/default',
  before   => Exec['restart Nginx'],
} ->

file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test'
} ->

file {'/data/':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
} ->

exec {'restart Nginx':
  provider => shell,
  command  => 'sudo service nginx restart',
}

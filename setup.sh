#!/bin/bash

function install_node_exporter() {
  version=${1}
  echo "Install node exporter version ${version}"
  url="https://github.com/prometheus/node_exporter/releases/download/v${version}/node_exporter-${version}.linux-amd64.tar.gz"
  wget -O - ${url} | tar zxvf - -C /tmp
  cp /tmp/node_exporter-${version}.linux-amd64/node_exporter /usr/sbin/
}

function setup_node_exporter() {
  echo "set up node_exporter"
  echo "link node_exporter.service to /etc/systemd/system/node_exporter.service"
  ln -nfs $(pwd)/node_exporter.service /etc/systemd/system/node_exporter.service
  echo "link sysconfig.node_exporter to /etc/node_exporter"
  ln -nfs $(pwd)/sysconfig.node_exporter /etc/node_exporter
  echo "reload systemd ..."
  /bin/systemctl daemon-reload
  /bin/systemctl enable node_exporter.service
  /bin/systemctl start node_exporter.service
  /bin/systemctl status node_exporter.service -l
  echo "finish"
}

function setup_textfile_collector() {
  echo "set up textfile collector"
  textfile_collector_dir=${1}
  # TODO: avoid dupulication
  echo "30 * * * * root $(pwd)/text_collector/apt.sh > ${textfile_collector_dir}/apt.prom" >> /etc/crontab
  echo "5 * * * * root $(pwd)/text_collector/user.py > ${textfile_collector_dir}/user.prom" >> /etc/crontab
}

function setup_cadvisor() {
  echo "set up cadvisor ..."
  docker-compose down
  docker-compose up -d --build
  docker-compose ps
  echo "finish"
}

install_node_exporter "0.15.2"
setup_node_exporter
setup_textfile_collector "/var/lib/node_exporter/textfile_collector"
setup_cadvisor

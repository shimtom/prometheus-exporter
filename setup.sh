#!/bin/bash

function install_node_exporter() {
  version=${1}
  echo "Install node exporter version ${version}"
  url="https://github.com/prometheus/node_exporter/releases/download/v${version}/node_exporter-${version}.linux-amd64.tar.gz"
  wget -O - ${url} | tar zxvf -
  cp node_exporter-${version}.linux-amd64/node_exporter /usr/sbin/
}

function setup_node_exporter() {
  echo "set up node_exporter"
  echo "copy node_exporter.service to /etc/systemd/system/node_exporter.service"
  cp ./node_exporter.service /etc/systemd/system/
  echo "copy sysconfig.node_exporter to /etc/node_exporter"
  cp ./sysconfig.node_exporter /etc/node_exporter
  echo "reload systemd ..."
  /bin/systemctl daemon-reload
  /bin/systemctl enable node_exporter.service
  /bin/systemctl start node_exporter.service
  /bin/systemctl status node_exporter.service -l
  echo "finish"
}

function setup_cadvisor() {
  echo "set up cadvisor ..."
  docker-compose up -d --build
  docker-compose ps
  echo "finish"
}

install_node_exporter "0.15.2"
setup_node_exporter
setup_cadvisor

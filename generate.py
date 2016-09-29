#!/usr/bin/env python3

# MAINTAINER Pierre-Antoine 'ZHAJOR' Tible <antoinetible@gmail.com>

import argparse
import os.path


api_availables = {'laravel': 'zhajor/docker-apache-2.4-php5.6-for-laravel',
                  'phalcon': 'zhajor/docker-apache-php7-phalcon'}

db_availables = {'postgres': 'postgres:latest'}

"""The API image to use when the parameter --api-image is not set"""
default_api_image = api_availables['phalcon']

"""The db image to use wghen the parameter --db-image is not set"""
default_db_image = db_availables['postgres']

"""The base name to set to containers"""
default_base_container_name = 'zhajor-compose-'


default_api = {
    'image': default_api_image,
    'ports': [[2000, 80], [3000, 22]],
    'container-name': 'api',
    'volumes': [['./tutorial', '/var/www/html'], ['direcoty', '/boom/boom']],
    'networks': [['net', ['api', 'api2']], ['nety', ['apiy', 'apiy2']]],
    'environments': [['proxy', '/api'], ['proxy-host', 'http://api']]
}


def check_docker_compose_exists():
    if os.path.exists('./docker-compose.yml'):
        exit('A docker-compose.yml already exists. Abort.')


class ImageBlock:
    """This class allows to create a configuration for an image"""
    block = ""
    image = ""
    ports = ""
    container_name = ""
    volumes = ""
    networks = ""
    environments = ""

    not_mapped = ["block"]
    """All the variables in this array will not be put in the docker compose block code"""

    def __init__(self, name):
        self.block = "\t" + name + ":"

    def set_from_conf(self, conf):
        if 'image' in conf:
            self.set_image(conf.get('image'))
        if 'ports' in conf:
            self.set_ports(conf.get('ports'))
        if 'container_name' in conf:
            self.set_container_name(conf.get('container_name'))
        if 'volumes' in conf:
            self.set_volumes(conf.get('volumes'))
        if 'networks' in conf:
            self.set_networks(conf.get('networks'))
        if 'environments' in conf:
            self.set_environments(conf.get('environments'))

    def set_image(self, name):
        self.image += "\n\t\timage: " + name

    def set_ports(self, ports):
        self.ports += '\n\t\tports:'
        for port in ports:
            self.ports += '\n\t\t\t- "' + str(port[0]) + ':' + str(port[1]) + '"'

    def set_container_name(self, container_name):
        self.container_name += "\n\t\tcontainer_name: " + default_base_container_name+ container_name

    def set_volumes(self, volumes):
        self.volumes += "\n\t\tvolumes:"
        for volume in volumes:
            self.volumes += "\n\t\t\t- " + volume[0] + ":" + volume[1]

    def set_networks(self, networks):
        self.networks += "\n\t\tnetworks:"
        for net in networks:
            self.networks += '\n\t\t\t' + net[0] + ':'
            self.networks += '\n\t\t\t\taliases:'
            for alias in net[1]:
                self.networks += "\n\t\t\t\t\t- " + alias

    def set_environments(self, environments):
        self.environments += "\n\t\tenvironment:"
        for environment in environments:
            self.environments += "\n\t\t\t- "+environment[0]+"="+environment[1]

    def get(self):
        value = self.block
        for item in vars(self).items():
            if item.__getitem__(0) not in self.not_mapped:
                value += item.__getitem__(1)
        return value


parser = argparse.ArgumentParser(description='Create your docker-compose configuration')
parser.add_argument('--name', help='The project name', required=False, metavar='my-project')
parser.add_argument('--port', help='The port', required=False, metavar='24000')
parser.add_argument('--with-proxy', dest='with_proxy', help='Use a proxy for the api', action='store_true')

args = parser.parse_args()


bouga = ImageBlock('api')
bouga.set_from_conf(default_api)

bouga.get()


#print(args.with_proxy)
file = open('test', 'w')
file.write(bouga.get())
file.close()

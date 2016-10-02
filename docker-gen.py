#!/usr/bin/env python3

# MAINTAINER Pierre-Antoine 'ZHAJOR' Tible <antoinetible@gmail.com>

import argparse
import os.path

"""The list of available images"""
images_available = {'api':
                        {'laravel': 'zhajor/docker-apache-2.4-php5.6-for-laravel',
                         'phalcon': 'zhajor/docker-apache-php7-phalcon'},
                    'db':
                        {'postgres': 'postgres:latest'},
                    'front':
                        {'angular': 'zhajor/docker-apache-2.4-proxy'},
                    'db_administration':
                        {'phppgadmin': 'zhajor/docker-phppgadmin'}
                    }

"""The image to use when the parameter --api or --front or --db or --db-admin is not set"""
default_image = {'api': images_available['api']['phalcon'],
                 'db': images_available['db']['postgres'],
                 'front': images_available['front']['angular'],
                 'db_administration': images_available['db_administration']['phppgadmin']}

default_compose_version = 2

api_configuration = {
    'image': default_image['api'],
    'ports': [80],
    'container-name': 'api',
    'volumes': [['./api', '/var/www/html']],
    'networks': [['net', ['api']]]
}

front_configuration = {
    'image': default_image['front'],
    'ports': [80],
    'container-name': 'front',
    'volumes': [['./front', '/var/www/html']],
    'networks': [['net', ['front']]],
    'environments': [['proxy', '/api'], ['proxy-host', 'http://api']]
}

db_configuration = {
    'image': default_image['db'],
    'container-name': 'db',
    'volumes': [['./database/data', '/var/lib/postgresql/data']],
    'networks': [['net', ['database']]],
    'environments': [['POSTGRES_USER', '/api'],
                     ['POSTGRES_DB', 'http://api'],
                     ['POSTGRES_PASSWORD', 'http://api']]
}

db_administration_configuration = {
    'image': default_image['db_administration'],
    'ports': [80],
    'container-name': 'db_administration',
    'networks': [['net', ['phppgadmin']]],
    'environments': [['DB_PORT', '5432'],
                     ['DB_HOST', 'http://database']]
}


parser = argparse.ArgumentParser(description='Create your docker-compose configuration within a minute')
parser.add_argument('--name', help='The project name', required=True, metavar='my-project')
parser.add_argument('--port', help='The port', required=True, metavar='24000')
parser.add_argument('--file', help='The output file name', metavar='docker-compose.yml', default='docker-compose.yml')
parser.add_argument('--no-front', dest='no_front', help='Do not use a front container', action='store_true')
parser.add_argument('--no-api', dest='no_api', help='Do not use an api container', action='store_true')
parser.add_argument('--no-db', dest='no_db', help='Do not use a db container', action='store_true')
parser.add_argument('--no-db-admin', dest='no_db_admin', help='Do not use a db configuration container', action='store_true')
parser.add_argument('--api', help='The image to use for an api', metavar='phalcon')
parser.add_argument('--front', help='The image to use for an api', metavar='angular')
parser.add_argument('--db', help='The image to use for an api', metavar='postgres')
parser.add_argument('--db-admin', help='The image to use for an api', metavar='phppgadmin')
args = parser.parse_args()

defined_port = int(args.port)
defined_base_container_name = args.name + "-"
document = "version: '" + str(default_compose_version) + "'\n\nservices:\n"
default_networks = "networks:\n  net:"


def check_images(args):
    if args.api is not None:
        api_configuration['image'] = images_available['api'][args.api]
    if args.front is not None:
        front_configuration['image'] = images_available['front'][args.front]
    if args.db is not None:
        db_configuration['image'] = images_available['db'][args.db]
    if args.db_admin is not None:
        db_administration_configuration['image'] = images_available['db_administration'][args.db_admin]


def update_conf(config):
    new_conf = []
    for p in config['ports']:
        new_conf.append([int(args.port), p])
        print(config['container-name'] + " set to port " + args.port)
        args.port = str(int(args.port) + 1)
        config['ports'] = new_conf


class colors:
    CIAN = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def check_file_exists():
    if os.path.exists(args.file):
        error = input(colors.FAIL + "[WARNING]" + colors.ENDC + " " + args.file + " already exists, do you want to ecrase it ?\n[Y,n]: ")
        if error.lower() == "y" or error == "":
            print("Erasing the file...")
        else:
            exit("Aborted.")


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
        self.block = "  " + name + ":"

    def set_from_conf(self, conf):
        if 'image' in conf:
            self.set_image(conf.get('image'))
        if 'ports' in conf:
            self.set_ports(conf.get('ports'))
        if 'container-name' in conf:
            self.set_container_name(conf.get('container-name'))
        if 'volumes' in conf:
            self.set_volumes(conf.get('volumes'))
        if 'networks' in conf:
            self.set_networks(conf.get('networks'))
        if 'environments' in conf:
            self.set_environments(conf.get('environments'))

    def set_image(self, name):
        self.image += "\n    image: " + name

    def set_ports(self, ports):
        self.ports += '\n    ports:'
        for port in ports:
            self.ports += '\n      - "' + str(port[0]) + ':' + str(port[1]) + '"'

    def set_container_name(self, container_name):
        self.container_name += "\n    container_name: " + defined_base_container_name + container_name

    def set_volumes(self, volumes):
        self.volumes += "\n    volumes:"
        for volume in volumes:
            self.volumes += "\n      - " + volume[0] + ":" + volume[1]

    def set_networks(self, networks):
        self.networks += "\n    networks:"
        for net in networks:
            self.networks += '\n      ' + net[0] + ':'
            self.networks += '\n        aliases:'
            for alias in net[1]:
                self.networks += "\n          - " + alias

    def set_environments(self, environments):
        self.environments += "\n    environment:"
        for environment in environments:
            self.environments += "\n      - "+environment[0]+"="+environment[1]

    def get(self):
        value = self.block
        for item in vars(self).items():
            if item.__getitem__(0) not in self.not_mapped:
                value += item.__getitem__(1)
        return value + "\n\n"


check_file_exists()
check_images(args)

if not args.no_front:
    update_conf(front_configuration)
    front = ImageBlock('front')
    front.set_from_conf(front_configuration)
    document += front.get()
if not args.no_api:
    update_conf(api_configuration)
    api = ImageBlock('api')
    api.set_from_conf(api_configuration)
    document += api.get()
if not args.no_db:
    db = ImageBlock('db')
    db.set_from_conf(db_configuration)
    document += db.get()
    if not args.no_db_admin:
        update_conf(db_administration_configuration)
        db_admin = ImageBlock('db_admin')
        db_admin.set_from_conf(db_administration_configuration)
        document += db_admin.get()


document += default_networks

file = open(args.file, 'w')
file.write(document)
file.close()

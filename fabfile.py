from fabric import *
import datetime

config.datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
config.source = '/home/gustavo/www/wms'
config.project = 'wms'
config.package_compress = '$(project).tar.gz'

config.destination = '/var/www/projects'

# Remote servers
config.fab_user = 'username'
config.fab_password = 'password'
config.fab_hosts = ['gustavohenrique.net']

def deploy():
    # Remove os *.pyc
    local("find $(source)/$(project) -name '*.pyc' -delete")
    local("find $(source)/$(project) -name '*~' -delete")

    # Compacta
    local('cd $(source) && tar czvf /tmp/$(package_compress) $(project) --exclude=files --exclude-vcs')

    # Envia ao dir /tmp do servidor
    put('/tmp/$(package_compress)','/tmp')

    # Backup do dir do projeto no servidor
    run('tar czvf $(destination)/$(datetime).tar.gz $(destination)/$(project)')

    # Descompacta
    run('tar zxvf /tmp/$(package_compress) -C $(destination)')

    # Cria symlinks
    run('ln -sf /var/www/projects/wms/grappelli/templates/admin /var/www/projects/wms/templates/admin')
    run('ln -sf /var/www/projects/wms/grappelli/media /var/www/projects/wms/media/admin')

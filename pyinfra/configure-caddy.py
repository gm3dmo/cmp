from pyinfra.operations import files

# Define your Caddyfile configuration
caddyfile_config = '''
www.corpsofmilitarypolice.org, corpsofmilitarypolice.org {
    root * /usr/share/caddy
    file_server
    reverse_proxy 127.0.0.1:8000
}
'''

# Put the configuration into the Caddyfile
files.put(
    name='Put configuration into Caddyfile',
    src=caddyfile_config,
    dest='/etc/caddy/Caddyfile',
)

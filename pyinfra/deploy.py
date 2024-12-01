
import sys
from pyinfra import host
from pyinfra.api import deploy
from pyinfra.facts.server import LinuxDistribution
from pyinfra.operations import apt, files, server, git


@deploy("Install common base packages for The Power")
def install_base_packages():
    apt.packages(
        name="Install base packages",
        packages=["python3.12-venv", "vim", "zip", "sqlite3" ],
        update=True,
        _sudo=True,
        cache_time=3600,
    )


@deploy("Install third party products")
def install_third_party_packages():
    server.shell(
    name='Setup apt sources for third party products caddy, gh cli, git',
    commands=[
        'sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https curl',
        'curl -1sLf \'https://dl.cloudsmith.io/public/caddy/stable/gpg.key\' | sudo apt-key add -'
        'curl -1sLf \'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt\' | sudo tee /etc/apt/sources.list.d/caddy-stable.list',
        # gh cli
        "curl -1sLf https://cli.github.com/packages/githubcli-archive-keyring.gpg -o githubcli-archive-keyring.gpg",
        "sudo mv githubcli-archive-keyring.gpg /usr/share/keyrings/githubcli-archive-keyring.gpg",
        'sudo apt update',

    ]
    )
    apt.packages(
        name="Debian third party packages",
        packages=["caddy", "gh" ],
        update=True,
        _sudo=True,
        cache_time=3600,
    )

@deploy("Configure Caddy Proxying Web Server")
def configure_caddy_server():
 
    files.template(
        name="Create a templated caddy config file",
        src="caddyfile.template",
        dest="/etc/caddy/Caddyfile",
        _sudo = True
)


linux_distribution = host.get_fact(LinuxDistribution)

if linux_distribution['name'].lower() in ['ubuntu', 'debian']:
    install_base_packages()
    install_third_party_packages()
else:
    print(f"Unsupported operating system: {linux_distribution['name']}")

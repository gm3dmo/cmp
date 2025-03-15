
import sys
from pyinfra import host
from pyinfra.api import deploy
from pyinfra.facts.server import LinuxDistribution
from pyinfra.operations import apt, files, server, git


@deploy("Install base packages for CMP")
def install_base_packages():
    apt.packages(
        name="Install base packages from Ubuntu sources",
        packages=["python3.12-venv", "vim", "zip", "apt-transport-https",
                  "ca-certificates", "curl", "gnupg", "lsb-release",
                  ],
        update=True,
        _sudo=True,
        cache_time=3600,
    )


@deploy("Install third party products")
def install_third_party_packages():
    server.shell(
    name='Setup apt sources for third party products caddy, gh cli, git, azure cli',
    commands=[
        'sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https curl',
        'curl -1sLf \'https://dl.cloudsmith.io/public/caddy/stable/gpg.key\' | sudo apt-key add -'
        'curl -1sLf \'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt\' | sudo tee /etc/apt/sources.list.d/caddy-stable.list',
        # gh cli
        "curl -1sLf https://cli.github.com/packages/githubcli-archive-keyring.gpg -o githubcli-archive-keyring.gpg",
        "sudo mv githubcli-archive-keyring.gpg /usr/share/keyrings/githubcli-archive-keyring.gpg",
        'sudo apt update',
        # Azure CLI
        'sudo mkdir -p /etc/apt/keyrings',
        'curl -sLS https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | sudo tee /etc/apt/keyrings/microsoft.gpg > /dev/null',
  'sudo chmod go+r /etc/apt/keyrings/microsoft.gpg',
  'AZ_DIST=$(lsb_release -cs)',
  """echo "Types: deb
URIs: https://packages.microsoft.com/repos/azure-cli/
Suites: ${AZ_DIST}
Components: main
Architectures: $(dpkg --print-architecture)
Signed-by: /etc/apt/keyrings/microsoft.gpg" | sudo tee /etc/apt/sources.list.d/azure-cli.sources"""
    ]
    )
    apt.packages(
        name="Debian third party packages",
        packages=["caddy", "gh"  ],
        update=True,
        _sudo=True,
        cache_time=3600,
    )

@deploy("Configure Caddy Proxying Web Server")
def configure_caddy_server():
    # Prompt the user to enter their hostname
    hostname = input("Please enter your hostname: ")

    files.template(
        name="Create a templated caddy config file",
        src="caddyfile.template",
        dest="/etc/caddy/Caddyfile",
        hook_hostname=hostname,
        _sudo=True
    )


@deploy("Clone CMP Project")
def clone_cmp():
    git.repo(
        name="Clone CMP",
        src="https://github.com/gm3dmo/cmp.git",
        dest="/home/azureuser/cmp",
    )


# Determine the Linux distribution
linux_distribution = host.get_fact(LinuxDistribution)

if linux_distribution['name'].lower() in ['ubuntu', 'debian']:
    install_base_packages()
    install_third_party_packages()
    #configure_caddy_server()
    #clone_cmp()
else:
    print(f"Unsupported operating system: {linux_distribution['name']}")

from pyinfra import host
from pyinfra.facts.server import LinuxDistribution
from pyinfra.operations import apt, server

def install_gh_cli_ubuntu():
    # Download the GitHub CLI GPG key
    server.shell(
        name="Download GitHub CLI GPG key",
        _sudo=True,
        commands=[
            "curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg -o githubcli-archive-keyring.gpg",
            "sudo mv githubcli-archive-keyring.gpg /usr/share/keyrings/githubcli-archive-keyring.gpg",
        ],
    )

    # Correctly add the GitHub CLI repository using heredoc
    server.shell(
        name="Add the GitHub CLI repository",
        _sudo=True,
        commands='''
sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null <<EOF
deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main
EOF
        ''',
    )

    # Update apt repositories and install GitHub CLI
    apt.packages(
        name="Update and install GitHub CLI",
        packages=["gh"],
        update=True,
        latest=True,
        _sudo=True,
    )

# Determine the Linux distribution
linux_distribution = host.get_fact(LinuxDistribution)

if linux_distribution['name'].lower() in ['ubuntu', 'debian']:
    install_gh_cli_ubuntu()
else:
    print(f"Unsupported operating system: {linux_distribution['name']}")

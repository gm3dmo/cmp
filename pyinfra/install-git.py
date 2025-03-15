from pyinfra.operations import apt, server

# Add the PPA for git-core
server.shell(
    name='Add git-core PPA',
    commands='sudo add-apt-repository -y ppa:git-core/ppa',
    _sudo=True,
)

# Update apt repositories
apt.update(
    name='Update apt cache',
    _sudo=True,
)

# Install git
apt.packages(
    name='Install git (latest version)',
    packages=['git'],
    _sudo=True,
    update=True,      # Ensures the apt cache is updated
    latest=True       # Upgrades to the newest available version
)

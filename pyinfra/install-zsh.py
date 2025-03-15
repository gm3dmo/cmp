from pyinfra.operations import apt

apt.packages(
    name='Ensure zsh is installed',
    packages=['zsh'],
    update=True,  # Runs `apt-get update` before installing
    _sudo=True,
    cache_time=3600,  # Cache update for 3600 seconds to speed up subsequent runs
)

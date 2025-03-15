from pyinfra.operations import apt

apt.packages(
    name='Ensure python-venv is installed',
    packages=['python3.12-venv'],
    update=True,  # Runs `apt-get update` before installing
    _sudo=True,
    cache_time=3600,  # Cache update for 3600 seconds to speed up subsequent runs
)

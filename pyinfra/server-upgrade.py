from pyinfra.operations import apt, server

# Update package lists with sudo
apt.update(
    name="Update package lists",
    _sudo=True
)

# Upgrade all packages with sudo
apt.upgrade(
    name="Upgrade all packages",
    _success_exit_codes=[0, 100],  # 100 is returned if there are no packages to upgrade
    _sudo=True
)

# Perform a distribution upgrade with sudo
apt.dist_upgrade(
    name="Perform a distribution upgrade",
    _success_exit_codes=[0, 100],  # As above, to handle no upgrades case
    _sudo=True
)

# Optionally reboot the server if required (useful for kernel upgrades)
# Reboot does not require sudo=True as it's inherently a privileged operation
server.reboot(
    name="Reboot the server if required",
    reboot_timeout=300,  # Wait up to 5 minutes for the server to reboot
    _sudo=True
)

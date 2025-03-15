from pyinfra.operations import server

sudoers_line = 'azureuser ALL=(ALL) NOPASSWD: ALL'
file_path = '/etc/sudoers.d/azureuser'

# Use echo to write the line to a file in /etc/sudoers.d, setting correct permissions
server.shell(
    name="Allow azureuser to sudo without a password",
    commands=[
        f'echo "{sudoers_line}" > {file_path}',
        f'chmod 0440 {file_path}',  # Set correct permissions
        f'chown root:root {file_path}',  # Ensure ownership is root
    ],
    _sudo=True,
)

from pyinfra.operations import server

# Command to set the default editor to vim
set_default_editor_command = 'update-alternatives --set editor /usr/bin/vim.basic'

# Execute the command on the remote host
server.shell(
    name="Set default editor to vim",
    commands=set_default_editor_command,
    _sudo=True,  # This command requires superuser privileges
)

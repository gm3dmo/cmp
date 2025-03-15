import sys
from pyinfra import logger
from pyinfra.operations import python, server

# Define the crontab entry
crontab_entry = '0 6,22 * * * /usr/bin/apt-get update && /usr/bin/apt-get -y upgrade'

# Check if the crontab entry already exists
check_crontab_command = f'(crontab -l 2>/dev/null | grep -F "{crontab_entry}") || echo "not found"'

# Add the crontab entry if it doesn't exist
add_crontab_command = f'(crontab -l 2>/dev/null; echo "{crontab_entry}") | crontab -'


result = server.shell(
    name='Check if crontab entry exists',
    commands=[check_crontab_command],
    _sudo=True,
)


def callback():
    if 'not found' in result.stdout_lines:
        logger.info("Crontab entry not found, adding it now.")
        server.shell(
            name='Add crontab entry',
            commands=[add_crontab_command],
            _sudo=True
        )
    else:
        logger.info(f"Crontab entry found: {result.stdout}")


python.call(
    name="Execute callback function to print the result",
    function=callback,
)

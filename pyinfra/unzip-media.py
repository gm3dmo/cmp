from pyinfra.operations import server

# Unzip the file
server.shell(
    name='Unzip media.zip',
    commands=[
        'unzip media.zip -d cmp/staticfiles/media',
    ],
)

from pyinfra.operations import git

# Clone the 'bobby' branch of the repository
git.clone(
    name='Clone bobby branch of cmp repository',
    repo='https://github.com/gm3dmo/cmp.git',
    target='cmp',
    branch='main',
)

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    
    name = "crowdplay",
    version = "0.1",
    packages = ['crowdplay'],
    package_dir = {'':'src'},

    install_requires = [
        'setuptools',
        'tornado',
        'pymongo',
        'mutagen',
        ],
                        
    include_package_data = True,
    zip_safe = True,

    entry_points = {
        'console_scripts' : [
            'server = crowdplay.main:start_server',
            'next_song = crowdplay.queue:next_song',
            'update_catalog = crowdplay.catalog:update_music_catalog',
            ],
        },
    
    author = 'John E Doig III',
    author_email = 'john@doig.me',
    description = 'Simple web app that allows users to vote up or down tracks to be played in a web stream.',
    license = 'AGPL 3.0',

    )

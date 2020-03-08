from setuptools import setup

setup(
    name='nous_app',
    packages=['nous_app'],
    include_package_data=True,
    install_requires=[
        'flask',
        'pandas',
        'bokeh',
        'emoji'
    ],
)
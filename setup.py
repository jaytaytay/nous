from setuptools import setup

setup(
    name='nous_app',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'pandas',
        'bokeh',
        'emoji'
    ],
)
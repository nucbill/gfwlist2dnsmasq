from setuptools import setup

with open('README.rst') as f:
    long_description = f.read()

setup(
    name="gfwlist2dnsmasq",
    version="0.1.0",
    license='MIT',
    description="convert gfwlist to dnsmasq config file",
    author='nucbill',
    author_email='nucbill100@gmail.com',
    url='https://github.com/nucbill/gfwlist2dnsmasq',
    packages=['gfwlist2dnsmasq', 'gfwlist2dnsmasq.resources'],
    package_data={
        'gfwlist2dnsmasq': ['README.rst', 'LICENSE', 'resources/*']
    },
    install_requires=[],
    entry_points="""
    [console_scripts]
    gfwlist2dnsmasq = gfwlist2dnsmasq.main:main
    """,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    long_description=long_description,
)

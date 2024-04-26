from setuptools import setup, find_packages 

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name = 'mt5_dataloader',
    description = 'A query engine for historical market data on MetaTrader5',
    long_description = readme,
    long_description_content_type = 'text/markdown',
    version = '1.0.0',
    author = 'Jay Alfaras',
    author_email='alfarasjb@gmail.com',
    url ='https://github.com/alfarasjb/MT5-Dataloader',
    packages = find_packages(),
    license='MIT',
    install_requires = [
        'pandas>=2.0.0',
        'matplotlib>=3.5.2',
        'MetaTrader5>=5.0.45'
    ],
    include_package_data=True,
    python_requires = '>=3.8'
)
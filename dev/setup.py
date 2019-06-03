from setuptools import setup, find_packages

install_requires = ['django', 'mysqlclient', 'channels', 'channels_redis', 'daphne','pywin32','django-formtools','django_countries', 'websocket-client','pypiwin32',
                    'django-guardian', 'GeoIP2']


setup(
	name='SADNA',
	version='1.0.0',
	packages=find_packages(),
	url='https://github.com/ashr123/Workshop-On-Software-Engineering-Project-2019',
	license='',
	author='Rotem Barak',
	author_email='rotba@post.bgu.ac.il',
	install_requires=install_requires,
	description='Python Distribution Utilities',

)

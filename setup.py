from distutils.core import setup


setup(
    name="djangorestframeworkcache",
    packages=["rest_framework_cache"],
    version="0.0.2",
    license="MIT",
    description="REST Framework Cache is a powerful and flexible toolkit for building cached views based on a fully dynamic lifecycle based on the variation of the information they provide.",
    author="Eduardo Ventura Izquierdo Nuñez",
    author_email="in.eduardo.v@outlook.com",
    url="https://github.com/dot-tostring/rest_framework_cache",
    keywords=["django", "rest", "cache"],
    install_requires=[
        "django",
        "djangorestframework",
    ],
)

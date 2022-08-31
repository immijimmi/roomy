from setuptools import setup

with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="roomy",
    packages=[
        "roomy",
        "roomy.animations", "roomy.extensions", "roomy.handlers",
        "roomy.hitboxes", "roomy.roomoccupants", "roomy.screens",
        "roomy.extensions.entity"
    ],
    version="0.2.0",
    license="MIT",
    description="A game engine specialised for building 2D non-scrolling games, written in python",
    long_description_content_type="text/markdown",
    long_description=long_description,
    author="immijimmi",
    author_email="imranhamid99@msn.com",
    url="https://github.com/immijimmi/roomy",
    download_url="https://github.com/immijimmi/roomy/archive/refs/tags/v0.2.0.tar.gz",
    keywords=["game", "engine", "2D"],
    install_requires=[
        "pygame~=2.0.1",
        "managedstate~=2.1.0",
        "recurfaces~=1.0.4",
        "objectextensions~=1.2.1"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: pygame",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8"
    ],
)

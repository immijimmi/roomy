from setuptools import setup

with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="roomy",
    packages=[
        "roomy",
        "roomy.animations",
        "roomy.extensions", "roomy.extensions.renderable",
        "roomy.handlers", "roomy.hitboxes",
        "roomy.renderables", "roomy.renderables.screens",
        "roomy.stats"
    ],
    version="0.10.0",
    license="MIT",
    description="A game engine specialised for building 2D non-scrolling games, written in python",
    long_description_content_type="text/markdown",
    long_description=long_description,
    author="immijimmi",
    author_email="immijimmi1@gmail.com",
    url="https://github.com/immijimmi/roomy",
    download_url="https://github.com/immijimmi/roomy/archive/refs/tags/v0.10.0.tar.gz",
    keywords=["game", "engine", "2D"],
    install_requires=[
        "pygame~=2.0.1",
        "managedstate~=5.0.0",
        "recurfaces~=2.1.0",
        "objectextensions~=2.0.1"
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

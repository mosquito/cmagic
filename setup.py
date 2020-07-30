import os
from importlib.machinery import SourceFileLoader

from setuptools import Extension, setup


module_name = "cmagic"
module = SourceFileLoader(
    "version", os.path.join(module_name, "version.py"),
).load_module()


setup(
    name=module_name,
    version=module.__version__,
    ext_modules=[
        Extension(
            "{}._magic".format(module_name),
            ["cmagic/_magic.c"],
            libraries=["magic"],
            extra_compile_args=[],
        ),
    ],
    include_package_data=True,
    description=module.package_info,
    long_description=open("README.rst").read(),
    license=module.package_license,
    author=module.__author__,
    author_email=module.team_email,
    package_data={
        module_name: [
            "{}/_magic.pyi".format(module_name),
            "{}/py.typed".format(module_name),
        ],
    },
    url="https://github.com/mosquito/cmagic/",
    project_urls={
        "Documentation": "https://github.com/mosquito/cmagic/",
        "Source": "https://github.com/mosquito/cmagic/",
        "Tracker": "https://github.com/mosquito/cmagic/issues",
        "Say Thanks!": "https://saythanks.io/to/me%40mosquito.su",
    },
    packages=[module_name],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Operating System :: Microsoft",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    python_requires=">=3.5.*, <4",
    extras_require={
        "develop": [
            "pytest",
            "pytest-cov",
        ],
    },
)

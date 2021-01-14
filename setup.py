import io
import os
import setuptools


name = "seqerrdemo"
description = "Sequencing Error Demonstration Library"
version = "0.1.0"
# Should be one of:
# "Development Status :: 3 - Alpha"
# "Development Status :: 4 - Beta"
# "Development Status :: 5 - Production/Stable"
release_status = "Development Status :: 3 - Alpha"
dependencies = [
    "pysam"
]
extras = {

}
python_version = ">=3.6"
urls = {

}


package_root = os.path.abspath(os.path.dirname(__file__))

readme_filename = os.path.join(package_root, "README.rst")
with io.open(readme_filename, encoding="utf-8") as readme_file:
    readme = readme_file.read()

packages = [
    "seqerrdemo"
]

setuptools.setup(
    name=name,
    version=version,
    description=description,
    long_description=readme,
    author="Robert Klein",
    author_email="b.klein345@gmail.com",
    license="Apache 2.0",
    url="",
    classifiers=[
        release_status,
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ],
    keywords="bioinformatics, sequencing errors, paired-end reads",
    packages=packages,
    install_requires=dependencies,
    python_requires=python_version,
    extras_require=extras,
    entry_points={
        "console_scripts": [
            "FindSequencingErrors=seqerrdemo.controller:main"
        ]
    },
    project_urls=urls
)

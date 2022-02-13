from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="leggo_builder",
    version="1.0.0",
    description="WSU Leggo Function Libraries",
    long_description=readme,
    author="Ivan Bojicic",
    author_email="ibojicic@gmail.com",
    license=license,
    packages=find_packages(),
    install_requires=[
        "astropy",
        "MontagePy",
        "reproject"
    ],
    # entry_points={
    #     "console_scripts": [
    #         "fitscutout        = leggo_scripts.cutout:cli",
    #     ]
    # }

)

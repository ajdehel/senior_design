import setuptools

setuptools.setup(
    name="PlumbIntelligent",
    version="1.0.0dev",
    packages=setuptools.find_packages(),
    install_requires=["paho-mqtt", "pypyodbc"],
    entry_points={
        "console_scripts": [
            "plumbintel = plumbintel.__main__:main"
        ],
    },
)

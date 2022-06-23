from setuptools import setup, find_packages
with open('requirements.txt', 'r') as my_file:
    requirements = [x for x in my_file.readlines()]
setup(
    name='house_prediction',
    version='0.0.1',
    packages=find_packages(),
    scripts=['scripts/house_prediction_script'],
    requirements=requirements,
    package_data="": ["*.joblib"],,
    include_package_data=True,
    )
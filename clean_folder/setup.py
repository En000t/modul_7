from setuptools import setup, find_packages

setup(
    name='clean_folder',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'clean-folder = clean_folder.clean:main'
        ]
    },
    install_requires=[],
    author='Enot',
    author_email='chernovartem522@gmail.com',
    description='Інструмент для очищення та організації папок',
    license='MIT',
    keywords='папка очищення організація',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

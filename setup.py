import setuptools

with open('DESCRIPTION.txt') as file: 
    long_description = file.read()

REQUIREMENTS = ['pillow']

CLASSIFIERS = [ 
    'Development Status :: 1.0 - Beta', 
    'Intended Audience :: Developers', 
    'Topic :: Internet', 
    'License :: OSI Approved :: MIT License', 
    'Programming Language :: Python', 
    'Programming Language :: Python :: 3', 
    'Programming Language :: Python :: 3.3', 
    'Programming Language :: Python :: 3.4', 
    'Programming Language :: Python :: 3.5', 
    ]

setuptools.setup(name='CGM', 
      version='1.0.0', 
      description='This is a bulk certificate generator / Mailer package', 
      long_description=long_description, 
      url='https://github.com/saran-surya/CGM', 
      author='Saran Surya Ravichandran', 
      author_email='saransurya199@gmail.com', 
      license='MIT', 
      packages=setuptools.find_packages(), 
      classifiers=CLASSIFIERS, 
      install_requires=REQUIREMENTS, 
      keywords='emails certificates bulk e-certificates'
      )
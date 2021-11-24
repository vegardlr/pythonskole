
from distutils.core import setup

setup(
  name = 'pythonskole',         # How you named your package folder (MyLib)
  packages = ['pythonskole'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='gpl-3.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Codes to do fun educational stuff in Python',   # Give a short description about your library
  author = 'Vegard Lundby Rekaa',                   # Type in your name
  author_email = 'vegard@pythonskole.no',      # Type in your E-Mail
  url = 'https://github.com/vegardlr/pythonskole',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/vegardlr/pythonskole/archive/refs/tags/v0.1.tar.gz',    # I explain this later on
  keywords = ['Pythonskole', 'Undervisning', 'Koding','Python','Programmering','Læring'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'matplotlib',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.8',
  ],
)

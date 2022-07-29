
from distutils.core import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

version = '1.2'

setup(
  name = 'pythonskole',         # How you named your package folder (MyLib)
  packages = ['pythonskole'],   # Chose the same as "name"
  version = version,      # Start with a small number and increase it with every change you make
  license='gpl-3.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Koder til bruk i undervisning i Python',   # Give a short description about your library
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Vegard Lundby Rekaa',                   # Type in your name
  author_email = 'vegard@pythonskole.no',      # Type in your E-Mail
  url = 'https://github.com/vegardlr/pythonskole',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/vegardlr/pythonskole/archive/refs/tags/v'+version+'.tar.gz',    # I explain this later on
  keywords = ['Pythonskole', 'Undervisning', 'Koding','Python','Programmering','Læring'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'sys',
          'numpy',
          'matplotlib',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Education',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.8',
  ],
)

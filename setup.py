from distutils.core import setup
setup(
  name = 'ScrapyProxyCompat',
  packages = ['ScrapyProxyCompat'],
  version = '0.1',
  license='MIT',
  description = 'A module to wrap PProxy and allow more proxy options in Scrapy',
  author = 'Eli Hopkins',
  author_email = 'ewh3157@rit.edu',
  url = 'https://github.com/elihopk/ScrapyProxyCompat',
  download_url = 'https://github.com/elihopk/ScrapyProxyCompat/archive/v_01.tar.gz',
  keywords = ['Scrapy', 'Proxy'],
  install_requires=[
          'scrapy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)
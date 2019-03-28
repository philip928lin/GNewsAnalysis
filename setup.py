from setuptools import setup

setup(name='GNewsAnalysis',
      version='1.0.1',
      description='Search News with Google News Search Engine and Jiaba nlp analysis.',
      url='',
      author='Chung-Yi Lin',
      author_email='philip928lin@gmail.com',
      license='MIT',
      packages=['GNewsAnalysis'],
      install_requires=['requests', 'bs4', 'html5lib', 'tqdm', 'pandas', 
			'newspaper3k', 'matplotlib', 'wordcloud', 'jieba'],
      include_package_data = True,
      zip_safe=False)

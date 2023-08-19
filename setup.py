from distutils.core import setup

setup(
      name='prayer-time-notifier',
      version='1.0',
      description='This app serves as notifier for the 5 times prayers for Muslims',
      author='Mohamed',
      author_email='mohamed.ea.der@gmail.com',
      url='https://github.com/medea-learner/prayer-time-notifier',
      packages=[
            'distutils', 'distutils.command',
            'PyQt6', 'requests', 'schedule',
            'pygame'
      ],
)

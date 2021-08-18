from setuptools import setup, find_packages

setup(
    name='LabOrchestratorFlaskSQLAlchemyAdapter',
    version='0.0.0',
    packages=find_packages(),
    url='https://github.com/LabOrchestrator/LabOrchestratorLib-FlaskSQLAlchemyAdapter',
    license='MPL',
    author='Marco Schlicht',
    author_email='git@privacymail.dev',
    description='An adapter to use the lab orchestrator lib in flask-sqlalchemy projects.',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent"
    ],
)


import click
import kurator as k

# -*- coding: utf-8 -*-
"""Example Google style docstrings.

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
@click.group()
def cli():
    """ Performs operations on a photo library """
    pass

@click.command()
@click.argument('source', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.argument('library', type=click.Path(exists=True, file_okay=False, dir_okay=True))
def import_media(source, library):
    """ Imports media from source into library """
    k.import_media(source, library)


@click.command()
@click.argument('target', type=click.Path(exists=True, file_okay=False, dir_okay=True))
def prune(target):
    """Removes duplicate files from the target"""
    k.prune(target)

@click.command()
@click.argument('target', type=click.Path(exists=True, file_okay=False, dir_okay=True))
def fix_names(target):
    """ Checks that the name of the file_item matches the exif data
    contained in the file_item
    """
    k.fix_names(target)

@click.command()
@click.argument('library', type=click.Path(exists=True, file_okay=False, dir_okay=True))
def update_database(library):
    """ Syncs the database with the library """
    k.update_database(library)

def main():
    cli.add_command(import_media)
    cli.add_command(prune)
    cli.add_command(fix_names)
    cli.add_command(update_database)
    cli()

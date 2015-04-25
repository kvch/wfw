import click
from wfw.wfexceptions import (InvalidTagFormatException,
                              LocalChangePostingError,
                              LoginFailedException,
                              NodeNotFoundError)
from wfw.lib import fetch_list, export_list, print_list, search_tags, search_nodes, add_item, remove_item

@click.group()
def cli():
    pass

@cli.command()
def fetch():
    """Fetch list from WorkFlowy server"""

    try:
        fetch_list()
    except LoginFailedException:
        click.echo("Unable to fetch your list: wrong e-mail or password.")
    except IOError:
        click.echo("Error while fetching: missing config")


@cli.command()
@click.argument('file-name', default='tree.exported')
def export(file_name):
    """Export your list"""

    try:
        export_list(file_name)
    except IOError:
        click.echo("You have no local tree")
    except Exception as ex:
        click.echo("Error while exporting: {msg}".format(msg=ex.message))


@cli.command()
@click.argument('level', default=1)
@click.option('--root', default=None)
def show(level, root):
    """Print your list"""

    try:
        print_list(level, root)
    except IOError:
        click.echo("You have no local tree")
    except NodeNotFoundError:
        click.echo("No such node")
    except Exception as ex:
        click.echo("Error while printing list: {msg}".format(msg=ex.message))


@cli.command()
@click.argument('pattern')
def find(pattern):
    """Find items using pattern matching"""

    try:
        search_nodes(pattern)
    except IOError:
        click.echo("You have no local tree")
    except Exception as ex:
        click.echo("Error while printing list: {msg}".format(msg=ex.message))


@cli.command()
@click.argument('parent-item')
@click.argument('new-item')
def add(parent_item, new_item):
    """Add new item to list"""

    try:
        add_item(parent_item, new_item)
    except LocalChangePostingError:
        click.echo("Error while posting your change")
    except Exception as ex:
        click.echo("Error while adding new item: {msg}".format(msg=ex.message))


@cli.command()
@click.argument('parent-item')
@click.argument('deleted-item')
def rm(parent_item, deleted_item):
    """Remove item from list"""

    try:
        remove_item(parent_item, deleted_item)
    except LocalChangePostingError:
        click.echo("Error while posting your change")
    except Exception as ex:
        click.echo("Error while removing item: {msg}".format(msg=ex.message))


@cli.command()
@click.argument('tag-to-find')
def tag(tag_to_find):
    """Find items containing the given tag"""

    try:
        search_tags(tag_to_find)
    except IOError:
        click.echo("You have no local tree")
    except InvalidTagFormatException as ex:
        click.echo("Invalid tag format: {msg}".format(msg=ex.message))
    except Exception as ex:
        click.echo("Error while searching tag: {msg}".format(msg=ex.message))

import click
from wfw.wfexceptions import LoginFailedException
from wfw.lib import fetch_list, export_list, print_list, search_tags

@click.group()
def cli():
    pass

@cli.command()
@click.option('--email', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def fetch(email, password):
    """Fetch list from WorkFlowy server"""

    try:
        fetch_list(email, password)
    except LoginFailedException:
        click.echo("Unable to fetch your list: wrong e-mail or password.")


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
    except Exception as ex:
        click.echo("Error while printing list: {msg}".format(msg=ex.message))


@cli.command()
@click.argument('tag-to-find')
def tag(tag_to_find):
    """Find items containing the given tag"""

    try:
        search_tags(tag_to_find)
    except IOError:
        click.echo("You have no local tree")
    except Exception as ex:
        click.echo("Error while searching tag: {msg}".format(msg=ex.message))

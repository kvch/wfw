import click
from wfw.wfexceptions import LoginFailedException
from wfw.lib import WorkFlowy

pass_workflowy = click.make_pass_decorator(WorkFlowy, True)

@click.group()
@click.pass_context
def cli(context):
    context.workflowy = WorkFlowy()


@cli.command()
@click.option('--email', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
@pass_workflowy
def sync(workflowy, email, password):
    """Fetch list from WorkFlowy server"""

    try:
        workflowy.get_list(email, password)
    except LoginFailedException:
        click.echo("Unable to fetch your list: wrong e-mail or password.")


@cli.command()
@click.argument('file-name', default='tree.exported')
@pass_workflowy
def export(workflowy, file_name):
    """Export your list"""

    workflowy.export_list(file_name)


@cli.command()
@click.argument('level', default=1)
@click.option('--root', default=None)
@pass_workflowy
def show(workflowy, level, root):
    """Print your list"""

    workflowy.print_list(level, root)


@cli.command()
@click.argument('tag-to-find')
@pass_workflowy
def tag(workflowy, tag_to_find):
    """Find items containing the given tag"""

    workflowy.search_tags(tag_to_find)

@cli.command()
@click.argument('name')
@click.argument('parent')
@pass_workflowy
def add(workflowy, name, parent):
    """Add item to list"""

    workflowy.add_item(name, parent)

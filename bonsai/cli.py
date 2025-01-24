import click
from bonsai import commands

@click.group()
def cli():
    pass


cli.add_command(commands.tree)
cli.add_command(commands.relative)
cli.add_command(commands.json_tree)
cli.add_command(commands.save_tree)
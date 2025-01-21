import click
from bonsai.core import generate_directory_tree, visualize_tree, get_relative_path


@click.command()
@click.argument('directory_path', type=click.Path(exists=True))
def tree(directory_path):
    generated_tree_structure = generate_directory_tree(directory_path)
    click.echo(visualize_tree(generated_tree_structure))

@click.command()
@click.argument('destination_path', type=click.Path(exists=True))
@click.argument('base_path', type=click.Path(exists=True))
def relative(destination_path, base_path):
    click.echo(get_relative_path(destination_path, base_path))
import click
from bonsai.core import generate_directory_tree, visualize_tree


@click.command()
@click.argument('directory_path', type=click.Path(exists=True))
def tree(directory_path):
    generated_tree_structure = generate_directory_tree(directory_path)
    click.echo(visualize_tree(generated_tree_structure))
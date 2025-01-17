import os
import click

@click.command()
@click.argument('target_path', type=click.Path(exists=True))
@click.argument('start_path', required=False, type=click.Path(exists=True))
def print_relative_path(target_path, start_path=None):
    """
    Prints the relative path to the TARGET_PATH from the START_PATH.
    If START_PATH is not provided, the current working directory is used.
    """
    start_path = start_path or os.getcwd()
    
    try:
        relative_path = os.path.relpath(target_path, start_path)
        click.echo(f"Relative path: {relative_path}")
    except Exception as e:
        click.echo(f"Error: {e}")

if __name__ == "__main__":
    print_relative_path()

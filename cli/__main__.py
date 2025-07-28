import anyio

import click

from cli.ioc_container import container
from cli.commands import create_records, clear_records


@click.group()
def cli():
    pass


@click.command(name="seed")
def seed():
    anyio.run(create_records, container)


@click.command(name="clear")
def clear():
    anyio.run(clear_records, container)


cli.add_command(seed)
cli.add_command(clear)

if __name__ == "__main__":
    cli()

import anyio

import click

from cli.ioc_container import container
from cli.faker_utils import create_records


@click.command()
def seed():
    anyio.run(create_records, container)


if __name__ == "__main__":
    seed()

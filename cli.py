import asyncio

import typer

from app.database import init_models

cli = typer.Typer()


@cli.command()
def db_init_models():
    asyncio.run(init_models())


if __name__ == '__main__':
    cli()

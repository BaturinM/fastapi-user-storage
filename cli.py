import asyncio

import typer

from app.database import init_models

app = typer.Typer()


@app.command()
def hello():
    asyncio.run(init_models())


if __name__ == '__main__':
    app()

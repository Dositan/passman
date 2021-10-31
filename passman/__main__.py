import typer

from passman import log, quick, setup_func

CONFIG_PATH = "./data/config.json"

app = typer.Typer(no_args_is_help=True)
app.add_typer(log.app)
app.add_typer(quick.app)


@app.command()
def setup(show_credits: bool = False) -> None:
    """Set up a new account (or replace the previous one)"""
    setup_func(show_credits)


if __name__ == "__main__":
    app()

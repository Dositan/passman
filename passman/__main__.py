import typer

from passman import setup_func
from passman.commands import log, quick

app = typer.Typer(no_args_is_help=True)
app.add_typer(log.app)
app.add_typer(quick.app)


@app.command()
def setup(
    show_credits: bool = typer.Option(False, help="Show login details after setup")
) -> None:
    """Set up a new account (or replace the previous one)"""
    setup_func(show_credits=show_credits)


if __name__ == "__main__":
    app()

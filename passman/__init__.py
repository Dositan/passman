"""
Passman
=======
A quite powerful password manager for those who love terminals.
"""
import json
import os.path

import typer

__version__ = "1.0.1"


CONFIG_PATH = "./data/config.json"
first_time = not os.path.isfile(CONFIG_PATH)


def setup_func(*, show_credits: bool):
    name = input("Alright, what name you would like to set? ")
    password = input("What about password? ")

    with open(CONFIG_PATH, "w") as fp:
        json.dump({"name": name, "password": password}, fp, indent=4)

    typer.secho("✅ Setup process ended successfully.", fg="green")
    if show_credits is True:
        typer.echo(f"Username: {name} | Password: {password}")


if first_time:
    typer.secho("You seem to be using passman for the first time", fg="yellow")
    setup_func(show_credits=True)
    typer.echo("=" * 45)

with open(CONFIG_PATH, "r") as fp:
    config = json.load(fp)

"""Here we got commands with custom callback"""

from pathlib import Path

import bcrypt
import typer
from passman import config
from passman.database import DatabaseManager
from passman.utils import TabulateData

db = DatabaseManager()


def callback() -> None:
    typer.secho("⚠️  This command requires logging in first.", fg="yellow")
    name = typer.prompt("Name")
    password = typer.prompt("Password", hide_input=True)

    check = bcrypt.checkpw(password.encode("utf-8"), config["password"].encode("utf-8"))
    if name == config["name"] and check:
        return True

    typer.secho("❌ Wrong owner credits were entered, exiting...", fg="red")
    raise typer.Exit()


# All commmands below should require logging in first.
# we achieve this by overriding the default callback
app = typer.Typer(
    name="log",
    callback=callback,
    no_args_is_help=True,
    help="A set of commands that require logging in before work"
)


@app.command(name="save")
def save_password(network: str, email: str, content: str) -> None:
    """saves user data (network, email, password)"""
    db.add(network, email, content)
    typer.secho("✅ Inserted the data successfully.", fg="green")


@app.command(name="delete")
def delete_password(
    row_id: str = typer.Argument(..., help="Row ID of the user data you want to delete")
) -> None:
    """delete a row of user data depending on what ID you provide"""
    db.remove(row_id)
    typer.secho(f"✅ Deleted password #{row_id} successfully.")


def return_data() -> None:
    table = TabulateData()
    table.set_columns(["id", "network", "email", "content", "saved_at"])

    results = db.push("SELECT * FROM passwords;").fetchall()
    table.set_rows(results)

    return table.render()


@app.command()
def show() -> None:
    """shows user data in a pretty-formatted table"""
    typer.echo(return_data())


@app.command(name="export")
def export_data(path: str) -> None:
    """extracts all the user data into `passwords.txt` file"""
    try:
        with open(f"{Path.home()}/{path}/passwords.txt", "w") as f:
            f.write(return_data())
        typer.secho("✅ Exported all of your passwords successfully.", fg="green")
    except FileNotFoundError as e:
        typer.secho(f"❌ Something went wrong: {e}", fg="red")

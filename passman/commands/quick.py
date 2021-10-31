import random
import re
import string

import typer

app = typer.Typer(
    name="quick",
    no_args_is_help=True,
    help="A set of commands that do not need logging in"
)


@app.command(name="genpass")
def generate_password(
    length: int = typer.Argument(8, help="specify length for the password"),
    numbers: bool = typer.Option(False, help="include numbers"),
    uppercase: bool = typer.Option(False, help="include uppercase characters"),
    special_characters: bool = typer.Option(False, help="include special characters")
) -> None:
    """generates passwords for given parameters"""
    BASE = string.ascii_lowercase
    if numbers:
        BASE += string.digits
    if uppercase:
        BASE += string.ascii_uppercase
    if special_characters:
        BASE += string.punctuation

    result = random.choices(BASE, k=length)
    typer.echo("".join(result))


@app.command(name="strength")
def check_password(
    password: str = typer.Argument(..., help="a password you need to check")
) -> None:
    """checks password strength"""
    pattern = re.compile(r"((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,30})")
    if pattern.match(password):
        return typer.secho("✅ The password is valid.", fg="green")

    typer.secho(f"❌ This password ({password}) is weak.", fg="red")

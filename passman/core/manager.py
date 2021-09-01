# stdlibs
import json
import logging
import random
import re
from pathlib import Path
from typing import Dict, Tuple

# local code
from .database import DatabaseManager
from .errors import NotOwner, WrongChoice
from .utils import TabulateData

__all__ = ("PasswordManager",)
log = logging.getLogger("passman.manager")

CONFIG_PATH = "./passman/data/config.json"
DASH_LINE = "-" * 40
MENU_INFO = """
    Welcome to the passman menu.
Currently-supported features:
1. Generate the password.
2. Save the password.
3. Check the password strength.
4. Show all the data stored in the database.
5. Export all of your passwords.
"""


def sinput(message: str) -> str:
    """This avoids extra spaces in the user-input that may cause some issues.

    Parameters
    ----------
    message : str
        The message content to get the input by.

    Returns
    -------
    str
        Stripped user-input content.
    """
    return input(message).strip()


def convert_choice(choice: str.lower) -> bool:
    """The way of figuring out the user choice.

    Parameters
    ----------
    choice : str.lower
        User-input to calculate the choice from.

    Returns
    -------
    bool
        Either True or False, according to the convertation.

    Raises
    ------
    WrongChoice
        When the user provides an unexpected choice.
    """
    if choice in ("y", "yes", "+"):
        return True
    elif choice in ("n", "no", "-"):
        return False
    # Consider anything else as the attempt to crash the program.
    raise WrongChoice('Wrong choice provided, choose from "y/n"')


def keep_living(func):
    """This makes endless loops for methods that have sense being used with a loop."""

    def inner(*args, **kwargs):
        func(*args, **kwargs)
        print(DASH_LINE)

        while convert_choice(sinput("📢 Do you want to repeat (y/n)? ")):
            func(*args, **kwargs)
            print(DASH_LINE)

    return inner


class PasswordManager(DatabaseManager):
    """The Password Manager class to manipulate with generating passwords."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Important instances.
        with open(CONFIG_PATH, "r") as fp:
            self.config = json.load(fp)

    @keep_living
    def check_password(self) -> None:
        """This makes the user sure about their password strength.

        Planned to be used everywhere the password was entered.
        """
        pattern = re.compile(r"((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,30})")
        password = sinput("Enter the password that should be checked: ")
        if pattern.match(password):
            return print("✅ The password is valid.")

        print(f"This password ({password}) looks kind of weak.")

    def check_config(self) -> bool:
        """This manipulates with the configuration file before the program menu opens.

        Returns
        -------
        bool
            The check result.
        """
        # It is useful when the user did not provide their credits to log
        # in and this function exactly catches those moments.
        if not self.config:
            log.warning("Hey, looks like you did not set up your configuration yet")
            choice = convert_choice(sinput("but would you want to (y/n)? "))
            if choice:  # Checking for the "True" case.
                self.setup()

                # The setup process was already finished.
                log.info(
                    "You are ready to go, run the program again and explore the features."
                )
                return True  # At this point, the config will exist.
        return False

    def reset_config(self) -> None:
        """Helper method for the flag "--reset-config" to clear config consequently."""

        with open(CONFIG_PATH, "w") as fp:
            # That is simply how we are going to reset the config.
            # This also avoids all possible errors, but anyways
            # we got to check for errors by doing try/catch.
            json.dump({}, fp)
        try:
            log.info("Reset the user configuration successfully.")
        except Exception as e:
            log.error(f"Unexpected error occured: {e}")

    def setup(self) -> None:
        """The setup method called by --setup flag."""
        log.info("Setup process has been started.")
        name = sinput("What name you would like to set? ")
        password = sinput("What about password? ")

        with open(CONFIG_PATH, "w") as fp:
            json.dump({"name": name, "password": password}, fp, indent=4)

        log.info("Setup process was finished successfully.")
        log.info(f"Current username: {name}")
        log.info(f"Current password: {password}")

    def menu(self):
        """The main menu: should be called when the app gets no flags."""
        methods = (
            self.generate_password,
            self.save_password,
            self.check_password,
            self.show_data,
            self.export_data,
        )
        # Menu stuff.
        print(MENU_INFO)
        print(DASH_LINE)
        try:
            # Asking the user to choose one of the features.
            option = int(input("What option would you choose? "))
            return methods[option - 1]()  # Consequently calling the method.

        except (ValueError, TypeError, IndexError) as e:
            log.error(e)

    def show_data(self):
        """This visualize the user data, i.e. formats in a pretty-formatted table."""
        table = TabulateData()
        table.set_columns(["network", "email", "password"])

        results = self.push("SELECT * FROM passwords;").fetchall()
        table.set_rows(results)

        print(table.render())

    def export_data(self) -> str:
        """This extracts all of the user data into the `passwords.txt` file."""
        path = sinput(
            "Enter the path you would like to save your data in.\n"
            "For example, Desktop/main: "
        )

        try:
            with open(f"{Path.home()}/{path}/passwords.txt", "w") as f:
                f.write(self.show_data())
            log.info("Exported all of your passwords successfully.")
        except FileNotFoundError as e:
            log.error(f"Something went wrong: {e}")

    @staticmethod
    def _get_params(message: str, options: Tuple[str]) -> Dict[str, str]:
        """The interactive way to get kwargs that gets passed in `generate_password`.

        Parameters
        ----------
        message : str
            Message sample to get user-inputs with.
        options : Tuple[str]
            A tuple of options to provide our user.

        Returns
        -------
        Dict[str, str]
            A dictionary of necessary keys.
        """
        inputs = {option: sinput(message.format(option)) for option in options}
        print(DASH_LINE)
        return inputs

    @staticmethod
    def _true_false_only(message: str, options: Tuple[str]):
        """Does the same stuff as _get_params, but is limited in arguments choice.

        Here (y|yes|+) are considered as True, anything else as False.
        """
        inputs = {
            option: convert_choice(sinput(message.format(option))) for option in options
        }
        print(DASH_LINE)
        return inputs

    @keep_living
    def generate_password(self, **kwargs) -> str:
        """This function is created to generate passwords of the given length."""
        BASE = "qwertyuiopasdfghjklzxcvbnm"
        NUMBERS = "1234567890"
        UPPERCASE = "QWERTYUIOPASDFGHJKLZXCVBNM"
        SPECIAL = "!@#$%^&*()"

        options = ("numbers", "uppercase", "special characters")

        length = int(input("Enter the length: "))
        kwargs = kwargs or self._true_false_only("Enter the {} option: ", options)

        if kwargs.pop("numbers"):
            BASE += NUMBERS
        if kwargs.pop("uppercase"):
            BASE += UPPERCASE
        if kwargs.pop("special characters"):
            BASE += SPECIAL

        result = random.choices(BASE, k=length)
        print("".join(result))

    @keep_living
    def save_password(self, **kwargs) -> str:
        """This saves passwords according to the given credits."""
        options = ("network", "email", "content")
        kwargs = kwargs or self._get_params("Enter the {} credits: ", options)

        self.add(**kwargs)  # i.e saving the account.
        log.info("✅ Inserted the data successfully.")

    def check_owner(self) -> bool:
        """This is the method to check the correct owner beforehand.

        Raises:
            NotOwner: If the given credits did not match.

        Returns:
            bool: True, if the user passes owner check.
        """
        log.info("Login process has been started.")
        name = sinput("Enter your name: ")
        password = sinput("Enter your password: ")

        if name == self.config["name"] and password == self.config["password"]:
            print(f"Welcome back, {name}!\n{DASH_LINE}")
            return True

        raise NotOwner("Wrong owner credits were entered, exiting...")

"""
================================================================================
Author:      Twyla Washington
Course:      Security Scripting with Python
Assignment:  Registry Storage Script
Date:        27/9/26
Description: Prompts the user for a value and stores it in the Windows
             registry under HKCU\Software\RegistryStoreDemo. Also stores
             the current date/time and a REG_MULTI_SZ value containing a
             directory listing of the current working directory.
================================================================================
"""

import os
import sys
from datetime import datetime

try:
    import winreg  # Windows-only module for registry access
except ImportError:
    sys.exit("Error: This script must be run on Windows (winreg is unavailable).")


# ----------------------------------------------------------------------------
# Registry location constants (self-documenting names)
# ----------------------------------------------------------------------------
REGISTRY_ROOT_KEY = winreg.HKEY_CURRENT_USER
REGISTRY_SUBKEY_PATH = r"Software\RegistryStoreDemo"
VALUE_NAME_USER_INPUT = "UserProvidedValue"
VALUE_NAME_TIMESTAMP = "EntryCreatedAt"
VALUE_NAME_DIRECTORY_LISTING = "CurrentDirectoryListing"


def get_directory_listing_multi_sz(directory_path):
    """
    Return the contents of the given directory as a list of strings,
    suitable for storage as a REG_MULTI_SZ registry value.

    Parameters:
        directory_path (str): Path of the directory to list.

    Returns:
        list[str]: Filenames/subdirectory names found in the directory.
                   An empty list is returned if the directory is empty.
    """
    try:
        return os.listdir(directory_path)
    except OSError as error:
        print(f"Warning: could not list directory '{directory_path}': {error}")
        return []


def store_value_in_registry(key_handle, value_name, value_data, value_type):
    """
    Write a single named value into an already-open registry key.

    Parameters:
        key_handle (PyHKEY): Open handle to the target registry key.
        value_name (str):    Name of the registry value to create/update.
        value_data:          The data to store (type must match value_type).
        value_type (int):    Registry type constant, e.g. winreg.REG_SZ
                             or winreg.REG_MULTI_SZ.
    """
    winreg.SetValueEx(key_handle, value_name, 0, value_type, value_data)


def main():
    """
    Main program flow: gather data from the user and the environment,
    then persist it in the Windows registry.
    """
    # 1. Collect the value supplied by the user.
    user_supplied_value = input("Enter a value to store in the registry: ")

    # 2. Record the exact date and time the entry is being created.
    current_timestamp = datetime.now().isoformat(timespec="seconds")

    # 3. Build a directory listing of the current working directory.
    current_working_directory = os.getcwd()
    directory_entries = get_directory_listing_multi_sz(current_working_directory)

    print(f"Writing registry values under {REGISTRY_SUBKEY_PATH} ...")

    # Create the key (or open it if it already exists) and write the values.
    with winreg.CreateKey(REGISTRY_ROOT_KEY, REGISTRY_SUBKEY_PATH) as registry_key_handle:
        store_value_in_registry(
            registry_key_handle,
            VALUE_NAME_USER_INPUT,
            user_supplied_value,
            winreg.REG_SZ,
        )
        store_value_in_registry(
            registry_key_handle,
            VALUE_NAME_TIMESTAMP,
            current_timestamp,
            winreg.REG_SZ,
        )
        store_value_in_registry(
            registry_key_handle,
            VALUE_NAME_DIRECTORY_LISTING,
            directory_entries,
            winreg.REG_MULTI_SZ,
        )

    print("Done. Verify with: reg query HKCU\\Software\\RegistryStoreDemo")


if __name__ == "__main__":
    main()

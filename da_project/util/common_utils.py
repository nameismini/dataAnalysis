"""
Project Name: dataAnalysis
File Name: common_utils.py.py
Author: MKIM
Created Date: 2024-08-07
Description: 
"""

import os
import datetime
import logging


class CommonUtils:
    """
    A collection of common utility functions.
    """

    @staticmethod
    def string_to_int(s: str) -> int:
        """
        Converts a string to an integer.

        Parameters:
        s (str): The string to convert.

        Returns:
        int: The converted integer, or None if conversion fails.
        """
        try:
            return int(s)
        except ValueError:
            logging.error(f"Cannot convert {s} to int.")
            return None

    @staticmethod
    def current_datetime_str(format: str = "%Y-%m-%d %H:%M:%S") -> str:
        """
        Returns the current date and time as a string.

        Parameters:
        format (str): The format of the date and time string. Default is "%Y-%m-%d %H:%M:%S".

        Returns:
        str: The formatted date and time string.
        """
        return datetime.datetime.now().strftime(format)

    @staticmethod
    def read_file(file_path: str) -> str:
        """
        Reads the content of a file.

        Parameters:
        file_path (str): The path to the file to read.

        Returns:
        str: The content of the file.
        """
        if not os.path.exists(file_path):
            logging.error(f"File {file_path} does not exist.")
            return None
        with open(file_path, 'r') as file:
            return file.read()

    @staticmethod
    def write_file(file_path: str, content: str) -> None:
        """
        Writes content to a file.

        Parameters:
        file_path (str): The path to the file to write to.
        content (str): The content to write to the file.
        """
        with open(file_path, 'w') as file:
            file.write(content)
        logging.info(f"Content written to {file_path}")

    @staticmethod
    def list_files(directory: str) -> list:
        """
        Lists all files in a directory.

        Parameters:
        directory (str): The directory to list files from.

        Returns:
        list: A list of file names in the directory.
        """
        if not os.path.isdir(directory):
            logging.error(f"Directory {directory} does not exist.")
            return []
        return os.listdir(directory)
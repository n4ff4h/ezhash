import typer
import hashlib
from pathlib import Path
from typing import Optional

app = typer.Typer()


# Main command
@app.command()
def main(algorithm: str, path: str, compare_with: Optional[str] = typer.Argument(None)):
    hash = Hash(algorithm, path, compare_with)  # Initialize a Hash object

    typer.secho(hash.display_progress())


class Hash():
    # Default constructor
    def __init__(self, algorithm, path, compare_with):
        self.algorithm = algorithm
        self.path = path
        self.compare_with = compare_with

    """ Function to generate and return file hash as a string """

    def generate_file_hash(self):
        if self.algorithm not in hashlib.algorithms_available:  # If the user defined algorithm is not available
            raise TypeError(f'Algorithm: {self.algorithm} not supported!')

        # Opens a file, and returns it as a file object
        with open(self.path, 'rb') as f:
            algorithm = hashlib.new(self.algorithm)
            file_size = Path(self.path).stat().st_size

            with typer.progressbar(length=file_size, label='HASHING:') as pbar:
                while True:
                    chunk = f.read(8192)
                    if not chunk:  # If no more bytes to be read
                        break
                    algorithm.update(chunk)
                    pbar.update(len(chunk))
        return algorithm.hexdigest()  # hexdigest() returns a string

    """ 
    Calls 'generate_file_hash' function and 
    displays the file hash along with 
    algorithm, path or file hash compared with
    """

    def display_progress(self):
        self.generate_file_hash()

        dictionary = (vars(self))  # Convert class properties into a dictionary

        # Iterate over the key value pairs in the dictionary and print them
        for key, value in dictionary.items():
            typer.secho(f'{key.upper()}: {value}')

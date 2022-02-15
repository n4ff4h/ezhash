import typer
import hashlib
from pathlib import Path
from typing import Optional

app = typer.Typer()


# Main command
@app.command()
def main(algorithm: str, path: str, compare_with: Optional[str] = typer.Argument(None)):
    hash = Hash(algorithm, path, compare_with)  # Initialize a Hash object

    if compare_with is None:  # If the file hash to be compared with is not defined
        typer.secho()
    else:
        typer.secho()


class Hash():
    # Default constructor
    def __init__(self, algorithm, path, compare_with):
        self.algorithm = algorithm
        self.path = path
        self.compare_with = compare_with

    # Function to generate and return file hash as a string
    def generate_file_hash(self):
        if self.algorithm in hashlib.algorithms_available:  # If the user defined algorithm is available
            # Opens a file, and returns it as a file object
            with open(self.path, 'rb') as f:
                algorithm = hashlib.new(self.algorithm)
                file_size = Path(self.path).stat().st_size

                with typer.progressbar(length=file_size) as pbar:
                    while True:
                        chunk = f.read(8192)
                        if not chunk:  # If no more bytes to be read
                            break
                        algorithm.update(chunk)
                        pbar.update(len(chunk))
            return algorithm.hexdigest()  # hexdigest() returns a string
        raise TypeError(f'Algorithm: {self.algorithm} not supported!')

    def display_progress(self):
        self.generate_file_hash()

        for i in range(self):

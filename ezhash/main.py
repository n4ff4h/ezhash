import typer
import hashlib
from pathlib import Path
from typing import Optional

app = typer.Typer()


# Main command
@app.command()
def main(algorithm: str, path: str, compare_with: Optional[str] = typer.Argument(None)):
    hash = Hash(algorithm, path)

    if compare_with is None:  # if the file hash to be compared with is not defined
        print(hash.generate_file_hash())
    else:
        print()


#
class Hash():
    def __init__(self, algorithm, path):
        self.algorithm = algorithm
        self.path = path

    def generate_file_hash(self):
        if self.algorithm in hashlib.algorithms_available:  # If the user defined algorithm is available
            with open(self.path, 'rb') as f:
                algorithm = hashlib.new(self.algorithm)
                file_size = Path(self.path).stat().st_size

                with typer.progressbar(range(file_size)) as pbar:
                    while True:
                        chunk = f.read(8192)
                        if not chunk:
                            break
                        algorithm.update(chunk)
                        pbar.update(len(chunk))
            return algorithm.hexdigest()
        raise TypeError(f'Algorithm: {algorithm} not supported!')

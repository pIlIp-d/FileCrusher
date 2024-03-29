import os
import subprocess
import sys
from subprocess import CalledProcessError

from src.file_crusher.config import PNGCRUSH_PATH
from src.file_crusher.file_operations import compare_and_use_better_option, check_if_valid_image
from src.file_crusher.processor import processor


class PNGCrushCompressor:
    def __init__(
            self,
            event_handlers=None
    ):
        """
        Compresses PNG images using pngcrush.
        :param event_handlers: (list of EventHandler) A list of event handlers. (pre and postprocessors)
        :returns: None
        """

        pngcrush_path = PNGCRUSH_PATH
        self.event_handlers = event_handlers
        if self.event_handlers is None:
            self.event_handlers = []

        if not os.path.isfile(pngcrush_path):
            linux_error = "Install it with 'sudo apt install pngcrush'." if os.name != "nt" else ""
            raise FileNotFoundError(rf"pngcrush path not found at '{pngcrush_path}'. {linux_error}")

        system_extra = "powershell.exe" if os.name == 'nt' else ""
        pngcrush_options = "-rem alla -rem text -reduce"  # -brute"
        # TODO add option brute when compression mode is high
        self.pngcrush_command = f"{system_extra} {pngcrush_path} {pngcrush_options}"

    @processor
    def process_file(self, source_file: str, destination_path: str) -> None:
        check_if_valid_image(source_file)

        try:
            subprocess.check_output(rf'{self.pngcrush_command} "{source_file}" "{source_file[:-4] + "-comp.png"}"',
                                    stderr=subprocess.STDOUT, shell=True)
            result_file = source_file[:-4] + '-comp.png'
            compare_and_use_better_option(source_file, result_file, destination_path)
            if os.path.exists(result_file):
                os.remove(result_file)
        except CalledProcessError as cpe:
            print(repr(cpe), file=sys.stderr)
            print("processing failed at the pngcrush stage. (IGNORE)\n", file=sys.stderr)
        except Exception as e:
            print(repr(e), file=sys.stderr)  # dont raise e

import os.path
import re


class CompressionPostprocessor:
    __compressor_name: str

    def __init__(self, compressor_name: str):
        self.__compressor_name = compressor_name

    def postprocess(self, source_file: str, destination_file: str) -> None:
        # page_number is the first number in the filename
        page_number = re.search(r'\d+\D', os.path.basename(source_file))
        if page_number:
            page_number = page_number[0]
            print(f"** - Compressed Page {page_number} with {self.__compressor_name}")

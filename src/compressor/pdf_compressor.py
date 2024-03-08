import asyncio
import os
import shutil
import sys
from enum import Enum
from io import TextIOWrapper

from src.batch_processor import batch_process_files_async
from src.compressor.config import TESSERACT_PATH
from src.compressor.converter.image_to_pdf_converter import ImagesToPdfConverter
from src.compressor.converter.pdf_merger import merge_pdf_files
from src.compressor.converter.pdf_to_image_converter import PdfToImageConverter
from src.compressor.cpdfsqueeze_compressor import CPdfSqueezeCompressor
from src.compressor.file_operations import get_file_size, get_files_in_folder, get_and_create_temp_folder
from src.compressor.png_compressor import PNGCompressor
from src.compressor.processor import processor


class PDFCompressor:
    Mode = Enum("Mode", ["AUTO", "LOSSLESS", "FORCE_OCR", "NO_OCR"])

    def __init__(
            self,
            compression_mode: int = 5,
            force_ocr: bool = False,
            no_ocr: bool = False,
            tesseract_language: str = "eng",
            default_pdf_dpi: int = 400,
            event_handlers=None
    ):
        self.event_handlers = event_handlers
        if event_handlers is None:
            self.event_handlers = []

        self.__tessdata_prefix = None
        self.__force_ocr = force_ocr

        # configure compressors
        try:
            # lossless compressor
            self.__cpdf_squeeze_compressor = CPdfSqueezeCompressor()
        except ValueError as error:
            self.__cpdf_squeeze_compressor = None
            print(str(error) + " -> skipping compression with cpdfsqueeze.")

        if (not no_ocr and force_ocr) and not os.path.exists(TESSERACT_PATH):
            # if tesseract is definitely necessary
            raise ValueError(
                "TESSERACT_PATH not found."
                "If force-ocr is active tesseract needs to be configured correctly."
            )
        # init lossy compressor
        self.__png_crunch_compressor = PNGCompressor(compression_mode)
        self.__image_to_pdf_converter = ImagesToPdfConverter(
            self.__force_ocr,
            no_ocr,
            tesseract_language,
        )
        self.__pdf_to_image_converter = PdfToImageConverter("png", default_pdf_dpi)

    @processor
    def process_file(self, source_file: str, destination_path: str) -> None:
        temp_folder_01 = get_and_create_temp_folder()
        temp_folder_02 = get_and_create_temp_folder()

        # create new empty folder for temporary files
        shutil.rmtree(temp_folder_01, ignore_errors=True)
        os.makedirs(temp_folder_01)

        # split pdf into images that can be compressed using crunch
        self.__pdf_to_image_converter.process_file(source_file, temp_folder_01)

        # 1. compress all images in temp_folder
        asyncio.run(
            batch_process_files_async(get_files_in_folder(temp_folder_01), temp_folder_02, self.__png_crunch_compressor)
        )

        # 2. convert pngs to pdfs (as separate pages) and optionally apply OCR
        asyncio.run(
            batch_process_files_async(get_files_in_folder(temp_folder_02), temp_folder_02,
                                      self.__image_to_pdf_converter)
        )

        # 3. merge pdf pages into pdf
        merge_pdf_files(get_files_in_folder(temp_folder_02, "*.pdf"), destination_path)

        # clean up temp folders
        shutil.rmtree(temp_folder_01, ignore_errors=True)
        shutil.rmtree(temp_folder_02, ignore_errors=True)

        # supress normal console outputs
        stdin_buffer = sys.stdin
        sys.stdin = TextIOWrapper(open(os.devnull, "w"))

        if self.__cpdf_squeeze_compressor is not None:
            # compression with cpdf
            self.__cpdf_squeeze_compressor.process_file(destination_path, destination_path)

        if not self.__force_ocr and get_file_size(source_file) < get_file_size(destination_path):
            if self.__cpdf_squeeze_compressor is not None:
                self.__cpdf_squeeze_compressor.process_file(source_file, destination_path)
            if get_file_size(source_file) < get_file_size(destination_path):
                print("File couldn't be compressed.", file=sys.stderr)
                # copy source_file to destination_file
                if not source_file == destination_path:
                    shutil.copy(source_file, destination_path)
            else:
                print(
                    "File couldn't be compressed using crunch cpdf combi. "
                    "However cpdf could compress it. -> No OCR was Created. (force ocr with option -f/--force-ocr)"
                    , file=sys.stderr
                )
        # load normal stdin from buffer
        sys.stdin = stdin_buffer

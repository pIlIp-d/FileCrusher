import os
import sys
import time

from src.file_crusher.CompressionPostprocessor import CompressionPostprocessor
from src.file_crusher.advpng_compressor import ADVPNGCompressor
from src.file_crusher.file_operations import copy_file
from src.file_crusher.pngcrush_compressor import PNGCrushCompressor
from src.file_crusher.pngquant_compressor import PNGQuantCompressor
from src.file_crusher.processor import processor


class PNGCompressor:
    def __init__(
            self,
            compression_mode: int = 3,
            event_handlers=None
    ):
        """
         Compresses PNG images using a combination of compression tools.
         :param compression_mode: Speed of compression,
            where 0 is the slowest (best quality) and 10 is the fastest.
         :param event_handlers: A list of event handlers. (pre and postprocessors)
         :returns: None
         """

        self.event_handlers = event_handlers
        if self.event_handlers is None:
            self.event_handlers = []

        if compression_mode <= 0 or compression_mode >= 6:
            raise ValueError("Compression mode must be in range 1-5")

        advcomp_iterations = None
        advcomp_shrink_rate = None
        pngquant_max_quality = None
        pngquant_min_quality = None
        pngquant_speed = None
        match compression_mode:
            case 1:
                advcomp_iterations = 3
                advcomp_shrink_rate = 4
                pngquant_max_quality = 80
                pngquant_min_quality = 0
                pngquant_speed = 1
            case 2:
                advcomp_iterations = 2
                advcomp_shrink_rate = 3
                pngquant_max_quality = 85
                pngquant_min_quality = 25
                pngquant_speed = 2
            case 3:
                advcomp_iterations = 2
                advcomp_shrink_rate = 2
                pngquant_max_quality = 85
                pngquant_min_quality = 25
                pngquant_speed = 2
            case 4:
                advcomp_iterations = 1
                advcomp_shrink_rate = 2
                pngquant_max_quality = 90
                pngquant_min_quality = 25
                pngquant_speed = 8
            case 5:
                advcomp_iterations = 1
                advcomp_shrink_rate = 1
                pngquant_max_quality = 99
                pngquant_min_quality = 25
                pngquant_speed = 9

        try:
            self.__advcomp = ADVPNGCompressor(
                shrink_rate=advcomp_shrink_rate,
                iterations=advcomp_iterations,
                event_handlers=[CompressionPostprocessor("advcomp")]
            )
        except FileNotFoundError:
            print("Error: Program advcomp not found, skipped compression with advcomp.", file=sys.stderr)
            self.__advcomp = None

        try:
            self.__pngquant = PNGQuantCompressor(
                speed=pngquant_speed,
                min_quality=pngquant_min_quality,
                max_quality=pngquant_max_quality,
                event_handlers=[CompressionPostprocessor("pngquant")]
            )
        except FileNotFoundError:
            print("Error: Program pngquant not found, skipped compression with pngquant.", file=sys.stderr)
            self.__pngquant = None

        try:
            self.__pngcrush = PNGCrushCompressor(
                event_handlers=[CompressionPostprocessor("pngcrush")]
            )
        except FileNotFoundError:
            print("Error: Program pngcrush not found, skipped compression with pngcrush.", file=sys.stderr)
            self.__pngcrush = None

    @processor
    def process_file(self, source_file: str, destination_path: str) -> None:
        if os.path.isdir(destination_path):
            destination_path = os.path.join(destination_path, os.path.basename(source_file))

        current_source_file = source_file
        # run compress tools on single file
        if self.__pngquant is not None:
            new_destination = destination_path + ".pngquant.png"
            self.__pngquant.process_file(current_source_file, new_destination)
            os.remove(current_source_file)
            current_source_file = new_destination
            time.sleep(0)

        if self.__advcomp is not None:
            new_destination = destination_path + ".advcomp.png"
            self.__advcomp.process_file(current_source_file, new_destination)
            os.remove(current_source_file)
            current_source_file = new_destination
            time.sleep(0)

        if self.__pngcrush is not None:
            self.__pngcrush.process_file(current_source_file, destination_path)
            os.remove(current_source_file)
        else:
            copy_file(current_source_file, destination_path)
            os.remove(current_source_file)

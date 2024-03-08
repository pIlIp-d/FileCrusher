import os
from unittest import TestCase

from src.batch_processor import batch_process_files
from src.compressor.cpdfsqueeze_compressor import CPdfSqueezeCompressor
from src.compressor.pdf_compressor import PDFCompressor


class TestProcessor(TestCase):
    def test_cpdfsqueeze_processor(self):
        destination_file = "tmp.pdf"
        self.assertFalse(os.path.exists(destination_file))
        batch_process_files(["../../test_data/testFile.pdf"], destination_file, CPdfSqueezeCompressor())
        self.assertTrue(os.path.exists(destination_file))
        os.remove(destination_file)

    def test_pdf_crunch_processor(self):
        destination_file = "tmp.pdf"
        self.assertFalse(os.path.exists(destination_file))
        batch_process_files(["../../test_data/testFile.pdf"], destination_file, PDFCompressor())
        self.assertTrue(os.path.exists(destination_file))
        os.remove(destination_file)

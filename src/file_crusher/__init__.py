from .cpdfsqueeze_compressor import CPdfSqueezeCompressor
from .advpng_compressor import ADVPNGCompressor
from .pdf_compressor import PDFCompressor
from .png_compressor import PNGCompressor
from .pngquant_compressor import PNGQuantCompressor
from .pngcrush_compressor import PNGCrushCompressor
from .pipeline_processor import PipelineProcessor
import batch_processor

__all__ = ["CPdfSqueezeCompressor", "ADVPNGCompressor", "PDFCompressor", "PNGCompressor", "PNGQuantCompressor",
           "PNGCrushCompressor", "PipelineProcessor", "batch_processor"]

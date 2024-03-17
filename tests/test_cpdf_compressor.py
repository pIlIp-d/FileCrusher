import os
from unittest import TestCase
import file_crusher


class TestCPDFCompressor(TestCase):
    folder_url = os.path.join(os.path.dirname(__file__), "testdata")
    source_file_url = os.path.join(folder_url, "test_file.pdf")
    destination_file_url = os.path.join(folder_url, "test_file.pdf")

    def test_extra_args_empty_string(self):
        # no error
        file_crusher.CPdfSqueezeCompressor(extra_args="").process_file(self.source_file_url, self.destination_file_url)

    def test_extra_args_some_arguments(self):
        compressor = file_crusher.CPdfSqueezeCompressor(extra_args="-upw password")
        self.assertEqual(compressor.extra_args, "-upw password")

    def test_extra_args_incorrect(self):
        with self.assertRaises(ValueError):
            file_crusher.CPdfSqueezeCompressor(extra_args="incorrect")

    def test_event_handlers_none(self):
        compressor = file_crusher.CPdfSqueezeCompressor(event_handlers=None)
        self.assertIsNone(compressor.event_handlers)

    def test_event_handlers_one(self):
        compressor = file_crusher.CPdfSqueezeCompressor(event_handlers=[EventHandler()])
        self.assertEqual(len(compressor.event_handlers), 1)

    def test_event_handlers_multiple(self):
        compressor = file_crusher.CPdfSqueezeCompressor(event_handlers=[EventHandler(), AnotherEventHandler()])
        self.assertEqual(len(compressor.event_handlers), 2)

    def test_event_handlers_wrong_type(self):
        with self.assertRaises(TypeError):
            file_crusher.CPdfSqueezeCompressor(event_handlers="incorrect")

    def test_event_handlers_mix(self):
        with self.assertRaises(TypeError):
            file_crusher.CPdfSqueezeCompressor(event_handlers=[EventHandler(), "incorrect"])

    def test_process_file_file_to_file(self):
        compressor = file_crusher.CPdfSqueezeCompressor()
        source_file = self.source_file_url
        destination_path = os.path.join(self.folder_url, "compressed_file.pdf")
        compressor.process_file(source_file, destination_path)
        self.assertTrue(os.path.exists(destination_path))

    def test_process_file_file_to_folder(self):
        compressor = file_crusher.CPdfSqueezeCompressor()
        source_file = self.source_file_url
        destination_folder = self.folder_url
        compressor.process_file(source_file, destination_folder)
        compressed_file_path = os.path.join(destination_folder, os.path.basename(source_file))
        self.assertTrue(os.path.exists(compressed_file_path))

    def test_cpdf_use_wine_on_linux_is_false(self):
        raise NotImplementedError("TODO")

    def test_cpdf_use_wine_on_linux_is_true(self):
        raise NotImplementedError("TODO")

    def test_cpdf_extra_args_empty(self):
        raise NotImplementedError("TODO")

    def test_cpdf_extra_args_none(self):
        raise NotImplementedError("TODO")

    def test_cpdf_extra_args_working_command(self):
        raise NotImplementedError("TODO")

    def test_cpdf_extra_args_incorrect_command(self):
        raise NotImplementedError("TODO")

    def test_cpdf_event_handlers_none(self):
        raise NotImplementedError("TODO")

    def test_cpdf_event_handlers_one_call(self):
        raise NotImplementedError("TODO")

    def test_cpdf_event_handlers_multiple_calls(self):
        raise NotImplementedError("TODO")

    def test_cpdf_event_handlers_empty_list(self):
        raise NotImplementedError("TODO")

    def test_cpdf_event_handlers_none_of_the_methods_implemented(self):
        raise NotImplementedError("TODO")

    def test_cpdf_event_handlers_only_preprocessor_implemented(self):
        raise NotImplementedError("TODO")

    def test_cpdf_event_handlers_only_postprocessor_implemented(self):
        raise NotImplementedError("TODO")

    def test_cpdf_with_relative_source_path(self):
        raise NotImplementedError("TODO")

    def test_cpdf_with_absolute_source_path(self):
        raise NotImplementedError("TODO")

    def test_cpdf_with_source_path_none(self):
        raise NotImplementedError("TODO")

    def test_cpdf_with_source_path_empty(self):
        raise NotImplementedError("TODO")

    def test_cpdf_with_source_path_ends_with_some_text(self):
        raise NotImplementedError("TODO")

    def test_cpdf_with_source_path_wrong_file_type(self):
        raise NotImplementedError("TODO")

    def test_cpdf_with_source_path_only_file_ending(self):
        raise NotImplementedError("TODO")

    def test_cpdf_with_source_path_doesnt_exist(self):
        raise NotImplementedError("TODO")

    def test_cpdf_with_relative_path_to_output_file(self):
        raise NotImplementedError("TODO")

    def test_cpdf_with_absolute_path_to_output_file(self):
        raise NotImplementedError("TODO")

    def test_cpdf_with_relative_path_to_output_folder(self):
        raise NotImplementedError("TODO")

    def test_cpdf_with_absolute_path_to_output_folder(self):
        raise NotImplementedError("TODO")

    def test_cpdf_with_output_path_none(self):
        raise NotImplementedError("TODO")

    def test_cpdf_with_output_path_empty(self):
        raise NotImplementedError("TODO")

    def test_cpdf_with_output_path_has_no_file_ending(self):
        raise NotImplementedError("TODO")

    def test_cpdf_with_output_path_has_wrong_file_ending(self):
        raise NotImplementedError("TODO")

    def test_cpdf_with_output_path_is_only_file_ending(self):
        raise NotImplementedError("TODO")

    def test_cpdf_with_output_path_already_exists(self):
        raise NotImplementedError("TODO")

    def tearDown(self):
        # Clean up any files or folders created during testing
        pass


# "../test_data/testFile.pdf"


"""
Constructor
    use_wine_on_linux:
        True
        False

    extra_args
        ""
        None
        Something else like -upw
        incorrect one

    event_handlers
        None
        One
        Multiple
        []
        wrong type of class
        mix of wrong and correct classes

process_file:
    source_file:
    destination_path:
        file -> file
        file -> folder
        
"""

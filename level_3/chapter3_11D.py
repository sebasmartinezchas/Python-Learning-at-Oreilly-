import unittest
from unittest.mock import mock_open,patch

from chapter3_11C import FileManager

class TestFileManager(unittest.TestCase):
    def setUp(self) -> None:
        self.file_manager=FileManager("test.txt")

    @patch("builtins.open",new_callable=mock_open,read_data="file content")
    def test_read_data(self,mock_file):
        result=self.file_manager.read_data()
        self.assertEqual(result,'file content')
        mock_file.assert_called_once_with("test.txt","r")

    @patch('builtins.open',new_callable=mock_open)
    def test_write_data(self,mock_file):
        result=self.file_manager.write_data("new content")
        self.assertEqual(result,11)
        mock_file.assert_called_once_with("test.txt","w")
        mock_file().write.assert_called_once_with("new content")

    @patch("builtins.open",new_callable=mock_open,read_data="  spaces  ")
    def test_read_data_strips_whitespace(self,mock_file):
        result=self.file_manager.read_data()
        self.assertEqual(result,"spaces")

    # TODO: Add edge case tests (e.g., FileNotFoundError, empty files, encoding issues).
    
if __name__ == "__main__":
    unittest.main()

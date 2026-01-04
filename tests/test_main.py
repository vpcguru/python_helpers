import unittest
import os
import shutil
import tempfile
import time
import sys
from pathlib import Path

# Import the function to test
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from move_sort_files.main import t_or_f


class TestTOrFFunction(unittest.TestCase):
    """Test cases for the t_or_f function - positive and negative inputs"""

    # Positive test cases
    def test_true_lowercase(self):
        """Test that 'true' returns True"""
        self.assertTrue(t_or_f('true'))

    def test_true_uppercase(self):
        """Test that 'TRUE' returns True"""
        self.assertTrue(t_or_f('TRUE'))

    def test_true_mixedcase(self):
        """Test that 'TrUe' returns True"""
        self.assertTrue(t_or_f('TrUe'))

    def test_t_single_char(self):
        """Test that 't' returns True (starts with TRUE)"""
        self.assertTrue(t_or_f('t'))

    def test_tr_prefix(self):
        """Test that 'tr' returns True"""
        self.assertTrue(t_or_f('tr'))

    def test_false_lowercase(self):
        """Test that 'false' returns False"""
        self.assertFalse(t_or_f('false'))

    def test_false_uppercase(self):
        """Test that 'FALSE' returns False"""
        self.assertFalse(t_or_f('FALSE'))

    def test_false_mixedcase(self):
        """Test that 'FaLsE' returns False"""
        self.assertFalse(t_or_f('FaLsE'))

    def test_f_single_char(self):
        """Test that 'f' returns False (starts with FALSE)"""
        self.assertFalse(t_or_f('f'))

    def test_fa_prefix(self):
        """Test that 'fa' returns False"""
        self.assertFalse(t_or_f('fa'))

    # Negative test cases
    def test_invalid_string_returns_none(self):
        """Test that invalid string returns None"""
        self.assertIsNone(t_or_f('invalid'))

    def test_empty_string_returns_none(self):
        """Test that empty string returns None"""
        self.assertIsNone(t_or_f(''))

    def test_number_string_returns_none(self):
        """Test that number string returns None"""
        self.assertIsNone(t_or_f('123'))

    def test_special_chars_returns_none(self):
        """Test that special characters return None"""
        self.assertIsNone(t_or_f('@#$'))

    def test_integer_input(self):
        """Test that integer input is handled (converted to string)"""
        self.assertIsNone(t_or_f(123))

    def test_none_input(self):
        """Test that None input returns None"""
        self.assertIsNone(t_or_f(None))


class TestFileCopyOperations(unittest.TestCase):
    """Test cases for file copy operations"""

    def setUp(self):
        """Set up temporary directories for testing"""
        self.test_dir = tempfile.mkdtemp()
        self.source_dir = os.path.join(self.test_dir, 'source/')
        self.dest_dir = os.path.join(self.test_dir, 'dest/')
        os.makedirs(self.source_dir, exist_ok=True)

        # Create test files
        self.test_file1 = os.path.join(self.source_dir, 'test1.txt')
        self.test_file2 = os.path.join(self.source_dir, 'test2.txt')

        with open(self.test_file1, 'w') as f:
            f.write('Test content 1')
        with open(self.test_file2, 'w') as f:
            f.write('Test content 2')

        # Set different modification times
        old_time = time.time() - 86400  # 1 day ago
        os.utime(self.test_file1, (old_time, old_time))

    def tearDown(self):
        """Clean up temporary directories"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_copy_preserves_source_file(self):
        """Test that copy operation preserves source file"""
        dest_file = os.path.join(self.dest_dir, 'test1.txt')
        os.makedirs(self.dest_dir, exist_ok=True)

        shutil.copy2(self.test_file1, dest_file)

        self.assertTrue(os.path.exists(self.test_file1), "Source file should still exist")
        self.assertTrue(os.path.exists(dest_file), "Destination file should exist")

    def test_copy_preserves_file_attributes(self):
        """Test that copy2 preserves file metadata"""
        dest_file = os.path.join(self.dest_dir, 'test1.txt')
        os.makedirs(self.dest_dir, exist_ok=True)

        source_stat = os.stat(self.test_file1)
        shutil.copy2(self.test_file1, dest_file)
        dest_stat = os.stat(dest_file)

        self.assertAlmostEqual(source_stat.st_mtime, dest_stat.st_mtime, places=0)

    def test_move_removes_source_file(self):
        """Test that move operation removes source file"""
        dest_file = os.path.join(self.dest_dir, 'test1.txt')
        os.makedirs(self.dest_dir, exist_ok=True)

        shutil.move(self.test_file1, dest_file)

        self.assertFalse(os.path.exists(self.test_file1), "Source file should be removed")
        self.assertTrue(os.path.exists(dest_file), "Destination file should exist")

    def test_directory_creation(self):
        """Test that destination directory is created if it doesn't exist"""
        new_dir = os.path.join(self.test_dir, 'new_dest/')

        self.assertFalse(os.path.exists(new_dir))
        os.makedirs(new_dir, exist_ok=True)
        self.assertTrue(os.path.exists(new_dir))


class TestFileOperationsEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions"""

    def setUp(self):
        """Set up temporary directories for testing"""
        self.test_dir = tempfile.mkdtemp()
        self.source_dir = os.path.join(self.test_dir, 'source/')
        os.makedirs(self.source_dir, exist_ok=True)

    def tearDown(self):
        """Clean up temporary directories"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_empty_directory(self):
        """Test handling of empty source directory"""
        dir_list = os.listdir(self.source_dir)
        self.assertEqual(len(dir_list), 0, "Directory should be empty")

    def test_nonexistent_directory(self):
        """Test that accessing nonexistent directory raises error"""
        nonexistent_path = os.path.join(self.test_dir, 'nonexistent/')

        with self.assertRaises(FileNotFoundError):
            os.listdir(nonexistent_path)

    def test_file_with_special_characters(self):
        """Test handling of files with special characters in name"""
        special_file = os.path.join(self.source_dir, 'test file #1.txt')
        with open(special_file, 'w') as f:
            f.write('content')

        dir_list = os.listdir(self.source_dir)
        self.assertIn('test file #1.txt', dir_list)

    def test_path_without_trailing_slash(self):
        """Test that paths work with and without trailing slashes"""
        # Create a test file
        test_file = os.path.join(self.source_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('content')

        # Test without trailing slash
        dir_list = os.listdir(self.source_dir.rstrip('/'))
        self.assertEqual(len(dir_list), 1)

        # Test with trailing slash
        dir_list = os.listdir(self.source_dir)
        self.assertEqual(len(dir_list), 1)

    def test_overwrite_existing_file(self):
        """Test behavior when destination file already exists"""
        dest_dir = os.path.join(self.test_dir, 'dest/')
        os.makedirs(dest_dir, exist_ok=True)

        source_file = os.path.join(self.source_dir, 'test.txt')
        dest_file = os.path.join(dest_dir, 'test.txt')

        # Create source and destination files
        with open(source_file, 'w') as f:
            f.write('source content')
        with open(dest_file, 'w') as f:
            f.write('old content')

        # Copy should overwrite
        shutil.copy2(source_file, dest_file)

        with open(dest_file, 'r') as f:
            content = f.read()

        self.assertEqual(content, 'source content')

    def test_permission_error_simulation(self):
        """Test handling of permission errors (conceptual test)"""
        # Note: This test demonstrates the concept but may not work on all systems
        # In production, you would mock file operations to test error handling
        restricted_dir = os.path.join(self.test_dir, 'restricted/')
        os.makedirs(restricted_dir, exist_ok=True)

        # Create a file
        test_file = os.path.join(restricted_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('content')

        # Make directory read-only (Unix-like systems)
        if sys.platform != 'win32':
            try:
                os.chmod(restricted_dir, 0o444)

                # Try to create a file in read-only directory
                new_file = os.path.join(restricted_dir, 'new.txt')
                with self.assertRaises(PermissionError):
                    with open(new_file, 'w') as f:
                        f.write('new content')
            finally:
                # Restore permissions for cleanup
                os.chmod(restricted_dir, 0o755)


class TestTimestampFormatting(unittest.TestCase):
    """Test timestamp formatting for different platforms"""

    def test_timestamp_format_unix(self):
        """Test that Unix timestamp format uses forward slashes"""
        m_time = time.ctime(time.time())
        t_obj = time.strptime(m_time)

        if sys.platform != 'win32':
            T_stamp = time.strftime("%Y_%m_%d", t_obj)
            self.assertIn('_', T_stamp)

    def test_timestamp_format_windows(self):
        """Test that Windows timestamp format works correctly"""
        m_time = time.ctime(time.time())
        t_obj = time.strptime(m_time)

        T_stamp = time.strftime("%Y_%m_%d", t_obj)
        self.assertIn('_', T_stamp)

    def test_timestamp_year_format(self):
        """Test that timestamp includes 4-digit year"""
        m_time = time.ctime(time.time())
        t_obj = time.strptime(m_time)
        T_stamp = time.strftime("%Y_%m_%d", t_obj)

        # Check format: YYYY_MM_DD
        parts = T_stamp.split('_')
        self.assertEqual(len(parts), 3)
        self.assertEqual(len(parts[0]), 4)  # Year should be 4 digits
        self.assertEqual(len(parts[1]), 2)  # Month should be 2 digits
        self.assertEqual(len(parts[2]), 2)  # Day should be 2 digits


if __name__ == '__main__':
    unittest.main()

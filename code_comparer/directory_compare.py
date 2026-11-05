#!/usr/bin/env python3
"""
Directory Comparison Script
Compares files between home/ and office/ directories and logs changes.
Usage: python directory_compare.py
"""

from typing import Union

import os
import hashlib
import logging
from pathlib import Path
from datetime import datetime
import filecmp
import json

_APP_DIR = Path(__file__).resolve().parent


def _resolve_app_path(p: Union[str, Path]) -> Path:
    path = Path(p)
    return path if path.is_absolute() else _APP_DIR / path


class DirectoryComparer:
    def __init__(self, home_dir="home", office_dir="office", log_file="changes.log"):
        self.home_dir = _resolve_app_path(home_dir)
        self.office_dir = _resolve_app_path(office_dir)
        self.log_file = str(_resolve_app_path(log_file))
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def calculate_md5(self, file_path):
        """Calculate MD5 hash of a file"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            self.logger.error(f"Error calculating MD5 for {file_path}: {e}")
            return None

    def get_file_info(self, directory):
        """Get file information for all files in directory"""
        file_info = {}
        
        if not directory.exists():
            self.logger.warning(f"Directory does not exist: {directory}")
            return file_info
            
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = Path(root) / file
                relative_path = file_path.relative_to(directory)
                
                try:
                    stat = file_path.stat()
                    file_info[str(relative_path)] = {
                        'size': stat.st_size,
                        'modified': stat.st_mtime,
                        'md5': self.calculate_md5(file_path),
                        'full_path': str(file_path)
                    }
                except Exception as e:
                    self.logger.error(f"Error getting info for {file_path}: {e}")
                    
        return file_info

    def compare_files(self, file1_path, file2_path):
        """Compare two files using filecmp"""
        try:
            return filecmp.cmp(file1_path, file2_path, shallow=False)
        except Exception as e:
            self.logger.error(f"Error comparing {file1_path} and {file2_path}: {e}")
            return False

    def compare_directories(self):
        """Compare home and office directories"""
        self.logger.info("Starting directory comparison...")
        self.logger.info(f"Home directory: {self.home_dir}")
        self.logger.info(f"Office directory: {self.office_dir}")
        
        # Get file information from both directories
        home_files = self.get_file_info(self.home_dir)
        office_files = self.get_file_info(self.office_dir)
        
        # Files only in home directory
        home_only = set(home_files.keys()) - set(office_files.keys())
        if home_only:
            self.logger.info("\n=== FILES ONLY IN HOME DIRECTORY ===")
            for file in sorted(home_only):
                self.logger.info(f"HOME ONLY: {file}")
                self.logger.info(f"  Size: {home_files[file]['size']} bytes")
                self.logger.info(f"  Modified: {datetime.fromtimestamp(home_files[file]['modified'])}")
        
        # Files only in office directory
        office_only = set(office_files.keys()) - set(home_files.keys())
        if office_only:
            self.logger.info("\n=== FILES ONLY IN OFFICE DIRECTORY ===")
            for file in sorted(office_only):
                self.logger.info(f"OFFICE ONLY: {file}")
                self.logger.info(f"  Size: {office_files[file]['size']} bytes")
                self.logger.info(f"  Modified: {datetime.fromtimestamp(office_files[file]['modified'])}")
        
        # Files in both directories - check for differences
        common_files = set(home_files.keys()) & set(office_files.keys())
        if common_files:
            self.logger.info("\n=== COMPARING COMMON FILES ===")
            different_files = []
            
            for file in sorted(common_files):
                home_info = home_files[file]
                office_info = office_files[file]
                
                # Compare by MD5 hash
                if home_info['md5'] != office_info['md5']:
                    different_files.append(file)
                    self.logger.warning(f"DIFFERENT CONTENT: {file}")
                    
                    # Compare modification times
                    home_time = datetime.fromtimestamp(home_info['modified'])
                    office_time = datetime.fromtimestamp(office_info['modified'])
                    
                    if home_info['modified'] > office_info['modified']:
                        self.logger.info(f"  HOME is newer: {home_time} > {office_time}")
                    elif office_info['modified'] > home_info['modified']:
                        self.logger.info(f"  OFFICE is newer: {office_time} > {home_time}")
                    else:
                        self.logger.info(f"  Same modification time but different content")
                    
                    self.logger.info(f"  HOME - Size: {home_info['size']}, Modified: {home_time}")
                    self.logger.info(f"  OFFICE - Size: {office_info['size']}, Modified: {office_time}")
                
                # Check size differences even if content is same
                elif home_info['size'] != office_info['size']:
                    self.logger.warning(f"DIFFERENT SIZE (same MD5): {file}")
                    self.logger.info(f"  HOME: {home_info['size']} bytes")
                    self.logger.info(f"  OFFICE: {office_info['size']} bytes")
        
        # Summary
        self.logger.info("\n=== SUMMARY ===")
        self.logger.info(f"Files only in HOME: {len(home_only)}")
        self.logger.info(f"Files only in OFFICE: {len(office_only)}")
        self.logger.info(f"Common files: {len(common_files)}")
        
        if common_files:
            different_content = sum(1 for file in common_files 
                                 if home_files[file]['md5'] != office_files[file]['md5'])
            self.logger.info(f"Files with different content: {different_content}")
        
        self.logger.info("Comparison completed!")
        
        return {
            'home_only': list(home_only),
            'office_only': list(office_only),
            'common_files': list(common_files),
            'timestamp': datetime.now().isoformat()
        }

    def create_sample_structure(self):
        """Create sample directory structure for testing"""
        # Create directories
        self.home_dir.mkdir(exist_ok=True)
        self.office_dir.mkdir(exist_ok=True)
        
        # Create some sample files in home directory
        (self.home_dir / "README.md").write_text("# Project Documentation\nThis is the main project.")
        (self.home_dir / "main.py").write_text("def main():\n    print('Hello from home!')\n\nif __name__ == '__main__':\n    main()")
        (self.home_dir / "config.json").write_text('{"version": "1.0", "debug": true}')
        
        # Create subdirectory
        subdir = self.home_dir / "src"
        subdir.mkdir(exist_ok=True)
        (subdir / "utils.py").write_text("def helper_function():\n    return 'utility function'")
        
        # Create similar structure in office directory with some differences
        (self.office_dir / "README.md").write_text("# Project Documentation\nThis is the main project from office.")
        (self.office_dir / "main.py").write_text("def main():\n    print('Hello from office!')\n\nif __name__ == '__main__':\n    main()")
        (self.office_dir / "config.json").write_text('{"version": "1.1", "debug": false}')
        (self.office_dir / "office_only.txt").write_text("This file only exists in office")
        
        # Create subdirectory
        subdir_office = self.office_dir / "src"
        subdir_office.mkdir(exist_ok=True)
        (subdir_office / "utils.py").write_text("def helper_function():\n    return 'utility function'")  # Same content
        
        self.logger.info("Sample directory structure created!")

def main():
    """Main function"""
    comparer = DirectoryComparer()
    
    # Create sample structure if directories don't exist
    if not comparer.home_dir.exists() or not comparer.office_dir.exists():
        print("Creating sample directory structure...")
        comparer.create_sample_structure()
        print("Sample structure created. You can now modify files and run the script again.")
        return
    
    # Run comparison
    result = comparer.compare_directories()
    
    # Save results to JSON file for further processing
    with open(_APP_DIR / "comparison_result.json", "w") as f:
        json.dump(result, f, indent=2)
    
    print(f"\nComparison completed! Check '{comparer.log_file}' for detailed logs.")
    print("Results also saved to 'comparison_result.json'")

if __name__ == "__main__":
    main()
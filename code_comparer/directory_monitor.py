#!/usr/bin/env python3
"""
Enhanced Directory Comparison and Monitoring Script
Compares files between home/ and office/ directories with optional real-time monitoring.
Usage: 
    python directory_monitor.py --compare    # One-time comparison
    python directory_monitor.py --monitor    # Real-time monitoring
    python directory_monitor.py --help       # Show help
"""

import os
import hashlib
import logging
import argparse
from pathlib import Path
from datetime import datetime
import filecmp
import json
import time
from typing import Union

# Optional watchdog for real-time monitoring
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False

    class FileSystemEventHandler:
        """Stub base class when watchdog is not installed."""

    Observer = None  # type: ignore[misc, assignment]


_APP_DIR = Path(__file__).resolve().parent


def _resolve_app_path(p: Union[str, Path]) -> Path:
    path = Path(p)
    return path if path.is_absolute() else _APP_DIR / path


class ChangeHandler(FileSystemEventHandler):
    """Handler for file system events"""
    
    def __init__(self, comparer):
        self.comparer = comparer
        self.logger = comparer.logger
        
    def on_any_event(self, event):
        if event.is_directory:
            return
            
        self.logger.info(f"File {event.event_type}: {event.src_path}")
        
        # Trigger a new comparison after a short delay
        time.sleep(1)  # Avoid rapid successive comparisons
        self.comparer.quick_compare(event.src_path)

class EnhancedDirectoryComparer:
    def __init__(self, home_dir="home", office_dir="office", log_file="directory_changes.log"):
        self.home_dir = _resolve_app_path(home_dir)
        self.office_dir = _resolve_app_path(office_dir)
        self.log_file = str(_resolve_app_path(log_file))
        self.last_comparison = None
        
        # Setup logging with more detailed format
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - [%(funcName)s] - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, mode='a'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Store last known state
        self.last_home_state = {}
        self.last_office_state = {}
        
    def calculate_file_hash(self, file_path):
        """Calculate SHA256 hash of a file for better accuracy"""
        try:
            hash_sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            self.logger.error(f"Error calculating hash for {file_path}: {e}")
            return None

    def get_file_metadata(self, directory, relative_to=None):
        """Get comprehensive file metadata"""
        file_data = {}
        base_dir = relative_to or directory
        
        if not directory.exists():
            self.logger.warning(f"Directory does not exist: {directory}")
            return file_data
            
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = Path(root) / file
                try:
                    relative_path = file_path.relative_to(base_dir)
                    stat = file_path.stat()
                    
                    file_data[str(relative_path)] = {
                        'size': stat.st_size,
                        'modified': stat.st_mtime,
                        'created': getattr(stat, 'st_birthtime', stat.st_ctime),
                        'hash': self.calculate_file_hash(file_path),
                        'full_path': str(file_path),
                        'permissions': oct(stat.st_mode)[-3:]
                    }
                except Exception as e:
                    self.logger.error(f"Error processing {file_path}: {e}")
                    
        return file_data

    def find_changes(self, old_state, new_state, location_name):
        """Find changes between two states"""
        changes = {
            'added': [],
            'removed': [],
            'modified': [],
            'unchanged': []
        }
        
        old_files = set(old_state.keys())
        new_files = set(new_state.keys())
        
        # Added files
        added_files = new_files - old_files
        for file in added_files:
            changes['added'].append({
                'file': file,
                'info': new_state[file]
            })
            self.logger.info(f"[{location_name}] ADDED: {file}")
        
        # Removed files
        removed_files = old_files - new_files
        for file in removed_files:
            changes['removed'].append({
                'file': file,
                'info': old_state[file]
            })
            self.logger.warning(f"[{location_name}] REMOVED: {file}")
        
        # Check for modifications in common files
        common_files = old_files & new_files
        for file in common_files:
            old_info = old_state[file]
            new_info = new_state[file]
            
            if old_info['hash'] != new_info['hash']:
                changes['modified'].append({
                    'file': file,
                    'old_info': old_info,
                    'new_info': new_info
                })
                self.logger.warning(f"[{location_name}] MODIFIED: {file}")
                self.logger.info(f"  Old: {datetime.fromtimestamp(old_info['modified'])} ({old_info['size']} bytes)")
                self.logger.info(f"  New: {datetime.fromtimestamp(new_info['modified'])} ({new_info['size']} bytes)")
            else:
                changes['unchanged'].append(file)
        
        return changes

    def quick_compare(self, changed_file_path=None):
        """Quick comparison focusing on recently changed files"""
        if changed_file_path:
            self.logger.info(f"Quick comparison triggered by: {changed_file_path}")
        
        # Get current state
        current_home = self.get_file_metadata(self.home_dir)
        current_office = self.get_file_metadata(self.office_dir)
        
        # Find changes since last check
        if self.last_home_state:
            home_changes = self.find_changes(self.last_home_state, current_home, "HOME")
        if self.last_office_state:
            office_changes = self.find_changes(self.last_office_state, current_office, "OFFICE")
        
        # Update last known state
        self.last_home_state = current_home
        self.last_office_state = current_office
        
        # Compare between directories
        self._compare_directories_detailed(current_home, current_office)

    def full_compare(self):
        """Comprehensive directory comparison"""
        self.logger.info("="*60)
        self.logger.info("STARTING FULL DIRECTORY COMPARISON")
        self.logger.info(f"Home directory: {self.home_dir.absolute()}")
        self.logger.info(f"Office directory: {self.office_dir.absolute()}")
        self.logger.info("="*60)
        
        # Get file information from both directories
        home_files = self.get_file_metadata(self.home_dir)
        office_files = self.get_file_metadata(self.office_dir)
        
        # Store current state
        self.last_home_state = home_files
        self.last_office_state = office_files
        
        return self._compare_directories_detailed(home_files, office_files)

    def _compare_directories_detailed(self, home_files, office_files):
        """Detailed comparison between home and office directories"""
        # Files only in home
        home_only = set(home_files.keys()) - set(office_files.keys())
        if home_only:
            self.logger.info("\n" + "="*40)
            self.logger.info("FILES ONLY IN HOME DIRECTORY")
            self.logger.info("="*40)
            for file in sorted(home_only):
                info = home_files[file]
                self.logger.info(f"ðŸ“ HOME ONLY: {file}")
                self.logger.info(f"   Size: {info['size']:,} bytes")
                self.logger.info(f"   Modified: {datetime.fromtimestamp(info['modified'])}")
        
        # Files only in office
        office_only = set(office_files.keys()) - set(home_files.keys())
        if office_only:
            self.logger.info("\n" + "="*40)
            self.logger.info("FILES ONLY IN OFFICE DIRECTORY")
            self.logger.info("="*40)
            for file in sorted(office_only):
                info = office_files[file]
                self.logger.info(f"ðŸ¢ OFFICE ONLY: {file}")
                self.logger.info(f"   Size: {info['size']:,} bytes")
                self.logger.info(f"   Modified: {datetime.fromtimestamp(info['modified'])}")
        
        # Common files - check for differences
        common_files = set(home_files.keys()) & set(office_files.keys())
        different_files = []
        
        if common_files:
            self.logger.info("\n" + "="*40)
            self.logger.info("COMPARING COMMON FILES")
            self.logger.info("="*40)
            
            for file in sorted(common_files):
                home_info = home_files[file]
                office_info = office_files[file]
                
                # Compare by hash
                if home_info['hash'] != office_info['hash']:
                    different_files.append(file)
                    self.logger.warning(f"âš ï¸  CONTENT DIFFERS: {file}")
                    
                    home_time = datetime.fromtimestamp(home_info['modified'])
                    office_time = datetime.fromtimestamp(office_info['modified'])
                    
                    # Determine which is newer
                    if home_info['modified'] > office_info['modified']:
                        self.logger.info(f"   ðŸ  HOME is newer: {home_time}")
                        self.logger.info(f"   ðŸ¢ OFFICE older: {office_time}")
                        time_diff = home_info['modified'] - office_info['modified']
                        self.logger.info(f"   â° Difference: {time_diff/3600:.1f} hours")
                    elif office_info['modified'] > home_info['modified']:
                        self.logger.info(f"   ðŸ¢ OFFICE is newer: {office_time}")
                        self.logger.info(f"   ðŸ  HOME older: {home_time}")
                        time_diff = office_info['modified'] - home_info['modified']
                        self.logger.info(f"   â° Difference: {time_diff/3600:.1f} hours")
                    else:
                        self.logger.info(f"   ðŸ“… Same modification time but different content!")
                    
                    # Size comparison
                    size_diff = home_info['size'] - office_info['size']
                    if size_diff != 0:
                        self.logger.info(f"   ðŸ“Š Size difference: {size_diff:+} bytes")
                    
                    self.logger.info(f"   ðŸ  HOME: {home_info['size']:,} bytes")
                    self.logger.info(f"   ðŸ¢ OFFICE: {office_info['size']:,} bytes")
                    self.logger.info("")
        
        # Generate summary
        self.logger.info("\n" + "="*40)
        self.logger.info("COMPARISON SUMMARY")
        self.logger.info("="*40)
        self.logger.info(f"ðŸ“Š Files only in HOME: {len(home_only)}")
        self.logger.info(f"ðŸ“Š Files only in OFFICE: {len(office_only)}")
        self.logger.info(f"ðŸ“Š Common files: {len(common_files)}")
        self.logger.info(f"ðŸ“Š Files with differences: {len(different_files)}")
        
        if different_files:
            self.logger.warning("\nðŸš¨ ACTION NEEDED: Files with differences detected!")
            self.logger.info("Different files:")
            for file in different_files:
                self.logger.info(f"  - {file}")
        else:
            self.logger.info("\nâœ… All common files are identical!")
        
        # Save detailed results
        results = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'home_only_count': len(home_only),
                'office_only_count': len(office_only),
                'common_files_count': len(common_files),
                'different_files_count': len(different_files)
            },
            'home_only_files': list(home_only),
            'office_only_files': list(office_only),
            'different_files': different_files,
            'all_files': {
                'home': {k: v for k, v in home_files.items()},
                'office': {k: v for k, v in office_files.items()}
            }
        }
        
        # Save to JSON
        with open(_APP_DIR / "detailed_comparison.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        
        self.logger.info(f"\nðŸ’¾ Detailed results saved to 'detailed_comparison.json'")
        return results

    def monitor_directories(self):
        """Monitor directories for real-time changes"""
        if not WATCHDOG_AVAILABLE or Observer is None:
            self.logger.error("Watchdog library not available. Install with: pip install watchdog")
            return
        
        self.logger.info("Starting real-time directory monitoring...")
        self.logger.info("Press Ctrl+C to stop monitoring")
        
        # Initial comparison
        self.full_compare()
        
        # Set up monitoring
        event_handler = ChangeHandler(self)
        observer = Observer()
        
        # Monitor both directories
        if self.home_dir.exists():
            observer.schedule(event_handler, str(self.home_dir), recursive=True)
            self.logger.info(f"Monitoring HOME directory: {self.home_dir}")
        
        if self.office_dir.exists():
            observer.schedule(event_handler, str(self.office_dir), recursive=True)
            self.logger.info(f"Monitoring OFFICE directory: {self.office_dir}")
        
        observer.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Stopping monitoring...")
            observer.stop()
        
        observer.join()
        self.logger.info("Monitoring stopped.")

    def create_sample_files(self):
        """Create sample directory structure for testing"""
        self.logger.info("Creating sample directory structure...")
        
        # Create directories
        self.home_dir.mkdir(exist_ok=True)
        self.office_dir.mkdir(exist_ok=True)
        
        # Sample content for home
        home_files = {
            "README.md": "# My Project\n\nThis is my main project repository.\nLast updated from home.",
            "main.py": """#!/usr/bin/env python3
def main():
    print("Hello from home version!")
    return "home"

if __name__ == "__main__":
    main()""",
            "config.json": '{"version": "1.2.0", "environment": "home", "debug": true}',
            "data.txt": "Home data\nLine 2\nLine 3"
        }
        
        # Sample content for office (with some differences)
        office_files = {
            "README.md": "# My Project\n\nThis is my main project repository.\nLast updated from office.",
            "main.py": """#!/usr/bin/env python3
def main():
    print("Hello from office version!")
    return "office"

if __name__ == "__main__":
    main()""",
            "config.json": '{"version": "1.1.0", "environment": "office", "debug": false}',
            "office_notes.txt": "Notes taken during office hours\nRemember to sync changes"
        }
        
        # Create subdirectories
        (self.home_dir / "src").mkdir(exist_ok=True)
        (self.office_dir / "src").mkdir(exist_ok=True)
        
        # Create files in home
        for filename, content in home_files.items():
            (self.home_dir / filename).write_text(content)
        
        (self.home_dir / "src" / "utils.py").write_text("""
def get_timestamp():
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def home_function():
    return "This function was added at home"
""")
        
        # Create files in office
        for filename, content in office_files.items():
            (self.office_dir / filename).write_text(content)
        
        (self.office_dir / "src" / "utils.py").write_text("""
def get_timestamp():
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def office_function():
    return "This function was added at office"
""")
        
        self.logger.info("Sample directory structure created!")
        self.logger.info("You can now run the comparison to see the differences.")

def main():
    parser = argparse.ArgumentParser(
        description="Compare and monitor directories for changes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python directory_monitor.py --compare     # One-time comparison
  python directory_monitor.py --monitor     # Real-time monitoring  
  python directory_monitor.py --sample      # Create sample structure
  python directory_monitor.py --home ./my_home --office ./my_office --compare
        """
    )
    
    parser.add_argument('--compare', action='store_true', 
                       help='Perform one-time directory comparison')
    parser.add_argument('--monitor', action='store_true',
                       help='Start real-time monitoring (requires watchdog)')
    parser.add_argument('--sample', action='store_true',
                       help='Create sample directory structure')
    parser.add_argument('--home', default='home',
                       help='Home directory path (default: home)')
    parser.add_argument('--office', default='office', 
                       help='Office directory path (default: office)')
    parser.add_argument('--log', default='directory_changes.log',
                       help='Log file path (default: directory_changes.log)')
    
    args = parser.parse_args()
    
    # Create comparer instance
    comparer = EnhancedDirectoryComparer(args.home, args.office, args.log)
    
    if args.sample:
        comparer.create_sample_files()
    elif args.monitor:
        comparer.monitor_directories()
    elif args.compare:
        comparer.full_compare()
    else:
        # Default behavior
        if not comparer.home_dir.exists() or not comparer.office_dir.exists():
            print("Directories don't exist. Creating sample structure...")
            comparer.create_sample_files()
        else:
            print("Running comparison...")
            comparer.full_compare()

if __name__ == "__main__":
    main()
"""
Setup Test Script for Storm911
Tests application setup and dependencies
"""

import os
import sys
import logging
import importlib
import subprocess
from typing import List, Tuple

class SetupTester:
    def __init__(self):
        """Initialize Setup Tester"""
        self.required_dirs = [
            'assets',
            'EXPORTS',
            'logs',
            'data'
        ]
        
        self.required_files = [
            'app.py',
            'config.py',
            'requirements.txt',
            'LICENSE'
        ]
        
        self.required_modules = [
            'customtkinter',
            'Pillow',
            'requests',
            'reportlab',
            'email_validator',
            'phonenumbers',
            'python-dateutil',
            'cryptography',
            'pydantic'
        ]
    
    def run_tests(self) -> bool:
        """Run all setup tests"""
        try:
            print("\nRunning Storm911 Setup Tests")
            print("============================")
            
            # Test directory structure
            print("\nTesting directory structure...")
            dir_result = self.test_directories()
            self._print_result("Directory structure", dir_result)
            
            # Test required files
            print("\nTesting required files...")
            file_result = self.test_files()
            self._print_result("Required files", file_result)
            
            # Test Python version
            print("\nTesting Python version...")
            python_result = self.test_python_version()
            self._print_result("Python version", python_result)
            
            # Test dependencies
            print("\nTesting dependencies...")
            dep_result = self.test_dependencies()
            self._print_result("Dependencies", dep_result)
            
            # Test imports
            print("\nTesting module imports...")
            import_result = self.test_imports()
            self._print_result("Module imports", import_result)
            
            # Test permissions
            print("\nTesting file permissions...")
            perm_result = self.test_permissions()
            self._print_result("File permissions", perm_result)
            
            # Overall result
            all_passed = all([
                dir_result[0],
                file_result[0],
                python_result[0],
                dep_result[0],
                import_result[0],
                perm_result[0]
            ])
            
            print("\nOverall Test Result:")
            print("===================")
            if all_passed:
                print("✅ All tests passed successfully!")
                return True
            else:
                print("❌ Some tests failed. Please check the details above.")
                return False
            
        except Exception as e:
            print(f"\n❌ Error running tests: {str(e)}")
            return False
    
    def test_directories(self) -> Tuple[bool, List[str]]:
        """Test required directories"""
        missing = []
        for directory in self.required_dirs:
            if not os.path.exists(directory):
                missing.append(directory)
        
        return len(missing) == 0, missing
    
    def test_files(self) -> Tuple[bool, List[str]]:
        """Test required files"""
        missing = []
        for file in self.required_files:
            if not os.path.exists(file):
                missing.append(file)
        
        return len(missing) == 0, missing
    
    def test_python_version(self) -> Tuple[bool, str]:
        """Test Python version"""
        version = sys.version_info
        required = (3, 8)
        
        if version >= required:
            return True, f"Python {version.major}.{version.minor}.{version.micro}"
        else:
            return False, f"Python {required[0]}.{required[1]}+ required"
    
    def test_dependencies(self) -> Tuple[bool, List[str]]:
        """Test required dependencies"""
        missing = []
        for module in self.required_modules:
            try:
                importlib.import_module(module)
            except ImportError:
                missing.append(module)
        
        return len(missing) == 0, missing
    
    def test_imports(self) -> Tuple[bool, List[str]]:
        """Test application module imports"""
        failed = []
        modules = [
            'app_initializer',
            'api_handler',
            'caller_info_panel',
            'config',
            'dialog_manager',
            'disposition_handler',
            'email_handler',
            'event_logger',
            'hotkey_manager',
            'menu_manager',
            'objection_responses',
            'pdf_handler',
            'settings_manager',
            'state_manager',
            'theme_manager',
            'transcript_content',
            'transcript_panel',
            'ui_panels',
            'utils'
        ]
        
        for module in modules:
            try:
                importlib.import_module(module)
            except ImportError as e:
                failed.append(f"{module}: {str(e)}")
        
        return len(failed) == 0, failed
    
    def test_permissions(self) -> Tuple[bool, List[str]]:
        """Test file permissions"""
        failed = []
        
        # Test directory permissions
        for directory in self.required_dirs:
            if os.path.exists(directory):
                if not os.access(directory, os.W_OK):
                    failed.append(f"No write permission: {directory}")
        
        # Test file permissions
        for file in self.required_files:
            if os.path.exists(file):
                if not os.access(file, os.R_OK):
                    failed.append(f"No read permission: {file}")
        
        return len(failed) == 0, failed
    
    def _print_result(self, test_name: str, result: Tuple[bool, any]) -> None:
        """Print test result"""
        success, details = result
        
        if success:
            print(f"✅ {test_name} test passed")
        else:
            print(f"❌ {test_name} test failed")
            if isinstance(details, list):
                for item in details:
                    print(f"   - {item}")
            else:
                print(f"   - {details}")

def main():
    """Main entry point"""
    try:
        # Create and run tester
        tester = SetupTester()
        success = tester.run_tests()
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"\n❌ Setup test failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

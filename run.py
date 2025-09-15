#!/usr/bin/env python3
"""
YouTube Video Downloader Launcher
Quick start script with dependency checking.
"""

import sys
import os
import subprocess


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = {
        'customtkinter': 'customtkinter>=5.2.0',
        'pytube': 'pytube>=15.0.0',
        'PIL': 'Pillow>=9.0.0'
    }
    
    missing_packages = []
    
    for package, pip_name in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {package} is available")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(pip_name)
    
    return missing_packages


def install_dependencies(packages):
    """Install missing dependencies."""
    if not packages:
        return True
    
    print(f"\n📦 Installing missing packages: {', '.join(packages)}")
    try:
        cmd = [sys.executable, '-m', 'pip', 'install'] + packages
        subprocess.check_call(cmd)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies!")
        print("   Please install manually with:")
        print(f"   pip install {' '.join(packages)}")
        return False


def launch_app():
    """Launch the main application."""
    print("\n🚀 Launching YouTube Video Downloader...")
    try:
        # Change to script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Import and run the app
        from main import App
        app = App()
        app.mainloop()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Please ensure all dependencies are installed.")
        return False
    except Exception as e:
        print(f"❌ Error launching app: {e}")
        return False
    
    return True


def main():
    """Main launcher function."""
    print("🎬 YouTube Video Downloader Launcher")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check dependencies
    missing = check_dependencies()
    
    if missing:
        print(f"\n🔧 Missing dependencies detected!")
        response = input("   Install automatically? (y/n): ").lower().strip()
        
        if response in ['y', 'yes']:
            if not install_dependencies(missing):
                sys.exit(1)
        else:
            print("   Please install dependencies manually and try again.")
            sys.exit(1)
    
    # Launch the application
    print("\n" + "=" * 40)
    if not launch_app():
        sys.exit(1)


if __name__ == "__main__":
    main()
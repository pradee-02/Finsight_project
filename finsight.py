import os
import sys
import subprocess

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_terminal()
    banner = """
========================================================================
     _______ _       _____ _       _     _      _    _               _ 
    |  _____(_)     / ____(_)     | |   | |    | |  | |             | |
    | |__    _ _ __| (___  _  __ _| |__ | |_   | |__| | ___  _ __ __| |
    |  __|  | | '_ \\\\___ \\| |/ _` | '_ \\| __|  |  __  |/ _ \\| '__/ _` |
    | |     | | | | |___) | | (_| | | | | |_   | |  | | (_) | | | (_| |
    |_|     |_|_| |_|____/|_|\\__, |_| |_|\\__|  |_|  |_|\\___/|_|  \\__,_|
                              __/ |                                    
                             |___/                                     
========================================================================
   INTELLIGENT FINANCE & MILESTONE ROADMAP WORKSPACE - PYTHON CENTER
========================================================================
    """
    print(banner)
    print("Welcome, Arjun Mehta!")
    print("You have requested the full project in Python code. To provide maximum")
    print("versatility, two full-featured Python implementations have been compiled:")
    print("")
    print(" [1] Modern Analytics Streamlit Dashboard (Web-based interactive experience)")
    print("     - Rich interactive Plotly graphs (Bar, Pie, Area trends)")
    print("     - Modern reactive design, sidebar layouts, tab controls")
    print("     - Requires: pip install streamlit pandas plotly")
    print("")
    print(" [2] Standalone Desktop Tkinter GUI (Desktop window experience)")
    print("     - Zero-dependencies! Runs on any system with pre-installed Python")
    print("     - Responsive frames, tables, scrollbars, and inputs")
    print("     - Fully synchronized local JSON database sharing with Streamlit")
    print("")
    print("========================================================================")
    print("Both applications load/save from the unified local database: finsight_data.json")
    print("========================================================================")
    print("")
    
    choice = input("Enter your selection (1 or 2) to launch, or 'q' to exit: ").strip().lower()
    
    if choice == '1':
        print("\nChecking if Streamlit is installed...")
        try:
            import streamlit
            print("Streamlit detected! Initializing local web server...")
            subprocess.run([sys.executable, "-m", "streamlit", "run", "finsight_streamlit.py"])
        except ImportError:
            print("\n❌ Streamlit is not installed in this environment.")
            print("To run the interactive analytical dashboard, install requirements via:")
            print("  pip install streamlit pandas plotly")
            print("\nAttempting fallback to launch standard zero-dependency Desktop GUI (Option 2) instead...")
            input("Press [Enter] to continue...")
            launch_tkinter()
            
    elif choice == '2':
        launch_tkinter()
    elif choice in ['q', 'exit', 'quit']:
        print("\nExiting FinSight Python center. Have a productive day!")
    else:
        print("\nInvalid choice. Exiting.")

def launch_tkinter():
    print("\nLaunching zero-dependency Desktop GUI application...")
    try:
        subprocess.run([sys.executable, "finsight_gui.py"])
    except Exception as e:
        print(f"❌ Failed to launch Tkinter GUI. Error: {e}")
        print("Please run manually using: python finsight_gui.py")

if __name__ == "__main__":
    main()

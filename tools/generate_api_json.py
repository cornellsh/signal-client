import griffe
import json
import sys
import os

def main():
    try:
        # Ensure the current directory is in sys.path so griffe can find the package if it relies on import or path traversal
        sys.path.insert(0, os.getcwd())
        
        print("Loading signal_client package analysis...")
        data = griffe.load("signal_client")
        
        print("Converting to JSON...")
        # as_json() returns a JSON string and handles internal types like Docstring
        json_str = data.as_json(indent=2)
        
        output_file = "signal_client_api.json"
        print(f"Writing to {output_file}...")
        with open(output_file, "w") as f:
            f.write(json_str)
            
        print(f"Successfully generated {output_file}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

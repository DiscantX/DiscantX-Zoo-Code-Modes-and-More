import os
import glob
import shutil

def batch_convert_xml_script_dir():
    # Get the absolute path of the directory where this script lives
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the parent directory of where the script lives
    parent_dir = os.path.dirname(script_dir)
    
    # Define the target subdirectory relative to the parent directory
    target_dir = os.path.join(parent_dir, "txt")
    target_dir = f"{target_dir}"
    
    # Create the directory if it does not exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"Created subdirectory: '{target_dir}/'")
        
    # Find all .xml files in the parent directory
    search_path = os.path.join(parent_dir, "*.xml")
    xml_files = glob.glob(search_path)
    
    if not xml_files:
        print(f"No .xml files found in the parent directory: {parent_dir}")
        return

    for xml_path in xml_files:
        # Get just the file name (e.g., "data.xml")
        xml_filename = os.path.basename(xml_path)
        
        # Build the destination path (e.g., script_dir/txt/data.xml.txt)
        new_filepath = os.path.join(target_dir, f"{xml_filename}.txt")
        
        try:
            # Copy and overwrite if it already exists
            shutil.copy2(xml_path, new_filepath)
            print(f"Copied: {xml_filename} -> txt/{xml_filename}.txt")
            
        except Exception as e:
            print(f"Error copying {xml_filename}: {e}")

if __name__ == "__main__":
    batch_convert_xml_script_dir()

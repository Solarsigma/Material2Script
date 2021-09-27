# Material2Script
A script to convert a node setup (for a material) to a script which can recreate the material procedurally.  
  
# Steps to Use
The script basically gives a function called `materialToScript` which takes 1 argument: the name of the material in your .blend file. Here are the steps to use it:  
1. Open the .blend file in which you have the materials you want to script and open the file `mat2script.py` from the blend file (in the Scripting tab).
2. Edit the last line and replace `"Material"` to the name of the material in your blend file and run the script (Shortcut Alt+P)
3. A file called `script.py` will be created in the same folder as your blend file.
> Note: If you have multiple materials in the same blend file, then either add lines to the end of the file calling the function with other material names, or run the script once, copy paste the contents of `script.py` somewhere else, and run the script again with another material name. Running the program twice consecutively will overwrite the original material code.  
  
# Additional Info
The script only supports ShaderNodes sadly  
The script adds comments so it is easy for you to navigate in the script made if needed.  
Since the script is currently not completely compatible with all kinds of objects in some ShaderNodes (like `Blender Collection` or `Blender NodeGroup` etc it adds comments at the places in the script where you can add these properties yourself.

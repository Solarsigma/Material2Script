import bpy
import os

DEFAULT_NA_SOCKETS = ["NodeSocketGeometry", "NodeSocketShader", "NodeSocketVirtual"]
DEFAULT_BLENDER_OBJ_SOCKETS = ["NodeSocketCollection", "NodeSocketImage", "NodeSocketObject"]
DEFAULT_ARRAY_SOCKETS = ["NodeSocketColor", "NodeSocketVector", "NodeSocketVectorAcceleration", "NodeSocketVectorDirection", "NodeSocketVectorEuler", "NodeSocketVectorTranslation", "NodeSocketVectorVelocity", "NodeSocketVectorXYZ"]
DEFAULT_ATTRS = ['color', 'dimensions', 'height', 'hide', 'inputs', 'internal_links', 'label', 'location', 'mute', 'name', 'outputs', 'parent', 'select', 'show_options', 'show_preview', 'show_texture', 'type', 'use_custom_color', 'width', 'width_hidden', 'rna_type']





def materialToScript(materialName):
    
    def handleImage(node, nodeName, f):
        image = node.image
        f.write('## Image Filepath added below please check\n')
        f.write(f'img = bpy.data.images.load(bpy.path.relpath("{image.filepath}"))\n')
        f.write(f'{nodeName}.image = img\n')
    
    def handleColorRamp(node, nodeName, f):
        colorRamp = node.color_ramp
        f.write(f'{nodeName}.color_ramp.color_mode = {colorRamp.color_mode}\n')
        f.write(f'{nodeName}.color_ramp.hue_interpolation = {colorRamp.hue_interpolation}\n')
        f.write(f'{nodeName}.color_ramp.interpolation = {colorRamp.interpolation}\n')
        f.write(f'{nodeName}.color_ramp.elements.remove({nodeName}.color_ramp.elements[1])\n')
        f.write(f'{nodeName}.color_ramp.elements.remove({nodeName}.color_ramp.elements[0])\n')
        for element in colorRamp.elements:
            f.write(f'temp = {nodeName}.color_ramp.elements.new({element.position})\n')
            f.write(f'temp.alpha = {element.alpha}\n')
            f.write(f'temp.color = {list(element.color)}\n')
        return

    with open("script.py", "w") as f:        
        material = bpy.data.materials.get(materialName)
        if material is None:
            print("Error: Material Name specified does not exist")
            f.close()
            return
        nodes = material.node_tree.nodes
        links = material.node_tree.links
        
        f.write("import bpy\n")
        f.write('\n')
        f.write(f'material = bpy.data.materials.new("{materialName}")\n')
        f.write('material.use_nodes = True\n')
        f.write('nodes = material.node_tree.nodes\n')
        f.write('links = material.node_tree.links\n')
        f.write('\n')
        f.write('nodes.remove(nodes.get("Principled BSDF"))\n')
        f.write('nodes.remove(nodes.get("Material Output"))\n')
        f.write('\n')
        f.write('## Adding all nodes\n')
        for node in nodes:
            nodeName = '_'.join('_'.join(node.name.split(' ')).split('.'))
            f.write(f'# {nodeName} Node\n')
            f.write(f'{nodeName} = nodes.new(type="{node.bl_idname}")\n')
            f.write(f'{nodeName}.location = {list(node.location)}\n')
            for attrName in [i for i in dir(node) if ((not i.startswith('_')) and (not i.startswith('bl_')) and (not callable(getattr(node, i))) and (i not in DEFAULT_ATTRS))]:
                attr = getattr(node, attrName)
                if type(attr) == str:
                    f.write(f'{nodeName}.{attrName} = "{attr}"\n')
                elif type(attr) == bool or type(attr) == int or type(attr) == float:
                    f.write(f'{nodeName}.{attrName} = {attr}\n')
                else:
                    if attrName == 'color_ramp':
                        handleColorRamp(node, nodeName, f)
                    elif attrName == 'image':
                        handleImage(node, nodeName, f)
                    else:
                        print(attr)
                        f.write(f'# {nodeName}_{attrName} Add the {attrName} property of {nodeName} hereeee!!!!\n')
                    
            for input in node.inputs:
                if not input.is_linked:
                    if input.bl_idname in DEFAULT_NA_SOCKETS:
                        pass
                    elif input.bl_idname in DEFAULT_BLENDER_OBJ_SOCKETS:
                        f.write(f'# Default value of {input.bl_idname} of {node.name} Node is an Blender Image, Blender Collection or Blender Object\n')
                    elif input.bl_idname in DEFAULT_ARRAY_SOCKETS:
                        f.write(f'{nodeName}.inputs[{node.inputs.values().index(input)}].default_value = {list(input.default_value)}\n')
                    else:
                        f.write(f'{nodeName}.inputs[{node.inputs.values().index(input)}].default_value = {input.default_value}\n')
            f.write('\n')
        f.write('\n')
        
        f.write('## Adding all links\n')
        for link in links:
            fromNodeName = '_'.join('_'.join(link.from_node.name.split(' ')).split('.'))
            toNodeName = '_'.join('_'.join(link.to_node.name.split(' ')).split('.'))
            f.write(f'links.new({fromNodeName}.outputs[{link.from_node.outputs.values().index(link.from_socket)}], {toNodeName}.inputs[{link.to_node.inputs.values().index(link.to_socket)}])\n')
        
        f.write('\n')
        f.write(f'bpy.data.objects["Cube"].data.materials.append(material)\n')
        f.write(f'bpy.ops.wm.save_as_mainfile(filepath="./material_test.blend")\n')


materialToScript("Material")
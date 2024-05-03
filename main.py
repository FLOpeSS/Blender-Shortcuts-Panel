bl_info = {
    "name": "Shortcut Panel",
    "author": "SleeToo, Flopes",
    "version": (0, 1, 7),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Shortcuts Panel",
    "description": "Some useful shortcuts easily accessible if you can't remember them all ",
    "category": "",
}

import bpy
import bmesh

class ShortcutsPanel(bpy.types.Panel):
    """Creates a panel in the object context"""
    bl_label = "Modifier"
    bl_idname = "OBJECT_PT_shortcuts"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Shortcut Panel"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        operators = [
            "object.bevel_and_smooth", "operator.array", "operator.boolean",
            "operator.mirror", "operator.solidify", "operator.subdivision_surface",
            "operator.displace", "operator.decimate", "operator.shrinkwrap",
            "operator.weighted_normals", "operator.lattice"
        ]
        for operator in operators:
            row = layout.row()
            row.operator(operator)

class ShortcutsPanel2(bpy.types.Panel):
    """Creates a panel in the object context"""
    bl_label = "Selection"
    bl_idname = "OBJECT_PT_shortcuts2"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Shortcut Panel"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        operators = [
            "object.edge_ring", "object.edge_loop",
            "object.grow_selection", "object.shrink_selection"
        ]
        for operator in operators:
            row = layout.row()
            row.operator(operator)

class ShortcutsPanel3(bpy.types.Panel):
    """Creates a panel in the object context"""
    bl_label = "Edit"
    bl_idname = "OBJECT_PT_shortcuts3"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Shortcut Panel"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        operators = [
            "object.merge_distance", "object.bridge_edge", "object.bridge_edge_loop",
            "object.subdivide_edge", "object.grid_fill", "object.loop_cut",
            "object.mark_seam", "object.clear_seam", "object.mark_sharp",
            "object.clear_sharp", "operator.flip_normal", "operator.separate_selection",
            "operator.merge_selected", "operator.knife"
        ]
        for operator in operators:
            row = layout.row()
            row.operator(operator)
        

        

class OBJECT_OT_BevelAndSmooth(bpy.types.Operator):
    bl_idname = "object.bevel_and_smooth"
    bl_label = "Bevel and Smooth"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Adiciona o modificador "Smooth by Angle"
        bpy.ops.object.modifier_add_node_group(asset_library_type="ESSENTIALS", asset_library_identifier="", relative_asset_identifier="geometry_nodes\\smooth_by_angle.blend\\NodeTree\\Smooth by Angle")
        

        if context.mode == 'EDIT_MESH':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.modifier_add(type='BEVEL')
            bpy.context.object.modifiers["Bevel"].limit_method = 'WEIGHT'
            bpy.context.object.modifiers["Bevel"].segments = 2  # Altera os segmentos para 2
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.transform.edge_bevelweight(value=1)
            bpy.ops.object.mode_set(mode='OBJECT')
        else:
            bpy.ops.object.modifier_add(type='BEVEL')
            bpy.context.object.modifiers["Bevel"].segments = 2  # Altera os segmentos para 2
            bpy.context.object.modifiers.new(name="Weighted Normal", type='WEIGHTED_NORMAL')
        
        
        
        return {'FINISHED'}

class Edge_Ring(bpy.types.Operator):
    bl_idname = "object.edge_ring"
    bl_label = "Select Edge Ring"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.loop_multi_select(ring=True)
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        return {'FINISHED'} 
    
    
class Edge_Loop(bpy.types.Operator):
    bl_idname = "object.edge_loop"
    bl_label = "Select Edge Loop" 
    bl_options = {'REGISTER', 'UNDO'}  
    
    def execute(self, context):
        # Switching to EDIT mode to read mesh data
        bpy.ops.object.mode_set(mode = 'EDIT')

        # Get the active mesh
        obj = bpy.context.edit_object
        me = obj.data

        # Get a BMesh from the active mesh
        bm = bmesh.from_edit_mesh(me)

        # Get the selected edges
        selected_edges = [e for e in bm.edges if e.select]

        # Perform the edge loop selection
        for edge in selected_edges:
            # Set the edge as active in the bpy context
            bpy.context.view_layer.objects.active = obj

            # Select the edge loop
            bpy.ops.mesh.loop_multi_select(ring=False)

        # Update the mesh to reflect the changes
        bmesh.update_edit_mesh(me)

        return {'FINISHED'}     


class Merge_Distance(bpy.types.Operator):
    bl_idname = "object.merge_distance"
    bl_label = "Merge by Distance" 
    bl_options = {'REGISTER', 'UNDO'} 

    # Create a FloatProperty for the distance
    distance: bpy.props.FloatProperty(name="Distance", default=0.0001)

    def execute(self, context):
        # Get the active object
        obj = bpy.context.active_object

        # Ensure we're in edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Get the active mesh
        me = obj.data

        # Get a BMesh from the active mesh
        bm = bmesh.from_edit_mesh(me)

        # Get the selected vertices
        selected_verts = [v for v in bm.verts if v.select]

        # Use the built-in "Merge by Distance" operator
        bpy.ops.mesh.remove_doubles(threshold=self.distance)

        # Update the mesh with the new data
        bmesh.update_edit_mesh(me)

        return {'FINISHED'}
    
    
class Grow_Selection(bpy.types.Operator):
    bl_idname = "object.grow_selection"
    bl_label = "Grow Selection"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Check if the active object is a mesh
        if context.object and context.object.type == 'MESH':
            # Set the mode to 'EDIT'
            bpy.ops.object.mode_set(mode='EDIT')

            # Get a BMesh from the active object
            bm = bmesh.from_edit_mesh(context.object.data)

            # Grow the selection
            bpy.ops.mesh.select_more()

            # Update the BMesh
            bmesh.update_edit_mesh(context.object.data)

        else:
            self.report({'WARNING'}, "Active object is not a mesh")
        return {'FINISHED'}
    
class Shrink_Selection(bpy.types.Operator):
    bl_idname = "object.shrink_selection"
    bl_label = "Shrink Selection"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Check if the active object is a mesh
        if context.object and context.object.type == 'MESH':
            # Set the mode to 'EDIT'
            bpy.ops.object.mode_set(mode='EDIT')

            # Get a BMesh from the active object
            bm = bmesh.from_edit_mesh(context.object.data)

            # Shrink the selection
            bpy.ops.mesh.select_less()

            # Update the BMesh
            bmesh.update_edit_mesh(context.object.data)

        else:
            self.report({'WARNING'}, "Active object is not a mesh")
        return {'FINISHED'}
    

class Bridge_Edges(bpy.types.Operator):
    bl_idname = "object.bridge_edge"
    bl_label = "Bridge Edges"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Ensure we're in edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Bridge the selected edge loops
        bpy.ops.mesh.bridge_edge_loops()

        return {'FINISHED'}
    
    
class Bridge_Edge_Loop(bpy.types.Operator):
    bl_idname = "object.bridge_edge_loop"
    bl_label = "Bridge Edge Loops"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Ensure we're in edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Assuming the edges are already selected, perform Bridge Edge Loops operation
        bpy.ops.mesh.bridge_edge_loops()  

        return {'FINISHED'}
           
           

class Subdivide_Edge(bpy.types.Operator):
    bl_idname = "object.subdivide_edge"
    bl_label = "Subdivide Edge"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Get the active object
        obj = bpy.context.object

        # Ensure it's a mesh
        if obj.type == 'MESH':
            # Switch to edit mode
            bpy.ops.object.mode_set(mode='EDIT')

            # Subdivide the selected edges
            bpy.ops.mesh.subdivide()

        return {'FINISHED'}


class Grid_fill(bpy.types.Operator):
    bl_idname = "object.grid_fill"
    bl_label = "Grid Fill"
    bl_options = {'REGISTER', 'UNDO'}

    # Define properties
    span: bpy.props.IntProperty(name="Span", default=2, min=1, max=100)
    offset: bpy.props.IntProperty(name="Offset", default=0, min=0, max=100)

    def execute(self, context):
        # Ensure we're in edit mode
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Perform the fill operation with the specified span and offset
        result = bpy.ops.mesh.fill_grid(span=self.span, offset=self.offset)
        
        # Check if the operation was successful
        if 'FINISHED' in result:
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Fill operation failed. Please check your selection.")
        
        # Always return a set
        return {'CANCELLED'} if 'FINISHED' not in result else {'FINISHED'}
    
    


class Loop_Cut(bpy.types.Operator):
    bl_idname = "object.loop_cut"
    bl_label = "Loop Cut"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Call the Edge_Ring operator
        bpy.ops.object.edge_ring()

        # Call the Subdivide_Edge operator
        bpy.ops.object.subdivide_edge()
        
        # Call the Shrink_Selection operator
        bpy.ops.object.shrink_selection()

        return {'FINISHED'}
    

class Mark_Seam(bpy.types.Operator):
    bl_idname = "object.mark_seam"
    bl_label = "Mark Seam"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self,Operator):
        # Ensure we're in edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Get the active mesh
        obj = bpy.context.active_object
        me = obj.data

        # Create a bmesh from the active mesh
        bm = bmesh.from_edit_mesh(me)

        # Ensure the bmesh edges can be accessed by index
        bm.edges.ensure_lookup_table()

        # Get the selected edges and mark them as a seam
        for e in bm.edges:
            if e.select:
                e.seam = True

        # Update the bmesh to the mesh
        bmesh.update_edit_mesh(me)
        
        return {'FINISHED'}


class Mark_Sharp(bpy.types.Operator):
    bl_idname = "object.mark_sharp"
    bl_label = "Mark Sharp"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, Operator):
        # Ensure we're in edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Get the active mesh
        obj = bpy.context.active_object
        me = obj.data

        # Create a bmesh from the active mesh
        bm = bmesh.from_edit_mesh(me)

        # Ensure the bmesh edges can be accessed by index
        bm.edges.ensure_lookup_table()

        # Get the selected edges and mark them as sharp
        for e in bm.edges:
            if e.select:
                e.smooth = False

        # Update the bmesh to the mesh
        bmesh.update_edit_mesh(me)

        return {'FINISHED'}
    
class Clear_Sharp(bpy.types.Operator):
    bl_idname = "object.clear_sharp"
    bl_label = "Clear Sharp"    
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self,Operator):
        # Ensure we're in edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Get the active mesh
        obj = bpy.context.active_object
        me = obj.data

        # Create a bmesh from the active mesh
        bm = bmesh.from_edit_mesh(me)

        # Ensure the bmesh edges can be accessed by index
        bm.edges.ensure_lookup_table()

        # Get the selected edges and clear sharp
        for e in bm.edges:
            if e.select:
                e.smooth = True

        # Update the bmesh to the mesh
        bmesh.update_edit_mesh(me)
        
        return {'FINISHED'}

class Clear_Seam(bpy.types.Operator):
    bl_idname = "object.clear_seam"
    bl_label = "Clear Seam"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self,Operator):
        # Ensure we're in edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Get the active mesh
        obj = bpy.context.active_object
        me = obj.data

        # Create a bmesh from the active mesh
        bm = bmesh.from_edit_mesh(me)

        # Ensure the bmesh edges can be accessed by index
        bm.edges.ensure_lookup_table()

        # Get the selected edges and clear seams
        for e in bm.edges:
            if e.select:
                e.seam = False

        # Update the bmesh to the mesh
        bmesh.update_edit_mesh(me)
        
        return {'FINISHED'}

class Flip_Normal(bpy.types.Operator):
    bl_idname = "operator.flip_normal"
    bl_label = "Flip Normals" 
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self,Operator):
        # Ensure we're in edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Get the active mesh
        obj = bpy.context.active_object
        me = obj.data

        # Create a bmesh from the active mesh
        bm = bmesh.from_edit_mesh(me)

        # Ensure the bmesh faces can be accessed by index
        bm.faces.ensure_lookup_table()

        # Get the selected faces and flip normals
        for f in bm.faces:
            if f.select:
                f.normal_flip()

        # Update the bmesh to the mesh
        bmesh.update_edit_mesh(me)
        
        return {'FINISHED'}       
    
class Separate_Selection(bpy.types.Operator):
    bl_idname = "operator.separate_selection"
    bl_label = "Separate Selection"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self,Operator):
        # Ensure we're in edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Separate selected geometry into a new mesh
        bpy.ops.mesh.separate(type='SELECTED')    
        
        return {'FINISHED'}
    
class Merge_Selected(bpy.types.Operator):
    bl_idname = "operator.merge_selected"
    bl_label = "Merge Selected"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self,Operator):
        # Get the selected objects
        selected_objects = bpy.context.selected_objects

        # Check if there are at least two objects selected
        if len(selected_objects) < 2:
            print("Please select at least two objects.")
        else:
            # Set the active object to the first selected object
            bpy.context.view_layer.objects.active = selected_objects[0]

            # Join all selected objects
            bpy.ops.object.join()
            
        return {'FINISHED'}
    
class Knife(bpy.types.Operator):
    bl_idname = "operator.knife"
    bl_label = "Knife tool"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self,Operator):
        # Ensure we're in the 3D View context
        bpy.context.area.type = 'VIEW_3D'

        # Change the active tool to the Knife
        bpy.ops.wm.tool_set_by_id(name="builtin.knife")       
        return {'FINISHED'}
    
class Array(bpy.types.Operator):
    bl_idname = "operator.array"
    bl_label = "Array"    
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self,Operator):
        # Get the active object
        obj = bpy.context.active_object

        # Add array modifier
        mod_array = obj.modifiers.new(name="Array", type='ARRAY')

        # Set properties (if any)
        mod_array.count = 3
        mod_array.relative_offset_displace[0] = 1.0  # Offset in the X direction
        return {'FINISHED'}
    
class Boolean(bpy.types.Operator):
    bl_idname = "operator.boolean"
    bl_label = "Boolean"  
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self,Operator):
        # Get the active object
        obj = bpy.context.active_object

        # Add boolean modifier
        mod_boolean = obj.modifiers.new(name="Boolean", type='BOOLEAN')
        return {'FINISHED'}
    

class Mirror(bpy.types.Operator):
    bl_idname = "operator.mirror"
    bl_label = "Mirror"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self,Operator):
        # Get the active object
        obj = bpy.context.active_object

        # Add mirror modifier
        mod_mirror = obj.modifiers.new(name="Mirror", type='MIRROR')

        # Set properties (if any)
        mod_mirror.use_axis = [True, False, False]  # Mirror in the X axis
        return {'FINISHED'} 
    
class Solidify(bpy.types.Operator):
    bl_idname = "operator.solidify"
    bl_label = "Solidify"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self,Operator):
        # Get the active object
        obj = bpy.context.active_object

        # Add solidify modifier
        mod_solidify = obj.modifiers.new(name="Solidify", type='SOLIDIFY')

        # Set properties (if any)
        mod_solidify.thickness = 0.1  # Set the thickness
        return {'FINISHED'}    
    
class Subdivision_Surface(bpy.types.Operator):
    bl_idname = "operator.subdivision_surface"    
    bl_label = "Subdivision Surface"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self,Operator):
        # Get the active object
        obj = bpy.context.active_object

        # Add subdivision surface modifier
        mod_subsurf = obj.modifiers.new(name="Subsurf", type='SUBSURF')

        # Set properties (if any)
        mod_subsurf.levels = 2
        mod_subsurf.render_levels = 2
        return {'FINISHED'} 
    
class Displace(bpy.types.Operator):
    bl_idname = "operator.displace"
    bl_label = "Displace"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self,Operator):
        # Get the active object
        obj = bpy.context.active_object

        # Add displace modifier
        mod_displace = obj.modifiers.new(name="Displace", type='DISPLACE')

        # Set properties (if any)
        mod_displace.strength = 0.5  # Set the strength    
        return {'FINISHED'} 
    
    
class Decimate(bpy.types.Operator):
    bl_idname = "operator.decimate"
    bl_label = "Decimate"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self,Operator):
        # Get the active object
        obj = bpy.context.active_object

        # Add decimate modifier
        mod_decimate = obj.modifiers.new(name="Decimate", type='DECIMATE')

        # Set properties (if any)
        mod_decimate.ratio = 0.5  # Set the ratio
        return {'FINISHED'}          
    
class Shrinkwrap(bpy.types.Operator):
    bl_idname = "operator.shrinkwrap"
    bl_label = "Shrinkwrap"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self,Operator):
        # Check if there are at least two objects selected
        if len(bpy.context.selected_objects) < 2:
            print("Please select at least two objects.")
            return

        # Get the first and second selected objects
        obj = bpy.context.selected_objects[1]
        target_obj = bpy.context.selected_objects[0]

        # Add Shrinkwrap modifier to the first selected object
        mod_shrinkwrap = obj.modifiers.new(name="Shrinkwrap", type='SHRINKWRAP')

        # Set the second selected object as the target
        mod_shrinkwrap.target = target_obj
        return {'FINISHED'}
    
    
class Weighted_Normals(bpy.types.Operator):
    bl_idname = "operator.weighted_normals"
    bl_label = "Weighted_Normals"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self,Operator):
        # Get the active object
        obj = bpy.context.active_object

        # Add Weighted Normals modifier
        mod_weighted_normals = obj.modifiers.new(name="Weighted Normals", type='WEIGHTED_NORMAL')

        # Set properties (if any)
        mod_weighted_normals.keep_sharp = True  # Keep sharp edges
        return {'FINISHED'}
    
    
class Lattice(bpy.types.Operator):
    bl_idname = "operator.lattice"
    bl_label = "Lattice" 
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self,Operator):
        # Get the active object
        obj = bpy.context.active_object

        # Add Lattice modifier
        mod_lattice = obj.modifiers.new(name="Lattice", type='LATTICE') 
        return {'FINISHED'}  
    
    


def register():
    classes = [ShortcutsPanel, ShortcutsPanel2, ShortcutsPanel3, OBJECT_OT_BevelAndSmooth, Edge_Ring, Edge_Loop, Merge_Distance, Grow_Selection, Shrink_Selection, Bridge_Edges,
               Bridge_Edge_Loop, Subdivide_Edge, Grid_fill, Loop_Cut, Mark_Seam, Clear_Seam, Mark_Sharp, Clear_Sharp, Flip_Normal, Separate_Selection, Merge_Selected, Knife, Array, Boolean,
               Mirror, Solidify, Subdivision_Surface, Displace, Decimate, Shrinkwrap, Weighted_Normals, Lattice]

    for cls in classes:
        if cls._name_ not in bpy.types._dict_:
            bpy.utils.register_class(cls)

def unregister():
    classes = [ShortcutsPanel, ShortcutsPanel2, ShortcutsPanel3, OBJECT_OT_BevelAndSmooth, Edge_Ring, Edge_Loop, Merge_Distance, Grow_Selection, Shrink_Selection, Bridge_Edges,
               Bridge_Edge_Loop, Subdivide_Edge, Grid_fill, Loop_Cut, Mark_Seam, Clear_Seam, Mark_Sharp, Clear_Sharp, Flip_Normal, Separate_Selection, Merge_Selected, Knife, Array, Boolean,
               Mirror, Solidify, Subdivision_Surface, Displace, Decimate, Shrinkwrap, Weighted_Normals, Lattice]
    for cls in classes:
        if cls._name_ in bpy.types._dict_:
            bpy.utils.unregister_class(cls)



if _name_ == "_main_":
    register()

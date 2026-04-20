import bpy
import math

# Clear existing mesh/armature objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Create armature
bpy.ops.object.armature_add(enter_editmode=True)
armature = bpy.context.object
armature.name = "GoofyHorse_Rig"
bpy.ops.object.mode_set(mode='EDIT')
bones = armature.data.edit_bones

# Create root bone (for moving the whole horse)
root = bones[0]
root.name = "Root"
root.head = (0, 0, 0)
root.tail = (0, 0, 0.2)

# Body bone (chest)
body = bones.new("Body")
body.head = (0, 0, 0.3)
body.tail = (0.8, 0, 0.3)
body.parent = root

# Neck and Head (goofy long neck)
neck = bones.new("Neck")
neck.head = (0.7, 0, 0.35)
neck.tail = (1.1, 0, 0.5)
neck.parent = body

head = bones.new("Head")
head.head = (1.05, 0, 0.5)
head.tail = (1.3, 0, 0.55)
head.parent = neck

# Front left leg
FL_upper = bones.new("FL_Upper")
FL_upper.head = (0.3, -0.25, 0.3)
FL_upper.tail = (0.3, -0.25, 0.0)
FL_upper.parent = body

FL_lower = bones.new("FL_Lower")
FL_lower.head = (0.3, -0.25, 0.0)
FL_lower.tail = (0.3, -0.25, -0.4)
FL_lower.parent = FL_upper

# Front right leg
FR_upper = bones.new("FR_Upper")
FR_upper.head = (0.3, 0.25, 0.3)
FR_upper.tail = (0.3, 0.25, 0.0)
FR_upper.parent = body

FR_lower = bones.new("FR_Lower")
FR_lower.head = (0.3, 0.25, 0.0)
FR_lower.tail = (0.3, 0.25, -0.4)
FR_lower.parent = FR_upper

# Back left leg
BL_upper = bones.new("BL_Upper")
BL_upper.head = (0.65, -0.25, 0.3)
BL_upper.tail = (0.65, -0.25, 0.0)
BL_upper.parent = body

BL_lower = bones.new("BL_Lower")
BL_lower.head = (0.65, -0.25, 0.0)
BL_lower.tail = (0.65, -0.25, -0.4)
BL_lower.parent = BL_upper

# Back right leg
BR_upper = bones.new("BR_Upper")
BR_upper.head = (0.65, 0.25, 0.3)
BR_upper.tail = (0.65, 0.25, 0.0)
BR_upper.parent = body

BR_lower = bones.new("BR_Lower")
BR_lower.head = (0.65, 0.25, 0.0)
BR_lower.tail = (0.65, 0.25, -0.4)
BR_lower.parent = BR_upper

# Tail (extra goofy)
tail = bones.new("Tail")
tail.head = (-0.05, 0, 0.32)
tail.tail = (-0.5, 0, 0.28)
tail.parent = body

# Exit edit mode
bpy.ops.object.mode_set(mode='OBJECT')

# Create 2D planes with materials


def create_plane(name, location, scale_x, scale_y, bone_name):
    bpy.ops.mesh.primitive_plane_add(size=1, location=location)
    plane = bpy.context.active_object
    plane.name = name
    plane.scale = (scale_x, scale_y, 1)

    # Material with placeholder color
    mat = bpy.data.materials.new(name=f"{name}_Material")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]

    # Assign different placeholder colors for visual clarity
    colors = {
        "Body": (0.6, 0.4, 0.2, 1),
        "Head": (0.5, 0.3, 0.1, 1),
        "Neck": (0.55, 0.35, 0.15, 1),
        "Tail": (0.3, 0.2, 0.1, 1),
    }
    color = colors.get(name, (0.4, 0.3, 0.2, 1))
    bsdf.inputs['Base Color'].default_value = color

    # Add texture node placeholder note
    tex_node = mat.node_tree.nodes.new('ShaderNodeTexImage')
    tex_node.location = (-300, 300)
    tex_node.label = f"Load {name} image here"

    if plane.data.materials:
        plane.data.materials[0] = mat
    else:
        plane.data.materials.append(mat)

    # Parent to bone
    plane.select_set(True)
    armature.select_set(True)
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.parent_set(type='BONE_RELATIVE')

    # Assign to specific bone
    vertex_group = plane.vertex_groups.new(name=bone_name)
    vertex_group.add(range(len(plane.data.vertices)), 1.0, 'REPLACE')

    return plane


# Create all parts
parts = [
    ("Body", (0.4, 0, 0.35), 0.9, 0.6, "Body"),
    ("Head", (1.2, 0, 0.55), 0.5, 0.45, "Head"),
    ("Neck", (0.9, 0, 0.44), 0.4, 0.35, "Neck"),
    ("FL_Upper", (0.3, -0.25, 0.15), 0.25, 0.5, "FL_Upper"),
    ("FL_Lower", (0.3, -0.25, -0.2), 0.22, 0.5, "FL_Lower"),
    ("FR_Upper", (0.3, 0.25, 0.15), 0.25, 0.5, "FR_Upper"),
    ("FR_Lower", (0.3, 0.25, -0.2), 0.22, 0.5, "FR_Lower"),
    ("BL_Upper", (0.65, -0.25, 0.15), 0.25, 0.5, "BL_Upper"),
    ("BL_Lower", (0.65, -0.25, -0.2), 0.22, 0.5, "BL_Lower"),
    ("BR_Upper", (0.65, 0.25, 0.15), 0.25, 0.5, "BR_Upper"),
    ("BR_Lower", (0.65, 0.25, -0.2), 0.22, 0.5, "BR_Lower"),
    ("Tail", (-0.25, 0, 0.33), 0.2, 0.45, "Tail"),
]

for name, loc, sx, sy, bone in parts:
    create_plane(name, loc, sx, sy, bone)

# --- WALKING ANIMATION ---
bpy.context.view_layer.objects.active = armature
bpy.ops.object.mode_set(mode='POSE')

# Clear any existing animation
# for bone in armature.pose.bones:
#    bone.animation_data_clear()

# Walk cycle parameters
frames_per_step = 12  # 12 frames per step = 2 steps per second at 24fps
total_frames = 48     # 2 full steps (left-right cycle)


def walk_cycle(frame):
    # Normalized position in cycle (0 to 1)
    t = (frame % total_frames) / total_frames

    # Body bounce (goofy up-down)
    body_height = 0.05 * math.sin(t * math.pi * 2)
    armature.pose.bones["Body"].location = (0, 0, body_height)
    armature.pose.bones["Body"].keyframe_insert(data_path="location", index=-1)

    # Head bob and tilt (goofy)
    head_rotation_z = 0.15 * math.sin(t * math.pi * 4)  # faster wobble
    head_rotation_x = 0.1 * math.sin(t * math.pi * 2)
    armature.pose.bones["Head"].rotation_euler = (
        head_rotation_x, 0, head_rotation_z)
    armature.pose.bones["Head"].keyframe_insert(
        data_path="rotation_euler", index=-1)

    # Neck stretch (goofy)
    neck_rotation = 0.08 * math.sin(t * math.pi * 2)
    armature.pose.bones["Neck"].rotation_euler = (neck_rotation, 0, 0)
    armature.pose.bones["Neck"].keyframe_insert(
        data_path="rotation_euler", index=-1)

    # Tail wag (side to side)
    tail_rotation = 0.5 * math.sin(t * math.pi * 8)  # fast wag
    armature.pose.bones["Tail"].rotation_euler = (0, tail_rotation, 0)
    armature.pose.bones["Tail"].keyframe_insert(
        data_path="rotation_euler", index=-1)

    # Leg phase: front legs move opposite to back legs (like real horse trot)
    # Phase shift for diagonal pairs
    phase = t * math.pi * 2

    # Front Left (forward when phase 0-180)
    fl_phase = math.sin(phase)
    fl_angle = max(-0.8, min(0.8, fl_phase * 0.7))
    armature.pose.bones["FL_Upper"].rotation_euler = (fl_angle, 0, 0)
    armature.pose.bones["FL_Upper"].keyframe_insert(
        data_path="rotation_euler", index=-1)

    # Front Right (opposite phase)
    fr_phase = math.sin(phase + math.pi)
    fr_angle = max(-0.8, min(0.8, fr_phase * 0.7))
    armature.pose.bones["FR_Upper"].rotation_euler = (fr_angle, 0, 0)
    armature.pose.bones["FR_Upper"].keyframe_insert(
        data_path="rotation_euler", index=-1)

    # Back Left (same as front right for trot)
    bl_phase = math.sin(phase + math.pi)
    bl_angle = max(-0.8, min(0.8, bl_phase * 0.7))
    armature.pose.bones["BL_Upper"].rotation_euler = (bl_angle, 0, 0)
    armature.pose.bones["BL_Upper"].keyframe_insert(
        data_path="rotation_euler", index=-1)

    # Back Right (same as front left)
    br_phase = math.sin(phase)
    br_angle = max(-0.8, min(0.8, br_phase * 0.7))
    armature.pose.bones["BR_Upper"].rotation_euler = (br_angle, 0, 0)
    armature.pose.bones["BR_Upper"].keyframe_insert(
        data_path="rotation_euler", index=-1)

    # Lower legs (follow upper with delay for "floppy" look)
    fl_lower_angle = fl_angle * 0.5 + 0.2 * math.sin(phase * 2)
    armature.pose.bones["FL_Lower"].rotation_euler = (fl_lower_angle, 0, 0)
    armature.pose.bones["FL_Lower"].keyframe_insert(
        data_path="rotation_euler", index=-1)

    fr_lower_angle = fr_angle * 0.5 + 0.2 * math.sin((phase + math.pi) * 2)
    armature.pose.bones["FR_Lower"].rotation_euler = (fr_lower_angle, 0, 0)
    armature.pose.bones["FR_Lower"].keyframe_insert(
        data_path="rotation_euler", index=-1)

    bl_lower_angle = bl_angle * 0.5 + 0.2 * math.sin((phase + math.pi) * 2)
    armature.pose.bones["BL_Lower"].rotation_euler = (bl_lower_angle, 0, 0)
    armature.pose.bones["BL_Lower"].keyframe_insert(
        data_path="rotation_euler", index=-1)

    br_lower_angle = br_angle * 0.5 + 0.2 * math.sin(phase * 2)
    armature.pose.bones["BR_Lower"].rotation_euler = (br_lower_angle, 0, 0)
    armature.pose.bones["BR_Lower"].keyframe_insert(
        data_path="rotation_euler", index=-1)


# Generate keyframes for each frame
for frame in range(total_frames + 1):
    bpy.context.scene.frame_set(frame)
    walk_cycle(frame)

# Set animation range
bpy.context.scene.frame_start = 0
bpy.context.scene.frame_end = total_frames
bpy.context.scene.render.fps = 24

# Add a moving floor reference (optional)
bpy.ops.mesh.primitive_grid_add(size=5, location=(0.4, 0, -0.6))
floor = bpy.context.active_object
floor.name = "Ground"
floor_mat = bpy.data.materials.new("GroundMaterial")
floor_mat.use_nodes = True
floor_mat.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = (
    0.2, 0.6, 0.2, 1)
floor.data.materials.append(floor_mat)

# Return to object mode
bpy.ops.object.mode_set(mode='OBJECT')

print("=" * 50)
print("✓ GOOFY HORSE with WALK CYCLE created!")
print("=" * 50)
print("\nTo add YOUR horse images:")
print("1. Select a body part (Body, Head, FL_Upper, etc.)")
print("2. Go to Material Properties → Use Nodes")
print("3. Add an Image Texture node")
print("4. Load your horse part PNG")
print("5. Connect to Base Color")
print("6. Set Blend Mode to 'Alpha Blend' if needed")
print("\nAnimation controls:")
print("- Press Spacebar to play the walk cycle")
print("- Adjust 'frames_per_step' variable for faster/slower walk")
print("- Modify 'total_frames' for longer animation")
print("\nMake it even GOOFIER:")
print("- Increase head_rotation_z to 0.3 for floppy head")
print("- Increase tail_rotation to 0.8 for crazy wagging")
print("- Add noise modifiers to bones for random wobble")
print("=" * 50)

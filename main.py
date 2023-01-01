#   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *
# 
# Name: algorithm demo
# Version (date): 2021_06_04
# Author: Moshnyakov Anton
# E-mail: anton.source@gmail.com
# 
#   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *





import bpy
import math
from random import randint, choice
from pathlib import Path

# Two way for script running:
# 
# 1 Write in console:
# blender --background --python main.py
# where "blender" is directory of executable file of Blender
# in PATH in Environment variable
# (Win + R > SystemPropertiesAdvanced > Environment variable)
# 
# 2 Or open file "start.blend" and click on Run Script (Alt + P)

# Blender's constants
C = bpy.context
D = bpy.data
O = bpy.ops

# Output directory in variable PATH_OUT between ''
# Example for output directory in Windows D:\py\out is:
# PATH_OUT = r'D:\py\out'
PATH_OUT = r'C:\py\out'

# Set hand-picked number X_NUM
X_NUM = 15

# Set number of objects
NUM_OBJS = 64

# Set number of objects in row/col
M_SIZE = 8

# Steps in Algorithm of searching hand-picked number X_NUM
STEPS = int(1 + math.log(NUM_OBJS, 2))
print("Maximum number of steps: " + str(STEPS) + "\n")

# Set dimensions of frames
FR_DIM_X = 1080
FR_DIM_Y = 1080

# Set step
STEP_ = 72

# Set timeline (if FR_START = 1, so FR_END will define number of frames):
FR_START = 1
# FR_END = STEP_*STEPS
FR_END = 2

# Activating show telemetry:
TELEMETRY_SHOW = True

# Activating animation:
ANIM = False


def degrees_to_radians(x,y,z):
    x = math.radians(x)
    y = math.radians(y)
    z = math.radians(z)
    return (x,y,z)


def del_all_objs():
    O.object.select_all(action='SELECT')
    O.object.delete(use_global=False,confirm=False)
    while len(D.meshes) != 0:
        D.meshes.remove(D.meshes[0])
    while len(D.materials) != 0:
        D.materials.remove(D.materials[0])
    while len(D.textures) != 0:
        D.textures.remove(D.textures[0])
    while len(D.images) != 0:
        D.images.remove(D.images[0])
    while len(D.lights) != 0:
        D.lights.remove(D.lights[0])
    while len(D.curves) != 0:
        D.curves.remove(D.curves[0])


def camera_add(x,y,z,rx,ry,rz,type_='PERSP'):
    O.object.camera_add(
        align = 'VIEW',
        location = (x,y,z),
        rotation = degrees_to_radians(rx,ry,rz))
    C.scene.camera = D.objects[C.active_object.name]
    if type_ == 'ORTHO':
        C.object.data.ortho_scale = 23
        C.object.data.type = 'ORTHO'
    else:
        C.object.data.type = 'PERSP'
    return C.active_object.name


def light_add(name_type,x,y,z,energy_=80000,r=1,g=1,b=1):
    O.object.light_add(type = name_type,location = (x,y,z))
    C.object.data.color = (r,g,b)
    C.object.data.energy = energy_

    if name_type == 'AREA':
        C.object.data.size = 50
    return C.active_object.name


def export_image_settings(start_,end_,x,y,render_samples,stamp,anim):
    C.scene.render.fps = 24
    C.scene.render.fps_base = 1
    C.scene.frame_start = start_
    C.scene.frame_end = end_
    C.scene.render.use_file_extension = True
    if anim == True:
        C.scene.render.image_settings.file_format = 'AVI_JPEG'
    else:
        C.scene.render.image_settings.file_format = 'JPEG'
    C.scene.eevee.taa_render_samples = render_samples
    C.scene.render.resolution_x = x
    C.scene.render.resolution_y = y
    C.scene.render.resolution_percentage = 100
    C.scene.render.image_settings.quality = 100
    C.scene.render.use_stamp = stamp
    C.scene.render.use_stamp_date = False
    C.scene.render.use_stamp_time = False
    C.scene.render.use_stamp_render_time = False
    C.scene.render.use_stamp_frame = False
    C.scene.render.use_stamp_camera = False
    C.scene.render.use_stamp_scene = False
    C.scene.render.use_stamp_filename = False
    C.scene.render.stamp_font_size = 16 # 20
    C.scene.render.stamp_foreground = (0,0,0,1)
    C.scene.render.stamp_background = (1,1,1,0.25)
    C.scene.render.use_stamp_note = True


def world_color(r=1,g=1,b=1,strength_=1):
    world = D.worlds['World'].node_tree.nodes['Background']
    world.inputs[0].default_value = (r,g,b,1)
    world.inputs[1].default_value = strength_
    C.scene.eevee.use_soft_shadows = True   # soft shadows


def rgb_rand(start,end):
    r = randint(start,end)*0.001
    g = randint(start,end)*0.001
    b = randint(start,end)*0.001

    # bicycle
    # for not gray colors
    dif = 0.05
    while ((b >= (r - dif) and b <=(r + dif))
        and (b >= (g - dif) and b <= (g + dif))):
        b = randint(start,end)*0.001
    return [r,g,b]


def rigidbody_for_obj(obj,shape,kinematic_,kg):
    O.rigidbody.object_add()
    obj.rigid_body.type = 'ACTIVE'
    obj.rigid_body.collision_shape = shape
    obj.rigid_body.kinematic = kinematic_
    obj.rigid_body.mesh_source = 'BASE'
    obj.rigid_body.collision_margin = 1
    obj.rigid_body.mass = kg
    obj.rigid_body.use_margin = True


def mat_for_obj(
    obj,
    mat_name,
    rgba = [1,1,1,1],
    shader = 'Principled BSDF',
    blend_method = 'BLEND',
    alpha = 1):
    mat = D.materials.new(name = mat_name)
    mat.use_nodes = True
    mat.node_tree.nodes.new('ShaderNodeEmission')
    mat.blend_method = blend_method
    if blend_method == 'BLEND':
        mat.use_backface_culling = False
        mat.show_transparent_back = False   # show backface
    mat_in = mat.node_tree.nodes.get(shader)
    mat_out = mat.node_tree.nodes.get('Material Output')
    node_links = mat.node_tree.links.new
    if shader == 'Principled BSDF':
        mat_in.inputs[0].default_value = rgba
        mat_in.inputs[5].default_value = 0
        mat_in.inputs[7].default_value = 1
        mat_in.inputs[18].default_value = 0
        mat_in.inputs[19].default_value = alpha
        out_name = 'BSDF'
    elif shader == 'Emission':
        mat_in.inputs['Color'].default_value = rgba
        mat_in.inputs['Strength'].default_value = 1
        out_name = 'Emission'
    node_links(mat_out.inputs['Surface'],mat_in.outputs[out_name])
    obj.active_material = mat


def mod_apply_bevel(obj,width_,segments_):
    O.object.modifier_add(type = 'BEVEL')
    obj.modifiers['Bevel'].width = width_
    obj.modifiers['Bevel'].segments = segments_
    O.object.modifier_apply(modifier='Bevel',report=True)


def mod_apply_subsurf(obj,levels_,render_levels_):
    O.object.modifier_add(type='SUBSURF')
    obj.modifiers['Subdivision'].levels = levels_
    obj.modifiers['Subdivision'].render_levels = render_levels_
    O.object.modifier_apply(modifier='Subdivision',report=True)


def cube():
    name = 'cube'
    min_size = 10
    max_size = 28
    return [name,min_size,max_size]


def arr_xyz(obj,arr_size,numObj,m_size):
    arr_x = []
    arr_y = []
    arr_z = []
    border = x = y = z = -arr_size + (arr_size/m_size)
    for i in range(numObj):
        arr_x.append(x)
        arr_y.append(y)
        arr_z.append(z)
        if x < -border:
            x += arr_size*2/m_size
        elif y < -border:
            x = border
            y += arr_size*2/m_size
        elif z < -border:
            x = border
            y = border
            z += arr_size*2/m_size

    return [arr_x,arr_y,arr_z]


def obj_add(obj_type,o_size,xyz,rx=0,ry=0,rz=0):
    if obj_type == 'cube':
        O.mesh.primitive_cube_add(
            size=o_size,
            location=xyz,
            rotation=(rx,ry,rz))
    elif obj_type == 'sphere':
        O.mesh.primitive_uv_sphere_add(
            radius=o_size,
            location=xyz,
            rotation=(rx,ry,rz))
    elif obj_type == 'torus':
        O.mesh.primitive_torus_add(
            location=xyz,
            major_segments=40,
            major_radius=o_size,
            minor_radius=o_size/4,
            rotation=(rx,ry,rz))
    elif obj_type == 'cone':
        O.mesh.primitive_cone_add(
            vertices=3,
            radius1=o_size,
            depth=o_size*1.5,
            location=xyz,
            rotation=(rx,ry,rz))

    ob = C.active_object
    r = randint(200,1000)*0.001
    g = randint(200,1000)*0.001
    b = randint(200,1000)*0.001
    mat_for_obj(ob,'Mat',[r,g,b,0])
    rigidbody_for_obj(ob,'CONVEX_HULL',True,100)

    # add modifiers
    if obj_type == 'cube':
        mod_apply_bevel(ob,round(o_size)*0.1,1)
        mod_apply_subsurf(ob,3,3)
    elif obj_type == 'cone':
        mod_apply_bevel(ob,o_size/4,4)
        mod_apply_subsurf(ob,3,3)
    elif obj_type == 'sphere':
        mod_apply_subsurf(ob,1,1)
    elif obj_type == 'torus':
        mod_apply_subsurf(ob,1,1)
    O.object.shade_smooth()

def font_object(
    name_,
    text_,
    loc_,
    alignX = 'CENTER',
    alignY = 'CENTER',
    scale_ = (1,1,1),
    rot=(0,0,0)):
    font_curve = D.curves.new(type="FONT", name=name_)
    font_curve.align_x = alignX
    font_curve.align_y = alignY
    font_curve.body = text_
    
    obj_name = name_ + "Obj"
    font_obj = D.objects.new(obj_name, font_curve)
    font_obj.location = loc_
    font_obj.scale = scale_
    rot_x = math.radians(rot[0])
    rot_y = math.radians(rot[1])
    rot_z = math.radians(rot[2])
    font_obj.rotation_euler = (rot_x,rot_y,rot_z)
    C.scene.collection.objects.link(font_obj)


def step_in_circle(st_,fr_,st_txt_):
    if fr_ > STEP_+st_*STEP_:
        st_txt_.body = str(st_+1)


def update_steps_in_circle(self):
    step_txt = D.curves["FontCubes"]
    step_txt.body = str(0)
    frame_ = C.scene.frame_current
    for i in range(-1,6):
        step_in_circle(i, frame_,step_txt)


del_all_objs()

light_add('POINT',0,0,-32,50000)

camera_add(0,0,-29,180,0,0,'ORTHO')

world_color()

export_image_settings(
    FR_START,
    FR_END,
    FR_DIM_X,
    FR_DIM_Y,
    32,
    TELEMETRY_SHOW,
    ANIM) # 64


# create big Cube scene
O.mesh.primitive_cube_add(size=500)
cube_ = C.active_object
rigidbody_for_obj(cube_, 'MESH', True, 100)
mat_for_obj(cube_, 'Mat_big_cube',[0.1,0.1,0.2,1],blend_method='OPAQUE')
mod_apply_bevel(cube_, 1, 1)
mod_apply_subsurf(cube_, 3, 3)
O.object.shade_smooth()


# add step number in circle
font_object(
    "FontCubes",
    "0",
    (-10.25,-10.25,-10.2),
    scale_=(1,1,1),
    rot=(180,0,0))
ob_font = D.objects['FontCubesObj']
mat_for_obj(ob_font,'Mat_text', [1,1,1,1])

O.mesh.primitive_circle_add(
    enter_editmode=True,
    location=(-10.25,-10.25,-10.1),
    radius=0.8)
O.mesh.edge_face_add()
O.object.editmode_toggle()
ob_cir = D.objects['Circle']
mat_for_obj(ob_cir,'Mat_cir',[0,0,0,1],alpha=0.5)

bpy.app.handlers.frame_change_post.append(update_steps_in_circle)


# generate array of small objects XY-positions in Cube scene
OBJ = cube()
area_size = 10
ar = arr_xyz(OBJ, area_size,NUM_OBJS,M_SIZE)


# add small cubes in array
for i in range(NUM_OBJS):
    if M_SIZE >= 16:
        obj_size = 0.7
    elif M_SIZE >= 8 and M_SIZE <= 15:
        obj_size = 1.6
    elif M_SIZE >= 4 and M_SIZE <= 7:
        obj_size = 3
    elif M_SIZE <= 2:
        obj_size = 6
    xyz = [ar[0][i],ar[1][i],ar[2][i]]
    rx_ = math.radians(randint(0,359))
    ry_ = math.radians(randint(0,359))
    rz_ = 0
    obj_add(OBJ[0],obj_size,xyz,rx_,ry_,rz_)
    print(str(i)+' '+OBJ[0])
    font_object(
        "FontCubes",
        str(i+1),
        (ar[0][i],ar[1][i],-11.4),
        scale_=(0.9,0.9,1),
        rot=(180,0,0))


# flow and color small cubes
FR_END_ico = FR_END + STEP_
for i in range(FR_START,FR_END_ico,STEP_):
    rad = int(i/3)
    for j in range(1, NUM_OBJS+1):
        j_ = str(j)
        j_ = j_.zfill(3)
        obj_ = D.objects['Cube.'+j_]
        obj_.rotation_euler[2] = math.radians(rad)
        obj_.location[0] = ar[0][j-1]
        obj_.keyframe_insert(data_path='location',frame=1)
        obj_.keyframe_insert(data_path='rotation_euler',frame=i)
    
        j_mat = j-1
        j_mat_ = str(j_mat)
        j_mat_ = j_mat_.zfill(3)
        if j_mat != 0:
            mat_ = D.materials['Mat.'+j_mat_].node_tree.nodes['Principled BSDF']
        else:
            mat_ = D.materials['Mat'].node_tree.nodes['Principled BSDF']
        mat_.inputs[0].default_value = (0.27,0.5,0.8,1)
    

# Material of X_NUM
x_mat = X_NUM-1
x_ = str(x_mat)
x_ = x_.zfill(3)
if X_NUM != 1:
    mat = D.materials['Mat.'+x_]
else:
    mat = D.materials['Mat']
mat.use_nodes = False
mat.diffuse_color = (0.27,0.5,0.8,1)
mat.keyframe_insert(data_path='diffuse_color',frame=1)
mat.keyframe_insert(data_path='diffuse_color',frame=STEP_-STEP_*0.75)
mat.diffuse_color = (0.1,0.9,0.15,1)
mat.keyframe_insert(data_path='diffuse_color',frame=STEP_)


# Array with numbers
arr = [0]*NUM_OBJS
for i in range(NUM_OBJS):
    arr[i] = i+1


guess_num = 0
count = 0
while (guess_num != X_NUM):
    guess_num = arr[int(len(arr)/2)-1]
    if guess_num > X_NUM:
        low_del = int(len(arr)/2)
        high_del = int(len(arr))
        arr_del = arr[low_del:high_del]
    elif guess_num == X_NUM:
        low_del = 0
        high_del = int(len(arr))
        arr_del = arr[low_del:high_del]
        for j in arr_del:
            if j == X_NUM:
                arr_del.remove(j)
    else:
        low_del = 0
        high_del = int(len(arr)/2)
        arr_del = arr[low_del:high_del]
    del arr[low_del:high_del]
    for j in arr_del:
        j_ = str(j)
        j_ = j_.zfill(3)
        obj_ = D.objects['Cube.'+j_]
        font_obj = D.objects["FontCubesObj."+j_]
        
        font_obj.location = (ar[0][j-1],ar[1][j-1],-10.2)
        font_obj.keyframe_insert(data_path='location',frame=STEP_+count*STEP_)
        obj_.location = (ar[0][j-1],ar[1][j-1],ar[2][j-1])
        obj_.keyframe_insert(data_path='location',frame=STEP_+count*STEP_)

        font_obj.location = (300,ar[1][j-1],-10.2)
        font_obj.keyframe_insert(data_path='location',frame=STEP_*2+count*STEP_)
        obj_.location = (300,ar[1][j-1],ar[2][j-1])
        obj_.keyframe_insert(data_path='location',frame=STEP_*2+count*STEP_)
    count += 1
    

path_out = PATH_OUT + '\\'
file_out = 'fr'
path_file = Path(path_out, file_out)
C.scene.render.filepath = str(path_file)
O.render.render(animation = True)

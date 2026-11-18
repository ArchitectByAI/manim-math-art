"""ArchitectByAI Batch 02 / Episode 04: 3D creation studio.

Generate a genuinely animated 3D sequence, with no people and no physical books.
Requires Blender 4.3+.  Captions are composited by render_release.py.
"""
import bpy
import math
import random
import os
from mathutils import Vector
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "frames"
OUTPUT.mkdir(exist_ok=True)

FPS = 12
DURATION = 16

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.eevee.taa_render_samples = 8
scene.render.resolution_x = 540
scene.render.resolution_y = 960
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.film_transparent = False
scene.render.fps = FPS
scene.frame_start = 1
scene.frame_end = FPS * DURATION
scene.render.filepath = str(OUTPUT / "frame_")

world = bpy.data.worlds.new('Deep midnight atmosphere')
scene.world = world
world.use_nodes = True
world.node_tree.nodes['Background'].inputs['Color'].default_value = (0.006, 0.007, 0.024, 1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.4

def material(name, color, metallic=0, roughness=.4, emission=0):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (*color, 1)
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness
    if emission:
        bsdf.inputs['Emission Color'].default_value = (*color, 1)
        bsdf.inputs['Emission Strength'].default_value = emission
    return mat

NAVY = material('Anodized midnight aluminum', (.025,.042,.095), .75, .24)
BLACK = material('Obsidian glass', (.009,.011,.027), .5, .18)
SCREEN = material('Active luminous screen', (.018,.030,.070), .04, .23, .17)
GOLD = material('Warm champagne gold', (.95,.57,.20), .45, .2, 1.6)
ROSE = material('Aurora rose', (.94,.31,.52), .25, .2, 1.0)
CYAN = material('Liquid cyan', (.11,.67,.80), .25, .19, 1.3)
VIOLET = material('Digital lavender', (.53,.35,.96), .23, .2, 1.3)
WHITE = material('Pearl typography', (.89,.90,.98), .1, .3, .4)
SHADOW = material('Stage floor', (.012,.015,.037), .17, .35)

def cube(name, location, scale, mat, bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    ob = bpy.context.object
    ob.name = name
    ob.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    ob.data.materials.append(mat)
    if bevel:
        mod = ob.modifiers.new('soft machined edges', 'BEVEL')
        mod.width = bevel
        mod.segments = 3
        mod2=ob.modifiers.new('weighted normals','WEIGHTED_NORMAL')
    return ob

def curve(name, pts, mat, bevel=.012):
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '3D'
    cu.bevel_depth = bevel
    cu.bevel_resolution = 3
    spline=cu.splines.new('POLY')
    spline.points.add(len(pts)-1)
    for point, co in zip(spline.points,pts):
        point.co=(*co,1)
    ob=bpy.data.objects.new(name,cu)
    bpy.context.collection.objects.link(ob)
    ob.data.materials.append(mat)
    return ob

def text(name, body, location, size, mat, align='LEFT'):
    cu = bpy.data.curves.new(name, 'FONT')
    cu.body = body
    cu.size = size
    cu.align_x=align
    cu.extrude = .0006
    ob=bpy.data.objects.new(name,cu)
    bpy.context.collection.objects.link(ob)
    ob.location=location
    ob.data.materials.append(mat)
    # Blender's text lies in XY by default; rotate so it faces camera (towards -Y)
    ob.rotation_euler=(math.pi/2,0,0)
    return ob

def key_visibility(ob, start, end=None, initial=.001, final=1):
    startf=int(start*FPS)+1
    ob.scale = (initial,)*3
    ob.keyframe_insert(data_path='scale',frame=max(1,startf-14))
    ob.scale = (final,)*3
    ob.keyframe_insert(data_path='scale',frame=startf+11)
    if end is not None:
        ob.keyframe_insert(data_path='scale',frame=int(end*FPS))
        ob.scale=(.001,)*3
        ob.keyframe_insert(data_path='scale',frame=int((end+.5)*FPS))

def animate_loc(ob, a, b, ta, tb):
    ob.location=Vector(a)
    ob.keyframe_insert(data_path='location',frame=int(ta*FPS)+1)
    ob.location=Vector(b)
    ob.keyframe_insert(data_path='location',frame=int(tb*FPS)+1)

floor=cube('Infinite studio floor', (0,0,-.63), (19,19,.16),SHADOW)
cube('Laptop lower plate', (0,-.57,-.14), (3.6,2.35,.13),NAVY,.11)
cube('Laptop keyboard inset', (0,-.65,-.061), (2.98,1.6,.016),BLACK,.09)
for row in range(4):
    for col in range(12):
        key=cube(f'Key {row}-{col}',(-1.40+col*.254,-1.35+row*.31,-.047),(.204,.205,.006),NAVY,.024)
        key_visibility(key,1.6+col*.028+row*.05)

# The screen is a true vertical device, not a rectangle pasted onto a slide.
screen_rig=bpy.data.objects.new('Tilting laptop display',None)
bpy.context.collection.objects.link(screen_rig)
screen_rig.location=(0,.43,-.06)
screen_rig.rotation_euler.x=math.radians(17)
def in_screen(ob):
    # XY-local rectangles have front faces towards the viewer when rotated.
    ob.parent=screen_rig
    ob.matrix_parent_inverse=screen_rig.matrix_world.inverted()

display=cube('Laptop active display',(0,.40,1.18),(3.50,.085,2.60),NAVY,.07)
in_screen(display)
glass=cube('Deep glass workspace',(0,.342,1.18),(3.26,.018,2.33),SCREEN,.036)
in_screen(glass)
key_visibility(display,.25)
key_visibility(glass,1.35)

title=text('Software heading','PROJECT / 001',(-1.36,.318,2.12),.14,WHITE)
in_screen(title)
key_visibility(title,2.1)
for i, mat in enumerate((ROSE,GOLD,CYAN)):
    # Work panels visibly assemble into a full product design.
    x=-.98+i*.93
    card=cube(f'Creative tile {i}',(x,.30,1.18),(.76,.014,1.18),BLACK,.028)
    in_screen(card)
    key_visibility(card,3.1+i*.5)
    edge=cube(f'Color swatch {i}',(x,.288,1.53),(.63,.01,.38),mat,.008)
    in_screen(edge)
    key_visibility(edge,3.4+i*.5)
    for j in range(3):
        ln=cube(f'Editable content line {i}-{j}',(x-.27,.280,1.13-j*.15),(.52-.09*j,.006,.026),WHITE)
        in_screen(ln)
        key_visibility(ln,4+i*.38+j*.19)

status=text('Workspace live','EXPORT  •  READY',(-1.25,.28,.10),.11,GOLD)
in_screen(status)
key_visibility(status,6.0)

# After the digital canvas resolves, three actual deliverables emerge out of the monitor.
product_mats=[GOLD,CYAN,ROSE]
product_names=['GUIDE','TEMPLATE','KIT']
for i, mat in enumerate(product_mats):
    x=(-1.43,0,1.43)[i]
    card=cube(f'Product output / {product_names[i]}',(x,.0,1.35),(.94,.1,1.31),BLACK,.048)
    card.rotation_euler.y=math.radians([-15,0,15][i])
    key_visibility(card,8.4+i*.36)
    animate_loc(card,(x,.23,1.48),(x,-.96,1.78+(.16 if i==1 else 0)),8.6+i*.32,12.8)
    stripe=cube(f'Product brand stripe {i}',(x,-.067,1.76),(.80,.013,.37),mat,.006)
    key_visibility(stripe,9.4+i*.40)
    animate_loc(stripe,(x,.15,1.78),(x,-1.04,2.11+(.16 if i==1 else 0)),9.1+i*.36,13.0)
    lbl=text(f'{product_names[i]} category',product_names[i],(x-.31,-.11,1.51),.17,WHITE)
    key_visibility(lbl,10+i*.34)
    animate_loc(lbl,(x-.31,.12,1.44),(x-.31,-1.09,1.82+(.16 if i==1 else 0)),9.6+i*.33,13.0)

# Animated conversion trail: luminous flow from the idea in the laptop to the outputs.
trail_materials=[GOLD,CYAN,ROSE]
for k in range(11):
    ang=k*math.tau/11
    r=1.68+(.22 if k%2 else 0)
    pos=(r*math.cos(ang),-.6+(.25 if k%3==0 else 0),1.35+r*.45*math.sin(ang))
    bpy.ops.mesh.primitive_uv_sphere_add(segments=10,ring_count=6,radius=.023+k%3*.012,location=pos)
    p=bpy.context.object
    p.name='Idea particles'
    p.data.materials.append(trail_materials[k%3])
    key_visibility(p,4+k*.24)
    animate_loc(p,(0,.12,1.6),pos,4+k*.24,11+k*.09)

for i, (p,q) in enumerate(zip((-.9,.2,.85),(0,.2,1.5))):
    pass

def area_light(name,location,power,color,size):
    data=bpy.data.lights.new(name,'AREA')
    data.energy=power
    data.color=color
    data.shape='DISK'
    data.size=size
    ob=bpy.data.objects.new(name,data)
    bpy.context.collection.objects.link(ob)
    ob.location=location
    direction=Vector((0,0,.4))-ob.location
    ob.rotation_euler=direction.to_track_quat('-Z','Y').to_euler()
area_light('Warm key',(-4,-4,7),1050,(1,.68,.35),5)
area_light('Lavender rim',(4,2,6),1350,(.42,.34,1),3)
area_light('Cold screen',(-1,-4,3),420,(.16,.77,1),4)

bpy.ops.object.camera_add(location=(0,-8.6,4.05))
camera=bpy.context.object
scene.camera=camera
target=Vector((0,0,.82))
camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
camera.data.type='PERSP'
camera.data.lens=36
for sec, xyz in ((0,(.0,-9.1,4.25)),(6,(-.28,-8.15,3.85)),(11,(.35,-7.65,3.72)),(16,(.0,-8.30,3.94))):
    camera.location=xyz
    camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
    camera.keyframe_insert(data_path='location',frame=int(sec*FPS)+1)
    camera.keyframe_insert(data_path='rotation_euler',frame=int(sec*FPS)+1)

scene.view_settings.view_transform='AgX'
scene.render.image_settings.color_mode='RGB'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'episode04_scene.blend'))
if os.environ.get('ARCHITECT_KEYFRAMES'):
    for frame in map(int, os.environ['ARCHITECT_KEYFRAMES'].split(',')):
        scene.frame_set(frame)
        scene.render.filepath = str(ROOT / f'stage_{frame:03d}.png')
        bpy.ops.render.render(write_still=True)
elif os.environ.get('ARCHITECT_PREVIEW_FRAME'):
    scene.frame_set(int(os.environ['ARCHITECT_PREVIEW_FRAME']))
    scene.render.filepath = str(ROOT / 'preview3d.png')
    bpy.ops.render.render(write_still=True)
else:
    bpy.ops.render.render(animation=True)

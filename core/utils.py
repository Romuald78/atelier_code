import arcade

# def createSound(fileName):
#     snd = arcade.load_sound(fileName)
#     return snd

def createText(params):
    # retrieve parameters
    x       = params["x"]
    y       = params["y"]
    message = params["message"]
    size    = 12                if "size"   not in params else params["size"  ]
    color   = (255,255,255,255) if "color"  not in params else params["color" ]
    alignH  = "center"          if "alignH" not in params else params["alignH"]    # left, center, right
    alignV  = "center"          if "alignV" not in params else params["alignV"]    # top, center, bottom
    angle   = 0                 if "angle"  not in params else params["angle" ]
    bold    = False             if "bold"   not in params else params["bold"  ]
    italic  = False             if "italic" not in params else params["italic"]
    # draw text according to configuration
    text_spr = arcade.create_text_sprite(text=message, color=color, font_size=size,
                                         bold=bold, italic=italic, anchor_x=alignH)
    text_spr.center_x = x
    text_spr.center_y = y
    text_spr.angle = angle

    # TODO align_v is not working at the moment

    # End of process
    spr_list = arcade.SpriteList()
    spr_list.append(text_spr)
    return spr_list


def createFixedSprite(params):
    # retrieve parameters
    filePath    = params["filePath"  ]
    size        = None if "size" not in params else params["size"]
    filterColor = (255,255,255,255) if "filterColor" not in params else params["filterColor"]
    isMaxRatio  = False if "isMaxRatio" not in params else params["isMaxRatio"]
    position    = (0,0) if "position" not in params else params["position"]
    flipH       = False  if "flipH" not in params else params["flipH"]
    flipV       = False  if "flipV" not in params else params["flipV"]

    # load texture for sprite and resize
    texture = arcade.load_texture(filePath)
    # Flip texture
    if flipH:
        texture = texture.flip_horizontally()
    if flipV:
        texture = texture.flip_vertically()
    # Size
    size_ratio = 1.0
    if size != None:
        if isMaxRatio:
            size_ratio = max(size[0] / texture.width, size[1] / texture.height)
        else:
            size_ratio = min(size[0]/ texture.width, size[1] / texture.height)
    # Create sprite from texture
    spr = arcade.Sprite(texture)
    # set color, size and position (init)
    spr.color    = filterColor
    spr.scale    = size_ratio
    spr.center_x = position[0]
    spr.center_y = position[1]
    # End of process
    spr_list = arcade.SpriteList()
    spr_list.append(spr)
    return spr_list

def createAnimatedSprite(params):
    filePath      = params["filePath"  ]
    size          = None if "size" not in params else params["size"]
    filterColor   = (255, 255, 255, 255) if "filterColor" not in params else params["filterColor"]
    isMaxRatio    = False  if "isMaxRatio" not in params else params["isMaxRatio"]
    position      = (0, 0) if "position" not in params else params["position"]
    spriteBox     = params["spriteBox" ]
    startIndex    = params["startIndex"]
    endIndex      = params["endIndex"  ]
    frameduration = 1/60   if "frameDuration" not in params else params["frameDuration"]
    flipH         = False  if "flipH" not in params else params["flipH"]
    flipV         = False  if "flipv" not in params else params["flipV"]

    # Get sprite box
    nbX, nbY, szW, szH = spriteBox
    # Create animation + load textures (loop)
    # Read Horizontal first, then vertical
    tkfs = []
    for y in range(nbY):
        for x in range(nbX):
            index = x + y*nbX
            # add index only if in range
            if index >= startIndex and index <= endIndex:
                tex = arcade.load_texture(filePath)
                tex = tex.crop(x * szW, y * szH, szW, szH)
                if flipH:
                    tex = tex.flip_horizontally()
                if flipV:
                    tex = tex.flip_vertically()
                tkf = arcade.TextureKeyframe(tex, frameduration * 1000)
                tkfs.append(tkf)
    # Create animation + sprite
    anim = arcade.TextureAnimation(tkfs)
    spr = arcade.TextureAnimationSprite(animation=anim)
    spr.update_animation()
    # Size
    size_ratio = 1.0
    if size != None:
        if isMaxRatio:
            size_ratio = max(size[0] / spr.width, size[1] / spr.height)
        else:
            size_ratio = min(size[0] / spr.width, size[1] / spr.height)
    # set color, size and position (init)
    spr.color    = filterColor
    spr.scale    = size_ratio
    spr.center_x = position[0]
    spr.center_y = position[1]
    # End of process
    spr_list = arcade.SpriteList()
    spr_list.append(spr)
    return spr_list




# def createParticleBurst(params):
#     # retrieve parameters
#     x0            = params["x0"           ]
#     y0            = params["y0"           ]
#     partSize      = params["partSize"     ]
#     partScale     = params["partScale"    ]
#     partSpeed     = params["partSpeed"    ]
#     color         = params["color"        ]
#     startAlpha    = params["startAlpha"   ]
#     endAlpha      = params["endAlpha"     ]
#     imagePath     = None if "imagePath" not in params else params["imagePath"]
#
#     partInterval  = params["partInterval" ]
#     totalDuration = params["totalDuration"]
#
#     # create particle emitter
#     e = arcade.Emitter(
#         center_xy=(x0, y0),
#         emit_controller=arcade.EmitterIntervalWithTime(partInterval, totalDuration),
#         particle_factory=lambda emitter: arcade.FadeParticle(
#             filename_or_texture=imagePath if imagePath is not None else arcade.make_circle_texture(partSize, color),
#             change_xy=arcade.rand_in_circle((0.0, 0.0), partSpeed),
#             scale=partScale,
#             lifetime=uniform(totalDuration/4, totalDuration),
#             start_alpha=startAlpha,
#             end_alpha=endAlpha,
#         ),
#     )
#     # return result
#     return e



# def createParticleEmitter(params):
#     # retrieve parameters
#     x0            = params["x0"          ]
#     y0            = params["y0"          ]
#     partSize      = params["partSize"    ]
#     partScale     = params["partScale"   ]
#     partSpeed     = params["partSpeed"   ]
#     color         = params["color"       ]
#     startAlpha    = params["startAlpha"  ]
#     endAlpha      = params["endAlpha"    ]
#
#     partNB        = params["partNB"      ]
#     maxLifeTime   = params["maxLifeTime" ]
#
#     imagePath     = None  if "imagePath"  not in params else params["imagePath"]
#     spriteBox     = None if "spriteBox" not in params else params["spriteBox"]
#     spriteSelect  = None if "spriteSelect" not in params else params["spriteSelect"]
#     flipH = False if "flipH" not in params else params["flipH"]
#     flipV = False if "flipv" not in params else params["flipV"]
#
#     # Prepare Texture
#     if imagePath == None:
#         tex = arcade.make_circle_texture(partSize, color)
#     else:
#         nbX, nbY, szW, szH = spriteBox
#         x, y = spriteSelect
#         tex = arcade.load_texture(imagePath, x * szW, y * szH, szW, szH,
#                                   flipped_horizontally=flipH,
#                                   flipped_vertically=flipV)
#     # Create emitter
#     e = arcade.Emitter(
#         center_xy        = (x0, y0),
#         emit_controller  = arcade.EmitMaintainCount(partNB),
#         particle_factory = lambda emitter: arcade.FadeParticle(
#             filename_or_texture = tex,
#             change_xy           = arcade.rand_in_circle( (0.0,0.0), partSpeed),
#             lifetime            = uniform(maxLifeTime/40,maxLifeTime),
#             scale = partScale,
#             start_alpha=startAlpha,
#             end_alpha=endAlpha,
#         ),
#     )
#     return e



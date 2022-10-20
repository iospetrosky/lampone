from PIL import Image


big_source = 'nethack32.png'
out_dir = 'tiles'
tile_w = 32
tile_h = 32
tile_prefix = 'nethack'

cols = 40
rows = 27

orig = Image.open(big_source)
for r in range(0,rows):
    for c in range(0,cols):
        print("Row: {0} - Col: {1}".format(r,c))
        box = (c*tile_w, r*tile_h, c*tile_w+tile_w, r*tile_h+tile_h)
        tile = orig.crop(box)
        tile.save("{0}/{3}_{1}_{2}.png".format(out_dir,r,c,tile_prefix))



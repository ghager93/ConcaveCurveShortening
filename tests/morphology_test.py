import bin.image
import bin.image_array
import bin.morphology
from bin.util.base_dir import base_dir

img = bin.image.open(base_dir + 'lib/shapes/overlapped_squares.bmp')
img_array = bin.image_array.convert_image_to_array(img)
struct_elem = bin.morphology.get_circular_structuring_element(radius=8)

eroded_array = bin.morphology.binary_erosion(img_array, struct_elem)
bin.image_array.show(eroded_array)

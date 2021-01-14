import bin.image
import bin.image_array
import bin.morphology
import bin.morphology._operations
import bin.morphology.structuring_element
import bin.utils.imshow
from bin.utils.base_dir import base_dir

img = bin.image.open_image(base_dir + 'lib/shapes/overlapped_squares.bmp')
img_array = bin.image_array.convert_image_to_array(img)
struct_elem = bin.morphology.structuring_element.circular_structuring_element(radius=8)

eroded_array = bin.morphology._operations.binary_erosion(img_array, struct_elem)
bin.utils.imshow.show(eroded_array)

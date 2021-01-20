import bin.adj_image
import bin.adj_image_array
import bin.morphology
import bin.morphology._adj_operations
import bin.morphology.adj_structuring_element
import bin.utils.imshow
from bin.utils.base_dir import base_dir

img = bin.adj_image.open_image(base_dir + 'lib/shapes/overlapped_squares.bmp')
img_array = bin.adj_image_array.convert_image_to_array(img)
struct_elem = bin.morphology.adj_structuring_element.circular_structuring_element(radius=8)

eroded_array = bin.morphology._adj_operations.binary_erosion(img_array, struct_elem)
bin.utils.imshow.show(eroded_array)

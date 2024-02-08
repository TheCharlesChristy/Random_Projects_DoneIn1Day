from PIL import Image
import math
from tqdm import tqdm
import os

def read_large_file_in_chunks(file_path, chunk_size=1024 * 1024):
    file_size = os.path.getsize(file_path)
    with open(file_path, 'r') as file, tqdm(total=file_size, unit='B', unit_scale=True) as pbar:
        chunk = ""
        while True:
            next_chunk = file.read(chunk_size)
            if not next_chunk:
                if chunk:
                    yield from (int(num) for num in chunk.split(',') if num)
                break
            
            chunk += next_chunk
            pbar.update(len(next_chunk))
            
            last_comma = chunk.rfind(',')
            if last_comma == -1:
                continue
            
            to_process, chunk = chunk[:last_comma], chunk[last_comma+1:]
            yield from (int(num) for num in to_process.split(',') if num)

# Assuming the dimensions are known or stored elsewhere
image_width = 10001  # You'll need to set this based on your specific case
image_height = 10001  # Same as above

# Create a new image with the determined size
image = Image.new('RGB', (image_width, image_height))
pixels = image.load()

index = 0
# Now we don't have the total number of pixels beforehand to set up a progress bar for pixel processing
# If you know the total, you can add it here
pixel_data_generator = read_large_file_in_chunks('PrimeSpiralPixelData.txt')
for pixel_value in pixel_data_generator:
    i = index // image_height
    j = index % image_height
    r = (pixel_value >> 16) & 0xFF
    g = (pixel_value >> 8) & 0xFF
    b = pixel_value & 0xFF
    pixels[i, j] = (255-r, 255-g, 255-b)
    index += 1

# Save the image
image.save('PerfectNumSpiral.png')

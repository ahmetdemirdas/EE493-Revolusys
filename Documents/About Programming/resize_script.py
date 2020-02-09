from PIL import Image

im = Image.open("eee.png")

# Provide the target width and height of the image
(width, height) = (im.width // 2, im.height // 2)
im_resized = im.resize((width, height))
im_resized.show()
				
from PIL import Image, ImageDraw, ImageFont

lettersize = 70
image = Image.new("1", (800,800), 1)
font = ImageFont.truetype("fonts/Helv25.ttf", lettersize)
draw = ImageDraw.Draw(image)
size = draw.text((0,0), "M e r c u r y", font=font)
size = draw.text((5,75), "e", font=font)
size = draw.text((15,150), "t", font=font)
size = draw.text((5,225), "a", font=font)
size = draw.text((15,300), "l    bitbre a ke r", font=font)
size = draw.text((5,375), "v", font=font)
size = draw.text((5,450), "o", font=font)
size = draw.text((15,525), "t o p y 4 4", font=font)
size = draw.text((5,600), "z", font=font)
size = draw.text((5,675), "e", font=font)
size = draw.text((272,150), "e", font=font)
size = draw.text((272,225), "h", font=font)
size = draw.text((405,225), "u", font=font)
size = draw.text((405,375), "s", font=font)
image.save("Test.bmp", "BMP")


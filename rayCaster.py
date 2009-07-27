from geom3 import Point3, Vector3, Ray3, cross, dot, unit, length
from math import sqrt, tan
from colour import Colour
from sphere import Sphere
from plane import Plane
import Image
from material import Material
from scene import Scene    


# Define various scene constants

WIN_SIZE = 200                              # Screen window size (square)
SPACING = 1.0 / WIN_SIZE                    # Pixel spacing on viewplane

LIGHT_DIR = unit(Vector3(2,5,3))            # The direction vector towards the light source
OFFSET = 0.0000001 * LIGHT_DIR              # Offset to avoid surface cancer
LIGHT_COLOUR = Colour(0.8, 0.8, 0.8)        # Colour of the single light source
AMBIENT = Colour(0.1, 0.1, 0.1)             # Ambient light level (assumed white light)
BACKGROUND = Colour(0.6,0.6,0.6)            # Colour of the background

SHINY_RED = Material(Colour(0.7, 0.3, 0.2), Colour(0.4,0.4,0.4), 100)
SHINY_BLUE = Material(Colour(0.2, 0.3, 0.7), Colour(0.8,0.8,0.8), 200)
MATT_GREEN = Material(Colour(0.1, 0.7, 0.1), None, None)

EYEPOINT = Point3(0.5, 0.5, 2)

SCENE = Scene([Sphere(Point3(0.35,0.6,0.5), 0.25, SHINY_BLUE),
               Sphere(Point3(0.75,0.2,0.6), 0.15, SHINY_RED),
               Plane(Point3(0,0,0), Vector3(0,1,0), MATT_GREEN)])

# Main body. Set up an image then compute colour at each pixel

img = Image.new("RGB", (WIN_SIZE, WIN_SIZE))

for row in range(WIN_SIZE):
    for col in range(WIN_SIZE):
		
        pixelCentre = Point3((col + 0.5) * SPACING, ((WIN_SIZE -row) + 0.5) * SPACING, 1)
        rayDir = pixelCentre - EYEPOINT
        ray = Ray3(EYEPOINT, rayDir)

        # Compute the ray from the eye through the centre
        # of pixel (col, row)
        # ***** DO IT!!! ******

        hitPoint = SCENE.intersect(ray)

        if hitPoint is None:
            colour = BACKGROUND
        else:
            (obj, t) = hitPoint
            surface = obj.material

            normal = obj.normal(ray.pos(t))
            view = -rayDir
			
			# Shadow Test
            sray = Ray3(ray.pos(t), LIGHT_DIR)
            shadowTest = SCENE.intersect(sray)
            if shadowTest:
                (sobj, st) = shadowTest
                if sobj == obj:
                    shadowTest = None
            if shadowTest is None:
                colour = surface.litColour(normal, AMBIENT, LIGHT_DIR, LIGHT_COLOUR, view)
            else:
                colour = surface.litColour(normal, AMBIENT, LIGHT_DIR, None, view)

        img.putpixel((col, row), colour.intColour())

img.show()  # Display image in default image-viewer application

import Core
import Game
import Math
import Random
import Resources
import UserData
import ImageResources
import Graphics2D
import Graphics2DText

Game.onScreenCreated.append(Graphics2D.addScreenRef)

def make_a_texture(pygame_image):
	width, height = pygame_image.get_size()
	imgRes = ImageResources.ImageResource(width, height, False)
	imgRes.image = pygame_image
	return Graphics2D.GraphicsTexture(imgRes)

Graphics2DText.g2d_texture_constructor = make_a_texture

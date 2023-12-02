#!/usr/bin/env python
# Default libs
import sys
import os
from pathlib import Path

# Ursina
from ursina import *
from prefabs import osu_splash

# ConfigSections
import tomli


#app = Ursina()
app = Ursina(borderless=False)

camera.ortographic = True
#camera.fov = 1
camerae = EditorCamera(enabled=1)




class OsuMenu(Entity):
	def __init__(self, configItems):
		super().__init__()

		self.configItems = configItems

		self.current_background = 0
		self.background_textures = ['bg1.jpg', 'bg2.jpg', 'bg3.jpg', 'bg4.jpg']

		#cursor =  Cursor(model=Mesh(vertices=[(-.5,0,0),(.5,0,0),(0,-.5,0),(0,.5,0)], triangles=[(0,1),(2,3)], mode='line', thickness=2), scale=.02)
		mouse.visible = False
		cursor = Cursor(texture="osu-resources/osu.Game.Resources/Textures/Cursor/menu-cursor.png", scale_x=.02, scale_y=.035)

		self.background = Entity(
				model='quad',
				texture=f"osu-resources/osu.Game.Resources/Textures/Backgrounds/{self.background_textures[self.current_background]}",
				scale=(
					14 *camera.aspect_ratio,
					7 * camera.aspect_ratio
					)
			)

			

		self.textures: dict = self.loadTextures()
		self.CentralOsuButton = Button(
			color=color.white,
			parent=scene,
			model = "quad", 
			texture = self.textures['menuTextures']['content']['logo'],
			scale=4,
			z = -1,
			on_click = self.osuButtonClicked
		)

		self.welcome_audio = Audio("osu-resources/osu.Game.Resources/Samples/Intro/welcome.mp3")
		#self.audio = Audio("osu-resources/osu.Game.Resources/Samples/Gameplay/pause-loop.mp3", loop=True, autoplay=True)


	def loadTextures(self) -> dict:
		#print(self.configItems)
		
		resources_path = self.configItems['resources']['path']

		textures_dict = self.configItems['resources']['textures']
		textures_folder = resources_path + textures_dict['path']

		menu_textures_path = str(textures_folder + textures_dict['menu']['path'])

		newDict = {
			'menuTextures': {
				'path': menu_textures_path,
				'content': textures_dict['menu']['textures']
			}
		}
		

		

		return newDict

	def osuButtonClicked(self):
		#play sound
		play_audio = Audio("osu-resources/osu.Game.Resources/Samples/Menu/osu-logo-select.wav", volume=.5).play()
		if self.current_background <= len(self.background_textures) - 1:
			self.current_background += 1

		if self.current_background == len(self.background_textures):
			self.current_background = 0

		

		self.background.texture = f"osu-resources/osu.Game.Resources/Textures/Backgrounds/{self.background_textures[self.current_background]}"



class Textures():
	def __init__(self, config_dict):
		self.origin_config_dict = config_dict



class Engine(Entity):
	def __init__(self):
		super().__init__()

		self.ent = Entity(
			model="quad", 
			visible=False
		)

		camera.add_script(
				SmoothFollow(
					target=self.ent, 
					offset=[0,0,-30], 
					speed=4
				)
			)

	def input(self, key):
		pass

	def update(self):
		parallax = .5

		mp = (
			mouse.position[0] * parallax, 
			mouse.position[1] * parallax, 
			mouse.position[2] * parallax
		)

		self.ent.position = mp

class Central():
	def __init__(self):
		# Window defaults (if config.toml does not exist)
		self.window_title : str = "Test"
		self.fullscreen: bool = False
		self.borderless: bool = True
		self.exit_button_visible: bool = True
		self.showfps: bool = True

		self.config_file = "config.toml"
		self.config_content = self.LoadConfigContent(self.config_file)

		self.loadGlobalVars()
		self.defineWindow()
		
	def LoadConfigContent(self,config_file) -> dict:
		try:
			with open(config_file, 'rb') as cfile:
				cfg = tomli.load(cfile)

			return cfg

		except Exception as e:
			return {"error": f"Config file couldn't be loaded\n Error: {str(e)}"}

	def loadGlobalVars(self):
		try:
			with open("config.toml", 'rb') as cfile:
				cfg = tomli.load(cfile)

				self.window_title= cfg["window"]["title"]
				self.fullscreen = cfg["window"]["fullscreen"]
				self.borderless = cfg["window"]["borderless"]
				self.exit_button_visible = cfg["window"]["exit_button_visible"]
				self.showfps = cfg["window"]["fps_counter"]

		except Exception as e:
			print("Error reading config.toml")
			raise e


	def defineWindow(self):
		window.title = self.window_title
		window.fullscreen = self.fullscreen
		window.borderless = self.borderless
		window.exit_button.visible = self.exit_button_visible
		window.fps_counter.enabled = self.showfps
		#window.color = color._16



if __name__ == "__main__":
	central = Central()
	engine = Engine()
	menu = OsuMenu(configItems=central.config_content)
	app.run()

import pyautogui
import time
from PIL import Image as pil_image
import imagehash
import json

class Scraper():
	
	PRESS_SCREENSHOT_CURSOR = (352, 705)
	NEXT_PHOTO_CURSOR = (586, 710)
	OPEN_BIO_CURSOR = (314, 1280)
	NEXT_USER_CURSOR = (77, 1289)

	POINT1_PHOTO = (25, 165)
	POINT2_PHOTO = (25, 1295)
	POINT3_PHOTO = (620, 165)
	POINT4_PHOTO = (620, 1295)

	POINT1_BIO = (0, 70)
	POINT2_BIO = (0, 1365)
	POINT3_BIO = (635, 70)
	POINT4_BIO = (635, 1365)
	
	POINT1_NAME = (28, 984)
	POINT2_NAME = (28, 1048)
	POINT3_NAME = (600, 984)
	POINT4_NAME = (600, 1048)

	CLOSE_ADVERTISEMENT = (570, 222)

	def __init__(self, iterations, city):

		self.city = city
		self.users = []
		first_user_id = int(self.get_first_user())
		
		for self.user_id in range(first_user_id+1, first_user_id+iterations+1):
			print(f"Юзер номер {self.user_id}")
			self.main_func()
			self.users.append(self.user_id)

	def main_func(self, iterations=11):
		self.hash_list = []
		self.images = []
		self.advertise_checker()
		self.get_screenshot('info', self.POINT1_PHOTO, self.POINT2_PHOTO, self.POINT3_PHOTO, self.POINT4_PHOTO)

		for self.number_of_photo in range(1, iterations):
			new_photo = self.get_user_photo()
			if new_photo:
				self.click_with_checker(self.NEXT_PHOTO_CURSOR[0], self.NEXT_PHOTO_CURSOR[1])
			else:
				time.sleep(1)
				self.work_with_bio()
				time.sleep(1)
				self.add_to_json()
				next_user_check = self.click_with_checker(self.NEXT_USER_CURSOR[0], self.NEXT_USER_CURSOR[1])
				if next_user_check == True:
					break
				else:
					self.from_bottom_to_main()
				
	
	def get_first_user(self):
		try:
			with open('datas/twinby.json', 'r', encoding='utf-8') as json_file:
				data = json.load(json_file)
				# Получение списка ключей
				keys = list(data.keys())
				# Получение последнего ключа
				last_id = keys[-1]
				return last_id
		except json.decoder.JSONDecodeError:
			last_id = 0
			return last_id


	def add_to_json(self):
		try:
			with open('datas/twinby.json', 'r', encoding='utf-8') as json_file:
				data = json.load(json_file)
		except json.decoder.JSONDecodeError:
			data = {}
		
		data[self.user_id] = {"city": self.city,"images": self.images}
		with open('datas/twinby.json', 'w+', encoding='utf-8') as json_file:
			json.dump(data, json_file, ensure_ascii=False)
	
	def advertise_checker(self):
		try:
			location = pyautogui.locateOnScreen('fix_element.png', confidence=0.9)
			pyautogui.moveTo(location)
			time.sleep(1)
			pyautogui.click(location)
			time.sleep(3)
		except:
			pass

	def get_raw_hash(self):
		left = min(self.POINT1_PHOTO[0], self.POINT2_PHOTO[0])
		top = min(self.POINT1_PHOTO[1], self.POINT3_PHOTO[1])
		width = max(self.POINT2_PHOTO[0], self.POINT4_PHOTO[0]) - left
		height = max(self.POINT3_PHOTO[1], self.POINT4_PHOTO[1]) - top
		screenshot = pyautogui.screenshot(region=(left, top, width, height))
		hash_value = str(imagehash.phash(screenshot))
		return hash_value
	
	def click_with_checker(self, x, y):
		first_hash = self.get_raw_hash()
		pyautogui.click(x, y)
		time.sleep(2)
		second_hash = self.get_raw_hash()
		timeout = 0
		print(first_hash, second_hash)
		while second_hash == first_hash and timeout < 5:
			print(f'не нажалось {timeout+1}')
			pyautogui.click(x, y)
			time.sleep(2)
			second_hash = self.get_raw_hash()
			print(first_hash, second_hash)
			timeout += 1
		if timeout < 5:
			return True

	def from_bottom_to_main(self):
		pyautogui.moveTo(250, 65)
		pyautogui.mouseDown()
		pyautogui.moveTo(260, 1290)
		pyautogui.mouseUp()
		self.click_with_checker(185, 1195)

	def get_screenshot(self, screenshot_type, point1, point2, point3, point4):
		left = min(point1[0], point2[0])
		top = min(point1[1], point3[1])
		width = max(point2[0], point4[0]) - left
		height = max(point3[1], point4[1]) - top

		screenshot = pyautogui.screenshot(region=(left, top, width, height))
		if screenshot_type == 'photo':
			hash_value = str(imagehash.phash(screenshot))
			if hash_value not in self.hash_list:
				name = f"user{self.user_id}_{self.number_of_photo}"
				screenshot.save(f"screenshots/{name}.png")
				self.images.append(name)
				self.hash_list.append(hash_value)
				return True
			else:
				return False
		elif screenshot_type == 'name':
			screenshot.save(f"screenshots/user{self.user_id}_name.png")
		elif screenshot_type == 'info':
			screenshot.save(f"screenshots/user{self.user_id}_0.png")
		elif screenshot_type == 'bio':
			screenshot.save(f"screenshots/user{self.user_id}_bio.png")
		
	
	
	def get_user_photo(self):
		pyautogui.moveTo(self.PRESS_SCREENSHOT_CURSOR[0], self.PRESS_SCREENSHOT_CURSOR[1])
		time.sleep(0.5)
		pyautogui.mouseDown()
		time.sleep(3)
		new_photo = self.get_screenshot('photo', self.POINT1_PHOTO, self.POINT2_PHOTO, self.POINT3_PHOTO, self.POINT4_PHOTO)
		pyautogui.mouseUp()
		time.sleep(2)
		return new_photo

	def work_with_bio(self):
		self.click_with_checker(self.OPEN_BIO_CURSOR[0], self.OPEN_BIO_CURSOR[1])
		self.get_screenshot('name', self.POINT1_NAME, self.POINT2_NAME, self.POINT3_NAME, self.POINT4_NAME)
		for _ in range(15):
			pyautogui.scroll(-1000)  # Отрицательное значение для скролла вниз
			time.sleep(0.01)
		self.get_screenshot('bio', self.POINT1_BIO, self.POINT2_BIO, self.POINT3_BIO, self.POINT4_BIO)

x = Scraper(5000, city='Moscow')
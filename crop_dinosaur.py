# ===== 恐龙养殖模块 =====
# 类似贪吃蛇的智能算法，使用 measure() 追踪苹果位置
# 装备恐龙帽，吃苹果增长尾巴，收获 n² 根骨头
# 策略：持续吃苹果直到完全无法移动

import utils

def abs_value(n):
	if n < 0:
		return -n
	return n

def farm_dinosaur(target_size=None):
	# 如果指定了目标大小，调整农场
	if target_size != None:
		current_size = get_world_size()
		if current_size != target_size:
			set_world_size(target_size)
	
	# 获取农场大小
	size = get_world_size()
	
	# 检查仙人掌资源
	cactus_count = num_items(Items.Cactus)
	required_cactus = size * size
	
	if cactus_count < required_cactus:
		return False
	
	# 装备恐龙帽
	change_hat(Hats.Dinosaur_Hat)
	
	# 无限循环，直到四个方向都无法移动
	stuck_count = 0
	max_attempts = size * size * 10
	attempts = 0
	
	while attempts < max_attempts:
		# 获取下一个苹果的位置
		apple_pos = measure()
		apple_x = apple_pos[0]
		apple_y = apple_pos[1]
		
		# 尝试导航到苹果
		success = navigate_to_apple(apple_x, apple_y, size)
		
		if not success:
			if try_any_move():
				stuck_count = 0
			else:
				stuck_count = stuck_count + 1
				if stuck_count >= 3:
					break
		else:
			stuck_count = 0
		
		attempts = attempts + 1
	
	# 卸下恐龙帽
	change_hat(Hats.Straw_Hat)
	
	return True


def navigate_to_apple(target_x, target_y, world_size):
	max_steps = world_size * 2
	steps = 0
	last_distance = -1
	stuck_count = 0
	
	while steps < max_steps:
		# 获取当前位置
		current_x = get_pos_x()
		current_y = get_pos_y()
		
		# 计算曼哈顿距离
		distance = abs_value(target_x - current_x) + abs_value(target_y - current_y)
		
		if distance == 0:
			return True
		
		# 检查是否卡住
		if last_distance != -1 and distance >= last_distance:
			stuck_count = stuck_count + 1
			if stuck_count >= 3:
				return False
		else:
			stuck_count = 0
		
		last_distance = distance
		
		# 计算x和y方向的距离
		dx = target_x - current_x
		dy = target_y - current_y
		
		# 优先向距离更大的方向移动
		moved = False
		
		if abs_value(dx) >= abs_value(dy):
			# x方向距离更大
			if dx > 0:
				if move(East):
					moved = True
			else:
				if move(West):
					moved = True
			
			# 如果x方向失败，尝试y方向
			if not moved:
				if dy > 0:
					if move(North):
						moved = True
				else:
					if move(South):
						moved = True
		else:
			# y方向距离更大
			if dy > 0:
				if move(North):
					moved = True
			else:
				if move(South):
					moved = True
			
			# 如果y方向失败，尝试x方向
			if not moved:
				if dx > 0:
					if move(East):
						moved = True
				else:
					if move(West):
						moved = True
		
		if not moved:
			return False
		
		steps = steps + 1
	
	return False


def try_any_move():
	directions = [North, East, South, West]
	
	for direction in directions:
		if move(direction):
			return True
	
	return False


def farm_dinosaur_efficient(apple_count=50):
	size = get_world_size()
	
	# 检查资源
	cactus_count = num_items(Items.Cactus)
	if cactus_count < apple_count:
		return False
	
	# 装备恐龙帽
	change_hat(Hats.Dinosaur_Hat)
	
	# 吃指定数量的苹果
	apples_eaten = 0
	max_attempts = apple_count * 5
	attempts = 0
	
	while apples_eaten < apple_count and attempts < max_attempts:
		apple_pos = measure()
		apple_x = apple_pos[0]
		apple_y = apple_pos[1]
		
		if navigate_to_apple(apple_x, apple_y, size):
			apples_eaten = apples_eaten + 1
		else:
			if not try_any_move():
				break
		
		attempts = attempts + 1
	
	# 卸下恐龙帽
	change_hat(Hats.Straw_Hat)
	
	return True


def farm_dinosaur_optimal():
	cactus_count = num_items(Items.Cactus)
	
	# 根据资源选择农场大小
	if cactus_count >= 400:
		target_size = 6
	else:
		if cactus_count >= 200:
			target_size = 5
		else:
			if cactus_count >= 100:
				target_size = 4
			else:
				return False
	
	return farm_dinosaur(target_size)

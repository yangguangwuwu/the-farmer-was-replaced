# ===== 恐龙养殖模块 =====
# 装备恐龙帽，吃苹果增长尾巴，收获 n² 根骨头
# 策略：遍历整个场地，让尾巴填满农场以获得最大收益

import utils

def farm_dinosaur(target_size=None):	
	# 如果指定了目标大小，调整农场
	if target_size != None:
		current_size = get_world_size()
		if current_size != target_size:
			set_world_size(target_size)
	
	# 获取农场大小
	size = get_world_size()
	
	# 检查仙人掌资源（每颗苹果消耗仙人掌）
	# 保守估计：至少需要 size*size 个仙人掌
	cactus_count = num_items(Items.Cactus)
	required_cactus = size * size
	
	if cactus_count < required_cactus:
		# 资源不足，先返回
		return False
	
	# 装备恐龙帽
	change_hat(Hats.Dinosaur_Hat)
	
	# 按S形路径遍历农场，确保覆盖每个格子
	# 这样尾巴会完全填满农场
	y = 0
	while y < size:
		# 偶数行：从左到右
		if y % 2 == 0:
			x = 0
			while x < size:
				# 移动到目标位置
				success = move_to_safe(x, y)
				if not success:
					# 移动失败说明尾巴已经填满农场
					break
				x = x + 1
		# 奇数行：从右到左（S形）
		else:
			x = size - 1
			while x >= 0:
				success = move_to_safe(x, y)
				if not success:
					# 移动失败说明尾巴已经填满农场
					break
				x = x - 1
		
		# 检查是否无法继续移动（尾巴填满）
		if not success:
			break
		
		y = y + 1
	
	# 卸下恐龙帽，收获骨头（n² 根）
	# 装备任意其他帽子来卸下恐龙帽
	change_hat(Hats.Straw_Hat)
	
	return True

def move_to_safe(target_x, target_y):
	current_x = get_pos_x()
	current_y = get_pos_y()
	
	# 已经在目标位置
	if current_x == target_x and current_y == target_y:
		return True
	
	# 先移动X方向
	while current_x != target_x:
		if current_x < target_x:
			# 向右移动
			success = move(East)
			if not success:
				return False
		else:
			# 向左移动
			success = move(West)
			if not success:
				return False
		current_x = get_pos_x()
	
	# 再移动Y方向
	while current_y != target_y:
		if current_y < target_y:
			# 向上移动
			success = move(North)
			if not success:
				return False
		else:
			# 向下移动
			success = move(South)
			if not success:
				return False
		current_y = get_pos_y()
	
	return True

def farm_dinosaur_efficient(apple_count):	
	# 检查仙人掌
	cactus_count = num_items(Items.Cactus)
	if cactus_count < apple_count:
		return False
	
	# 装备恐龙帽
	change_hat(Hats.Dinosaur_Hat)
	
	# 吃指定数量的苹果
	apples_eaten = 0
	while apples_eaten < apple_count:
		# 获取下一个苹果位置
		apple_pos = measure()
		next_x = apple_pos[0]
		next_y = apple_pos[1]
		
		# 移动到苹果位置
		success = move_to_safe(next_x, next_y)
		if not success:
			# 无法移动（尾巴阻挡），提前结束
			break
		
		apples_eaten = apples_eaten + 1
	
	# 卸下帽子收获
	change_hat(Hats.Straw_Hat)
	
	return True

def farm_dinosaur_optimal():
	# 检查仙人掌库存
	cactus_count = num_items(Items.Cactus)
	
	# 根据仙人掌数量选择最佳农场大小
	# 仙人掌越多，可以支撑更大的农场
	optimal_size = 1
	
	if cactus_count >= 10000:
		optimal_size = 10  # 10x10 = 100格 = 10000骨头
	elif cactus_count >= 6400:
		optimal_size = 8   # 8x8 = 64格 = 4096骨头
	elif cactus_count >= 3600:
		optimal_size = 6   # 6x6 = 36格 = 1296骨头
	elif cactus_count >= 1600:
		optimal_size = 4   # 4x4 = 16格 = 256骨头
	elif cactus_count >= 400:
		optimal_size = 2   # 2x2 = 4格 = 16骨头
	else:
		# 仙人掌不足，不养殖
		return False
	
	# 使用选定的大小养殖
	return farm_dinosaur(optimal_size)

def calculate_move_cost(apples_eaten):
	ticks = 400
	i = 0
	while i < apples_eaten:
		ticks = ticks - (ticks * 3 // 100)  # 每个苹果减少3%
		i = i + 1
	return ticks

# ===== 使用示例 =====
# 
# 1. 完全填满当前农场（最大收益）
# crop_dinosaur.farm_dinosaur()
#
# 2. 指定农场大小养殖
# crop_dinosaur.farm_dinosaur(6)  # 6x6农场
#
# 3. 只吃特定数量苹果（快速模式）
# crop_dinosaur.farm_dinosaur_efficient(20)  # 吃20个苹果 = 400根骨头
#
# 4. 自动最优策略
# crop_dinosaur.farm_dinosaur_optimal()  # 根据资源自动选择

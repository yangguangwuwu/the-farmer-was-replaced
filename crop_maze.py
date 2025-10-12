# ===== 迷宫探索模块 =====
# 生成树篱迷宫，寻找宝藏，收集金币
# 使用右手法则（或左手法则）遍历迷宫

import utils

def farm_maze(reuse_count=0):	
	# 获取农场大小
	world_size = get_world_size()
	
	# 计算所需的奇异物质数量
	# 基础公式: world_size * 2^(迷宫升级次数 - 1)
	maze_upgrades = num_unlocked(Unlocks.Mazes)
	if maze_upgrades == 0:
		# 还没解锁迷宫
		return False
	
	substance_per_maze = world_size * (2 ** (maze_upgrades - 1))
	total_substance_needed = substance_per_maze * (reuse_count + 1)
	
	# 检查奇异物质是否足够
	substance_available = num_items(Items.Weird_Substance)
	if substance_available < total_substance_needed:
		return False
	
	# 移动到 (0, 0) 种植灌木
	utils.move_to(0, 0)
	
	# 清理并种植灌木
	if can_harvest():
		harvest()
	plant(Entities.Bush)
	
	# 使用奇异物质生成迷宫
	use_item(Items.Weird_Substance, substance_per_maze)
	
	# 解决迷宫并收获宝藏（使用右手法则）
	reuses_done = 0
	while reuses_done <= reuse_count:
		# 找到宝藏
		found = solve_maze_righthand()
		
		if not found:
			# 如果右手法则失败，尝试左手法则
			found = solve_maze_lefthand()
		
		if not found:
			# 都失败了，直接收获清除迷宫
			harvest()
			return False
		
		# 检查是否需要重用迷宫
		if reuses_done < reuse_count:
			# 重用迷宫：在宝藏上使用奇异物质
			use_item(Items.Weird_Substance, substance_per_maze)
			reuses_done = reuses_done + 1
		else:
			# 最后一次，收获宝藏
			harvest()
			break
	
	return True

def solve_maze_righthand():
	# 方向数组（顺时针）
	directions = [North, East, South, West]
	direction_index = 0  # 初始朝北
	
	# 最大步数限制（防止无限循环）
	max_steps = 10000
	steps = 0
	
	while steps < max_steps:
		# 检查当前位置是否是宝藏
		if get_entity_type() == Entities.Treasure:
			return True
		
		# 右手法则：尝试右转、直走、左转、后转
		# 1. 尝试右转
		right_index = (direction_index + 1) % 4
		if can_move(directions[right_index]):
			direction_index = right_index
			move(directions[direction_index])
			steps = steps + 1
			continue
		
		# 2. 尝试直走
		if can_move(directions[direction_index]):
			move(directions[direction_index])
			steps = steps + 1
			continue
		
		# 3. 尝试左转
		left_index = (direction_index - 1) % 4
		if can_move(directions[left_index]):
			direction_index = left_index
			move(directions[direction_index])
			steps = steps + 1
			continue
		
		# 4. 尝试后转（180度）
		back_index = (direction_index + 2) % 4
		if can_move(directions[back_index]):
			direction_index = back_index
			move(directions[back_index])
			steps = steps + 1
			continue
		
		# 四个方向都走不了，被困住了
		return False
	
	# 超过最大步数，失败
	return False

def solve_maze_lefthand():	
	# 方向数组
	directions = [North, East, South, West]
	direction_index = 0  # 初始朝北
	
	# 最大步数限制
	max_steps = 10000
	steps = 0
	
	while steps < max_steps:
		# 检查当前位置是否是宝藏
		if get_entity_type() == Entities.Treasure:
			return True
		
		# 左手法则：尝试左转、直走、右转、后转
		# 1. 尝试左转
		left_index = (direction_index - 1) % 4
		if can_move(directions[left_index]):
			direction_index = left_index
			move(directions[direction_index])
			steps = steps + 1
			continue
		
		# 2. 尝试直走
		if can_move(directions[direction_index]):
			move(directions[direction_index])
			steps = steps + 1
			continue
		
		# 3. 尝试右转
		right_index = (direction_index + 1) % 4
		if can_move(directions[right_index]):
			direction_index = right_index
			move(directions[direction_index])
			steps = steps + 1
			continue
		
		# 4. 尝试后转
		back_index = (direction_index + 2) % 4
		if can_move(directions[back_index]):
			direction_index = back_index
			move(directions[back_index])
			steps = steps + 1
			continue
		
		# 被困住了
		return False
	
	# 超过最大步数
	return False

def solve_maze_measure():	
	max_steps = 10000
	steps = 0
	
	while steps < max_steps:
		# 检查是否到达宝藏
		if get_entity_type() == Entities.Treasure:
			return True
		
		# 获取宝藏位置
		treasure_pos = measure()
		treasure_x = treasure_pos[0]
		treasure_y = treasure_pos[1]
		
		# 获取当前位置
		current_x = get_pos_x()
		current_y = get_pos_y()
		
		# 计算方向
		moved = False
		
		# 优先X方向
		if current_x < treasure_x:
			if can_move(East):
				move(East)
				moved = True
		elif current_x > treasure_x:
			if can_move(West):
				move(West)
				moved = True
		
		# 如果X方向走不了，尝试Y方向
		if not moved:
			if current_y < treasure_y:
				if can_move(North):
					move(North)
					moved = True
			elif current_y > treasure_y:
				if can_move(South):
					move(South)
					moved = True
		
		# 如果目标方向都走不了，尝试其他方向
		if not moved:
			if can_move(North):
				move(North)
				moved = True
			elif can_move(East):
				move(East)
				moved = True
			elif can_move(South):
				move(South)
				moved = True
			elif can_move(West):
				move(West)
				moved = True
		
		if not moved:
			# 完全被困住
			return False
		
		steps = steps + 1
	
	return False

def farm_maze_optimal():
	# 检查是否解锁迷宫
	maze_upgrades = num_unlocked(Unlocks.Mazes)
	if maze_upgrades == 0:
		return False
	
	# 获取当前奇异物质数量
	substance_available = num_items(Items.Weird_Substance)
	
	# 计算当前世界大小所需的奇异物质
	world_size = get_world_size()
	substance_per_maze = world_size * (2 ** (maze_upgrades - 1))
	
	# 根据资源决定策略
	if substance_available >= substance_per_maze * 10:
		# 资源充足，生成并重用9次
		return farm_maze(9)
	elif substance_available >= substance_per_maze * 5:
		# 中等资源，重用4次
		return farm_maze(4)
	elif substance_available >= substance_per_maze * 2:
		# 少量资源，重用1次
		return farm_maze(1)
	elif substance_available >= substance_per_maze:
		# 最少资源，只生成一次
		return farm_maze(0)
	else:
		# 资源不足
		return False

def farm_maze_smart(target_size=None):
	# 保存原始农场大小
	original_size = get_world_size()
	
	# 如果指定了目标大小，调整农场
	if target_size != None and target_size != original_size:
		set_world_size(target_size)
	
	# 执行迷宫探索（使用最优策略）
	result = farm_maze_optimal()
	
	# 恢复原始农场大小
	if target_size != None and target_size != original_size:
		set_world_size(original_size)
	
	return result

# ===== 使用示例 =====
# 
# 1. 基础迷宫（一次）
# crop_maze.farm_maze(0)
#
# 2. 重用迷宫5次
# crop_maze.farm_maze(5)
#
# 3. 自动最优策略
# crop_maze.farm_maze_optimal()
#
# 4. 指定大小（节省资源）
# crop_maze.farm_maze_smart(5)  # 使用5x5迷宫

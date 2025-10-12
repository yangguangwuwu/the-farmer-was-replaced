import utils

# ===== 树木种植（高价值木材） =====
# 优化：棋盘种植避免16倍生长时间惩罚，处理现有作物
def farm_trees():
	size = get_world_size()
	
	# 间隔种植（避免生长速度减慢）
	# 每个方向的相邻树使生长时间翻倍，4个方向=2^4=16倍
	# 棋盘模式避免所有4个方向的惩罚
	x = 0
	while x < size:
		y = 0
		while y < size:
			utils.move_to(x, y)
			
			entity = get_entity_type()
			
			# 每隔一格种树（棋盘模式）
			if (x + y) % 2 == 0:
				# 先尝试收获成熟作物，避免浪费
				# 草地特殊处理：直接收获
				if entity == Entities.Grass:
					harvest()
				elif can_harvest():
					harvest()
				
				entity = get_entity_type()
				
				# 种植树木（会自动清理枯萎南瓜和未成熟作物）
				if entity != Entities.Tree:
					plant(Entities.Tree)
					# 种植时就浇水
					if get_water() < 0.8:
						use_item(Items.Water)
			else:
				# 棋盘空位：清理所有作物，保持草地
				# 先尝试收获成熟作物，避免浪费
				# 草地特殊处理：直接收获
				if entity == Entities.Grass:
					harvest()
				elif can_harvest():
					harvest()
				
				entity = get_entity_type()
				
				# 清理非草地作物，转回草地
				if entity != None and entity != Entities.Grass:
					# 转回草地（会自动清理未成熟作物和枯萎南瓜）
					if get_ground_type() == Grounds.Soil:
						till()
			
			y = y + 1
		x = x + 1
	
	# 等待成熟（不用肥料，避免感染减产）
	all_mature = False
	while not all_mature:
		all_mature = True
		x = 0
		while x < size:
			y = 0
			while y < size:
				utils.move_to(x, y)
				if get_entity_type() == Entities.Tree:
					if not can_harvest():
						all_mature = False
						# 高水位=5倍速度
						if get_water() < 0.8:
							use_item(Items.Water)
				y = y + 1
			x = x + 1
	
	# 收获（每棵树5份木材）
	x = 0
	while x < size:
		y = 0
		while y < size:
			utils.move_to(x, y)
			if can_harvest():
				harvest()
			y = y + 1
		x = x + 1

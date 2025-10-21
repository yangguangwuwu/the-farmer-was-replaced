import utils

# ===== 南瓜种植（巨型南瓜策略）优化版 =====
# 优化：处理场上现有作物，持续补种枯萎南瓜直到全部成熟
def farm_pumpkins():
	size = get_world_size()
	
	# 合并阶段：清理并种植满场南瓜，同时进行初始浇水
	x = 0
	y = 0
	direction = 1  # 1 表示向右，-1 表示向左
	
	# 蛇形路径移动，提高效率
	withered_positions = []
	while x < size:
		# 根据方向确定y的起始和结束值
		if direction == 1:
			y = 0
			y_end = size
		else:
			y = size - 1
			y_end = -1
		
		while y != y_end:
			utils.move_to(x, y)
			utils.tilling()
			
			entity = get_entity_type()
			
			# 先尝试收获成熟作物，避免浪费
			# 草地特殊处理：直接收获
			if entity == Entities.Grass:
				harvest()
			elif can_harvest():
				harvest()
			
			entity = get_entity_type()
			
			# 种植南瓜（会自动清理枯萎南瓜和未成熟作物）
			if entity != Entities.Pumpkin:
				plant(Entities.Pumpkin)
			
			# 高水位加速成熟（只在需要时浇水）
			if get_water() < 0.8:
				use_item(Items.Water)
			
			# 检查是否为枯萎南瓜
			if entity != Entities.Pumpkin:
				withered_positions.append((x, y))
			
			# 根据方向更新y值
			y = y + direction
		
		# 更新方向和x值
		direction = direction * -1
		x = x + 1
	
	# 循环检查枯萎南瓜位置，直到全部成熟
	while withered_positions:
		new_withered = []
		
		# 只检查上一轮枯萎南瓜的位置
		for pos in withered_positions:
			x, y = pos
			utils.move_to(x, y)
			entity = get_entity_type()
			
			if entity == Entities.Pumpkin:
				if not can_harvest():
					# 仍未成熟，继续等待
					new_withered.append(pos)
					# 高水位加速成熟（只在需要时浇水）
					if get_water() < 0.8:
						use_item(Items.Water)
				# else: 已成熟，从列表中移除（不加入new_withered）
			else:
				# 又枯萎了，补种并继续记录
				plant(Entities.Pumpkin)
				new_withered.append(pos)
		
		withered_positions = new_withered
	
	# 收获巨型南瓜（nxn产出n*n*n，n>=6时产出n*n*6）
	if can_harvest():
		harvest()

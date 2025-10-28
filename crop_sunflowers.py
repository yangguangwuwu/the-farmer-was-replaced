import utils

# ===== 向日葵种植（能量收集） =====
# 优化：收获所有最大花瓣数的向日葵，每株都获得5倍能量！
def farm_sunflowers():
	size = get_world_size()
	
	# 存储每个位置的花瓣数 {(x,y): petals}
	petal_map = {}
	
	# 使用蛇形路径移动，提高效率
	x = 0
	y = 0
	direction = 1  # 1 表示向右，-1 表示向左
	
	# 按照蛇形路径遍历整个农场
	while x < size:
		# 根据方向确定y的起始和结束值
		if direction == 1:
			y_start = 0
			y_end = size
		else:
			y_start = size - 1
			y_end = -1
		
		y = y_start
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
			
			# 种植向日葵（会自动清理枯萎南瓜和未成熟作物）
			if entity != Entities.Sunflower:
				plant(Entities.Sunflower)
			
			if get_water() < 0.75:
				use_item(Items.Water)
			
			# 立即测量并存储花瓣数（种植后就能测量）
			petals = measure()
			petal_map[(x, y)] = petals
			
			# 根据方向更新y值
			y = y + direction
		
		# 更新方向和x值
		direction = direction * -1
		x = x + 1
	
	# 等待成熟（只需检查第一个种植的向日葵）
	# 因为是同时种植，第一个成熟了其他的也都成熟了
	utils.move_to(0, 0)
	while not can_harvest():
		# 维持更高水位获得5倍速度
		if get_water() < 0.8:
			use_item(Items.Water)
	
	# 持续收获最大花瓣数的向日葵（每次都获得5倍能量！）
	# 利用已存储的花瓣数，无需重复测量
	while petal_map:
		# 如果petal_map长度小于10，跳出循环
		if len(petal_map) < 10:
			petal_map = {}
			break
		# 找出当前最大花瓣数
		current_max = 0
		for pos in petal_map:
			petals = petal_map[pos]
			if petals > current_max:
				current_max = petals
		
		# 收获所有当前最大花瓣数的向日葵
		positions_to_remove = []
		for pos in petal_map:
			if petal_map[pos] == current_max:
				x, y = pos
				utils.move_to(x, y)
				if get_entity_type() == Entities.Sunflower and can_harvest():
					harvest()
					positions_to_remove.append(pos)
		
		# 从字典中移除已收获的位置
		for pos in positions_to_remove:
			petal_map.pop(pos)

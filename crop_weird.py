import utils

# ===== 奇异物质收集（感染策略） =====
# 优化：全场感染+快速收获，最大化奇异物质产量
# 原理：感染植物收获时50%产量变为奇异物质

def farm_weird_substance():
	size = get_world_size()
	
	# 第一阶段：种植快速生长的作物（选择草地，生长最快）
	x = 0
	while x < size:
		y = 0
		while y < size:
			utils.move_to(x, y)
			
			# 先尝试收获成熟作物
			if can_harvest():
				harvest()
			
			# 确保是草地（最快收获周期）
			if get_ground_type() == Grounds.Soil:
				till()
			
			y = y + 1
		x = x + 1
	
	# 第二阶段：使用肥料加速生长并感染所有植物
	x = 0
	while x < size:
		y = 0
		while y < size:
			utils.move_to(x, y)
			
			entity = get_entity_type()
			
			# 对草地使用肥料（加速生长+感染）
			if entity == Entities.Grass:
				# 使用肥料：减少2秒生长时间+感染
				if num_items(Items.Fertilizer) > 0:
					use_item(Items.Fertilizer)
			
			y = y + 1
		x = x + 1
	
	# 第三阶段：等待第一个草成熟
	utils.move_to(0, 0)
	while not can_harvest():
		# 继续使用肥料加速
		if num_items(Items.Fertilizer) > 0:
			use_item(Items.Fertilizer)
	
	# 第四阶段：收获所有感染的草（获得50%干草+50%奇异物质）
	x = 0
	while x < size:
		y = 0
		while y < size:
			utils.move_to(x, y)
			if can_harvest():
				harvest()
			y = y + 1
		x = x + 1


# ===== 高级策略：最大化奇异物质（使用胡萝卜/南瓜） =====
# 优化：种植高价值作物+全场感染，获得更多奇异物质
def farm_weird_substance_advanced():
	size = get_world_size()
	
	# 第一阶段：种植胡萝卜（产量高于草地）
	x = 0
	while x < size:
		y = 0
		while y < size:
			utils.move_to(x, y)
			utils.tilling()
			
			entity = get_entity_type()
			
			# 先收获成熟作物
			if entity == Entities.Grass:
				harvest()
			elif can_harvest():
				harvest()
			
			entity = get_entity_type()
			
			# 种植胡萝卜
			if entity != Entities.Carrot:
				if num_items(Items.Carrot) >= 1:
					plant(Entities.Carrot)
			
			y = y + 1
		x = x + 1
	
	# 第二阶段：全场施肥感染
	x = 0
	while x < size:
		y = 0
		while y < size:
			utils.move_to(x, y)
			
			entity = get_entity_type()
			
			if entity == Entities.Carrot:
				# 使用肥料感染（加速+感染）
				while num_items(Items.Fertilizer) > 0:
					use_item(Items.Fertilizer)
					# 多次施肥进一步加速
					if get_water() < 0.75:
						use_item(Items.Water)
					# 如果已成熟则停止
					if can_harvest():
						break
			
			y = y + 1
		x = x + 1
	
	# 第三阶段：等待第一个胡萝卜成熟
	utils.move_to(0, 0)
	while not can_harvest():
		if num_items(Items.Fertilizer) > 0:
			use_item(Items.Fertilizer)
		if get_water() < 0.75:
			use_item(Items.Water)
	
	# 第四阶段：收获所有感染的胡萝卜
	# 50%胡萝卜+50%奇异物质
	x = 0
	while x < size:
		y = 0
		while y < size:
			utils.move_to(x, y)
			if can_harvest():
				harvest()
			y = y + 1
		x = x + 1


# ===== 终极策略：连锁感染（利用奇异物质扩散） =====
# 优化：少量肥料+奇异物质扩散，全场感染
def farm_weird_substance_chain():
	size = get_world_size()
	
	# 第一阶段：种植草地
	x = 0
	while x < size:
		y = 0
		while y < size:
			utils.move_to(x, y)
			
			if can_harvest():
				harvest()
			
			if get_ground_type() == Grounds.Soil:
				till()
			
			y = y + 1
		x = x + 1
	
	# 第二阶段：只在中心点施肥感染
	center = size / 2
	utils.move_to(center, center)
	if num_items(Items.Fertilizer) > 0:
		use_item(Items.Fertilizer)
	
	# 第三阶段：使用奇异物质扩散感染
	# 策略：在感染植物上使用奇异物质，会感染相邻植物
	if num_items(Items.Weird_Substance) > 0:
		# 从中心向外扩散
		utils.move_to(center, center)
		use_item(Items.Weird_Substance)
		
		# 相邻位置会被感染，继续扩散
		x = 0
		while x < size:
			y = 0
			while y < size:
				utils.move_to(x, y)
				# 如果有奇异物质，继续扩散感染
				if num_items(Items.Weird_Substance) > 0:
					use_item(Items.Weird_Substance)
				y = y + 1
			x = x + 1
	
	# 第四阶段：等待成熟
	utils.move_to(0, 0)
	while not can_harvest():
		if get_water() < 0.75:
			use_item(Items.Water)
	
	# 第五阶段：收获
	x = 0
	while x < size:
		y = 0
		while y < size:
			utils.move_to(x, y)
			if can_harvest():
				harvest()
			y = y + 1
		x = x + 1

import utils

# ===== 胡萝卜种植（基础作物） =====
# 优化：快速种植和收获，处理现有作物
def farm_carrots():
	size = get_world_size()
	
	# 清理并种植胡萝卜
	x = 0
	while x < size:
		y = 0
		while y < size:
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
			
			# 种植胡萝卜（会自动清理枯萎南瓜和未成熟作物）
			if entity != Entities.Carrot:
				plant(Entities.Carrot)
				# 种植后立即浇水，5倍速度
				if get_water() < 0.8:
					use_item(Items.Water)
			
			y = y + 1
		x = x + 1
	
	# 收获
	x = 0
	while x < size:
		y = 0
		while y < size:
			utils.move_to(x, y)
			if can_harvest():
				harvest()
			y = y + 1
		x = x + 1

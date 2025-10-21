import utils

# ===== 胡萝卜种植（基础作物）优化版 =====
# 优化：快速种植和收获，处理现有作物，采用蛇形路径提高效率
def farm_carrots():
	size = get_world_size()
	
	# 使用蛇形路径移动，提高效率
	x = 0
	y = 0
	direction = 1  # 1 表示向右，-1 表示向左
	
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
			
			# 获取实体类型并处理
			entity = get_entity_type()
			
			# 先尝试收获成熟作物，避免浪费
			# 草地特殊处理：直接收获
			if entity == Entities.Grass:
				harvest()
			elif can_harvest():
				harvest()
			
			# 种植胡萝卜（会自动清理枯萎南瓜和未成熟作物）
			# 检查当前实体是否为胡萝卜
			plant(Entities.Carrot)
			# 种植后立即浇水，5倍速度
			if get_water() < 0.8:
				use_item(Items.Water)
			# 根据方向更新y值
			y = y + direction
		
		# 更新方向和x值
		direction = direction * -1
		x = x + 1

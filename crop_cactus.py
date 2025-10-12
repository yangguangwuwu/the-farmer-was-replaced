import utils

# ===== 仙人掌排序收获 =====
# 优化：完整冒泡排序确保正确排序，从左下角收获获得n²产量
def farm_cactus():
	size = get_world_size()
	
	# 清理并种植仙人掌
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
			
			# 种植仙人掌（会自动清理枯萎南瓜和未成熟作物）
			if entity != Entities.Cactus:
				plant(Entities.Cactus)
			
			y = y + 1
		x = x + 1
	
	# 等待成熟（只检查第一个仙人掌，因为同时种植）
	utils.move_to(0, 0)
	while not can_harvest():
		# 中等水位节省水资源
		if get_water() < 0.7:
			use_item(Items.Water)
	
	# 优化冒泡排序（逐行/逐列完成策略）
	# 关键优化1：行排序完成后，列排序不会破坏行的顺序
	# 关键优化2：逐行完成排序，减少长距离移动，提高局部性
	
	# 第一步：逐行排序（每行完整排序后再处理下一行）
	y = 0
	while y < size:
		# 对当前行进行冒泡排序直到完成
		row_sorted = False
		while not row_sorted:
			row_sorted = True
			x = 0
			while x < size - 1:
				utils.move_to(x, y)
				size1 = measure()
				size2 = measure(East)
				
				if size1 > size2:
					swap(East)
					row_sorted = False
				
				x = x + 1
		
		y = y + 1
	
	# 第二步：逐列排序（每列完整排序后再处理下一列）
	x = 0
	while x < size:
		# 对当前列进行冒泡排序直到完成
		col_sorted = False
		while not col_sorted:
			col_sorted = True
			y = 0
			while y < size - 1:
				utils.move_to(x, y)
				size1 = measure()
				size2 = measure(North)
				
				if size1 > size2:
					swap(North)
					col_sorted = False
				
				y = y + 1
		
		x = x + 1
	
	# 从左下角(0,0)收获，递归收获整片田地，获得n²产量
	utils.move_to(0, 0)
	harvest()

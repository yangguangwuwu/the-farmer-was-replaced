import utils

# ===== 混合种植（伴生植物策略）优化版 =====
# 优化：利用伴生植物机制，获得5倍（或更高）产量
# 支持：Grass、Bush、Tree、Carrot
# 参数：main_crop - 指定主作物类型（Entities.Bush/Tree/Carrot/Grass，默认Bush）
def farm_mixed(main_crop=None):
	size = get_world_size()
	
	# 如果未指定主作物，默认使用Bush
	if main_crop == None:
		main_crop = Entities.Bush
	
	# 存储伴生需求 {(x,y): (companion_type, (cx, cy))}
	companion_map = {}
	
	# 使用蛇形路径移动，提高效率
	x = 0
	y = 0
	direction = 1  # 1 表示向右，-1 表示向左
	
	# 合并阶段：种植主作物并记录伴生需求
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
			if entity == Entities.Grass:
				harvest()
			elif can_harvest():
				harvest()
			
			entity = get_entity_type()
			
			# 如果主作物是Tree，使用棋盘种植（避免16倍生长时间惩罚）
			should_plant_here = True
			if main_crop == Entities.Tree:
				if (x + y) % 2 != 0:
					should_plant_here = False
			
			# 种植指定的主作物
			if should_plant_here and entity != main_crop:
				# 检查资源是否足够
				can_plant = False
				if main_crop == Entities.Bush:
					if num_items(Items.Wood) >= 5:
						can_plant = True
				elif main_crop == Entities.Tree:
					can_plant = True  # Tree无需资源
				elif main_crop == Entities.Carrot:
					if num_items(Items.Carrot) >= 1:
						can_plant = True
				elif main_crop == Entities.Grass:
					# 转回草地
					if get_ground_type() == Grounds.Soil:
						till()
					can_plant = True
				
				# 种植主作物
				if can_plant and main_crop != Entities.Grass:
					plant(main_crop)
			
			# 获取伴生需求（只记录已种植的主作物）
			if should_plant_here:
				companion_info = get_companion()
				if companion_info != None:
					companion_type, companion_pos = companion_info
					companion_map[(x, y)] = (companion_type, companion_pos)
			
			# 根据方向更新y值
			y = y + direction
		
		# 更新方向和x值
		direction = direction * -1
		x = x + 1
	
	# 第二阶段：种植伴生植物
	# 统计每个位置被需要的次数
	position_demand = {}
	for main_pos in companion_map:
		companion_type, companion_pos = companion_map[main_pos]
		
		if companion_pos not in position_demand:
			position_demand[companion_pos] = []
		
		position_demand[companion_pos].append((main_pos, companion_type))
	
	# 存储主作物坐标列表
	main_crop_positions = []
	for main_pos in companion_map:
		main_crop_positions.append(main_pos)
	
	# 种植伴生植物（优先满足需求最多的位置）
	for comp_pos in position_demand:
		cx, cy = comp_pos
		# 检查位置是否在场地范围内
		if cx >= 0 and cx < size and cy >= 0 and cy < size:
			utils.move_to(cx, cy)
			entity = get_entity_type()
			
			# 收获现有作物
			if entity == Entities.Grass:
				harvest()
			elif can_harvest():
				harvest()
			
			entity = get_entity_type()
			
			# 找出这个位置最需要的伴生植物类型
			# 如果多个主植物需要不同类型，选择需求最多的
			type_count = {}
			for main_pos, comp_type in position_demand[comp_pos]:
				if comp_type not in type_count:
					type_count[comp_type] = 0
				type_count[comp_type] = type_count[comp_type] + 1
			
			# 找出需求最多的类型
			best_type = None
			max_count = 0
			for comp_type in type_count:
				if type_count[comp_type] > max_count:
					max_count = type_count[comp_type]
					best_type = comp_type
			
			# 种植伴生植物
			if best_type != None:
				if best_type == Entities.Grass:
					# 转回草地
					if get_ground_type() == Grounds.Soil:
						till()
					# 如果这个位置原本是主作物，需要从主作物坐标列表中移除
					if (cx, cy) in main_crop_positions:
						main_crop_positions.remove((cx, cy))
				elif best_type == Entities.Bush:
					if num_items(Items.Wood) >= 5:
						plant(Entities.Bush)
						# 如果这个位置原本是主作物，需要从主作物坐标列表中移除
						if (cx, cy) in main_crop_positions:
							main_crop_positions.remove((cx, cy))
				elif best_type == Entities.Tree:
					plant(Entities.Tree)
					# 如果这个位置原本是主作物，需要从主作物坐标列表中移除
					if (cx, cy) in main_crop_positions:
						main_crop_positions.remove((cx, cy))
				elif best_type == Entities.Carrot:
					if num_items(Items.Carrot) >= 1:
						plant(Entities.Carrot)
						# 如果这个位置原本是主作物，需要从主作物坐标列表中移除
						if (cx, cy) in main_crop_positions:
							main_crop_positions.remove((cx, cy))

	for main_pos in main_crop_positions:
		x, y = main_pos
		utils.move_to(x, y)
		entity = get_entity_type()
		
		# 收获主作物
		if entity == main_crop and can_harvest():
			harvest()

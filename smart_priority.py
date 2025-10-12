# ===== 智能作物控制器 =====
# 用户自定义优先级 + 自动资源管理 + 效率最大化

import utils
import crop_grass
import crop_trees
import crop_carrots
import crop_pumpkins
import crop_sunflowers
import crop_cactus
import crop_mix
import crop_weird
import crop_dinosaur
import crop_maze
from config import PRIORITY, THRESHOLDS

# ====================================
# 🧠 智能决策系统
# ====================================

def check_resources():
	return {
		"power": num_items(Items.Power),
		"carrot": num_items(Items.Carrot),
		"wood": num_items(Items.Wood),
		"pumpkin": num_items(Items.Pumpkin),
		"hay": num_items(Items.Hay),
		"fertilizer": num_items(Items.Fertilizer),
		"water": num_items(Items.Water),
		"cactus": num_items(Items.Cactus),
		"weird_substance": num_items(Items.Weird_Substance),
		"bone": num_items(Items.Bone),
		"gold": num_items(Items.Gold),
	}

def can_plant_crop(crop_info, resources):
	# 解析crop_info字典
	crop_name = crop_info["crop"]
	main_crop = None
	if "main" in crop_info:
		main_crop = crop_info["main"]
	
	# 草地：无需资源
	if crop_name == "grass":
		return True
	
	# 树木：需要在草地上种植（无消耗）
	if crop_name == "trees":
		return True
	
	# 混合种植：根据主作物类型检查资源
	if crop_name == "mixed":
		if main_crop == Entities.Bush:
			if resources["wood"] >= 10:  # Bush需要木材
				return True
			return False
		elif main_crop == Entities.Tree:
			return True  # Tree无需资源
		elif main_crop == Entities.Carrot:
			if resources["carrot"] >= 10:
				return True
			return False
		else:
			return True  # Grass无需资源
	
	# 奇异物质：需要肥料
	if crop_name == "weird":
		if resources["fertilizer"] >= THRESHOLDS["fertilizer_min"]:
			return True
		return False
	
	# 恐龙：需要仙人掌（购买苹果）
	if crop_name == "dinosaur":
		# 根据养殖模式检查资源
		dino_mode = "optimal"  # 默认模式
		if "mode" in crop_info:
			dino_mode = crop_info["mode"]
		
		# optimal模式：根据仙人掌数量自动决定
		if dino_mode == "optimal":
			if resources["cactus"] >= 400:  # 至少2x2农场
				return True
			return False
		
		# full模式：需要更多仙人掌填满当前农场
		elif dino_mode == "full":
			field_size = get_world_size()
			required_cactus = field_size * field_size
			if resources["cactus"] >= required_cactus:
				return True
			return False
		
		# efficient模式：检查是否有指定数量的仙人掌
		else:
			apple_count = 20  # 默认20个苹果
			if "apples" in crop_info:
				apple_count = crop_info["apples"]
			if resources["cactus"] >= apple_count:
				return True
			return False
	
	# 迷宫：需要奇异物质
	if crop_name == "maze":
		# 检查是否解锁迷宫
		maze_upgrades = num_unlocked(Unlocks.Mazes)
		if maze_upgrades == 0:
			return False
		
		# 计算所需奇异物质
		field_size = get_world_size()
		substance_per_maze = field_size * (2 ** (maze_upgrades - 1))
		
		# 检查模式
		maze_mode = "optimal"
		if "mode" in crop_info:
			maze_mode = crop_info["mode"]
		
		# optimal模式：至少能生成一次
		if maze_mode == "optimal":
			if resources["weird_substance"] >= substance_per_maze:
				return True
			return False
		
		# smart模式：检查指定大小
		elif maze_mode == "smart":
			target_size = field_size
			if "size" in crop_info:
				target_size = crop_info["size"]
			required = target_size * (2 ** (maze_upgrades - 1))
			if resources["weird_substance"] >= required:
				return True
			return False
		
		# 默认：检查基础资源
		else:
			reuse = 0
			if "reuse" in crop_info:
				reuse = crop_info["reuse"]
			required = substance_per_maze * (reuse + 1)
			if resources["weird_substance"] >= required:
				return True
			return False
	
	# 获取作物对应的Entity类型
	entity_type = None
	if crop_name == "carrots":
		entity_type = Entities.Carrot
	elif crop_name == "pumpkins":
		entity_type = Entities.Pumpkin
	elif crop_name == "sunflowers":
		entity_type = Entities.Sunflower
	elif crop_name == "cactus":
		entity_type = Entities.Cactus
	else:
		return False
	
	# 使用get_cost()获取准确成本
	cost = get_cost(entity_type)
	if cost == None:
		return True  # 无成本要求
	
	# 计算需要种满全场的资源
	field_size = get_world_size()
	total_plants = field_size * field_size
	
	# 检查每种资源是否充足
	for item in cost:
		amount_per_plant = cost[item]
		# 保守估计：至少能种满一半田地
		required = amount_per_plant * (total_plants / 2)
		
		# 根据item类型检查资源
		if item == Items.Carrot:
			if resources["carrot"] < required:
				return False
		elif item == Items.Wood:
			if resources["wood"] < required:
				return False
		elif item == Items.Hay:
			if resources["hay"] < required:
				return False
		elif item == Items.Pumpkin:
			if resources["pumpkin"] < required:
				return False
	
	return True

def get_crop_benefit(crop_info, resources):
	# 解析crop_info字典
	crop_name = crop_info["crop"]
	main_crop = None
	if "main" in crop_info:
		main_crop = crop_info["main"]
	
	score = 0
	
	# 能量紧急情况：向日葵最高优先级
	if resources["power"] < THRESHOLDS["power_low"]:
		if crop_name == "sunflowers":
			return 1000  # 紧急最高优先级
	
	# 基础资源短缺
	if resources["carrot"] < THRESHOLDS["carrot_min"]:
		if crop_name == "carrots":
			return 900
		if crop_name == "grass":
			return 850  # 草能产干草，间接帮助种胡萝卜
	
	if resources["wood"] < THRESHOLDS["wood_min"]:
		if crop_name == "trees":
			return 880
		# 木材短缺时，混合种植优先级降低
		if crop_name == "mixed":
			return 0  # 资源不足，跳过
	
	if resources["hay"] < THRESHOLDS["hay_min"]:
		if crop_name == "grass":
			return 870
	
	# 能量充足且资源充足：种植高价值作物
	if resources["power"] >= THRESHOLDS["power_safe"]:
		if crop_name == "maze":
			return 580  # 迷宫：n²金币（重用可叠加）
		if crop_name == "dinosaur":
			return 570  # 恐龙：n²根骨头（远古资源）
		if crop_name == "weird":
			return 560  # 奇异物质：利用肥料获取特殊资源
		if crop_name == "mixed":
			return 550  # 混合种植：5倍产量（最高优先级）
		if crop_name == "cactus":
			return 500  # 仙人掌：n²产量
		if crop_name == "pumpkins":
			return 450  # 南瓜：n³产量
	
	# 维持能量水平
	if resources["power"] < THRESHOLDS["power_safe"]:
		if crop_name == "sunflowers":
			return 400
	
	# 默认分数
	return 100

def select_best_crop(resources):
	
	# 按用户配置的优先级顺序检查
	best_crop = None
	best_score = -1
	best_priority = 999
	
	# 遍历所有优先级作物
	for crop_info in PRIORITY:
		priority_index = 0
		temp_index = 0
		for c in PRIORITY:
			if c == crop_info:
				priority_index = temp_index
			temp_index = temp_index + 1
		
		# 检查是否有足够资源
		if can_plant_crop(crop_info, resources):
			# 计算收益分数
			benefit = get_crop_benefit(crop_info, resources)
			
			# 结合优先级和收益分数
			# 紧急情况（benefit > 800）忽略用户优先级
			if benefit > 800:
				if benefit > best_score:
					best_crop = crop_info
					best_score = benefit
					best_priority = priority_index
			else:
				# 正常情况下遵循用户优先级
				if priority_index < best_priority:
					best_crop = crop_info
					best_score = benefit
					best_priority = priority_index
	
	return best_crop

def plant_crop(crop_info):
	# 解析crop_info字典
	crop_name = crop_info["crop"]
	main_crop = None
	strategy = None
	if "main" in crop_info:
		main_crop = crop_info["main"]
	if "strategy" in crop_info:
		strategy = crop_info["strategy"]
	
	if crop_name == "grass":
		crop_grass.farm_grass()
	elif crop_name == "trees":
		crop_trees.farm_trees()
	elif crop_name == "carrots":
		crop_carrots.farm_carrots()
	elif crop_name == "pumpkins":
		crop_pumpkins.farm_pumpkins()
	elif crop_name == "sunflowers":
		crop_sunflowers.farm_sunflowers()
	elif crop_name == "cactus":
		crop_cactus.farm_cactus()
	elif crop_name == "mixed":
		crop_mix.farm_mixed(main_crop)
	elif crop_name == "weird":
		# 根据策略选择不同的奇异物质收集方法
		if strategy == "basic":
			crop_weird.farm_weird_substance()
		elif strategy == "chain":
			crop_weird.farm_weird_substance_chain()
		else:
			# 默认使用高产策略
			crop_weird.farm_weird_substance_advanced()
	elif crop_name == "dinosaur":
		# 根据模式选择不同的恐龙养殖方法
		dino_mode = "optimal"  # 默认模式
		if "mode" in crop_info:
			dino_mode = crop_info["mode"]
		
		if dino_mode == "full":
			# 填满整个当前农场
			crop_dinosaur.farm_dinosaur()
		elif dino_mode == "efficient":
			# 只吃指定数量的苹果
			apple_count = 20
			if "apples" in crop_info:
				apple_count = crop_info["apples"]
			crop_dinosaur.farm_dinosaur_efficient(apple_count)
		else:
			# 最优策略（根据仙人掌自动决定）
			crop_dinosaur.farm_dinosaur_optimal()
	elif crop_name == "maze":
		# 根据模式选择不同的迷宫策略
		maze_mode = "optimal"  # 默认模式
		if "mode" in crop_info:
			maze_mode = crop_info["mode"]
		
		if maze_mode == "smart":
			# 智能模式：指定迷宫大小
			target_size = None
			if "size" in crop_info:
				target_size = crop_info["size"]
			crop_maze.farm_maze_smart(target_size)
		elif maze_mode == "optimal":
			# 最优模式：自动决定重用次数
			crop_maze.farm_maze_optimal()
		else:
			# 基础模式：指定重用次数
			reuse_count = 0
			if "reuse" in crop_info:
				reuse_count = crop_info["reuse"]
			crop_maze.farm_maze(reuse_count)

# ====================================
# 🚀 主循环
# ====================================

while True:
	# 检查当前资源
	resources = check_resources()
	
	# 智能选择最佳作物
	best_crop = select_best_crop(resources)
	
	if best_crop:
		# 种植选中的作物
		plant_crop(best_crop)
	else:
		# 如果所有作物都无法种植，收割草地获取基础资源
		crop_grass.farm_grass()

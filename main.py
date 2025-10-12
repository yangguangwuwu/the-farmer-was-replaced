# ===== 超级高效多作物自动化农场 =====
# 智能资源管理 + 优化种植策略 + 自动化轮作

# 导入工具库和各种作物模块
import utils
import crop_grass
import crop_trees
import crop_carrots
import crop_pumpkins
import crop_sunflowers
import crop_cactus

# ===== 主循环：智能优先级系统 =====
while True:
	# 检查资源状态
	power = num_items(Items.Power)
	carrot = num_items(Items.Carrot)
	wood = num_items(Items.Wood)
	pumpkin = num_items(Items.Pumpkin)
	hay = num_items(Items.Hay)
	fertilizer = num_items(Items.Fertilizer)
	
	# 优先级1：能量管理（能量<100时优先种向日葵）
	if power < 100:
		crop_sunflowers.farm_sunflowers()
	
	# 优先级2：基础资源（胡萝卜<300时种胡萝卜）
	elif carrot < 300:
		crop_carrots.farm_carrots()
	
	# 优先级3：木材收集（木材<800时种树）
	elif wood < 800:
		crop_trees.farm_trees()
	
	# 优先级4：高价值作物（有充足胡萝卜时种南瓜）
	elif carrot > 400:
		crop_pumpkins.farm_pumpkins()
	
	# 优先级5：持续向日葵（维持能量）
	elif power < 300:
		crop_sunflowers.farm_sunflowers()
	
	# 优先级6：顶级作物（仙人掌）
	else:
		crop_cactus.farm_cactus()
			
		
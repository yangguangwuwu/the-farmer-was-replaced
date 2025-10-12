import utils

# ===== 草地收割（最快，获取干草） =====
def farm_grass():
	size = get_world_size()
	x = 0
	while x < size:
		y = 0
		while y < size:
			utils.move_to(x, y)
			if can_harvest():
				harvest()
			# 确保是草地
			if get_ground_type() == Grounds.Soil:
				till()  # 转回草地
			
			# 收获成熟的草
			if can_harvest():
				harvest()
			
			y = y + 1
		x = x + 1

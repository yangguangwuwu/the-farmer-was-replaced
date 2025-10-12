def is_even(n):
	return n % 2 == 0

# 移动到指定位置（优化：利用环形世界特性）
def move_to(target_x, target_y):
	current_x = get_pos_x()
	current_y = get_pos_y()
	world_size = get_world_size()
	
	# 计算X轴最短路径（考虑环形世界）
	dx = target_x - current_x
	# 如果绕过边界更近，则使用环形路径
	if dx > world_size / 2:
		dx = dx - world_size  # 向西绕过边界
	elif dx < -world_size / 2:
		dx = dx + world_size  # 向东绕过边界
	
	# 移动X轴
	while current_x != target_x:
		if dx > 0:
			move(East)
		else:
			move(West)
		current_x = get_pos_x()
	
	# 计算Y轴最短路径（考虑环形世界）
	dy = target_y - current_y
	# 如果绕过边界更近，则使用环形路径
	if dy > world_size / 2:
		dy = dy - world_size  # 向南绕过边界
	elif dy < -world_size / 2:
		dy = dy + world_size  # 向北绕过边界
	
	# 移动Y轴
	while current_y != target_y:
		if dy > 0:
			move(North)
		else:
			move(South)
		current_y = get_pos_y()

def water():
	# 当水量低于50%时浇水
	if get_water() <= 0.5:
		use_item(Items.Water)

def tilling():
	# 确保土地已耕种
	if get_ground_type() != Grounds.Soil:
		till()

def water_full():
	# 浇水至满
	while get_water() < 0.9:
		use_item(Items.Water)
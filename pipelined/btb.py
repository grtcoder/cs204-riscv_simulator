''' add curr_pc and iag from where this is called
if branch is taken , then try to load from btb
if load is unsuccessful, then return value is -1, otherwise we get the target_pc
check btb for next pc during fetch as we only need curr_pc.
'''
class branch_target_buffer():
	def __init__(self):
		self.btb = dict()
	
	def update(self,curr_pc,target_pc):
		self.btb[curr_pc] = target_pc
	
	def find(self,curr_pc):
		target_pc = self.btb.get(curr_pc)
		if(target_pc == None):
			return -1
		return target_pc
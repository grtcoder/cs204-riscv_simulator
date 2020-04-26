''' add curr_pc and iag from where this is called
if branch is taken , then try to load from btb
if load is unsuccessful, then return value is -1, otherwise we get the target_pc
check btb for next pc during fetch as we only need curr_pc.
'''
class branch_target_buffer():
	def __init__(self):
		self.btb = dict()
	
	def insert_val(self,curr_pc,target_pc,valid_bit,predictor_state):
		self.btb[curr_pc] = dict()
		self.btb[curr_pc]["target_address"] = target_pc
		self.btb[curr_pc]["valid_bit"] = valid_bit
		self.btb[curr_pc]["predictor_state"] = predictor_state
	
	def find(self,curr_pc):
		target_dict = self.btb.get(curr_pc)
		if(target_dict == None or target_dict["target_address"] == None or target_dict["valid_bit"]==0):
			return -1
		return target_dict["target_address"]

	def get_valid_bit(self,curr_pc):
		if(self.find(curr_pc)==-1):
			return -1
		return self.btb[curr_pc]["valid_bit"]

	def show(self):
		for x,y in self.btb.items():
			print(x," : ",y)
	
	def update(self,curr_pc,valid_bit):
		self.btb[curr_pc]["valid_bit"] = valid_bit

#!/usr/bin/python

# EE677 VLSI Project 
# This function call, fills a single LUT 
# with values according to definition of input subgraph

# Written by Shashank Gangrade 

_GATE = {'0':0, '1':1, 'and':2, 'nand':3, 'or':4, 'nor':5, 'xor':6, 'xnor':7}


# subgraph : adjacency matrix for small subgraphs with 
# at most 5 inputs and 1 output
# input : List of input nodes
# topo_order : Topological order in subgraph
# output : The output node

# The protocol for subgraph/nodes is similar to programming assignment
# This currently supports

def generateLUT(subgraph, input_nodes, topo_order, output_node):
	
	# input in the list 
	# pi is the number of inut nodes in graph which are not neccecarily 5
	pi = len(input_nodes)

	LUT_size = 5					# LUT by definition is 5 input
	LUT_array = (1<<5);				# Size of final LUT Array (32)
	
	num_sig = len(subgraph)			# Number of signals in graph
	sigval = [-1 for i in range(num_sig)]
	# signal values ( at the output ) of nodes.
    # +1 means HIGH, 0 means LOW, -1 means "undefined"

	LUT = [-4 for i in range(LUT_array)]	# Initilizig LUT list with -1
	input_list  = [[-1 for i in range(LUT_size)]for i in range(LUT_array)]

	# Initializing input_list with all posibble inputs
	for i in range(LUT_array):
		temps = bin(i)[2:].zfill(LUT_size)
		input_list[i] = map(int, temps) 
	
	node_temp = 0

	for i in range(LUT_array):

		for j in range(pi):
			sigval[input_nodes[j]] = input_list[i][j]
				# Part of input_list is applied to all the input nodes
				# This is because number of inputs in current LUT might be less		

		for jj in range(pi,num_sig):			# Computing rest of the nodes other than input
			node_temp = topo_order[jj]			# jj is the first node in topological order
			node_temp_inputs = 0
			temp_input = [-1 for n in range(num_sig)]

			for k in range(jj):
				if subgraph[topo_order[k]][node_temp] > -1 :
					temp_input[node_temp_inputs] = sigval[topo_order[k]]
					node_temp_inputs = node_temp_inputs + 1
#			print(temp_input)		

			# Find the gate corresponding to this node	
			column = []
			for z in range (len(subgraph)):
				row = subgraph[z]
				column.append(row[node_temp])

			gate = max(column)
#			print(gate)

			sigval[node_temp] = nodeSolver(gate, node_temp_inputs, temp_input)			

		LUT[i] = sigval[output_node]
	
	return LUT,input_list

# Solve Node
# Input gate, node_temp_inputs, temp_inputs			
# Output Value of sigval
def nodeSolver( gate, node_temp_inputs, temp_input ) :

	# NAND Operation
	if gate==3 :
		sigval=1
		for m in range(node_temp_inputs):
			sigval = sigval*temp_input[m]

		if	 sigval == 1 :
			sigval = 0
		elif sigval == 0 :
			sigval = 1

	# NOR Operation
	elif gate==5 :
		sigval=0
		for m in range(node_temp_inputs):
			sigval = sigval + temp_input[m]
		
		if sigval > 1 :
			sigval = 1

		if	 sigval == 1 :
			sigval = 0
		elif sigval == 0 :
			sigval = 1


	# OR Operation
	elif gate==4 :
		sigval=0
		for m in range(node_temp_inputs):
			sigval = sigval + temp_input[m]
		if sigval > 1 :
			sigval = 1

	# AND Operation	
	elif gate==2 :
		sigval=1
		for m in range(node_temp_inputs):
			sigval = sigval*temp_input[m]

	# XOR Operation	
	elif gate==6 :
		sigval = temp_input[0]
		for m in range(1,node_temp_inputs):
			sigval = sigval^temp_input[m]

	return sigval

## Main Function starts from here, modify to view changes 

nodes = 6
sub  = [[-1 for i in range(nodes)]for i in range(nodes)]
sub[0][5] = 6
sub[1][5] = 6
sub[2][5] = 6
sub[3][5] = 6
sub[4][5] = 6

input_nodes = [0, 1, 2, 3, 4]
topo_order = [0, 1, 2, 3, 4, 5]
output_node = 5

LUT, input_list = generateLUT(sub, input_nodes, topo_order, output_node)

for i in range(32):
	print (input_list[i])
	print (LUT[i])

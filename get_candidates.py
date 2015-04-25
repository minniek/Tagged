#/usr/bin/python
import os, sys

'''
Function definitions
'''
def generate_file(source, file_name):
	# Get source type before sorting
	source_type = str(type(source))
	print "Source type: ", source_type
	source = sorted(source) # sorted will return a list!
	with open(file_name, 'w') as output_file:
		for x in source:
			if 'set' in source_type:
				output_file.write(x)
			if 'list' in source_type:
				output_file.write(str(x) + "\n")

def are_elements_unique(list):
	no_dupes_set = set()
	for element in list:
		#print "Element: ", element
		if element in no_dupes_set:
			return False
		else:
			no_dupes_set.add(element)
	return True

'''
Main program
'''
# Get number of files
count = len(sys.argv) - 1
if count < 2:
	print "Error: need at least two files as command-line args. Exiting."
	exit(1)

# Store each file content as a set, and add to list "all_file_sets"
x = 1; all_file_sets = []; file_name_list = []
while x <= count:
	file_in = sys.argv[x]
	file_name_list.append(str(file_in))
	with open(file_in, 'r') as current_file:
		current_set = set(current_file); current_set.discard('\n'); all_file_sets.append(current_set)
		x += 1

# Get intersection of all file sets
same_set = set.intersection(all_file_sets[0], all_file_sets[1])
for s in all_file_sets:
	same_set.intersection_update(s)

# Write intersection to output text file
generate_file(same_set, 'intersection.txt')

# Get difference set for each file set in list "all_file_sets"
# Store all difference sets in list "all_file_difference_sets"
all_file_difference_sets = []
for file_set in all_file_sets:
	d = set.difference(file_set, same_set)
	all_file_difference_sets.append(d)

# Get ONLY the methods found in all_file_difference_sets
method_set = set()
for d in all_file_difference_sets:
	for element in d:
		if "=" in element: # Assuming only methods contain "=" (to avoid processing values such as "AE	+2518+05518	Asia/Dubai")
			method = element.split("=")[0]
			print "Method: ", method
			method_set.add(method)

'''
For each method, create a list that contains the method itself as the first element and then the return values from each device
Ex. [method_1, device_1_val, device_2_val, ..., device_n_val]
If return value of the method does not exist for a device, write "---" in its corresponding index to indicate "not available"
Store each method list (i.e. candidate) into list "candidate_list"
'''
candidate_list = []
for method in method_set:
	candidate = []; candidate.append(method)
	for current_candidate in all_file_difference_sets:
		# If method is in set, get the value and add it to list
		if any(method == element.split("=")[0] for element in current_candidate):
			#print "Method is in current set", method
			for element in current_candidate:
				#print "Element: ", element
				if method == element.split("=")[0]:
					value = element.split("=")[1]
					candidate.append(value.strip())
		# If method is not in set, write "---" to indicate "not available"
		else:
			candidate.append("---")
	candidate_list.append(candidate)

# Print all methods and values
generate_file(candidate_list, 'candidate_list_base.txt')

# Print only methods that contain values for each device
candidate_list_sorted = sorted(candidate_list)
with open('candidate_list_prefinal.txt', 'w') as output_file:
	output_file.write("Method\t")
	for file_name in file_name_list:
		output_file.write(file_name + "\t")
	output_file.write("\n")
	for candidate in candidate_list_sorted:
		if not "---" in candidate:
			output_file.write(str(candidate) + "\n")

# Print only methods that contain unique values for each device
with open('candidate_list_final.txt', 'w') as output_file:
	output_file.write("Method\t")
	for file_name in file_name_list:
		output_file.write(file_name + "\t")
	output_file.write("\n")
	for candidate in candidate_list_sorted:
		if not "---" in candidate and are_elements_unique(candidate):
			output_file.write(str(candidate) + "\n")

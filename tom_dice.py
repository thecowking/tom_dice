#! python 2.7
#Author: Dominic Kua
"""
This is a quick and dirty script to show why excel is not the tool for everything
It's a lot more extensible and mutable than the original spreadsheet, as you only need to add
a die to the dictionary and/or a combination to the combinations array
"""
try:
	from matplotlib import pyplot as plt
except ImportError:
	exit("""This script requires matplotlib installed, please pip install matplotlib.
		If you don't have Pip, you can find it here:
		https://pip.pypa.io/en/stable/installing/
		""")
try:
	import numpy as np
except ImportError:
	exit("""This script requires numpy installed, please pip install numpy.
		If you don't have Pip, you can find it here:
		https://pip.pypa.io/en/stable/installing/
		""")
#This is the global dice dictionary that we operate on, these dice can be edited, added to and otherwise changed before runtime. 
#Editing them on the fly is possible, but this is the easy way for a proof of concept. 
DICE_DICT = {'A': [0,1,2,3],'B' : [0,1,2,3,4,5],'C' : [0,1,2,3,4,5,6,7],'D' : [0,1,2,3,4,5,6,7,8,9],'E' : [0,1,2,3,4,5,6,7,8,9,10,11]}

#combinations can be added to this list by simply adding a string with the combination comma separated
combinations = ['A,A,B', 'A,B,B', 'A,B,C', 'B,B,C', 'B,C,C', 'B,C,D', 'C,C,D', 'C,D,D', 'C,D,E', 'D,D,E', 'D,E,E', 'D,E,E,A', 'D,E,E,B', 'D,E,E,C', 'D,E,E,D']

def make_combo_list():
	"""
	Splits the combinations into lists and then grabs
	the die values from the dictionary and puts
	all of these into a list of lists of lists
	sounds complicated but saves me moving everything
	in a variable number of variables. This should allow as
	many combinations as will fit in RAM.
	"""
	combo_dict = {}
	for combination in combinations:
		dice = combination.split(',')
		dice_array = []
		for die in dice:
			dice_array.append(DICE_DICT[die])
		combo_dict[combination] = dice_array
	return combo_dict

def cartesian(arrays, out=None):
    """
    Generate a cartesian product of input arrays.

    Parameters
    ----------
    arrays : list of array-like
        1-D arrays to form the cartesian product of.
    out : ndarray
        Array to place the cartesian product in.

    Returns
    -------
    out : ndarray
        2-D array of shape (M, len(arrays)) containing cartesian products
        formed of input arrays.

    Examples
    --------
    >>> cartesian(([1, 2, 3], [4, 5], [6, 7]))
    array([[1, 4, 6],
           [1, 4, 7],
           [1, 5, 6],
           [1, 5, 7],
           [2, 4, 6],
           [2, 4, 7],
           [2, 5, 6],
           [2, 5, 7],
           [3, 4, 6],
           [3, 4, 7],
           [3, 5, 6],
           [3, 5, 7]])

    """

    arrays = [np.asarray(x) for x in arrays]
    dtype = arrays[0].dtype

    n = np.prod([x.size for x in arrays])
    if out is None:
        out = np.zeros([n, len(arrays)], dtype=dtype)

    m = n / arrays[0].size
    out[:,0] = np.repeat(arrays[0], m)
    if arrays[1:]:
        cartesian(arrays[1:], out=out[0:m,1:])
        for j in xrange(1, arrays[0].size):
            out[j*m:(j+1)*m,1:] = out[0:m,1:]
    return out


def create_all_sums(combo_dict, out = None):
	"""
	Here's where programming shines. I am not going to write a function to create
	all the possible combinations, why would I need to? There's a library for
	that! Here, I'm using numpy, which is awesome. I also employed the 
	advanced programming technique known as 'stealing it from Stack Overflow'
	specifically, I used:
	https://stackoverflow.com/questions/1208118/using-numpy-to-build-an-array-of-all-combinations-of-two-arrays/1235363#1235363
	it was faster than working it out myself.
	"""
	dict_of_sums = {}
	dict_of_combos = {}
	for combination in combo_dict:
		#looks horribly nested, but basically adds a value from a call to 
		#the cartesian function to the dict. We will iterate over
		#these lists in the next step to make it all work 
		dict_of_combos[combination] = (cartesian(combo_dict[combination]))
	for dicty in dict_of_combos:
		list_of_sums = []
		for x in dict_of_combos[dicty]:
			list_of_sums.append(sum(x))
		dict_of_sums[dicty] = sorted(list_of_sums)
	return dict_of_sums

def main():
	combo_dict = make_combo_list()
	dict_of_sums = create_all_sums(combo_dict)
	"""
	I got tired here and gave up on names. 
	Whelk is a perfectly good name for keys in a 
	dictionary anyway. 
	"""
	for whelk in dict_of_sums:
		"""
		#this was debug code but you can uncomment it if you want to see its
		#output in the terminal
		print "***************"
		print whelk
		print dict_of_sums[whelk]
		print "*************"
		print "\n\n\n"
		"""
		freqency = counter(dict_of_sums[whelk])
		graph = np.histogram(dict_of_sums[whelk])
		plt.hist(graph[0], graph[1])
		plt.show()

if __name__ == "__main__":
	main()

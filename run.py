import sys
import numpy as np

from util import read_data_from_file, SS_Score, Max_Matrix_Score

def print_max_ss_scores():
	file_path = sys.argv[1]

	cases = read_data_from_file(file_path)

	for case in cases:
		max_ss_score = determine_max_ss_score(case)
		output_ss_score = str.format('{0:.2f}', max_ss_score)
		print output_ss_score
	
def determine_max_ss_score(case):
	customers = case[0]
	customers_len = len(customers)
	products = case[1]
	products_len = len(products)
	matrix = np.zeros( (customers_len, products_len))
	
	for customer_index in range(0, len(customers)):
		customer_name = customers[customer_index]
		for product_index in range(0, len(products)):
			product_name = products[product_index]
			ss_score = SS_Score(customer_name, product_name)
			score = ss_score.compute_score()
			matrix[customer_index][product_index] = score

	max_matrix_score = Max_Matrix_Score(matrix)
	combined_ss_score = max_matrix_score.compute_score()

	return combined_ss_score

print_max_ss_scores()

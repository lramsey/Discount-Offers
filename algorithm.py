import numpy as np
import re

def print_max_ss_scores(file_path):
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

####################### Read Data from File #######################

def read_data_from_file(file_path):
	f = open(file_path, 'r')
	decoded_text = ''
	for line in f:
		for item in line.split():
   			decoded_text += chr(int(item))
	
	f.close()

  	cases = decoded_text.split('\r\n')

  	cleaned_cases = []
  	for case in cases:
  		customers,products = case.split(';')
  		customer_names = customers.split(',')
  		product_names = products.split(',')
  		cleaned_cases.append([customer_names, product_names])

  	return cleaned_cases

####################### Scoring For Each Product Customer Pairing ########################

class SS_Score():
	def __init__(self, customer_name, product_name):
		self.customer_name = customer_name.lower()
		self.product_name = product_name.lower()

	def compute_score(self):
		customer_name_letter_count = self.count_letters(self.customer_name)
		product_name_letter_count = self.count_letters(self.product_name)
		if product_name_letter_count % 2 == 0:
			# SS Rule 1: for even letter count product name, count vowels * 1.5
			vowel_count = self.count_customer_vowels()
			base_score = vowel_count * 1.5
		else:
			# SS Rule 2: for odd letter count product name, count consonants
			consonant_count = self.count_customer_consonants()
			base_score = consonant_count

		customer_factors = self.find_factors_excluding_1(customer_name_letter_count)
		product_factors = self.find_factors_excluding_1(product_name_letter_count)

		if(self.has_customer_product_factors_match(customer_factors, product_factors)):
			# SS Rule 3: if factor is shared, multiply base score by 1.5
			score = base_score * 1.5
		else:
			score = base_score

		return score

	def count_letters(self, name):
		count = 0
		name = name.lower()
		for char in name:
			if re.match("^[a-z]*$", char):
				count += 1
		return count

	def count_customer_vowels(self):
		count = 0
		for char in self.customer_name:
			if re.match("^[aeiouy]*$", char):
				count += 1

		return count

	def count_customer_consonants(self):
		count = 0
		for char in self.customer_name:
			if re.match("^[b-df-hj-np-tv-xz]*$", char):
				count += 1

		return count

	def find_factors_excluding_1(self, number):
		factorsDict = {}
		for i in range(2, number + 1):
			if number % i == 0:
				factorsDict[i] = True
		return factorsDict

	def has_customer_product_factors_match(self, customer_factors, product_factors):
		for factor in customer_factors:
			if product_factors.get(factor, False) is True:
				return True
		return False

####################### Find Max Scores From Scores Matrix #######################

class Max_Matrix_Score():
	def __init__(self, matrix):
		self.matrix = matrix
		self.used_columns = {}

	def compute_score(self):
		row_score = self.compute_score_by_row(self.matrix)
		column_score = self.compute_score_by_column()

		max_score = row_score if row_score > column_score else column_score

		return max_score

	def compute_score_by_row(self, matrix, current_score=0, row_index=0):
		if row_index == len(matrix):
			return current_score

		max_score = current_score
		row = matrix[row_index]
		for column_index in range(0, len(row)):
			if self.used_columns.get(column_index, False) is False:
				cell_score = row[column_index]
				# ensure that used column is not reused lower on recursive stack
				self.used_columns[column_index] = True
				# add score from cell to current score on lower level.
				# increment row_index to investigate next row in recursive call
				score = self.compute_score_by_row(matrix, current_score + cell_score, row_index + 1)
				if score > max_score:
					# current max_score always saved in each function scope and ultimately returned
					max_score = score
				# not currently using this column, so make available again
				self.used_columns[column_index] = False
		return max_score

	def compute_score_by_column(self):
		# if there are more rows than columns, prior approach could exclude some high value fields
		# transposing matrix allows all combinations missed by other routine to be checked
		transposed_matrix = self.matrix.transpose()
		return self.compute_score_by_row(transposed_matrix)

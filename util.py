import re

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
			vowel_count = self.count_customer_vowels()
			base_score = vowel_count * 1.5
		else:
			consonant_count = self.count_customer_consonants()
			base_score = consonant_count

		customer_factors = self.find_factors_excluding_1(customer_name_letter_count)
		product_factors = self.find_factors_excluding_1(product_name_letter_count)

		if(self.has_customer_product_factors_match(customer_factors, product_factors)):
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
		self.used_rows = {}
		self.used_columns = {}

	def compute_score(self, current_score=0):
		max_score = current_score
		for row_index in range(0, len(self.matrix)):
			row = self.matrix[row_index]
			if self.used_rows.get(row_index, False) is False:
				for column_index in range(0, len(row)):
					if self.used_columns.get(column_index, False) is False:
						cell_score = row[column_index]
						self.used_rows[row_index] = True
						self.used_columns[column_index] = True
						score = self.compute_score(current_score + cell_score)
						if score > max_score:
							max_score = score
						self.used_rows[row_index] = False
						self.used_columns[column_index] = False

		return max_score

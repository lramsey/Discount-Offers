import unittest
import numpy as np

from algorithm import print_max_ss_scores, determine_max_ss_score, read_data_from_file, SS_Score, Max_Matrix_Score

class Print_Max_SS_Score_Test_Case(unittest.TestCase):
	def test_print_max_ss_scores(self):
		print "\nShould print 21.00, 83.50, and  71.25 in the console on separate lines"
		self.assertEqual(print_max_ss_scores("data.txt"), None)

class Determine_Max_SS_Score_Test_Case(unittest.TestCase):
	def test_determine_max_ss_score(self):
		case = [["Jack Abraham", "John Evans", "Ted Dziuba"], ["iPad 2 - 4-pack", "Girl Scouts Thin Mints", "Nerf Crossbow"]]
		self.assertEqual(determine_max_ss_score(case), 21.0)

class Read_Data_From_File_Test_Case(unittest.TestCase):
	def test_read_data_from_file(self):
		file_path = "data.txt"
		cases = read_data_from_file(file_path)
		self.assertEqual(type(cases), list)
		self.assertEqual(len(cases), 3)
		self.assertEqual(cases[0][0][1], "John Evans")


customer_name = "Robert"
even_letter_product_name = "big wheel"
odd_letter_product_name = "car"
even_ss_score = SS_Score(customer_name, even_letter_product_name)
odd_ss_score = SS_Score(customer_name, odd_letter_product_name)

class SS_Score_Test_Case(unittest.TestCase):
	def test_letter_count(self):
		self.assertEqual(even_ss_score.count_letters(even_letter_product_name), 8)
		self.assertEqual(odd_ss_score.count_letters(odd_letter_product_name), 3)
		self.assertEqual(even_ss_score.count_letters(customer_name), 6)

	def test_customer_vowel_count(self):
		self.assertEqual(even_ss_score.count_customer_vowels(), 2)

	def test_customer_consonant_count(self):
		self.assertEqual(odd_ss_score.count_customer_consonants(), 4)

	def test_find_factors(self):
		factors = even_ss_score.find_factors_excluding_1(9)
		self.assertEqual(factors.get(3, False), True)
		self.assertEqual(factors.get(2, False), False)

	def test_has_customer_product_factor_match(self):
		six_factors = even_ss_score.find_factors_excluding_1(6)
		
		five_factors = even_ss_score.find_factors_excluding_1(5)
		self.assertEqual(even_ss_score.has_customer_product_factors_match(six_factors, five_factors), False)
		three_factors = even_ss_score.find_factors_excluding_1(3)
		self.assertEqual(even_ss_score.has_customer_product_factors_match(six_factors, three_factors), True)

	def test_compute_score(self):
		self.assertEqual(even_ss_score.compute_score(), 4.5)
		self.assertEqual(odd_ss_score.compute_score(), 6)


class Max_Matrix_Test_Case(unittest.TestCase):
	def test_compute_score(self):
		matrix_1 = np.array([[1, 2], [1, 3],[4, 5]])
		max_matrix_score_1 = Max_Matrix_Score(matrix_1)
		self.assertEqual(max_matrix_score_1.compute_score(), 7)
		matrix_2 = np.array([[3, 5, 6], [4, 2, 7]])
		max_matrix_score_2 = Max_Matrix_Score(matrix_2)
		self.assertEqual(max_matrix_score_2.compute_score(), 12)

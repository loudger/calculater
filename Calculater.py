import math


class Calc:
	all_operations = {'all':['*', '/', '+', '-'], 'first_priority':['*', '/'], 'second_priority':['+', '-']}

	def __init__(self):
		pass

	# Принимает выражение
	def get_expression(self, expression):
		self.expression = expression

	# Реализуется одно из возможных операций
	def act(self, terms):
		if terms[1] == '+':
			return self.summation(terms[0], terms[2])
		elif terms[1] == '-':
			return self.subtraction(terms[0], terms[2])
		elif terms[1] == '*':
			return self.multiplication(terms[0], terms[2])
		elif terms[1] == '/':
			return self.division(terms[0], terms[2])


	# Реализация сложения
	def summation(self, f_val, s_val):
		return str(float(f_val) + float(s_val))

	# Реализация вычитания
	def subtraction(self, f_val, s_val):
		return str(float(f_val) - float(s_val))

	# Реализация умножения
	def multiplication(self, f_val, s_val):
		return str(float(f_val) * float(s_val))

	# Реализация деления
	def division(self, f_val, s_val):
		return str(float(f_val) / float(s_val))

	# Ищет операцию в выражении
	# Возвращает index, если есть
	def search_operation(self, expression, key = 'all'):
		deep = 0
		index = 0
		for el in expression:
			if el == '(':
				deep += 1
			elif el == ')':
				deep -= 1
			if el in self.all_operations[key] and deep == 0:
				return index
			index += 1
		return False

	# Проверка на лишние скобки
	def check_on_brace(self, expression):
		if expression[0] == '(' and expression[len(expression) - 1] == ')':
			return True
		else:
			return False

	# Удаляет внешние скобки.
	def delete_useless_brace(self, expression):
		expression = expression[1:len(expression) - 1]
		return expression

	# Обрабатывает строку для обработки
	# Удалять все пробелы в выражении и приводит всё в нижний регистр
	def right_view(self, expression):
		expression = expression.lower()
		expression = expression.replace(' ', '')
		return expression

	# Разделяет выражение на 3 части (левый операнд, операция, правый операнд)
	def partition(self, expression, index):
		terms = []
		terms.append(expression[0:index])
		terms.append(expression[index])
		terms.append(expression[index+1:len(expression)])
		return terms

	# terms == ['(23*2+1)', '+', '32']

	# Обработка и высчитывание выражения
	def treatment(self, expression):
		if self.search_operation(expression) != False:
			if self.search_operation(expression, 'second_priority') != False:
				index = self.search_operation(expression, 'second_priority')
				terms = self.partition(expression, index)
				terms[0] = self.treatment(terms[0])
				terms[2] = self.treatment(terms[2])
				result = self.act(terms)
				return result
			elif self.search_operation(expression, 'first_priority') != False:
				index = self.search_operation(expression, 'first_priority')
				terms = self.partition(expression, index)
				terms[0] = self.treatment(terms[0])
				terms[2] = self.treatment(terms[2])
				result = self.act(terms)
				return result
		if self.check_on_brace(expression):
			expression = self.delete_useless_brace(expression)
			expression = self.treatment(expression)
		return expression

	# Команда help
	def print_help(self):
		print('help, help() - общие сведения о программе\n'+
			'exit, exit() - выход из программы\n'+
			'Задача этой программы в вычислении различных выражений\n'+
			'Неверно записанные выражения вычисляться не будут\n'+
			'Количество пробелов и регистр не влияют на результат\n'+
			'Программа поддерживает данные операции '+ str(self.all_operations['all']) +'!\n'+
			'Пример: >>>(((2+2*3)+8.3/2)/3+1)*0.5')

	# Проверка введённого выражения
	def check_expression(self, expression):
		check_list = ['0','1','2','3','4','5','6','7','8','9','(',')']
		check_list.extend(self.all_operations['all'])
		deep = 0
		for el in expression:
			if el in check_list:
				if el == '(':
					deep += 1
				if el == ')':
					deep -= 1
				if deep < 0:
					print ('Ошибка записи, найдена неверная скобка')
					return False
			else:
				print('Ошибка записи, найден неверный символ')
				return False
		return True


# Доделать проверку выражения
# Сделать как подключаемый модуль




calculater = Calc()
print('Если что - "help"\n')
while True:
	command = input('>>>')
	command = calculater.right_view(command)
	if command in ['help', 'help()']:
		calculater.print_help()
	elif command in ['exit', 'exit()']:
		print ('Прекращение работы')
		break
	else:
		if calculater.check_expression(command):
			try:
				print('Ответ: {}'.format(calculater.treatment(command)))
			except:
				print('Ошибка записи, повторите попытку')













# 
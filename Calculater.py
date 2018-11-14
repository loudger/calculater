# PEP 8
# PEP 257

import math

class Calc:
	all_operations = {'all':['*', '/', '+', '-', '^', 'l', 's', 'c'], 'zero_priority':['l', 's', 'c'], 'first_priority':['*', '/', '^'], 'second_priority':['+', '-']}
	# Словарь, который заключает в себе все операции
	# нулевой приоритет - это операции типа "O(x,x)", где О - операция, x - аргумент
	# первый и второй приоритет - это операция типа "(x)O(x)"

	def __init__(self):
		pass

	def act(self, terms):
		"""
		Реализуется одно из возможных операций
		Принимает terms = ['аргумент','операция', 'аргумент']
		"""
		if terms[1] == '+':
			return self.summation(terms[0], terms[2])
		elif terms[1] == '-':
			return self.subtraction(terms[0], terms[2])
		elif terms[1] == '*':
			return self.multiplication(terms[0], terms[2])
		elif terms[1] == '/':
			return self.division(terms[0], terms[2])
		elif terms[1] == '^':
			return self.pow(terms[0], terms[2])
		elif terms[1] == 'l':
			return self.logarithmization(terms[0], terms[2])
		elif terms[1] == 's':
			return self.sin(terms[0])
		elif terms[1] == 'c':
			return self.cos(terms[0])

	def summation(self, f_val, s_val):
		"""
		Реализация сложения
		Так как f_val и s_val - объекты типа str, то вычисления их сначала нужно привести
		к типу float, а после выполнения, вернуть обратно объект типа str
		С остальными операциями аналогично
		"""
		return str(float(f_val) + float(s_val))

	def subtraction(self, f_val, s_val):
		"""
		Реализация вычитания
		"""
		return str(float(f_val) - float(s_val))

	def multiplication(self, f_val, s_val):
		"""
		Реализация умножения
		"""
		return str(float(f_val) * float(s_val))

	def division(self, f_val, s_val):
		"""
		Реализация деления
		"""
		return str(float(f_val) / float(s_val))

	def pow(self, f_val, s_val):
		"""
		Реализация степени
		"""
		return str(math.pow(float(f_val),float(s_val)))

	def logarithmization(self, f_val, s_val):
		"""
		Реализация логарифма
		"""
		try:
			return str(math.log(float(f_val), float(s_val)))
		except:
			print('Ошибка записи, неверные аргументы у логарифма')

	def sin(self, f_val):
		"""
		Реализация sin
		"""
		try:
			return str(math.sin(float(f_val)))
		except:
			print('Ошибка записи, неверный аргумент у синуса')

	def cos(self, f_val):
		"""
		Реализация cos
		"""
		try:
			return str(math.cos(float(f_val)))
		except:
			print('Ошибка записи, неверный аргумент у косинуса')

	def search_operation(self, expression, key = 'all'):
		"""
		Ищет операция в выражении, возвращает index, если есть.
		Здесь идея в том, что параметр deep определяет "глубину" в каждом месте строки:
		Например: 5+4*(3*(1+1+1)+2)
				  00001112222222111
		Метод ищет операции только там, где глубина равна нулю

		Осторожно костыль: Индекс сначала имеет значение 0
		И если операция находится в начале строки, то метод вернёт index = 0,
		Далее в другом методе у меня проверка на (False == index), но в python (False == 0) -> True
		Поэтому если операция встречается в самом начале строки, то я возвращаю не index, а True
		"""
		deep = 0
		index = 0
		for el in expression:
			if el == '(':
				deep += 1
			elif el == ')':
				deep -= 1
			if el in self.all_operations[key] and deep == 0:
				if index == 0:
					return True
				else:
					return index
			index += 1
		return False

	def check_on_brace(self, expression):
		"""
		Проверка на скобки на бокам строки "(....)"
		"""
		if expression[0] == '(' and expression[len(expression) - 1] == ')':
			return True
		else:
			return False

	def delete_useless_brace(self, expression):
		"""
		Удаляет внешние скобки
		"(5+5)" -> "5+5"
		"""
		expression = expression[1:len(expression) - 1]
		return expression

	def right_view(self, expression):
		"""
		Обрабатывает строку для обработки
		Удалять все пробелы в выражении и приводит всё в нижний регистр
		Заменяет длинные названия операция на один характерный символ
		"""
		expression = expression.lower()
		expression = expression.replace(' ', '')
		expression = expression.replace('sin','s')
		expression = expression.replace('cos','c')
		expression = expression.replace('log','l')
		expression = expression.replace('**','^')
		return expression

	def partition(self, expression, index, only_right = False):
		"""
		Разделяет выражение на 3 части (левый операнд, операция, правый операнд)
		параметр only_right отвечает за вид обработки
		если only_right = False, то метод обрабатывает выражение "(x)О(x)", где О - операция, а x - аргументы
		если only_right = True, то обрабатывает выражение "O(x, x)"

		Пример результата: terms == ['(23*2+1)', '+', '32']
		"""
		if only_right:
			terms = []
			if ',' in expression:
				terms.append(expression[2:expression.index(',')])
				terms.append(expression[0])
				terms.append(expression[expression.index(',')+1:len(expression)-1])
			else:
				terms.append(expression[2:len(expression)-1])
				terms.append(expression[0])
				terms.append('0')
			return terms
		else:
			terms = []
			terms.append(expression[0:index])
			terms.append(expression[index])
			terms.append(expression[index+1:len(expression)])
			return terms

	def treatment(self, expression):
		"""
		Обработка и высчитывание выражения
		"""
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
			elif self.search_operation(expression, 'zero_priority') != False:
				terms = self.partition(expression, index = 0, only_right = True)
				terms[0] = self.treatment(terms[0])
				terms[2] = self.treatment(terms[2])
				result = self.act(terms)
				return result
		if self.check_on_brace(expression):
			expression = self.delete_useless_brace(expression)
			expression = self.treatment(expression)
		try:
			float(expression)
			return expression
		except:
			pass

	def print_help(self):
		"""
		Команда help
		"""
		print('help, help() - общие сведения о программе\n'+
			'exit, exit() - выход из программы\n'+
			'Задача этой программы в вычислении различных выражений\n'+
			'Неверно записанные выражения вычисляться не будут\n'+
			'Количество пробелов и регистр не влияют на результат\n'+
			'Программа поддерживает данные операции '+ str(self.all_operations['all']) +'!\n'+
			'Где l - log(), ^ - степень (или **), s - sin(), c - cos()\n'+
			'Пример: >>>(log((23+1+4)/10, 3)*cos(3.1/2))^(2)+3')

	def check_expression(self, expression):
		"""
		Проверка введённого выражения:
			1.Проверка на наличие лишних символов
			2.Проверка на правильность скобок
		"""
		check_list = ['0','1','2','3','4','5','6','7','8','9','(',')',',','.']
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
		if deep != 0:
			print ('Ошибка записи, найдена неверная скобка')
			return False
		return True


# Доделать проверку выражения
"""
Следующая строчка позволяет подключать это приложение как отдельный модуль.
Если запустить приложение, то __name__=__main__
если заупстить как модуль, то __name__=__Calculater__
"""
if __name__ == '__main__':
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
					result = calculater.treatment(command)
					if result is None:
						pass
					else:
						print('Ответ: {}'.format(result))
				except:
					print('Ошибка записи, повторите попытку')


import numpy as np
from typing import List, Union

class Table:
	"""
	Convert a set of data to a LaTeX-readable string that can be pasted into the source code of a LaTeX document.
	
	Attributes
	----------
	data : Union[List[List[int]], np.ndarray[float][int]]
		Contains the table entries in a nested list.
	rowlabels : List[str], default=None
		Contains names of the table rows.
	collabels : List[str], default=None
		Contains names of the table columns.
	caption : str, default=None
		The caption displayed above the table in LaTeX.
	label : str, default=None
		The label used for cross-referencing the table environment in LaTeX.
	precision : Union[int, List[int]], default=None
		The amount of decimal characters of the table entries. Numbers with greater precision are rounded and numbers with less precision are filled with ending zeros. 'None' keeps the amount of decimals as in the original nested list.
	booktabs : bool, default=True
		Whether the booktabs package is used in LaTeX. If True, top-, mid- and bottomrules are used instead of hlines.
	decimal : str, default='{,}'
		The decimal separator to be used for all numbers.
	position : str, default='htbp'
		Position of the table on the LaTeX page.
	table : str, default=''
		The generated LaTeX-readable string that can be pasted into the source code of a LaTeX document.
	
	Methods
	-------
	set_rowlabels : Set the names of the table rows.
	set_collabels : Set the names of the table columns.
	set_caption : Set the caption displayed above the table in LaTeX.
	set_label : Set the label used for cross-referencing the table environment in LaTeX.
	set_precision : Configure the amount of decimal characters of the table entries.
	set_decimal : Configure the decimal separator.
	set_booktabs : Configure whether the booktabs package is used in LaTeX.
	set_position : Set the position of the table.
	transpose : Change rows and columns of the table.
	generate : Generate the table.
	save : Save the table as a file.
	print : Print the table to the standard output.

	Examples
	--------
	>>> import tablenator as tn
	>>> x = tn.Table([[1,9],[3,4]])
	>>> x.set_collabels(['a', 'b'])
	>>> x.set_rowlabels(['erste Zeile', 'zweite Zeile'])
	>>> x.set_precision(2)
	>>> x.set_label('example')
	>>> x.generate()
	>>> x.print()
	\\begin{table}[htbp] ... \\end{table}

	>>> import tablenator as tn
	>>> x = tn.Table(np.array(((1,9.3),(3.01,4.83))))
	>>> x.set_caption('Example table.')
	>>> x.transpose()
	>>> x.set_precision([1,2])
	>>> x.generate()
	>>> x.save('test.tex')
	"""
	def __init__(self, data: Union[List[List[float]], np.ndarray[float]]):
		'''Initialize an instance of a table.

		Parameters
		----------
		data : Union[List[List[float]], np.ndarray[float]]
			The input data to be set. Can be either a list of lists or a 2-dimensional numpy array.

		Raises
		------
		TypeError: If the input data is not of type List[List[float]] or np.ndarray[float]

		Examples
		--------
		>>> t = Table([[1,2],[3,4]])

		>>> t = Table(np.array((('a', 'b'), ('c', 'd'))))
		'''
		self.data = None
		self.rowlabels = None
		self.collabels = None
		self.caption = None
		self.label = None
		self.precision = None
		self.booktabs = True
		self.decimal = '{,}'
		self.position = 'htbp'
		self.table = ''

		self._set_data(data)

	def _set_data(self, data: Union[List[List[float]], np.ndarray[float]]):
		'''Set the data for the table.

		Parameters
		----------
		data : Union[List[List[float]], np.ndarray[float]]
			The input data to be set. Can be either a list of lists or a 2-dimensional numpy array.

		Raises
		------
		TypeError : If input is not of type List[List[float]] or np.ndarray[float]
		ValueError : If input is not 2-dimensional
		'''
		# First case: type(data) = List[List[float]]
		if isinstance(data, list):
			for row in data:
				if isinstance(row, list):
					if all(isinstance(val, float) or isinstance(val, int) for val in row):
						continue
					else:
						raise TypeError("'data' must only contain floats")
				else:
					raise TypeError("'data' must be a list of lists")
			self.data = data
	
		# Second case: type(data) = np.array
		elif isinstance(data, np.ndarray):
			# Remove axes of length one from labels
			data = np.squeeze(data)
			# Iterate over all entries; use .item() to convert 0-dimensional arrays to numbers
			if all(isinstance(val.item(), float) or isinstance(val.item(), int) for val in np.nditer(data)):
				# Check if data is two-dimensional
				if data.ndim == 2:
					# Convert to list
					data = data.tolist()
					self.data = data
				else:
					raise ValueError(
						f"Data dimension mismatch. Expected 2, but got {data.ndim}."
						)
			else:
				raise TypeError("'data' must only contain floats")
		
		# Third case: Wrong type
		else:		
			raise TypeError("'data' must be a list of lists")
		
	def set_rowlabels(self, labels: List[str]):
		'''Set the names of the table rows.
		
		Parameters
		----------
		labels : List[str]
			Names of the table rows. Number of labels in the list must match number of rows in data.
		
		Raises
		------
		TypeError : If input is not of type List[str].
		ValueError : If number of row labels does not match number of rows in data
		'''
		# Check if labels is of type list
		if isinstance(labels, list):
			# Check that labels only contains str
			if all(isinstance(label, str) for label in labels):
				# Check if number of row labels matches number of rows in data
				if len(labels) == len(self.data):
					self.rowlabels = labels
				else:
					raise ValueError(
						f"Number of row labels does not match number of rows in data. Expected {len(self.data)}, but got {len(labels)}."
						)
			else:
				raise TypeError("'rowlabels' may only contain strings")
		else:		
			raise TypeError("'rowlabels' must be a list")

	def set_collabels(self, labels: List[str]):
		'''Set the names of the table columns.
		
		Parameters
		----------
		labels : List[str]
			Names of the table rows. Number of labels in the list must match number of columns in data.
		
		Raises
		------
		TypeError : If input is not of type List[str]
		ValueError : If number of column labels does not match number of columns in data
		'''
		# Check if labels is of type list
		if isinstance(labels, list):
			# Check that labels only contains str
			if all(isinstance(label, str) for label in labels):
				# Check if number of row labels matches number of rows in data
				if len(labels) == len(self.data[0]):
					self.collabels = labels
				else:
					raise ValueError(
						f"Number of column labels does not match number of columns in data. Expected {len(self.data[0])}, but got {len(labels)}."
						)
			else:
				raise TypeError("'collabels' may only contain strings")
		else:		
			raise TypeError("'collabels' must be a list")
	
	def set_caption(self, caption: str):
		'''Set the caption displayed above the table in LaTeX.
		
		Parameters
		----------
		caption : str
			Name of the caption.
		
		Raises
		------
		TypeError : If input is not of type str.
		'''
		# Check if caption is a string
		if isinstance(caption, str):
			self.caption = caption
		else:
			raise TypeError("'caption' must be a string")

	def set_label(self, label: str):
		'''Set the label used for cross-referencing the table environment in LaTeX.
		
		Prefix 'tab:' is added automatically.
		
		Parameters
		----------
		label : str
			Name of the label.
		
		Raises
		------
		TypeError : If input is not of type str.
		'''
		# Check if label is a string
		if isinstance(label, str):
			self.label = label
		else:
			raise TypeError("'label' must be a string")
	
	def set_precision(self, precision: Union[int, List[int]]):
		'''Configure the amount of decimal characters of the table entries.

		Spezifies the decimal place to which rounding is performed.
		By default, the precision is as in the original data.
		A negative precision results in rounding the number to digits before the decimal point.
		If input is an integer, all values are rounded to the same precision.
		If input is a list of integers, values are rounded per column.

		Parameters
		----------
		precision : Union[int, List[int]]
			Spezifies the decimal place to which rounding is performed.

		Raises
		------
		TypeError : If input is not of type int or List[int]
		ValueError : If number of column labels does not match number of columns in data
		'''
		# Check if precision is an integer
		if isinstance(precision, int):
			self.precision = precision
			for i, row in enumerate(self.data):
				self.data[i]=["%.*f" % (self.precision,round(x,self.precision)) for x in row]
		elif isinstance(precision, list) and all(isinstance(prec, int) for prec in precision):
			if not len(precision) == len(self.data):
				raise ValueError(
					f"Number of entries in 'precision' does not match number of columns in data. Expected {len(self.data)}, but got {len(precision)}."
					)
			self.precision = precision
			for i, row in enumerate(self.data):
				self.data[i]=["%.*f" % (self.precision[i],round(x,self.precision[i])) for x in row]
		else:
			raise TypeError(f"'precision' must be an integer or a list of integers")

	def set_decimal(self, sep: str):
		'''Configure the decimal separator.
		
		Parameters
		----------
		sep : str
			The decimal separator

		Raises
		------
		TypeError : If input is not of type str
		'''
		# Check if decimal is a string
		if isinstance(sep, str):
			self.decimal = sep
		else:
			raise TypeError("'sep' must be a string")

	def set_booktabs(self, state: bool):
		'''Configure whether the booktabs package is used in LaTeX.
		
		If True, top-, mid- and bottomrules are used instead of hlines.

		Parameters
		----------
		state : bool
			Use of booktabs package.

		Raises
		------
		TypeError : If input is not of type bool
		'''
		if not isinstance(state, bool):
			raise TypeError("'value' must be a bool")
		self.booktabs = state
	
	def set_position(self, pos):
		'''Set the position of the table.
		
		Parameters
		----------
		pos : str
			Position of the table
		
		Raises
		------
		TypeError : If input is not of type str.
		'''
		if isinstance(pos, str):
			self.position = pos
		else:
			raise TypeError("'pos' must be a str")

	def transpose(self, change_labels: bool=True):
		'''Change rows and columns of the table.
		
		Parameters
		----------
		change_labels : bool, default=True
			Whether to include 'rowlabels' and 'collabels' in the transposition.

		Raises
		------
		TypeError : If input is not of type bool
		'''
		if isinstance(change_labels, bool):
			if change_labels:
				self.rowlabels, self.collabels = self.collabels, self.rowlabels
		else:
			raise TypeError("'change_labels' must be a bool")
		
		self.data = [list(x) for x in zip(*self.data)]

	def _toprule(self):
		'''Adds the toprule to the table'''
		if self.booktabs:
			self.table += "\t\\toprule\n\t"
		else:
			self.table += "\t\\hline\n\t"

	def _midrule(self):
		'''Adds the midrule to the table'''
		if self.booktabs:
			self.table += "\t\\midrule\n\t"
		else:
			self.table += "\t\\hline\n\t"

	def _bottomrule(self):
		'''Adds the bottomrule to the table'''
		if self.booktabs:
			self.table += "\\bottomrule\n\t"
		else:
			self.table += "\\hline\n\t"

	def generate(self):
		'''Generate the table.'''
		# Begin table environment
		self.table = "\\begin{table}" + f"[{self.position}]\n"
		# Center table within table environment
		self.table += "\t\\centering\n"
		# Add caption if necessary
		if self.caption != None:
			self.table += "\t\\caption{" + self.caption + "}\n"
		# Begin LaTeX table
		self.table += "\t\\begin{tabular}{"
		# Add column for row labels (if any)
		if self.rowlabels:
			self.table += "l|"
			if self.collabels:
				self.collabels.insert(0,'')
		# Add column specification for data columns
		self.table += "c" * len(self.data[0]) + "}\n"
		# Add horizontal line above top row
		self._toprule()
		# Add column labels (if any)
		if self.collabels:
			self.table += " & ".join(self.collabels) + " \\\\\n"
			# Add horizontal line below column labels
			self._midrule()
		# Add rows with data and row labels (if any)
		for i, row in enumerate(self.data):
			# Add row labels (if any)
			if self.rowlabels:
				self.table += self.rowlabels[i] + " & "
			row=[str(x) for x in row]
			# Replace dots with decimal separator and add rows with data
			self.table += " & ".join(x.replace('.',self.decimal) for x in row) + " \\\\\n\t"
		# Add horizontal line below bottom row
		self._bottomrule()
		# End LaTeX table
		self.table += "\\end{tabular}\n"
		# Add label if necessary
		if self.label != None:
			self.table += "\t\\label{tab:" + self.label + "}\n"
		# End table environment
		self.table += "\\end{table}"

	def save(self, path: str):
		'''Save the table as a file.
		
		Parameters
		----------
		path : str
			Set location and file name.
		
		Raises
		------
		TypeError : If input is not of type str
		'''
		if isinstance(path, str):
			with open(path, 'w') as f:
				f.write(self.table)
		else:
			raise TypeError("'path' must be a str")

	def print(self):
		'''Print the table to the standard output.'''
		print(self.table)

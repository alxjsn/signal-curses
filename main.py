import npyscreen

class MainForm(npyscreen.Popup):
	def create(self):
		self.to = self.add(npyscreen.TitleSelectOne, max_height=3,
			name='To:',
			values=['Bob Smith', 'John Doe', 'Jane Doe', 'Todd Smith'],
			scroll_exit=True)
		self.msg = self.add(npyscreen.TitleText, name='Message:')

	def afterEditing(self):
		print('after editing', self.to.value, self.msg.value)
		self.parentApp.setNextForm('DONE')

class MessagesLine(npyscreen.MultiLine):
	_size = 15
	_size_max = 30
	_real_values = []
	def __init__(self, *args, **kwargs):
		#kwargs['columns'] = 6
		#kwargs['column_width'] = 20
		super(MessagesLine, self).__init__(*args, **kwargs)

	def update(self, *args, **kwargs):
		if self._real_values:
			self._gen_size()
			self._gen_values()
		super(MessagesLine, self).update(*args, **kwargs)

	def _gen_size(self):
		self._size = min(max([len(i[0]) for i in self._real_values]), self._size_max)

	def display_value(self, val):
		return val

	def _gen_line_max(self, val, size_max):
		if len(val) < size_max:
			return val
		c = '…'
		return val[:size_max-len(c)]+c

	def _gen_lines(self, val):
		return self._gen_lines_full(val, self._size, self._size_max)

	def _gen_lines_full(self, val, size, size_max):
		beg_fmt = '{:>'+str(size)+'} | '
		first_beg = beg_fmt.format(self._gen_line_max(val[0], size_max))
		cont_beg = beg_fmt.format('')
		ret = []
		text = val[1]
		
		ret.append(first_beg + str(text[:self.width]))
		text = text[self.width:]
		while len(text) > 0:
			ret.append(cont_beg + str(text[:self.width]))
			text = text[self.width:]
		return ret

	def _gen_values(self):
		self.values = []
		for v in self._real_values:
			[self.values.append(i) for i in self._gen_lines(v)]

	def addValues(self, values):
		self._real_values += values
		self.update()


class AppForm(npyscreen.FormMuttActiveTraditionalWithMenus):
	COMMAND_WIDGET_CLASS = npyscreen.TitleText
	COMMAND_WIDGET_NAME = 'Send: '
	COMMAND_WIDGET_BEGIN_ENTRY_AT = 1
	MAIN_WIDGET_CLASS = MessagesLine

	def create(self):
		self.m1 = self.add_menu(name="Main Menu", shortcut="^X")
		self.m1.addItemsFromList([
			("Add Lines", self.whenAddLines, None, None, ("blah",)),
			("Switch", self.whenSwitch, None, None, ("blah",)),
			("Exit", self.whenExit, "e"),
		])

		super(AppForm, self).create()


	def whenAddLines(self, arg):
		self.wMain.addValues([
		('John Doe', 'text '*10),
		('Bob Smith', 'text '*50),])

	def whenSwitch(self, arg):
		self._updateTitle('John Smith')

	def whenExit(self):
		self.parentApp.setNextForm(None)
		self.editing = False
		self.parentApp.switchFormNow()

	def beforeEditing(self):
		self.wMain.always_show_cursor = False
		self.wMain.addValues([
			('John Smith', 'great weather huh? how are you doing'),
			('Jane', 'foobarfoobar asdf asdf asdf asdf asdf asdf asdf '),
			('Almosttoolong butnottoolong a', 'test foo'),
			('Longlonglong Tootoolonglonglong', 'test blah'),
			('John Smith', 'too long '*30),
			('After', 'after text')])
		self.wMain.display()

		self._updateTitle('Andrew Wang')

	def _updateTitle(self, name):
		self.wStatus1.value = 'Signal: {} '.format(name)
		self.wStatus2.value = '{} '.format(name)
		self.wStatus1.display()
		self.wStatus2.display()

class SignalApp(npyscreen.NPSAppManaged):
	def onStart(self):
		#self.addForm('MAIN', MainForm, name='Enter Message')
		self.addForm('MAIN', AppForm, name='Application')


if __name__ == '__main__':
	signal = SignalApp()
	signal.run()

	#print(npyscreen.wrapper_basic(formFunc))
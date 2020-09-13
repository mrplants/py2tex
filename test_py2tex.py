import unittest, re
import py2tex

class Test_Pattern(unittest.TestCase):

  @staticmethod
  def get_matches(pytex):
    matches = re.search(py2tex.PYTEX_PATTERN, pytex)
    return matches.groups() if matches is not None else []

  def compare_string_list(self, strlist1, strlist2):
    """ Compares respective strings in two lists.
    """
    for str1, str2 in zip(strlist1, strlist2):
      self.assertMultiLineEqual(str1, str2)

  def test_empty_input(self):
    """ Verify pytex pattern works with empty input.
    """
    filestring = ''
    executables = self.get_matches(filestring)
    self.assertEqual(len(executables), 0)

  def test_no_executables(self):
    """ Verify get_executable_strings() works with only non-executable input.
    """
    filestring = 'this is some test LaTeX input.'
    executables = self.get_matches(filestring)
    self.assertEqual(len(executables), 0)
    filestring = 'this is some test LaTeX input.\nThis time, multiline!'
    executables = self.get_matches(filestring)
    self.assertEqual(len(executables), 0)

  def test_only_single_executable(self):
    """ Verify get_executable_strings() works with executable input (single).
    """
    executables = self.get_matches('🐍🐍')
    self.compare_string_list(executables, [''])

  def test_repeated_executable(self):
    """ Verify get_executable_strings() works with executable input (multiple).
    """
    executables = self.get_matches('🐍🐍🐍🐍🐍🐍')
    self.compare_string_list(executables, ['','',''])
    executables = self.get_matches('🐍some python code🐍')
    self.compare_string_list(executables, ['some python code'])
    executables = self.get_matches('🐍some python code🐍🐍more python code🐍')
    self.compare_string_list(executables, ['some python code','more python code'])

  def test_start_with_executable(self):
    """ Verify get_executable_strings() works when starting with an executable.
    """
    executables = self.get_matches('🐍🐍 and some LaTeX')
    self.compare_string_list(executables, [''])
    executables = self.get_matches('🐍some python🐍 and some LaTeX')
    self.compare_string_list(executables, ['some python'])
    executables = self.get_matches('🐍some python🐍 and some LaTeX 🐍and more python🐍 and more LaTeX')
    self.compare_string_list(executables, ['some python','and more python'])

  def test_end_with_executable(self):
    """ Verify get_executable_strings() works when ending with an executable.
    """
    executables = self.get_matches('Some LaTeX 🐍🐍')
    self.compare_string_list(executables, [''])
    executables = self.get_matches('Some LaTeX 🐍and some python🐍')
    self.compare_string_list(executables, ['and some python'])
    executables = self.get_matches('Some LaTeX 🐍and some python🐍 and some LaTeX 🐍and more python🐍')
    self.compare_string_list(executables, ['and some python','and more python'])

class Test_Run_Executable(unittest.TestCase):
  def test_collect_print_statements(self):
    """ Verify that print statements are collected.
    """
    self.assertMultiLineEqual('printed\n',
                              py2tex.collect_stdout_from_executable('print("printed")'))
    self.assertMultiLineEqual('printed\nprinted again\n',
                              py2tex.collect_stdout_from_executable('print("printed")\nprint("printed again")'))

  def test_import_between_execs(self):
    """ Verify that imported packages are available between calls to exec.
    """
    local_scope = global_scope = {}
    py2tex.collect_stdout_from_executable('import sys', local_scope, global_scope)
    out = py2tex.collect_stdout_from_executable('sys.stdout.write("sys still exists")', local_scope, global_scope)
    self.assertMultiLineEqual(out, "sys still exists")
  
  def test_exception_passed_through(self):
    """ Verify that exceptions are passed through.
    """
    self.assertRaises(Exception, py2tex.collect_stdout_from_executable, 'raise Exception')

class Test_Pytex_Conversion(unittest.TestCase):
  def test_empty_input(self):
    """ Verify conversion works with empty input.
    """
    self.assertMultiLineEqual('', py2tex.pytex_to_tex(''))

  def test_no_executables(self):
    """ Verify conversion works with only non-executable input.
    """
    self.assertMultiLineEqual('this is some test LaTeX input.',
                              py2tex.pytex_to_tex('this is some test LaTeX input.'))
    self.assertMultiLineEqual('this is some test LaTeX input.\nThis time, multiline!',
                              py2tex.pytex_to_tex('this is some test LaTeX input.\nThis time, multiline!'))

  def test_only_single_executable(self):
    """ Verify conversion works with executable input (single).
    """
    self.assertMultiLineEqual('', py2tex.pytex_to_tex('🐍🐍'))

  def test_repeated_executable(self):
    """ Verify conversion works with executable input (multiple).
    """
    self.assertMultiLineEqual('', py2tex.pytex_to_tex('🐍🐍🐍🐍🐍🐍'))
    self.assertMultiLineEqual('test\n',
                              py2tex.pytex_to_tex('🐍print("test")🐍'))
    self.assertMultiLineEqual('test\ntest again\n',
                              py2tex.pytex_to_tex('🐍print("test")🐍🐍print("test again")🐍'))
    self.assertMultiLineEqual('sys still exists',
                              py2tex.pytex_to_tex('🐍import sys🐍🐍sys.stdout.write("sys still exists")🐍'))

  def test_start_with_executable(self):
    """ Verify conversion works when starting with an executable.
    """
    self.assertMultiLineEqual(' and some LaTeX',
                              py2tex.pytex_to_tex('🐍🐍 and some LaTeX'))
    self.assertMultiLineEqual('test\n and some LaTeX',
                              py2tex.pytex_to_tex('🐍print("test")🐍 and some LaTeX'))
    self.assertMultiLineEqual('some python\n and some LaTeX and more python\n and more LaTeX',
                              py2tex.pytex_to_tex('🐍print("some python")🐍 and some LaTeX 🐍print("and more python")🐍 and more LaTeX'))

  def test_end_with_executable(self):
    """ Verify conversion works when ending with an executable.
    """
    self.assertMultiLineEqual('and some LaTeX ',
                              py2tex.pytex_to_tex('and some LaTeX 🐍🐍'))
    self.assertMultiLineEqual('Some LaTeX test\n',
                              py2tex.pytex_to_tex('Some LaTeX 🐍print("test")🐍'))
    self.assertMultiLineEqual('Some LaTeX and more python\n and more LaTeX some other python\n',
                              py2tex.pytex_to_tex('Some LaTeX 🐍print("and more python")🐍 and more LaTeX 🐍print("some other python")🐍'))
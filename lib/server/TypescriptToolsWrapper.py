# coding=utf8

import sublime
import json

from ..display.Message import MESSAGE
from ..display.T3SViews import T3SVIEWS

from .AsyncCommand import AsyncCommand

from ..utils import make_hash, Debug, max_calls
from ..utils.fileutils import is_dts, fn2l
from ..utils.viewutils import get_file_infos
from ..utils.CancelCommand import CancelCommand


# --------------------------- TypescriptToolsWrapper ------------------------------------ #

class TypescriptToolsWrapper(object):
	""" This Class translates the available commands to the corresponding string
		command for the typescript-tools from clausreinke   """


	def __init__(self, project):
		self.project = project
		self.added_files = {} # added_files[filename] = hash
		self.executed_with_most_recent_file_contents = []
		self.is_killed = False


	# RELOAD PROCESS
	@max_calls()
	def reload(self, filename_or_root, callback=None):
		AsyncCommand('reload', get_root(filename_or_root)) \
			.set_id('reload') \
			.set_result_callback(lambda r: callback is None or callback()) \
			.append_to_both_queues()
		self.project.errors.start_recalculation()


	# GET INDEXED FILES
	@max_calls()
	def get_tss_indexed_files(self, filename, callback):
		AsyncCommand('files', get_root(filename)) \
			.do_json_decode_tss_answer() \
			.set_result_callback(callback) \
			.append_to_fast_queue()

	# DUMP FILE (untested)
	@max_calls()
	def dump(self, filename, output, callback):
		dump_command = 'dump {0} {1}'.format( output, fn2l(filename) )
		AsyncCommand(dump_command, get_root(filename)) \
			.set_result_callback(callback) \
			.append_to_fast_queue()

	# TYPE
	@max_calls()
	def type(self, filename, line, col, callback):
		""" callback({ tss type answer }, filename=, line=, col=) """

		type_command = 'type {0} {1} {2}'.format( str(line+1), str(col+1), fn2l(filename) )

		AsyncCommand(type_command, get_root(filename)) \
			.set_id("type_command") \
			.set_callback_kwargs(filename=filename, line=line, col=col) \
			.do_json_decode_tss_answer() \
			.set_result_callback(callback) \
			.append_to_fast_queue()


	# DEFINITION
	@max_calls()
	def definition(self, filename, line, col, callback):
		""" callback({ tss type answer }, filename=, line=, col=) """

		definition_command = 'definition {0} {1} {2}'.format( str(line+1), str(col+1), fn2l(filename) )

		AsyncCommand(definition_command, get_root(filename)) \
			.set_id("definition_command") \
			.set_callback_kwargs(filename=filename, line=line, col=col) \
			.do_json_decode_tss_answer() \
			.set_result_callback(callback) \
			.append_to_fast_queue()


	# REFERENCES
	@max_calls()
	def references(self, filename, line, col, callback):
		""" callback({ tss type answer }, filename=, line=, col=) """

		references_command = 'references {0} {1} {2}'.format( str(line+1), str(col+1), fn2l(filename) )

		AsyncCommand(references_command, get_root(filename)) \
			.set_id("references_command") \
			.set_callback_kwargs(filename=filename, line=line, col=col) \
			.do_json_decode_tss_answer() \
			.set_result_callback(callback) \
			.append_to_fast_queue()

	# STRUCTURE
	@max_calls()
	def structure(self, filename, sender_view_id, callback):
		""" callback({ tss type answer }, filename=, sender_view_id=) """

		structure_command = 'structure {0}'.format(fn2l(filename))

		AsyncCommand(structure_command, get_root(filename)) \
			.set_id("structure_command for view %i" % sender_view_id) \
			.set_callback_kwargs(filename=filename, sender_view_id=sender_view_id) \
			.do_json_decode_tss_answer() \
			.set_result_callback(callback) \
			.append_to_fast_queue()


	# ASK FOR COMPLETIONS
	@max_calls()
	def complete(self, filename, line, col, is_member_str, callback):
		""" callback("tss type answer as string") """

		completions_command = 'completions {0} {1} {2} {3}'.format(is_member_str, str(line+1), str(col+1), fn2l(filename))

		Debug('autocomplete', "Send async completion command for line %i , %i" % (line+1, col+1))

		AsyncCommand(completions_command, self.project) \
			.set_id("completions_command") \
			.procrastinate() \
			.set_result_callback(callback) \
			.set_callback_kwargs(filename=filename, line=line, col=col, is_member_str=is_member_str) \
			.append_to_fast_queue()


	# UPDATE FILE
	@max_calls()
	def update(self, view):
		""" updates the view.buffer's content to the buffer in tss.js """

		# only update if the file contents have changed since last update call on this file
		filename, lines, content = get_file_infos(view)
		if self.need_update(filename, content):
			update_command = 'update nocheck {0} {1}\n{2}'.format(str(lines+1), fn2l(filename), content)

			AsyncCommand(update_command, self.project) \
				.set_id('update %s' % filename) \
				.append_to_both_queues()

			self.on_file_contents_have_changed()


	# ADD FILE
	@max_calls()
	def add(self, root, filename, lines, content):

		update_command = 'update nocheck {0} {1}\n{2}'.format(str(lines+1), fn2l(filename), content)

		AsyncCommand(update_command, root) \
			.set_id('add %s' % filename) \
			.append_to_both_queues()

		self.need_update(filename, content) # save current state
		self.on_file_contents_have_changed()


	@max_calls()
	def need_update(self, filename, unsaved_content):
		""" Returns True if <unsaved_content> has changed since last call to need_update(). """
		newhash = make_hash(unsaved_content)
		oldhash = self.added_files[filename] if filename in self.added_files else "nohash"
		if newhash == oldhash:
			Debug('tss+', "NO UPDATE needed for file : %s" % filename)
			return False
		else:
			Debug('tss+', "UPDATE needed for file %s : %s" % (newhash, filename) )
			self.added_files[filename] = newhash
			return True


	def on_file_contents_have_changed(self):
		"""
			Every command that wants to only be executed when file changes have been made
			can use self.executed_with_most_recent_file_contents to remember a previous execution.
			After any change, this array will be cleared
		"""
		self.executed_with_most_recent_file_contents = []

	def files_changed_after_last_call(self, cmd_hint):
		"""
			Returns True if there have been any file changes after last call
			to this function.
		"""
		if cmd_hint in self.executed_with_most_recent_file_contents:
			return False
		self.executed_with_most_recent_file_contents.append(cmd_hint)
		return True


	# ERRORS
	@max_calls()
	def errors(self, callback=None):
		""" callback format: callback(result) """

		# TODO: this may prevent initial error display or if user triggers manually
		if not self.files_changed_after_last_call('errors'):
			return

		T3SVIEWS.ERROR.on_calculation_initiated()

		AsyncCommand('showErrors', self.project) \
			.set_id('showErrors') \
			.procrastinate() \
			.activate_debounce() \
			.set_result_callback(lambda errors: [callback(errors), T3SVIEWS.ERROR.on_calculation_finished()] ) \
			.set_executing_callback(lambda: T3SVIEWS.ERROR.on_calculation_executing()) \
			.set_replaced_callback(lambda by: T3SVIEWS.ERROR.on_calculation_replaced()) \
			.append_to_slow_queue()


	# KILL PROCESS (if no more files in editor)
	@max_calls()
	def kill(self, filename):
		if not PROCESSES.is_initialized(get_root(filename)) \
			or self.is_killed:
			return

		self.is_killed = False

		def async_react_files(files):
			def kill_and_remove(_async_command=None):
				# Dont execute this twice (this fct will be called 3 times)
				if self.is_killed:
					Debug('tss+', "ALREADY closed ts project")
					return
				self.is_killed = True

				root = get_root(filename)
				PROCESSES.kill_and_remove(root)
				MESSAGE.show('TypeScript project will close', True)
				self.notify('kill', root)

			def still_used_ts_files_open_in_window(files):
				views = sublime.active_window().views()
				for v in views:
					if v.file_name() == None:
						continue
					for f in files:
						if v.file_name().replace('\\','/').lower() == f.lower() and not is_dts(v):
							Debug('tss+', "KILL? STILL MORE TS FILES open -> do nothing")
							return True
				Debug('tss', "NO MORE TS FILES -> kill TSS process")
				return False

			if not files: # TODO: why?
				return

			# don't quit tss if an added *.ts file is still open in an editor view
			if still_used_ts_files_open_in_window(files):
				return

			Debug('tss+', "No .ts files for rootfile left open => closing project %s" % get_root(filename))

			# send quit and kill process afterwards
			AsyncCommand('quit', get_root(filename)) \
				.set_id('quit') \
				.set_result_callback(kill_and_remove) \
				.append_to_both_queues()


			# if the tss process has hang up (previous lambda will not be executed)
			# , force kill after 5 sek
			sublime.set_timeout(kill_and_remove,10000)


		sublime.active_window().run_command('save_all')
		self.get_tss_indexed_files(filename, async_react_files)




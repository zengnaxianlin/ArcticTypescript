# coding=utf8

import sublime
import sublime_plugin

import os

from .TsconfigLinter import check_tsconfig, show_lint_in_status
from .tsconfigglobexpand import expand_filesglob
from ..utils.CancelCommand import catch_CancelCommand, CancelCommand

class TsconfigEventListener(sublime_plugin.EventListener):

    def on_activated_async(self, view):
        check_tsconfig(view)


    def on_load_async(self, view):
        check_tsconfig(view)


    def on_modified(self, view):
        check_tsconfig(view)


    def on_clone_async(self, view):
        check_tsconfig(view)


    @catch_CancelCommand
    def on_post_save_async(self, view):
        expand_filesglob(check_tsconfig(view))


    def on_selection_modified_async(self, view):
        show_lint_in_status(view)

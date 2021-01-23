import sublime
import sublime_plugin

import os

import re

def settings():
    return sublime.load_settings('devnotes.sublime-settings')


def get_root():
    project_settings = sublime.active_window().active_view().settings().get('devnotes')
    if project_settings:
        root = os.path.normpath(os.path.expanduser(project_settings.get('root', settings().get("root"))))
    else:
        root = os.path.normpath(os.path.expanduser(settings().get("root")))
    return root


def expand_to_braces(string, region_begin, region_end):
    regex = re.compile("(\[\[)([^\[\]]+)(\]\])")
    for match in regex.finditer(string):
        brace_begin = match.start()
        brace_end = match.end()
        if brace_end < region_end:
            continue
        if brace_begin > region_end:
            return None
        if brace_begin < region_begin:
            return match.group(2)
        return None


class OpenNoteCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        self.notes_dir = get_root()
        self.window = sublime.active_window()
        view = self.window.active_view()
        for region in view.sel():
            line = view.line(region)
            region_begin = region.begin() - line.begin()
            region_end = region.end() - line.begin()
            link = expand_to_braces(view.substr(line), region_begin, region_end)
            if link:
                self.open(link)
    def open(self, link):
        ext = "." + settings().get("note_save_extension")
        file = os.path.join(self.notes_dir, link + ext)
        if not os.path.exists(file):
            open(file, 'w+').close()
        view = self.window.open_file(file)



class NewNoteCommand(sublime_plugin.ApplicationCommand):
    def run(self, title=None, linked=False):
        self.notes_dir = get_root()
        self.window = sublime.active_window()
        self.linked = linked
        if title is None:
            self.window.show_input_panel("Title:", "", self.create_note, None, None)
        else:
            self.create_note(title)

    def create_note(self, title):
        fullname = title
        filename = title.split("/")
        if len(filename) > 1:
            title = filename[-1]
            folder = "\\"
            folder = folder.join(filename[:-1])
            directory = os.path.join(self.notes_dir, folder)
            tag = filename[0]
        else:
            title = filename[0]
            directory = self.notes_dir
            tag = ""
        if self.linked:
            view = self.window.active_view()
            view.run_command("insert_note_link", {"title": fullname})
        if not os.path.exists(directory):
            os.makedirs(directory)
        ext = "." + settings().get("note_save_extension")
        file = os.path.join(directory, title + ext)
        if not os.path.exists(file):
            open(file, 'w+').close()
        view = sublime.active_window().open_file(file)


class InsertNoteLinkCommand(sublime_plugin.TextCommand):

    def run(self, edit, title):
        for region in self.view.sel():
            self.view.insert(edit, region.begin(), "[["+title+"]]")

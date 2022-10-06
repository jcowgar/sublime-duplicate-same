import difflib

import sublime
import sublime_plugin

class DuplicateSameCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        region = self.view.sel()[0]
        if not region.empty():
            sublime.status_message(
                'no selection allowed when running duplicate same')
            return

        line = self.view.line(region)
        current_row, current_column = self.view.rowcol(region.begin())

        p1p = self.view.text_point(current_row - 1, current_column)
        p2p = self.view.text_point(current_row - 2, current_column)

        r1 = self.view.line(p1p)  # 1 line ago region
        r2 = self.view.line(p2p)  # 2 lines ago region

        line1 = self.view.substr(sublime.Region(p1p, r1.end()))
        line2 = self.view.substr(sublime.Region(p2p, r2.end()))

        snippet = self.generate_snippet(line1, line2)

        self.view.run_command("insert_snippet", {"contents": snippet})

    def generate_snippet(self, a, b):
        snippet = ''
        snippet_idx = 0
        in_snippet = False

        for i, s in enumerate(difflib.ndiff(a, b)):
            if s[0] == ' ':
                snippet += s[2]
            elif s[0] == '-':
                if in_snippet is False:
                    snippet_idx += 1
                    snippet += '${%i:' % snippet_idx
                    in_snippet = True
                snippet += s[2]
            elif s[0] == '+':
                if in_snippet is True:
                    in_snippet = False
                    snippet += '}'

        if in_snippet is True:
            snippet += '}'

        return snippet

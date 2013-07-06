import sublime
import sublime_plugin


class DuplicateSameCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        region = self.view.sel()[0]
        if not region.empty():
            sublime.status_message('no selection allowed when running duplicate same')
            return

        line = self.view.line(region)
        current_row, current_column = self.view.rowcol(region.begin())

        p1p = self.view.text_point(current_row - 1, current_column)
        p2p = self.view.text_point(current_row - 2, current_column)

        r1 = self.view.line(p1p)  # 1 line ago region
        r2 = self.view.line(p2p)  # 2 lines ago region

        line1 = self.view.substr(sublime.Region(p1p, r1.end()))
        line2 = self.view.substr(sublime.Region(p2p, r2.end()))

        for i in range(0, min(len(line1), len(line2))):
            if line1[i] != line2[i]:
                self.view.insert(edit, line.end(), line1[0:i])
                return

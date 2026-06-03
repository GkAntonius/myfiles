"""
Module to print out information.
"""

class ReportScreen:

    width = 79

    def get_banner(title):
            S = self.width * '=' + '\n'
            n = (self.width - len(title) - 2) // 2
            line = n*'=' + f' {title} ' + n*'='
            line += (len(line) % width) * '='
            S += line + '\n'
            S += self.width * '=' + '\n'
            return S

    def get_header(self):
        return self.get_banner('File Stoat')

    def get_footer(self):
        S = self.width * '=' + '\n'
        S += self.width * '=' + '\n'
        return S


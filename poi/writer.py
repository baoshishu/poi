from io import BytesIO

import xlsxwriter


class Writer:
    def __init__(self, global_format=None):
        self.output = BytesIO()
        self.workbook = xlsxwriter.Workbook(self.output)
        self.worksheet = self.workbook.add_worksheet()
        self.global_format = self.workbook.add_format(global_format)
        self.global_format_dict = global_format or {}

    def close(self):
        self.workbook.close()

    def read(self):
        self.output.seek(0)
        return self.output.read()

    def _calc_format(self, cell_format):
        if cell_format is None:
            cell_format = self.global_format
        elif isinstance(cell_format, dict):
            cell_format = self.workbook.add_format(
                {**self.global_format_dict, **cell_format}
            )
        return cell_format

    def _path_args(self, args):
        last_arg = args[-1]
        if isinstance(last_arg, dict):
            args = list(args[:-1]) + [self._calc_format(last_arg)]
        return args

    def write(self, *args):
        args = self._path_args(args)
        self.worksheet.write(*args)

    def merge_range(self, *args):
        args = self._path_args(args)
        self.worksheet.merge_range(*args)

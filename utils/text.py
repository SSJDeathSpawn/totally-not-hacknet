import re


class Text(object):
    def __init__(self, string, color, style, fontsize, scale=1, startingpos=[0, 0], ending=[20, 10], additional_colors:dict=None):
        
        self.string = string
        self.starting_color = color
        self.starting_style = style
        self.fontsize = fontsize
        self.scale_factor = scale
        self.startingpos = startingpos
        self.ending = ending
        
        self.escape_codes = { 
            'color': { '${c:reset}': self.starting_color, '${c:black}': (0, 0, 0), '${c:red}': (255, 0, 0), '${c:green}': (0, 255, 0), '${c:yellow}': (255, 255, 0), '${c:blue}': (0, 0, 255), '${c:magenta}': (255, 0, 255), '${c:cyan}': (0, 255, 255), '${c:white}': (255, 255, 255) },

            'style': { '${s:reset}': self.starting_style, '${s:regular}': 'regular', '${s:bold}': 'bold', '${s:italic}': 'italic', '${s:bold-italic}': 'bold-italic'}
        }

        if additional_colors: self.escape_codes['color'].update(additional_colors)

        self.escape_pattern = re.compile(r'(\$\{(?:c|s):[a-zA-Z-]+\})')
        self._process_string()

    def _process_string(self):
        base = self.string.split('\n')
        string = []

        for s in base:
            matches = self.escape_pattern.finditer(s)
            s_split = self.escape_pattern.split(s)
            codes = s_split[1::2] if len(s_split) > 1 else s_split

            code_to_index = {}

            while True:
                try:
                    item = next(matches)
                    code_to_index[item.start(0)] = codes.pop(0)
                except StopIteration:
                    break

            temp = ''.join(s_split[::2])

            i = 1
            while True:
                if len(temp) > self.ending[0] * i + i - 1:
                    temp = temp[:self.ending[0] * i + i - 1] + '\n' + temp[self.ending[0] * i + i - 1:]
                    i += 1
                else: break

            for i in code_to_index:
                original = i
                altered = original + temp[:i].count('\n')

                temp = temp[:altered] + code_to_index[i] + temp[altered:]

            string.append(temp)

        string = '\n'.join(string)
        
        self.processed = []

        color = self.starting_color
        style = self.starting_style
        fontsize = self.get_font_size()

        height = fontsize
        width = fontsize * 3 / 5
        
        pos = self.startingpos.copy()

        groups = self.escape_pattern.split(string)

        strings = groups[::2]
        codes = groups[1::2] if len(groups) > 1 else []

        for string in strings:
            if len(string) > 0:
                splitstring = string.split('\n')
                for part in splitstring:
                    self.processed.append((part, style, color, tuple(pos)))
                    pos[0] += (len(part) * (width))
                    if splitstring.index(part) + 1 < len(splitstring): 
                        pos[0] = self.startingpos[0]
                        pos[1] += height
            if codes: 
                code = codes.pop(0)
                if code[2] == 'c':
                    try: color = self.escape_codes['color'][code]
                    except KeyError as e: pass
                if code[2] == 's':
                    try: style = self.escape_codes['style'][code]
                    except KeyError as e: pass

        number_of_lines = 1
        pos = self.startingpos[1]
        for group in self.processed:
            if group[3][1] != pos:
                pos = group[3][1]
                number_of_lines += 1

        push = None

        index_to_start = 0

        if number_of_lines > self.ending[1]:
            count = 1
            pos = self.startingpos[1]
            for index, group in enumerate(self.processed):
                if group[3][1] != pos:
                    count += 1
                    pos = group[3][1]
                    if count > number_of_lines - self.ending[1]:
                        push = number_of_lines - self.ending[1]
                        index_to_start = index
                        break

        if not push: push = 0

        truncated = self.processed[index_to_start:]
        self.processed = [(group[0], group[1], group[2], (group[3][0], group[3][1] - (height * push))) for group in truncated]

    def get_raw_text(self):
        filtered = re.split(r'${[a-zA-Z0-9]+}', self.string)
        return ''.join(filtered[::2])

    def get_font_size(self):
        return self.fontsize

    def get_font_size_scaled(self):
        return int(self.fontsize * self.scale_factor)

    def update_string(self, string, new=False):
        self.string = self.string + string if not new else string 
        self._process_string()

    def update_color(self, color):
        self.starting_color = color
        self.escape_codes['color']['${color:reset}'] = self.starting_color

    def update_style(self, style):
        self.starting_style = style
        self.escape_codes['style']['${style:reset}'] = self.starting_style

    def update_scale_factor(self, scale):
        self.scale_factor = scale
        self._process_string

    def update_starting_position(self, startpos):
        self.startingpos = startpos
        self._process_string

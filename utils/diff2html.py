from unidiff import PatchSet
from copy import deepcopy
import io
import sys
import subprocess
import enum

class LineType(enum.Enum):
    Add = 1
    Rem = 2
    Empty = 3
    Both = 4
    Special = 5
    Current_Add = 6

css_styles = '''
    * {
        box-sizing: border-box;
    }
    .diff-container {
        box-shadow: 0px 0px 5px #000;
        margin-bottom: 50px;
        margin-top: 50px;
        border-radius: 10px;
        overflow: hidden;
        background-color: #eee;
    }
    .diff-container > .diff-row:first-child {
        height: 30px;
    }
    .diff-container > .diff-row:nth-child(2) > .diff-column .diff-line-number,
    .diff-container > .diff-row:nth-child(2) > .diff-column .diff-content {
        box-shadow: inset 0px 5px 5px -5px #000;
    }
    .diff-container .diff-pre {
        padding: 0;
        margin: 0;
        white-space: break-spaces;
        word-break: break-word;
    }
    .diff-container .diff-row > .diff-column:first-child{
        border-right: 1px solid #bbb;
    }
    .diff-container .diff-row {
        width: 100%;
        display: table;
    }
    .diff-container .diff-row > .diff-column:first-child {
        left: 0;
    }
    .diff-container .diff-row > .diff-column:nth-child(2) {
        right: 0;
    }
    .diff-container .diff-special {
        width: 100%;
        text-align: center;
        height: 24px;
        line-height: 24px;
        background-color: #eee;
        border-top: 1px solid #bbb;
        border-bottom: 1px solid #bbb;
    }
    .diff-container .diff-column {
        width: 50%;
        display: table-cell;
        vertical-align:top;
    }
    .diff-container .diff-column > div {
        display: table;
        width: 100%;
    }
    .diff-container .diff-header {
        padding-left: calc(5% + 3px);
        text-align: left;
        font-family: monospace;
        font-weight: normal;
        font-size: 12pt;
        background-color: #fff;
        height: 30px;
        line-height: 30px;
    }
    .diff-container .diff-line-number {
        width: 10%;
        display: table-cell;
        background-color: #eee;
        text-align: right;
        padding-right: 10px;
        vertical-align:top;
    }
    .diff-container .diff-content {
        display: table-cell;
        width: 90%;
        padding-left: 3px;
        vertical-align:top;
        background-color: #fff;
    }
    .diff-container .diff-content.diff-empty {
        background-color: #eee;
    }
    .diff-container .diff-after .diff-line-number.diff-added {
        background-color: rgb(191, 242, 191);
    }
    .diff-container .diff-after .diff-line-number.diff-current-added {
        background-color: rgb(169, 189, 245);
    }
    .diff-container .diff-before .diff-line-number.diff-removed {
        background-color: rgb(242, 191, 191);
    }
    .diff-container .diff-after .diff-content.diff-added {
        background-color: rgb(228, 255, 228);
    }
    .diff-container .diff-after .diff-content.diff-current-added {
        background-color: rgb(169, 189, 245);
    }
    .diff-container .diff-before .diff-content.diff-removed {
        background-color: rgb(255, 228, 228);
    }
'''

def convert_string_for_html(string):
    return string.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def convert_to_html(patches_before, patches_after):
    html_str = '<body><style>' + css_styles + '</style>'

    for patch_index in range(0, len(patches_before)):
        html_str += '<div class="diff-container"><div class="diff-row"><div class="diff-column diff-header">'
        html_str += patches_before[patch_index][0]
        html_str += '</div><div class="diff-column diff-header">'
        html_str += patches_after[patch_index][0]
        html_str += '</div></div>'

        for hunk_index in range(0, len(patches_before[patch_index][1])):
            for line_index in range(0, len(patches_before[patch_index][1][hunk_index])):
                html_str += '<div class="diff-row">'
                line_before = patches_before[patch_index][1][hunk_index][line_index]
                line_after = patches_after[patch_index][1][hunk_index][line_index]

                if line_before[0] == None:
                    html_str += '<div class="diff-special">'
                    html_str += convert_string_for_html(line_before[2])
                    html_str += '</div></div>'
                    continue

                element_class = 'diff-line-number'
                element_class += ' diff-removed' if line_before[1] == LineType.Rem else ''
                element_class += ' diff-empty' if line_before[1] == LineType.Empty else ''
                html_str += '<div class="diff-column diff-before"><div><div class="' + element_class + '">'
                html_str += str(line_before[0]) if line_before[1] != LineType.Empty else ''

                element_class = 'diff-content'
                element_class += ' diff-removed' if line_before[1] == LineType.Rem else ''
                element_class += ' diff-empty' if line_before[1] == LineType.Empty else ''
                html_str += '</div><div class="' + element_class + '"><div class="diff-pre">'
                html_str += convert_string_for_html(line_before[2])
                html_str += '</div></div></div></div>'

                element_class = 'diff-line-number'
                element_class += ' diff-added' if line_after[1] == LineType.Add else ''
                element_class += ' diff-current-added' if line_after[1] == LineType.Current_Add else ''
                element_class += ' diff-empty' if line_after[1] == LineType.Empty else ''
                html_str += '<div class="diff-column diff-after"><div><div class="' + element_class + '">'
                html_str += str(line_after[0]) if line_after[1] != LineType.Empty else ''
                
                element_class = 'diff-content'
                element_class += ' diff-added' if line_after[1] == LineType.Add else ''
                element_class += ' diff-current-added' if line_after[1] == LineType.Current_Add else ''
                element_class += ' diff-empty' if line_after[1] == LineType.Empty else ''
                html_str += '</div><div class="' + element_class + '"><div class="diff-pre">'
                html_str += convert_string_for_html(line_after[2])
                html_str += '</div></div></div></div></div>'

        html_str += '</div>'

    html_str += '</body>'

    return html_str


def highlight_n_change(patches, line_no):
    new_patches = deepcopy(patches)
    for patch_index in range(0, len(new_patches)):
        for hunk_index in range(0, len(new_patches[patch_index][1])):
            for line_index in range(0, len(new_patches[patch_index][1][hunk_index])):
                value = new_patches[patch_index][1][hunk_index][line_index]
                if value[1] == LineType.Add and value[0] == line_no:
                    new_patches[patch_index][1][hunk_index][line_index] = \
                                (value[0], LineType.Current_Add, value[2])
    return new_patches


def get_no_changes_lines(patches):
    indices = []
    for patch_index in range(0, len(patches)):
        for hunk_index in range(0, len(patches[patch_index][1])):
            for line_index in range(0, len(patches[patch_index][1][hunk_index])):
                value = patches[patch_index][1][hunk_index][line_index]
                if value[1] == LineType.Add:
                    indices.append(value[0])
    return indices

def parse_diff(diff):
    patch_set = PatchSet(diff)

    patches_before = []
    patches_after = []

    for patched_file in patch_set:
        file_before = []
        patches_before.append((patched_file.source_file, file_before))
        file_after = []
        patches_after.append((patched_file.target_file, file_after))

        for hunk in patched_file:
            if len(file_before):
                file_before[-1].append((None, LineType.Special, '. . . . .'))
                file_after[-1].append((None, LineType.Special, '. . . . .'))
            add_after = []
            hunk_before = []
            file_before.append(hunk_before)
            hunk_after = []
            file_after.append(hunk_after)

            for line in hunk:
                if line.line_type == '+':
                    value = (line.target_line_no, LineType.Add, line.value)
                    if len(hunk_before) and hunk_before[-1][1] == LineType.Rem and hunk_after[-1][1] == LineType.Empty:
                        try:
                            index = len(hunk_after) - 1
                            while (hunk_after[index][1] == LineType.Empty):
                                index -= 1
                            hunk_after[index + 1] = value
                        except Exception as e:
                            pass
                    else:
                        hunk_after.append(value)
                        hunk_before.append((0, LineType.Empty, ''))

                elif line.line_type == '-':
                    value = (line.source_line_no, LineType.Rem, line.value)
                    if len(hunk_after) and hunk_after[-1][1] == LineType.Add and hunk_before[-1][1] == LineType.Empty:
                        index = len(hunk_before) - 1
                        while (hunk_before[index][1] == LineType.Empty):
                            index -= 1
                        hunk_before[index + 1] = value
                    else:
                        hunk_before.append(value)
                        hunk_after.append((0, LineType.Empty, ''))
                elif line.source_line_no == None:
                    add_after.append((None, LineType.Special, line.value))
                else:
                    hunk_before.append((line.source_line_no, LineType.Both, line.value))
                    hunk_after.append((line.target_line_no, LineType.Both, line.value))
        
            for line in add_after:
                hunk_before.append(line)
                hunk_after.append(line)
    
    return patches_before, patches_after


def compare_files(file1, file2, lines=None):
    """
    Compares two files using the 'diff' command and returns the differences.
    Raises an exception if an error occurs.
    
    Parameters:
    file1 (str): The path to the first file to compare.
    file2 (str): The path to the second file to compare.
    
    Returns:
    str: The differences between the two files.
    """
    if not lines:
        args = ['diff', '-u', file1, file2]
    else:
        args = ['diff', f'-u{lines}', file1, file2]
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True
        )

        if result.stderr:
            raise Exception(result.stderr)

        return result.stdout
    
    except Exception as e:
        raise Exception(f"An error occurred: {e}")


def get_html_diff(file1, file2, lines=None):
    html_str_list = []
    patch_diff = compare_files(file1, file2, lines=lines)
    patches_before, patches_after = parse_diff(patch_diff)
    diff_lines = get_no_changes_lines(patches_after)
    for line in diff_lines:
        modified_patches_after = highlight_n_change(patches_after, line)
        html_str_list.append((line, convert_to_html(patches_before, modified_patches_after)))

    return html_str_list
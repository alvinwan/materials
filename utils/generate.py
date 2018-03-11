import sys
import json
import os
import re
import shutil

arguments = sys.argv

category = arguments[1]
number = arguments[2]
base_dir = 'src/%s' % category

title = '%s%s' % (category, number)

# Grab base tex
with open(os.path.join(base_dir, '%s.base.tex' % title)) as f:
    base_latex = f.read()


def hook_process_tex(filepath, tex, out_dir):
    """Process tex for question."""
    return hook_process_tex_code(filepath, tex, out_dir)


def hook_process_tex_code(filepath, tex, out_dir):
    """Process code snippets for code.
    1. Extract solutions from relevant file. Place solutions in .tex file.
    2. Generate starter python file. Place starter in output directory.
    3. Place solution in output directory.
    """

    pyfilepath = filepath.replace('.tex', '.py')
    pyfilename = os.path.basename(pyfilepath)
    if not os.path.exists(pyfilepath):
        return tex

    # Extract solutions
    format = '%%% insert {} %%%'
    regex = re.compile(r"### start ([\S]) ###\n([\s\S]+)\n[\s]+### end \1 ###")
    with open(pyfilepath) as f:
         content = f.read()
         starter = content
         for match in regex.finditer(content):
              # 1. Add to tex
              match, key, sol = match.group(0), match.group(1), match.group(2)
              tex = tex.replace(format.format(key), sol)

              # 2. Setup starter
              starter = starter.replace(sol, '')

    # 2. Generate starter python file
    pybasename = pyfilename.replace('.py', '')
    with open(os.path.join(out_dir, '%s-starter.py' % pybasename), 'w') as f:
        f.write(starter)

    # 3. Copy solution python file
    shutil.copy(pyfilepath, out_dir)

    return tex

# Grab raw tex
questions = []
base_texs = []
filenames = []
delimiters = ('\\begin{solution}', '\end{solution}')
regex = '|'.join(map(re.escape, delimiters))
out_dir = os.path.join(base_dir, '%s_data' % title)
for input_ in base_latex.splitlines():
    if not input_:
        continue
    filepath = 'src/problems/%s' % input_.replace('\input{', '')[:-1]
    filenames.append(filepath)
    tex = open(filepath).read()
    tex = hook_process_tex(filepath, tex, out_dir)
    base_texs.append(tex)
    pieces = re.split(regex, tex)
    raw_tex = ''.join(pieces[::2])
    questions.append(raw_tex)

with open(os.path.join(base_dir, '%s-raw.tex' % title), 'w') as f:
    f.write('\n'.join(questions))

generated_files = [
    {'template': 'template.tex', 'out': '%s.tex'},
    {'template': 'template-sol.tex', 'out': '%s-sol.tex'}
]

base_latex = '\n'.join(base_texs)

for data in generated_files:
    with open(os.path.join(base_dir, data['template'])) as f:
        latex = f.read().replace('<<title>>', title) \
                        .replace('<<base>>', base_latex)
    with open(os.path.join(base_dir, data['out'] % title), 'w') as f:
        f.write(latex)

# Generate images
template_img_path = os.path.join(base_dir, 'template-img.tex')
if os.path.exists(template_img_path):
    with open(template_img_path) as f:
        template = f.read()

    for i, filename in enumerate(filenames):
        with open(os.path.join(base_dir, '%s-img-%d.tex' % (title, i)), 'w') as f:
            f.write(template.replace('<<question>>', filename))

import sys
import json
import os
import re

arguments = sys.argv

category = arguments[1]
number = arguments[2]
base_dir = 'src/%s' % category

title = '%s%s' % (category, number)

# Grab base tex
with open(os.path.join(base_dir, '%s.base.tex' % title)) as f:
    base_latex = f.read()


def hook_process_tex(filename, tex):
    """Process tex for question."""
    return hook_process_tex_code(filename, tex)


def hook_process_tex_code(filename, tex):
    """Process code snippets for code.
    1. Extract solutions from relevant file. Place solutions in .tex file.
    2. Generate starter python file. Place starter in output directory.
    3. Generate solution python file. Place solution in output directory.
    """

    pyfilename = filename.replace('.tex', '.py')
    if not os.path.exists(pyfilename):
        return tex

    # 1. Extract solutions
    format = '%%% insert {} %%%'
    regex = re.compile(r"%%% start ([\S]) %%%([\s\S]+)%%% end \1 %%%")
    with open(pyfilename) as f:
         content = f.read()
         for match in regex.finditer(content):
              key, sol = match.group(1), match.group(2)
              code = r"\begin{lstlisting}%s\end{lstlisting}" % sol
              tex = tex.replace(format.format(key), code)
    return tex

# Grab raw tex
questions = []
base_texs = []
filenames = []
delimiters = ('\\begin{solution}', '\end{solution}')
regex = '|'.join(map(re.escape, delimiters))
for input_ in base_latex.splitlines():
    if not input_:
        continue
    filename = 'src/problems/%s' % input_.replace('\input{', '')[:-1]
    filenames.append(filename)
    tex = open(filename).read()
    tex = hook_process_tex(filename, tex)
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

#base_latex = base_latex.replace('\input{', '\input{src/problems/')
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

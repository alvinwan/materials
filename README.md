# Course Content Repository

This repository's primary purpose is to make document generation easier for course staff.

created by [Alvin Wan](http://alvinwan.com) and [Sinho Chewi](http://chewisinho.github.io)

# Installation

Clone the repository and change into the directory.

```
git clone https://github.com/alvinwan/materials.git
cd materials
```

Check that you have [Latex installed](http://latex-project.org/get). Then, install the necessary Python dependencies. (Optionally, [install in a virtual environment](#virtual-environment) instead of the following.)

```
pip install -r requirements.txt
```

# Installation for Piazza

If you are only using this repository to review or create documents from the command line, installation is complete. If you would like to generate image files to post on Piazza, you will need NodeJS and ImageMagick installed (for now).

> On Mac, [Homebrew](http://brew.sh) is the recommended package manager: ```brew install imagemagick npm nodejs``` installs ImageMagick, NodeJS and its package manager `npm`.

Install the Node packages required for the Piazza script.

```
npm install package.json
```

Installation complete. See "How to Use" to get started.

# How to Use

All commands are available via `make`. If for some reason, `make` is not installed on your OS, check the `Makefile` for the bash commands. For rendering assignments, you will not need the virtual environment. Only specific make commands require it, and when required, instructions below will specify how to activate the virtual environment.

## Adding Code

For code, *just add one solution file*. This file must have the same name as your original `tex` file. For example, if the original file is `extended-gcd.tex`, the file must be named `extended-gcd.py`. Delimit all question solutions using `%%% start [name] %%%` and `%%% end [name] %%%`, where `[name]` is any string, without punctuation. For example, see this solution file. There are two solutions sections, one named `a` and the other named `b`.

```
def extended_gcd(x, y):
    print('x:', x, 'y:', y)
    if y == 0:
        ### start a ###
        return (x, 1, 0)
        ### end a ###
    else:
        ### start b ###
        d, a, b = extended_gcd(y, x % y)
        print('d:', d, 'a:', a, 'b:', b)
        return (d, b, a - (x // y)*b)
        ### end b ###
```

In your `.tex` file, insert the relevant code in your solutions, using the `%%% insert [name] %%%` syntax. Here, we insert both solution parts `a` and `b`. These names have no significance and can be arbitrary.

```
\Question{Extended GCD}

\begin{Parts}

\Part Program the base case.

\begin{solution}
\begin{lstlisting}
%%% insert a %%%
\end{lstlisting}
\end{solution}

\Part Program the recursive case.

\begin{solution}
\begin{lstlisting}
%%% insert b %%%%
\end{lstlisting}
\end{solution}

\end{Parts}
```

The script will automatically:
1. Insert relevant code sections into your solutions PDF.
2. Generate a starter `.py` file in the document's respective output directory.
3. Copy solution `.py` into the document's respective output directory.

## Creating Documents

We now support a workflow which produces the `.tex` files from templates. The templates are located at `src/[category]/template.tex` and `src/[category]/template-sol.tex`. In order to make the actual documents, the only documents you need to edit are: a base `.base.tex` file containing the input problems, and the `.tex` files for the problems themselves.

Here, we will create a new document of the form `[category][num]`. This may be a discussion or homework; for simplicity, let us consider a document `dis01a`.

First, navigate to `src/dis/`, and make a file called `dis01a.base.tex`.

```
cd src/dis
touch dis01a.base.tex
```

Open up `dis01a.base.tex` using a text editor of your choice. Here is an example:

```
\input{modulararithmetic/text/introduction.tex}
\input{modulararithmetic/divisible-or-not.tex}
```

This file should only contain a list of `\input{...}`, each on its own line, referencing a problem or a text blurb. Browse through problems in `src/problems/`, and add problems above.

> Note: An old version of this repository split files into `folder/question.tex` and `folder/question.tex`. Simply merge the two.

## Adding Questions

The file starts with the command `\Question`. You are free to include whatever you want afterwards, and the solution should be wrapped in the `solution` environment. Example:

```
\Question{Compute This}

Suppose you had a program...

\begin{solution}

The program can indeed be computed by...

\end{solution}
```

## Rendering Document

First, navigate to the root directory of this repo. In other words `pwd` should end with `/materials`.

Then, to render an assignment, use `make [category] n=[number]`.
The following are valid categories:

- `dis`
- `hw`

For example, to make Discussion 1a, use

```
make dis n=01a
```

This will create two PDF files:

- `rendered/dis01a/dis01a.pdf`
- `rendered/dis01a/dis01a-sol.pdf`

What's going on when you run the command?
- First, the Python script `generate.py` is run to generate the `.tex` files from the base tex file, along with the embedded template files (files matching `template-*.tex`). (After rendering, you should find the generated `.tex` files in `src/[category]`.
- Then, the generated `.tex` files are compiled into `.pdf` files, and dumped into the `rendered` directory.

## Generating Image Files

After running `make hw n=[number]` as above, the command `make img n=[number]` will generate PNG image files, also in the `rendered` directory. To use this feature, you must have ImageMagick installed (see the requirements above).

## Posting to Piazza

Before using this utility, make sure to create `config.json`. We have provided a sample for you to fill in. You may duplicate the sample to get started.

```
cp sample_config.json config.json
```

We have provided a Piazza Course id, created for anyone to test on. You must fill in `username` and `password` with valid Piazza credentials.

After generating images per instructions in the previous section and setting up your configuration file, the command `make piazza n=[number]` will post all images on Piazza.

## Virtual Environment

Setup your virtual environment. The following will create a new environment called `course`.

```
conda create -n course python=3.5
```

Activate your virtual environment, and install all dependencies from `requirements.txt`.

```
source activate course
pip install -r requirements.txt
```

At this point, you may exit your virtual environment

```
source deactivate
```

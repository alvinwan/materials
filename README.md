# Course Content Repository

This repository's primary purpose is to make document generation easier for course staff.

created by [Alvin Wan](http://alvinwan.com) and [Sinho Chewi](http://chewisinho.github.io)

# Installation

Clone the repository.

```
git clone https://github.com/alvinwan/materials-template.git
```

Check if you have TeX installed.

```
tex --version
```

If not, install TeX [from source](https://www.tug.org/begin.html), **OR** by running the following to install Homebrew and then install TeX using it.

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install tex
```

In addition, you may need to install a few Ruby gems.

```
gem install erubis
gem install json
```

If you are only using this repository to review or create documents from the command line, installation is complete. If you would like to:

- import LaTeX files from other repositories
- use the web interface for this repository (not ready)
- post to Piazza automatically

you will need to setup a virtual environment as detailed in the following steps.

Setup your virtual environment. The following will create a new environment called `cs70`.

```
conda create -n cs70 python=3.5
```

Activate your virtual environment, and install all dependencies from `requirements.txt`.

```
source activate cs70
pip install -r requirements.txt
```

At this point, you may exit your virtual environment

```
source deactivate
```

If you would like to generate image files to post on Piazza, you will need to install ImageMagick.

```
brew install imagemagick
```

Installation complete. See "How to Use" to get started.

# How to Use

All commands are available via `make`. If for some reason, `make` is not installed on your OS, check the `Makefile` for the bash commands. For rendering assignments, you will not need the virtual environment. Only specific make commands require it, and when required, instructions below will specify how to activate the virtual environment.

## Creating Documents

We now support a workflow which produces the `.tex` files from templates. The templates are located at `src/[category]/template.tex.erb` and `src/[category]/template-sol.tex.erb`. In order to make the actual documents, the only documents you need to edit are: a JSON file containing the data for a document, and the `.tex` files for the problems themselves.

Here, we will create a new document of the form `[category][num]`. This may be a discussion or homework; for simplicity, let us consider a document `dis03b`.

First, navigate to `src/dis/`, and make a file called `dis03b.json`.

```
cd src/dis
touch dis03b.json
```

Open up `dis03b.json` using a text editor of your choice. If you are unfamiliar with JSON format, don't worry: the basics are simple. Here is an example:

```
{
  "questions": [
    "proofs/contraposition"
  ],
  "title": "DIS 07b"
}
```

The fields are documented below:
* `questions`: A comma-separated list of the problems, found in the directory `src/problems`.
* `title`: This will appear in the header of the document.

Browse through problems in `src/problems/`, and add problems to the `questions` field. If we want to add the question `computability/compute-this`, we need to ensure that the following files exist:
* `src/problems/computability/compute-this.tex`
* `src/problems/computability/compute-this-sol.tex`

Anything inside of the `src/problems/[category]/text/` category does not require a `-sol.tex` file.

(The `-sol` suffix is by convention, and is required for proper rendering.) If the question you want to use does not have these two files, then you will need to add them.

## Adding Questions

The question file starts with the command `\Question`. You are free to include whatever you want afterwards. Example:

```
\Question{Compute This}

Suppose you had a program...
```

The solution file should be wrapped in the `solution` environment. Example:

```
\begin{solution}

The program can indeed be computed by...

\end{solution}
```

## Rendering Document

First, navigate to the root directory of this repo. In other words `pwd` should end with `/materials-template`.

Then, to render an assignment, use `make [category] n=[number]`.
The following are valid categories:

- `dis`
- `hw`

For example, to make Discussion 3b, use

```
make dis n=03b
```

> **Note**: We have not yet run sanity checks against all of the LaTeX files. Some of them may contain random `\fi`s, misplaced curly braces, undefined control sequences, or otherwise incorrect syntax. Common mishaps include:
>
> - misplaced: `\fi`s, without an `\ifsolution` (remove both)
> - undefined: `\qitem`, which should be renamed to `\Part`
> - extra: `\end{enumerate}` or `\end{document}`
>
> Additionally, some files may contain multiple `\Question`s. This occurs when two problems are given the same title, to let us resolve duplicates easier. If they are the same, feel free to delete one copy. If they are different, feel free to split them up into multiple files.

This will create two PDF files:

- `rendered/dis03/dis03b.pdf`
- `rendered/dis03/dis03b-sol.pdf`

What's going on when you run the command?
- First, the Ruby script `generate.rb` is run to generate the `.tex` files from the JSON data file, along with the embedded Ruby template files (files ending with `.tex.erb`). (After rendering, you should find the generated `.tex` files in `src/[category]`.
- Then, the generated `.tex` files are compiled into `.pdf` files, and dumped into the `rendered` directory.

## Generating Image Files

After running `make hw n=[number]` as above, the command `make img n=[number]` will generate PNG image files, also in the `rendered` directory. To use this feature, you must have ImageMagick installed (see the requirements above).
# py2tex
Use Python within your latex files.

Within a LaTeX file, encapsulate  python code between 🐍 tags.  Anything you print will be inserted into the resulting LaTeX document.

## Example

Here's what a `.pytex` file might look like:
```
\documentclass{article}
\begin{document}

🐍
print('Python -> \\LaTeX!')
🐍

\end{document}
```
The corresponding LaTeX for this would be:
```
\documentclass{article}
\begin{document}

Python -> \LaTeX!


\end{document}
```

## How to use it: Standalone
If you compile your latex documents manually using `pdflatex` or some other LaTeX engine, simple run the following command beforehand:
```
$ py2tex infile.pytex outfile.tex
```

## How to use it: latexmk
If you use `latexmk`, perform the following steps to add `py2tex` as a custom dependency:
1. Place py2tex.py into your project's root directory
2. Create a `latexmkrc` file (if you don't already have one) and add a custom dependency to the end of it like this:
```perl
add_cus_dep('pytex','tex',0,'py2tex');
sub py2tex {
  system("./py2tex.py \"$_[0].pytex\" \"$_[0].tex\"");
}
```

That's it!  Now `latexmk` will use the `py2tex.py` to convert your `.py2tex` files to `.tex` files.  Here are some general guidelines for how `latexmk` decides to run the dependency:
- The `.pytex` and corresponding `.tex` file must have the same basename (e.g., main.pytex -> main.tex).
- The `.pytex` must have a system modiciation date earlier than the `.tex` file for `latexmk` to trigger the custom dependency.

If you want your root latex file (`latexmk`'s `default_files` variable) to be a .pytex file perform the following steps (assuming your root is named `main.pytex`):
1. Add the following line to your `latexmkrc`:
```perl
@default_files = ("main.tex");
```
2. Ensure that `main.tex` exists and has a system modification date older than your `main.pytex` file.

## Styling
If you use the [Sublime Text editor](https://www.sublimetext.com), you might find the `pytex.sublime-syntax` file helpful.  It provides syntax highlighting for pytex files (standard LaTeX outside 🐍 tags, standard python within 🐍 tags).  Import it using "Tools -> Developer -> New Syntax".

## Additional Information
This utility does not recognize escaped 🐍 tags.  If you must use 🐍 in your python code, consider using its unicode encoding instead (U+1F40D).


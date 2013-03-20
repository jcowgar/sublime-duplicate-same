# Duplicate Same

Duplicates what is the same between the previous two lines
from the current cursor position on.

For example, say you have:

    1: fname = models.CharField(blank=False, max_length=15)
    2: lname = models.CharField(blank=False, max_length=25)
    3: mname^

and your cursor is the ^ symbol on line three. Running the
command `Duplicate Same` would fill in line 3 to look like:

    3: mname = models.CharField(blank=False, max_length=

## For Help

Please visit http://github.com/jcowgar/sublime-duplicate-same

## Change Log

### Version 1.0.0

The initial release.

## License

Copyright (c) 2013 Jeremy Cowgar

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

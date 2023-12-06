Objective
---------

Provide an implementation of a parser for the NCVEC HAM Radio question pool.

The input should be a text document in the format provided by NCVEC.

The output should be a json document which can be used for subsequent
translations or higher level projects.


Motivation
----------

While there are existing JSON documents available with the same data, I did
not find the related source code which would enable me to change the output
formatting, write my own study app, validate the accuracy and completeness of
translation, or update the JSON documents when upstream changes are made.

Note that the Amateur Extra question pool is [slated for update][1] in 2024.

The objective is primarily to write my own study app but the source will be
made available to enable volunteer efforts around improved consistency of data
formatting with regard to the question pool, to encourage contributions and
collaboration around HAM study tools, and to provide a starting point for
anyone who might want to leverage or improve the code.

[1]: http://www.ncvec.org/page.php?id=333


NCVEC Resources
---------------

* [Technician](http://www.ncvec.org/page.php?id=373)
* [General](http://www.ncvec.org/page.php?id=369)
* [Extra](http://www.ncvec.org/page.php?id=356)

*NOTE:*
The diagrams for Technician and General license exams are available as JPEG
as well as embedded in the PDF documents. The PDF versions are higher quality
so I used the MacOS Preview application and screen capture to create PNG
format images from the PDF docs. I discarded the JPEG images.

*NOTE:*
The PDF document for Tech yeilds malformatted text when I copy/paste. Not
sure what the problem is but copy/paste from the docx format works fine. So
just use the DOCX documents for all the inputs. That is, copy/paste from the
docx resources instead of the PDF or text version. A text version of the
questions is available for download for the Extra license, but not for the
other licenses.

*NOTE:*
The General question docx has one formatting error in question G2E02.
I manually added a space after answer option "D".


Other Resources
---------------

Additional resources related to the NCVEC question pools.

* https://www.arrl.org/chapter-1-eclm-introduction
* https://hamexam.org/view_pool/17-Extra
* https://hamstudy.org/browse/E4_2020/E1D
* https://hamradioprep.com/
* https://github.com/russolsen/ham_radio_question_pool/tree/master
* https://github.com/statianzo/hampool
* https://arrlexamreview.appspot.com/

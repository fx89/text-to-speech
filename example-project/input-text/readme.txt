{{NARRATOR}}

The directory structure and file names do not have to abide by any
sort of rules other than the fact that the files containing the text
must have the TXT extension and that everything has to be placed in
the input-text directory.

The utility script parses the input-text directory recursively and,
provided it doesn't enter an infinite loop due to ill-placed symbolic
links, it transforms the content of every TXT file encountered into
wave files. The wave files are saved into the output-audio directory,
which is automatically created in the same root as the input-text
directory.

The structure of the output-audio directory will be the same as that
of the input-text directory. Provided the script doesn't crash and is
not interrupted, the output-audio directory will contain one wave file
for each TXT file contained in the input-text directory.

In addition to the aforementioned wave files, the audio segments from
which each wave file has been stitched together are also saved. They
are not saved as temporary files, and they are not deleted, because
they may prove to be useful for video editing projects.

The format of an input text file itself is not too restrictive. There
are, however, rules about identifying the voice actor that's meant to
speak the text. Voice actors are referenced using labels. A label is
the voice actor's ID, as defined in the voices yaml configuration file,
encased within double curly brackets. The labels are case-sensitive
and there is no trimming or other form of normalization being applied,
meaning that they must be written exactly as the actor IDs are written
in the configuration file. Input text files may include blank lines,
but each in put text file must have an actor label before the first
paragraph. If not, then the script will raise an exception because the
actor that's supposed to speak the paragraph is unknown. If there are
two or more consecutive actor labels without any sort of text in between,
then the first paragraph to follow will be spoken by the last actor to
have been referenced before the beginning of the paragraph. Actor labels
are allowed inside paragraphs and will result in switching voice actors
accordingly. However, every switch between voice actors will result in
the creation of a new audio segment. Placing an actor label at the end
of an input text file will have no effect.

The input text files are expected to have english text. The use of any
non-ASCII characters is not explicitly handled, therefore it may and is
very likely to produce unforeseen consequences.

Last, but not least, please note that the utility script is not using
streams or any other kind of memory optimization. Therefore, please be
sure to keep your input text files as short as humanly possible. Thank
you for understanding.
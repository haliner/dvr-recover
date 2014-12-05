#!/usr/bin/perl -W
#
# This script generates the Makefile to build the whole project.
#

use strict;


# Include paths
our $incpath = '-Isrc/';

# Userdefined variables
our $cc = 'gcc';

print(
"CC=$cc
LD=gcc
RM=rm -f
VERBOSE=@
CFLAGS=-g3 -O0 -Wall -Werror -D_LARGEFILE_SUPPORT -D_FILE_OFFSET_BITS=64
INCPATH=$incpath\n\n");



# This arrays will be filled with the filenames of all corresponding files, that
# might be build.
our @objects = ();
our @executables = ();
our @tests = ();




#
# Write make target definition for one c-source-file.
#
# The first argument must be the filename of the source-file.
#
sub compile_c_file {
	my $cfile = $_[0];

	my $target = $cfile;
	$target =~ s/\.c$/.o/;

	push(@objects, $target);

	print(`$cc $incpath -MM -MT "$target" "$cfile"` .
	      "\t\@echo [CC] $target\n" .
	      "\t" .'${VERBOSE}${CC} ${CFLAGS} ${INCPATH} -c -o $@ $<' . "\n\n");
}


#
# Write make target definition for an executable.
#
# The first argument must be the name of the target.
# The second argument must be a reference to an array of object files to
# link against.
#
sub link_executable {
	my $target = $_[0];
	my $obj = $_[1];

	push(@executables, $target);
	print("$target: " . join(' ', @$obj) . "\n" .
	      "\t\@echo [LD] $target\n" .
	      "\t" . '${VERBOSE}${LD} ${CFLAGS} -o $@ $^' . "\n\n");
}


#
# Write make target definition for a test.
#
# Arguments are the same as for link_executable.
#
sub link_test {
	link_executable(@_);
	push(@tests, $_[0]);
}




# Standard phony target.
print(".PHONY: all\nall: mpegrecover ;\n\n");


# Create target for every c-file.
foreach my $cfile(split(/\n/, `find . -name '*.c'`)) {
	# remove ./ at the beginning
	$cfile =~ s/^\.\///;
	compile_c_file($cfile);
}

link_test('tests/analysis', ['tests/analysis.o', 'src/analysis.o',
                             'src/dllist.o', 'src/endianness.o',
                             'src/mpeg.o']);
link_test('tests/buffer', ['tests/buffer.o', 'src/buffer.o']);
link_test('tests/dllist', ['tests/dllist.o', 'src/dllist.o']);
link_test('tests/mpeg', ['tests/mpeg.o', 'src/mpeg.o', 'src/endianness.o']);

link_executable('mpegrecover', ['src/main.o', 'src/analysis.o', 'src/buffer.o',
                                'src/dllist.o', 'src/endianness.o',
                                'src/mpeg.o']);


# Phony target to build all tests
print(".PHONY: tests\n" .
      "tests: " . join(' ', @tests) . " ;\n");


# Phony target to remove all cruft.
print(".PHONY: clean\n" .
      "clean:\n" .
      "\t" . '${RM} ' . join(' ', @objects) . "\n" .
      "\t" . '${RM} ' . join(' ', @executables) . "\n");

#!/usr/bin/perl -w
# Creates the Makefile for the mpegrecover project.

use strict;

print(
"RELEASE_JAR = mpegrecover.jar\n".
"TESTS_JAR = mpegrecover-tests.jar\n\n\n" .
".PHONY: all\n" .
"all: \$(RELEASE_JAR) ;\n\n"
);

open(my $fd_find, '-|', "find -name '*.java'");
while (<$fd_find>) {
 	my $source = $_;

	# remove ./ in front of filename
	$source =~ s/^\.\///;

	# remove new line at end of filename;
	$source =~ s/\n$//;

	my $target = $source;
	$target =~ s/\.java$/.class/;

	print("$target:\n");
}
close($fd_find);
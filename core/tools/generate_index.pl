#!/usr/bin/env perl

use strict;
use warnings;

my $content_dir = "content";
my $index_file  = "$content_dir/index.tex";

opendir(my $dh, $content_dir)
    or die "Cannot open '$content_dir': $!";

my @files = sort grep {
    /^[0-9][0-9]_.*\.tex$/
} readdir($dh);

closedir($dh);

open(my $fh, ">", $index_file)
    or die "Cannot create '$index_file': $!";

print $fh "% -------------------------------------------------\n";
print $fh "% Automatically generated -- DO NOT EDIT\n";
print $fh "% -------------------------------------------------\n\n";

foreach my $file (@files) {

    (my $name = $file) =~ s/\.tex$//;

    print $fh "\\input{content/$name}\n";
}

close($fh);

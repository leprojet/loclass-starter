#!/usr/bin/env perl

use strict;
use warnings;

sub generate_inputs {
    my ($dir, $pattern) = @_;

    my $outfile = "$dir/_inputs.tex";

    opendir(my $dh, $dir)
        or die "Cannot open '$dir': $!";

    my @files = sort grep {
        /$pattern/
        && $_ ne "_inputs.tex"
        && $_ ne "index.tex"
    } readdir($dh);
    
    closedir($dh);

    open(my $fh, ">", $outfile)
        or die "Cannot create '$outfile': $!";

    print $fh "% -------------------------------------------------\n";
    print $fh "% This file is generated automatically.\n";
    print $fh "% Do not edit manually.\n";
    print $fh "% -------------------------------------------------\n\n";    print "Generating $outfile\n";

    foreach my $file (@files) {
        print "  $file\n";
        (my $name = $file) =~ s/\.tex$//;
        print $fh "\\input{$dir/$name}\n";
    }

    close($fh);
}

generate_inputs(
    "content",
    qr/^[0-9][0-9]_.*\.tex$/,
);

generate_inputs(
    "project",
    qr/\.tex$/,
);

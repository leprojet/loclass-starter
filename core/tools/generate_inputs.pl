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
    print $fh "% Automatically generated -- DO NOT EDIT\n";
    print $fh "% -------------------------------------------------\n\n";

    foreach my $file (@files) {
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

# -------------------------------------------------
# Helpers
# -------------------------------------------------

sub shell_quote {
    my ($value) = @_;

    $value =~ s/'/'"'"'/g;
    return "'$value'";
}

sub run_or_die {
    my ($command) = @_;

    print "$command\n";

    my $status = system($command);

    if ($status == -1) {
        die "Could not execute command: $command\n";
    }

    my $exit_code = $status >> 8;

    if ($exit_code != 0) {
        die "Command failed with exit code $exit_code: $command\n";
    }
}

# -------------------------------------------------
# Project configuration
# -------------------------------------------------

sub loclass_config {
    my ($key) = @_;

    my $value = `uv run python core/tools/project_config.py $key`;
    my $status = $? >> 8;

    chomp $value;

    if ($status != 0 || $value eq '') {
        die "Could not read loclass project configuration: $key\n";
    }

    return $value;
}

my $loclass_tex_main = loclass_config('tex-main');
my $loclass_build_dir = loclass_config('build-dir');

my $loclass_source = "core/docs/ldl-specification.ldl";
my $loclass_generated_dir = "$loclass_build_dir/loclass";
my $loclass_package_preamble =
    "$loclass_generated_dir/loclass-generated-packages.tex";
my $loclass_tex_resource_dir = "$loclass_generated_dir/tex";
my $loclass_generated_content = "content/10_ldl_specification.tex";

# -------------------------------------------------
# Inputs
# -------------------------------------------------

my $existing_texinputs = $ENV{'TEXINPUTS'} // '';

$ENV{'TEXINPUTS'} =
    "core//:"
    . "$loclass_generated_dir//:"
    . $existing_texinputs;

# -------------------------------------------------
# Build
# -------------------------------------------------

$out_dir = $loclass_build_dir;
$pdf_mode = 1;

# -------------------------------------------------
# Main document
# -------------------------------------------------

@default_files = ($loclass_tex_main);

# -------------------------------------------------
# Pre-build
# -------------------------------------------------

run_or_die(
    "uv run loclass latex prepare "
    . shell_quote($loclass_source)
    . " --preamble "
    . shell_quote($loclass_package_preamble)
    . " --resource-dir "
    . shell_quote($loclass_tex_resource_dir)
);

run_or_die(
    "uv run loclass convert "
    . shell_quote($loclass_source)
    . " --backend latex "
    . "--output "
    . shell_quote($loclass_generated_content)
);

run_or_die(
    "perl core/tools/generate_inputs.pl"
);

# -------------------------------------------------
# Clean up
# -------------------------------------------------

$clean_ext .= " lor";

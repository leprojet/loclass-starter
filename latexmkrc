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

# -------------------------------------------------
# Inputs
# -------------------------------------------------

$ENV{'TEXINPUTS'} = "core//:";

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

system(
    "uv run loclass convert "
    . "core/docs/ldl-specification.ldl "
    . "--backend latex "
    . "--output content/10_ldl_specification.tex"
);

system("perl core/tools/generate_inputs.pl");

# -------------------------------------------------
# Clean up
# -------------------------------------------------

$clean_ext .= " lor";

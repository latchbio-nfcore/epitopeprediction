
from dataclasses import dataclass
import typing
import typing_extensions

from flytekit.core.annotation import FlyteAnnotation

from latch.types.metadata import NextflowParameter
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir

# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters

generated_parameters = {
    'input': NextflowParameter(
        type=LatchFile,
        default=None,
        section_title='Input/output options',
        description='Path to comma-separated file containing information about the samples in the experiment.',
    ),
    'outdir': NextflowParameter(
        type=typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})],
        default=None,
        section_title=None,
        description='The output directory where the results will be saved. You have to use absolute paths to storage on Cloud infrastructure.',
    ),
    'email': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Email address for completion summary.',
    ),
    'multiqc_title': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='MultiQC report title. Printed as page header, used for filename if not otherwise specified.',
    ),
    'genome_reference': NextflowParameter(
        type=typing.Optional[str],
        default='grch37',
        section_title='Reference options',
        description='Specifies the Ensembl genome reference version that will be used.',
    ),
    'proteome': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Specifies the reference proteome.',
    ),
    'filter_self': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Peptide prediction options',
        description='Filter against human proteome.',
    ),
    'max_peptide_length': NextflowParameter(
        type=typing.Optional[int],
        default=11,
        section_title=None,
        description='Specifies the maximum peptide length.',
    ),
    'min_peptide_length': NextflowParameter(
        type=typing.Optional[int],
        default=8,
        section_title=None,
        description='Specifies the minimum peptide length.',
    ),
    'max_peptide_length_class2': NextflowParameter(
        type=typing.Optional[int],
        default=16,
        section_title=None,
        description='Specifies the maximum peptide length for MHC class II peptides.',
    ),
    'min_peptide_length_class2': NextflowParameter(
        type=typing.Optional[int],
        default=15,
        section_title=None,
        description='Specifies the minimum peptide length for MHC class II peptides.',
    ),
    'tools': NextflowParameter(
        type=typing.Optional[str],
        default='syfpeithi',
        section_title=None,
        description='Specifies the prediction tool(s) to use.',
    ),
    'tool_thresholds': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Specifies tool-specific binder thresholds in a JSON file. This can be used to override the given default binder threshold values.',
    ),
    'use_affinity_thresholds': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Specifies the affinity metric instead of the rank metric used for determining whether a peptide is considered as a binder.',
    ),
    'wild_type': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Specifies whether wild-type sequences should be predicted.',
    ),
    'fasta_output': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Specifies that sequences of proteins, affected by provided variants, will be written to a FASTA file.',
    ),
    'show_supported_models': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Writes out supported prediction models.',
    ),
    'split_by_variants': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Run optimisation',
        description='Split VCF file into multiple files by number of variants.',
    ),
    'split_by_variants_size': NextflowParameter(
        type=typing.Optional[int],
        default=0,
        section_title=None,
        description='Number of variants that should be written into one file. Default: number of variants divided by ten',
    ),
    'split_by_variants_distance': NextflowParameter(
        type=typing.Optional[int],
        default=110000,
        section_title=None,
        description='Number of nucleotides between previous and current variant across split.',
    ),
    'peptides_split_maxchunks': NextflowParameter(
        type=typing.Optional[int],
        default=100,
        section_title=None,
        description='Specifies the maximum number of peptide chunks.',
    ),
    'peptides_split_minchunksize': NextflowParameter(
        type=typing.Optional[int],
        default=5000,
        section_title=None,
        description='Specifies the minimum number of peptides that should be written into one chunk.',
    ),
    'external_tools_meta': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='External software',
        description='Specifies the path to the JSON file with meta information on external prediction tools.',
    ),
    'netmhc_system': NextflowParameter(
        type=typing.Optional[str],
        default='linux',
        section_title=None,
        description='Specifies the operating system in use (Linux or Darwin). This is only necessary if conda is used.',
    ),
    'netmhcpan_path': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description="To use the 'netmhcpan' tool, specify the path to the original software tarball for NetMHCpan 4.0 here.",
    ),
    'netmhc_path': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description="To use the 'netmhc' tool, specify the path to the original software tarball for NetMHC 4.0 here.",
    ),
    'netmhciipan_path': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description="To use the 'netmhciipan' tool, specify the path to the original software tarball for NetMHCIIpan 3.1 here.",
    ),
    'netmhcii_path': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description="To use the 'netmhcii' tool, specify the path to the original software tarball for NetMHCII 2.2 here.",
    ),
    'multiqc_methods_description': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Generic options',
        description='Custom MultiQC yaml file containing HTML including a methods description.',
    ),
}


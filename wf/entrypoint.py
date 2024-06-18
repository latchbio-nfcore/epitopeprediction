from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, input: LatchFile, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], proteome: typing.Optional[str], filter_self: typing.Optional[bool], tool_thresholds: typing.Optional[str], use_affinity_thresholds: typing.Optional[bool], wild_type: typing.Optional[bool], fasta_output: typing.Optional[bool], show_supported_models: typing.Optional[bool], split_by_variants: typing.Optional[bool], external_tools_meta: typing.Optional[str], netmhcpan_path: typing.Optional[LatchFile], netmhc_path: typing.Optional[LatchFile], netmhciipan_path: typing.Optional[LatchFile], netmhcii_path: typing.Optional[LatchFile], multiqc_methods_description: typing.Optional[str], genome_reference: typing.Optional[str], max_peptide_length: typing.Optional[int], min_peptide_length: typing.Optional[int], max_peptide_length_class2: typing.Optional[int], min_peptide_length_class2: typing.Optional[int], tools: typing.Optional[str], split_by_variants_size: typing.Optional[int], split_by_variants_distance: typing.Optional[int], peptides_split_maxchunks: typing.Optional[int], peptides_split_minchunksize: typing.Optional[int], netmhc_system: typing.Optional[str]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('input', input),
                *get_flag('outdir', outdir),
                *get_flag('email', email),
                *get_flag('multiqc_title', multiqc_title),
                *get_flag('genome_reference', genome_reference),
                *get_flag('proteome', proteome),
                *get_flag('filter_self', filter_self),
                *get_flag('max_peptide_length', max_peptide_length),
                *get_flag('min_peptide_length', min_peptide_length),
                *get_flag('max_peptide_length_class2', max_peptide_length_class2),
                *get_flag('min_peptide_length_class2', min_peptide_length_class2),
                *get_flag('tools', tools),
                *get_flag('tool_thresholds', tool_thresholds),
                *get_flag('use_affinity_thresholds', use_affinity_thresholds),
                *get_flag('wild_type', wild_type),
                *get_flag('fasta_output', fasta_output),
                *get_flag('show_supported_models', show_supported_models),
                *get_flag('split_by_variants', split_by_variants),
                *get_flag('split_by_variants_size', split_by_variants_size),
                *get_flag('split_by_variants_distance', split_by_variants_distance),
                *get_flag('peptides_split_maxchunks', peptides_split_maxchunks),
                *get_flag('peptides_split_minchunksize', peptides_split_minchunksize),
                *get_flag('external_tools_meta', external_tools_meta),
                *get_flag('netmhc_system', netmhc_system),
                *get_flag('netmhcpan_path', netmhcpan_path),
                *get_flag('netmhc_path', netmhc_path),
                *get_flag('netmhciipan_path', netmhciipan_path),
                *get_flag('netmhcii_path', netmhcii_path),
                *get_flag('multiqc_methods_description', multiqc_methods_description)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_epitopeprediction", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_epitopeprediction(input: LatchFile, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], proteome: typing.Optional[str], filter_self: typing.Optional[bool], tool_thresholds: typing.Optional[str], use_affinity_thresholds: typing.Optional[bool], wild_type: typing.Optional[bool], fasta_output: typing.Optional[bool], show_supported_models: typing.Optional[bool], split_by_variants: typing.Optional[bool], external_tools_meta: typing.Optional[str], netmhcpan_path: typing.Optional[LatchFile], netmhc_path: typing.Optional[LatchFile], netmhciipan_path: typing.Optional[LatchFile], netmhcii_path: typing.Optional[LatchFile], multiqc_methods_description: typing.Optional[str], genome_reference: typing.Optional[str] = 'grch37', max_peptide_length: typing.Optional[int] = 11, min_peptide_length: typing.Optional[int] = 8, max_peptide_length_class2: typing.Optional[int] = 16, min_peptide_length_class2: typing.Optional[int] = 15, tools: typing.Optional[str] = 'syfpeithi', split_by_variants_size: typing.Optional[int] = 0, split_by_variants_distance: typing.Optional[int] = 110000, peptides_split_maxchunks: typing.Optional[int] = 100, peptides_split_minchunksize: typing.Optional[int] = 5000, netmhc_system: typing.Optional[str] = 'linux') -> None:
    """
    nf-core/epitopeprediction

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, input=input, outdir=outdir, email=email, multiqc_title=multiqc_title, genome_reference=genome_reference, proteome=proteome, filter_self=filter_self, max_peptide_length=max_peptide_length, min_peptide_length=min_peptide_length, max_peptide_length_class2=max_peptide_length_class2, min_peptide_length_class2=min_peptide_length_class2, tools=tools, tool_thresholds=tool_thresholds, use_affinity_thresholds=use_affinity_thresholds, wild_type=wild_type, fasta_output=fasta_output, show_supported_models=show_supported_models, split_by_variants=split_by_variants, split_by_variants_size=split_by_variants_size, split_by_variants_distance=split_by_variants_distance, peptides_split_maxchunks=peptides_split_maxchunks, peptides_split_minchunksize=peptides_split_minchunksize, external_tools_meta=external_tools_meta, netmhc_system=netmhc_system, netmhcpan_path=netmhcpan_path, netmhc_path=netmhc_path, netmhciipan_path=netmhciipan_path, netmhcii_path=netmhcii_path, multiqc_methods_description=multiqc_methods_description)


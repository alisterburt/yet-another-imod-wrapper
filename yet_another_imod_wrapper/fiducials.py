import subprocess
from os import PathLike
from pathlib import Path
from typing import Dict, Any
import tempfile

from .constants import TARGET_PIXEL_SIZE_FOR_ALIGNMENT, BATCHRUNTOMO_CONFIG_FIDUCIALS
from .utils import find_optimal_power_of_2_binning_factor
from .batchruntomo_config.io import read_adoc, write_adoc


def batchruntomo_fiducials(tilt_series_file, pixel_size, fiducial_size, rotation_angle):
    tilt_series_directory = Path(tilt_series_file).parent
    root_name = Path(tilt_series_file).stem
    directive = generate_fiducial_alignment_directive(
        tilt_series_file=tilt_series_file,
        pixel_size=pixel_size,
        fiducial_size=fiducial_size,
        rotation_angle=rotation_angle
    )
    with tempfile.TemporaryDirectory() as temporary_directory:
        directive_file = Path(temporary_directory) / 'directive.adoc'
        write_adoc(directive, directive_file)
        batchruntomo_command = [
            'batchruntomo',
            '-DirectiveFile', f'{directive_file}',
            '-RootName', f'{root_name}',
            '-CurrentLocation', f'{tilt_series_directory}',
            '-EndingStep', '6'
        ]
        subprocess.run(batchruntomo_command)


def generate_fiducial_alignment_directive(
        tilt_series_file: PathLike,
        pixel_size: float,
        fiducial_size: float,
        rotation_angle: float
) -> Dict[str, Any]:
    """Generate a fiducial-based alignment directive file for batchruntomo

    Parameters
    ----------
    tilt_series_file : file containing the tilt-series stack
    pixel_size : pixel size in the tilt-series (angstroms per pixel)
    fiducial_size : fiducial size (nanometers)
    rotation_angle : initial estimate for the rotation angle
        https://bio3d.colorado.edu/imod/doc/tomoguide.html#UnknownAxisAngle
    """
    alignment_binning_factor = find_optimal_power_of_2_binning_factor(
        src_pixel_size=pixel_size, target_pixel_size=TARGET_PIXEL_SIZE_FOR_ALIGNMENT
    )
    directive = read_adoc(BATCHRUNTOMO_CONFIG_FIDUCIALS)
    directive['setupset.copyarg.stackext'] = Path(tilt_series_file).suffix
    directive['setupset.copyarg.rotation'] = rotation_angle
    directive['setupset.copyarg.pixel'] = pixel_size / 10
    directive['setupset.copyarg.gold'] = fiducial_size
    directive['comparam.prenewst.newstack.BinByFactor'] = alignment_binning_factor
    return directive


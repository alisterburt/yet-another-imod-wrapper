from pathlib import Path as _Path

BATCHRUNTOMO_CONIFG_DIR = _Path(__file__).parent / 'batchruntomo_config'
BATCHRUNTOMO_CONFIG_FIDUCIALS = BATCHRUNTOMO_CONIFG_DIR / 'fiducials.adoc'
BATCHRUNTOMO_CONFIG_PATCH_TRACKING = BATCHRUNTOMO_CONIFG_DIR / 'patch_tracking.adoc'

TARGET_PIXEL_SIZE_FOR_ALIGNMENT = 10

MINIMUM_IMOD_VERSION = '4.11.0'

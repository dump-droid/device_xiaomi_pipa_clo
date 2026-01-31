#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2016 The CyanogenMod Project
# SPDX-FileCopyrightText: 2017-2024 The LineageOS Project
# SPDX-FileCopyrightText: 2021-2024 Paranoid Android
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)
from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)

blob_fixups: blob_fixups_user_type = {
    'odm/bin/hw/vendor.dolby_v3_6.hardware.dms360@2.0-service': blob_fixup()
        .add_needed('libstagefright_foundation-v33.so'),
    ('vendor/lib64/libcodec2_soft_ac4dec.so', 'vendor/lib64/libcodec2_soft_ddpdec.so'): blob_fixup()
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v34_cancunf.so'),
    'vendor/lib64/libdeccfg.so': blob_fixup()
        .replace_needed('libdapparamstorage.so', 'libdapparamstorage-v34_cancunf.so'),
    ('vendor/lib64/mediadrm/libwvdrmengine.so', 'vendor/lib64/libwvhidl.so'): blob_fixup()
        .add_needed('libcrypto_shim.so'),
    ('vendor/lib/libaudioroute_ext.so', 'vendor/lib/hw/audio.primary.kona.so'): blob_fixup()
        .replace_needed('libaudioroute.so', 'libaudioroute-v34.so'),
}  # fmt: skip

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
}

namespace_imports = [
    'device/xiaomi/pipa',
    'vendor/qcom/common/vendor/adreno-r',
    'vendor/qcom/common/vendor/display',
    'vendor/qcom/common/vendor/display/4.19',
    'vendor/qcom/common/vendor/media/legacy',
    'hardware/xiaomi',
]

module = ExtractUtilsModule(
    'pipa',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    check_elf=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()

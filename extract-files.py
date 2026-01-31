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
   ('vendor/lib64/mediadrm/libwvdrmengine.so', 'vendor/lib64/libwvhidl.so'): blob_fixup()
        .add_needed('libcrypto_shim.so'),
    'vendor/lib/hw/audio.primary.pipa.so': blob_fixup()
        .replace_needed('/vendor/lib/liba2dpoffload.so', 'liba2dpoffload_pipa.so\x00\x00\x00\x00\x00\x00\x00')
        .replace_needed('/vendor/lib/libssrec.so', 'libssrec_pipa.so\x00\x00\x00\x00\x00\x00\x00'),
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

SUMMARY = "The API for Pytesseract"
HOMEPAGE = "https://github.com/madmaze/pytesseract"
LICENSE = "Apache-2.0"
LIC_FILES_CHKSUM = "file://LICENSE;md5=86d3f3a95c324c9479bd8986968f4327"

SRC_URI[sha256sum] = "b79641b7915ff039da22d5591cb2f5ca6cb0ed7c65194c9c750360dc6a1cc87f"

inherit pypi setuptools3

RDEPENDS_${PN} += "\
    ${PYTHON_PN}-pillow \
"

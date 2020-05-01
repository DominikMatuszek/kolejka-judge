#!/bin/bash
LIBRARY="kolejka-judge"
OFFICE="$(dirname "$(readlink -f "$(dirname "$(which "$0")")")")"
JUDGE="${OFFICE}/judges/generic"

pushd "${JUDGE}" >/dev/null 2>&1
    rm -rf "${LIBRARY}" 

    pushd "${OFFICE}/packages/KolejkaJudge" >/dev/null 2>&1
        rm -rf dist
        python3 setup.py bdist_wheel >/dev/null 2>&1
        BUILD="$(ls -1 dist/KolejkaJudge-*-py3-none-any.whl |tail -n 1)"
        cp -a "${BUILD}" "${JUDGE}/${LIBRARY}"
    popd >/dev/null 2>&1
    pushd "${OFFICE}/packages" >/dev/null 2>&1
        python3 wheel_repair.py "${JUDGE}/${LIBRARY}" >/dev/null 2>&1
    popd >/dev/null 2>&1

popd >/dev/null 2>&1

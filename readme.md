# cyclonedds

## cmake-vars
- `-DBUILD_EXAMPLES=1`: to build the included examples
- `-DBUILD_TESTING=1`: to build the test suite (forces exporting all symbols from the library)
- `-DBUILD_IDLC=0`: to disable building the IDL compiler (affects building examples, tests and `ddsperf`)
- `-DBUILD_DDSPERF=0`: to disable building the [`ddsperf`](https://github.com/eclipse-cyclonedds/cyclonedds/tree/master/src/tools/ddsperf) tool for performance measurement
- `-DENABLE_SSL=0`: to not look for OpenSSL, remove TLS/TCP support and avoid building the plugins that implement authentication and encryption (default is `AUTO` to enable them if OpenSSL is found)
- `-DENABLE_ICEORYX=0`: do not look for Iceoryx disable building the PSMX Iceoryx plugin (default is `AUTO` to enable it if Iceoryx is found)
- `-DENABLE_SECURITY=0`: to not build the security interfaces and hooks in the core code, nor the plugins (one can enable security without OpenSSL present, you'll just have to find plugins elsewhere in that case)
- `-DENABLE_LIFESPAN=0`: to exclude support for finite lifespans QoS
- `-DENABLE_DEADLINE_MISSED=0`: to exclude support for finite deadline QoS settings
- `-DENABLE_TYPELIB=0`: to exclude support for type library, requires also disabling type and topic discovery using `-DENABLE_TYPE_DISCOVERY=0` and `-DENABLE_TOPIC_DISCOVERY=0`
- `-DENABLE_TYPE_DISCOVERY=0`: to exclude support for type discovery and checking type compatibility (effectively most of XTypes), requires also disabling topic discovery using `-DENABLE_TOPIC_DISCOVERY=0`
- `-DENABLE_TOPIC_DISCOVERY=0`: to exclude support for topic discovery
- `-DENABLE_SOURCE_SPECIFIC_MULTICAST=0`: to disable support for source-specific multicast (disabling this and `-DENABLE_IPV6=0` may be needed for QNX builds)
- `-DENABLE_IPV6=0`: to disable ipv6 support (disabling this and `-DENABLE_SOURCE_SPECIFIC_MULTICAST=0` may be needed for QNX builds)
- `-DBUILD_IDLC_XTESTS=0`: Include a set of tests for the IDL compiler that use the C back-end to compile an idl file at (test) runtime, and use the C compiler to build a test application for the generated types, that is executed to do the actual testing (not supported on Windows)

## how-to-configure
1. `cmake --preset ${preset}` where `${preset}` is one of `cmake --list-presets`

## how-to-build
1. follow `how-to-configure`
2. `cmake --build --preset ${preset}`
3. `cmake --build --preset ${preset} --target cmake-install`

## how-to-export
1. follow `how-to-configure`
2. `cmake --build --preset ${preset} --target conan-remove`
3. `cmake --build --preset ${preset}`
4. `cmake --build --preset ${preset} --target conan-export`

## how-to-export-all-packages
1. `conan remove -c cyclonedds`
2. `git clean -xdf`
3. `cmake --list-presets | cut -d ':' -f2 | xargs -I '{}' echo '{}' | xargs -I '{}' bash -c "cmake --preset {} || exit 255"`
4. `cmake --list-presets | cut -d ':' -f2 | xargs -I '{}' echo '{}' | xargs -I '{}' bash -c "cmake --build --preset {} || exit 255"`
5. `cmake --list-presets | cut -d ':' -f2 | xargs -I '{}' echo '{}' | xargs -I '{}' bash -c "cmake --build --preset {} --target conan-export || exit 255"`

### examples

#### build-example
1. `cmake --preset windows.ninja.msvc-x64-x64.debug.shared`
2. `cmake --build --preset windows.ninja.msvc-x64-x64.debug.shared`
3. `cmake --build --preset windows.ninja.msvc-x64-x64.debug.shared --target cmake-install`

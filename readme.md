# cyclonedds

##### Variables:

* `-DBUILD_EXAMPLES=ON`: to build the included examples
* `-DBUILD_TESTING=ON`: to build the test suite (forces exporting all symbols from the library)
* `-DBUILD_IDLC=NO`: to disable building the IDL compiler (affects building examples, tests and `ddsperf`)
* `-DBUILD_DDSPERF=NO`: to disable building the [`ddsperf`](https://github.com/eclipse-cyclonedds/cyclonedds/tree/master/src/tools/ddsperf) tool for performance measurement
* `-DENABLE_SSL=NO`: to not look for OpenSSL, remove TLS/TCP support and avoid building the plugins that implement authentication and encryption (default is `AUTO` to enable them if OpenSSL is found)
* `-DENABLE_ICEORYX=NO`: do not look for Iceoryx disable building the PSMX Iceoryx plugin (default is `AUTO` to enable it if Iceoryx is found)
* `-DENABLE_SECURITY=NO`: to not build the security interfaces and hooks in the core code, nor the plugins (one can enable security without OpenSSL present, you'll just have to find plugins elsewhere in that case)
* `-DENABLE_LIFESPAN=NO`: to exclude support for finite lifespans QoS
* `-DENABLE_DEADLINE_MISSED=NO`: to exclude support for finite deadline QoS settings
* `-DENABLE_TYPELIB=NO`: to exclude support for type library, requires also disabling type and topic discovery using `-DENABLE_TYPE_DISCOVERY=NO` and `-DENABLE_TOPIC_DISCOVERY=NO`
* `-DENABLE_TYPE_DISCOVERY=NO`: to exclude support for type discovery and checking type compatibility (effectively most of XTypes), requires also disabling topic discovery using `-DENABLE_TOPIC_DISCOVERY=NO`
* `-DENABLE_TOPIC_DISCOVERY=NO`: to exclude support for topic discovery
* `-DENABLE_SOURCE_SPECIFIC_MULTICAST=NO`: to disable support for source-specific multicast (disabling this and `-DENABLE_IPV6=NO` may be needed for QNX builds)
* `-DENABLE_IPV6=NO`: to disable ipv6 support (disabling this and `-DENABLE_SOURCE_SPECIFIC_MULTICAST=NO` may be needed for QNX builds)
* `-DBUILD_IDLC_XTESTS=NO`: Include a set of tests for the IDL compiler that use the C back-end to compile an idl file at (test) runtime, and use the C compiler to build a test application for the generated types, that is executed to do the actual testing (not supported on Windows)

##### Build:

```
cmake --preset windows.ninja.msvc-16-x64-x64.release.shared
cmake --build --preset windows.ninja.msvc-16-x64-x64.release.shared
cmake --build --preset windows.ninja.msvc-16-x64-x64.release.shared --target conan-export
```

##### Examples:

* Build `idlc`:
  * `cmake -DBUILD_IDLC=ON --preset windows.ninja.msvc-16-x64-x64.debug.shared`
  * `cmake --build --preset windows.ninja.msvc-16-x64-x64.debug.shared --target idlc`
  * `cmake --build --preset windows.ninja.msvc-16-x64-x64.debug.shared --target cmake-install`

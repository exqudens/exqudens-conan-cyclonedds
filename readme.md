# cyclonedds

### How To

##### How To Create Package

```
cmake --preset windows.ninja.msvc-16-x64-x64.debug.shared
cmake --build --preset windows.ninja.msvc-16-x64-x64.debug.shared
cmake --build --preset windows.ninja.msvc-16-x64-x64.debug.shared --target cmake-install
```

##### How To Create Conan Package

```
cmake --preset windows.ninja.msvc-16-x64-x64.debug.shared
cmake --build --preset windows.ninja.msvc-16-x64-x64.debug.shared
cmake --build --preset windows.ninja.msvc-16-x64-x64.debug.shared --target conan-export
```

# Changelog

## [2.4.0](https://github.com/rokam/midea-local/compare/v2.3.0...v2.4.0) (2024-07-24)


### Features

* **cli:** set attribute from device ([#241](https://github.com/rokam/midea-local/issues/241)) ([6f0a109](https://github.com/rokam/midea-local/commit/6f0a10942c0b5defd3622c14bcd2795b34ec01a8))
* segregate connect/auth/refresh/enable device duties ([#233](https://github.com/rokam/midea-local/issues/233)) ([681bd79](https://github.com/rokam/midea-local/commit/681bd79f078deafe82cc4708f47c53c808dca064))

## [2.3.0](https://github.com/rokam/midea-local/compare/v2.2.0...v2.3.0) (2024-07-23)


### Features

* **message:** body parsers ([#235](https://github.com/rokam/midea-local/issues/235)) ([c636eee](https://github.com/rokam/midea-local/commit/c636eeef5128504c079704d023e2215896e3c770))

## [2.2.0](https://github.com/rokam/midea-local/compare/v2.1.1...v2.2.0) (2024-07-20)


### Features

* redact data from cloud ([#232](https://github.com/rokam/midea-local/issues/232)) ([c61991e](https://github.com/rokam/midea-local/commit/c61991eb93ca817d6245328fe1f5828a33dc5738))

## [2.1.1](https://github.com/rokam/midea-local/compare/v2.1.0...v2.1.1) (2024-07-16)


### Bug Fixes

* **cloud:** get default keys as static ([#229](https://github.com/rokam/midea-local/issues/229)) ([815643a](https://github.com/rokam/midea-local/commit/815643a1a59a14863090b0cdd65170605a8b91da))

## [2.1.0](https://github.com/rokam/midea-local/compare/v2.0.0...v2.1.0) (2024-07-16)


### Features

* **c3:** add option to set super_silent ([#210](https://github.com/rokam/midea-local/issues/210)) ([dcef500](https://github.com/rokam/midea-local/commit/dcef500f073ce150283730132fd4a3155850e332))
* **c3:** query and set silence level ([#227](https://github.com/rokam/midea-local/issues/227)) ([556f7c2](https://github.com/rokam/midea-local/commit/556f7c234d4581472b0ce2f3830289b2ba529c90))

## [2.0.0](https://github.com/rokam/midea-local/compare/v1.3.2...v2.0.0) (2024-07-12)


### ⚠ BREAKING CHANGES

* rework auth flow - part 1 ([#219](https://github.com/rokam/midea-local/issues/219)) ([d8ac4fb](https://github.com/rokam/midea-local/commit/d8ac4fb5de25dbf04548b411f5a930878b32a2df))

### Features

* **cli:** download protocol ([#214](https://github.com/rokam/midea-local/issues/214)) ([7a99374](https://github.com/rokam/midea-local/commit/7a993745c0c7fcf1e9eff86a2287e3cbff3f3d8d))
* rework auth flow - part 1 ([#219](https://github.com/rokam/midea-local/issues/219)) ([d8ac4fb](https://github.com/rokam/midea-local/commit/d8ac4fb5de25dbf04548b411f5a930878b32a2df))
* rework auth flow - part 2 ([#221](https://github.com/rokam/midea-local/issues/221)) ([f74ff8e](https://github.com/rokam/midea-local/commit/f74ff8e1af924d84621958d0c6d8659cef1b98e6))

## [1.3.2](https://github.com/rokam/midea-local/compare/v1.3.1...v1.3.2) (2024-07-11)


### Bug Fixes

* **capabilities:** make capabilities optional ([#217](https://github.com/rokam/midea-local/issues/217)) ([c269e71](https://github.com/rokam/midea-local/commit/c269e717c2b2b5e7f390f0e2ba781513584442b2))

## [1.3.1](https://github.com/rokam/midea-local/compare/v1.3.0...v1.3.1) (2024-07-10)


### Bug Fixes

* wrong dependencies with package ([#215](https://github.com/rokam/midea-local/issues/215)) ([d63fc6b](https://github.com/rokam/midea-local/commit/d63fc6b49394f9bfc9c9cb32b34c36b5e97f02a6))

## [1.3.0](https://github.com/rokam/midea-local/compare/v1.2.0...v1.3.0) (2024-07-10)


### Features

* **c3:** temperature step as customize ([#209](https://github.com/rokam/midea-local/issues/209)) ([4da6e3e](https://github.com/rokam/midea-local/commit/4da6e3eb18eae9b24b4300274e307db0af8633de))
* **cli:** midealocal CLI tool ([#204](https://github.com/rokam/midea-local/issues/204)) ([236e33a](https://github.com/rokam/midea-local/commit/236e33a95fde65aba499832bb6901f32ac21628d))


### Bug Fixes

* **device:** capabilities ([#212](https://github.com/rokam/midea-local/issues/212)) ([f7cff37](https://github.com/rokam/midea-local/commit/f7cff3767522a6f1008a5f7b4ef8677ecd9296bc))

## [1.2.0](https://github.com/rokam/midea-local/compare/v1.1.4...v1.2.0) (2024-07-08)


### Features

* **ac:** mode capabilities ([#196](https://github.com/rokam/midea-local/issues/196)) ([43d9918](https://github.com/rokam/midea-local/commit/43d9918be79f8dbb4f8b126d121619d04efe47cf))


### Bug Fixes

* **da:** avoid indexes out of bounds ([#199](https://github.com/rokam/midea-local/issues/199)) ([246f9c7](https://github.com/rokam/midea-local/commit/246f9c752f49a5425e06ea1b3772347bc4eb3880))
* rollback get_keys with 3 keys ([#200](https://github.com/rokam/midea-local/issues/200)) ([54153a8](https://github.com/rokam/midea-local/commit/54153a8fd24c5f5ae3ef2b02e7ef863d18bc998a))

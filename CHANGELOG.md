# Changelog

## [6.0.3](https://github.com/rokam/midea-local/compare/v6.0.2...v6.0.3) (2024-10-15)


### Bug Fixes

* cleanup and complete body and subbody types lists ([#325](https://github.com/rokam/midea-local/issues/325)) ([914dcb8](https://github.com/rokam/midea-local/commit/914dcb8098efe50cc1583ad81fd22b49e9e2536b))

## [6.0.2](https://github.com/rokam/midea-local/compare/v6.0.1...v6.0.2) (2024-10-08)


### Bug Fixes

* add more BodyType ([#321](https://github.com/rokam/midea-local/issues/321)) ([a1b4ac8](https://github.com/rokam/midea-local/commit/a1b4ac807e3b475f0a32f44c0f1d7af980d7a486))

## [6.0.1](https://github.com/rokam/midea-local/compare/v6.0.0...v6.0.1) (2024-10-06)


### Bug Fixes

* add missing body_type "163" ([#317](https://github.com/rokam/midea-local/issues/317)) ([45f7bd2](https://github.com/rokam/midea-local/commit/45f7bd2432a04fb69c9fdb9b6204de7eac87aa2e))
* message protocol version default ([#316](https://github.com/rokam/midea-local/issues/316)) ([2f4e5d1](https://github.com/rokam/midea-local/commit/2f4e5d1d1335696cc3a179a67cf287eef54b6864))
* protocol check in B6 devices ([#320](https://github.com/rokam/midea-local/issues/320)) ([55659c1](https://github.com/rokam/midea-local/commit/55659c19a642fadfd37aee32fbeae76e48aed3dd))

## [6.0.0](https://github.com/rokam/midea-local/compare/v5.0.0...v6.0.0) (2024-10-03)


### ⚠ BREAKING CHANGES

* **cloud:** rename MSmartHome ([#306](https://github.com/rokam/midea-local/issues/306))

### Miscellaneous Chores

* **cloud:** rename MSmartHome ([#306](https://github.com/rokam/midea-local/issues/306)) ([20c796e](https://github.com/rokam/midea-local/commit/20c796eb9f9728ff4042f3caf2e0ff11012e12f5)), closes [#286](https://github.com/rokam/midea-local/issues/286)

## [5.0.0](https://github.com/rokam/midea-local/compare/v4.0.0...v5.0.0) (2024-10-02)


### ⚠ BREAKING CHANGES

* **device:** rollback and socket refresh_status ([#307](https://github.com/rokam/midea-local/issues/307))

### Bug Fixes

* **device:** rollback and socket refresh_status ([#307](https://github.com/rokam/midea-local/issues/307)) ([f65b6ac](https://github.com/rokam/midea-local/commit/f65b6ac8fcc8ff2ae7085068498b96066213b658))

## [4.0.0](https://github.com/rokam/midea-local/compare/v3.0.1...v4.0.0) (2024-09-29)


### ⚠ BREAKING CHANGES

* **device:** rollback and improve send/recv socket exception ([#304](https://github.com/rokam/midea-local/issues/304))

### Bug Fixes

* **device:** rollback and improve send/recv socket exception ([#304](https://github.com/rokam/midea-local/issues/304)) ([7083464](https://github.com/rokam/midea-local/commit/7083464bba91e2f341d09de3b90b6bc77ccac9cb))

## [3.0.1](https://github.com/rokam/midea-local/compare/v3.0.0...v3.0.1) (2024-09-21)


### Bug Fixes

* **device:** prevent while true loop high cpu usage bug ([#298](https://github.com/rokam/midea-local/issues/298)) ([3bdec5c](https://github.com/rokam/midea-local/commit/3bdec5cbbad960d4fbc5b9a5520fa7c9219fe405))

## [3.0.0](https://github.com/rokam/midea-local/compare/v2.7.1...v3.0.0) (2024-09-20)


### ⚠ BREAKING CHANGES

* **device:** socket exception and process rebuild ([#296](https://github.com/rokam/midea-local/issues/296))

### Bug Fixes

* **device:** socket exception and process rebuild ([#296](https://github.com/rokam/midea-local/issues/296)) ([7f2e572](https://github.com/rokam/midea-local/commit/7f2e57294802d6ecae64618d28d1659465077672))

## [2.7.1](https://github.com/rokam/midea-local/compare/v2.7.0...v2.7.1) (2024-09-12)


### Bug Fixes

* ed device power/lock return message set and body_type 0x15 parse ([#284](https://github.com/rokam/midea-local/issues/284)) ([d9d4fac](https://github.com/rokam/midea-local/commit/d9d4faca3bf7a3096f1e12a53dd5953b79f2a422))

## [2.7.0](https://github.com/rokam/midea-local/compare/v2.6.3...v2.7.0) (2024-08-21)


### Features

* **cli:** use of preset account if cloud info missing ([#278](https://github.com/rokam/midea-local/issues/278)) ([84293bf](https://github.com/rokam/midea-local/commit/84293bfd86b9bb55f59b6897ff5d356df51f7fdb))


### Bug Fixes

* **cloud:** meiju cloud download_lua appliance_type error ([#281](https://github.com/rokam/midea-local/issues/281)) ([54f1bf4](https://github.com/rokam/midea-local/commit/54f1bf4a812c44590d9e01e9cd91c4c0f1768948))

## [2.6.3](https://github.com/rokam/midea-local/compare/v2.6.2...v2.6.3) (2024-08-13)


### Bug Fixes

* body_type default value is zero and not None ([#271](https://github.com/rokam/midea-local/issues/271)) ([bf6b4f0](https://github.com/rokam/midea-local/commit/bf6b4f0d0548bf495339cf793acd30673634f6d1))
* **c3:** silent level as string ([#270](https://github.com/rokam/midea-local/issues/270)) ([c851e33](https://github.com/rokam/midea-local/commit/c851e33dc9e8f7bb5a2f7d49f2e7c557d3a7151f))

## [2.6.2](https://github.com/rokam/midea-local/compare/v2.6.1...v2.6.2) (2024-08-10)


### Bug Fixes

* **cli:** discover must return a list ([#266](https://github.com/rokam/midea-local/issues/266)) ([345794b](https://github.com/rokam/midea-local/commit/345794b1241c149c172c117412ed48707daff6b9))

## [2.6.1](https://github.com/rokam/midea-local/compare/v2.6.0...v2.6.1) (2024-08-09)


### Bug Fixes

* **c3:** silent typo ([#265](https://github.com/rokam/midea-local/issues/265)) ([97defcd](https://github.com/rokam/midea-local/commit/97defcdc100424992c0f2bc7d4797cbbb6825076))
* **cli:** authenticate on discover v3 device ([#263](https://github.com/rokam/midea-local/issues/263)) ([05b0b11](https://github.com/rokam/midea-local/commit/05b0b11d98a3435373742c2cf50142f618700ed1))

## [2.6.0](https://github.com/rokam/midea-local/compare/v2.5.0...v2.6.0) (2024-08-02)


### Features

* parse all the response items from MeijuCloud for get_device_inf ([#231](https://github.com/rokam/midea-local/issues/231)) ([1976eb6](https://github.com/rokam/midea-local/commit/1976eb63578698d2b9a745a92c9c61a887219e0d))


### Bug Fixes

* **cli:** authenticate to get keys ([#256](https://github.com/rokam/midea-local/issues/256)) ([a017e7a](https://github.com/rokam/midea-local/commit/a017e7af46130266226f6c9a100b05703dd6cb5c))
* tank is always seen as full ([#255](https://github.com/rokam/midea-local/issues/255)) ([3524405](https://github.com/rokam/midea-local/commit/3524405fd36131deb83c9ded236eb686860f58c2))

## [2.5.0](https://github.com/rokam/midea-local/compare/v2.4.0...v2.5.0) (2024-07-30)


### Features

* **40:** add `precision_halves` customization ([#248](https://github.com/rokam/midea-local/issues/248)) ([8f5ec79](https://github.com/rokam/midea-local/commit/8f5ec79fe859ad88519360353cd3b6e159200625))
* **b8:** first implementation ([#225](https://github.com/rokam/midea-local/issues/225)) ([259e4f2](https://github.com/rokam/midea-local/commit/259e4f2f715b38a280789530941acc53d98beca4))


### Bug Fixes

* `break` the loop when connected ([#244](https://github.com/rokam/midea-local/issues/244)) ([536f975](https://github.com/rokam/midea-local/commit/536f975b93a3d68466a1bfa5a7c152570121531e))
* **ac:** correct attributes based on msg type ([#251](https://github.com/rokam/midea-local/issues/251)) ([fada9bc](https://github.com/rokam/midea-local/commit/fada9bc5fcc4158a6315566b8e9372c8805e21b4))
* **cloud:** fix email obfuscation ([#245](https://github.com/rokam/midea-local/issues/245)) ([ad9f278](https://github.com/rokam/midea-local/commit/ad9f278c7284e7e80285d66adc8320bb944f1162))

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

local bit = require "bit"
local VALUE_VERSION = 7
local JSON = require "cjson"
local VALUE_ON = "on"
local VALUE_OFF = "off"
local function getBit(oneByte, bitIndex)
    local bitBandList = {0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80}
    if bitIndex >= 0 and bitIndex <= 7 then
        if bit.band(oneByte, bitBandList[bitIndex + 1]) ==
            bitBandList[bitIndex + 1] then
            return '1'
        else
            return '0'
        end
    end
    return '2'
end
local function setBit(oneByte, bitIndex, value)
    local bitBorList = {0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80}
    local bitBandList = {0xFE, 0xFD, 0xFB, 0xF7, 0xEF, 0xDF, 0xBF, 0x7F}
    if bitIndex >= 0 and bitIndex <= 7 then
        if value == '1' then
            oneByte = bit.bor(oneByte, bitBorList[bitIndex + 1])
        elseif value == '0' then
            oneByte = bit.band(oneByte, bitBandList[bitIndex + 1])
        end
    end
    return oneByte
end
local function getNumber(x)
    local t = type(x)
    local rs = x
    if (t == "number") then
    elseif (t == "string") then
        rs = tonumber(x) or x
    end
    return rs
end
local function jsonToCmd(json, cmd)
    local query = json["query"]
    local ctrl = json["control"]
    if (ctrl) then
        if (ctrl.electronic_control_version == nil or
            ctrl.electronic_control_version == 1) then
            cmd[10] = 0x02
            cmd[11] = 0x22
            if (ctrl["gear_inc"] or ctrl["volume_inc"]) then
                cmd[12] = 0x02
                if (ctrl["gear_inc"]) then
                    cmd[13] = 0x00
                    local inc = getNumber(ctrl["gear_inc"]);
                    if (inc < 0x00) then
                        inc = inc + 0xFF + 0x01
                    end
                    cmd[14] = inc
                end
                if (ctrl["volume_inc"]) then
                    local inc = getNumber(ctrl["volume_inc"]);
                    if (inc < 0x00) then
                        inc = inc + 0xFF + 0x01
                    end
                    cmd[13] = inc
                    cmd[14] = 0x00
                end
            else
                cmd[12] = 0x01
                cmd[13] = 0xff
                cmd[14] = 0xff
                cmd[15] = 0xff
                cmd[16] = 0xff
                cmd[17] = 0xff
                cmd[18] = 0xff
                cmd[19] = 0xff
                cmd[20] = 0xff
                if (ctrl["light"]) then
                    if (ctrl["light"] == VALUE_ON) then
                        cmd[13] = 0x1a
                        if (ctrl["lightness"]) then
                            local lightness = getNumber(ctrl["lightness"])
                            if (lightness ~= 0x00) then
                                cmd[13] = lightness
                            end
                        end
                    elseif (ctrl["light"] == VALUE_OFF) then
                        cmd[13] = 0x00
                    end
                end
                if (ctrl["power"]) then
                    if (ctrl["power"] == VALUE_ON) then
                        cmd[14] = 0x02
                        cmd[15] = 0x02
                    elseif (ctrl["power"] == VALUE_OFF) then
                        cmd[14] = 0x03
                    elseif (ctrl["power"] == "delay_off") then
                        cmd[14] = 0x00
                    end
                end
                if (ctrl["gear"]) then
                    local gear = getNumber(ctrl["gear"])
                    if (gear ~= 0x00) then
                        cmd[14] = 0x02
                        cmd[15] = gear
                    else
                        cmd[14] = 0x03
                    end
                end
                if (ctrl["ir"]) then
                    if (ctrl["ir"] == VALUE_ON) then
                        cmd[16] = 0x03
                    elseif (ctrl["ir"] == VALUE_OFF) then
                        cmd[16] = 0x02
                    end
                end
                if (ctrl["speak"]) then
                    if (ctrl["speak"] == VALUE_ON) then
                        cmd[16] = 0x05
                    elseif (ctrl["speak"] == VALUE_OFF) then
                        cmd[16] = 0x04
                    end
                end
                if (ctrl["gesture"]) then
                    if (ctrl["gesture"] == VALUE_ON) then
                        cmd[16] = 0x09
                    elseif (ctrl["gesture"] == VALUE_OFF) then
                        cmd[16] = 0x08
                    end
                end
                if (ctrl["linkage"]) then
                    if (ctrl["linkage"] == VALUE_ON) then
                        cmd[16] = 0x11
                    elseif (ctrl["linkage"] == VALUE_OFF) then
                        cmd[16] = 0x10
                    end
                end
                if (ctrl["smoke_detector"]) then
                    if (ctrl["smoke_detector"] == VALUE_ON) then
                        cmd[16] = 0x21
                    elseif (ctrl["smoke_detector"] == VALUE_OFF) then
                        cmd[16] = 0x20
                    end
                end
                if (ctrl["steaming"]) then
                    if (ctrl["steaming"] == VALUE_ON) then
                        cmd[14] = 0x04
                    elseif (ctrl["steaming"] == VALUE_OFF) then
                        cmd[14] = 0x05
                    end
                end
                if (ctrl["one_key_start"] == VALUE_ON) then
                    cmd[14] = 0x06
                    cmd[15] = 0x02
                end
                if (ctrl["aidry"]) then
                    if (ctrl["aidry"] == VALUE_ON) then
                        cmd[14] = 0x02
                        cmd[15] = 0x15
                    elseif (ctrl["aidry"] == VALUE_OFF) then
                        cmd[14] = 0x03
                    end
                end
            end
        elseif (ctrl.electronic_control_version == 2) then
            cmd[10] = 0x02
            cmd[11] = 0x11
            if (ctrl.type == 'b6') then
                cmd[12] = 0x01
                if (ctrl.b6_action == "control") then
                    cmd[13] = 0x01
                    cmd[14] = 0xff
                    if (ctrl.wind_type) then
                        cmd[14] = getNumber(ctrl.wind_type)
                    end
                    cmd[15] = 0xff
                    if (ctrl.power == 'on' or ctrl.work_status == "working") then
                        cmd[15] = 0x02
                        cmd[16] = 0x02
                    elseif (ctrl.power == 'off' or ctrl.work_status ==
                        "power_off") then
                        cmd[15] = 0x01
                    elseif (ctrl.power == 'delay_off' or ctrl.work_status ==
                        "power_off_delay") then
                        cmd[15] = 0x03
                        cmd[16] = 0x01
                    elseif (ctrl.steaming == 'on' or ctrl.work_status ==
                        "hotclean") then
                        cmd[15] = 0x04
                        cmd[16] = 0x01
                    elseif (ctrl.steaming == 'off') then
                        cmd[15] = 0x04
                        cmd[16] = 0x03
                    elseif (ctrl.inverter == 'on') then
                        cmd[15] = 0x08
                        cmd[16] = 0x01
                    elseif (ctrl.inverter == 'off') then
                        cmd[15] = 0x08
                        cmd[16] = 0x02
                    elseif (ctrl.mute == 'on') then
                        cmd[15] = 0x09
                        cmd[16] = 0x01
                    elseif (ctrl.mute == 'off') then
                        cmd[15] = 0x09
                        cmd[16] = 0x02
                    elseif (ctrl.aidry == 'on') then
                        cmd[15] = 0x0a
                        cmd[16] = 0x01
                    elseif (ctrl.aidry == 'off') then
                        cmd[15] = 0x0a
                        cmd[16] = 0x02
                    end
                    if (ctrl.gear ~= nil) then
                        cmd[15] = 0x02
                        cmd[16] = getNumber(ctrl.gear)
                        if (cmd[16] == 0x00) then
                            cmd[15] = 0x01
                        end
                    end
                elseif (ctrl.b6_action == "setting") then
                    cmd[13] = 0x02
                    cmd[14] = 0xff
                    cmd[15] = 0xff
                    if (ctrl.setting == "power_off_delay") then
                        cmd[16] = 0xff
                        cmd[17] = 0xff
                        if (ctrl.power_off_delay_timevalue and
                            getNumber(ctrl.power_off_delay_timevalue) == 0) then
                            cmd[14] = 0x01
                            cmd[15] = 0x00
                        elseif (ctrl.power_off_delay_timevalue and
                            getNumber(ctrl.power_off_delay_timevalue) ~= 0) then
                            cmd[14] = 0x01
                            cmd[15] = 0x01
                            cmd[16] = getNumber(ctrl.power_off_delay_timevalue)
                        end
                        if (ctrl.power_off_delay_gearvalue and
                            getNumber(ctrl.power_off_delay_gearvalue) ~= 0) then
                            cmd[17] = getNumber(ctrl.power_off_delay_gearvalue)
                        end
                    elseif (ctrl.setting == "light") then
                        cmd[14] = 0x02
                        cmd[15] = 0xff
                        cmd[16] = 0xff
                        cmd[17] = 0xff
                        cmd[18] = 0xff
                        if (ctrl.light and ctrl.light == "on") then
                            cmd[15] = 0x01
                        elseif (ctrl.light and ctrl.light == "off") then
                            cmd[15] = 0x00
                        end
                        if (ctrl.lightness) then
                            cmd[16] = getNumber(ctrl.lightness)
                        end
                        if (ctrl.light_on_setting) then
                            if (getNumber(ctrl.light_on_setting) == 0x00) then
                                cmd[18] = 0x01
                            elseif (getNumber(ctrl.light_on_setting) == 0x01) then
                                cmd[18] = 0x01
                            elseif (getNumber(ctrl.light_on_setting) == 0x02) then
                                cmd[18] = 0x02
                            end
                        end
                        if (ctrl.light_off_setting) then
                            if (getNumber(ctrl.light_off_setting) == 0x00) then
                                cmd[18] = 0x10
                            elseif (getNumber(ctrl.light_off_setting) == 0x01) then
                                cmd[18] = 0x10
                            elseif (getNumber(ctrl.light_off_setting) == 0x02) then
                                cmd[18] = 0x20
                            end
                        end
                    elseif (ctrl.setting == "gesture") then
                        cmd[14] = 0x03
                        cmd[15] = 0xff
                        cmd[16] = 0xff
                        cmd[17] = 0xff
                        if (ctrl.gesture == VALUE_ON) then
                            cmd[15] = 0x01
                        elseif (ctrl.gesture == VALUE_OFF) then
                            cmd[15] = 0x00
                        end
                        if (ctrl.gesture_value and getNumber(ctrl.gesture_value) ~=
                            0) then
                            cmd[16] = ctrl.gesture_value
                        end
                        if (ctrl.gesture_sensitivity_value and
                            getNumber(ctrl.gesture_sensitivity_value) ~= 0) then
                            cmd[17] = ctrl.gesture_sensitivity_value
                        end
                    elseif (ctrl.setting == "smoke_detector") then
                        if (ctrl.smoke_detector_value and
                            getNumber(ctrl.smoke_detector_value) == 0) then
                            cmd[14] = 0x04
                            cmd[15] = 0x00
                            cmd[16] = 0xff
                        elseif (ctrl.smoke_detector_value and
                            getNumber(ctrl.smoke_detector_value) ~= 0) then
                            cmd[14] = 0x04
                            cmd[15] = 0x01
                            cmd[16] = getNumber(ctrl.smoke_detector_value)
                        end
                    elseif (ctrl.setting == "ir") then
                        cmd[14] = 0x05
                        cmd[15] = 0xff
                        cmd[16] = 0xff
                        if (ctrl.ir == VALUE_ON) then
                            cmd[15] = 0x01
                        elseif (ctrl.ir == VALUE_OFF) then
                            cmd[15] = 0x00
                        end
                        if (ctrl.ir_value and getNumber(ctrl.ir_value) ~= 0) then
                            cmd[16] = ctrl.ir_value
                        end
                    elseif (ctrl.setting == "tvoc") then
                        cmd[14] = 0x07
                        cmd[15] = 0xff
                        if (ctrl.tvoc and ctrl.tvoc == "on") then
                            cmd[15] = 0x01
                        elseif (ctrl.tvoc and ctrl.tvoc == "off") then
                            cmd[15] = 0x00
                        end
                    elseif (ctrl.setting == "linkage") then
                        cmd[14] = 0x08
                        cmd[15] = 0xff
                        if (ctrl.linkage and ctrl.linkage == "on") then
                            cmd[15] = 0x01
                        elseif (ctrl.linkage and ctrl.linkage == "off") then
                            cmd[15] = 0x00
                        end
                    elseif (ctrl.setting == "stove_select") then
                        cmd[14] = 0x09
                        cmd[15] = 0xff
                        if (ctrl.stove_select and ctrl.stove_select == "left") then
                            cmd[15] = 0x01
                        elseif (ctrl.stove_select and ctrl.stove_select ==
                            "right") then
                            cmd[15] = 0x02
                        end
                    elseif (ctrl.setting == "stove_time_length") then
                        cmd[14] = 0x0A
                        cmd[15] = 0x00
                        cmd[16] = 0x00
                        if (ctrl.stove_time_length and
                            getNumber(ctrl.stove_time_length) ~= 0) then
                            cmd[16] = getNumber(ctrl.stove_time_length)
                        end
                    elseif (ctrl.setting == "automation") then
                        cmd[14] = 0x0B
                        cmd[15] = 0xff
                        if (ctrl.automation and ctrl.automation == "off") then
                            cmd[15] = 0x00
                        elseif (ctrl.automation and ctrl.automation == "on") then
                            cmd[15] = 0x01
                        end
                    elseif (ctrl.setting == "air_duct_detection") then
                        cmd[14] = 0x0C
                        cmd[15] = 0xff
                        if (ctrl.air_duct_detection and ctrl.air_duct_detection ==
                            "off") then
                            cmd[15] = 0x02
                        elseif (ctrl.air_duct_detection and
                            ctrl.air_duct_detection == "on") then
                            cmd[15] = 0x01
                        end
                    elseif (ctrl.setting == "ambient_light") then
                        cmd[14] = 0x0D
                        cmd[15] = 0xff
                        cmd[16] = 0xff
                        cmd[17] = 0xff
                        cmd[18] = 0xff
                        if (ctrl.ambient_light and ctrl.ambient_light == "on") then
                            cmd[15] = 0x01
                        elseif (ctrl.ambient_light and ctrl.ambient_light ==
                            "off") then
                            cmd[15] = 0x00
                        end
                        if (ctrl.ambient_lightness) then
                            cmd[16] = getNumber(ctrl.ambient_lightness)
                        end
                        if (ctrl.ambient_light_on_setting) then
                            if (getNumber(ctrl.ambient_light_on_setting) == 0x00) then
                                cmd[18] = 0x01
                            elseif (getNumber(ctrl.ambient_light_on_setting) ==
                                0x01) then
                                cmd[18] = 0x01
                            elseif (getNumber(ctrl.ambient_light_on_setting) ==
                                0x02) then
                                cmd[18] = 0x02
                            end
                        end
                        if (ctrl.ambient_light_off_setting) then
                            if (getNumber(ctrl.ambient_light_off_setting) ==
                                0x00) then
                                cmd[18] = 0x10
                            elseif (getNumber(ctrl.ambient_light_off_setting) ==
                                0x01) then
                                cmd[18] = 0x10
                            elseif (getNumber(ctrl.ambient_light_off_setting) ==
                                0x02) then
                                cmd[18] = 0x20
                            end
                        end
                    end
                end
            elseif (ctrl.type == 'b7') then
                cmd[12] = 0x02
                cmd[13] = 0xff
                if (ctrl.b7_work_burner_control ~= nil) then
                    cmd[13] = getNumber(ctrl.b7_work_burner_control)
                end
                cmd[14] = 0xff
                if (ctrl.b7_function_control ~= nil) then
                    cmd[14] = getNumber(ctrl.b7_function_control)
                end
                cmd[15] = 0xff
                cmd[16] = 0xff
                cmd[17] = 0xff
                cmd[18] = 0xff
                cmd[19] = 0xff
                if (cmd[14] == 2) then
                    if (cmd[13] == 1 and ctrl.b7_left_gear ~= nil) then
                        cmd[15] = getNumber(ctrl.b7_left_gear)
                    elseif (cmd[13] == 2 and ctrl.b7_right_gear ~= nil) then
                        cmd[15] = getNumber(ctrl.b7_right_gear)
                    elseif (cmd[13] == 3 and ctrl.b7_middle_gear ~= nil) then
                        cmd[15] = getNumber(ctrl.b7_middle_gear)
                    end
                    if (cmd[15] == 0x00) then cmd[14] = 0x01 end
                    if (cmd[13] == 1 and ctrl.b7_left_destination_time ~= nil) then
                        local seconds = getNumber(ctrl.b7_left_destination_time)
                        if (seconds < 256 * 256) then
                            cmd[16] = seconds % 256
                            cmd[17] = (seconds - cmd[16]) / 256
                        end
                    elseif (cmd[13] == 2 and ctrl.b7_right_destination_time ~=
                        nil) then
                        local seconds =
                            getNumber(ctrl.b7_right_destination_time)
                        if (seconds < 256 * 256) then
                            cmd[16] = seconds % 256
                            cmd[17] = (seconds - cmd[16]) / 256
                        end
                    elseif (cmd[13] == 3 and ctrl.b7_middle_destination_time ~=
                        nil) then
                        local minute =
                            getNumber(ctrl.b7_middle_destination_time)
                        if (minute < 256 * 256) then
                            cmd[17] = minute % 256
                            cmd[16] = (minute - cmd[17]) / 256
                        end
                    end
                elseif (cmd[14] == 3) then
                    cmd[15] = 0xff
                    if (cmd[13] == 1 and ctrl.b7_left_destination_time ~= nil) then
                        local minute = getNumber(ctrl.b7_left_destination_time)
                        if (minute < 256 * 256) then
                            cmd[17] = minute % 256
                            cmd[16] = (minute - cmd[17]) / 256
                        end
                    elseif (cmd[13] == 2 and ctrl.b7_right_destination_time ~=
                        nil) then
                        local minute = getNumber(ctrl.b7_right_destination_time)
                        if (minute < 256 * 256) then
                            cmd[17] = minute % 256
                            cmd[16] = (minute - cmd[17]) / 256
                        end
                    elseif (cmd[13] == 3 and ctrl.b7_middle_destination_time ~=
                        nil) then
                        local minute =
                            getNumber(ctrl.b7_middle_destination_time)
                        if (minute < 256 * 256) then
                            cmd[17] = minute % 256
                            cmd[16] = (minute - cmd[17]) / 256
                        end
                    end
                elseif (cmd[14] == 4) then
                    cmd[18] = 0x00
                    cmd[19] = 0x00
                    if (cmd[13] == 1 and ctrl.b7_left_destination_temp ~= nil) then
                        local seconds = getNumber(ctrl.b7_left_destination_temp)
                        if (seconds < 256 * 256) then
                            cmd[16] = seconds % 256
                            cmd[17] = (seconds - cmd[16]) / 256
                        end
                    elseif (cmd[13] == 2 and ctrl.b7_right_destination_temp ~=
                        nil) then
                        local seconds =
                            getNumber(ctrl.b7_right_destination_temp)
                        if (seconds < 256 * 256) then
                            cmd[16] = seconds % 256
                            cmd[17] = (seconds - cmd[16]) / 256
                        end
                    elseif (cmd[13] == 3 and ctrl.b7_middle_destination_temp ~=
                        nil) then
                        local temp = getNumber(ctrl.b7_middle_destination_temp)
                        if (temp < 256 * 256) then
                            cmd[17] = temp % 256
                            cmd[16] = (temp - cmd[17]) / 256
                        end
                    end
                end
            end
        end
    elseif (query) then
        cmd[10] = 0x03
        if (query.tips) then
            cmd[11] = 0x32
            cmd[12] = 0x01
        else
            if (query.electronic_control_version == nil or
                query.electronic_control_version == 1) then
                cmd[11] = 0x31
            elseif (query.electronic_control_version == 2) then
                cmd[11] = 0x11
            end
        end
    end
    return cmd
end
local function getPackage(position, cmd)
    local pkg = {}
    local i = 1
    while (i <= cmd[position + 1]) do
        pkg[i] = cmd[position + 1 + i]
        i = i + 1
    end
    return pkg
end
local function getB6Json(json, pkg)
    if (pkg[1] == nil) then return json; end
    if (pkg[2] ~= 0xff) then
        json.steaming = "off"
        json.power = VALUE_ON
        json.inverter = VALUE_OFF
        json.mute = VALUE_OFF
        json.aidry = VALUE_OFF
        json.air_duct_detection = VALUE_OFF
        if (pkg[2] == 0x00) then
            json.power = VALUE_OFF
            json.work_status_desc = "initial"
        elseif (pkg[2] == 0x01) then
            json.power = VALUE_OFF
            json.work_status_desc = "power_off"
        elseif (pkg[2] == 0x02) then
            json.work_status_desc = "working"
        elseif (pkg[2] == 0x03) then
            json.power = "delay_off"
            json.work_status_desc = "power_off_delay"
        elseif (pkg[2] == 0x04) then
            json.steaming = "on"
            json.work_status_desc = "hotclean"
        elseif (pkg[2] == 0x05) then
            json.power = VALUE_OFF
            json.work_status_desc = "error"
        elseif (pkg[2] == 0x06) then
            json.work_status_desc = "clean"
        elseif (pkg[2] == 0x07) then
            json.power = VALUE_OFF
            json.work_status_desc = "check"
        elseif (pkg[2] == 0x08) then
            json.work_status_desc = "vvvf_gear"
            json.inverter = VALUE_ON
        elseif (pkg[2] == 0x09) then
            json.work_status_desc = "mute_gear"
            json.mute = VALUE_ON
        elseif (pkg[2] == 0x0a) then
            json.work_status_desc = "aidry"
            json.aidry = VALUE_ON
        elseif (pkg[2] == 0x0C) then
            json.work_status_desc = "air_duct_detection"
            json.air_duct_detection = VALUE_ON
        end
    end
    if (pkg[3] ~= 0xff) then json.gear = pkg[3] end
    if (pkg[4] ~= 0xff) then json.hotclean_minutes = pkg[4] end
    if (pkg[5] ~= 0xff) then json.hotclean_stage = pkg[5] end
    if (pkg[6] ~= 0xff) then json.hotclean_remaining_minutes = pkg[6] end
    if (pkg[7] ~= 0xff) then
        if (pkg[7] == 0x00) then
            json.light = VALUE_OFF
        else
            json.light = VALUE_ON
        end
    end
    if (pkg[8] ~= 0xff) then json.lightness = pkg[8] end
    if (pkg[9] ~= 0xff) then
        json.light_on_setting = getNumber(pkg[9]) % 16
        json.light_off_setting = math.floor(getNumber(pkg[9]) / 16)
    end
    if (pkg[11] ~= 0xff) then
        if (pkg[11] <= 0x03) then
            json.smoke_detector = VALUE_OFF
            json.smoke_detector_value = 0
        else
            json.smoke_detector = VALUE_ON
            json.smoke_detector_value = getNumber(pkg[11]) % 16
        end
    end
    if (pkg[12] ~= 0xff) then
        if (pkg[12] <= 0x03) then
            json.ir = VALUE_OFF
            json.ir_value = 0
        else
            json.ir = VALUE_ON
            json.ir_value = getNumber(pkg[12]) % 16
        end
    end
    if (pkg[13] ~= 0xff) then
        if (pkg[13] == 0x00) then
            json.linkage = VALUE_OFF
        else
            json.linkage = VALUE_ON
        end
    end
    if (pkg[14] ~= 0xff) then
        if (pkg[14] < 0x80) then
            json.gesture = VALUE_OFF
            json.gesture_value = getNumber(pkg[14]) % 16
            json.gesture_sensitivity_value = math.floor(getNumber(pkg[14]) / 16)
        else
            json.gesture = VALUE_ON
            json.gesture_value = getNumber(pkg[14]) % 16
            json.gesture_sensitivity_value =
                math.floor(getNumber(pkg[14]) / 16) - 8
        end
    end
    if (pkg[15] ~= 0xff) then json.destination_time = pkg[15] end
    if (pkg[16] ~= 0xff) then json.remaining_time = pkg[16] end
    if (pkg[17] ~= 0xff) then
        json.total_working_time = pkg[17] * 256 + pkg[18]
    end
    json.oilcup_position = getBit(pkg[19], 2)
    json.hotclean_tips = getBit(pkg[19], 2)
    json.is_error = getBit(pkg[19], 7)
    json.error_type = "none"
    json.error_eq = "none"
    if (json.hotclean_tips == "1") then
        json.error_type = "tips"
        json.error_eq = "robam"
    end
    if (json.is_error == "1") then
        json.error_type = "error"
        json.error_eq = "robam"
    end
    json.error_code = pkg[20]
    if (pkg[25] and pkg[25] ~= 0xff) then
        if (pkg[25] < 0x80) then
            json.tvoc = VALUE_OFF
            json.tvoc_value = 0
        else
            json.tvoc = VALUE_ON
            json.tvoc_value = getNumber(pkg[25]) % 16
        end
    end
    if (pkg[28] ~= nil and pkg[29] ~= nil and pkg[28] ~= 0xff) then
        json.wind_pressure = pkg[28] * 256 + pkg[29]
    end
    if (pkg[31] and pkg[31] ~= 0xff) then
        if (pkg[31] == 1) then
            json.stove_select = "left"
        elseif (pkg[31] == 2) then
            json.stove_select = "right"
        end
    end
    if (pkg[32] and pkg[32] ~= 0xff) then json.stove_time_length = pkg[32] end
    if (pkg[33] and pkg[33] ~= 0xff) then json.stove_matched = pkg[33] end
    if (pkg[34] and pkg[34] ~= 0xff) then
        if (pkg[34] == 1) then
            json.automation = "on"
        elseif (pkg[34] == 2) then
            json.automation = "off"
        end
    end
    if (pkg[35] and pkg[36] and pkg[35] ~= 0xff) then
        json.temperature = pkg[35] * 256 + pkg[36]
    end
    if (pkg[37] and pkg[38] and pkg[37] ~= 0xff) then
        json.humidity = pkg[37] * 256 + pkg[38]
    end
    if (pkg[39] and pkg[40] and pkg[41] and pkg[39] ~= 0xff) then
        if (pkg[39] ~= 0xff) then
            if (pkg[39] == 0x00) then
                json.ambient_light = VALUE_OFF
            else
                json.ambient_light = VALUE_ON
            end
        end
        if (pkg[40] ~= 0xff) then json.ambient_lightness = pkg[40] end
        if (pkg[41] ~= 0xff) then
            json.ambient_light_on_setting = getNumber(pkg[41]) % 16
            json.ambient_light_off_setting = math.floor(getNumber(pkg[41]) / 16)
        end
    end
    return json
end
local function getB7Json(json, pkg)
    if (pkg[1] == nil) then return json; end
    if (pkg[1] == 0x01) then
        if (pkg[2] == 0x00) then
            json.b7_left_status = "initial"
        elseif (pkg[2] == 0x01) then
            json.b7_left_status = "power_off"
        elseif (pkg[2] == 0x02) then
            json.b7_left_status = "working"
        elseif (pkg[2] == 0x03) then
            json.b7_left_status = "power_off_delay"
        elseif (pkg[2] == 0x04) then
            json.b7_left_status = "temp"
        end
        json.b7_left_gear = pkg[3]
        json.b7_left_destination_time = 0
        if (pkg[4] ~= 0xff and pkg[5] ~= 0xff) then
            json.b7_left_destination_time = pkg[4] * 256 + pkg[5]
        end
        if (pkg[6] ~= 0xff and pkg[7] ~= 0xff) then
            json.b7_left_remaining_time = pkg[6] * 256 + pkg[7]
            if (json.b7_left_remaining_time > 0) then
                json.b7_left_status = "power_off_delay"
            end
        end
        if (pkg[8] ~= 0xff and pkg[9] ~= 0xff) then
            json.b7_left_work_time = pkg[8] * 256 + pkg[9]
        end
        json.b7_left_sensor = 0
        json.b7_gas_leakage_code = 0
        if (pkg[10] ~= 0xff) then
            json.b7_left_sensor = pkg[10]
            json.b7_gas_leakage_code = getNumber(getBit(pkg[10], 2))
        end
        if (pkg[11] ~= 0xff) then json.b7_vbatt = (pkg[11] + 100) * 10 end
    elseif (pkg[1] == 0x02) then
        if (pkg[2] == 0x00) then
            json.b7_right_status = "initial"
        elseif (pkg[2] == 0x01) then
            json.b7_right_status = "power_off"
        elseif (pkg[2] == 0x02) then
            json.b7_right_status = "working"
        elseif (pkg[2] == 0x03) then
            json.b7_right_status = "power_off_delay"
        elseif (pkg[2] == 0x04) then
            json.b7_right_status = "temp"
        end
        json.b7_right_gear = pkg[3]
        json.b7_right_destination_time = 0
        if (pkg[4] ~= 0xff and pkg[5] ~= 0xff) then
            json.b7_right_destination_time = pkg[4] * 256 + pkg[5]
        end
        if (pkg[6] ~= 0xff and pkg[7] ~= 0xff) then
            json.b7_right_remaining_time = pkg[6] * 256 + pkg[7]
            if (json.b7_right_remaining_time > 0) then
                json.b7_right_status = "power_off_delay"
            end
        end
        if (pkg[8] ~= 0xff and pkg[9] ~= 0xff) then
            json.b7_right_work_time = pkg[8] * 256 + pkg[9]
        end
        json.b7_right_sensor = 0
        json.b7_gas_leakage_code = 0
        if (pkg[10] ~= 0xff) then
            json.b7_right_sensor = pkg[10]
            json.b7_gas_leakage_code = getNumber(getBit(pkg[10], 2))
        end
        if (pkg[11] ~= 0xff) then json.b7_vbatt = (pkg[11] + 100) * 10 end
    elseif (pkg[1] == 0x03) then
        if (pkg[2] == 0x00) then
            json.b7_middle_status = "initial"
        elseif (pkg[2] == 0x01) then
            json.b7_middle_status = "power_off"
        elseif (pkg[2] == 0x02) then
            json.b7_middle_status = "working"
        elseif (pkg[2] == 0x03) then
            json.b7_middle_status = "power_off_delay"
        elseif (pkg[2] == 0x04) then
            json.b7_middle_status = "temp"
        end
        json.b7_middle_gear = pkg[3]
        json.b7_middle_destination_time = 0
        if (pkg[4] ~= 0xff and pkg[5] ~= 0xff) then
            json.b7_middle_destination_time = pkg[4] * 256 + pkg[5]
        end
        if (pkg[6] ~= 0xff and pkg[7] ~= 0xff) then
            json.b7_middle_remaining_time = pkg[6] * 256 + pkg[7]
            if (json.b7_middle_remaining_time > 0) then
                json.b7_middle_status = "power_off_delay"
            end
        end
        if (pkg[8] ~= 0xff and pkg[9] ~= 0xff) then
            json.b7_middle_work_time = pkg[8] * 256 + pkg[9]
        end
        json.b7_middle_sensor = 0
        json.b7_gas_leakage_code = 0
        if (pkg[10] ~= 0xff) then
            json.b7_middle_sensor = pkg[10]
            json.b7_gas_leakage_code = getNumber(getBit(pkg[10], 2))
        end
        if (pkg[11] ~= 0xff) then json.b7_vbatt = (pkg[11] + 100) * 10 end
    end
    return json
end
local function getAirJson(json, pkg)
    if (pkg[1] == nil) then return json; end
    json.air_duct_detection_time = pkg[1] + pkg[2] * 256
    json.air_duct_detection_score = pkg[3]
    json.air_duct_detection_windage = pkg[4]
    json.air_duct_detection_state = pkg[5]
    return json
end
local function queryAllCmdToJson(json, cmd)
    if (cmd[9] == 0 or cmd[9] == 1) then
        if (cmd[12] ~= 0xff) then
            if (cmd[12] == 0x00) then
                json["light"] = VALUE_OFF
            else
                json["light"] = VALUE_ON
                json["lightness"] = cmd[12]
            end
        end
        json["work_status"] = cmd[13]
        if (cmd[13] ~= 0xFF) then
            if (cmd[13] == 0x00 or cmd[13] == 0x01) then
                json["power"] = VALUE_OFF
                json["work_status_desc"] = "power_off"
            elseif (cmd[13] == 0x02 or cmd[13] == 0x06 or cmd[13] == 0x07 or
                cmd[13] == 0x14 or cmd[13] == 0x15 or cmd[13] == 0x16) then
                json["power"] = VALUE_ON
                json["work_status_desc"] = "working"
                if (cmd[13] == 0x06) then
                    json["work_status_desc"] = 'hotclean'
                elseif (cmd[13] == 0x07) then
                    json["work_status_desc"] = 'clean'
                elseif (cmd[13] == 0x14 or cmd[13] == 0x15 or cmd[13] == 0x16) then
                    json["gear"] = cmd[13]
                    json["gear_detail"] = cmd[14]
                end
            elseif (cmd[13] == 0x03) then
                json["power"] = "delay_off"
                json["work_status_desc"] = "power_off_delay"
                json["power_delay"] = 0x03
            elseif (cmd[13] == 0x0a) then
                json["power"] = VALUE_OFF
                json["work_status_desc"] = "power_off"
                json["is_error"] = "1"
            end
        end
        if (json["gear"] == nil and cmd[14] ~= 0xff) then
            json["gear"] = cmd[14]
        end
        json["oilcup_position"] = getBit(cmd[16], 1)
        json["hotclean_tips"] = getBit(cmd[16], 2)
        json["is_error"] = getBit(cmd[16], 7)
        if (getBit(cmd[24], 0) == "0") then
            json["ir"] = VALUE_OFF
        elseif (getBit(cmd[24], 0) == "1") then
            json["ir"] = VALUE_ON
        end
        if (getBit(cmd[24], 1) == "0") then
            json["speak"] = VALUE_OFF
        elseif (getBit(cmd[24], 1) == "1") then
            json["speak"] = VALUE_ON
        end
        if (getBit(cmd[24], 2) == "0") then
            json["gesture"] = VALUE_OFF
        elseif (getBit(cmd[24], 2) == "1") then
            json["gesture"] = VALUE_ON
        end
        if (getBit(cmd[24], 3) == "0") then
            json["linkage"] = VALUE_OFF
        elseif (getBit(cmd[24], 3) == "1") then
            json["linkage"] = VALUE_ON
        end
        if (getBit(cmd[24], 4) == "0") then
            json["smoke_detector"] = VALUE_OFF
        elseif (getBit(cmd[24], 4) == "1") then
            json["smoke_detector"] = VALUE_ON
        end
        json.error_type = "none"
        json.error_eq = "none"
        if (json.hotclean_tips == "1") then
            json.error_type = "tips"
            json.error_eq = "robam"
        end
        if (json.is_error == "1") then
            json.error_type = "error"
            json.error_eq = "robam"
        end
        if (cmd[28] and cmd[28] ~= 0) then
            json["error_code"] = cmd[28]
            json.error_type = "error"
            json.error_eq = "robam"
        else
            json["error_code"] = 0
        end
        if (cmd[13] == 0x06 and cmd[32] and cmd[32] ~= 0xff) then
            json["hotclean_minutes"] = cmd[32]
        end
        if (cmd[13] == 0x16 and cmd[35] + cmd[36] ~= 0) then
            json["wind_pressure"] = cmd[35] * 256 + cmd[36]
        end
        json["volume"] = 0
        if (cmd[43] and cmd[43] ~= 0) then json["volume"] = cmd[43] end
        return json
    elseif (cmd[9] == 2) then
        local position = 12
        while (cmd[position + 1] ~= nil) do
            if (cmd[position] == 0x01) then
                json = getB6Json(json, getPackage(position, cmd))
            elseif (cmd[position] == 0x02) then
                json = getB7Json(json, getPackage(position, cmd))
            elseif (cmd[position] == 0x03) then
                json = getAirJson(json, getPackage(position, cmd))
            end
            position = position + cmd[position + 1] + 2
        end
        return json
    end
end
local function queryErrorCmdToJson(json, cmd)
    if (getBit(cmd[13], 2) == "1") then
        json["error_code"] = 1
        json.error_type = "error"
        json.error_eq = "robam"
    end
    if (getBit(cmd[14], 0) == "1") then
        json["error_code"] = 3
        json.error_type = "error"
        json.error_eq = "robam"
    end
    if (getBit(cmd[14], 1) == "1") then
        json["error_code"] = 7
        json.error_type = "error"
        json.error_eq = "robam"
    end
    if (cmd[15] ~= 0 or cmd[16] ~= 0) then
        json["error_code"] = 5
        json.error_type = "error"
        json.error_eq = "robam"
    end
    if (cmd[17] and md[17] ~= 0) then json["error_code"] = cmd[17] end
    return json
end
local function cmdToJson(json, cmd)
    json["version"] = VALUE_VERSION
    json["electronic_control_version"] = cmd[9]
    if (cmd[10] == 0x02) then
        if (cmd[11] == 0x22) then
            if (cmd[12] == 0x01) then
                if (cmd[13] ~= 0xff) then
                    if (cmd[13] == 0x00) then
                        json["light"] = VALUE_OFF
                    else
                        json["light"] = VALUE_ON
                        json["lightness"] = cmd[13]
                    end
                end
                if (cmd[14] ~= 0xFF) then
                    if (cmd[14] == 0x03 or cmd[14] == 0x01 or cmd[14] == 0x05) then
                        json["power"] = VALUE_OFF
                        json["work_status_desc"] = "power_off"
                        json["work_status"] = 0x01
                    elseif (cmd[14] == 0x02) then
                        json["power"] = VALUE_ON
                        json["work_status_desc"] = "working"
                        json["work_status"] = 0x02
                    elseif (cmd[14] == 0x00) then
                        json["power"] = "delay_off"
                        json["work_status_desc"] = "power_off_delay"
                        json["power_delay"] = 0x03
                        json["work_status"] = 0x03
                    elseif (cmd[14] == 0x04) then
                        json["power"] = VALUE_ON
                        json["work_status_desc"] = 'hotclean'
                        json["work_status"] = 0x06
                    end
                end
                if (cmd[15] ~= 0xff) then json["gear"] = cmd[15] end
                if (cmd[16] ~= 0xFF) then
                    if (cmd[16] == 0x02) then
                        json["ir"] = VALUE_OFF
                    elseif (cmd[16] == 0x03) then
                        json["ir"] = VALUE_ON
                    end
                    if (cmd[16] == 0x04) then
                        json["speak"] = VALUE_OFF
                    elseif (cmd[16] == 0x05) then
                        json["speak"] = VALUE_ON
                    end
                    if (cmd[16] == 0x06) then
                        json["gesture"] = VALUE_OFF
                    elseif (cmd[16] == 0x07) then
                        json["gesture"] = VALUE_ON
                    end
                    if (cmd[16] == 0x08) then
                        json["linkage"] = VALUE_OFF
                    elseif (cmd[16] == 0x09) then
                        json["linkage"] = VALUE_ON
                    end
                    if (cmd[16] == 0x0A) then
                        json["smoke_detector"] = VALUE_OFF
                    elseif (cmd[16] == 0x0B) then
                        json["smoke_detector"] = VALUE_ON
                    end
                end
            elseif (cmd[12] == 0x02) then
                if (cmd[13] ~= 0x00) then
                    if (cmd[13] >= 128) then
                        cmd[13] = cmd[13] - 0xff - 0x01
                    end
                    json["volume_inc"] = cmd[13]
                end
                if (cmd[14] ~= 0x00) then
                    if (cmd[14] >= 128) then
                        cmd[14] = cmd[14] - 0xff - 0x01
                    end
                    json["gear_inc"] = cmd[14]
                end
            elseif (cmd[12] == 0xFE) then
                json["ctrl_fail"] = "1"
                if (cmd[14] ~= 0x00) then
                    json["ctrl_fail_reason"] = cmd[14]
                end
            end
        elseif (cmd[11] == 0x11) then
            if (cmd[12] == 0x01) then
                if (cmd[13] == 0x01) then
                    if (cmd[15] == 0x01) then
                        json.power = VALUE_OFF
                        json.work_status_desc = "power_off"
                    elseif (cmd[15] == 0x02) then
                        json.power = VALUE_ON
                        json.work_status_desc = "working"
                        if (cmd[16] ~= 0xFF) then
                            json.gear = cmd[16]
                        end
                    elseif (cmd[15] == 0x03) then
                        json.power = 'delay_off'
                        json.work_status_desc = "power_off_delay"
                    elseif (cmd[15] == 0x04) then
                        if (cmd[16] == 0x01) then
                            json.steaming = VALUE_ON
                            json.work_status_desc = "hotclean"
                        elseif (cmd[16] == 0x03) then
                            json.steaming = VALUE_OFF
                            json.work_status_desc = "power_off"
                        end
                    elseif (cmd[15] == 0x06) then
                        if (cmd[16] == 0x01) then
                            json.clean = VALUE_ON
                            json.work_status_desc = "clean"
                        elseif (cmd[16] == 0x02) then
                            json.clean = VALUE_OFF
                            json.work_status_desc = "power_off"
                        end
                    elseif (cmd[15] == 0x08) then
                        json.power = VALUE_ON
                        json.inverter = VALUE_ON
                        json.work_status_desc = "vvvf_gear"
                    elseif (cmd[15] == 0x09) then
                        json.power = VALUE_ON
                        json.mute = VALUE_ON
                        json.work_status_desc = "mute_gear"
                    elseif (cmd[15] == 0x0a) then
                        json.power = VALUE_ON
                        json.aidry = VALUE_ON
                        json.work_status_desc = "aidry"
                    elseif (cmd[15] == 0x0c) then
                        json.air_duct_detection = VALUE_ON
                        json.work_status_desc = "air_duct_detection"
                    end
                elseif (cmd[13] == 0x02) then
                    if (cmd[14] == 0x01) then
                        if (cmd[15] == 0x00) then
                            json.power_off_delay_timevalue = 0x00
                        elseif (cmd[15] ~= 0x00) then
                            json.power_off_delay_timevalue = cmd[16]
                            if (cmd[17] ~= 0x00 and cmd[17] ~= 0xff) then
                                json.power_off_delay_gearvalue = cmd[17]
                            end
                        end
                    elseif (cmd[14] == 0x02) then
                        if (cmd[15] == 0x00) then
                            json.light = 'off'
                        elseif (cmd[15] ~= 0x00 and cmd[15] ~= 0xff) then
                            json.light = 'on'
                        end
                        if (cmd[16] ~= 0x00 and cmd[16] ~= 0xff) then
                            json.lightness = cmd[16]
                        end
                        if (cmd[18] ~= 0xff) then
                            json.light_on_setting = getNumber(cmd[18]) % 16
                            json.light_off_setting =
                                math.floor(getNumber(cmd[18]) / 16)
                        end
                    elseif (cmd[14] == 0x03) then
                        if (cmd[15] == 0x00) then
                            json.gesture = VALUE_OFF
                            json.gesture_value = 0x00
                        elseif (cmd[15] == 0x01) then
                            json.gesture = VALUE_ON
                            if (cmd[16] ~= 0x00 and cmd[16] ~= 0xff) then
                                json.gesture_value = cmd[16]
                            end
                            if (cmd[17] ~= 0x00 and cmd[17] ~= 0xff) then
                                json.gesture_sensitivity_value = cmd[17]
                            end
                        end
                    elseif (cmd[14] == 0x04) then
                        if (cmd[15] == 0x00) then
                            json.smoke_detector = VALUE_OFF
                            json.smoke_detector_value = 0x00
                        elseif (cmd[15] == 0x01) then
                            json.smoke_detector = VALUE_ON
                            if (cmd[16] ~= 0x00 and cmd[16] ~= 0xff) then
                                json.smoke_detector_value = cmd[16]
                            end
                        end
                    elseif (cmd[14] == 0x05) then
                        if (cmd[15] == 0x00) then
                            json.ir = VALUE_OFF
                            json.ir_value = 0x00
                        elseif (cmd[15] == 0x01) then
                            json.ir = VALUE_ON
                            if (cmd[16] ~= 0x00 and cmd[16] ~= 0xff) then
                                json.ir_value = cmd[16]
                            end
                        end
                    elseif (cmd[14] == 0x06) then
                    elseif (cmd[14] == 0x07) then
                        if (cmd[15] == 0x00) then
                            json.tvoc = 'off'
                        elseif (cmd[15] ~= 0x00) then
                            json.tvoc = 'on'
                        end
                    elseif (cmd[14] == 0x08) then
                        if (cmd[15] == 0x00) then
                            json.linkage = 'off'
                        elseif (cmd[15] ~= 0x00) then
                            json.linkage = 'on'
                        end
                    elseif (cmd[14] == 0x09) then
                        if (cmd[15] == 0x01) then
                            json.stove_select = 'left'
                        elseif (cmd[15] == 0x02) then
                            json.stove_select = 'right'
                        end
                    elseif (cmd[14] == 0x0A) then
                        if (cmd[15] ~= 0xFF and cmd[16] ~= 0xFF) then
                            json.stove_time_length = cmd[16]
                        end
                    elseif (cmd[14] == 0x0B) then
                        if (cmd[15] == 0x00) then
                            json.automation = 'off'
                        elseif (cmd[15] ~= 0x00) then
                            json.automation = 'on'
                        end
                    elseif (cmd[14] == 0x0C) then
                        if (cmd[15] == 0x00) then
                            json.air_duct_detection = 'off'
                        elseif (cmd[15] ~= 0x00) then
                            json.air_duct_detection = 'on'
                        end
                    elseif (cmd[14] == 0x0D) then
                        if (cmd[15] == 0x00) then
                            json.ambient_light = 'off'
                        elseif (cmd[15] ~= 0x00 and cmd[16] ~= 0xff) then
                            json.ambient_light = 'on'
                        end
                        if (cmd[16] ~= 0x00 and cmd[16] ~= 0xff) then
                            json.ambient_lightness = cmd[16]
                        end
                        if (cmd[18] ~= 0xff) then
                            json.ambient_light_on_setting =
                                getNumber(cmd[18]) % 16
                            json.ambient_light_off_setting = math.floor(
                                                                 getNumber(
                                                                     cmd[18]) /
                                                                     16)
                        end
                    end
                end
            elseif (cmd[12] == 0x02) then
                if (cmd[13] == 0x01) then
                    if (cmd[14] == 0x01) then
                        json.b7_left_status = "power_off"
                    elseif (cmd[14] == 0x02) then
                        json.b7_left_status = "working"
                    elseif (cmd[14] == 0x03) then
                        json.b7_left_status = "power_off_delay"
                        if (cmd[16] ~= 0xff) then
                            json.b7_left_destination_time = cmd[16] * 256 +
                                                                cmd[17]
                            json.b7_left_remaining_time =
                                json.b7_left_destination_time
                        end
                    elseif (cmd[14] == 0x04) then
                        json.b7_left_status = "temp"
                        if (cmd[16] ~= 0xff) then
                            json.b7_left_destination_temp = cmd[16] * 256 +
                                                                cmd[17]
                        end
                    end
                    if (cmd[15] ~= 0xff) then
                        json.b7_left_gear = cmd[15]
                    end
                elseif (cmd[13] == 0x02) then
                    if (cmd[14] == 0x01) then
                        json.b7_right_status = "power_off"
                    elseif (cmd[14] == 0x02) then
                        json.b7_right_status = "working"
                    elseif (cmd[14] == 0x03) then
                        json.b7_right_status = "power_off_delay"
                        if (cmd[16] ~= 0xff) then
                            json.b7_right_destination_time = cmd[16] * 256 +
                                                                 cmd[17]
                            json.b7_right_remaining_time =
                                json.b7_right_destination_time
                        end
                    elseif (cmd[14] == 0x04) then
                        json.b7_right_status = "temp"
                        if (cmd[16] ~= 0xff) then
                            json.b7_right_destination_temp = cmd[16] * 256 +
                                                                 cmd[17]
                        end
                    end
                    if (cmd[15] ~= 0xff) then
                        json.b7_right_gear = cmd[15]
                    end
                elseif (cmd[13] == 0x03) then
                    if (cmd[14] == 0x01) then
                        json.b7_middle_status = "power_off"
                    elseif (cmd[14] == 0x02) then
                        json.b7_middle_status = "working"
                    elseif (cmd[14] == 0x03) then
                        json.b7_middle_status = "power_off_delay"
                        if (cmd[16] ~= 0xff) then
                            json.b7_middle_destination_time = cmd[16] * 256 +
                                                                  cmd[17]
                            json.b7_middle_remaining_time =
                                json.b7_middle_destination_time
                        end
                    elseif (cmd[14] == 0x04) then
                        json.b7_middle_status = "temp"
                        if (cmd[16] ~= 0xff) then
                            json.b7_middle_destination_temp = cmd[16] * 256 +
                                                                  cmd[17]
                        end
                    end
                    if (cmd[15] ~= 0xff) then
                        json.b7_middle_gear = cmd[15]
                    end
                end
            end
        end
    elseif (cmd[10] == 0x03) then
        if (cmd[11] == 0x11 or cmd[11] == 0x31) then
            json = queryAllCmdToJson(json, cmd)
        elseif (cmd[11] == 0x32) then
            json = queryErrorCmdToJson(json, cmd)
        end
    elseif (cmd[10] == 0x04) then
        if (cmd[11] == 0x11 or cmd[11] == 0x41) then
            json = queryAllCmdToJson(json, cmd)
        elseif (cmd[11] == 0x0A and cmd[12] == 0xA1) then
            json = queryErrorCmdToJson(json, cmd)
        end
    elseif (cmd[10] == 0x0A and cmd[11] == 0xA1) then
        if (getBit(cmd[12], 2) == "1") then
            json["error_type"] = "sensor_error"
        end
        if (getBit(cmd[13], 0) == "1") then
            json["error_type"] = "hotclean_error"
        end
        if (getBit(cmd[13], 1) == "1") then
            json["error_type"] = "split_error"
        end
        if (cmd[14] ~= 0 or cmd[15] ~= 0) then
            json["error_type"] = "inverter_error"
        end
    end
    return json
end
local function makeSum(tmpbuf, start_pos, end_pos)
    local resVal = 0
    for si = start_pos, end_pos do resVal = resVal + tmpbuf[si] end
    resVal = bit.bnot(resVal) + 1
    resVal = bit.band(resVal, 0x00ff)
    return resVal
end
local function string2table(hexstr)
    local tb = {}
    local i = 1
    local j = 1
    for i = 1, #hexstr - 1, 2 do
        local doublebytestr = string.sub(hexstr, i, i + 1)
        tb[j] = tonumber(doublebytestr, 16)
        j = j + 1
    end
    return tb
end
local function string2hexstring(str)
    local ret = ""
    for i = 1, #str do ret = ret .. string.format("%02x", str:byte(i)) end
    return ret
end
local function table2string(cmd)
    local ret = ""
    local i
    for i = 1, #cmd do ret = ret .. string.char(cmd[i]) end
    return ret
end
function jsonToData(jsonCmdStr)
    if (#jsonCmdStr == 0) then return nil end
    local result
    if JSON == nil then JSON = require "cjson" end
    result = JSON.decode(jsonCmdStr)
    if result == nil then return end
    local msgBytes = {0xAA, 0x00, 0xB6, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}
    msgBytes = jsonToCmd(result, msgBytes)
    local len = #msgBytes
    msgBytes[2] = len
    msgBytes[len + 1] = makeSum(msgBytes, 2, len)
    local ret = table2string(msgBytes)
    ret = string2hexstring(ret)
    return ret
end
function dataToJson(jsonStr)
    if (not jsonStr) then return nil end
    local result
    if JSON == nil then JSON = require "cjson" end
    result = JSON.decode(jsonStr)
    if result == nil then return end
    local binData = result["msg"]["data"]
    local ret = {}
    ret["status"] = {}
    local bodyBytes = string2table(binData)
    ret["status"] = cmdToJson(ret["status"], bodyBytes)
    local ret = JSON.encode(ret)
    return ret
end

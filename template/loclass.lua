#!/usr/bin/env lua

local loclass_command =
    os.getenv("LOCLASS_COMMAND") or "loclass"

local function shell_quote(value)
    return "'" .. tostring(value):gsub("'", "'\"'\"'") .. "'"
end

local function normalize_execute_result(ok, _, code)
    if ok == true then
        return 0
    end

    if type(ok) == "number" then
        return ok
    end

    if type(code) == "number" then
        return code
    end

    return 1
end

local function run(command, quiet)
    if not quiet then
        io.write("> ", command, "\n")
        io.flush()
    end

    local ok, reason, code = os.execute(command)

    return normalize_execute_result(ok, reason, code)
end

local function command_exists(name)
    local command =
        "command -v "
        .. shell_quote(name)
        .. " >/dev/null 2>&1"

    return run(command, true) == 0
end

local function loclass_available()
    return run(
        shell_quote(loclass_command)
        .. " --help >/dev/null 2>&1",
        true
    ) == 0
end

local function doctor()
    local missing = {}

    if not loclass_available() then
        table.insert(missing, "loclass")
    end

    for _, command in ipairs({
        "jq",
        "latexmk",
        "pdflatex",
    }) do
        if not command_exists(command) then
            table.insert(missing, command)
        end
    end

    if #missing > 0 then
        io.stderr:write(
            "Fehlende Voraussetzungen: ",
            table.concat(missing, ", "),
            "\n"
        )

        return 1
    end

    print("Alle Voraussetzungen sind vorhanden.")
    print("loclass: " .. loclass_command)

    return 0
end

local function build()
    local status = doctor()

    if status ~= 0 then
        return status
    end

    status = run("mkdir -p -- build content project")

    if status ~= 0 then
        return status
    end

    return run(
        "latexmk "
        .. "-pdf "
        .. "-interaction=nonstopmode "
        .. "-halt-on-error "
        .. "main.tex"
    )
end

local function build_odt()
    if not loclass_available() then
        io.stderr:write("loclass wurde nicht gefunden.\n")
        return 1
    end

    local status = run("mkdir -p -- build")

    if status ~= 0 then
        return status
    end

    return run(
        shell_quote(loclass_command)
        .. " convert "
        .. shell_quote("main.ldl")
        .. " --backend odt --output "
        .. shell_quote("build/document.odt")
    )
end

local function clean()
    local latexmk_status = 0

    if command_exists("latexmk") then
        latexmk_status = run(
            "LOCLASS_SKIP_PREBUILD=1 "
            .. "latexmk -C main.tex"
        )
    end

    local cleanup_status = run(
        "rm -rf -- "
        .. "build/loclass "
        .. "loclass-assets "
        .. "&& rm -f -- "
        .. "content/10_document.tex "
        .. "project/metadata.tex "
        .. "project/metadata.tex.tmp"
    )

    if latexmk_status ~= 0 then
        return latexmk_status
    end

    return cleanup_status
end

local function build_all()
    local status = build()

    if status ~= 0 then
        return status
    end

    return build_odt()
end

local function usage()
    print([[
loclass document runner

Verwendung:
  ./loclass.lua build
  ./loclass.lua odt
  ./loclass.lua all
  ./loclass.lua clean
  ./loclass.lua doctor
]])
end

local actions = {
    build = build,
    odt = build_odt,
    all = build_all,
    clean = clean,
    doctor = doctor,
}

local action = arg[1] or "build"
local handler = actions[action]

if not handler then
    usage()
    os.exit(2)
end

os.exit(handler())

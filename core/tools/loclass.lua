#!/usr/bin/env lua

--------------------------------------------------
-- Configuration
--------------------------------------------------

local VERSION = "0.1.0"

--------------------------------------------------
-- Utilities
--------------------------------------------------

local function shell_quote(value)
	return "'" .. tostring(value):gsub("'", "'\\''") .. "'"
end

local function file_exists(path)
	local file = io.open(path, "r")

	if file == nil then
		return false
	end

	file:close()
	return true
end

local function fail(message, exit_code)
	io.stderr:write("Error: " .. message .. "\n")
	os.exit(exit_code or 1)
end

local function run(command, background)
	print()
	print("----------------------------------------")
	print("> " .. command)
	print("----------------------------------------")

	if background then
		command = command .. " >/dev/null 2>&1 &"
	end

	local ok, exit_kind, exit_code = os.execute(command)

	if ok == true or ok == 0 then
		return
	end

	if exit_kind ~= nil and exit_code ~= nil then
		fail(
			"command failed with "
				.. tostring(exit_kind)
				.. " status "
				.. tostring(exit_code)
		)
	end

	fail("command failed")
end

--------------------------------------------------
-- Document paths
--------------------------------------------------

local function require_ldl_path(path)
	if path == nil or path == "" then
		fail("missing LDL document", 2)
	end

	if not path:match("%.ldl$") then
		fail("expected a .ldl file: " .. path, 2)
	end

	if not file_exists(path) then
		fail("LDL document not found: " .. path, 2)
	end

	return path
end

local function pdf_path_for(path)
	local filename = path:match("([^/]+)%.ldl$")

	if filename == nil then
		fail("unable to determine PDF filename", 2)
	end

	return "build/" .. filename .. ".pdf"
end

--------------------------------------------------
-- Commands
--------------------------------------------------

local function build(path)
	path = require_ldl_path(path)

	run(
		"uv run loclass-pdf "
			.. shell_quote(path)
	)
end

local function open_pdf(path)
	path = require_ldl_path(path)

	local pdf = pdf_path_for(path)

	if not file_exists(pdf) then
		fail(
			"PDF not found: "
				.. pdf
				.. "\nBuild the document first."
		)
	end

	run(
		"xdg-open " .. shell_quote(pdf),
		true
	)
end

local function clean()
	run("rm -rf build")
end

--------------------------------------------------
-- Help
--------------------------------------------------

local function help()
	print("loclass " .. VERSION)
	print()
	print("Usage:")
	print("  loclass <command> [document.ldl]")
	print()
	print("Commands:")
	print("  build <file.ldl>   Build an LDL document as PDF")
	print("  ldl <file.ldl>     Alias for build")
	print("  open <file.ldl>    Open the generated PDF")
	print("  clean              Remove generated build files")
	print("  version            Show version")
	print("  help               Show this help")
end

--------------------------------------------------
-- Main
--------------------------------------------------

local commands = {
	build = build,
	ldl = build,
	open = open_pdf,
	clean = clean,
}

local function main()
	local command_name = arg[1]

	if command_name == nil
		or command_name == "--help"
		or command_name == "help"
	then
		help()
		return
	end

	if command_name == "--version"
		or command_name == "version"
	then
		print("loclass " .. VERSION)
		return
	end

	local command = commands[command_name]

	if command == nil then
		io.stderr:write(
			"Unknown command: "
				.. tostring(command_name)
				.. "\n\n"
		)
		help()
		os.exit(2)
	end

	command(arg[2])
end

main()

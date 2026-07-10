#!/usr/bin/env lua

--------------------------------------------------
-- Configuration
--------------------------------------------------

local BUILD_COMMAND = "latexmk"
local CLEAN_COMMAND = "latexmk -C"
local WATCH_COMMAND = "latexmk -pvc"

local PDF = "build/main.pdf"

local LDL_PDF_TOOL = "core/tools/ldl_pdf.py"
local LDL_FORMAT_TOOL = "core/tools/ldl_format.py"

local VERSION = "0.1.0"

--------------------------------------------------
-- Shell
--------------------------------------------------

local function run(command, background)
	print()
	print("----------------------------------------")
	print("> " .. command)
	print("----------------------------------------")

	if background then
		command = command .. " >/dev/null 2>&1 &"
	end

	return os.execute(command)
end

local function shell_quote(value)
	return "'" .. tostring(value):gsub("'", "'\\''") .. "'"
end

--------------------------------------------------
-- Validation
--------------------------------------------------

local function validate_ldl_path(path)
	if path == nil or path == "" then
		print("Error: missing LDL file")
		return false
	end

	if not path:match("%.ldl$") then
		print("Error: expected a .ldl file")
		return false
	end

	return true
end

--------------------------------------------------
-- Standard Commands
--------------------------------------------------

local function build()
	run(BUILD_COMMAND)
end

local function clean()
	run(CLEAN_COMMAND)
end

local function rebuild()
	clean()
	build()
end

local function watch()
	run(WATCH_COMMAND)
end

local function open()
	run("xdg-open " .. shell_quote(PDF), true)
end

--------------------------------------------------
-- LDL Commands
--------------------------------------------------

local function build_ldl(path)
	if not validate_ldl_path(path) then
		print("Usage: loclass ldl <file.ldl>")
		return
	end

	run("uv run python " .. shell_quote(LDL_PDF_TOOL) .. " " .. shell_quote(path))
end

local function format_ldl(path)
	if not validate_ldl_path(path) then
		print("Usage: loclass ldl format <file.ldl>")
		return
	end

	run("uv run python " .. shell_quote(LDL_FORMAT_TOOL) .. " " .. shell_quote(path))
end

local function check_ldl(path)
	if not validate_ldl_path(path) then
		print("Usage: loclass ldl check <file.ldl>")
		return
	end

	run("uv run python " .. shell_quote(LDL_FORMAT_TOOL) .. " --check " .. shell_quote(path))
end

local function print_ldl(path)
	if not validate_ldl_path(path) then
		print("Usage: loclass ldl stdout <file.ldl>")
		return
	end

	run("uv run python " .. shell_quote(LDL_FORMAT_TOOL) .. " --stdout " .. shell_quote(path))
end

local function ldl(action, path)
	if action == nil or action == "" then
		print("Usage:")
		print("  loclass ldl <file.ldl>")
		print("  loclass ldl format <file.ldl>")
		print("  loclass ldl check <file.ldl>")
		print("  loclass ldl stdout <file.ldl>")
		return
	end

	-- Preserve the existing command:
	-- loclass ldl document.ldl
	if action:match("%.ldl$") then
		build_ldl(action)
		return
	end

	local actions = {
		build = build_ldl,
		format = format_ldl,
		check = check_ldl,
		stdout = print_ldl,
	}

	local command = actions[action]

	if not command then
		print("Unknown LDL command: " .. tostring(action))
		print()
		print("Available LDL commands:")
		print("  build")
		print("  format")
		print("  check")
		print("  stdout")
		return
	end

	command(path)
end

--------------------------------------------------
-- Command Dispatcher
--------------------------------------------------

local commands = {
	build = build,
	rebuild = rebuild,
	clean = clean,
	watch = watch,
	open = open,
	ldl = ldl,
}

local function execute(name, ...)
	local command = commands[name]

	if not command then
		print("Unknown command: " .. tostring(name))
		return
	end

	command(...)
end

--------------------------------------------------
-- Menu
--------------------------------------------------

local menu_items = {
	{ name = "build", label = "Build" },
	{ name = "rebuild", label = "Rebuild" },
	{ name = "clean", label = "Clean" },
	{ name = "watch", label = "Watch" },
	{ name = "open", label = "Open PDF" },
}

local function menu()
	while true do
		print()
		print("========================================")
		print("             loclass Tools")
		print("========================================")
		print()

		for i, item in ipairs(menu_items) do
			print(i .. ") " .. item.label)
		end

		print(#menu_items + 1 .. ") Quit")
		print()

		io.write("Selection: ")

		local choice = io.read()
		local index = tonumber(choice)

		if not index then
			print("Invalid selection.")
		elseif index == #menu_items + 1 then
			return
		elseif menu_items[index] then
			execute(menu_items[index].name)
		else
			print("Unknown selection.")
		end
	end
end

--------------------------------------------------
-- Help
--------------------------------------------------

local function help()
	print("loclass " .. VERSION)
	print()
	print("Usage:")
	print("  loclass <command>")
	print()
	print("Commands:")
	print("  build                         Build the document")
	print("  rebuild                       Clean and rebuild")
	print("  clean                         Remove build artifacts")
	print("  watch                         Continuous build")
	print("  open                          Open generated PDF")
	print("  ldl <file.ldl>                Build an LDL document as PDF")
	print("  ldl build <file.ldl>          Build an LDL document as PDF")
	print("  ldl format <file.ldl>         Format an LDL document")
	print("  ldl check <file.ldl>          Check LDL formatting")
	print("  ldl stdout <file.ldl>         Print formatted LDL")
	print("  version                       Show version")
	print("  help                          Show this help")
	print()
	print("Without arguments an interactive menu is shown.")
end

--------------------------------------------------
-- Version
--------------------------------------------------

local function version()
	print("loclass " .. VERSION)
end

--------------------------------------------------
-- Main
--------------------------------------------------

local function main()
	if arg[1] == "--help" or arg[1] == "help" then
		help()
		return
	end

	if arg[1] == "--version" or arg[1] == "version" then
		version()
		return
	end

	if #arg > 0 then
		execute(arg[1], arg[2], arg[3])
		return
	end

	menu()
end

main()

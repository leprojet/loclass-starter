#!/usr/bin/env lua

--------------------------------------------------
-- Configuration
--------------------------------------------------

local BUILD_COMMAND = "latexmk"
local CLEAN_COMMAND = "latexmk -C"
local WATCH_COMMAND = "latexmk -pvc"

local PDF = "build/main.pdf"

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
-- Commands
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

local function render_ldl(path)
	if path == nil or path == "" then
		print("Usage: loclass ldl <file.ldl>")
		return
	end

	if not path:match("%.ldl$") then
		print("Error: expected a .ldl file")
		return
	end

	run("uv run python core/tools/ldl_pdf.py " .. shell_quote(path))
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
	ldl = render_ldl,
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
	print("  build              Build the document")
	print("  rebuild            Clean and rebuild")
	print("  clean              Remove build artifacts")
	print("  watch              Continuous build")
	print("  open               Open generated PDF")
	print("  ldl <file.ldl>     Build a complete LDL document as PDF")
	print("  version            Show version")
	print("  help               Show this help")
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
		execute(arg[1], arg[2])
		return
	end

	menu()
end

main()

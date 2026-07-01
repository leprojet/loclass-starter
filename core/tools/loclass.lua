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

local function run(command)
	print()
	print("----------------------------------------")
	print("> " .. command)
	print("----------------------------------------")

	os.execute(command)

	print()
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
	run("xdg-open " .. PDF)
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
}

local function execute(name)
	local command = commands[name]

	if not command then
		print("Unknown command: " .. tostring(name))
		return
	end

	command()
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
	print("  build      Build the document")
	print("  rebuild    Clean and rebuild")
	print("  clean      Remove build artifacts")
	print("  watch      Continuous build")
	print("  open       Open generated PDF")
	print("  version    Show version")
	print("  help       Show this help")
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
		execute(arg[1])
		return
	end

	menu()
end
main()

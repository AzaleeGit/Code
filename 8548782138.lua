local Rayfield = loadstring(game:HttpGet('https://sirius.menu/rayfield'))()

local MAIN = Rayfield:CreateWindow({
	Name = "TheGame",
	Icon = 0, -- Icon in Topbar. Can use Lucide Icons (string) or Roblox Image (number). 0 to use no icon (default).
	LoadingTitle = "LOADING THE HUB",
	LoadingSubtitle = "by EElAZA",
	Theme = "DarkBlue", -- Check https://docs.sirius.menu/rayfield/configuration/themes

	DisableRayfieldPrompts = false,
	DisableBuildWarnings = false, -- Prevents Rayfield from warning when the script has a version mismatch with the interface

	ConfigurationSaving = {
		Enabled = false,
		FolderName = nil, -- Create a custom folder for your hub/game
		FileName = "Big Hub"
	},

	Discord = {
		Enabled = false, -- Prompt the user to join your Discord server if their executor supports it
		Invite = "noinvitelink", -- The Discord invite code, do not include discord.gg/. E.g. discord.gg/ ABCD would be ABCD
		RememberJoins = true -- Set this to false to make them join the discord every time they load it up
	},

	KeySystem = false, -- Set this to true to use our key system
	KeySettings = {
		Title = "Untitled",
		Subtitle = "Key System",
		Note = "No method of obtaining the key is provided", -- Use this to tell the user how to get a key
		FileName = "Key", -- It is recommended to use something unique as other scripts using Rayfield may overwrite your key file
		SaveKey = true, -- The user's key will be saved, but if you change the key, they will be unable to use your script
		GrabKeyFromSite = false, -- If this is true, set Key below to the RAW site you would like Rayfield to get the key from
		Key = {"Hello"} -- List of keys that will be accepted by the system, can be RAW file links (pastebin, github etc) or simple strings ("hello","key22")
	}
})

--VALUE--
getgenv().auto_tap = false
local _player = game:GetService("Players").LocalPlayer
--FUNCTIONS--
local function auto_click()
	while getgenv().auto_tap == true do
		game:GetService("ReplicatedStorage"):WaitForChild("TappingRemote"):WaitForChild("Tap"):FireServer()
		wait(1)
	end
end

--WINDOW--
local Farm = MAIN:CreateTab("Farming", 4483362458) --Creating a window
local developement = MAIN:CreateTab("Developement", 4483362458) --Creating a window

local Section_Farm = Farm:CreateSection("Farm")
--FARM TAB--a
--FARM SECTION--
local toggle_autoClick = Farm:CreateToggle({
	Name = "Auto_Click",
	CurrentValue = false,
	Flag = "Toggle1", -- A flag is the identifier for the configuration file, make sure every element has a different flag if you're using configuration saving to ensure no overlaps
	Callback = function(Value)
		getgenv().auto_tap = Value
		auto_click()
	end,
})


--DEVELOPEMENT TAB--
local button_UpdateHUB = developement:CreateButton({
	Name = "UpdateHUB",
	Callback = function()
		loadstring(game:HttpGet("https://raw.githubusercontent.com/AzaleeGit/Code/refs/heads/main/8548782138.lua"))()
		Rayfield:Destroy()
	end,
})

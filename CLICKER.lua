local Rayfield = loadstring(game:HttpGet('https://sirius.menu/rayfield'))()

local Window = Rayfield:CreateWindow({
	Name = "ClickerGame",
	Icon = 0, -- Icon in Topbar. Can use Lucide Icons (string) or Roblox Image (number). 0 to use no icon (default).
	LoadingTitle = "Loading HUB",
	LoadingSubtitle = "by EElAZA",
	Theme = "DarkBlue", -- Check https://docs.sirius.menu/rayfield/configuration/themes

	DisableRayfieldPrompts = false,
	DisableBuildWarnings = true, -- Prevents Rayfield from warning when the script has a version mismatch with the interface

	ConfigurationSaving = {
		Enabled = true,
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
_G.auto_tap = false
_G.auto_rebirth = false
_G.rebirth_amount = 1
local _player = game:GetService("Players").LocalPlayer
--FUNCTIONS--
function autoClick()
	while _G.auto_tap == true do
		game:GetService("ReplicatedStorage"):WaitForChild("Aero"):WaitForChild("AeroRemoteServices"):WaitForChild("ClickService"):WaitForChild("Click"):FireServer(9999)
		task.wait()
	end
end

function Rebirth()
	while _G.auto_rebirth == true do
		game:GetService("ReplicatedStorage"):WaitForChild("Aero"):WaitForChild("AeroRemoteServices"):WaitForChild("RebirthService"):WaitForChild("BuyRebirths"):FireServer(_G.rebirth_amount)
		task.wait()
	end
	
end

--CREATING TAB--

local Farm = Window:CreateTab("Farming", 4483362458) --Creating a window
local developement = Window:CreateTab("Developement", 4483362458) --Creating a window

local Section_Click = Farm:CreateSection("Farm")

local Toggle_Click = Farm:CreateToggle({
	Name = "Auto_Click",
	CurrentValue = false,
	Flag = "Toggle1", -- A flag is the identifier for the configuration file, make sure every element has a different flag if you're using configuration saving to ensure no overlaps
	Callback = function(Value)
		_G.auto_tap = Value
		autoClick()
	end,
})

local Section_Rebirth = Farm:CreateSection("Rebirth")

local Dropdown_Rebirth = Farm:CreateDropdown({
	Name = "Select Auto_Rebirth Amount",
	Options = {"1","10","100", "1000", "10000"},
	CurrentOption = {"1"},
	MultipleOptions = false,
	Flag = "Dropdown1", -- A flag is the identifier for the configuration file, make sure every element has a different flag if you're using configuration saving to ensure no overlaps
	Callback = function(Options)
		_G.rebirth_amount = Options[1]
		Rebirth()
	end,
})

local Toggle_Rebirth = Farm:CreateToggle({
	Name = "Auto_Rebirth",
	CurrentValue = false,
	Flag = "Toggle2", -- A flag is the identifier for the configuration file, make sure every element has a different flag if you're using configuration saving to ensure no overlaps
	Callback = function(Value)
		_G.auto_rebirth = Value
		Rebirth()
	end,
})


local button_UpdateHUB = developement:CreateButton({
	Name = "UpdateHUB",
	Callback = function()
		loadstring(game:HttpGet("https://raw.githubusercontent.com/AzaleeGit/Code/refs/heads/main/CLICKER.lua"))()
		Rayfield:Destroy()
	end,
})

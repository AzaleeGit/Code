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
getgenv().amount_rebirth = "1"
getgenv().auto_rebirth = false
getgenv().egg_toHatch = nil
getgenv().auto_hatch = false

local _player = game:GetService("Players").LocalPlayer
--FUNCTIONS--
function auto_click()
	while task.wait(0.000000001) do
		if getgenv().auto_tap == true then
			game:GetService("ReplicatedStorage"):WaitForChild("TappingRemote"):WaitForChild("Tap"):FireServer()
		end
	end
end

function rebirth()
	while task.wait(1) do
		if getgenv().auto_rebirth == true then
			game:GetService("ReplicatedStorage"):WaitForChild("Rebirth"):FireServer(tonumber(getgenv().amount_rebirth))
		end
	end
end

function auto_hatch()
	while getgenv().auto_hatch == true do
		game:GetService("ReplicatedStorage"):WaitForChild("EggHatchingRemote"):WaitForChild("HatchServer"):InvokeServer(getgenv().egg_toHatch)
		task.wait()
	end
end


--WINDOW--
local Farm = MAIN:CreateTab("Farming", 4483362458) --Creating a window
local developement = MAIN:CreateTab("Developement", 4483362458) --Creating a window


--FARM TAB--
--FARM SECTION--
local Section_Farm = Farm:CreateSection("Farm")

local toggle_autoClick = Farm:CreateToggle({
	Name = "Auto_Click",
	CurrentValue = false,
	Flag = "Toggle1", -- A flag is the identifier for the configuration file, make sure every element has a different flag if you're using configuration saving to ensure no overlaps
	Callback = function(Value)
		getgenv().auto_tap = Value
		auto_click()
	end,
})

local input_rebirth = Farm:CreateInput({
	Name = "Enter Auto_Rebirth Amount",
	CurrentValue = "",
	PlaceholderText = "rebirth",
	RemoveTextAfterFocusLost = false,
	Flag = "Input1",
	Callback = function(Text)
		local isNumber = tonumber(Text)
		if not isNumber then return end
		getgenv().amount_rebirth = Text
		rebirth()
	end,
})

local toggle_autoRebirth = Farm:CreateToggle({
	Name = "Auto_Rebirth",
	CurrentValue = false,
	Flag = "Toggle2", -- A flag is the identifier for the configuration file, make sure every element has a different flag if you're using configuration saving to ensure no overlaps
	Callback = function(Value)
		getgenv().auto_rebirth = Value
		rebirth()
	end,
})

--EGG SECTION--
local Section_Egg = Farm:CreateSection("Egg")

local dropdown_egg  = Farm:CreateDropdown({
	Name = "Egg to hatch",
	Options = {"Basic Egg", "Beach Egg", "Winter Egg", "Candy Egg", "Ninja Egg", "Atlantis Egg", "Lab Egg", "Jungle Egg", "Lucid Egg", "VIP Egg", "Lava Egg", "Magic Egg", "Mega Egg", "Mega Space Egg", "Brainrot Egg", "Overseer Egg", "Space Merchant Egg"},
	CurrentOption = {"Basic Egg"},
	MultipleOptions = false,
	Flag = "Dropdown1", -- A flag is the identifier for the configuration file, make sure every element has a different flag if you're using configuration saving to ensure no overlaps
	Callback = function(Options)
		local findEgg = workspace:WaitForChild("Eggs"):WaitForChild(Options[1])
		if not findEgg then return end
		getgenv().egg_toHatch = findEgg
		auto_hatch()
	end,
})

local toggle_autoHatch = Farm:CreateToggle({
	Name = "Auto_hatch",
	CurrentValue = false,
	Flag = "Toggle3", -- A flag is the identifier for the configuration file, make sure every element has a different flag if you're using configuration saving to ensure no overlaps
	Callback = function(Value)
		getgenv().auto_hatch = Value
		auto_hatch()
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

local button_KillScript = developement:CreateButton({
	Name = "KillScript",
	CallBack = function()
		Rayfield:Destroy()
	end,
})

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
_G.a_click = false
_G.a_collect = false
local _player = game:GetService("Players").LocalPlayer
--FUNCTIONS--
function CollectGems()
	local Gems = game.Workspace.Gems:GetChildren()
	if not Gems then return end
	while _G.a_collect == true do
		for i, v in pairs(Gems) do
			local isMesh = v:IsA("MeshPart")
			local hasTouchInterest = v:FindFirstChild("TouchInterest")
			if not isMesh or not hasTouchInterest then continue end

			if _G.a_collect == true then
				_player.Character.HumanoidRootPart.CFrame = v.CFrame + Vector3.new(0, 5, 0)
			end 
			wait(.5)
		end
	end
end

function Click()
	while _G.a_click == true do
		game:GetService("ReplicatedStorage").Tap:InvokeServer(true)
	end
end

--CREATING TAB--

local Farm = Window:CreateTab("Farming", 4483362458) --Creating a window

local Clicking = Farm:CreateSection("Click") -- a Tab

local Button = Clicking:CreateButton({
	Name = "Button Example",
	Callback = function()
		game:GetService("ReplicatedStorage"):WaitForChild("Packages"):WaitForChild("Knit"):WaitForChild("TaskService"):WaitForChild("RF"):WaitForChild("ClaimReward"):InvokeServer("Coins", 2)
	end,
})

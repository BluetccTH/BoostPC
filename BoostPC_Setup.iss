; ===========================
; BoostPC_Setup.iss
; ===========================

[Setup]
AppName=BoostPC
AppVersion=1.0
DefaultDirName={pf}\BoostPC
DefaultGroupName=BoostPC
DisableProgramGroupPage=yes
OutputDir=installer_output
OutputBaseFilename=BoostPC_Setup
Compression=lzma
SolidCompression=yes
AllowNoIcons=yes
ChangesAssociations=no
PrivilegesRequired=admin
WizardStyle=modern

; ===========================
; Languages
; ===========================
[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

; ===========================
; Tasks
; ===========================
[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked

; ===========================
; Files
; ===========================
[Files]
; Main executable
Source: "dist\BoostPC.exe"; DestDir: "{app}"; Flags: ignoreversion
; Config backup (ถ้ามี)
Source: "config\*"; DestDir: "{app}\config"; Flags: recursesubdirs createallsubdirs
; Modules
Source: "modules\*"; DestDir: "{app}\modules"; Flags: recursesubdirs createallsubdirs

; ===========================
; Icons
; ===========================
[Icons]
Name: "{group}\BoostPC"; Filename: "{app}\BoostPC.exe"
Name: "{commondesktop}\BoostPC"; Filename: "{app}\BoostPC.exe"; Tasks: desktopicon

; ===========================
; Uninstall
; ===========================
[UninstallDelete]
Type: filesandordirs; Name: "{app}\*"

; ===========================
; Run after install
; ===========================
[Run]
Filename: "{app}\BoostPC.exe"; Description: "Launch BoostPC"; Flags: nowait postinstall skipifsilent

; ===========================
; RestartReplace
; ===========================
[Files]
Source: "dist\BoostPC.exe"; DestDir: "{app}"; Flags: restartreplace
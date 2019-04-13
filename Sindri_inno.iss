; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{D3900E38-79E3-4D50-A50F-8C35F71529F0}
AppName=Sindri
AppVersion=1.0.0
;AppVerName=Sindri 1.0.0
AppPublisher=Marcus Bruno Fernandes Silva
AppPublisherURL=https://github.com/mrcsbrn/Sindri
AppSupportURL=https://github.com/mrcsbrn/Sindri
AppUpdatesURL=https://github.com/mrcsbrn/Sindri
DefaultDirName={pf}\Sindri
DisableProgramGroupPage=yes
OutputBaseFilename=Sindri
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Dirs]
Name: {app}; Permissions: users-full

[Files]
Source: ".\Sindri\Sindri.exe"; DestDir: "{app}"; Flags: ignoreversion; Permissions: everyone-full
Source: ".\Sindri\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Permissions: everyone-full
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{commonprograms}\Sindri"; Filename: "{app}\Sindri.exe"
Name: "{commondesktop}\Sindri"; Filename: "{app}\Sindri.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\Sindri.exe"; Description: "{cm:LaunchProgram,Sindri}"; Flags: nowait postinstall skipifsilent


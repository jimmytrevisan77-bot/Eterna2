; Inno Setup configuration for the Eterna2 local desktop suite
[Setup]
AppName=Eterna2
AppVersion=3.1
DefaultDirName={pf64}\\Eterna2
DefaultGroupName=Eterna2
UninstallDisplayIcon={app}\\Eterna2.exe
OutputDir=dist
OutputBaseFilename=Eterna2Setup
Compression=lzma2
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64

[Files]
Source: "..\\frontend\\bin\\Release\\net8.0-windows\\win10-x64\\publish\\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion
Source: "..\\backend\\*"; DestDir: "{app}\\backend"; Flags: recursesubdirs createallsubdirs
Source: "..\\Config\\*"; DestDir: "{app}\\Config"; Flags: recursesubdirs createallsubdirs
Source: "..\\assets\\logo.png"; DestDir: "{app}\\assets"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\\Eterna2"; Filename: "{app}\\Eterna2.exe"

[Run]
Filename: "{app}\\installers\\check_dependencies.py"; Description: "Verify runtime dependencies"; Flags: shellexec runhidden

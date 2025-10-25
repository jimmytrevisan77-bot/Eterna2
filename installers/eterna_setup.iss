; Inno Setup script for Eterna2 local deployment

[Setup]
AppName=Eterna2
AppVersion=0.6
DefaultDirName={pf64}\Eterna2
OutputDir=dist
OutputBaseFilename=Eterna2Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "..\frontend\bin\Release\net8.0-windows\*"; DestDir: "{app}"; Flags: recursesubdirs
Source: "..\backend\*"; DestDir: "{app}\backend"; Flags: recursesubdirs
Source: "..\Config\*"; DestDir: "{app}\Config"; Flags: recursesubdirs
Source: "..\assets\*"; DestDir: "{app}\assets"; Flags: recursesubdirs

[Run]
Filename: "{app}\Eterna.Desktop.exe"; Description: "Launch Eterna2"; Flags: nowait postinstall skipifsilent

Option Explicit

Function SelectFolder( myStartFolder )
    ' Standard housekeeping
    Dim objFolder, objItem, objShell
    
    ' Custom error handling
    On Error Resume Next
    SelectFolder = vbNull

    ' Create a dialog object
    Set objShell  = CreateObject( "Shell.Application" )
    Set objFolder = objShell.BrowseForFolder( 0, "Select Folder", 0, myStartFolder )

    ' Return the path of the selected folder
    If IsObject( objfolder ) Then SelectFolder = objFolder.Self.Path

    ' Standard housekeeping
    Set objFolder = Nothing
    Set objshell  = Nothing
    On Error Goto 0
End Function

Dim fso, folder, folders, subfolders, folderPath, files, file, filename, filenametemp, fileext, renamecount, Output, copyFolder, convertYN, preFix
Dim i

'=========================이부분부터 변경 시작=================================================
folderPath = SelectFolder( "" )
folderPath = "C:\Users\tshwang\Documents\VSCODE\WM"
If folderPath = vbNull Then
    WScript.Echo "Cancelled"
'Else
'    WScript.Echo "Selected Folder: """ & folderPath & """"
End If

'folderPath = "D:\temp"	 '원본 파일이 들어있는 폴더명
copyFolder = folderPath & "\3D_OUT"	'변환한 파일이 들어갈 폴더명 - 원본이 있는 폴더와 중복되지 않게 설정
'preFix = "img_"	'파일명 프리픽스 img_ 로 설정시 img_0001.jpg 형식으로 리네임됨
'=========================이부분까지 변경======================================================

Set fso = CreateObject("Scripting.FileSystemObject")
'Set Output = WScript.stdout

	Set folders = fso.GetFolder(folderPath & "\3D")
	Set subfolders = folders.SubFolders
	Set 
	
	i = 1
	renamecount = 0

	'WScript.Echo filenametemp
	Dim folders2, subfolders2, folders3, subfolders3, files3
	If fso.FolderExists(folderPath & "\" & "3D_LANDMARK") Then
		Set folders2 = fso.GetFolder(folderPath & "\3D_LANDMARK")
		Set subfolders2 = folders2.SubFolders
		If subfolders.count = 1 Then
			For Each folder In subfolders2
				Set folders3 = fso.GetFolder(folder.path)
				Set subfolders3 = folders3.SubFolders
				Set files3 = folders3.Files
				For Each file In files3
					WScript.Echo file.name
					file.Copy (copyFolder & "\" & filenametemp)
				Next
			Next
		Else
			WScript.Echo "Too many subfolders or no folder under 3D.   Script stopped."
		End If
	End If

Set fso = Nothing
Set Output = Nothing
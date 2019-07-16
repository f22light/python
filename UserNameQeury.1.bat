@Echo off

setlocal EnableExtensions EnableDelayedExpansion

set errstr=The user name could not be found.
echo "System","User ID","User Name"> result.csv
for /f "skip=1 tokens=1,3 delims=," %%a in (global_table_data_export.csv) do (  
    for /f "tokens=2 delims=\" %%s in (%%b) do (
        for /f "tokens=* delims=" %%i in ('net user %%s /domain 2^>^&1 ^| Findstr /c:"Full Name" /c:"%errstr%"') do (
            if "%%i"=="%errstr%" (
                echo %%a,"%%s","#N/A">> result.csv
            ) else (
                set x=%%i
                echo %%a,"%%s","!x:~29!">> result.csv
            )
        )
    )
)
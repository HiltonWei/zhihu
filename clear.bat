    :: file: �����ʱ�����ļ�.bat  
    :: purpose: �����ʱ�����ļ�  
    :: author: xue  
    :: time:2015.07.17  
      

    del *.pyc /S
	 
    

	
    @for /F "delims=" %%i in ('dir *.obj /S /B^|find "\Release\"') do del "%%i"  
    @for /F "delims=" %%i in ('dir *.obj /S /B^|find "\Debug\"') do del "%%i" 
    @for /f "delims=" %%i in ('dir /S /B /AD^|find "\Release"' ) do rd /q "%%i"  
    @for /f "delims=" %%i in ('dir /S /B /AD^|find "\Debug"' ) do rd /q "%%i"  
$this = split-path -parent $MyInvocation.MyCommand.Definition
$old_path = $Env:PATH
$old_python_path = $Env:PYTHONPATH
$Env:PATH = $this\latest\bin;$this\latest\python\Scripts;$old_path
$Env:PYTHONPATH = $this\latest\lib;$old_python_path

py_entry_point="$this\latest\bin\construct.bat"
& $py_entry_point $args

$Env:PYTHONPATH=$old_python_path
$Env:PATH=$old_path
Remove-Variable py_entry_point
Remove-Variable old_python_path
Remove-Variable old_path
Remove-Variable this
